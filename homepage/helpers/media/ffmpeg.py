from pathlib import Path
import platform

from django.conf import settings

BASE_DIR = Path(settings.BASE_DIR)

if platform.system() == "Windows":

    FFMPEG = BASE_DIR / "tools" / "ffmpeg" / "windows" / "ffmpeg.exe"
    FFPROBE = BASE_DIR / "tools" / "ffmpeg" / "windows" / "ffprobe.exe"

else:

    FFMPEG = BASE_DIR / "tools" / "ffmpeg" / "linux" / "ffmpeg"
    FFPROBE = BASE_DIR / "tools" / "ffmpeg" / "linux" / "ffprobe"