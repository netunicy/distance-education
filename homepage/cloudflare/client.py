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