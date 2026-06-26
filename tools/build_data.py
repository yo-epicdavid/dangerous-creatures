#!/usr/bin/env python3
"""Turn the liberation-workflow output into per-animal page JSON + the index.

Input : a JSON file {"animals":[...], "consistency":{...}}  (env WF_RESULT or
        web/wf_result.json) plus web/extracted-manifest.json
Output: web/data/<id>.json for every animal, and web/data/index.json
"""
import os, json, re

HERE = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.abspath(os.path.join(HERE, "..", "web"))
DATA = os.path.join(WEB, "data")
MANIFEST = os.path.join(WEB, "extracted-manifest.json")
WF_RESULT = os.environ.get("WF_RESULT", os.path.join(WEB, "wf_result.json"))

PROV = {
    "source": "Microsoft Dangerous Creatures (1994) CD-ROM",
    "note": "Text liberated from original screen art; images & clip restored from disc. "
            "Original media is Microsoft/supplier copyright — placeholder pending swap to open-licensed assets.",
}


def asset(slug, name):
    return f"assets/{slug}/{name}"


# --- browse taxonomies, derived from the liberated facts ---
WEAPON_RULES = [
    ("Venom & Poison", ["venom", "poison"]),
    ("Teeth & Jaws", ["bit", "jaw", "teeth"]),
    ("Claws & Talons", ["claw", "talon"]),
    ("Constriction", ["squeez", "constrict"]),
    ("Stings", ["sting"]),
    ("Horns, Tusks & Charging", ["horn", "tusk", "trampl", "gor", "charg", "slash"]),
    ("Electric Shock", ["electric"]),
    ("Spines & Quills", ["spine", "spiny", "quill"]),
    ("Disease Carriers", ["disease", "virus", "rabies", "plague", "infection", "infectious"]),
    ("Pack & Swarm Attacks", ["swarm", "group attack", "pack"]),
    ("Pincers", ["pincer"]),
]
REGION_RULES = [
    ("Africa", ["africa", "african", "madagascar"]),
    ("Asia", ["asia", "asian", "india", "china", "chinese", "indonesia", "thailand", "siberia", "siberian", "arabia", "arabian", "middle east", "southeast asia"]),
    ("Europe", ["europe", "european"]),
    ("North America", ["north america", "united states", "alaska", "canada", "greenland", "mexico", "florida"]),
    ("Central America", ["central america"]),
    ("South America", ["south america", "amazon"]),
    ("Australia & Oceania", ["australia", "australian", "australasia", "australasian", "tasmania", "tasmanian", "pacific island", "oceania"]),
    ("Oceans & Seas", ["sea", "ocean", "reef", "coral", "marine", "saltwater", "coastal"]),
    ("Polar Regions", ["arctic", "antarctic", "polar", "subarctic", "subantarctic"]),
    ("Worldwide", ["worldwide", "everywhere"]),
]


# Category/cross-links for the original main-screen hotspots that pointed at the game's
# guide/collection screens (now served by the Browse modes).
HOTSPOT_LINKS = {
    "arow": {"Fighting Back": "browse.html?tab=weapons#venom-poison"},
    "cdog": {"Packs and Partners": "browse.html?tab=weapons#pack-swarm-attacks"},
    "chee": {"Grassland Environments": "browse.html?tab=habitats#grassland-savanna"},
    "scor": {"Venom Producers": "browse.html?tab=weapons#venom-poison"},
    "wasp": {"Tarantula eaters": "animal.html?id=tran&mode=classic"},
}


def _hit(text, kw, mode):
    if mode == "word":      # whole word, plural-tolerant (regions: India != Indian Ocean)
        return bool(re.search(r"\b" + re.escape(kw) + r"s?\b", text))
    # "stem": word-initial stem, any suffix (weapons: venom->venomous, but twisting!=sting)
    return bool(re.search(r"\b" + re.escape(kw), text))


def derive_tags(text, rules, mode):
    t = (text or "").lower()
    return [label for label, kws in rules if any(_hit(t, kw, mode) for kw in kws)]


