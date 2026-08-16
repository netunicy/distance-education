def topics_cloudinary_path(material):

    asset_folder = (
        f"Topics Section/"
        f"{material.topics_content.topics.slug}/"
        f"{material.topics_content.slug}"
    )

    public_id = material.slug

    return asset_folder, public_id