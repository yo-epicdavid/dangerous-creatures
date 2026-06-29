#!/usr/bin/env python3
"""Extract the Oceans credits/acknowledgements embedded in MSOCEANS.THE -> web/data/credits.json.

The .THE holds an "Oceans Credits List" with SPECIAL MENTION / AUDIO CREDITS / VIDEO CREDITS
sections; video/image credits are "<Topic>.  Courtesy of <Agency>" lines.
"""
import os, re, json

HERE = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.abspath(os.path.join(HERE, "..", "web"))
DATA = os.path.join(WEB, "data")
THE = "/Volumes/MS_OCEANS/DATA/00SETUP/APP/MSOCEANS.THE"

NOTE = ("Microsoft Oceans (1995) was made with footage and images generously provided by the "
        "organizations below. This is a non-commercial, educational fan preservation; it is not "
        "affiliated with or endorsed by Microsoft or any listed organization. All original media "
        "remains © its respective owners. Content will be removed on request.")


def main():
    data = open(THE, "rb").read()
    strings = [m.decode("latin-1").strip() for m in re.findall(rb"[\x20-\x7e]{4,}", data)]
    try:
        start = next(i for i, s in enumerate(strings) if "Oceans Credits List" in s)
    except StopIteration:
        start = 0
    region = strings[start:start + 400]

    section = None
    video, audio, special = [], [], []
    sources = set()
    for s in region:
        if not s or "Oceans Credits List" in s:
            continue
        u = s.upper()
        if u.startswith("SPECIAL MENTION"):
            section = "special"; continue
        if "AUDIO CREDITS" in u:
            section = "audio"; continue
        if "VIDEO CREDITS" in u:
            section = "video"; continue
        m = re.match(r"^(.*?)\.\s+Courtesy of\s+(.+)$", s)
        if m:
            parts = [re.sub(r"\.+$", "", a).strip() for a in re.split(r"\s*/\s*", m.group(2)) if a.strip()]
            parts = [p for p in parts if p]
            video.append({"item": m.group(1).strip(), "source": " / ".join(parts)})
            sources.update(parts)
            continue
        if section == "audio" and 2 < len(s) < 90:
            audio.append(s)
        elif section == "special" and 2 < len(s) < 140:
            special.append(s)

    out = {
        "note": NOTE,
        "sources": sorted(sources, key=lambda x: x.lower()),
        "video": video,
        "audio": audio,
        "special": special,
    }
    os.makedirs(DATA, exist_ok=True)
    json.dump(out, open(os.path.join(DATA, "credits.json"), "w"), indent=2, ensure_ascii=False)
    print(f"sources={len(out['sources'])} video={len(video)} audio={len(audio)} special={len(special)}")
    print("sources:", "; ".join(out["sources"]))


if __name__ == "__main__":
    main()
