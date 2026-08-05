def training_cloudinary_path(material):

    asset_folder = (
        f"Training Section/"
        f"{material.training_content.training.slug}/"
        f"{material.training_content.slug}"
    )

    public_id = material.slug

    return asset_folder, public_id