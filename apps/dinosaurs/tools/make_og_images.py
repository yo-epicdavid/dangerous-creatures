#!/usr/bin/env python3
"""Per-entry Open Graph share cards for Dinosaurs. Renderer: packages/pipeline/og.py.
Subtitle = the name pronunciation (e.g. "al-BER-toe-SOR-us") when present, else the category
label. OG_ONLY=albe for a preview. Run with the venv python."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "packages", "pipeline"))
from og import make_all

HERE = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.abspath(os.path.join(HERE, "..", "web"))
ONLY = [s.strip() for s in os.environ.get("OG_ONLY", "").split(",") if s.strip()]
WORDMARK = "MICROSOFT DINOSAURS"
PALETTE = {"ink": (243, 236, 219), "ink_soft": (198, 180, 143), "gold": (224, 151, 58),
           "dark": (14, 11, 6), "scrim": (9, 7, 4)}
CAT = {"dinosaur": "Dinosaur", "creature": "Prehistoric creature", "concept": "Dinosaur science"}

if __name__ == "__main__":
    make_all(WEB, os.path.join(WEB, "data"), WORDMARK, PALETTE,
             lambda d: d.get("pronunciation") or CAT.get(d.get("category"), ""), only=ONLY)
