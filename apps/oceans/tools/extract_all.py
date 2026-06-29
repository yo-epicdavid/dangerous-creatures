#!/usr/bin/env python3
"""Extract Microsoft Oceans (1995) disc content.

Oceans co-locates each topic in DATA/ART_<range>/<CODE>/:
  <CODE>00AA.DIB        main screen
  <CODE>NNPU.DIB        sub-topic screens
  <CODE>07PV.DIB/.AVI   video still + clip
  <CODE>NNJN.WAV        per-screen narration (00 = main hook, NN = sub-topics/video)
  <CODE>NNQN.WAV        spoken answer / fuller explanation
  <CODE>00IX.WAV        ambient / creature sound

All DIB are SZDD-compressed (same engine as Dangerous Creatures). Disc mounted at
/Volumes/MS_OCEANS. Outputs PNGs + MP3s + clip.mp4 into ../web/assets/<slug>/ and a
../web/extracted-manifest.json describing every entry.
"""
import os, sys, glob, json, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from szdd import expand

DISC = "/Volumes/MS_OCEANS/DATA"
WEB = os.path.abspath(os.path.join(HERE, "..", "web"))
OUT_ROOT = os.path.join(WEB, "assets")
FF = "/opt/homebrew/bin/ffmpeg"
DN = subprocess.DEVNULL


def dib_to_png(dib, png):
    with open(dib, "rb") as f:
        data = f.read()
    if data[:4] == b"SZDD":
        data = expand(data)
    tmp = png[:-4] + ".bmp"
    with open(tmp, "wb") as f:
        f.write(data)
    r = subprocess.run(["sips", "-s", "format", "png", tmp, "--out", png],
                       stdout=DN, stderr=DN)
    os.remove(tmp)
    return r.returncode == 0


def to_mp3(src, dst):
    subprocess.run([FF, "-y", "-loglevel", "error", "-i", src,
                    "-codec:a", "libmp3lame", "-q:a", "5", dst], check=False)


def to_mp4(src, dst):
    subprocess.run([FF, "-y", "-loglevel", "error", "-i", src,
                    "-movflags", "+faststart", "-pix_fmt", "yuv420p",
                    "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2", dst], check=False)


def main():
    manifest = {}
    for artdir in sorted(glob.glob(os.path.join(DISC, "ART_*"))):
        for entry in sorted(os.listdir(artdir)):
            edir = os.path.join(artdir, entry)
            if not os.path.isdir(edir):
                continue
            if not os.path.exists(os.path.join(edir, f"{entry}00AA.DIB")):
                continue
            slug = entry.lower()
            out = os.path.join(OUT_ROOT, slug)
            os.makedirs(out, exist_ok=True)

            screens = []
            for dib in sorted(glob.glob(os.path.join(edir, "*.DIB"))):
                stem = os.path.splitext(os.path.basename(dib))[0]
                if dib_to_png(dib, os.path.join(out, stem + ".png")):
                    screens.append(stem)

            video = None
            avi = sorted(glob.glob(os.path.join(edir, "*.AVI")))
            if avi:
                to_mp4(avi[0], os.path.join(out, "clip.mp4"))
                video = "clip.mp4"

            audio = {"jn": [], "qn": [], "ix": [], "other": []}
            for wav in sorted(glob.glob(os.path.join(edir, "*.WAV"))):
                stem = os.path.splitext(os.path.basename(wav))[0]
                to_mp3(wav, os.path.join(out, stem + ".mp3"))
                suf = stem[-2:].lower()
                audio[suf if suf in ("jn", "qn", "ix") else "other"].append(stem)

            manifest[slug] = {"code": entry, "art": os.path.basename(artdir),
                              "screens": screens, "audio": audio, "video": video}
            print(f"{slug:6} scr={len(screens):2} jn={len(audio['jn'])} "
                  f"qn={len(audio['qn'])} ix={len(audio['ix'])} vid={'Y' if video else '-'}")

    os.makedirs(WEB, exist_ok=True)
    with open(os.path.join(WEB, "extracted-manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"\nDONE: {len(manifest)} entries -> {WEB}/extracted-manifest.json")


if __name__ == "__main__":
    main()
