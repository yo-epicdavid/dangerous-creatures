#!/usr/bin/env python3
"""Batch-extract every animal from the Dangerous Creatures disc.

For each ANIMAL/<CODE>00AA folder:
  - expand all SZDD .DIB screens -> PNG (web/assets/<slug>/<STEM>.png)
  - transcode article narration  -> narration.mp3
  - transcode the video clip      -> clip.mp4
Writes web/extracted-manifest.json describing what each animal has.

Deterministic + idempotent. Run: python3 tools/extract_all.py
"""
import os, sys, glob, json, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from szdd import expand

DISC = "/Volumes/DANGEROUS"
ANIMAL_DIR = os.path.join(DISC, "ANIMAL")
OUT_ROOT = os.path.abspath(os.path.join(HERE, "..", "web", "assets"))
MANIFEST = os.path.abspath(os.path.join(HERE, "..", "web", "extracted-manifest.json"))
FFMPEG = "/opt/homebrew/bin/ffmpeg"


def dib_to_png(dib, png):
    tmp = png[:-4] + ".bmp"
    with open(dib, "rb") as f:
        data = expand(f.read())
    with open(tmp, "wb") as f:
        f.write(data)
    subprocess.run(["sips", "-s", "format", "png", tmp, "--out", png],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
    os.remove(tmp)


def main():
    manifest = {}
    folders = sorted(d for d in os.listdir(ANIMAL_DIR) if os.path.isdir(os.path.join(ANIMAL_DIR, d)))
    for folder in folders:
        base = folder[:4]                       # e.g. LION
        slug = base.lower()
        src = os.path.join(ANIMAL_DIR, folder)
        out = os.path.join(OUT_ROOT, slug)
        os.makedirs(out, exist_ok=True)

        screens = []
        for dib in sorted(glob.glob(os.path.join(src, "*.DIB"))):
            stem = os.path.splitext(os.path.basename(dib))[0]   # LION00AA
            png = os.path.join(out, stem + ".png")
            try:
                dib_to_png(dib, png)
                screens.append(stem)
            except Exception as e:
                print(f"  !! {stem}: {e}")

        narration = None
        at = glob.glob(os.path.join(DISC, "AAARTCLE", "*", base + "00AT.WAV"))
        if at:
            mp3 = os.path.join(out, "narration.mp3")
            subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-i", at[0],
                            "-codec:a", "libmp3lame", "-q:a", "4", mp3], check=False)
            narration = "narration.mp3"

        video = None
        avi = glob.glob(os.path.join(DISC, "VFW", "**", base + "*TV.AVI"), recursive=True)
        if avi:
            mp4 = os.path.join(out, "clip.mp4")
            subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-i", avi[0],
                            "-movflags", "+faststart", "-pix_fmt", "yuv420p",
                            "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2", mp4], check=False)
            video = "clip.mp4"

        manifest[slug] = {"code": base, "folder": folder, "screens": screens,
                          "narration": narration, "video": video}
        print(f"{slug:18} screens={len(screens):2}  narration={'Y' if narration else '-'}  video={'Y' if video else '-'}")

    with open(MANIFEST, "w") as f:
        json.dump(manifest, f, indent=2)
    n_vid = sum(1 for m in manifest.values() if m["video"])
    n_nar = sum(1 for m in manifest.values() if m["narration"])
    print(f"\nDONE: {len(manifest)} animals  ({n_nar} narrations, {n_vid} videos)  ->  {MANIFEST}")


if __name__ == "__main__":
    main()
