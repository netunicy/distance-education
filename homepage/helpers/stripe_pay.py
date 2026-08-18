import logging

import stripe

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)

from homepage.models.school import Schoolcontexts
from homepage.models.school_chapter import Chapter


# ==========================================
# LOGGER
# ==========================================

logger = logging.getLogger(__name__)


# ==========================================
# STRIPE SETTINGS
# ==========================================

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = "2025-03-31.basil"


# ==========================================
# CHAPTER STRIPE PAYMENT
# ==========================================

@login_required
def chapter_stripe_payment(request, book_id, chapter_id):

    # ==========================================
    # Βιβλίο
    # ==========================================

    book = get_object_or_404(
        Schoolcontexts,
        id=book_id,
    )


    # ==========================================
    # Κεφάλαιο
    # ==========================================

    chapter = get_object_or_404(
        Chapter,
        id=chapter_id,
        context=book,
    )


    # ==========================================
    # Τιμή
    #
    # Stripe χρησιμοποιεί pence:
    # £10.00 = 1000
    # ==========================================

    amount = book.price_chapter * 100


    # ==========================================
    # Εικόνα βιβλίου
    # ==========================================

    images = []

    if book.image:
        images = [book.image.url]


    # ==========================================
    # SUCCESS URL
    #
    # LOCAL:
    # http://127.0.0.1:8000/pay_success/
    #
    # PRODUCTION:
    # https://www.turnonlearning.com/pay_success/
    # ==========================================

    success_url = (
        request.build_absolute_uri("/pay_success/")
        + "?session_id={CHECKOUT_SESSION_ID}"
    )


    # ==========================================
    # CANCEL URL
    # ==========================================

    cancel_url = request.build_absolute_uri(
        "/pay_cancel/"
    )


    # ==========================================
    # DEBUG
    # ==========================================

    logger.info(
        "Stripe checkout URLs - success=%s cancel=%s",
        success_url,
        cancel_url,
    )


    # ==========================================
    # CREATE STRIPE CHECKOUT SESSION
    # ==========================================

    try:

        session = stripe.checkout.Session.create(

            # ==================================
            # Managed Payments OFF
            # ==================================

            managed_payments={
                "enabled": False,
            },


            # ==================================
            # Adaptive Pricing OFF
            # ==================================

            adaptive_pricing={
                "enabled": False,
            },


            # ==================================
            # Προϊόν
            # ==================================

            line_items=[
                {
                    "price_data": {

                        "currency": "gbp",

                        "unit_amount": amount,

                        "product_data": {

                            "name": (
                                f"{book.title} - "
                                f"{chapter.title}"
                            ),

                            "images": images,

                            "tax_code": "txcd_20060158",
                        },
                    },

                    "quantity": 1,
                }
            ],


            # ==================================
            # One-off Payment
            # ==================================

            mode="payment",


            # ==================================
            # Metadata
            # ==================================

            metadata={

                "user_id": str(request.user.id),

                "purchase_type": "chapter",

                "book_id": str(book.id),

                "chapter_id": str(chapter.id),
            },


            # ==================================
            # Redirect URLs
            # ==================================

            success_url=success_url,

            cancel_url=cancel_url,
        )


        # ==========================================
        # Redirect στο Stripe Checkout
        # ==========================================

        return redirect(
            session.url
        )


    # ==========================================
    # STRIPE ERROR
    # ==========================================

    except stripe.error.StripeError as e:

        logger.exception(
            "Stripe checkout error for user=%s book=%s chapter=%s",
            request.user.id,
            book.id,
            chapter.id,
        )

        error_message = getattr(
            e,
            "user_message",
            str(e),
        )

        return render(
            request,
            "payment_error.html",
            {
                "error_message": error_message,
            },
        )