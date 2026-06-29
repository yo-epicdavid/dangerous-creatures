#!/usr/bin/env python3
"""Convert every PNG under web/assets/ to WebP (smaller, web-optimized) and remove the PNG.
Run AFTER the extract_* scripts and BEFORE the build_* scripts. Needs Pillow.
"""
import os, glob, sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.abspath(os.path.join(HERE, "..", "web", "assets"))


def dirsize(path):
    return sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(path) for f in fs)


def main():
    before = dirsize(ASSETS)
    pngs = glob.glob(os.path.join(ASSETS, "**", "*.png"), recursive=True)
    for i, p in enumerate(pngs, 1):
        im = Image.open(p).convert("RGB")
        im.save(p[:-4] + ".webp", "WEBP", quality=82, method=6)
        os.remove(p)
        if i % 100 == 0:
            print(f"  {i}/{len(pngs)}")
    after = dirsize(ASSETS)
    mb = lambda b: f"{b/1e6:.1f} MB"
    print(f"converted {len(pngs)} images. assets: {mb(before)} -> {mb(after)}")


if __name__ == "__main__":
    main()