def main():
    manifest = json.load(open(MANIFEST))
    result = json.load(open(WF_RESULT))
    animals = result["animals"]
    cons = result.get("consistency") or {}

    # consistency patches (tagline / name / scientificName only)
    patches = {}
    for p in cons.get("patches", []):
        if p.get("field") in ("tagline", "name", "scientificName"):
            patches.setdefault(p["id"], {})[p["field"]] = p["value"]
    canon = cons.get("canonicalFactLabels") or []

    corr_path = os.path.join(HERE, "corrections.json")
    CORR = json.load(open(corr_path)) if os.path.exists(corr_path) else {}

    hab_path = os.path.join(HERE, "habitats.json")
    HAB = json.load(open(hab_path)) if os.path.exists(hab_path) else {}
    HABITAT_ORDER = HAB.get("_order", [])

    ref_path = os.path.join(HERE, "hotspots_refined.json")
    REFINED = json.load(open(ref_path)) if os.path.exists(ref_path) else {}

    name_to_slug = {a["name"].strip().lower(): a["id"] for a in animals}
    all_slugs = {a["id"] for a in animals}
    LABEL_FIX = {"watch out!": "Watch out", "favorite food": "Favorite meals"}

    def norm_label(lbl):
        key = lbl.strip().lower()
        if key in LABEL_FIX:
            return LABEL_FIX[key]
        bare = key.rstrip("!").strip()
        for c in canon:
            if c.lower() == bare:
                return c
        return lbl.strip()

    os.makedirs(DATA, exist_ok=True)
    index = []
    report = {"external": [], "disabled": []}
    weapons_map, regions_map, habitats_map = {}, {}, {}
    quiz_rows = []

    for d in animals:
        slug = d["id"]
        man = manifest.get(slug, {})
        stems = man.get("screens", [])
        code = d.get("code", slug.upper())
        for field, val in patches.get(slug, {}).items():
            d[field] = val

        main_stem = next((s for s in stems if s.endswith("00AA")), f"{code}00AA")
        fb_stem = next((s for s in stems if "FB" in s), None)
        tv_stem = d.get("video", {}).get("screen") or next((s for s in stems if s.endswith("TV")), None)
        has_video = bool(man.get("video"))
        has_narr = bool(man.get("narration"))

        # facts: normalize labels then order by canonical labels when available
        facts = d.get("facts", [])
        for f in facts:
            f["label"] = norm_label(f["label"])
        if canon:
            facts = sorted(facts, key=lambda f: canon.index(f["label"]) if f["label"] in canon else len(canon))

        # derive browse taxonomies from the structured facts
        factmap = {f["label"]: f["value"] for f in facts}
        weapons = derive_tags(factmap.get("How it kills", ""), WEAPON_RULES, mode="stem")
        regions = derive_tags(factmap.get("Where it lives", ""), REGION_RULES, mode="word")
        habitats = HAB.get(slug, [])
        for w in weapons:
            weapons_map.setdefault(w, []).append(slug)
        for r in regions:
            regions_map.setdefault(r, []).append(slug)
        for h in habitats:
            habitats_map.setdefault(h, []).append(slug)
        quiz_rows.append({
            "id": slug, "name": d["name"], "thumb": asset(slug, main_stem + ".webp"),
            "weapons": weapons, "habitats": habitats, "regions": regions,
            "diet": factmap.get("Favorite meals", ""), "kill": factmap.get("How it kills", ""),
        })

        topics = []
        for t in d.get("topics", []):
            topic = {
                "id": t["id"], "title": t["title"],
                "image": asset(slug, t["screen"] + ".webp"),
                "text": t["text"],
            }
            if t.get("captions"):
                topic["captions"] = t["captions"]
            topics.append(topic)

        video = None
        if has_video:
            video = {
                "title": d.get("video", {}).get("title", "Watch"),
                "src": asset(slug, "clip.mp4"),
                "poster": asset(slug, (tv_stem or main_stem) + ".webp"),
                "caption": d.get("video", {}).get("caption", ""),
            }

        # classic mode graph
        screens = {"main": {"image": asset(slug, main_stem + ".webp"), "hotspots": []}}
        for t in d.get("topics", []):
            screens[t["id"]] = {"image": asset(slug, t["screen"] + ".webp"), "back": "main"}
        if fb_stem:
            screens["facts"] = {"image": asset(slug, fb_stem + ".webp"), "back": "main"}
        if has_video:
            screens["video"] = {"video": asset(slug, "clip.mp4"),
                                "poster": asset(slug, (tv_stem or main_stem) + ".webp"), "back": "main"}

        # resolve main-screen hotspots: local screen | cross-animal link | disabled
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
            if cand and cand != slug:
                nh = {k: v for k, v in h.items() if k != "to"}
                nh["external"] = f"animal.html?id={cand}"
                resolved.append(nh)
                report["external"].append(f"{slug}:{h.get('label')}->{cand}")
            else:
                link = HOTSPOT_LINKS.get(slug, {}).get((h.get("label") or "").strip())
                nh = {k: v for k, v in h.items() if k != "to"}
                if link:
                    nh["link"] = link
                    report.setdefault("linked", []).append(f"{slug}:{h.get('label')}")
                else:
                    nh["disabled"] = True
                    report["disabled"].append(f"{slug}:{h.get('label')}")
                resolved.append(nh)
        rf = REFINED.get(slug, {})
        for h in resolved:
            if h.get("label") in rf:
                h.update(rf[h["label"]])
        screens["main"]["hotspots"] = resolved

        sci_raw = d.get("scientificName", "")
        needs_sci = "(unverified)" in sci_raw.lower()
        sci = re.sub(r"\s*\(unverified\)\s*$", "", sci_raw, flags=re.I).strip()

        page = {
            "id": slug, "code": code, "name": d["name"],
            "scientificName": sci,
            "needsScientificVerify": needs_sci,
            "tagline": d.get("tagline", ""),
            "weapons": weapons,
            "habitats": habitats,
            "regions": regions,
            "hero": {"image": asset(slug, main_stem + ".webp"), "alt": d["name"]},
            "intro": d.get("intro", ""),
            "facts": facts,
            "topics": topics,
            "classic": {"start": "main", "screens": screens},
            "_provenance": PROV,
        }
        if has_narr:
            page["narration"] = asset(slug, "narration.mp3")
        if video:
            page["video"] = video

        # manual accuracy overrides (verified names, factual-flag fixes)
        ov = CORR.get(slug, {})
        if ov:
            page.update(ov)
            if "scientificName" in ov:
                page["needsScientificVerify"] = False

        json.dump(page, open(os.path.join(DATA, f"{slug}.json"), "w"), indent=2, ensure_ascii=False)

        # thumbnail = the main article portrait (00AA), which always shows the
        # actual animal. The video still (TV) often depicts prey or a rival.
        thumb = asset(slug, main_stem + ".webp")
        index.append({"id": slug, "name": d["name"], "thumb": thumb})

    if os.environ.get("SKIP_INDEX") != "1":
        index.sort(key=lambda x: x["name"])
        json.dump(index, open(os.path.join(DATA, "index.json"), "w"), indent=2, ensure_ascii=False)

        # browse indexes (Atlas by region, Weapons by attack)
        by_id = {e["id"]: e for e in index}

        def categories(amap, order):
            out = []
            for label in order:
                slugs = amap.get(label, [])
                if slugs:
                    animals = sorted((by_id[s] for s in slugs), key=lambda e: e["name"])
                    out.append({"category": label, "count": len(animals), "animals": animals})
            return out

        browse = {
            "regions": categories(regions_map, [l for l, _ in REGION_RULES]),
            "weapons": categories(weapons_map, [l for l, _ in WEAPON_RULES]),
            "habitats": categories(habitats_map, HABITAT_ORDER),
        }
        json.dump(browse, open(os.path.join(DATA, "browse.json"), "w"), indent=2, ensure_ascii=False)
        json.dump(quiz_rows, open(os.path.join(DATA, "quiz.json"), "w"), indent=2, ensure_ascii=False)
    print(f"wrote {len(animals)} page files{'' if os.environ.get('SKIP_INDEX')=='1' else ' + index.json'} -> {DATA}")
    print(f"cross-animal links resolved: {len(report['external'])}  ->  {', '.join(report['external'])}")
    print(f"category-link hotspots wired: {len(report.get('linked', []))}  ->  {', '.join(report.get('linked', []))}")
    print(f"disabled hotspots remaining: {len(report['disabled'])}  ->  {', '.join(report['disabled']) or 'none'}")


if __name__ == "__main__":
    main()
