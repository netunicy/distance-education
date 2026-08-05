import time
import jwt
from django.conf import settings


def create_signed_playback_url(uid, expires_in=300):
    """
    Δημιουργεί Signed Playback URL για Cloudflare Stream.

    uid: Cloudflare Stream UID
    expires_in: Χρόνος λήξης σε δευτερόλεπτα (default 1 ώρα)
    """

    payload = {
        "sub": uid,
        "kid": settings.CLOUDFLARE_STREAM_KEY_ID,
        "exp": int(time.time()) + expires_in,
    }

    token = jwt.encode(
        payload,
        settings.CLOUDFLARE_STREAM_PRIVATE_KEY,
        algorithm="RS256",
        headers={
            "kid": settings.CLOUDFLARE_STREAM_KEY_ID,
        },
    )

    return (
        f"https://{settings.CLOUDFLARE_STREAM_CUSTOMER_SUBDOMAIN}/"
        f"{uid}/manifest/video.m3u8?token={token}"
    )