#!/usr/bin/env python3
"""Per-entry Open Graph share cards for Oceans. Renderer: packages/pipeline/og.py.
Oceans entries have no scientific names, so the subtitle is the category label
(Sea life / Habitat / Ocean science / …). OG_ONLY=jell for a preview. Run with the venv python."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "packages", "pipeline"))
from og import make_all

HERE = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.abspath(os.path.join(HERE, "..", "web"))
ONLY = [s.strip() for s in os.environ.get("OG_ONLY", "").split(",") if s.strip()]
LOCALE = os.environ.get("LOCALE", "")          # "" = English, "es" = Castilian
DATA = os.path.join(WEB, "data", "es") if LOCALE == "es" else os.path.join(WEB, "data")
WORDMARK = "OCÉANOS DE MICROSOFT" if LOCALE == "es" else "MICROSOFT OCEANS"
PALETTE = {"ink": (234, 245, 252), "ink_soft": (167, 196, 218), "gold": (65, 196, 214),
           "dark": (5, 14, 26), "scrim": (3, 10, 18)}
CAT = ({"creature": "Vida marina", "habitat": "Hábitat", "concept": "Ciencia del océano",
        "place": "Mar o región", "human": "Las personas y el mar"} if LOCALE == "es" else
       {"creature": "Sea life", "habitat": "Habitat", "concept": "Ocean science",
        "place": "Sea or region", "human": "People & the sea"})

if __name__ == "__main__":
    make_all(WEB, DATA, WORDMARK, PALETTE,
             lambda d: d.get("scientificName") or CAT.get(d.get("category"), ""), only=ONLY)
