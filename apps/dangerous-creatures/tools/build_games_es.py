#!/usr/bin/env python3
"""Build the Spanish game data: web/data/es/quiz.json + web/data/es/games_eyes.json.

The Survival Quiz is rebuilt from the Spanish animal pages (Spanish names + weapons/habitats,
es video-frame photos). Whose Eyes Are These? reuses the language-neutral eye photos and just
swaps the answer to the Spanish animal name. Run after build_data_es.py.
"""
import os, json, glob

HERE = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.abspath(os.path.join(HERE, "..", "web"))
DATA_EN = os.path.join(WEB, "data")
DATA_ES = os.path.join(DATA_EN, "es")

# Eye-puzzle answers that aren't one of the 66 main animals get a manual Spanish name.
EYES_EXTRA_ES = {
    "Snowy Owl": "Búho nival", "Grass Snake": "Culebra de collar", "Bat": "Murciélago",
    "Green Iguana": "Iguana verde", "Toad": "Sapo", "Rainbow Trout": "Trucha arcoíris",
    "Bald Eagle": "Águila calva", "Mandrill": "Mandril", "Frog": "Rana", "Crocodile": "Cocodrilo",
}


def en_to_es_name():
    """Map each English animal name -> its Spanish name via the per-slug page data."""
    out = {}
    for f in glob.glob(os.path.join(DATA_ES, "*.json")):
        if os.path.basename(f) in ("index.json", "browse.json", "quiz.json", "games_eyes.json"):
            continue
        es = json.load(open(f))
        slug = es.get("id")
        en_path = os.path.join(DATA_EN, f"{slug}.json")
        if slug and os.path.exists(en_path):
            out[json.load(open(en_path))["name"].strip().lower()] = es["name"]
    return out


def build_quiz():
    rows = []
    for f in sorted(glob.glob(os.path.join(DATA_ES, "*.json"))):
        if os.path.basename(f) in ("index.json", "browse.json", "quiz.json", "games_eyes.json"):
            continue
        d = json.load(open(f))
        if not (isinstance(d, dict) and d.get("id") and d.get("classic")):
            continue
        slug = d["id"]
        factmap = {fa["label"]: fa["value"] for fa in d.get("facts", [])}
        poster = f"assets/{slug}/poster.webp"   # video-frame photo is language-neutral; reuse the English one
        rows.append({
            "id": slug, "name": d["name"], "thumb": d["hero"]["image"],
            "photo": poster if os.path.exists(os.path.join(WEB, poster)) else None,
            "weapons": d.get("weapons", []), "habitats": d.get("habitats", []),
            "regions": d.get("regions", []),
            "diet": factmap.get("Comida favorita", ""), "kill": factmap.get("Cómo mata", ""),
        })
    json.dump(rows, open(os.path.join(DATA_ES, "quiz.json"), "w"), indent=2, ensure_ascii=False)
    print(f"wrote quiz.json ({len(rows)} entries, {sum(1 for r in rows if r['photo'])} with photo) -> {DATA_ES}")


def build_eyes():
    src = os.path.join(DATA_EN, "games_eyes.json")
    if not os.path.exists(src):
        print("  !! no English games_eyes.json; skip")
        return
    name_map = en_to_es_name()
    g = json.load(open(src))
    miss = []
    for p in g.get("puzzles", []):
        en = (p.get("answer") or "").strip()
        es = name_map.get(en.lower()) or EYES_EXTRA_ES.get(en)
        if es:
            p["answer"] = es
        else:
            miss.append(en)
    g["_note"] = "Versión en español — fotos originales del disco, nombres en castellano."
    g["title"] = "¿De quién son estos ojos?"
    json.dump(g, open(os.path.join(DATA_ES, "games_eyes.json"), "w"), indent=2, ensure_ascii=False)
    print(f"wrote games_eyes.json ({len(g.get('puzzles', []))} puzzles) -> {DATA_ES}"
          + (f"  | untranslated: {miss}" if miss else ""))


if __name__ == "__main__":
    build_quiz()
    build_eyes()
