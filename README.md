# Dangerous Creatures — reborn

A modern, web-native recreation of **Microsoft Dangerous Creatures (1994)** — the classic
multimedia wildlife explorer — so any kid can meet the planet's most fascinating animals
in a browser.

## Two modes, one pipeline

A header toggle switches between **Modern** (liberated text, responsive, accessible) and
**Classic 1994** (the original composite screens rendered 1:1 with recreated hotspot
navigation). Both run off the same extracted assets and the same per-animal JSON, so adding a
creature lights up both modes at once. Deep-link with `?mode=classic`. Classic hotspot
coordinates are placed per-screen (by eye for the Lion; from `MSDANGER.THE` at scale).

## Approach: hybrid rebuild

The original disc stores every screen as a *pre-composited bitmap* — photo, body text, and
hotspot labels are all painted into one image, then SZDD-compressed. Our strategy:

1. **Extract** the original media losslessly (images, narration, video).
2. **Liberate the text** out of the screen art into structured JSON — so it becomes
   selectable, accessible, translatable, and searchable.
3. **Rebuild** each animal as a responsive, accessible HTML page driven by that data.
4. **Swap media before public launch:** the original photos/clips are Microsoft + supplier
   copyright. Because the text is already liberated, going public only requires replacing the
   imagery with openly-licensed assets (Wikimedia, public-domain footage, CC).

## What's on the source disc (decoded)

| Asset | Count | Format on disc | Pipeline |
|---|---|---|---|
| Animals | 66 | one folder each (`LION`, `COBR`=cobra, `GWSH`=great white…) | → one page each |
| Images | ~3,350 | `.DIB` 256-color masters + `.BMP` 16-color twins, **SZDD-compressed** | SZDD → BMP → PNG/WebP |
| Audio | 2,183 | `.WAV` 22 kHz mono PCM | → MP3/AAC |
| Video | 109 | `.AVI` Microsoft Video 1 (`CRAM`) | ffmpeg → MP4/WebM |
| Master DB | 1 | `MSDANGER.THE` — hotspot map, nav graph, captions + photo credits | → JSON (TODO) |
| Mini-games | ~9 | `GAME/*.CJS` puzzles ("whose eyes?") | → JS games (TODO) |

**Per-animal asset grammar:** `00AA` main article · `01–05PU` sub-topic screens (hotspots) ·
`00FB/01FB` fact boxes · `06TV` video still + matching `.AVI`. Narration: `…AT` article,
`…AF` facts, `…NJ`×7 hotspot jumps, `…NP` pop-ups.

Original nav modes to recreate: **Atlas · Weapons · Guides · Habitats · Index.**

## Project layout

```
_source/            # raw ISO + extracted originals — GITIGNORED (copyright)
tools/
  szdd.py           # Microsoft SZDD/COMPRESS.EXE decompressor (lossless)
web/
  index.html        # landing / creature grid
  animal.html       # template, reads ?id=<animal>
  app.js            # renders one animal from its JSON
  styles.css
  data/<animal>.json
  assets/<animal>/  # extracted images, narration.mp3, clip.mp4
```

## Run locally

```bash
cd web
python3 -m http.server 8731
# open http://localhost:8731/  (or /animal.html?id=lion)
```
(A static server is required — the pages `fetch()` their JSON data.)

## Status

- ✅ ISO acquired, mounted, fully inventoried & format-decoded
- ✅ Lossless image pipeline (SZDD → bitmap → PNG)
- ✅ Media transcoding (WAV→MP3, AVI→MP4)
- ✅ Data model + responsive/accessible renderer
- ✅ **Vertical slice: complete working Lion page** (`/animal.html?id=lion`)
- ✅ **Dual mode: Modern + Classic 1994** with recreated hotspot navigation
- ✅ **Batch-extracted all 66 animals** (`tools/extract_all.py`)
- ✅ **Liberated text at scale** — 66-animal multi-agent workflow (`tools/gen_workflow.py` → `tools/build_data.py`), Opus consistency pass, validated (`tools/validate_data.py`)
- ✅ **All 66 creatures live** in both modes; fact labels 100% normalized; cross-creature links wired
- ✅ Verified all scientific names; resolved factual flags (crab, python, mosquito, orca) via `tools/corrections.json`
- ✅ Browse modes: **Atlas** (region) + **Weapons** (attack) auto-derived from facts, + **Habitats** (9 environments, curated in `tools/habitats.json`) — 3-tab `browse.html` UI + creature-page chips
- ✅ Wired all 5 cross-link Classic hotspots to Browse categories / creatures (0 disabled remaining)
- ✅ **Guides** — all 12 narrated tours restored (real host narration audio + intro art, `tools/extract_guides.py` → `build_guides.py` → `guides.json`); `guides.html` menu (grouped by host) + tour player; geographic tours list their creatures. **All four original nav modes done: Atlas · Habitats · Weapons · Guides.**
- ✅ **Mini-games** (`games.html`): **Whose Eyes Are These?** (faithful — original close-up/reveal photos, multiple choice, win/lose sounds) + **Survival Quiz** (data-driven, replayable, from `quiz.json`). `tools/extract_games.py` is extensible to the other disc puzzles (Tracks, Camouflage, Close-up, etc.).
- ✅ Refined Classic hotspot coordinates via red-label detection (`tools/refine_hotspots.py` → `hotspots_refined.json`, applied by the build): 347/531 snapped tightly to their labels; the rest keep the vision estimate. (Needs Pillow + numpy.)
- ⬜ More mini-games from the disc (Tracks, Camouflage, …) using the same extractor
- ⬜ Open-licensed media swap for public release

## Legal

Original assets © 1994 Microsoft Corporation and its suppliers (photographers/filmmakers,
e.g. Oxford Scientific Films / Animals Animals). Kept in `_source/` for development only and
never committed. Public release will use only openly-licensed media.
