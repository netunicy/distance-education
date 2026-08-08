from django.db import models
from django.urls import reverse


class InformationPage(models.Model):

    title = models.CharField(max_length=200,verbose_name="Τίτλος",)
    path_image = models.URLField(max_length=500,verbose_name="Εικόνα",)
    order = models.PositiveIntegerField(default=1,verbose_name="Σειρά εμφάνισης",)

    class Meta:
        ordering = ["order"]
        verbose_name = "Card for Legal Information"
        verbose_name_plural = "Cards for Legal Information"

    def __str__(self):
        return self.title