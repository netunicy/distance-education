from django.db import models
from django.conf import settings

from .school import Schoolcontexts
from .school_chapter import Chapter


class UserPurchase(models.Model):

    # ==========================================
    # Χρήστης
    # ==========================================

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="purchases",
    )

    # ==========================================
    # Βιβλίο
    # ==========================================

    book = models.ForeignKey(
        Schoolcontexts,
        on_delete=models.CASCADE,
        related_name="purchases",
    )

    # ==========================================
    # Κεφάλαιο
    #
    # Αν chapter = NULL:
    # αγορά ολόκληρου βιβλίου
    #
    # Αν chapter έχει τιμή:
    # αγορά συγκεκριμένου κεφαλαίου
    # ==========================================

    chapter = models.ForeignKey(
        Chapter,
        on_delete=models.CASCADE,
        related_name="purchases",
        null=True,
        blank=True,
    )

    # ==========================================
    # Stripe Checkout Session
    # ==========================================

    stripe_session_id = models.CharField(
        max_length=255,
        unique=True,
        db_index=True,
    )

    # ==========================================
    # Ποσό που πληρώθηκε
    # Αποθηκεύεται σε pence
    # π.χ. £10.00 = 1000
    # ==========================================

    amount_paid = models.PositiveIntegerField()

    # ==========================================
    # Ημερομηνία αγοράς
    # ==========================================

    purchased_at = models.DateTimeField(
        auto_now_add=True,
    )

    # ==========================================
    # Meta
    # ==========================================

    class Meta:

        verbose_name = "User Purchase"
        verbose_name_plural = "User Purchases"

        ordering = [
            "-purchased_at",
        ]

    # ==========================================
    # String representation
    # ==========================================

    def __str__(self):

        if self.chapter:

            return (
                f"{self.user} | "
                f"{self.book.title} | "
                f"{self.chapter.title}"
            )

        return (
            f"{self.user} | "
            f"{self.book.title} | "
            f"Ολόκληρο βιβλίο"
        )