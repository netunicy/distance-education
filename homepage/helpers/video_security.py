from cloudinary.utils import cloudinary_url


def create_secure_url(public_id):

    secure_url, _ = cloudinary_url(
        public_id,
        sign_url=True,
        resource_type="video",
        format="m3u8",
        transformation=[
            {
                "streaming_profile": "full_hd",
            }
        ],
    )

    return secure_url