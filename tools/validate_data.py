#!/usr/bin/env python3
"""Validate the built per-animal page JSON files."""
import os, json, glob

HERE = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.abspath(os.path.join(HERE, "..", "web"))
DATA = os.path.join(WEB, "data")

REQ = ["id", "code", "name", "scientificName", "tagline", "hero", "intro", "facts", "topics", "classic"]
problems = []
label_counts = {}
n = 0

for fp in sorted(glob.glob(os.path.join(DATA, "*.json"))):
    if os.path.basename(fp) in ("index.json", "browse.json"):
        continue
    n += 1
    d = json.load(open(fp))
    slug = d.get("id", os.path.basename(fp))

    def has(p):
        return os.path.exists(os.path.join(WEB, p))

    for k in REQ:
        if k not in d or d[k] in ("", None):
            problems.append(f"{slug}: missing/empty {k}")
    if len(d.get("intro", "")) < 30:
        problems.append(f"{slug}: intro too short ({len(d.get('intro',''))} chars)")
    if not d.get("topics"):
        problems.append(f"{slug}: no topics")
    if not has(d.get("hero", {}).get("image", "")):
        problems.append(f"{slug}: hero image missing on disk")
    for t in d.get("topics", []):
        if not has(t.get("image", "")):
            problems.append(f"{slug}: topic image missing {t.get('image')}")
        for c in t.get("captions", []):
            if not c.get("label") or not c.get("text"):
                problems.append(f"{slug}: empty caption label/text in {t.get('id')}")
    # hotspot targets must resolve to a classic screen
    screens = set(d.get("classic", {}).get("screens", {}))
    for h in d["classic"]["screens"].get("main", {}).get("hotspots", []):
        if h.get("external") or h.get("disabled"):
            continue
        if h.get("to") not in screens:
            problems.append(f"{slug}: hotspot '{h.get('label')}' -> '{h.get('to')}' has no screen")
    v = d.get("video")
    if v and not has(v.get("src", "")):
        problems.append(f"{slug}: video src missing {v.get('src')}")
    for f in d.get("facts", []):
        label_counts[f["label"]] = label_counts.get(f["label"], 0) + 1

print(f"validated {n} animals")
print(f"\nfact-label vocabulary ({len(label_counts)} distinct):")
for lbl, c in sorted(label_counts.items(), key=lambda x: -x[1]):
    print(f"  {c:3}  {lbl!r}")
print(f"\n{len(problems)} problems:")
for p in problems[:60]:
    print("  -", p)
