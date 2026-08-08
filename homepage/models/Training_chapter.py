from django.db import models
from homepage.helpers.slug import generate_unique_slug
from homepage.models.training import Training


class TrainingContent(models.Model):

    training = models.ForeignKey(Training,on_delete=models.CASCADE,related_name="training_contents",)
    content = models.CharField(max_length=200,help_text="Περιεχόμενο του training",)
    slug = models.SlugField(max_length=200,blank=True,db_index=True,)
    description = models.TextField(blank=True,help_text="Περιγραφή του training",)
    order = models.PositiveIntegerField(default=1)

    class Meta:

        ordering = ["order"]
        verbose_name = "Training Chapter"
        verbose_name_plural = "Training Chapters"

        constraints = [
            models.UniqueConstraint(
                fields=["training", "content"],
                name="unique_content_per_training",
            ),

            models.UniqueConstraint(
                fields=["training", "slug"],
                name="unique_slug_per_training",
            ),

            models.UniqueConstraint(
                fields=["training", "order"],
                name="unique_content_order_per_training",
            ),

        ]

    def save(self, *args, **kwargs):

        if not self.slug:

            self.slug = generate_unique_slug(
                model=TrainingContent,
                value=self.content,
                instance=self,
                training=self.training,
            )

        super().save(*args, **kwargs)

    def __str__(self):

        return self.content