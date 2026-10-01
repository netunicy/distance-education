from django.db import models
from django.urls import reverse
from homepage.storage import get_r2_storage

class InformationPage(models.Model):

    title = models.CharField(max_length=200,verbose_name="Τίτλος",)
    path_image = models.ImageField(upload_to="information-pages/",storage=get_r2_storage,blank=True,null=True,verbose_name="Εικόνα",)
    order = models.PositiveIntegerField(default=1,verbose_name="Σειρά εμφάνισης",)

    class Meta:
        ordering = ["order"]
        verbose_name = "Card for Legal Information"
        verbose_name_plural = "Cards for Legal Information"

    def __str__(self):
        return self.title