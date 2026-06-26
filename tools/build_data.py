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

        topics = []
        for t in d.get("topics", []):
            topic = {
                "id": t["id"], "title": t["title"],
                "image": asset(slug, t["screen"] + ".png"),
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
                "poster": asset(slug, (tv_stem or main_stem) + ".png"),
                "caption": d.get("video", {}).get("caption", ""),
            }

        # classic mode graph
        screens = {"main": {"image": asset(slug, main_stem + ".png"), "hotspots": []}}
        for t in d.get("topics", []):
            screens[t["id"]] = {"image": asset(slug, t["screen"] + ".png"), "back": "main"}
        if fb_stem:
            screens["facts"] = {"image": asset(slug, fb_stem + ".png"), "back": "main"}
        if has_video:
            screens["video"] = {"video": asset(slug, "clip.mp4"),
                                "poster": asset(slug, (tv_stem or main_stem) + ".png"), "back": "main"}

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
                nh = dict(h); nh["disabled"] = True
                resolved.append(nh)
                report["disabled"].append(f"{slug}:{h.get('label')}")
        screens["main"]["hotspots"] = resolved

        sci_raw = d.get("scientificName", "")
        needs_sci = "(unverified)" in sci_raw.lower()
        sci = re.sub(r"\s*\(unverified\)\s*$", "", sci_raw, flags=re.I).strip()

        page = {
            "id": slug, "code": code, "name": d["name"],
            "scientificName": sci,
            "needsScientificVerify": needs_sci,
            "tagline": d.get("tagline", ""),
            "hero": {"image": asset(slug, main_stem + ".png"), "alt": d["name"]},
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
        thumb = asset(slug, main_stem + ".png")
        index.append({"id": slug, "name": d["name"], "thumb": thumb})

    if os.environ.get("SKIP_INDEX") != "1":
        index.sort(key=lambda x: x["name"])
        json.dump(index, open(os.path.join(DATA, "index.json"), "w"), indent=2, ensure_ascii=False)
    print(f"wrote {len(animals)} page files{'' if os.environ.get('SKIP_INDEX')=='1' else ' + index.json'} -> {DATA}")
    print(f"cross-animal links resolved: {len(report['external'])}  ->  {', '.join(report['external'])}")
    print(f"disabled hotspots (category jumps, not yet built): {len(report['disabled'])}  ->  {', '.join(report['disabled'])}")


if __name__ == "__main__":
    main()
