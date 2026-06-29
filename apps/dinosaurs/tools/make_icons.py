#!/usr/bin/env python3
"""Make favicon / Apple-touch / OG images from the Dinosaurs title screen.
Source: DIBS/TITL00NV.BMP (raw BMP — the "Microsoft Dinosaurs" T. rex title). Outputs
public/{favicon.png, apple-touch-icon.png, og-cover.jpg}. Run with the venv Python (Pillow).
"""
import os, tempfile, subprocess
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.abspath(os.path.join(HERE, ".."))
PUB = os.path.join(APP, "public")
TITLE = "/Volumes/DINOSAURS/DIBS/TITL00NV.BMP"
DN = subprocess.DEVNULL


def load(bmp):
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        png = f.name
    subprocess.run(["sips", "-s", "format", "png", bmp, "--out", png], stdout=DN, stderr=DN)
    im = Image.open(png).convert("RGB")
    os.remove(png)
    return im


def main():
    os.makedirs(PUB, exist_ok=True)
    title = load(TITLE)
    W, H = title.size

    # favicon / apple-touch: a square on the T. rex (upper-centre of the title)
    s = int(H * 0.82)
    x = (W - s) // 2
    sq = title.crop((x, 0, x + s, s))
    sq.resize((512, 512), Image.LANCZOS).save(os.path.join(PUB, "favicon.png"))
    sq.resize((180, 180), Image.LANCZOS).save(os.path.join(PUB, "apple-touch-icon.png"))

    # OG: scale to 1200 wide, centre-crop to 1200x630
    og = title.resize((1200, round(H * 1200 / W)), Image.LANCZOS)
    top = max(0, (og.height - 630) // 2)
    og.crop((0, top, 1200, top + 630)).save(os.path.join(PUB, "og-cover.jpg"), "JPEG", quality=88)
    print("title", (W, H), "-> wrote", sorted(os.listdir(PUB)))


if __name__ == "__main__":
    main()
