#!/usr/bin/env python3
"""Generate poster.webp for each clip.mp4 in this app. Shared logic: packages/pipeline/media.py.
Run with a Python that has Pillow (the project venv)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "packages", "pipeline"))
from media import make_posters

if __name__ == "__main__":
    assets = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "web", "assets"))
    make_posters(assets)
