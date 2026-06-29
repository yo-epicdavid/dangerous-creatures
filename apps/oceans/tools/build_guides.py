#!/usr/bin/env python3
"""Assemble web/data/guides.json from the guide manifest + metadata.

Inputs : web/guides-manifest.json (art/intro/tours-narration per host),
         tools/guides_meta.json (name/role/intro + tour titles).
Output : web/data/guides.json — 6 hosts, each with 3 named, narrated tours.
"""
import os, json

HERE = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.abspath(os.path.join(HERE, "..", "web"))
DATA = os.path.join(WEB, "data")


def main():
    manifest = json.load(open(os.path.join(WEB, "guides-manifest.json")))
    meta = json.load(open(os.path.join(HERE, "guides_meta.json")))

    guides = []
    for m in sorted(meta, key=lambda x: x.get("order", 99)):
        man = manifest.get(m["id"], {})
        man_tours = {t["section"]: t for t in man.get("tours", [])}
        tours = []
        for mt in m["tours"]:
            t = man_tours.get(mt["section"], {})
            tours.append({
                "id": mt["section"], "title": mt["title"],
                "narration": t.get("narration", []), "stepCount": t.get("stepCount", 0),
            })
        guides.append({
            "id": m["id"], "name": m["name"], "role": m["role"], "intro": m["intro"],
            "art": man.get("art"), "introAudio": man.get("intro"), "tours": tours,
        })

    os.makedirs(DATA, exist_ok=True)
    json.dump(guides, open(os.path.join(DATA, "guides.json"), "w"), indent=2, ensure_ascii=False)
    total = sum(len(g["tours"]) for g in guides)
    print(f"wrote guides.json ({len(guides)} hosts, {total} tours)")
    for g in guides:
        print(f"  {g['name']:8} [{g['role']}] " + " | ".join(f"{t['title']}({t['stepCount']})" for t in g["tours"]))


if __name__ == "__main__":
    main()
