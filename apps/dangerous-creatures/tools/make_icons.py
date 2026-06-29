#!/usr/bin/env python3
"""Generate favicon + OG image from the original box cover (_source/cover.jpg).
Needs Pillow. Writes into public/ (copied to dist by Astro).
"""
import os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
COVER = os.path.join(ROOT, "_source", "cover.jpg")
PUBLIC = os.path.join(ROOT, "public")
BG = (27, 23, 20)  # --bg

cover = Image.open(COVER).convert("RGB")

# favicon: square crop on the roaring grizzly
bear = cover.crop((180, 300, 620, 740))
bear.resize((64, 64), Image.LANCZOS).save(os.path.join(PUBLIC, "favicon.png"))
bear.resize((180, 180), Image.LANCZOS).save(os.path.join(PUBLIC, "apple-touch-icon.png"))

# OG image: 1200x630, full cover "contained" on the theme background
W, H = 1200, 630
canvas = Image.new("RGB", (W, H), BG)
cw, ch = cover.size
scale = min(W / cw, H / ch)
nw, nh = int(cw * scale), int(ch * scale)
canvas.paste(cover.resize((nw, nh), Image.LANCZOS), ((W - nw) // 2, (H - nh) // 2))
canvas.save(os.path.join(PUBLIC, "og-cover.jpg"), quality=86)

print("wrote public/favicon.png, apple-touch-icon.png, og-cover.jpg")
