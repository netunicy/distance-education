from django.db import models
from homepage.helpers.slug import generate_unique_slug
from cloudinary.models import CloudinaryField
class Topics(models.Model):

    class Category(models.TextChoices):
        PROGRAMMING = "Programming", "Programming"
        MATHEMATICS = "Mathematics", "Μαθηματικά"
        EDUCATION = "Education", "Education"
        LANGUAGES = "Languages", "Languages"
        BUSINESS = "Business", "Business"
        DESIGN = "Design", "Design"
        OTHER = "Other", "Other"

    class Level(models.TextChoices):
        BEGINNER = "Beginner", "Beginner"
        INTERMEDIATE = "Intermediate", "Intermediate"
        ADVANCED = "Advanced", "Advanced"
 

    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True,blank=True,db_index=True)
    category = models.CharField(max_length=50,choices=Category.choices,default=Category.OTHER)
    level = models.CharField(max_length=30,choices=Level.choices,default=Level.BEGINNER)
    description = models.TextField(blank=True)
    image = CloudinaryField("image",blank=True,null=True)
    alt = models.CharField(max_length=1000,blank=True,null=True)
    includes = models.TextField(blank=True,help_text="Τι περιλαμβάνει. Ένα στοιχείο ανά γραμμή.")
    price = models.DecimalField(max_digits=8,decimal_places=2,default=0)

    class Meta:
        ordering = ["title"]
        verbose_name = "Topic"
        verbose_name_plural = "Topics"


    def save(self, *args, **kwargs):

        if not self.slug:

            self.slug = generate_unique_slug(
                model=Topics,
                value=self.title,
                instance=self,
            )

        super().save(*args, **kwargs)


    def __str__(self):
        return self.title