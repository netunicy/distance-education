from django.db import models

from homepage.helpers.slug import generate_unique_slug
from .school import Schoolcontexts


class Chapter(models.Model):

    context = models.ForeignKey(
        Schoolcontexts,
        on_delete=models.CASCADE,
        related_name="chapters",
    )

    title = models.CharField(
        max_length=200,
        help_text="Τίτλος κεφαλαίου",
    )

    slug = models.SlugField(
        blank=True,
        db_index=True,
    )

    order = models.PositiveIntegerField(default=1)

    class Meta:

        ordering = ["order"]

        verbose_name = "School Chapter"
        verbose_name_plural = "School Chapters"

        constraints = [

            models.UniqueConstraint(
                fields=["context", "title"],
                name="unique_chapter_per_context",
            ),

            models.UniqueConstraint(
                fields=["context", "slug"],
                name="unique_chapter_slug_per_context",
            ),

            models.UniqueConstraint(
                fields=["context", "order"],
                name="unique_chapter_order_per_context",
            ),

        ]

    def save(self, *args, **kwargs):

        if not self.slug:

            self.slug = generate_unique_slug(
                model=Chapter,
                value=self.title,
                instance=self,
                context=self.context,
            )

        super().save(*args, **kwargs)

    def __str__(self):

        return self.title