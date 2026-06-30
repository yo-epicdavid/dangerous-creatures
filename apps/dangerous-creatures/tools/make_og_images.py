#!/usr/bin/env python3
"""Per-animal Open Graph share cards. Renderer: packages/pipeline/og.py.
Subtitle = the scientific name. Set LOCALE=es for the Castilian cards (Spanish names +
"ANIMALES PELIGROSOS" wordmark), OG_ONLY=lion,gwsh for a preview. Run with the venv python."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "packages", "pipeline"))
from og import make_all

HERE = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.abspath(os.path.join(HERE, "..", "web"))
LOCALE = os.environ.get("LOCALE", "")
ONLY = [s.strip() for s in os.environ.get("OG_ONLY", "").split(",") if s.strip()]
DATA = os.path.join(WEB, "data", "es") if LOCALE == "es" else os.path.join(WEB, "data")
WORDMARK = "ANIMALES PELIGROSOS" if LOCALE == "es" else "DANGEROUS CREATURES"
PALETTE = {"ink": (244, 236, 224), "ink_soft": (205, 191, 169), "gold": (232, 163, 61),
           "dark": (12, 10, 8), "scrim": (8, 7, 5)}

if __name__ == "__main__":
    make_all(WEB, DATA, WORDMARK, PALETTE, lambda d: d.get("scientificName", ""), only=ONLY)
