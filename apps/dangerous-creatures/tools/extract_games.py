#!/usr/bin/env python3
"""Extract mini-game image assets. Title/UI screens are SZDD-compressed; the puzzle
clue/reveal images are plain BMPs. This converts either to PNG.

Currently handles the EYES game ("Whose eyes are these?"): CLOS{NN}A = eyes close-up clue,
CLOS{NN}B = full-animal reveal. Output: web/assets/games/eyes/*.png
"""
import os, sys, glob, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "packages", "pipeline"))
from szdd import expand, MAGIC

DISC = "/Volumes/DANGEROUS"
WEB = os.path.abspath(os.path.join(HERE, "..", "web"))
DN = subprocess.DEVNULL


def convert(src, dst):
    with open(src, "rb") as f:
        head = f.read(8)
    if head == MAGIC:                       # SZDD-compressed -> expand first
        tmp = dst[:-4] + ".bmp"
        with open(src, "rb") as f:
            data = expand(f.read())
        with open(tmp, "wb") as f:
            f.write(data)
        subprocess.run(["sips", "-s", "format", "png", tmp, "--out", dst], stdout=DN, stderr=DN, check=False)
        os.remove(tmp)
    else:                                   # plain BMP
        subprocess.run(["sips", "-s", "format", "png", src, "--out", dst], stdout=DN, stderr=DN, check=False)


def extract_eyes():
    src = os.path.join(DISC, "GAME", "EYES00AA")
    out = os.path.join(WEB, "assets", "games", "eyes")
    os.makedirs(out, exist_ok=True)
    convert(os.path.join(src, "EYES00AA.DIB"), os.path.join(out, "title.png"))
    n = 0
    for dib in sorted(glob.glob(os.path.join(src, "CLOS*.DIB"))):
        stem = os.path.splitext(os.path.basename(dib))[0]   # CLOS01A
        convert(dib, os.path.join(out, stem + ".png"))
        n += 1
    print(f"EYES: title + {n} clue/reveal images -> {out}")


if __name__ == "__main__":
    extract_eyes()
