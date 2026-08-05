def video_cloudinary_path(video):

    asset_folder = (
        f"Schools Section/"
        f"{video.chapter.context.slug}/"
        f"{video.chapter.slug}"
    )

    public_id = video.slug

    return asset_folder, public_id