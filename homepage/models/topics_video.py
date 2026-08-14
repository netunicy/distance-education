from django.db import models
from homepage.helpers.slug import generate_unique_slug
from homepage.models.topics_chapter import TopicsContent


class TopicsVideo(models.Model):

    class MaterialType(models.TextChoices):
        VIDEO = "video", "Video"
        PDF = "pdf", "PDF"
        IMAGE = "image", "Image"
        PRESENTATION = "presentation", "Presentation"
        FILE = "file", "File"
        LINK = "link", "External Link"
        QUIZ = "quiz", "Quiz"

    topics_content = models.ForeignKey(TopicsContent,on_delete=models.CASCADE,related_name="materials")
    material_type = models.CharField(max_length=20,choices=MaterialType.choices,)
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,blank=True,db_index=True,)
    video_file = models.FileField(upload_to="temp/",blank=True,null=True,)
    cloudflare_uid = models.CharField(
        max_length=64,
        blank=True,
        editable=False,
    )

    cloudflare_status = models.CharField(
        max_length=20,
        default="pending",
        editable=False,
    )
    order = models.PositiveIntegerField(default=1)
    is_free = models.BooleanField(default=False)

    class Meta:

        ordering = ["order"]
        verbose_name = "Topic Video"
        verbose_name_plural = "Topic Videos"

        constraints = [

            models.UniqueConstraint(
                fields=["topics_content", "slug"],
                name="unique_material_slug_per_content",
            ),

            models.UniqueConstraint(
                fields=["topics_content", "order"],
                name="unique_material_order_per_content",
            ),

        ]

    def save(self, *args, **kwargs):

        if not self.slug:

            self.slug = generate_unique_slug(
                model=TopicsVideo,
                value=self.title,
                instance=self,
                topics_content=self.topics_content,
            )

        super().save(*args, **kwargs)

    def __str__(self):

        return self.title