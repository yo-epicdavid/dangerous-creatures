#!/usr/bin/env python3
"""Build the Castilian-Spanish Oceans data by overlaying the Spanish liberation text onto the
English structure (web/data/<id>.json), rewiring EVERY asset path to assets/es/ (Spanish
screens, narration, sounds, video), translating zone/ocean/category labels, and making
classic-mode hotspot + crosslink labels Spanish. -> web/data/es/<id>.json + index.json + browse.json.

Reuses from English (language-neutral): category, scientificName, zones/oceans grouping,
crosslink/hotspot targets and geometry, the classic scene graph.
Input: web/wf_result_es.json (env WF_RESULT) + web/data/<id>.json + web/extracted-manifest-es.json
"""
import os, json, html

HERE = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.abspath(os.path.join(HERE, "..", "web"))
DATA_EN = os.path.join(WEB, "data")
DATA_ES = os.path.join(DATA_EN, "es")
WF_ES = os.environ.get("WF_RESULT", os.path.join(WEB, "wf_result_es.json"))

ZONES_ES = {
    "Coast & tide pools": "Costa y charcas de marea", "Coral reef": "Arrecife de coral",
    "Kelp & seagrass": "Bosques de algas y praderas marinas", "Open ocean": "Mar abierto",
    "Deep sea": "Mar profundo", "Polar seas": "Mares polares", "Rivers & estuaries": "Ríos y estuarios",
}
OCEANS_ES = {
    "Pacific Ocean": "Océano Pacífico", "Atlantic Ocean": "Océano Atlántico",
    "Indian Ocean": "Océano Índico", "Arctic Ocean": "Océano Ártico",
    "Southern Ocean": "Océano Antártico", "Antarctic Ocean": "Océano Antártico",
    "Mediterranean Sea": "Mar Mediterráneo", "Caribbean Sea": "Mar Caribe", "Red Sea": "Mar Rojo",
    "North Sea": "Mar del Norte", "Baltic Sea": "Mar Báltico", "Black Sea": "Mar Negro",
    "Worldwide": "En todo el mundo",
}
CATEGORY_LABEL_ES = {
    "creature": "Vida marina", "habitat": "Hábitats", "concept": "Cómo funciona el océano",
    "place": "Mares y regiones", "human": "Las personas y el mar",
}
PROV_ES = {
    "source": "CD-ROM «Océanos de Microsoft» (1995)",
    "note": "Texto liberado del arte original de las pantallas; imágenes, audio y vídeo restaurados "
            "del disco. El contenido original es propiedad de Microsoft y sus proveedores — "
            "preservación educativa sin ánimo de lucro.",
}


def reloc(obj, slug):
    if isinstance(obj, str):
        return obj.replace(f"assets/{slug}/", f"assets/es/{slug}/")
    if isinstance(obj, list):
        return [reloc(x, slug) for x in obj]
    if isinstance(obj, dict):
        return {k: reloc(v, slug) for k, v in obj.items()}
    return obj


def clean(o):
    if isinstance(o, str):
        return html.unescape(o)
    if isinstance(o, list):
        return [clean(x) for x in o]
    if isinstance(o, dict):
        return {k: clean(v) for k, v in o.items()}
    return o


def screen_of(image):
    return os.path.splitext(os.path.basename(image))[0]


def build_browse(es_index):
    src = os.path.join(DATA_EN, "browse.json")
    if not os.path.exists(src):
        print("  !! no English browse.json; skip browse-es")
        return
    by_id = {a["id"]: a for a in es_index}
    LABELMAP = {"categories": CATEGORY_LABEL_ES, "zones": ZONES_ES, "oceans": OCEANS_ES}
    en = json.load(open(src))
    out = {}
    for axis, groups in en.items():
        lm = LABELMAP.get(axis, {})
        newgroups = []
        for g in groups:
            items = [{"id": a["id"], "name": by_id[a["id"]]["name"], "category": by_id[a["id"]]["category"],
                      "thumb": by_id[a["id"]]["thumb"]}
                     for a in g["items"] if a["id"] in by_id]
            items.sort(key=lambda a: a["name"].lower())
            label = lm.get(g.get("key"), lm.get(g.get("label"), g.get("label")))
            # categories keep the canonical key (entry chips link by raw category value);
            # zones/oceans use the Spanish label as the anchor so chips' catSlug() matches.
            key = g.get("key") if axis == "categories" else label
            newgroups.append({"key": key, "label": label, "count": len(items), "items": items})
        out[axis] = newgroups
    json.dump(out, open(os.path.join(DATA_ES, "browse.json"), "w"), indent=2, ensure_ascii=False)
    print(f"wrote browse.json ({sum(len(v) for v in out.values())} groups) -> {DATA_ES}")


