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

admin.site.register(Logo)
admin.site.register(Schoolcontexts)
admin.site.register(Chapter)
admin.site.register(TrainingContent)
admin.site.register(InformationPage)
admin.site.register(Informations)

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