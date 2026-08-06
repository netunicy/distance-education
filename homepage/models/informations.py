from django.db import models
from tinymce.models import HTMLField

from homepage.models.image_cards import InformationPage

# models/informations.py
class Informations(models.Model):
    page = models.OneToOneField(InformationPage, on_delete=models.CASCADE, related_name='modal_info', null=True, blank=True)
    title = models.CharField(max_length=200)
    image = models.CharField(max_length=1000, null=True, blank=True)
    description = HTMLField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Company Informations'
        ordering = ['id']

    def __str__(self):
        return f"{self.title}"
