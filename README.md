# Microsoft Home: Exploration Series — reborn

Modern, accessible, web-native recreations of three 1990s **Microsoft Home “Exploration
Series”** edutainment CD-ROMs — so any kid can explore them again in a browser.

This repo began as a single rebuild of *Microsoft Dangerous Creatures (1994)* and grew into a
**pnpm monorepo** housing three complete “museum editions,” plus a from-scratch reinterpretation
in progress.

## The editions

| Edition | Disc | Entries | Languages | Live |
|---|---|---|---|---|
| **Dangerous Creatures** | 1994 | 66 animals | EN · ES | https://dangerous-creatures.pages.dev |
| **Oceans** | 1995 | 93 (sea life, habitats, ocean science, seas & people) | EN · ES | https://oceans-2s9.pages.dev |
| **Dinosaurs** | 1993 | 166 (69 dinosaurs, 28 prehistoric creatures, 69 concepts) | EN · ES&nbsp;* | https://dinosaurs.pages.dev |

All three are **bilingual** — English at `/`, Castilian Spanish under `/es/`, with an EN·ES switcher.
Dangerous Creatures and Oceans are **authentic** Spanish editions, liberated from the *real Spanish
retail discs* («Animales Peligrosos de Microsoft», «Océanos de Microsoft») — Spanish text **and**
Spanish screens/audio/video. **\* Dinosaurs never shipped in Spanish** (only EN/FR/JA), so its `/es/`
is a clearly-labeled **AI fan translation** of the English text; the media stays English. The
**games are bilingual on DC + Oceans** (authentic Spanish); guides, credits and the making-of are
English-only for now.

Each site has a **Modern** view (liberated text, responsive, accessible) and a **Classic** view
that rebuilds the original composite screens 1:1 with working clickable hotspots
(`?mode=classic`). Every edition includes:

- **Browse** along that disc’s own axes — DC by region/habitat/weapon · Oceans by kind/zone/sea ·
  Dinosaurs by kind/period/diet
- **Guided tours** with the original narration — 12 (DC) · 18 (Oceans, 6 character hosts × 3) · 16 (Dinosaurs)
- **A game** — *Whose Eyes Are These?* + *Survival Quiz* (DC) · *Sea Riddles* (Oceans) · *Dino Riddles* (Dinosaurs)
- Restored video, per-entry audio (incl. Dinosaurs’ **“Say it” name pronunciation**), a **Credits**
  page pulled from the disc, and favicon/share art from the title screen. Dinosaurs also has a **Making-Of**.

## How it works — the shared pipeline

The original discs store every screen as a *pre-composited bitmap* (photo + body text + hotspot
labels painted into one image). Each app’s `tools/` turns a disc into a site:

1. **Extract** the original media losslessly — images (SZDD-compressed `.DIB`, or raw BMP on the
   1993 disc) → **WebP**, `.AVI` (Microsoft Video 1) → **MP4**, `.WAV` → **MP3**.
2. **Liberate the baked-in text** with a **multi-agent AI workflow** (Claude Code: Sonnet vision
   OCR → adversarial verify → Opus cross-entry consistency) into structured per-entry JSON.
3. **`build_data`** emits `web/data/*.json` + browse/index; **`build_guides`**, **`extract_credits`**,
   **`make_icons`** handle the rest.
4. **Astro** builds a static site — Modern pre-rendered (SSG), Classic as a client island off the same data.

## Layout

```
apps/
  dangerous-creatures/                # museum edition — 1994
  oceans/                             # museum edition — 1995
  dinosaurs/                          # museum edition — 1993
  dangerous-creatures-reimagined/     # WIP (see the `reimagined` branch)
packages/
  pipeline/                          # shared disc→site Python tooling (szdd, PNG→WebP, video posters)
  site-kit/                          # shared CSS base + design tokens (base.css)
_source/                             # raw ISOs + extracted originals — GITIGNORED
DEPLOY.md                            # Cloudflare Pages setup for every app
pnpm-workspace.yaml
```

Each app holds `src/` (Astro components/pages), `web/` (`data/` JSON + committed `assets/` media +
`styles.css`), `tools/` (the Python pipeline), and `public/` (icons).

Code shared across editions lives in **`packages/`**: **`pipeline/`** holds the media steps that
were identical in every app (SZDD/LZSS decompress, PNG→WebP, video-frame posters) — each app's
`tools/convert_to_webp.py` / `make_video_posters.py` is now a thin wrapper, and the `extract_*`
tools import `szdd` from here. **`site-kit/base.css`** holds the common component styles (topbar,
buttons, hero, fact card, topics, classic-1994 mode, hotspots, grids, chips, audio buttons); each
app's `web/styles.css` is just its theme `:root` tokens, imported after `base.css` in `Layout.astro`.
So a cross-cutting style or pipeline change is one edit, themed per app via tokens.

A separate **`reimagined` branch** explores a from-scratch interactive rebuild of Dangerous
Creatures with all-new, openly-licensed assets (`apps/dangerous-creatures-reimagined/`,
`REIMAGINED.md`). It’s a planning/spike stage, not yet built.

## Develop & build

Runtimes via **mise**; package manager is **pnpm** (pinned in `package.json`).

```bash
pnpm install
pnpm dc:dev          # dev server (also: oceans:dev, dino:dev)
pnpm dc:build        # build one app (also: oceans:build, dino:build)
pnpm build           # build all apps
```

Each app’s `build` runs `astro build` and copies its committed `web/assets` + `web/data` into
`dist/`. Media is already optimized and committed — no asset step runs in CI.

## Deploy

One **Cloudflare Pages** project per app (build command `pnpm install && pnpm run <app>:build`,
output `apps/<app>/dist`). Full settings — including the pnpm version notes and per-app
regeneration steps — are in **[`DEPLOY.md`](./DEPLOY.md)**.

## Source & provenance

The discs are preserved on the Internet Archive (Dangerous Creatures, [Oceans](https://archive.org/details/microsoft-oceans),
[Dinosaurs](https://archive.org/details/microsoft-dinosaurs)). They are the **full retail
content** — the “Demonstration” label on a title screen is a built-in store-kiosk slideshow mode,
not a limited edition. ISOs and raw extracts live in `_source/` and are gitignored.

This is a **non-commercial, educational fan preservation** — not affiliated with or endorsed by
Microsoft, no ads/sales/donations, with full attribution and removal on request. The optimized
media **is committed** (so Cloudflare can serve it) and every site links a **Credits** page naming
the original photographers, studios, museums, and agencies (extracted from each disc’s master
`*.THE` database). Credit and good faith — not a copyright license — are the basis for publishing
with the original media.
