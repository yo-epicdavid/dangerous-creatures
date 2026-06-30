#!/usr/bin/env python3
"""Convert this app's PNG assets to WebP. Shared logic: packages/pipeline/media.py."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "packages", "pipeline"))
from media import to_webp

if __name__ == "__main__":
    assets = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "web", "assets"))
    to_webp(assets)
