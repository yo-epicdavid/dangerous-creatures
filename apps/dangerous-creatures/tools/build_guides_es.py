#!/usr/bin/env python3
"""Assemble web/data/es/guides.json — the Castilian guided tours.

Authentic Spanish narration + intro art come from the Spanish disc (guides-manifest-es.json);
the Spanish title + intro come from OCR of the Spanish intro screens (guides_meta_es.json). The
geographic tours' creature lists are reused from the Spanish browse (es names + media).
"""
import os, json

HERE = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.abspath(os.path.join(HERE, "..", "web"))
DATA_ES = os.path.join(WEB, "data", "es")

HOST_NAME_ES = {"Story": "Cuentacuentos", "Annie": "Annie", "Fergie": "Fergie"}
# geographic/habitat tours -> (browse axis, Spanish category label) — keyed by tour number,
# since the titles are now Spanish and no longer match the English mapping.
TOUR_CREATURES_ES = {
    7: ("habitats", "Océanos y arrecifes de coral"),
    9: ("regions", "Sudamérica"),
    10: ("regions", "Australia y Oceanía"),
    11: ("regions", "África"),
    12: ("regions", "Norteamérica"),
}


def main():
    manifest = json.load(open(os.path.join(WEB, "guides-manifest-es.json")))
    meta_raw = json.load(open(os.path.join(WEB, "guides_meta_es.json")))
    meta_list = meta_raw.get("tours", meta_raw) if isinstance(meta_raw, dict) else meta_raw
    meta = {int(m["tour"]): m for m in meta_list}
    browse = json.load(open(os.path.join(DATA_ES, "browse.json")))

    def cat_animals(kind, label):
        for c in browse.get(kind, []):
            if c.get("category") == label or c.get("key") == label or c.get("label") == label:
                return c.get("animals") or c.get("items") or []
        return []

    guides = []
    for n in range(1, 13):
        nn = f"{n:02d}"
        m = manifest[nn]
        md = meta.get(n, {})
        entry = {
            "tour": n,
            "title": md.get("title", f"Visita {n}"),
            "host": HOST_NAME_ES.get(m["host"], m["host"]),
            "intro": md.get("intro", ""),
            "art": m["art"].replace(".png", ".webp"),
            "narration": m["narration"],
            "stepCount": m["stepCount"],
        }
        tc = TOUR_CREATURES_ES.get(n)
        if tc:
            entry["creatures"] = cat_animals(*tc)
        guides.append(entry)

    json.dump(guides, open(os.path.join(DATA_ES, "guides.json"), "w"), indent=2, ensure_ascii=False)
    print(f"wrote es/guides.json ({len(guides)} tours)")
    for g in guides:
        print(f"  {g['tour']:2} {g['title'][:28]:28} host={g['host']:13} steps={g['stepCount']:2} creatures={len(g.get('creatures', []))}")


if __name__ == "__main__":
    main()
