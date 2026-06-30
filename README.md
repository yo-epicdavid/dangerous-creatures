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
**games and guided tours are bilingual on all three** — authentic Spanish on DC + Oceans (real
Spanish narration, even localized host names like Kim→Carmen), and an AI fan translation on
Dinosaurs (Spanish titles/clues over the original English narration audio, clearly flagged).
The **Making Of** is bilingual on all three too (each edition's article translated to Spanish);
only the credits page is English-only for now.

Each site has a **Modern** view (liberated text, responsive, accessible) and a **Classic** view
that rebuilds the original composite screens 1:1 with working clickable hotspots
(`?mode=classic`). Every edition includes:

- **Browse** along that disc’s own axes — DC by region/habitat/weapon · Oceans by kind/zone/sea ·
  Dinosaurs by kind/period/diet
- **Guided tours** with the original narration — 12 (DC) · 18 (Oceans, 6 character hosts × 3) · 16 (Dinosaurs)
- **A game** — *Whose Eyes Are These?* + *Survival Quiz* (DC) · *Sea Riddles* (Oceans) · *Dino Riddles* (Dinosaurs)
- Restored video, per-entry audio (incl. Dinosaurs’ **“Say it” name pronunciation**), **tap-to-zoom**
  photos (hero + sub-topic images open full-screen in a lightbox), a **Credits** page pulled from the
  disc, and favicon/share art from the title screen. Each edition also has a bilingual **Making-Of**.

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

The discs are preserved on the Internet Archive ([Dangerous Creatures](https://archive.org/details/cdrom_Microsoft_Dangerous_Creatures_-_For_Windows_3.1_Eng),
[Oceans](https://archive.org/details/microsoft-oceans), [Dinosaurs](https://archive.org/details/microsoft-dinosaurs)).
They are the **full retail content** — the “Demonstration” label on a title screen is a built-in
store-kiosk slideshow mode, not a limited edition. ISOs and raw extracts live in `_source/` and are
gitignored — the project links to the Internet Archive rather than re-hosting the discs.

This is a **non-commercial, educational fan preservation** — not affiliated with or endorsed by
Microsoft, no ads/sales/donations, with full attribution and removal on request. The optimized
media **is committed** (so Cloudflare can serve it) and every site links a **Credits** page naming
the original photographers, studios, museums, and agencies (extracted from each disc’s master
`*.THE` database). Credit and good faith — not a copyright license — are the basis for publishing
with the original media.

### Original discs

The source images this build was extracted from, with their Internet Archive items so anyone can
fetch the same disc and confirm it matches. The images themselves stay **gitignored in `_source/`** —
only these links and checksums are committed (the discs are still © Microsoft; the Internet Archive
hosts them, this repo just points there).

| Edition | Disc | Internet Archive | `_source/` file |
|---|---|---|---|
| Dangerous Creatures | English | [`cdrom_Microsoft_Dangerous_Creatures…`](https://archive.org/details/cdrom_Microsoft_Dangerous_Creatures_-_For_Windows_3.1_Eng) | `MSDangerousCreatures.iso` |
| Oceans | English | [`microsoft-oceans`](https://archive.org/details/microsoft-oceans) | `MSOceans.iso` |
| Dinosaurs | English | [`microsoft-dinosaurs`](https://archive.org/details/microsoft-dinosaurs) | `MSDinosaurs.iso` |
| Dangerous Creatures | Spanish · «Animales Peligrosos de Microsoft» | [`MSAnimales`](https://archive.org/details/MSAnimales) | `MS_Animales.bin`+`.cue` → `MS_Animales.iso` |
| Oceans | Spanish · «Océanos de Microsoft» | [`MSOceanos`](https://archive.org/details/MSOceanos) | not retained locally |

The English discs are the `.iso` as downloaded from their items. The Spanish Dangerous Creatures
disc is a raw **BIN/CUE** image (`MODE2/2352`) that the pipeline extracts to `MS_Animales.iso`; the
Spanish Oceans disc was read at extraction time and not kept in `_source/`. **Dinosaurs never shipped
in Spanish** — its `/es/` site is an AI fan translation, so there is no Spanish disc to list.

Verify a fetched image against the exact bytes this build used — save as `_source/SHA256SUMS` and run
`shasum -a 256 -c SHA256SUMS`:

```text
4dcc1178c434e7a151ad7fe15f9db8706de5521fbf92a8c8266354706d76cd00  MSDangerousCreatures.iso
2b53a85f5170f3ab16c4439e7e955bb00992c6e474b559ef66d45d0f3b1ad2f7  MSOceans.iso
b30a1df5b2a4e629df79f8800c5e7633930dcd0fd218db9a90cf45e0dd6678c0  MSDinosaurs.iso
2ecc8bfdbffc2c39a566a1d14fc13fc35942a47e0af5e388377d75e2157bb5d1  MS_Animales.bin
d414f6618fe3d76e5289fbda6407c982b95e2f19b86a7560a21dd4ceca604b7f  MS_Animales.cue
37fc5db286969f9ed674f8e2cf1543994a7efd9454006123bbd7bcc7163c156c  MS_Animales.iso
```
