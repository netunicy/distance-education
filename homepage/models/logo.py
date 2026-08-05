from django.db import models

class Logo(models.Model):
    mylogo = models.CharField(max_length=1000, blank=True, null=True)
    
    def __str__(self):
        return f"Logo {self.id}"