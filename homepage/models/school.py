from django.db import models

from homepage.helpers.slug import generate_unique_slug


class Mycontexts(models.Model):

    class LevelType(models.TextChoices):
        # Εκπαίδευση
        ΔΗΜΟΤΙΚΟ = "Δημοτικού", "Δημοτικού"
        ΓΥΜΝΑΣΙΟ = "Γυμνασίου", "Γυμνασίου"
        ΛΥΚΕΙΟ = "Λυκείου", "Λυκείου"

    class SubjectLesson(models.TextChoices):
        GREEK = "Ελληνικά", "Ελληνικά"
        MATHS = "Μαθηματικά", "Μαθηματικά"
        HISTORY = "Ιστορία", "Ιστορία"
        PHYSICS = "Φυσική", "Φυσική"

    class ClassLevel(models.TextChoices):
        A = "Α΄ Τάξη", "Α΄ Τάξη"
        B = "Β΄ Τάξη", "Β΄ Τάξη"
        G = "Γ΄ Τάξη", "Γ΄ Τάξη"
        D = "Δ΄ Τάξη", "Δ΄ Τάξη"
        E = "Ε΄ Τάξη", "Ε΄ Τάξη"
        ST = "ΣΤ΄ Τάξη", "ΣΤ΄ Τάξη"

    title = models.CharField(max_length=1000, null=True, blank=True)

    slug = models.SlugField(
        unique=True,
        blank=True,
        db_index=True,
    )

    subject_lesson = models.CharField(
        max_length=1000,
        choices=SubjectLesson.choices,
        default=SubjectLesson.GREEK,
        null=True,
        blank=True,
    )

    stage = models.CharField(
        max_length=20,
        choices=LevelType.choices,
        default=LevelType.ΔΗΜΟΤΙΚΟ,
        null=True,
        blank=True,
    )

    class_is = models.CharField(
        max_length=1000,
        choices=ClassLevel.choices,
        default=ClassLevel.A,
        null=True,
        blank=True,
    )

    edition = models.CharField(
        max_length=1000,
        null=True,
        blank=True,
    )

    description = models.TextField(
        max_length=10000,
        null=True,
        blank=True,
    )

    image = models.CharField(
        max_length=1000,
        null=True,
        blank=True,
    )

    alt = models.CharField(
        max_length=1000,
        null=True,
        blank=True,
    )

    price_chapter = models.IntegerField(
        null=True,
        blank=True,
    )

    price_all = models.IntegerField(
        null=True,
        blank=True,
    )

    includes = models.TextField(
        blank=True,
        help_text="Ένα στοιχείο ανά γραμμή.",
    )

    class Meta:
        verbose_name_plural = "My Contexts"
        ordering = ["subject_lesson"]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "title",
                    "subject_lesson",
                    "class_is",
                    "edition",
                ],
                name="unique_context_per_class_level_edition",
            ),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(
                model=Mycontexts,
                value=self.title,
                instance=self,
            )
        super().save(*args, **kwargs)
    def __str__(self):
        return (
            f"{self.get_subject_lesson_display()} – "
            f"{self.get_class_is_display()} – "
            f"{self.get_stage_display()} – "
            f"{self.edition}"
        )