#!/usr/bin/env python3
"""Build the Castilian-Spanish DC data by overlaying the Spanish liberation text onto the
English structure (web/data/<id>.json), rewiring EVERY asset path to assets/es/ (Spanish
screens, narration, sounds, video), translating browse labels, and making classic-mode
hotspot tooltips Spanish. -> web/data/es/<id>.json + web/data/es/index.json.

Reuses from English (language-neutral): scientific names, region/habitat/weapon categories,
hotspot positions/targets, the classic scene graph.
"""
import os, json

HERE = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.abspath(os.path.join(HERE, "..", "web"))
DATA_EN = os.path.join(WEB, "data")
DATA_ES = os.path.join(DATA_EN, "es")
WF_ES = os.path.join(WEB, "wf_result_es.json")

WEAPONS_ES = {
    "Venom & Poison": "Veneno y ponzoña", "Teeth & Jaws": "Dientes y mandíbulas",
    "Claws & Talons": "Garras y zarpas", "Constriction": "Constricción", "Stings": "Aguijones",
    "Horns, Tusks & Charging": "Cuernos, colmillos y embestidas", "Electric Shock": "Descarga eléctrica",
    "Spines & Quills": "Púas y espinas", "Disease Carriers": "Transmisores de enfermedades",
    "Pack & Swarm Attacks": "Ataques en grupo", "Pincers": "Pinzas",
}
HABITATS_ES = {
    "Cities & Farmland": "Ciudades y campos", "Desert": "Desierto", "Forest & Woodland": "Bosques",
    "Grassland & Savanna": "Praderas y sabanas", "Mountains": "Montañas",
    "Oceans & Coral Reefs": "Océanos y arrecifes de coral", "Polar & Tundra": "Zonas polares y tundra",
    "Rainforest & Jungle": "Selva tropical", "Rivers, Lakes & Wetlands": "Ríos, lagos y humedales",
}
REGIONS_ES = {
    "Africa": "África", "Asia": "Asia", "Australia & Oceania": "Australia y Oceanía",
    "Central America": "Centroamérica", "Europe": "Europa", "North America": "Norteamérica",
    "Oceans & Seas": "Océanos y mares", "Polar Regions": "Regiones polares",
    "South America": "Sudamérica", "Worldwide": "En todo el mundo",
}
LABELMAP = {"regions": REGIONS_ES, "habitats": HABITATS_ES, "weapons": WEAPONS_ES}
PROV_ES = {
    "source": "CD-ROM «Animales Peligrosos de Microsoft» (1995)",
    "note": "Texto liberado del arte original de las pantallas; imágenes, audio y vídeo restaurados "
            "del disco. El contenido original es propiedad de Microsoft y sus proveedores — "
            "preservación educativa sin ánimo de lucro.",
}


def reloc(obj, slug):
    """Recursively rewrite asset paths assets/<slug>/... -> assets/es/<slug>/..."""
    if isinstance(obj, str):
        return obj.replace(f"assets/{slug}/", f"assets/es/{slug}/")
    if isinstance(obj, list):
        return [reloc(x, slug) for x in obj]
    if isinstance(obj, dict):
        return {k: reloc(v, slug) for k, v in obj.items()}
    return obj


def screen_of(image):
    return os.path.splitext(os.path.basename(image))[0]   # assets/es/lion/LION01PU.webp -> LION01PU


def build_browse(es_index):
    """Spanish browse.json: reuse the English grouping (language-neutral), translate the
    category labels, and swap in Spanish names + es thumbs, re-sorted in Spanish."""
    src = os.path.join(DATA_EN, "browse.json")
    if not os.path.exists(src):
        print("  !! no English browse.json; skip browse-es")
        return
    by_id = {a["id"]: a for a in es_index}
    out = {}
    for tab, groups in json.load(open(src)).items():
        labelmap = LABELMAP.get(tab, {})
        newgroups = []
        for g in groups:
            animals = [{"id": a["id"], "name": by_id[a["id"]]["name"], "thumb": by_id[a["id"]]["thumb"]}
                       for a in g["animals"] if a["id"] in by_id]
            animals.sort(key=lambda a: a["name"].lower())
            newgroups.append({"category": labelmap.get(g["category"], g["category"]),
                              "count": len(animals), "animals": animals})
        newgroups.sort(key=lambda x: x["category"].lower())
        out[tab] = newgroups
    json.dump(out, open(os.path.join(DATA_ES, "browse.json"), "w"), indent=2, ensure_ascii=False)
    print(f"wrote browse.json ({sum(len(v) for v in out.values())} groups across {len(out)} axes) -> {DATA_ES}")


def main():
    res = json.load(open(WF_ES))
    es_animals = {a["id"]: a for a in res["animals"]}
    cons = res.get("consistency") or {}
    patches = {}
    for p in cons.get("patches", []):
        if p.get("field") in ("tagline", "name", "scientificName"):
            patches.setdefault(p["id"], {})[p["field"]] = p["value"]

    os.makedirs(DATA_ES, exist_ok=True)
    index = []
    for slug, es in sorted(es_animals.items()):
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
        page["weapons"] = [WEAPONS_ES.get(w, w) for w in page.get("weapons", [])]
        page["habitats"] = [HABITATS_ES.get(h, h) for h in page.get("habitats", [])]
        page["regions"] = [REGIONS_ES.get(r, r) for r in page.get("regions", [])]

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

        # overlay Spanish video title/caption (the film label is Spanish on the disc)
        if es.get("video") and page.get("video"):
            page["video"]["title"] = es["video"].get("title") or page["video"].get("title")
            page["video"]["caption"] = es["video"].get("caption") or page["video"].get("caption")

        # Spanish classic-mode tooltips: topic title / Hechos / video title
        title_by_id = {t["id"]: t["title"] for t in page.get("topics", [])}
        for h in page["classic"]["screens"]["main"].get("hotspots", []):
            to = h.get("to")
            if to in title_by_id:
                h["label"] = title_by_id[to]
            elif to == "facts":
                h["label"] = "Hechos"
            elif to == "video" and page.get("video"):
                h["label"] = page["video"].get("title", h.get("label"))

        page["_provenance"] = PROV_ES
        json.dump(page, open(os.path.join(DATA_ES, f"{slug}.json"), "w"), indent=2, ensure_ascii=False)
        index.append({"id": slug, "name": es["name"], "thumb": page["hero"]["image"]})

    index.sort(key=lambda x: x["name"])
    json.dump(index, open(os.path.join(DATA_ES, "index.json"), "w"), indent=2, ensure_ascii=False)
    print(f"wrote {len(index)} Spanish page files + index.json -> {DATA_ES}")
    build_browse(index)


if __name__ == "__main__":
    main()
