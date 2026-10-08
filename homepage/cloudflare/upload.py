import os
import logging

from .client import CloudflareStreamClient


logger = logging.getLogger(__name__)


class CloudflareUploader:

    # 5 MiB - συμβατό μέγεθος τμήματος για Cloudflare TUS.
    CHUNK_SIZE = 5 * 1024 * 1024

    def __init__(self):
        self.client = CloudflareStreamClient()

    def upload_video(self, file_path, meta=None):

        if meta is None:
            meta = {}

        file_size = os.path.getsize(file_path)

        if file_size <= 0:
            raise ValueError("Video file is empty.")

        # Δημιουργία συνεδρίας TUS.
        # Δεν πραγματοποιείται τοπική συμπίεση.

        session = self.client.create_tus_upload(
            file_size=file_size,
            meta=meta,
        )

        upload_url = session["upload_url"]
        uid = session["uid"]

        logger.info(
            "CLOUDFLARE TUS UPLOAD STARTED: %s",
            uid,
        )

        # Μεταφόρτωση του αρχικού αρχείου σε τμήματα.

        offset = 0

        with open(file_path, "rb") as video:

            while offset < file_size:

                video.seek(offset)

                chunk = video.read(self.CHUNK_SIZE)

                if not chunk:
                    raise RuntimeError(
                        "Unexpected end of video file."
                    )

                new_offset = self.client.upload_tus_chunk(
                    upload_url=upload_url,
                    chunk=chunk,
                    offset=offset,
                )

                if not (
                    offset < new_offset <= offset + len(chunk)
                ):
                    raise RuntimeError(
                        "Invalid Cloudflare TUS upload offset."
                    )

                offset = new_offset

                logger.info(
                    "CLOUDFLARE UPLOAD PROGRESS: %s/%s",
                    offset,
                    file_size,
                )

        if offset != file_size:
            raise RuntimeError(
                "Cloudflare video upload incomplete."
            )

        logger.warning(
            "CLOUDFLARE VIDEO UPLOADED: %s",
            uid,
        )

        # Επαλήθευση προστασίας Signed URLs.
        # Η προστασία ζητήθηκε ήδη κατά τη δημιουργία TUS.

        try:

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

            logger.warning(
                "CLOUDFLARE SIGNED URL VERIFIED: %s",
                uid,
            )

        except Exception:

            logger.exception(
                "Cloudflare protection failed for UID: %s",
                uid,
            )

            raise

        logger.info(
            "Cloudflare video protected: %s",
            uid,
        )

        # Ίδια δομή επιστροφής με την προηγούμενη υλοποίηση,
        # ώστε να παραμείνει συμβατό το VideoProcessor.

        return {
            "success": True,
            "result": verified_video,
        }

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