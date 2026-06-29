#!/usr/bin/env python3
"""Extract the 12 Guided Tours: intro art (SZDD DIB -> PNG) + narration (WAV -> MP3).

Tours 1-4 are narrated from AAGUIDE/STORY, 5-8 from ANNIE, 9-12 from FERGIE.
Writes web/assets/guides/tourNN/{intro.png, stepMM.mp3} and web/guides-manifest.json.
"""
import os, sys, glob, json, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from szdd import expand

DISC = "/Volumes/DANGEROUS"
GUIDE = os.path.join(DISC, "AAGUIDE")
NV = os.path.join(DISC, "ABOUT", "GUID00NV")
WEB = os.path.abspath(os.path.join(HERE, "..", "web"))
OUT = os.path.join(WEB, "assets", "guides")
FF = "/opt/homebrew/bin/ffmpeg"
DN = subprocess.DEVNULL


def dib_png(dib, png):
    tmp = png[:-4] + ".bmp"
    with open(dib, "rb") as f:
        data = expand(f.read())
    with open(tmp, "wb") as f:
        f.write(data)
    subprocess.run(["sips", "-s", "format", "png", tmp, "--out", png], stdout=DN, stderr=DN, check=False)
    os.remove(tmp)


def main():
    os.makedirs(OUT, exist_ok=True)
    dib_png(os.path.join(NV, "GUID00NV.DIB"), os.path.join(OUT, "menu.png"))
    manifest = {}
    for n in range(1, 13):
        nn = f"{n:02d}"
        folder = "STORY" if n <= 4 else ("ANNIE" if n <= 8 else "FERGIE")
        tourdir = os.path.join(OUT, f"tour{nn}")
        os.makedirs(tourdir, exist_ok=True)
        dib = os.path.join(NV, f"GUID{nn}NV.DIB")
        if os.path.exists(dib):
            dib_png(dib, os.path.join(tourdir, "intro.png"))
        wavs = sorted(glob.glob(os.path.join(GUIDE, folder, f"GUID{nn}*.WAV")))
        steps = []
        for i, w in enumerate(wavs, 1):
            mp3 = os.path.join(tourdir, f"step{i:02d}.mp3")
            subprocess.run([FF, "-y", "-loglevel", "error", "-i", w, "-codec:a", "libmp3lame", "-q:a", "5", mp3], check=False)
            steps.append(f"step{i:02d}.mp3")
        manifest[nn] = {"host": folder.title(), "art": f"assets/guides/tour{nn}/intro.png",
                        "narration": [f"assets/guides/tour{nn}/{s}" for s in steps], "stepCount": len(steps)}
        print(f"tour {nn}  host={folder:6} steps={len(steps)}")
    json.dump(manifest, open(os.path.join(WEB, "guides-manifest.json"), "w"), indent=2)
    print(f"\nDONE -> {os.path.join(WEB, 'guides-manifest.json')}")


if __name__ == "__main__":
    main()
