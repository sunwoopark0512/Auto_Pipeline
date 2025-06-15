import subprocess
import textwrap
import os
import uuid
import pathlib

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def render_short(text: str, output_dir: str = "media") -> str:
    pathlib.Path(output_dir).mkdir(exist_ok=True)
    video_id = str(uuid.uuid4())
    outfile = f"{output_dir}/{video_id}.mp4"
    wrapped = textwrap.fill(text, 40)
    cmd = [
        "ffmpeg",
        "-f",
        "lavfi",
        "-i",
        "color=c=black:s=720x1280:d=20",
        "-vf",
        f"drawtext=fontsize=40:fontfile={FONT}:fontcolor=white:text='{wrapped}':x=(w-text_w)/2:y=(h-text_h)/2",
        "-y",
        outfile,
    ]
    subprocess.run(cmd, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    return outfile
