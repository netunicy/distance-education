import subprocess
from pathlib import Path

from homepage.helpers.media.ffmpeg import FFMPEG


VIDEO_CRF = 23
VIDEO_PRESET = "slow"


def compress_video(input_file, output_file):
    """
    Συμπιέζει ένα video με το FFmpeg.

    Args:
        input_file:
            Η διαδρομή του αρχικού video.

        output_file:
            Η διαδρομή του συμπιεσμένου video.

    Returns:
        Η διαδρομή του συμπιεσμένου video.
    """

    if not Path(FFMPEG).exists():
        raise RuntimeError(
            f"Το FFmpeg δεν βρέθηκε στη διαδρομή:\n{FFMPEG}"
        )

    input_file = str(Path(input_file))
    output_file = str(Path(output_file))

    command = [
        str(FFMPEG),

        "-i", input_file,

        # Video
        "-c:v", "libx264",
        "-preset", VIDEO_PRESET,
        "-crf", str(VIDEO_CRF),

        # Audio
        "-c:a", "aac",
        "-b:a", "128k",

        # Overwrite αν υπάρχει ήδη
        "-y",

        output_file,
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        check=False,
    )

    if result.returncode != 0:

        raise RuntimeError(
            result.stderr.decode(errors="ignore")
        )

    return output_file