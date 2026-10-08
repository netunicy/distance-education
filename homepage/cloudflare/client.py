import requests

from django.conf import settings


class CloudflareStreamClient:

    BASE_URL = "https://api.cloudflare.com/client/v4"

    def __init__(self):

        self.account_id = settings.CLOUDFLARE_ACCOUNT_ID

        self.base_url = (
            f"{self.BASE_URL}/accounts/{self.account_id}"
        )

        self.headers = {
            "Authorization": f"Bearer {settings.CLOUDFLARE_API_TOKEN}",
        }

    def get(self, endpoint):

        response = requests.get(
            self.base_url + endpoint,
            headers=self.headers,
            timeout=30,
        )

        response.raise_for_status()

        return response.json()

    def post(self, endpoint, json=None):

        response = requests.post(
            self.base_url + endpoint,
            headers=self.headers,
            json=json,
            timeout=30,
        )

        response.raise_for_status()

        return response.json()

    def upload(self, endpoint, files=None, data=None):

        response = requests.post(
            self.base_url + endpoint,
            headers=self.headers,
            files=files,
            data=data,
            timeout=600,
        )

        response.raise_for_status()

        return response.json()

    def put(self, endpoint, json=None):

        response = requests.put(
            self.base_url + endpoint,
            headers=self.headers,
            json=json,
            timeout=30,
        )

        response.raise_for_status()

        return response.json()

    def delete(self, endpoint):

        response = requests.delete(
            self.base_url + endpoint,
            headers=self.headers,
            timeout=30,
        )

        response.raise_for_status()

        return response.json()

    
    def create_tus_upload(self, file_size, meta=None):

        import base64

        if not isinstance(file_size, int) or file_size <= 0:
            raise ValueError("Invalid video file size.")

        if meta is None:
            meta = {}

        metadata = {
            "requiresignedurls": "true",
            "maxDurationSeconds": "600",
        }

        if meta.get("name"):
            metadata["name"] = str(meta["name"])

        encoded_metadata = ",".join(
            f"{key} {base64.b64encode(value.encode('utf-8')).decode('ascii')}"
            for key, value in metadata.items()
        )

        headers = {
            **self.headers,
            "Tus-Resumable": "1.0.0",
            "Upload-Length": str(file_size),
            "Upload-Metadata": encoded_metadata,
        }

        response = requests.post(
            self.base_url + "/stream",
            headers=headers,
            timeout=30,
        )

        response.raise_for_status()

        upload_url = response.headers.get("Location")
        uid = response.headers.get("stream-media-id")

        if not upload_url or not uid:
            raise RuntimeError(
                "Cloudflare did not return the upload URL or UID."
            )

        return {
            "upload_url": upload_url,
            "uid": uid,
        }

    def upload_tus_chunk(self, upload_url, chunk, offset):

        headers = {
            **self.headers,
            "Tus-Resumable": "1.0.0",
            "Upload-Offset": str(offset),
            "Content-Type": "application/offset+octet-stream",
        }

        response = requests.patch(
            upload_url,
            headers=headers,
            data=chunk,
            timeout=600,
        )

        response.raise_for_status()

        new_offset = response.headers.get("Upload-Offset")

        if new_offset is None:
            raise RuntimeError(
                "Cloudflare did not return Upload-Offset."
            )

        return int(new_offset)