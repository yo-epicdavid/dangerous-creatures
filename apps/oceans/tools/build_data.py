#!/usr/bin/env python3
"""Turn the Oceans liberation output into per-entry page JSON + indexes.

Input : a JSON file {"entries":[...], "consistency":{...}}  (env WF_RESULT or
        web/wf_result.json) plus web/extracted-manifest.json
Output: web/data/<id>.json for every entry, web/data/index.json, web/data/browse.json

Audio is wired deterministically from the manifest (the liberation step is text-only):
  per-screen narration  CODE<NN>JN.mp3   (00 = main hook, 01.. = sub-topics / video)
  ambient/creature sound CODE00IX.mp3
"""
import os, json, re, html

HERE = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.abspath(os.path.join(HERE, "..", "web"))
DATA = os.path.join(WEB, "data")
MANIFEST = os.path.join(WEB, "extracted-manifest.json")
WF_RESULT = os.environ.get("WF_RESULT", os.path.join(WEB, "wf_result.json"))

PROV = {
    "source": "Microsoft Oceans (1995) CD-ROM",
    "note": "Text liberated from original screen art; images, audio & clips restored from disc. "
            "Original media is Microsoft/supplier copyright — non-commercial educational preservation.",
}

CATEGORY_ORDER = ["creature", "habitat", "concept", "place", "human"]
CATEGORY_LABEL = {
    "creature": "Sea Life", "habitat": "Habitats", "concept": "How the Ocean Works",
    "place": "Seas & Regions", "human": "People & the Sea",
}
ZONE_ORDER = ["Coast & tide pools", "Coral reef", "Kelp & seagrass", "Open ocean",
              "Deep sea", "Polar seas", "Rivers & estuaries"]


def asset(slug, name):
    return f"assets/{slug}/{name}"


def clean(o):
    """Recursively un-escape HTML entities the OCR pass sometimes emits (&amp; -> &)."""
    if isinstance(o, str):
        return html.unescape(o)
    if isinstance(o, list):
        return [clean(x) for x in o]
    if isinstance(o, dict):
        return {k: clean(v) for k, v in o.items()}
    return o


