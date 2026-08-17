import logging
logger = logging.getLogger(__name__)
from django.shortcuts import redirect, render
import stripe
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from homepage.models.school import Schoolcontexts
from homepage.models.school_chapter import Chapter
from django.conf import settings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def read_secret(file_name, default=None):
    try:
        base_dir = BASE_DIR / "config" / "secrets"
        with open(base_dir / file_name) as f:
            return f.read().strip()
    except FileNotFoundError:
        return default

    
stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = "2025-03-31.basil"

@login_required
def chapter_stripe_payment(request, book_id, chapter_id):

    book = get_object_or_404(Schoolcontexts,id=book_id,)

    chapter = get_object_or_404(Chapter,id=chapter_id,context=book,)

    amount = book.price_chapter * 100

    images = []

    if book.image:
        images = [book.image.url]

    try:

        session = stripe.checkout.Session.create(

            managed_payments={
                "enabled": False,
            },

            adaptive_pricing={
                "enabled": False,
            },

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

            mode="payment",

            metadata={
                "user_id": str(request.user.id),
                "purchase_type": "chapter",
                "book_id": str(book.id),
                "chapter_id": str(chapter.id),
            },

            success_url="https://www.turnonlearning.com/pay_success/",
            cancel_url="https://www.turnonlearning.com/pay_cancel/",
        )

        return redirect(session.url)

    except stripe.error.StripeError as e:

        error_message = getattr(
            e,
            "user_message",
            str(e),
        )

        return render(
            request,
            "payment_error.html",
            {
                "error_message": error_message
            },
        )