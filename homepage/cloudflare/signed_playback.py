
from django.conf import settings

from .client import CloudflareStreamClient


def create_signed_playback_url(uid, expires_in=3600):

    if not uid:
        raise ValueError("Cloudflare video UID is missing.")

    client = CloudflareStreamClient()

    response = client.post(
        f"/stream/{uid}/token"
    )

    if not response.get("success"):
        raise RuntimeError(
            "Cloudflare failed to generate playback token."
        )

    token = response.get("result", {}).get("token")

    if not token:
        raise RuntimeError(
            "Cloudflare did not return a playback token."
        )

    customer_domain = (
        settings.CLOUDFLARE_STREAM_CUSTOMER_SUBDOMAIN
    ).strip().removeprefix("https://").rstrip("/")

    return (
        f"https://{customer_domain}/"
        f"{token}/manifest/video.m3u8"
    )
