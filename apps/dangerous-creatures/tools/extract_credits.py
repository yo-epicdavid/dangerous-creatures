#!/usr/bin/env python3
"""Extract photographer / agency / reference-work credits embedded in MSDANGER.THE
into web/data/credits.json for the acknowledgements page.
"""
import os, re, json

HERE = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.abspath(os.path.join(HERE, "..", "web"))
THE = "/Volumes/DANGEROUS/XFILES/APP/MSDANGER.THE"

AGENCIES = [
    "Photo Researchers, Inc.", "Animals Animals", "Oxford Scientific Films", "Earth Scenes",
    "ALLSTOCK, Inc.", "Science Photo Library", "Science Source", "World Wildlife Fund",
    "Norbert Wu", "NAS Collection", "Okapia", "Dorling Kindersley Limited", "Sea Studios",
]


def clean(s):
    s = s.strip().strip("/").strip()
    s = re.sub(r"\s+", " ", s)
    s = s.replace("ALLSTOCK, INC.", "ALLSTOCK, Inc.")
    return s


def main():
    data = open(THE, "rb").read()
    strings = [m.decode("latin-1") for m in re.findall(rb"[\x20-\x7e]{6,}", data)]

    credits, refs = set(), set()
    for s in strings:
        if "Courtesy of" in s:
            # reference work?  "Amazing Worlds Amazing Bats (c) 1991. Courtesy of"
            m = re.match(r"(.+?)\s*\(c\)\s*(\d{4})\.\s*Courtesy of", s)
            if m:
                refs.add(f"{clean(m.group(1))} ({m.group(2)})")
                continue
            who = clean(s.split("Courtesy of", 1)[1])
            if len(who) >= 3 and not who[0].isdigit():
                credits.add(who)

    # agencies actually present
    present = []
    blob = "\n".join(strings)
    for a in AGENCIES:
        if a.replace(", Inc.", "").split("/")[0] in blob:
            present.append(a)

    out = {
        "source": "Microsoft Dangerous Creatures (1994) — Microsoft Home, Microsoft Corporation",
        "agencies": present,
        "credits": sorted(credits, key=str.lower),
        "referenceWorks": sorted(refs, key=str.lower),
    }
    os.makedirs(os.path.join(WEB, "data"), exist_ok=True)
    json.dump(out, open(os.path.join(WEB, "data", "credits.json"), "w"), indent=2, ensure_ascii=False)
    print(f"agencies: {len(present)} | individual credits: {len(credits)} | reference works: {len(refs)}")
    print("sample credits:", out["credits"][:5])
    print("reference works:", out["referenceWorks"][:8])


if __name__ == "__main__":
    main()
