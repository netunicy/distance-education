from homepage.cloudflare.upload import CloudflareUploader


class VideoProcessor:

    def __init__(self):
        self.uploader = CloudflareUploader()

    def process(self, input_file, meta=None):

        if meta is None:
            meta = {}

        # ==========================================
        # Upload στο Cloudflare Stream
        # Χωρίς συμπίεση στο Render
        # ==========================================

        response = self.uploader.upload_video(
            file_path=str(input_file),
            meta=meta,
        )

        result = response["result"]

        return {
            "uid": result["uid"],
            "status": result["status"]["state"],
            "ready": result["readyToStream"],
        }