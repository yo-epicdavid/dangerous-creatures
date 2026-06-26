#!/usr/bin/env python3
"""Assemble web/data/guides.json from the guide manifest + titles + browse lists.

Inputs : web/guides-manifest.json (art/narration/host), tools/guides_meta.json (titles/intros),
         web/data/browse.json (for geographic tours' creature lists).
Output : web/data/guides.json
"""
import os, json

HERE = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.abspath(os.path.join(HERE, "..", "web"))
DATA = os.path.join(WEB, "data")

HOST_NAME = {"Story": "Storyteller", "Annie": "Annie", "Fergie": "Fergie"}

# Geographic/habitat tours that map to a set of real creatures.
TOUR_CREATURES = {
    "Amazon Adventure": ("regions", "South America"),
    "Australian Walkabout": ("regions", "Australia & Oceania"),
    "North American Trek": ("regions", "North America"),
    "African Safari": ("regions", "Africa"),
    "Coral Reef Dive": ("habitats", "Oceans & Coral Reefs"),
}


def main():
    manifest = json.load(open(os.path.join(WEB, "guides-manifest.json")))
    meta_list = json.load(open(os.path.join(HERE, "guides_meta.json")))
    meta = {int(m["tour"]): m for m in meta_list}
    browse = json.load(open(os.path.join(DATA, "browse.json")))

    def cat_animals(kind, label):
        for c in browse.get(kind, []):
            if c["category"] == label:
                return c["animals"]
        return []

    guides = []
    for n in range(1, 13):
        nn = f"{n:02d}"
        m = manifest[nn]
        md = meta.get(n, {})
        title = md.get("title", f"Tour {n}")
        entry = {
            "tour": n,
            "title": title,
            "host": HOST_NAME.get(m["host"], m["host"]),
            "intro": md.get("intro", ""),
            "art": m["art"],
            "narration": m["narration"],
            "stepCount": m["stepCount"],
        }
        tc = TOUR_CREATURES.get(title)
        if tc:
            entry["creatures"] = cat_animals(*tc)
        guides.append(entry)

    json.dump(guides, open(os.path.join(DATA, "guides.json"), "w"), indent=2, ensure_ascii=False)
    print(f"wrote guides.json ({len(guides)} tours)")
    for g in guides:
        print(f"  {g['tour']:2} {g['title']:24} host={g['host']:11} steps={g['stepCount']:2} creatures={len(g.get('creatures', []))}")


if __name__ == "__main__":
    main()
