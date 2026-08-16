from django.db import models
from homepage.helpers.slug import generate_unique_slug
from homepage.models.topics import Topics


class TopicsContent(models.Model):

    topics = models.ForeignKey(Topics,on_delete=models.CASCADE,related_name="topics_contents",)
    content = models.CharField(max_length=1000,help_text="Τίτλος Περιεχομένου π.χ 'Εισαγωγή στη Γεωμετρία' ",)
    slug = models.SlugField(max_length=1000,blank=True,db_index=True,)
    description = models.CharField(max_length=1000,blank=True,help_text="Περιγραφή του video. Γραψε μια συντομη περιγραφή π.χ 'Γεωμετρια - Θεωρια'.",)
    order = models.PositiveIntegerField(default=1)

    class Meta:

        ordering = ["order"]
        verbose_name = "Topic Chapter"
        verbose_name_plural = "Topic Chapters"

        constraints = [
            models.UniqueConstraint(
                fields=["topics", "content"],
                name="unique_content_per_topics",
            ),

            models.UniqueConstraint(
                fields=["topics", "slug"],
                name="unique_slug_per_topics",
            ),

            models.UniqueConstraint(
                fields=["topics", "order"],
                name="unique_content_order_per_topics",
            ),

        ]

    def save(self, *args, **kwargs):

        if not self.slug:

            self.slug = generate_unique_slug(
                model=TopicsContent,
                value=self.content,
                instance=self,
                topics=self.topics,
            )

        super().save(*args, **kwargs)

    def __str__(self):

        return self.content