#!/usr/bin/env python3
"""Make favicon / Apple-touch / OG images from the Oceans title screen.
Source: DATA/ART_TTOV/TITL/TITL01KK.DIB (the clean octopus title). Outputs
public/{favicon.png, apple-touch-icon.png, og-cover.jpg}. Run with the venv Python (Pillow).
"""
import os, sys, tempfile, subprocess
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from szdd import expand

TITL = "/Volumes/MS_OCEANS/DATA/ART_TTOV/TITL"
APP = os.path.abspath(os.path.join(HERE, ".."))
PUB = os.path.join(APP, "public")
DN = subprocess.DEVNULL


def dib_img(dib):
    data = open(dib, "rb").read()
    if data[:4] == b"SZDD":
        data = expand(data)
    with tempfile.NamedTemporaryFile(suffix=".bmp", delete=False) as f:
        f.write(data); bmp = f.name
    png = bmp[:-4] + ".png"
    subprocess.run(["sips", "-s", "format", "png", bmp, "--out", png], stdout=DN, stderr=DN)
    im = Image.open(png).convert("RGB")
    os.remove(bmp); os.remove(png)
    return im


def main():
    os.makedirs(PUB, exist_ok=True)
    title = dib_img(os.path.join(TITL, "TITL01KK.DIB"))   # 640x408 clean octopus title
    W, H = title.size

    # favicon / apple-touch: a centered square on the octopus
    s = 360
    sq = title.crop(((W - s) // 2, (H - s) // 2, (W - s) // 2 + s, (H - s) // 2 + s))
    sq.resize((512, 512), Image.LANCZOS).save(os.path.join(PUB, "favicon.png"))
    sq.resize((180, 180), Image.LANCZOS).save(os.path.join(PUB, "apple-touch-icon.png"))

    # OG: scale to 1200 wide, center-crop to 1200x630
    og = title.resize((1200, round(H * 1200 / W)), Image.LANCZOS)
    top = max(0, (og.height - 630) // 2)
    og.crop((0, top, 1200, top + 630)).save(os.path.join(PUB, "og-cover.jpg"), "JPEG", quality=88)
    print("wrote", sorted(os.listdir(PUB)))


if __name__ == "__main__":
    main()
