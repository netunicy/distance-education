from django.db import models
from homepage.helpers.slug import generate_unique_slug

class Training(models.Model):

    class Category(models.TextChoices):
        PROGRAMMING = "Programming", "Programming"
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
    image = models.CharField(max_length=1000,blank=True,null=True)
    alt = models.CharField(max_length=1000,blank=True,null=True)
    duration = models.CharField(max_length=100,blank=True)
    includes = models.TextField(blank=True,help_text="Ένα στοιχείο ανά γραμμή.")
    price = models.DecimalField(max_digits=8,decimal_places=2,default=0)
    is_free = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title"]
        verbose_name = "Training"
        verbose_name_plural = "Trainings"


    def save(self, *args, **kwargs):

        if not self.slug:

            self.slug = generate_unique_slug(
                model=Training,
                value=self.title,
                instance=self,
            )

        super().save(*args, **kwargs)


    def __str__(self):
        return self.title