
import json
from django.contrib import messages
from homepage.helpers.media.processor import VideoProcessor
from django.contrib import admin
from django.core.exceptions import PermissionDenied, ValidationError
from django.http import JsonResponse
from django.urls import path
from django.views.decorators.http import require_POST

from homepage.cloudflare.client import CloudflareStreamClient

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

    # -----------------------------------------------------
    # Cloudflare direct upload URL
    # -----------------------------------------------------

    def get_urls(self):
        custom_urls = [
            path(
                "create-upload/",
                self.admin_site.admin_view(
                    require_POST(self.create_upload)
                ),
                name="topicsvideo_create_upload",
            ),
        ]

        return custom_urls + super().get_urls()

    # -----------------------------------------------------
    # Create Cloudflare upload
    # -----------------------------------------------------

    def create_upload(self, request):

        if not (
            self.has_add_permission(request)
            or self.has_change_permission(request)
        ):
            return JsonResponse(
                {"error": "Permission denied"},
                status=403,
            )

        try:
            data = json.loads(request.body)
            file_size = data.get("file_size")

            if type(file_size) is not int or file_size <= 0:
                return JsonResponse(
                    {"error": "Invalid file size"},
                    status=400,
                )

            result = CloudflareStreamClient().create_tus_upload(
                file_size
            )

            pending = request.session.get(
                "pending_video_uploads",
                {},
            )

            pending[result["uid"]] = {
                "user_id": request.user.pk,
                "model": "TopicsVideo",
            }

            request.session["pending_video_uploads"] = pending
            request.session.modified = True

            return JsonResponse(result)

        except (ValueError, TypeError):
            return JsonResponse(
                {"error": "Invalid request"},
                status=400,
            )

        except Exception:
            return JsonResponse(
                {"error": "Cloudflare upload creation failed"},
                status=502,
            )

    # -----------------------------------------------------
    # Verify Cloudflare video before saving
    # -----------------------------------------------------

    def save_model(self, request, obj, form, change):

        uid = form.cleaned_data.get("cloudflare_upload_uid")

        if uid:
            pending = request.session.get(
                "pending_video_uploads",
                {},
            )

            upload = pending.get(uid)

            if (
                not upload
                or upload.get("user_id") != request.user.pk
                or upload.get("model") != "TopicsVideo"
            ):
                raise PermissionDenied(
                    "Unauthorised Cloudflare upload."
                )

            response = CloudflareStreamClient().get(
                f"/stream/{uid}"
            )

            if not response.get("success"):
                raise ValidationError(
                    "Cloudflare could not verify this video."
                )

            video = response.get("result", {})

            if video.get("uid") != uid:
                raise ValidationError(
                    "Cloudflare returned an unexpected video UID."
                )

            status = video.get(
                "status", {}
            ).get(
                "state", "pending"
            )

            if status == "error":
                raise ValidationError(
                    "Cloudflare reported a video processing error."
                )

            obj.cloudflare_uid = uid
            obj.cloudflare_status = status
            obj.video_file = None

        super().save_model(
            request,
            obj,
            form,
            change,
        )

        if uid:
            pending.pop(uid, None)

            request.session["pending_video_uploads"] = pending
            request.session.modified = True


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

    def save_model(self, request, obj, form, change):

        new_video = (
            "video_file" in form.changed_data
            and bool(obj.video_file)
        )

        # Αποθήκευση στο Django
        super().save_model(request, obj, form, change)

        if not new_video:
            return

        try:
            # Μεταφόρτωση χωρίς τοπική συμπίεση
            processor = VideoProcessor()

            result = processor.process(
                input_file=obj.video_file.path,
                meta={
                    "name": obj.activity_title or str(obj),
                },
            )

        except Exception:
            messages.error(
                request,
                "Η μεταφόρτωση στο Cloudflare απέτυχε. "
                "Το αρχικό αρχείο διατηρήθηκε για "
                "να μπορέσετε να δοκιμάσετε ξανά."
            )
            return

        # Αποθήκευση των στοιχείων Cloudflare
        obj.cloudflare_uid = result["uid"]
        obj.cloudflare_status = result["status"]
        obj.cloudflare_ready = result["ready"]

        # Αποθήκευση πριν από τη διαγραφή
        obj.save(
            update_fields=[
                "cloudflare_uid",
                "cloudflare_status",
                "cloudflare_ready",
            ]
        )

        # Αφαίρεση προσωρινού αρχείου
        obj.video_file.delete(save=True)

        messages.success(
            request,
            "Το βίντεο μεταφορτώθηκε στο Cloudflare."
        )
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
