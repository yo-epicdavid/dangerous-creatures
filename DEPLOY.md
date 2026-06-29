# Deploying the monorepo to Cloudflare Pages

This repo is a **pnpm monorepo** with one Cloudflare Pages project per app:

| App | Package | Lives in | Output |
|-----|---------|----------|--------|
| Dangerous Creatures | `dangerous-creatures` | `apps/dangerous-creatures/` | `apps/dangerous-creatures/dist` |
| Oceans | `oceans` | `apps/oceans/` | `apps/oceans/dist` |

Both are static Astro sites. Each app's `build` script runs `astro build` and copies its
committed `web/assets` (media) + `web/data` (JSON) into `dist/`.

---

## ⚠️ Read this before merging `oceans` → `main`

The live Dangerous Creatures site currently deploys from `main`, where DC sits at the **repo
root** (build command `npm run build`, output `dist`). Merging `oceans` moves DC into
`apps/dangerous-creatures/` and makes the root a pnpm workspace. **The existing DC Pages
project will fail its next build until you update its settings** (below). Safe order:

1. Update the **Dangerous Creatures** Pages project settings (don't deploy yet).
2. Merge `oceans` → `main`.
3. Let the DC project redeploy with the new settings; verify the live site.
4. Create the **Oceans** Pages project.

Cloudflare won't replace a live deployment with a failed build, so a misconfigured build is
recoverable — but updating settings first avoids a red build entirely.

---

## Dangerous Creatures project (UPDATE on merge)

Cloudflare dashboard → the existing **dangerous-creatures** Pages project → **Settings → Build**:

- **Production branch:** `main`
- **Framework preset:** None
- **Build command:** `pnpm install && pnpm run dc:build`
- **Build output directory:** `apps/dangerous-creatures/dist`
- **Root directory:** `/` (leave at repo root — the pnpm workspace resolves from there)

## Oceans project (NEW)

**Workers & Pages → Create → Pages → Connect to Git** → same repo:

- **Production branch:** `main` (or deploy from the `oceans` branch first to preview)
- **Project name:** `oceans` → gives `https://oceans.pages.dev`
- **Framework preset:** None
- **Build command:** `pnpm install && pnpm run oceans:build`
- **Build output directory:** `apps/oceans/dist`
- **Root directory:** `/`

---

## pnpm version (important)

The workspace uses pnpm 11 syntax (`allowBuilds:` in `pnpm-workspace.yaml`, which approves the
native `esbuild`/`sharp` postinstall scripts Astro needs). The root `package.json` pins
`"packageManager": "pnpm@11.9.0"` so Cloudflare's corepack uses a matching pnpm. If a build
errors on an ignored/!unknown build script, set a Pages **environment variable**
`PNPM_VERSION = 11.9.0` (and `NODE_VERSION = 20` or newer).

## Updates

Every push to `main` redeploys both projects (each only rebuilds from its own output dir).
The committed `web/assets` media is what gets served — no asset step runs in CI.

---

## Regenerating Oceans from the ISO (only if needed)

Mount the disc at `/Volumes/MS_OCEANS` (`hdiutil attach _source/MSOceans.iso`), then from
`apps/oceans/`:

```
python3 tools/extract_all.py                     # images -> PNG, audio -> MP3, video -> MP4
WF_OUT=tools/wf_full.js python3 tools/gen_workflow.py   # build the liberation workflow
#   run tools/wf_full.js with the Workflow tool, save its result to web/wf_result.json
python3 tools/build_data.py                      # web/data/*.json + index/browse
<venv>/bin/python tools/extract_guides.py        # 6 hosts x 3 narrated tours
python3 tools/build_guides.py                    # web/data/guides.json
<venv>/bin/python tools/make_video_posters.py    # real video-frame posters
<venv>/bin/python tools/convert_to_webp.py       # PNG -> WebP (deletes PNGs; run LAST)
```
