#!/usr/bin/env python3
"""Extract the narration we missed the first time:
  - NP{n}  -> spoken narration for each sub-topic (PU) screen
  - AF     -> the animal's own sound (roar/call/etc.)
into web/assets/<slug>/. Needs the disc mounted at /Volumes/DANGEROUS + ffmpeg.
"""
import os, glob, json, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.abspath(os.path.join(HERE, "..", "web"))
DISC = "/Volumes/DANGEROUS"
FF = "/opt/homebrew/bin/ffmpeg"


def to_mp3(src, dst):
    subprocess.run([FF, "-y", "-loglevel", "error", "-i", src, "-codec:a", "libmp3lame", "-q:a", "5", dst], check=False)


def main():
    manifest = json.load(open(os.path.join(WEB, "extracted-manifest.json")))
    np_n = af_n = fb_n = 0
    for slug, info in manifest.items():
        code = info["code"]
        out = os.path.join(WEB, "assets", slug)
        os.makedirs(out, exist_ok=True)
        # sub-topic narration: AANPOP/<bucket>/<CODE>{n}NP.WAV
        for wav in sorted(glob.glob(os.path.join(DISC, "AANPOP", "**", f"{code}*NP.WAV"), recursive=True)):
            stem = os.path.splitext(os.path.basename(wav))[0]   # e.g. LION03NP
            to_mp3(wav, os.path.join(out, stem + ".mp3"))
            np_n += 1
        # animal sound: AAFACT/<bucket>/<CODE>00AF.WAV
        af = glob.glob(os.path.join(DISC, "AAFACT", "**", f"{code}00AF.WAV"), recursive=True)
        if af:
            to_mp3(af[0], os.path.join(out, f"{code}00AF.mp3"))
            af_n += 1
        # fact-box "Free Advice" narration: AAFBOX/<bucket>/<CODE>00FB.WAV
        fb = glob.glob(os.path.join(DISC, "AAFBOX", "**", f"{code}00FB.WAV"), recursive=True)
        if fb:
            to_mp3(fb[0], os.path.join(out, f"{code}00FB.mp3"))
            fb_n += 1
    print(f"sub-topic narrations: {np_n}  |  animal sounds: {af_n}  |  fact-box narrations: {fb_n}  -> web/assets/*/")


if __name__ == "__main__":
    main()
