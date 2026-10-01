from django.contrib import admin

from .models import (
    Logo,
    Schoolcontexts,
    Chapter,
    SchoolVideo,
    Topics,
    TopicsContent,
    TopicsVideo,
    InformationPage,
    Informations,
)

from .forms import (
    TopicsVideoAdminForm,
    VideoAdminForm,
)


# =========================================================
# Simple registrations
# =========================================================

admin.site.register(Logo)
admin.site.register(Chapter)
admin.site.register(TopicsContent)
admin.site.register(InformationPage)
admin.site.register(Informations)


# =========================================================
# School Contexts
# =========================================================

@admin.register(Schoolcontexts)
class SchoolcontextsAdmin(admin.ModelAdmin):

    exclude = ("slug",)


# =========================================================
# Topics Videos
# =========================================================

@admin.register(TopicsVideo)
class TopicsVideoAdmin(admin.ModelAdmin):

    exclude = ("slug",)
    form = TopicsVideoAdminForm


# =========================================================
# School Videos
# =========================================================

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

    filter_horizontal = (
        "topics_contents",
    )

    list_per_page = 30

    @admin.display(description="Book")
    def book(self, obj):
        return obj.chapter.context


# =========================================================
# Topics
# =========================================================

@admin.register(Topics)
class TopicsAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "category",
        "level",
        "price",
    )

    list_filter = (
        "category",
        "level",
    )

    search_fields = (
        "title",
        "description",
    )