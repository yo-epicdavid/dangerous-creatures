#!/usr/bin/env python3
"""Extract the 16 Dinosaurs guided tours: each GUIDE/GUID00NN/ holds a sequence of
narration steps (GUID<NN>MM.WAV). Writes web/assets/guides/tourNN/stepMM.mp3 +
web/guides-manifest.json. (No per-tour artwork on this disc.)
"""
import os, glob, json, shutil, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.abspath(os.path.join(HERE, "..", "web"))
OUT = os.path.join(WEB, "assets", "guides")
GUIDE = "/Volumes/DINOSAURS/GUIDE"
FF = "/opt/homebrew/bin/ffmpeg"


def to_mp3(src, dst):
    subprocess.run([FF, "-y", "-loglevel", "error", "-i", src,
                    "-codec:a", "libmp3lame", "-q:a", "5", dst], check=False)


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT, exist_ok=True)
    manifest = {}
    for nn in range(1, 17):
        folder = os.path.join(GUIDE, f"GUID00{nn:02d}")
        if not os.path.isdir(folder):
            continue
        slug = f"tour{nn:02d}"
        out = os.path.join(OUT, slug)
        os.makedirs(out, exist_ok=True)
        steps = sorted(glob.glob(os.path.join(folder, "*.WAV")))
        narration = []
        for j, w in enumerate(steps, 1):
            to_mp3(w, os.path.join(out, f"step{j:02d}.mp3"))
            narration.append(f"assets/guides/{slug}/step{j:02d}.mp3")
        manifest[slug] = {"num": nn, "narration": narration, "stepCount": len(narration)}
        print(f"{slug}: {len(narration)} steps")

    json.dump(manifest, open(os.path.join(WEB, "guides-manifest.json"), "w"), indent=2)
    print(f"wrote {WEB}/guides-manifest.json")


if __name__ == "__main__":
    main()
