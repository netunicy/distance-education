from django.db import models
from django.conf import settings

from .topics import Topics


class TopicPurchase(models.Model):

    # ==========================================
    # Χρήστης
    # ==========================================

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="topic_purchases",
    )

    # ==========================================
    # Topic που αγοράστηκε
    # ==========================================

    topic = models.ForeignKey(
        Topics,
        on_delete=models.CASCADE,
        related_name="purchases",
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
    # Ποσό που πληρώθηκε σε pence
    # ==========================================

    amount_paid = models.PositiveIntegerField()

    # ==========================================
    # Ημερομηνία αγοράς
    # ==========================================

    purchased_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:

        verbose_name = "Topic Purchase"
        verbose_name_plural = "Topic Purchases"

        ordering = [
            "-purchased_at",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=["user", "topic"],
                name="unique_topic_purchase_per_user",
            ),
        ]

    def __str__(self):

        return (
            f"{self.user} | "
            f"{self.topic.title}"
        )