#!/usr/bin/env python3
"""Turn the Dinosaurs liberation output into per-entry page JSON + indexes.

Input : web/wf_result.json {"entries":[...], "consistency":{...}} + web/extracted-manifest.json
Output: web/data/<id>.json, web/data/index.json, web/data/browse.json

Audio is wired from the manifest: pronunciation (CODE00AP) -> "say it", scene narration
(CODE00SA) -> "Listen".
"""
import os, json, re, html

HERE = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.abspath(os.path.join(HERE, "..", "web"))
DATA = os.path.join(WEB, "data")
MANIFEST = os.path.join(WEB, "extracted-manifest.json")
WF_RESULT = os.environ.get("WF_RESULT", os.path.join(WEB, "wf_result.json"))

PROV = {
    "source": "Microsoft Dinosaurs (1993) CD-ROM",
    "note": "Text liberated from original screen art; images & audio restored from disc. "
            "Original media is Microsoft/supplier copyright — non-commercial educational preservation.",
}

CATEGORY_ORDER = ["dinosaur", "creature", "concept"]
CATEGORY_LABEL = {"dinosaur": "Dinosaurs", "creature": "Other Prehistoric Life", "concept": "The Dinosaur World"}
PERIOD_ORDER = ["Triassic", "Jurassic", "Cretaceous"]
DIET_ORDER = ["Carnivore", "Herbivore", "Omnivore"]


def asset(slug, name):
    return f"assets/{slug}/{name}"


def clean(o):
    if isinstance(o, str):
        return html.unescape(o)
    if isinstance(o, list):
        return [clean(x) for x in o]
    if isinstance(o, dict):
        return {k: clean(v) for k, v in o.items()}
    return o


def period_group(p):
    p = (p or "").lower()
    for g in PERIOD_ORDER:
        if g.lower() in p:
            return g
    return None


def main():
    manifest = json.load(open(MANIFEST))
    result = json.load(open(WF_RESULT))
    entries = result["entries"]
    cons = result.get("consistency") or {}

    patches = {}
    for p in cons.get("patches", []):
        if p.get("field") in ("tagline", "name", "category", "period", "diet"):
            patches.setdefault(p["id"], {})[p["field"]] = p["value"]

    name_to_slug = {e["name"].strip().lower(): e["id"] for e in entries}
    all_slugs = {e["id"] for e in entries}

    os.makedirs(DATA, exist_ok=True)
    index = []
    cat_map, period_map, diet_map = {}, {}, {}

    for d in entries:
        slug = d["id"]
        man = manifest.get(slug, {})
        stems = man.get("screens", [])
        code = d.get("code", slug.upper())
        audio = man.get("audio", {})
        for field, val in patches.get(slug, {}).items():
            d[field] = val

        main_stem = next((s for s in stems if s.endswith("00AA")), f"{code}00AA")
        fb_stem = next((s for s in stems if "FB" in s), None)

        topics = []
        for t in d.get("topics", []):
            topic = {"id": t["id"], "title": t["title"],
                     "image": asset(slug, t["screen"] + ".webp"), "text": t["text"]}
            if t.get("captions"):
                topic["captions"] = t["captions"]
            topics.append(topic)

        # classic-mode scene graph
        screens = {"main": {"image": asset(slug, main_stem + ".webp"), "hotspots": []}}
        for t in d.get("topics", []):
            screens[t["id"]] = {"image": asset(slug, t["screen"] + ".webp"), "back": "main"}
        if fb_stem:
            screens["facts"] = {"image": asset(slug, fb_stem + ".webp"), "back": "main"}

        local = set(screens.keys())
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

        category = d.get("category", "dinosaur")
        period = d.get("period", "") or ""
        diet = d.get("diet", "") or ""
        pg = period_group(period)
        cat_map.setdefault(category, []).append(slug)
        if pg:
            period_map.setdefault(pg, []).append(slug)
        if diet in DIET_ORDER:
            diet_map.setdefault(diet, []).append(slug)

        page = {
            "id": slug, "code": code, "name": d["name"], "category": category,
            "scientificName": sci, "needsScientificVerify": needs_sci,
            "pronunciation": d.get("pronunciation", ""), "meaning": d.get("meaning", ""),
            "period": period, "diet": diet, "tagline": d.get("tagline", ""),
            "hero": {"image": asset(slug, main_stem + ".webp"), "alt": d["name"]},
            "intro": d.get("intro", ""), "facts": d.get("facts", []),
            "topics": topics, "crosslinks": crosslinks,
            "classic": {"start": "main", "screens": screens},
            "_provenance": PROV,
        }
        if audio.get("pron") and os.path.exists(os.path.join(WEB, "assets", slug, f"{code}00AP.mp3")):
            page["sayIt"] = asset(slug, f"{code}00AP.mp3")      # name pronunciation -> "Say it"
        if audio.get("jump") and os.path.exists(os.path.join(WEB, "assets", slug, f"{code}00AJ.mp3")):
            page["narration"] = asset(slug, f"{code}00AJ.mp3")  # spoken entry summary -> "Listen" (all 166)
        if audio.get("scene") and os.path.exists(os.path.join(WEB, "assets", slug, f"{code}00SA.mp3")):
            page["sound"] = asset(slug, f"{code}00SA.mp3")      # dramatic scene sound effect -> "Hear it" (52)

        page = clean(page)
        json.dump(page, open(os.path.join(DATA, f"{slug}.json"), "w"), indent=2, ensure_ascii=False)
        index.append({"id": slug, "name": clean(d["name"]), "category": category,
                      "thumb": asset(slug, main_stem + ".webp")})

    if os.environ.get("SKIP_INDEX") != "1":
        index.sort(key=lambda x: x["name"])
        json.dump(index, open(os.path.join(DATA, "index.json"), "w"), indent=2, ensure_ascii=False)
        by_id = {e["id"]: e for e in index}

        def cats(amap, order, labels=None):
            out = []
            for label in list(order) + sorted(k for k in amap if k not in order):
                slugs = amap.get(label, [])
                if slugs:
                    items = sorted((by_id[s] for s in slugs), key=lambda e: e["name"])
                    out.append({"key": label, "label": (labels or {}).get(label, label),
                                "count": len(items), "items": items})
            return out

        browse = {
            "categories": cats(cat_map, CATEGORY_ORDER, CATEGORY_LABEL),
            "periods": cats(period_map, PERIOD_ORDER),
            "diets": cats(diet_map, DIET_ORDER),
        }
        json.dump(browse, open(os.path.join(DATA, "browse.json"), "w"), indent=2, ensure_ascii=False)
    print(f"wrote {len(entries)} page files -> {DATA}")


if __name__ == "__main__":
    main()
