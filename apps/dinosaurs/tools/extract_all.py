#!/usr/bin/env python3
"""Extract Microsoft Dinosaurs (1993) disc content.

Structure mirrors Dangerous Creatures: DINOPAGE/<CODE>00AA/ per-entry folders with
  <CODE>00AA.BMP   main screen (title + pronunciation icon + intro + hotspots)
  <CODE>NNPU.BMP   sub-topic screens
  <CODE>50FB.BMP   fact box ("fast facts")
Images are RAW BMP (640x460, 24-bit) — no SZDD. Audio lives in separate top-level dirs:
  AUDPRON/<bucket>/<CODE>00AP.WAV   name pronunciation
  AUDSCENE/<CODE>00SA.WAV           scene / intro narration (only some entries)
  AUDJUMP/<bucket>/<CODE>00AJ.WAV   cross-link narration
Disc mounted at /Volumes/DINOSAURS. Outputs PNG + MP3 into ../web/assets/<slug>/ and a
../web/extracted-manifest.json.
"""
import os, re, glob, json, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.abspath(os.path.join(HERE, "..", "web"))
OUT_ROOT = os.path.join(WEB, "assets")
DISC = "/Volumes/DINOSAURS"
DINOPAGE = os.path.join(DISC, "DINOPAGE")
FF = "/opt/homebrew/bin/ffmpeg"
DN = subprocess.DEVNULL


def bmp_to_png(bmp, png):
    r = subprocess.run(["sips", "-s", "format", "png", bmp, "--out", png], stdout=DN, stderr=DN)
    return r.returncode == 0


def to_mp3(src, dst):
    subprocess.run([FF, "-y", "-loglevel", "error", "-i", src,
                    "-codec:a", "libmp3lame", "-q:a", "5", dst], check=False)


def first(pattern):
    hits = glob.glob(pattern, recursive=True)
    return hits[0] if hits else None


def main():
    manifest = {}
    for folder in sorted(os.listdir(DINOPAGE)):
        m = re.match(r"^([A-Z]{2,5})00AA$", folder)
        if not m:
            continue  # skip nav screens (……00NV) and loose files
        code = m.group(1)
        fdir = os.path.join(DINOPAGE, folder)
        if not os.path.isdir(fdir) or not os.path.exists(os.path.join(fdir, f"{code}00AA.BMP")):
            continue
        slug = code.lower()
        out = os.path.join(OUT_ROOT, slug)
        os.makedirs(out, exist_ok=True)

        screens = []
        for bmp in sorted(glob.glob(os.path.join(fdir, "*.BMP"))):
            stem = os.path.splitext(os.path.basename(bmp))[0]
            if bmp_to_png(bmp, os.path.join(out, stem + ".png")):
                screens.append(stem)

        audio = {}
        pron = first(os.path.join(DISC, "AUDPRON", "**", f"{code}*AP.WAV"))
        if pron:
            to_mp3(pron, os.path.join(out, f"{code}00AP.mp3")); audio["pron"] = f"{code}00AP"
        scene = first(os.path.join(DISC, "AUDSCENE", f"{code}*SA.WAV"))
        if scene:
            to_mp3(scene, os.path.join(out, f"{code}00SA.mp3")); audio["scene"] = f"{code}00SA"
        jump = first(os.path.join(DISC, "AUDJUMP", "**", f"{code}*AJ.WAV"))
        if jump:
            to_mp3(jump, os.path.join(out, f"{code}00AJ.mp3")); audio["jump"] = f"{code}00AJ"

        manifest[slug] = {"code": code, "screens": screens, "audio": audio, "video": None}
        print(f"{slug:6} screens={len(screens):2} pron={'Y' if 'pron' in audio else '-'} "
              f"scene={'Y' if 'scene' in audio else '-'}")

    with open(os.path.join(WEB, "extracted-manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"\nDONE: {len(manifest)} entries -> {WEB}/extracted-manifest.json")


if __name__ == "__main__":
    main()
