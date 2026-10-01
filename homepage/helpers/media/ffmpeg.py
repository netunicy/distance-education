
from pathlib import Path
import platform
import shutil

from django.conf import settings

BASE_DIR = Path(settings.BASE_DIR)

if platform.system() == "Windows":
    FFMPEG = BASE_DIR / "tools" / "ffmpeg" / "windows" / "ffmpeg.exe"
    FFPROBE = BASE_DIR / "tools" / "ffmpeg" / "windows" / "ffprobe.exe"
else:
    FFMPEG = shutil.which("ffmpeg") or (
        BASE_DIR / "tools" / "ffmpeg" / "linux" / "ffmpeg"
    )
    FFPROBE = shutil.which("ffprobe") or (
        BASE_DIR / "tools" / "ffmpeg" / "linux" / "ffprobe"
    )
