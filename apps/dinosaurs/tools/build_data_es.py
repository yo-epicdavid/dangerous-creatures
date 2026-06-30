#!/usr/bin/env python3
"""Build the Castilian-Spanish Dinosaurs data by overlaying the AI fan-translation onto the
English structure. UNLIKE DC/Oceans there is NO Spanish disc, so assets are NOT relocated —
the es pages reuse the ENGLISH media (screens, audio, video). Only text is translated; period
and diet are translated via dicts; every page is marked as an unofficial fan translation.
-> web/data/es/<id>.json + index.json + browse.json.

Input: web/wf_result_es.json (env WF_RESULT) + web/data/<id>.json
"""
import os, json, html

HERE = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.abspath(os.path.join(HERE, "..", "web"))
DATA_EN = os.path.join(WEB, "data")
DATA_ES = os.path.join(DATA_EN, "es")
WF_ES = os.environ.get("WF_RESULT", os.path.join(WEB, "wf_result_es.json"))

PERIOD_ES = {
    "Cretaceous": "Cretácico", "Late Cretaceous": "Cretácico superior", "Early Cretaceous": "Cretácico inferior",
    "Jurassic": "Jurásico", "Late Jurassic": "Jurásico superior", "Early Jurassic": "Jurásico inferior",
    "Triassic": "Triásico", "Late Triassic": "Triásico superior", "Early Triassic": "Triásico inferior",
    "Permian": "Pérmico", "Early Permian": "Pérmico inferior", "Present": "Actualidad",
    "Devonian-Present": "Devónico-Actualidad", "Devonian - Cretaceous": "Devónico - Cretácico",
    "Cambrian - Permian": "Cámbrico - Pérmico",
}
DIET_ES = {"Carnivore": "Carnívoro", "Herbivore": "Herbívoro", "Omnivore": "Omnívoro"}
PERIOD_GROUP_ES = {"Triassic": "Triásico", "Jurassic": "Jurásico", "Cretaceous": "Cretácico"}
CATEGORY_LABEL_ES = {"dinosaur": "Dinosaurios", "creature": "Criaturas prehistóricas", "concept": "Ciencia de los dinosaurios"}
PROV_ES = {
    "source": "«Microsoft Dinosaurs» (1993) — traducción no oficial de aficionados",
    "note": "Traducción al español generada con IA a partir del texto original en inglés. «Microsoft "
            "Dinosaurs» nunca se publicó en español; las imágenes, el audio y el vídeo son los originales "
            "EN INGLÉS. Preservación educativa sin ánimo de lucro; contenido original © Microsoft y sus proveedores.",
}


def clean(o):
    if isinstance(o, str):
        return html.unescape(o)
    if isinstance(o, list):
        return [clean(x) for x in o]
    if isinstance(o, dict):
        return {k: clean(v) for k, v in o.items()}
    return o


def build_browse(es_index):
    src = os.path.join(DATA_EN, "browse.json")
    if not os.path.exists(src):
        print("  !! no English browse.json; skip browse-es")
        return
    by_id = {a["id"]: a for a in es_index}
    LABELMAP = {"categories": CATEGORY_LABEL_ES, "periods": PERIOD_GROUP_ES, "diets": DIET_ES}
    out = {}
    for axis, groups in json.load(open(src)).items():
        lm = LABELMAP.get(axis, {})
        newgroups = []
        for g in groups:
            items = [{"id": a["id"], "name": by_id[a["id"]]["name"], "category": by_id[a["id"]]["category"],
                      "thumb": by_id[a["id"]]["thumb"]}
                     for a in g["items"] if a["id"] in by_id]
            items.sort(key=lambda a: a["name"].lower())
            label = lm.get(g.get("key"), lm.get(g.get("label"), g.get("label")))
            # categories keep the canonical key; periods/diets use the Spanish label so chips match.
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
        if p.get("field") in ("name", "tagline"):
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

        page = json.load(open(en_path))   # English structure — assets stay English (no Spanish disc)
        page["name"] = es["name"]
        page["tagline"] = es.get("tagline", page.get("tagline", ""))
        page["intro"] = es.get("intro", page.get("intro", ""))
        page["facts"] = es.get("facts", page.get("facts"))
        page["hero"]["alt"] = es["name"]
        if es.get("meaning"):
            page["meaning"] = es["meaning"]
        if page.get("period"):
            page["period"] = PERIOD_ES.get(page["period"], page["period"])
        if page.get("diet"):
            page["diet"] = DIET_ES.get(page["diet"], page["diet"])

        # overlay Spanish topic text by id (the translator keeps the English ids)
        es_by_id = {t["id"]: t for t in es.get("topics", [])}
        for t in page.get("topics", []):
            est = es_by_id.get(t["id"])
            if est:
                t["title"] = est.get("title", t["title"])
                t["text"] = est.get("text", t["text"])
                if est.get("captions"):
                    t["captions"] = est["captions"]
                elif "captions" in t:
                    del t["captions"]

        if es.get("video") and page.get("video"):
            page["video"]["title"] = es["video"].get("title") or page["video"].get("title")
            page["video"]["caption"] = es["video"].get("caption") or page["video"].get("caption")

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
            elif to in ("sayit", "say"):
                h["label"] = "Cómo se dice"
            elif ext in es_name:
                h["label"] = es_name[ext]

        page["_provenance"] = PROV_ES
        page["fanTranslation"] = True
        page = clean(page)
        json.dump(page, open(os.path.join(DATA_ES, f"{slug}.json"), "w"), indent=2, ensure_ascii=False)
        index.append({"id": slug, "name": es["name"], "category": page["category"], "thumb": page["hero"]["image"]})

    index.sort(key=lambda x: x["name"])
    json.dump(index, open(os.path.join(DATA_ES, "index.json"), "w"), indent=2, ensure_ascii=False)
    print(f"wrote {len(index)} Spanish page files + index.json -> {DATA_ES}")
    build_browse(index)


if __name__ == "__main__":
    main()
