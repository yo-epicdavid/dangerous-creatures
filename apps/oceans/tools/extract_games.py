#!/usr/bin/env python3
"""Extract the Oceans quiz feedback sounds (RIGHT/WRONG) for the games page."""
import os, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.abspath(os.path.join(HERE, "..", "web"))
OUT = os.path.join(WEB, "assets", "games")
GAMES = "/Volumes/MS_OCEANS/DATA/GAMES"
FF = "/opt/homebrew/bin/ffmpeg"


def main():
    os.makedirs(OUT, exist_ok=True)
    for src, dst in [("RIGHT.WAV", "right.mp3"), ("WRONG.WAV", "wrong.mp3")]:
        subprocess.run([FF, "-y", "-loglevel", "error", "-i", os.path.join(GAMES, src),
                        "-codec:a", "libmp3lame", "-q:a", "5", os.path.join(OUT, dst)], check=False)
        print(f"  {src} -> assets/games/{dst}")


if __name__ == "__main__":
    main()
