# `packages/pipeline` — shared disc→site tooling

Code used by **every app's** `tools/` to turn an original CD-ROM into site assets. Extracted
here so it lives once instead of being copy-pasted per app.

| Module | What it provides |
|---|---|
| `szdd.py` | `expand(bytes) -> bytes`, `MAGIC` — decompress Microsoft SZDD/LZSS (`.DIB` screens, some audio) |
| `media.py` | `to_webp(assets_dir)` — PNG→WebP for an app's `web/assets`; `make_posters(assets_dir)` — a `poster.webp` video frame next to each `clip.mp4` |

## How apps use it

Per-app tools add this package to `sys.path` (three levels up from `tools/`) and import:

```python
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "packages", "pipeline"))
from szdd import expand            # or: from media import to_webp, make_posters
```

`tools/convert_to_webp.py` and `tools/make_video_posters.py` in each app are thin wrappers that
call the shared functions against that app's `web/assets`. Needs **Pillow**; `make_posters`
needs **ffmpeg**. Disc-specific logic (`extract_*`, `build_data`) stays in each app's `tools/`.
