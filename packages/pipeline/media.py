#!/usr/bin/env python3
"""Shared media steps for the disc→site pipeline, used by every app's tools/.

- to_webp(assets_dir)     : convert every PNG under an app's web/assets to WebP, drop the PNG
- make_posters(assets_dir): write a poster.webp (a representative video frame) next to each clip.mp4

The per-app tools/convert_to_webp.py and tools/make_video_posters.py are thin wrappers that
call these against their own web/assets. szdd.py (SZDD/LZSS decompressor) also lives here.
Needs Pillow; make_posters needs ffmpeg.
"""
import os
import glob

FFMPEG = "/opt/homebrew/bin/ffmpeg"


def _dirsize(path):
    return sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(path) for f in fs)


def to_webp(assets_dir, quality=82, method=6):
    """Convert every PNG under assets_dir to WebP and remove the PNG. Idempotent: re-running
    after the PNGs are gone is a no-op."""
    from PIL import Image
    before = _dirsize(assets_dir)
    pngs = glob.glob(os.path.join(assets_dir, "**", "*.png"), recursive=True)
    for i, p in enumerate(pngs, 1):
        Image.open(p).convert("RGB").save(p[:-4] + ".webp", "WEBP", quality=quality, method=method)
        os.remove(p)
        if i % 100 == 0:
            print(f"  {i}/{len(pngs)}")
    after = _dirsize(assets_dir)
    mb = lambda b: f"{b/1e6:.1f} MB"
    print(f"converted {len(pngs)} images. assets: {mb(before)} -> {mb(after)}")


def make_posters(assets_dir, ffmpeg=FFMPEG, quality=82, method=6):
    """Generate poster.webp (ffmpeg picks a representative frame) for each clip.mp4 directly
    under assets_dir/*/. Far better than the original composite 'TV' screens."""
    import tempfile
    import subprocess
    DN = subprocess.DEVNULL
    n = 0
    for clip in sorted(glob.glob(os.path.join(assets_dir, "*", "clip.mp4"))):
        out = os.path.join(os.path.dirname(clip), "poster.webp")
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tf:
            tmp = tf.name
        subprocess.run([ffmpeg, "-y", "-loglevel", "error", "-i", clip, "-vf", "thumbnail", "-frames:v", "1", tmp],
                       stdout=DN, stderr=DN, check=False)
        if os.path.getsize(tmp) > 0:
            from PIL import Image
            Image.open(tmp).convert("RGB").save(out, "WEBP", quality=quality, method=method)
            n += 1
        os.remove(tmp)
    print(f"wrote {n} video posters (poster.webp) -> {assets_dir}/*/")
