#!/usr/bin/env python3
"""Assemble web/data/es/guides.json — the Spanish FAN TRANSLATION of the 16 narrated tours.

No Spanish "Microsoft Dinosaurs" disc ever existed, so this reuses the ENGLISH narration
audio from guides-manifest.json unchanged; only the titles and blurbs are translated
(guides_meta_es.json). The guide pages surface a fan-translation note about the English audio.
"""
import os, json

HERE = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.abspath(os.path.join(HERE, "..", "web"))
DATA_ES = os.path.join(WEB, "data", "es")


def main():
    manifest = json.load(open(os.path.join(WEB, "guides-manifest.json")))
    meta = json.load(open(os.path.join(HERE, "guides_meta_es.json")))

    guides = []
    for m in meta:
        man = manifest.get(m["id"], {})
        guides.append({
            "id": m["id"], "title": m["title"], "icon": m.get("icon", "🦕"),
            "blurb": m.get("blurb", ""),
            # English narration reused verbatim — no Spanish recording exists.
            "narration": man.get("narration", []), "stepCount": man.get("stepCount", 0),
        })

    os.makedirs(DATA_ES, exist_ok=True)
    json.dump(guides, open(os.path.join(DATA_ES, "guides.json"), "w"), indent=2, ensure_ascii=False)
    print(f"wrote es/guides.json ({len(guides)} tours, {sum(g['stepCount'] for g in guides)} steps)")


if __name__ == "__main__":
    main()