def main():
    res = json.load(open(WF_ES))
    es_entries = {e["id"]: clean(e) for e in res["entries"]}
    cons = res.get("consistency") or {}
    patches = {}
    for p in cons.get("patches", []):
        if p.get("field") in ("tagline", "name"):
            patches.setdefault(p["id"], {})[p["field"]] = p["value"]
    es_name = {i: e["name"] for i, e in es_entries.items()}

    os.makedirs(DATA_ES, exist_ok=True)
    index = []
    for slug, es in sorted(es_entries.items()):
        en_path = os.path.join(DATA_EN, f"{slug}.json")
        if not os.path.exists(en_path):
            print(f"  !! no English data for {slug}; skip")
            continue
        for f, v in patches.get(slug, {}).items():
            es[f] = v

        page = reloc(json.load(open(en_path)), slug)   # English structure, assets -> es/
        page["name"] = es["name"]
        page["tagline"] = es.get("tagline", "")
        page["intro"] = es.get("intro", "")
        page["facts"] = es.get("facts", page.get("facts"))
        page["hero"]["alt"] = es["name"]
        page["zones"] = [ZONES_ES.get(z, z) for z in page.get("zones", [])]
        page["oceans"] = [OCEANS_ES.get(o, o) for o in page.get("oceans", [])]

        # overlay Spanish topic text by screen
        es_by_screen = {t["screen"]: t for t in es.get("topics", [])}
        for t in page.get("topics", []):
            est = es_by_screen.get(screen_of(t["image"]))
            if est:
                t["title"] = est.get("title", t["title"])
                t["text"] = est.get("text", t["text"])
                if est.get("captions"):
                    t["captions"] = est["captions"]
                elif "captions" in t:
                    del t["captions"]

        # Spanish video title/caption
        if es.get("video") and page.get("video"):
            page["video"]["title"] = es["video"].get("title") or page["video"].get("title")
            page["video"]["caption"] = es["video"].get("caption") or page["video"].get("caption")

        # Spanish crosslink labels -> the target entry's Spanish name
        for c in page.get("crosslinks", []):
            if c.get("to") in es_name:
                c["label"] = es_name[c["to"]]

        # Spanish classic-mode hotspot tooltips
        title_by_id = {t["id"]: t["title"] for t in page.get("topics", [])}
        for h in page["classic"]["screens"]["main"].get("hotspots", []):
            to, ext = h.get("to"), h.get("external")
            if to in title_by_id:
                h["label"] = title_by_id[to]
            elif to == "facts":
                h["label"] = "Datos"
            elif to == "video" and page.get("video"):
                h["label"] = page["video"].get("title", h.get("label"))
            elif to == "quiz":
                h["label"] = "Cuestionario"
            elif ext in es_name:
                h["label"] = es_name[ext]

        page["_provenance"] = PROV_ES
        page = clean(page)
        json.dump(page, open(os.path.join(DATA_ES, f"{slug}.json"), "w"), indent=2, ensure_ascii=False)
        index.append({"id": slug, "name": es["name"], "category": page["category"],
                      "thumb": page["hero"]["image"]})

    index.sort(key=lambda x: x["name"])
    json.dump(index, open(os.path.join(DATA_ES, "index.json"), "w"), indent=2, ensure_ascii=False)
    print(f"wrote {len(index)} Spanish page files + index.json -> {DATA_ES}")
    build_browse(index)


if __name__ == "__main__":
    main()
