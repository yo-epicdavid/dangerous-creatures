#!/usr/bin/env python3
"""Refine Classic-mode hotspot boxes by snapping each to the red label text near its
vision-estimated seed position. Writes tools/hotspots_refined.json (slug -> label -> %box),
which build_data.py applies. Run with `--preview <slug>` to render an overlay instead.

Uses Pillow + numpy (run with the scratchpad venv python).
"""
import os, sys, json, glob
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.abspath(os.path.join(HERE, "..", "web"))
DATA = os.path.join(WEB, "data")
OUT = os.path.join(HERE, "hotspots_refined.json")


def red_mask(arr):
    R, G, B = arr[..., 0], arr[..., 1], arr[..., 2]
    # the label red is highly saturated (e.g. [232,66,37]); reject warm fur ([199,103,24])
    # by demanding a low green channel and a large R-G gap.
    return (R > 165) & (R - G > 105) & (R - B > 120) & (G < 105) & (B < 95)


def trim(sub):
    """Tight bbox of red pixels in a window, trimming sparse stray columns/rows."""
    ys, xs = np.where(sub)
    if len(xs) < 14:
        return None
    colc = sub.sum(axis=0)
    rowc = sub.sum(axis=1)
    cthr = max(1, 0.12 * colc.max())
    rthr = max(1, 0.12 * rowc.max())
    cols = np.where(colc >= cthr)[0]
    rows = np.where(rowc >= rthr)[0]
    if len(cols) == 0 or len(rows) == 0:
        return None
    return int(cols.min()), int(rows.min()), int(cols.max()), int(rows.max())


def refine_box(mask, seed_px, W, H):
    sx, sy, sw, sh = seed_px
    mx, my = int(0.06 * W), int(0.05 * H)
    x0, y0 = max(0, sx - mx), max(0, sy - my)
    x1, y1 = min(W, sx + sw + mx), min(H, sy + sh + my)
    box = trim(mask[y0:y1, x0:x1])
    if not box:
        return None
    bx0, by0, bx1, by1 = box
    return x0 + bx0, y0 + by0, x0 + bx1, y0 + by1


def process(slug, preview=False):
    d = json.load(open(os.path.join(DATA, f"{slug}.json")))
    main = d.get("classic", {}).get("screens", {}).get("main", {})
    hotspots = main.get("hotspots", [])
    img_path = os.path.join(WEB, main.get("image", ""))
    if not hotspots or not os.path.exists(img_path):
        return None
    img = Image.open(img_path).convert("RGB")
    W, H = img.size
    arr = np.asarray(img).astype(int)
    mask = red_mask(arr)
    pad_x, pad_y = 0.006 * W, 0.012 * H
    refined = {}
    draw = ImageDraw.Draw(img) if preview else None
    for h in hotspots:
        seed = (int(h["x"] / 100 * W), int(h["y"] / 100 * H), int(h["w"] / 100 * W), int(h["h"] / 100 * H))
        if preview:
            draw.rectangle([seed[0], seed[1], seed[0] + seed[2], seed[1] + seed[3]], outline=(255, 230, 0), width=2)
        box = refine_box(mask, seed, W, H)
        if not box:
            continue
        bx0, by0, bx1, by1 = box
        # guard: a label is small text; if the detected box ballooned, keep the estimate
        if (by1 - by0) / H * 100 > 9 or (bx1 - bx0) / W * 100 > 45:
            continue
        bx0 = max(0, bx0 - pad_x); by0 = max(0, by0 - pad_y); bx1 = min(W, bx1 + pad_x); by1 = min(H, by1 + pad_y)
        if preview:
            draw.rectangle([bx0, by0, bx1, by1], outline=(60, 255, 90), width=2)
        refined[h["label"]] = {
            "x": round(bx0 / W * 100, 2), "y": round(by0 / H * 100, 2),
            "w": round((bx1 - bx0) / W * 100, 2), "h": round((by1 - by0) / H * 100, 2),
        }
    if preview:
        out = f"/private/tmp/claude-502/-Users-ddomingo-Code-Personal-dangerous-creatures-web/b5ad2477-e56e-4263-bb27-a4c153210c64/scratchpad/refine_{slug}.png"
        img.save(out)
        print(f"preview -> {out}  ({len(refined)}/{len(hotspots)} snapped)")
    return refined


def main():
    if len(sys.argv) > 2 and sys.argv[1] == "--preview":
        process(sys.argv[2], preview=True)
        return
    allref = {}
    total = snapped = 0
    for fp in sorted(glob.glob(os.path.join(DATA, "*.json"))):
        slug = os.path.basename(fp)[:-5]
        if slug in ("index", "browse", "quiz", "guides", "games_eyes"):
            continue
        r = process(slug)
        if r:
            allref[slug] = r
            d = json.load(open(fp))
            total += len(d["classic"]["screens"]["main"]["hotspots"])
            snapped += len(r)
    json.dump(allref, open(OUT, "w"), indent=2)
    print(f"wrote {OUT}: refined {snapped}/{total} hotspots across {len(allref)} animals")


if __name__ == "__main__":
    main()
