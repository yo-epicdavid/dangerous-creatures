#!/usr/bin/env python3
"""Extract the Dinosaurs credits/acknowledgements from MSDINOS.THE -> web/data/credits.json.

The .THE holds AUDIO CREDITS / VIDEO CREDITS sections; many video credits are split across two
strings ("...Department of Library Services/American" + "Museum of Natural History").
"""
import os, re, json

HERE = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.abspath(os.path.join(HERE, "..", "web"))
DATA = os.path.join(WEB, "data")
THE = "/Volumes/DINOSAURS/XFILES/MSDINOS.THE"

NOTE = ("Microsoft Dinosaurs (1993) was made with footage, images, and music from the museums "
        "and artists below. This is a non-commercial, educational fan preservation; it is not "
        "affiliated with or endorsed by Microsoft or any listed organization. All original media "
        "remains © its respective owners. Content will be removed on request.")

INSTITUTIONS = [
    "American Museum of Natural History", "The Natural History Museum", "Natural History Museum",
    "Department of Library Services", "Smithsonian", "British Museum",
]


def main():
    data = open(THE, "rb").read()
    raw = [m.decode("latin-1").strip() for m in re.findall(rb"[\x20-\x7e]{3,}", data)]
    try:
        start = next(i for i, s in enumerate(raw) if "AUDIO CREDITS" in s.upper())
    except StopIteration:
        start = 0
    region = raw[start:start + 200]

    # stitch split credit lines back together
    merged, skip = [], False
    for i, s in enumerate(region):
        if skip:
            skip = False
            continue
        if s.endswith(("American", "Library", "/")) and i + 1 < len(region):
            merged.append((s + " " + region[i + 1]).replace("/ ", "/"))
            skip = True
        else:
            merged.append(s)

    CREDIT_RE = re.compile(r"\(c\)|©|Courtesy|Museum|Productions|Films|Inc\.|WHYY|Tippett|Windows on the World|\b19\d\d\b")
    section, audio, video, sources = None, [], [], set()
    dry = 0
    for s in merged:
        u = s.upper()
        if "AUDIO CREDITS" in u:
            section = "audio"; dry = 0; continue
        if "VIDEO CREDITS" in u or "IMAGES AND TEXT" in u:
            section = "video"; dry = 0; continue
        if len(s) < 3 or s.startswith("Copyright"):
            continue
        if section == "video":
            if CREDIT_RE.search(s):
                video.append(s); dry = 0
                m = re.search(r"\(c\)\s*\d{4}\s+(.+)$", s) or re.search(r"Courtesy\s+(.+)$", s)
                if m:
                    sources.add(re.sub(r"\s+", " ", m.group(1)).strip().rstrip("."))
                for inst in INSTITUTIONS:
                    if inst in s:
                        sources.add(inst)
        elif section == "audio" and len(s) < 90:
            audio.append(s)

    # normalize / dedupe sources, dedupe video, keep order
    def norm(s):
        return "American Museum of Natural History" if "American Museum" in s else s
    sources = {norm(s) for s in sources if s not in ("Natural History Museum", "Department of Library Services")}
    if any("Windows on the World" in v for v in video):
        sources.add("Windows on the World")
    seen, vid = set(), []
    for v in video:
        if v not in seen:
            seen.add(v); vid.append(v)

    out = {
        "note": NOTE,
        "sources": sorted(sources, key=lambda x: x.lower()),
        "video": vid,
        "audio": audio,
        "special": [],
    }
    os.makedirs(DATA, exist_ok=True)
    json.dump(out, open(os.path.join(DATA, "credits.json"), "w"), indent=2, ensure_ascii=False)
    print(f"sources={len(out['sources'])} video={len(vid)} audio={len(audio)}")
    print("sources:", "; ".join(out["sources"]))
    print("video sample:", vid[:4])


if __name__ == "__main__":
    main()
