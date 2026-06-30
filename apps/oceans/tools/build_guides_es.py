#!/usr/bin/env python3
"""Assemble web/data/es/guides.json — the Castilian Oceans guided tours (6 hosts × 3 tours).

Authentic Spanish portraits + intro audio + narration come from the Spanish disc
(guides-manifest-es.json). Host name/role + tour titles come from OCR of the Spanish portraits;
the host intro paragraph (spoken on the disc) is translated. Both live in guides_ocr_es.json.
"""
import os, json

HERE = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.abspath(os.path.join(HERE, "..", "web"))
DATA_ES = os.path.join(WEB, "data", "es")
HOST_ORDER = ["kim", "eli", "curtis", "frank", "zarka", "rebecca"]


def main():
    manifest = json.load(open(os.path.join(WEB, "guides-manifest-es.json")))
    ocr_raw = json.load(open(os.path.join(WEB, "guides_ocr_es.json")))
    ocr_list = ocr_raw.get("hosts", ocr_raw) if isinstance(ocr_raw, dict) else ocr_raw
    ocr = {h["id"]: h for h in ocr_list}

    guides = []
    for hid in HOST_ORDER:
        man = manifest.get(hid, {})
        o = ocr.get(hid, {})
        titles = {t["section"]: t["title"] for t in o.get("tours", [])}
        man_tours = sorted(man.get("tours", []), key=lambda t: t["section"])
        tours = [{"id": mt["section"], "title": titles.get(mt["section"], f"Recorrido {i + 1}"),
                  "narration": mt["narration"], "stepCount": mt["stepCount"]}
                 for i, mt in enumerate(man_tours)]
        guides.append({
            "id": hid, "name": o.get("name", hid.title()), "role": o.get("role", ""),
            "intro": o.get("intro", ""), "art": man.get("art"), "introAudio": man.get("intro"),
            "tours": tours,
        })

    os.makedirs(DATA_ES, exist_ok=True)
    json.dump(guides, open(os.path.join(DATA_ES, "guides.json"), "w"), indent=2, ensure_ascii=False)
    total = sum(len(g["tours"]) for g in guides)
    print(f"wrote es/guides.json ({len(guides)} hosts, {total} tours)")
    for g in guides:
        print(f"  {g['name']:9} [{g['role'][:22]:22}] " + " | ".join(f"{t['title'][:22]}({t['stepCount']})" for t in g["tours"]))


if __name__ == "__main__":
    main()
