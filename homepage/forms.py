from pathlib import Path
import tempfile
import uuid

from django import forms

from .models import TrainingVideo, SchoolVideo

from homepage.helpers.media.processor import VideoProcessor
from homepage.helpers.media.training_cloudinary_path import (
    training_cloudinary_path,
)


class TrainingVideoAdminForm(forms.ModelForm):

    class Meta:
        model = TrainingVideo
        fields = "__all__"

    def save(self, commit=True):

        obj = super().save(commit=False)

        if obj.pk is None:
            obj.save()

        if obj.video_file:

            processor = VideoProcessor()

            # Κρατάμε το παλιό UID
            old_uid = obj.cloudflare_uid

            with tempfile.TemporaryDirectory() as temp_dir:

                extension = Path(obj.video_file.name).suffix

                temp_input = (
                    Path(temp_dir) /
                    f"{uuid.uuid4()}{extension}"
                )

                with open(temp_input, "wb") as destination:

                    for chunk in obj.video_file.chunks():
                        destination.write(chunk)

                asset_folder, public_id = training_cloudinary_path(obj)

                response = processor.process(
                    input_file=temp_input,
                    meta={
                        "section": "Training",
                        "category": obj.training_content.training.category,
                        "level": obj.training_content.training.level,
                        "training": obj.training_content.training.slug,
                        "content": obj.training_content.slug,
                        "material": obj.slug,
                    }
                )

            # Αν το upload πέτυχε και υπήρχε παλιό video,
            # το διαγράφουμε από το Cloudflare.
            if old_uid:
                try:
                    processor.uploader.delete_video(old_uid)
                except Exception:
                    pass

            obj.cloudflare_uid = response["uid"]
            obj.cloudflare_status = response["status"]

            obj.video_file.delete(save=False)
            obj.video_file = None

            obj.save(
                update_fields=[
                    "cloudflare_uid",
                    "cloudflare_status",
                    "video_file",
                ]
            )

        return obj
class VideoAdminForm(forms.ModelForm):

    class Meta:
        model = SchoolVideo
        fields = "__all__"

    def save(self, commit=True):

        obj = super().save(commit=False)

        if obj.pk is None:
            obj.save()

        if obj.video_file:

            processor = VideoProcessor()

            # Κρατάμε το παλιό UID
            old_uid = obj.cloudflare_uid

            with tempfile.TemporaryDirectory() as temp_dir:

                extension = Path(obj.video_file.name).suffix

                temp_input = (
                    Path(temp_dir) /
                    f"{uuid.uuid4()}{extension}"
                )

                with open(temp_input, "wb") as destination:

                    for chunk in obj.video_file.chunks():
                        destination.write(chunk)

                response = processor.process(
                    input_file=temp_input,
                    meta={
                        "section": "Schools",
                        "subject": obj.chapter.context.subject_lesson,
                        "class": obj.chapter.context.class_is,
                        "book": obj.chapter.context.slug,
                        "chapter": obj.chapter.slug,
                        "video": obj.slug,
                    }
                )

            if old_uid:
                processor.uploader.delete_video(old_uid)

            obj.cloudflare_uid = response["uid"]
            obj.cloudflare_status = response["status"]

            obj.video_file.delete(save=False)
            obj.video_file = None

            obj.save(
                update_fields=[
                    "cloudflare_uid",
                    "cloudflare_status",
                    "video_file",
                ]
            )

        return obj