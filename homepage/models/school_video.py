from django.db import models

from homepage.helpers.slug import generate_unique_slug
from .school_chapter import Chapter


class SchoolVideo(models.Model):

    class CloudflareStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        QUEUED = "queued", "Queued"
        PROCESSING = "processing", "Processing"
        READY = "ready", "Ready"
        ERROR = "error", "Error"

    class Part(models.TextChoices):
        SINGLE = "", "Ένα Video"
        PART1 = "1", "1ο Μέρος"
        PART2 = "2", "2ο Μέρος"
        PART3 = "3", "3ο Μέρος"
        PART4 = "4", "4ο Μέρος"
        PART5 = "5", "5ο Μέρος"
        PART6 = "6", "6ο Μέρος"
        PART7 = "7", "7ο Μέρος"
        PART8 = "8", "8ο Μέρος"
        PART9 = "9", "9ο Μέρος"

    # Το chapter στο οποίο ανήκει το video
    chapter = models.ForeignKey(
        Chapter,
        on_delete=models.CASCADE,
        related_name="videos",
    )

    # Περιγραφή της δραστηριότητας
    activity_title = models.CharField(
        max_length=200,
        blank=True,
        help_text=(
            "Περιγραφή της δραστηριότητας της σελίδας, "
            "π.χ. 'Εισαγωγή στο κεφάλαιο', "
            "'Άσκηση 1', 'Άσκηση 2' κλπ."
        ),
    )

    # Slug
    slug = models.SlugField(
        blank=True,
        db_index=True,
    )
    

    # Αριθμός σελίδας
    page = models.PositiveSmallIntegerField(
        default=1,
        help_text="Αριθμός σελίδας του βιβλίου",
    )

    # Μέρος video
    part = models.CharField(
        max_length=2,
        choices=Part.choices,
        default=Part.SINGLE,
        blank=True,
    )

    # Προσωρινό upload
    video_file = models.FileField(
        upload_to="temp/",
        blank=True,
        null=True,
    )

    cloudflare_uid = models.CharField(
        max_length=64,
        blank=True,
        editable=False,
        db_index=True,
    )

    cloudflare_status = models.CharField(
        max_length=20,
        choices=CloudflareStatus.choices,
        default=CloudflareStatus.PENDING,
        editable=False,
    )

    cloudflare_ready = models.BooleanField(
        default=False,
        editable=False,
    )
    
    # Προβολές
    views = models.PositiveIntegerField(
        default=0,
        editable=False,
    )

    # Δωρεάν
    is_free = models.BooleanField(default=False)

    class Meta:

        verbose_name = "School Video"
        verbose_name_plural = "School Videos"

        ordering = (
            "chapter__order",
            "page",
            "part",
        )

        constraints = [

            models.UniqueConstraint(
                fields=[
                    "chapter",
                    "slug",
                ],
                name="unique_video_slug_per_chapter",
            ),

            models.UniqueConstraint(
                fields=[
                    "chapter",
                    "page",
                    "part",
                ],
                name="unique_video_location",
            ),

        ]

    def save(self, *args, **kwargs):

        if not self.slug:

            value = self.activity_title.strip()

            if not value:
                value = f"page-{self.page}"

            if self.part:
                value = f"{value}-{self.part}"

            self.slug = generate_unique_slug(
                model=SchoolVideo,
                value=value,
                instance=self,
                chapter=self.chapter,
            )

        super().save(*args, **kwargs)

    def __str__(self):

        return (
            f"{self.chapter.title} | "
            f"Σελίδα {self.page} | "
            f"{self.get_part_display()}"
        )