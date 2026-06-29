#!/usr/bin/env python3
"""Assemble web/data/guides.json from the guide manifest + metadata (16 narrated tours)."""
import os, json

HERE = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.abspath(os.path.join(HERE, "..", "web"))
DATA = os.path.join(WEB, "data")


def main():
    manifest = json.load(open(os.path.join(WEB, "guides-manifest.json")))
    meta = json.load(open(os.path.join(HERE, "guides_meta.json")))

    guides = []
    for m in meta:
        man = manifest.get(m["id"], {})
        guides.append({
            "id": m["id"], "title": m["title"], "icon": m.get("icon", "🦕"),
            "blurb": m.get("blurb", ""),
            "narration": man.get("narration", []), "stepCount": man.get("stepCount", 0),
        })

    os.makedirs(DATA, exist_ok=True)
    json.dump(guides, open(os.path.join(DATA, "guides.json"), "w"), indent=2, ensure_ascii=False)
    print(f"wrote guides.json ({len(guides)} tours, {sum(g['stepCount'] for g in guides)} steps)")


if __name__ == "__main__":
    main()
