from django.db import models
from tinymce.models import HTMLField

class Informations(models.Model):
    title = models.CharField(max_length=200)
    image=models.CharField(max_length=1000,null=True,blank=True,help_text="Βάλε URL της εικόνας")
    description = HTMLField(null=True,blank=True)

    class Meta:
        verbose_name_plural = 'Company Informations'
        ordering = ['id']

    def __str__(self):
        return f"{self.title}"
