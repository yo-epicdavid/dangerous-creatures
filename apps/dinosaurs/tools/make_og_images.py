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
# es is a fan translation that reuses the ENGLISH media, so its cards live next to them as og-es.jpg.
LOCALE = os.environ.get("LOCALE", "")
DATA = os.path.join(WEB, "data", "es") if LOCALE == "es" else os.path.join(WEB, "data")
WORDMARK = "DINOSAURIOS DE MICROSOFT" if LOCALE == "es" else "MICROSOFT DINOSAURS"
OUT_NAME = "og-es.jpg" if LOCALE == "es" else "og.jpg"
PALETTE = {"ink": (243, 236, 219), "ink_soft": (198, 180, 143), "gold": (224, 151, 58),
           "dark": (14, 11, 6), "scrim": (9, 7, 4)}
CAT = ({"dinosaur": "Dinosaurio", "creature": "Criatura prehistórica", "concept": "Ciencia de los dinosaurios"}
       if LOCALE == "es" else
       {"dinosaur": "Dinosaur", "creature": "Prehistoric creature", "concept": "Dinosaur science"})

if __name__ == "__main__":
    make_all(WEB, DATA, WORDMARK, PALETTE,
             lambda d: d.get("pronunciation") or CAT.get(d.get("category"), ""), only=ONLY, out_name=OUT_NAME)
