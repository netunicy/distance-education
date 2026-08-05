import os
import json
from .client import CloudflareStreamClient


class CloudflareUploader:

    def __init__(self):
        self.client = CloudflareStreamClient()

    def upload_video(self, file_path, meta=None):

        if meta is None:
            meta = {}

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

        if not response["success"]:
            raise Exception(response)

        return response
    
    def delete_video(self, uid):
        try:
            response = self.client.delete(
                f"/stream/{uid}"
            )
            return response
        except Exception:
            # Το video δεν υπάρχει ήδη στο Cloudflare.
            return None