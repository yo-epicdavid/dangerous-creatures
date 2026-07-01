#!/usr/bin/env python3
"""Phase 1: turn the walkthrough video into a set of unique screen keyframes.

1. Extract a frame at each scene cut (ffmpeg scene detection) + its timestamp.
2. De-duplicate near-identical frames with a perceptual hash (dHash).
Outputs <out>/keyframes/*.jpg (deduped) and <out>/keyframes.json (file, time, hash).

Needs ffmpeg + Pillow + imagehash. Usage:
  python tools/map_walkthrough.py _source/walkthrough/walkthrough.mp4 _source/walkthrough [scene_thresh] [hash_dist]
"""
import os, re, sys, glob, json, shutil, subprocess
from PIL import Image
import imagehash

FF = "/opt/homebrew/bin/ffmpeg"


def extract(video, raw_dir, thresh):
    os.makedirs(raw_dir, exist_ok=True)
    meta = os.path.join(raw_dir, "scenes.txt")
    # one frame per scene cut; log each kept frame's pts_time to meta
    subprocess.run([
        FF, "-y", "-i", video,
        "-vf", f"select='gt(scene,{thresh})',metadata=print:file={meta}",
        "-vsync", "vfr", "-q:v", "3", os.path.join(raw_dir, "%05d.jpg"),
    ], check=False)
    times = [float(t) for t in re.findall(r"pts_time:([\d.]+)", open(meta).read())]
    frames = sorted(glob.glob(os.path.join(raw_dir, "*.jpg")))
    # pad/truncate times to frames just in case
    while len(times) < len(frames):
        times.append(times[-1] if times else 0.0)
    return list(zip(frames, times))


def dedupe(frames_times, out_dir, dist):
    os.makedirs(out_dir, exist_ok=True)
    kept, last = [], None
    for f, t in frames_times:
        try:
            h = imagehash.dhash(Image.open(f), hash_size=12)
        except Exception:
            continue
        if last is not None and (h - last) <= dist:
            continue  # too similar to the last kept screen
        last = h
        kept.append({"time": round(t, 2), "hash": str(h), "src": f})
    manifest = []
    for i, k in enumerate(kept):
        name = f"{i:04d}_{int(k['time'])}s.jpg"
        shutil.copy(k["src"], os.path.join(out_dir, name))
        manifest.append({"i": i, "file": f"keyframes/{name}", "time": k["time"], "hash": k["hash"]})
    return manifest


def main():
    video = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.dirname(video)
    thresh = float(sys.argv[3]) if len(sys.argv) > 3 else 0.30
    dist = int(sys.argv[4]) if len(sys.argv) > 4 else 8
    raw = os.path.join(out, "_raw_frames")
    print(f"extracting scene-cut frames (thresh={thresh})…")
    ft = extract(video, raw, thresh)
    print(f"  {len(ft)} scene frames")
    print(f"de-duplicating (hash dist<= {dist})…")
    manifest = dedupe(ft, os.path.join(out, "keyframes"), dist)
    json.dump(manifest, open(os.path.join(out, "keyframes.json"), "w"), indent=2)
    print(f"  {len(manifest)} unique screens -> {out}/keyframes/  (+ keyframes.json)")
    shutil.rmtree(raw, ignore_errors=True)


if __name__ == "__main__":
    main()
