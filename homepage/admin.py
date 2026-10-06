import logging

from django.contrib import admin, messages

from homepage.helpers.media.processor import VideoProcessor
from homepage.cloudflare.client import CloudflareStreamClient

from .models import (
    Logo,
    FooterLogo,
    BackgroundImage,
    Schoolcontexts,
    Chapter,
    SchoolVideo,
    Topics,
    TopicsContent,
    TopicsVideo,
    InformationPage,
    Informations,
)
from .forms import TopicsVideoAdminForm, VideoAdminForm

logger = logging.getLogger(__name__)

admin.site.register(FooterLogo)
admin.site.register(BackgroundImage)
# Other registrations (unchanged)
admin.site.register(Logo)
admin.site.register(Chapter)
admin.site.register(TopicsContent)
admin.site.register(InformationPage)
admin.site.register(Informations)


@admin.register(Schoolcontexts)
class SchoolcontextsAdmin(admin.ModelAdmin):
    exclude = ("slug",)


class CloudflareVideoUploadMixin:
    """Shared admin upload path for SchoolVideo and video-type TopicsVideo."""

    def should_upload_video(self, obj, form):
        return "video_file" in form.changed_data and bool(obj.video_file)

    def video_name(self, obj):
        raise NotImplementedError

    def save_model(self, request, obj, form, change):
        should_upload = self.should_upload_video(obj, form)
        model_name = type(obj).__name__
        old_uid = None
        if change and obj.pk:
            old_uid = (
                type(obj).objects.filter(pk=obj.pk)
                .values_list("cloudflare_uid", flat=True)
                .first()
            )

        # Save the record and its temporary file first.
        super().save_model(request, obj, form, change)
        if not should_upload:
            logger.warning("%s saved without new video: id=%s", model_name, obj.pk)
            return

        try:
            logger.warning("%s Cloudflare upload started: id=%s", model_name, obj.pk)
            result = VideoProcessor().process(
                input_file=obj.video_file.path,
                meta={"name": self.video_name(obj)},
            )
            uid = result.get("uid")
            if not uid:
                raise RuntimeError("Cloudflare did not return a video UID")
            logger.warning("%s Cloudflare upload verified: id=%s uid=%s", model_name, obj.pk, uid)
        except Exception:
            logger.exception("%s Cloudflare upload/protection failed: id=%s", model_name, obj.pk)
            messages.error(
                request,
                "Η εγγραφή αποθηκεύτηκε, αλλά η μεταφόρτωση ή η προστασία "
                "στο Cloudflare απέτυχε. Το προσωρινό αρχείο διατηρήθηκε. "
                "Ελέγξτε τα Render Logs πριν δοκιμάσετε ξανά.",
            )
            return

        # Persist Cloudflare identifiers before removing the local temporary file.
        try:
            obj.cloudflare_uid = uid
            obj.cloudflare_status = result.get("status", "pending")
            update_fields = ["cloudflare_uid", "cloudflare_status"]
            if isinstance(obj, SchoolVideo):
                obj.cloudflare_ready = result.get("ready", False)
                update_fields.append("cloudflare_ready")
            obj.save(update_fields=update_fields)
        except Exception:
            logger.exception("%s Cloudflare UID save failed: id=%s uid=%s", model_name, obj.pk, uid)
            messages.error(
                request,
                "Το βίντεο ανέβηκε στο Cloudflare, αλλά δεν αποθηκεύτηκε το UID. "
                "Μην το ανεβάσετε ξανά πριν ελέγξετε τα Render Logs.",
            )
            return

        try:
            obj.video_file.delete(save=True)
        except Exception:
            logger.exception("%s temporary file deletion failed: id=%s", model_name, obj.pk)
            messages.warning(
                request,
                "Το βίντεο ανέβηκε και αποθηκεύτηκε, αλλά δεν διαγράφηκε "
                "το προσωρινό αρχείο.",
            )

        # Delete the previous Cloudflare video only after the new one is
        # protected, its UID is saved, and the temporary file is removed.
        if old_uid and old_uid != uid:
            try:
                deletion = CloudflareStreamClient().delete(f"/stream/{old_uid}")
                if deletion is not None and deletion.get("success") is False:
                    raise RuntimeError(f"Cloudflare rejected deletion: {deletion}")
                logger.warning(
                    "%s previous Cloudflare video deleted: id=%s old_uid=%s new_uid=%s",
                    model_name, obj.pk, old_uid, uid,
                )
            except Exception:
                logger.exception(
                    "%s old Cloudflare video deletion failed: id=%s old_uid=%s new_uid=%s",
                    model_name, obj.pk, old_uid, uid,
                )
                messages.warning(
                    request,
                    "Το νέο βίντεο αποθηκεύτηκε και προστατεύτηκε, αλλά δεν "
                    "διαγράφηκε το παλιό από το Cloudflare. Ελέγξτε τα Render Logs.",
                )
                return

        messages.success(
            request,
            "Το βίντεο ανέβηκε στο Cloudflare και επαληθεύτηκε η προστασία Signed URLs.",
        )


@admin.register(TopicsVideo)
class TopicsVideoAdmin(CloudflareVideoUploadMixin, admin.ModelAdmin):
    form = TopicsVideoAdminForm
    exclude = ("slug",)

    def should_upload_video(self, obj, form):
        return (
            obj.material_type == TopicsVideo.MaterialType.VIDEO
            and super().should_upload_video(obj, form)
        )

    def video_name(self, obj):
        return obj.title


@admin.register(SchoolVideo)
class SchoolVideoAdmin(CloudflareVideoUploadMixin, admin.ModelAdmin):
    form = VideoAdminForm
    list_display = ("book", "chapter", "page", "part", "views")
    list_filter = ("chapter",)
    search_fields = ("activity_title", "page")
    ordering = ("chapter__context", "chapter__order", "page", "part")
    exclude = ("slug",)
    filter_horizontal = ("topics_contents",)
    list_per_page = 30

    @admin.display(description="Book")
    def book(self, obj):
        return obj.chapter.context

    def video_name(self, obj):
        return obj.activity_title or str(obj)


@admin.register(Topics)
class TopicsAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "level", "price")
    list_filter = ("category", "level")
    search_fields = ("title", "description")
