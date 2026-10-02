import logging

import stripe

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from homepage.models.school import Schoolcontexts
from homepage.models.school_chapter import Chapter
from homepage.models.topics import Topics
from homepage.models.user_purchases import UserPurchase
from homepage.models.topic_purchases import TopicPurchase


logger = logging.getLogger(__name__)

User = get_user_model()


def register_stripe_purchase(session):

    # Επεξεργαζόμαστε μόνο ολοκληρωμένες πληρωμές.
    if session.get("payment_status") != "paid":
        return

    metadata = session.get("metadata") or {}

    user_id = metadata.get("user_id")
    purchase_type = metadata.get("purchase_type")
    session_id = session.get("id")
    amount_paid = session.get("amount_total")

    if (
        not user_id
        or not session_id
        or amount_paid is None
        or purchase_type not in ("book", "chapter", "topic")
    ):
        raise ValueError("Invalid Stripe purchase information")

    user = User.objects.get(pk=user_id)

    # ==========================================
    # ΑΓΟΡΑ TOPIC
    # ==========================================

    if purchase_type == "topic":

        topic_id = metadata.get("topic_id")

        if not topic_id:
            raise ValueError("Missing topic_id")

        topic = Topics.objects.get(pk=topic_id)

        existing_purchase = TopicPurchase.objects.filter(
            stripe_session_id=session_id,
        ).first()

        if existing_purchase:
            if (
                existing_purchase.user_id != user.pk
                or existing_purchase.topic_id != topic.pk
            ):
                raise ValueError("Stripe session purchase mismatch")

            return

        # Αποφυγή δεύτερης αγοράς του ίδιου Topic.
        existing_purchase = TopicPurchase.objects.filter(
            user=user,
            topic=topic,
        ).first()

        if existing_purchase:
            logger.error(
                "Additional paid Topic transaction requires review: "
                "user=%s topic=%s session=%s",
                user.pk,
                topic.pk,
                session_id,
            )
            return

        try:
            TopicPurchase.objects.create(
                user=user,
                topic=topic,
                stripe_session_id=session_id,
                amount_paid=amount_paid,
            )

        except IntegrityError:
            # Πιθανή ταυτόχρονη καταχώριση από pay_success.
            existing_purchase = TopicPurchase.objects.filter(
                stripe_session_id=session_id,
                user=user,
                topic=topic,
            ).exists()

            if not existing_purchase:
                raise

        return

    # ==========================================
    # ΑΓΟΡΑ ΒΙΒΛΙΟΥ Ή ΚΕΦΑΛΑΙΟΥ
    # ==========================================

    book_id = metadata.get("book_id")

    if not book_id:
        raise ValueError("Missing book_id")

    book = Schoolcontexts.objects.get(pk=book_id)

    chapter = None

    if purchase_type == "chapter":

        chapter_id = metadata.get("chapter_id")

        if not chapter_id:
            raise ValueError("Missing chapter_id")

        chapter = Chapter.objects.get(
            pk=chapter_id,
            context=book,
        )

    purchase, created = UserPurchase.objects.get_or_create(
        stripe_session_id=session_id,
        defaults={
            "user": user,
            "book": book,
            "chapter": chapter,
            "amount_paid": amount_paid,
        },
    )

    if (
        purchase.user_id != user.pk
        or purchase.book_id != book.pk
        or purchase.chapter_id != (
            chapter.pk if chapter else None
        )
    ):
        raise ValueError("Stripe session purchase mismatch")


@csrf_exempt
def stripe_webhook(request):

    if request.method != "POST":
        return HttpResponse(status=405)

    webhook_secret = getattr(
        settings,
        "STRIPE_WEBHOOK_SECRET",
        None,
    )

    if not webhook_secret:
        logger.error("Stripe webhook secret is missing")
        return HttpResponse(status=500)

    payload = request.body
    signature = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(
            payload,
            signature,
            webhook_secret,
        )

    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)

    if event["type"] in (
        "checkout.session.completed",
        "checkout.session.async_payment_succeeded",
    ):

        session = event["data"]["object"]

        try:
            register_stripe_purchase(session)

        except Exception:
            logger.exception(
                "Stripe webhook purchase registration failed"
            )
            return HttpResponse(status=500)

    return HttpResponse(status=200)