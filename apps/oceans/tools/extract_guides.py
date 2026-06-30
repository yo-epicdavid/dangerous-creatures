#!/usr/bin/env python3
"""Extract the Oceans guided tours: 6 hosts, each with a portrait + 3 named tours.

Layout per host dir GUIDES/<HOST>/:
  *N2.DIB                portrait/menu screen (host + their 3 tour buttons)
  *IN.WAV                host intro ("choose a tour")
  GUID<SS><NN>.WAV       narration step NN of tour-section SS (each host owns 3 sections)

Writes web/assets/guides/<host>/{portrait.webp, intro.mp3, <SS>/stepNN.mp3} + web/guides-manifest.json.
Run with the venv Python (needs Pillow).
"""
import os, sys, re, glob, json, shutil, subprocess
from collections import defaultdict
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "packages", "pipeline"))
from szdd import expand

DISC = os.environ.get("DISC", "/Volumes/MS_OCEANS/DATA/GUIDES")
LOCALE = os.environ.get("LOCALE", "")
WEB = os.path.abspath(os.path.join(HERE, "..", "web"))
GP = "assets/guides/es" if LOCALE else "assets/guides"
OUT = os.path.join(WEB, *GP.split("/"))
FF = "/opt/homebrew/bin/ffmpeg"
DN = subprocess.DEVNULL
HOSTS = ["KIM", "ELI", "CURTIS", "FRANK", "ZARKA", "REBECCA"]


def dib_webp(dib, webp):
    with open(dib, "rb") as f:
        data = f.read()
    if data[:4] == b"SZDD":
        data = expand(data)
    bmp, png = webp[:-5] + ".bmp", webp[:-5] + ".png"
    with open(bmp, "wb") as f:
        f.write(data)
    subprocess.run(["sips", "-s", "format", "png", bmp, "--out", png], stdout=DN, stderr=DN)
    Image.open(png).convert("RGB").save(webp, "WEBP", quality=82, method=6)
    os.remove(bmp); os.remove(png)


def to_mp3(src, dst):
    subprocess.run([FF, "-y", "-loglevel", "error", "-i", src, "-codec:a", "libmp3lame", "-q:a", "5", dst], check=False)


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT, exist_ok=True)
    manifest = {}
    for host in HOSTS:
        slug = host.lower()
        hd = os.path.join(DISC, host)
        out = os.path.join(OUT, slug)
        os.makedirs(out, exist_ok=True)

        dibs = glob.glob(os.path.join(hd, "*N2.DIB"))
        art = None
        if dibs:
            dib_webp(dibs[0], os.path.join(out, "portrait.webp"))
            art = f"{GP}/{slug}/portrait.webp"

        intro = None
        ins = sorted(glob.glob(os.path.join(hd, "*IN.WAV")))
        if ins:
            to_mp3(ins[0], os.path.join(out, "intro.mp3"))
            intro = f"{GP}/{slug}/intro.mp3"

        sections = defaultdict(list)
        for w in glob.glob(os.path.join(hd, "*.WAV")):
            mm = re.search(r"GUID(\d{2})(\d{2})\.WAV$", os.path.basename(w), re.I)
            if mm:
                sections[mm.group(1)].append((mm.group(2), w))

        tours = []
        for ss in sorted(sections):
            sdir = os.path.join(out, ss)
            os.makedirs(sdir, exist_ok=True)
            narration = []
            for j, (_nn, w) in enumerate(sorted(sections[ss]), 1):
                to_mp3(w, os.path.join(sdir, f"step{j:02d}.mp3"))
                narration.append(f"{GP}/{slug}/{ss}/step{j:02d}.mp3")
            tours.append({"section": ss, "narration": narration, "stepCount": len(narration)})

        manifest[slug] = {"art": art, "intro": intro, "tours": tours}
        print(f"{slug:8} portrait={'Y' if art else '-'} sections={[t['section'] for t in tours]} "
              f"steps={[t['stepCount'] for t in tours]}")

    mname = f"guides-manifest-{LOCALE}.json" if LOCALE else "guides-manifest.json"
    json.dump(manifest, open(os.path.join(WEB, mname), "w"), indent=2)
    print(f"wrote {WEB}/guides-manifest.json")


if __name__ == "__main__":
    main()
