# ms-exploration-archive — project guide

Modern, accessible web recreations of three 1990s **Microsoft Home "Exploration Series"** CD-ROMs.
A **pnpm monorepo**. Each app turns one original disc into a static Astro site with a **Modern**
view (liberated text) and a **Classic** view that rebuilds the original screens 1:1 with working
hotspots (`?mode=classic`).

## Layout

```
apps/
  dangerous-creatures/   # 1994 · 66 animals · bilingual EN/ES (authentic Spanish disc)
  oceans/                # 1995 · 93 entries · bilingual EN/ES (authentic Spanish disc)
  dinosaurs/             # 1993 · 166 entries · bilingual EN/ES (ES = AI fan translation; no Spanish disc)
  dangerous-creatures-reimagined/  # WIP spike (see `reimagined` branch)
packages/
  pipeline/              # shared disc→site Python tooling (see below)
  site-kit/base.css      # shared CSS component skeleton; themed per app via :root tokens
```
Each app: `src/` (Astro), `web/` (`data/*.json` + committed `assets/` media + `styles.css`),
`tools/` (per-disc Python pipeline), `public/` (icons).

## The pipeline (per app, in `tools/`)

1. **Extract** original media: SZDD `.DIB` (or raw BMP on the 1993 disc) → WebP, `.AVI` → MP4, `.WAV` → MP3.
2. **Liberate** the baked-in screen text with a multi-agent workflow (Sonnet vision OCR → adversarial
   verify → Opus consistency) → structured per-entry JSON.
3. **`build_data.py`** → `web/data/*.json` + browse/index; plus `build_guides`, `extract_credits`, `make_icons`.
4. **Astro** builds a static site; Classic mode is a client island off the same data.

Run tools with the project venv (needs Pillow); ffmpeg at `/opt/homebrew/bin/ffmpeg`. Discs mount
under `/Volumes/...`; raw extracts/ISOs live in gitignored `_source/`.

## Shared code — edit once

- **`packages/pipeline/`**: `szdd.py` (SZDD/LZSS decompress) + `media.py` (`to_webp`, `make_posters`).
  Each app's `convert_to_webp.py` / `make_video_posters.py` is a thin wrapper; `extract_*` import
  `szdd` from here via a `sys.path` insert. Offline only — no effect on built sites.
- **`packages/site-kit/base.css`**: the component skeleton shared by all editions. Each app's
  `web/styles.css` is **just its theme `:root` tokens**; `Layout.astro` imports `base.css` **before**
  it. Per-app page background/chrome are tokens (`--body-bg`, `--body-attach`, `--topbar-bg`).
  Change shared look-and-feel in `base.css`; theme per app via tokens. Don't re-duplicate styles.

## i18n — all three editions are bilingual

Astro i18n, `prefixDefaultLocale:false` (en at `/`, es under `/es/`). Each app: page bodies in shared
view components (`HomeView`/`AnimalView`(DC)/`TopicView`(Oceans)/`DinoView`(Dino)/`BrowseView`) with
thin per-locale route wrappers; UI strings in `src/i18n/ui.js`; EN·ES switcher; `build_data_es.py`
overlays Spanish text on the English structure. Two flavors:

- **Authentic (DC, Oceans):** liberated from the *real Spanish discs*. Spanish media lives in
  `web/data/es/` + `web/assets/es/`; `build_data_es` relocates asset paths to `assets/es/`.
- **Fan translation (Dinosaurs):** no Spanish disc exists, so the ES text is an AI translation
  (`gen_workflow_es.py` is a translator, not an OCR liberator). It **reuses the English media** —
  `build_data_es` does NOT relocate assets; pages carry a `fanTranslation` flag + a visible
  `.fan-note` banner; OG cards are `og-es.jpg` next to the shared English assets. **Never present it
  as official.** If a real Spanish Dinosaurs disc ever surfaces, redo it as an authentic edition.

ES coverage: home + entry pages + browse + **games + guided tours** on all three. DC + Oceans are
authentic (from the Spanish discs); **Dinosaurs games/guides are an AI fan translation** — Spanish
text over the original English narration audio, with `.fan-note` banners (no Spanish disc). Games:
`GamesView` per locale + `build_games_es.py` (DC); Dino *Dino Riddles* is data-driven, so its
`GamesView` just reads the es entry pool — no extra build step. Guides on DC + Oceans:
`extract_guides.py` (locale-aware, `DISC`+`LOCALE`) pulls the real Spanish narration + intro art; a
small OCR pass reads the Spanish titles/host names off the screens (Oceans even renames hosts,
Kim→Carmen) into `guides_meta_es.json`/`guides_ocr_es.json`. Dino guides are flat (16 tours, no
hosts): `guides_meta_es.json` is an AI translation of the titles/blurbs and `build_guides_es.py`
reuses the English narration paths verbatim. All three: `build_guides_es.py` assembles
`web/data/es/guides.json` and `GuideIndexView`/`GuideView` render per locale. Credits and making-of
stay English-only for now.

## Build & deploy

```bash
pnpm install
pnpm dc:dev            # also oceans:dev, dino:dev
pnpm dc:build          # also oceans:build, dino:build;  pnpm build = all
```
Each `build` runs `astro build` and copies committed `web/assets` + `web/data` into `dist/` (media
is pre-optimized & committed — no asset step in CI). Deploy: one **Cloudflare Pages** project per
app (build `pnpm install && pnpm run <app>:build`, output `apps/<app>/dist`, `PNPM_VERSION=11.9.0`).
`main` auto-deploys.

## Conventions

- Keep the **English site byte-identical** when adding locales/editions; verify with a build + grep.
- Verify every change with a build; for CSS refactors confirm no selector is dropped.
- **Git auth:** SSH when at the Mac; when on a **remote session** the SSH agent is unreachable —
  switch the remote to HTTPS+PAT and use `env -u GITHUB_TOKEN gh ...` (full-scope keyring token) for
  PR create/merge. Real gh at `/opt/homebrew/bin/gh`. Work via branch → PR → merge.
- Non-commercial educational preservation; ship with original media + per-disc Credits page.
