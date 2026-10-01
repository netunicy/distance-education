from django.db import models
from homepage.storage import get_r2_storage
class Logo(models.Model):
    mylogo = models.ImageField(
        upload_to="logos/",
        storage=get_r2_storage,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"Logo {self.id}"