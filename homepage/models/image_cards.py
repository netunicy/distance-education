from django.db import models
from django.urls import reverse


class InformationPage(models.Model):

    PAGE_CHOICES = (
        ("terms_and_conditions", "Όροι και Προϋποθέσεις"),
        ("register", "Register"),
        ("login", "Sign In"),
        ("online_lessons", "Online Μαθήματα"),
        ("announcements", "Ανακοινώσεις"),
        ("faq", "Συχνές Ερωτήσεις"),
        ("contact", "Επικοινωνία"),
        ("about_us", "Σχετικά με εμάς"),
        ("refund_policy", "Refund Policy"),
        ("copyright_notice", "Copyright Notice"),
        ("privacy_policy", "Privacy Policy"),
    )

    APP_CHOICES = (
        ("homepage", "Homepage"),
        ("accounts", "Accounts"),
    )

    app = models.CharField(max_length=20,choices=APP_CHOICES,default="homepage")
    page = models.CharField(max_length=50,choices=PAGE_CHOICES,unique=True,verbose_name="Σελίδα",)
    title = models.CharField(max_length=200,verbose_name="Τίτλος",)
    path_image = models.URLField(max_length=500,verbose_name="Εικόνα",)
    order = models.PositiveIntegerField(default=1,verbose_name="Σειρά εμφάνισης",)

    class Meta:
        ordering = ["order"]
        verbose_name = "Σελίδα Πληροφόρησης"
        verbose_name_plural = "Σελίδες Πληροφόρησης"

    @property
    def url(self):
        return reverse(f"{self.app}:{self.page}")

    def __str__(self):
        return self.title