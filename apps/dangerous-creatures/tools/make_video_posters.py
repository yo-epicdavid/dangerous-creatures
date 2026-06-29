#!/usr/bin/env python3
"""Generate a real video-frame poster for each clip.mp4 (ffmpeg picks a representative
frame; PIL writes WebP since this ffmpeg lacks a webp encoder). Output: web/assets/<slug>/poster.webp
Run with the venv python (needs Pillow). Far better than the original 'TV' composite screens,
which are inconsistent content pages.
"""
import os, glob, subprocess, tempfile
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.abspath(os.path.join(HERE, "..", "web", "assets"))
FF = "/opt/homebrew/bin/ffmpeg"
DN = subprocess.DEVNULL


def main():
    n = 0
    for clip in sorted(glob.glob(os.path.join(ASSETS, "*", "clip.mp4"))):
        out = os.path.join(os.path.dirname(clip), "poster.webp")
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tf:
            tmp = tf.name
        subprocess.run([FF, "-y", "-loglevel", "error", "-i", clip, "-vf", "thumbnail", "-frames:v", "1", tmp],
                       stdout=DN, stderr=DN, check=False)
        if os.path.getsize(tmp) > 0:
            Image.open(tmp).convert("RGB").save(out, "WEBP", quality=82, method=6)
            n += 1
        os.remove(tmp)
    print(f"wrote {n} video posters (poster.webp) -> web/assets/*/")


if __name__ == "__main__":
    main()