def main():
    manifest = json.load(open(MANIFEST))
    result = json.load(open(WF_RESULT))
    entries = result["entries"]
    cons = result.get("consistency") or {}

    patches = {}
    for p in cons.get("patches", []):
        if p.get("field") in ("tagline", "name", "scientificName", "category"):
            patches.setdefault(p["id"], {})[p["field"]] = p["value"]

    name_to_slug = {e["name"].strip().lower(): e["id"] for e in entries}
    all_slugs = {e["id"] for e in entries}

    os.makedirs(DATA, exist_ok=True)
    index = []
    cat_map, zone_map, ocean_map = {}, {}, {}

    for d in entries:
        slug = d["id"]
        man = manifest.get(slug, {})
        stems = man.get("screens", [])
        code = d.get("code", slug.upper())
        audio = man.get("audio", {})
        jn, ix = set(audio.get("jn", [])), set(audio.get("ix", []))
        for field, val in patches.get(slug, {}).items():
            d[field] = val

        main_stem = next((s for s in stems if s.endswith("00AA")), f"{code}00AA")
        pv_stem = (d.get("video") or {}).get("screen") or next((s for s in stems if "PV" in s), None)
        has_video = bool(man.get("video"))

        def jn_for(screen):
            """CODE01PU / CODE02PV -> assets/.../CODE01JN.mp3 if present."""
            mm = re.match(r"^" + re.escape(code) + r"(\d{2})", screen or "")
            if not mm:
                return None
            stem = f"{code}{mm.group(1)}JN"
            if stem in jn and os.path.exists(os.path.join(WEB, "assets", slug, stem + ".mp3")):
                return asset(slug, stem + ".mp3")
            return None

        topics = []
        for t in d.get("topics", []):
            topic = {"id": t["id"], "title": t["title"],
                     "image": asset(slug, t["screen"] + ".webp"), "text": t["text"]}
            if t.get("captions"):
                topic["captions"] = t["captions"]
            n = jn_for(t.get("screen", ""))
            if n:
                topic["narration"] = n
            topics.append(topic)

        video = None
        if has_video:
            poster_stem = "poster.webp" if os.path.exists(os.path.join(WEB, "assets", slug, "poster.webp")) \
                else (pv_stem or main_stem) + ".webp"
            video = {"title": (d.get("video") or {}).get("title", "Watch"),
                     "src": asset(slug, "clip.mp4"),
                     "poster": asset(slug, poster_stem),
                     "caption": (d.get("video") or {}).get("caption", "")}
            vn = jn_for(pv_stem)
            if vn:
                video["narration"] = vn

        # classic-mode scene graph
        screens = {"main": {"image": asset(slug, main_stem + ".webp"), "hotspots": []}}
        for t in d.get("topics", []):
            screens[t["id"]] = {"image": asset(slug, t["screen"] + ".webp"), "back": "main"}
        if has_video:
            screens["video"] = {"video": asset(slug, "clip.mp4"),
                                "poster": asset(slug, (pv_stem or main_stem) + ".webp"), "back": "main"}

        local = set(screens.keys()) | {"quiz", "facts"}
        resolved = []
        for h in d.get("hotspots", []):
            to = h.get("to")
            if to in local:
                resolved.append(h)
                continue
            cand = name_to_slug.get((h.get("label") or "").strip().lower())
            if not cand and to in all_slugs and to != slug:
                cand = to
            nh = {k: v for k, v in h.items() if k != "to"}
            if cand and cand != slug:
                nh["external"] = cand
            else:
                nh["disabled"] = True
            resolved.append(nh)
        screens["main"]["hotspots"] = resolved

        crosslinks = []
        for c in d.get("crosslinks", []):
            cand = c.get("to") if c.get("to") in all_slugs else \
                name_to_slug.get((c.get("label") or "").strip().lower())
            link = {"label": c["label"]}
            if cand and cand != slug:
                link["to"] = cand
            crosslinks.append(link)

        sci_raw = d.get("scientificName", "") or ""
        needs_sci = "(unverified)" in sci_raw.lower()
        sci = re.sub(r"\s*\(unverified\)\s*$", "", sci_raw, flags=re.I).strip()

        category = d.get("category", "creature")
        zones = d.get("zones", []) or []
        oceans = d.get("oceans", []) or []
        cat_map.setdefault(category, []).append(slug)
        for z in zones:
            zone_map.setdefault(z, []).append(slug)
        for o in oceans:
            ocean_map.setdefault(o, []).append(slug)

        page = {
            "id": slug, "code": code, "name": d["name"], "category": category,
            "scientificName": sci, "needsScientificVerify": needs_sci,
            "tagline": d.get("tagline", ""), "zones": zones, "oceans": oceans,
            "hero": {"image": asset(slug, main_stem + ".webp"), "alt": d["name"]},
            "intro": d.get("intro", ""), "facts": d.get("facts", []),
            "topics": topics, "crosslinks": crosslinks,
            "classic": {"start": "main", "screens": screens},
            "_provenance": PROV,
        }
        jn00 = f"{code}00JN"
        if jn00 in jn and os.path.exists(os.path.join(WEB, "assets", slug, jn00 + ".mp3")):
            page["narration"] = asset(slug, jn00 + ".mp3")   # main spoken intro -> "Listen"
        ix00 = f"{code}00IX"
        if ix00 in ix and os.path.exists(os.path.join(WEB, "assets", slug, ix00 + ".mp3")):
            page["sound"] = asset(slug, ix00 + ".mp3")        # ambient/creature sound
        if video:
            page["video"] = video

        page = clean(page)
        json.dump(page, open(os.path.join(DATA, f"{slug}.json"), "w"), indent=2, ensure_ascii=False)
        index.append({"id": slug, "name": clean(d["name"]), "category": category,
                      "thumb": asset(slug, main_stem + ".webp")})

    if os.environ.get("SKIP_INDEX") != "1":
        index.sort(key=lambda x: x["name"])
        json.dump(index, open(os.path.join(DATA, "index.json"), "w"), indent=2, ensure_ascii=False)
        by_id = {e["id"]: e for e in index}

        def cats(amap, order, labels=None):
            out, seen = [], set()
            for label in list(order) + sorted(k for k in amap if k not in order):
                slugs = amap.get(label, [])
                if slugs and label not in seen:
                    seen.add(label)
                    items = sorted((by_id[s] for s in slugs), key=lambda e: e["name"])
                    out.append({"key": label, "label": (labels or {}).get(label, label),
                                "count": len(items), "items": items})
            return out

        browse = {
            "categories": cats(cat_map, CATEGORY_ORDER, CATEGORY_LABEL),
            "zones": cats(zone_map, ZONE_ORDER),
            "oceans": cats(ocean_map, []),
        }
        json.dump(browse, open(os.path.join(DATA, "browse.json"), "w"), indent=2, ensure_ascii=False)
    print(f"wrote {len(entries)} page files -> {DATA}")


if __name__ == "__main__":
    main()
