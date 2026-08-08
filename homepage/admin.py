from django.contrib import admin
from .models import (
    Logo,
    Schoolcontexts,
    Chapter,
    SchoolVideo,
    Training,
    TrainingContent,
    TrainingVideo,
    InformationPage,
    Informations,
)
from .forms import (
    TrainingVideoAdminForm,
    VideoAdminForm,
)
import cloudinary.uploader

admin.site.register(Logo)
admin.site.register(Chapter)
admin.site.register(TrainingContent)
admin.site.register(InformationPage)
admin.site.register(Informations)

@admin.register(Schoolcontexts)
class SchoolcontextsAdmin(admin.ModelAdmin):

    exclude = ("slug",)

    def save_model(self, request, obj, form, change):

        uploaded_image = request.FILES.get("image")

        # Αποθηκεύουμε πρώτα τα υπόλοιπα στοιχεία
        # χωρίς να αφήσουμε το CloudinaryField να κάνει
        # το upload της νέας εικόνας μόνο του.
        if uploaded_image:

            old_image = None

            if obj.pk:
                old_obj = Schoolcontexts.objects.filter(
                    pk=obj.pk
                ).first()

                if old_obj:
                    old_image = old_obj.image

            obj.image = old_image

        super().save_model(request, obj, form, change)

        # Κάνουμε εμείς το upload στο σωστό Cloudinary folder
        if uploaded_image:

            folder = obj.get_cloudinary_folder()

            result = cloudinary.uploader.upload(
                uploaded_image,
                folder=folder,
                resource_type="image",
            )

            obj.image = result["public_id"]

            # update() για να μην ξανατρέξει το save()
            Schoolcontexts.objects.filter(
                pk=obj.pk
            ).update(
                image=result["public_id"]
            )
@admin.register(TrainingVideo)
class TrainingVideoAdmin(admin.ModelAdmin):
    exclude = ("slug",)
    form = TrainingVideoAdminForm
    

@admin.register(SchoolVideo)
class SchoolVideoAdmin(admin.ModelAdmin):

    form = VideoAdminForm

    list_display = (
        "book",
        "chapter",
        "page",
        "part",
        "views",
    )

    list_filter = (
        "chapter",
    )

    search_fields = (
        "activity_title",
        "page",
    )

    ordering = (
        "chapter__context",
        "chapter__order",
        "page",
        "part",
    )
    exclude = ("slug",)

    list_per_page = 30

    @admin.display(description="Book")
    def book(self, obj):
        return obj.chapter.context
    
@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "category",
        "level",
        "price",
        "is_free",
        "is_published",
    )

    list_filter = (
        "category",
        "level",
        "is_free",
        "is_published",
    )

    search_fields = (
        "title",
        "description",
    )

    readonly_fields = (
        "created",
        "updated",
    )