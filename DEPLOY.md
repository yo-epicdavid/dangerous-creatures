# Deploying to Cloudflare Pages

This is a plain static site — no build step. The deployable site is the **`web/`** folder
(HTML/CSS/JS + JSON data in `web/data/` + media in `web/assets/`, all committed).

## One-time setup (Cloudflare dashboard)

1. The repo is on GitHub: `github.com/yo-epicdavid/dangerous-creatures`.
2. Cloudflare dashboard → **Workers & Pages** → **Create** → **Pages** → **Connect to Git**.
3. Pick the **dangerous-creatures** repo, branch **main**.
4. Build settings:
   - **Framework preset:** None
   - **Build command:** *(leave empty)*
   - **Build output directory:** `web`
5. **Save and Deploy.** You'll get a `https://dangerous-creatures.pages.dev` URL in ~1 minute.

## Updates

Every `git push` to `main` triggers an automatic redeploy. Nothing else to do.

## Custom domain (optional)

Pages → your project → **Custom domains** → add your domain and follow the DNS steps.

## Regenerating the media from the ISO (only if needed)

The pipeline (mount the ISO at `/Volumes/DANGEROUS` first):

```
python3 tools/extract_all.py        # animals: images -> PNG, audio/video -> MP3/MP4
python3 tools/extract_guides.py     # 12 guided tours
python3 tools/extract_games.py      # mini-game images
<venv>/bin/python tools/convert_to_webp.py   # PNG -> WebP (needs Pillow)
<venv>/bin/python tools/refine_hotspots.py   # tighten Classic hotspots (needs Pillow+numpy)
python3 tools/extract_credits.py    # credits.json from MSDANGER.THE
python3 tools/build_data.py         # web/data/*.json + index/browse/quiz
python3 tools/build_guides.py       # web/data/guides.json
python3 tools/validate_data.py      # sanity check
```
