from django.db import models
from homepage.storage import get_r2_storage

class BackgroundImage(models.Model):
    image = models.ImageField(
        upload_to="backgrounds/",
        storage=get_r2_storage,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"Background Image {self.id}"