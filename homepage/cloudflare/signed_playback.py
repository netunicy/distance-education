
import time
import jwt

from django.conf import settings


def create_signed_playback_url(uid, expires_in=3600):
    """
    Δημιουργεί προστατευμένο Cloudflare Stream HLS URL.

    uid: Cloudflare Stream video UID
    expires_in: Χρόνος λήξης του token σε δευτερόλεπτα
                (προεπιλογή: 1 ώρα)
    """

    if not uid:
        raise ValueError("Cloudflare video UID is missing.")

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
        f"{token}/manifest/video.m3u8"
    )
