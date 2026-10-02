
import os
import json
import logging

from .client import CloudflareStreamClient


logger = logging.getLogger(__name__)


class CloudflareUploader:

    def __init__(self):
        self.client = CloudflareStreamClient()

    def upload_video(self, file_path, meta=None):

        if meta is None:
            meta = {}

        # Αποστολή του αρχικού αρχείου.
        # Καμία συμπίεση στο Render.

        with open(file_path, "rb") as video:

            files = {
                "file": (
                    os.path.basename(file_path),
                    video,
                    "video/mp4",
                )
            }

            data = {
                "meta": json.dumps(meta),
                "requireSignedURLs": "true",
            }

            response = self.client.upload(
                "/stream",
                files=files,
                data=data,
            )

        if not response.get("success"):
            raise RuntimeError(
                "Cloudflare video upload failed."
            )

        result = response.get("result") or {}
        uid = result.get("uid")

        if not uid:
            raise RuntimeError(
                "Cloudflare did not return a video UID."
            )

        # Ενεργοποίηση της προστασίας.
        # Το UID καταγράφεται για πιθανή ανάκτηση.

        try:
            update = self.client.post(
                f"/stream/{uid}",
                json={
                    "requireSignedURLs": True,
                },
            )

            if not update.get("success"):
                raise RuntimeError(
                    "Cloudflare rejected signed URL protection."
                )

            # Ανεξάρτητη επαλήθευση.

            verification = self.client.get(
                f"/stream/{uid}"
            )

            if not verification.get("success"):
                raise RuntimeError(
                    "Cloudflare verification failed."
                )

            verified_video = (
                verification.get("result") or {}
            )

            if (
                verified_video.get("uid") != uid
                or verified_video.get("requireSignedURLs")
                is not True
            ):
                raise RuntimeError(
                    "Signed URL protection was not confirmed."
                )

        except Exception:
            logger.exception(
                "Cloudflare protection failed for UID: %s",
                uid,
            )
            raise

        # Επιστρέφουμε τα επαληθευμένα στοιχεία.

        response["result"] = verified_video

        logger.info(
            "Cloudflare video protected: %s",
            uid,
        )

        return response

    def delete_video(self, uid):

        try:
            return self.client.delete(
                f"/stream/{uid}"
            )

        except Exception:
            logger.exception(
                "Cloudflare video deletion failed: %s",
                uid,
            )
            return None
