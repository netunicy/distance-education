from django.contrib import admin
from .models import (
    Logo,
    Mycontexts,
    Chapter,
    Video,
    Training,
    TrainingContent,
    TrainingMaterial,
    InformationPage,
)
from .forms import (
    TrainingMaterialAdminForm,
    VideoAdminForm,
)

admin.site.register(Logo)
admin.site.register(Mycontexts)
admin.site.register(Chapter)
admin.site.register(TrainingContent)
admin.site.register(InformationPage)

@admin.register(TrainingMaterial)
class TrainingMaterialAdmin(admin.ModelAdmin):
    exclude = ("slug",)
    form = TrainingMaterialAdminForm
    

@admin.register(Video)
class VideosAdmin(admin.ModelAdmin):

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