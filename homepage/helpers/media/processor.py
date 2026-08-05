from pathlib import Path
import tempfile

from .compressor import compress_video
from homepage.cloudflare.upload import CloudflareUploader


class VideoProcessor:

    def __init__(self):

        self.uploader = CloudflareUploader()

    def process(self, input_file, meta=None):

        if meta is None:
            meta = {}

        with tempfile.TemporaryDirectory() as temp_dir:

            temp_dir = Path(temp_dir)

            compressed_file = (
                temp_dir /
                f"{Path(input_file).stem}_compressed.mp4"
            )

            # ==========================
            # Συμπίεση
            # ==========================

            compress_video(
                input_file=input_file,
                output_file=compressed_file,
            )

            # ==========================
            # Upload στο Cloudflare Stream
            # ==========================

            response = self.uploader.upload_video(
                file_path=str(compressed_file),
                meta=meta,
            )

            result = response["result"]

            return {
                "uid": result["uid"],
                "status": result["status"]["state"],
                "ready": result["readyToStream"],
            }