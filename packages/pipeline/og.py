#!/usr/bin/env python3
"""Shared Open Graph share-card renderer for the museum editions.

Each app's tools/make_og_images.py is a thin wrapper passing its palette, wordmark, and a
subtitle rule. The card is a 1200x630 JPEG: the original screen framed on a blurred backdrop
of itself, with the edition wordmark + the entry's name (Papyrus) + a subtitle. Output is
og.jpg written next to each entry's hero image (so locale subdirs like assets/es/ are handled
automatically). Needs Pillow.
"""
import os
import glob
import json
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1200, 630
F_DISPLAY = "/System/Library/Fonts/Supplemental/Papyrus.ttc"   # matches the site hero font
F_SANS = "/System/Library/Fonts/Avenir Next.ttc"               # body font
SANS_BOLD, SANS_ITALIC = 0, 4                                  # .ttc face indices
DEFAULT_SKIP = {"index.json", "browse.json", "quiz.json", "credits.json", "games_eyes.json", "guides.json"}


def _font(path, size, index=0):
    return ImageFont.truetype(path, size, index=index)


def _cover(img, w, h):
    s = max(w / img.width, h / img.height)
    r = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    x, y = (r.width - w) // 2, (r.height - h) // 2
    return r.crop((x, y, x + w, y + h))


def _fit_height(img, h):
    return img.resize((round(img.width * h / img.height), h), Image.LANCZOS)


def _wrap(draw, text, f, maxw):
    out, cur = [], ""
    for word in text.split():
        t = (cur + " " + word).strip()
        if draw.textlength(t, font=f) <= maxw:
            cur = t
        else:
            if cur:
                out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def _fit_name(draw, text, maxw, start=96, lo=46):
    """Largest Papyrus size (<=2 lines) that fits maxw."""
    size = start
    while size >= lo:
        f = _font(F_DISPLAY, size)
        lines = _wrap(draw, text, f, maxw)
        if len(lines) <= 2 and all(draw.textlength(l, font=f) <= maxw for l in lines):
            return f, lines
        size -= 3
    f = _font(F_DISPLAY, lo)
    return f, _wrap(draw, text, f, maxw)


def _tracked(draw, xy, text, f, fill, spacing=5):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=f, fill=fill)
        x += draw.textlength(ch, font=f) + spacing


def render_card(web, hero_rel, name, subtitle, wordmark, palette, out):
    ink, ink_soft, gold = palette["ink"], palette["ink_soft"], palette["gold"]
    dark, scrim = palette["dark"], palette["scrim"]
    src = Image.open(os.path.join(web, hero_rel)).convert("RGB")

    # backdrop: blurred + darkened cover of the screen itself
    card = Image.blend(_cover(src, W, H).filter(ImageFilter.GaussianBlur(22)),
                       Image.new("RGB", (W, H), dark), 0.58)

    # the framed screen (right)
    screen = _fit_height(src, 452)
    sx, sy = W - 46 - screen.width, (H - screen.height) // 2

    # left gradient scrim so the name stays legible over the backdrop
    mask = Image.new("L", (W, H), 0)
    md = ImageDraw.Draw(mask)
    for x in range(sx):
        md.line([(x, 0), (x, H)], fill=int(205 * (1 - x / sx)))
    card = Image.composite(Image.new("RGB", (W, H), scrim), card, mask)

    # screen shadow
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rectangle([sx - 8, sy - 8, sx + screen.width + 8, sy + screen.height + 8], fill=(0, 0, 0, 170))
    card = Image.alpha_composite(card.convert("RGBA"), sh.filter(ImageFilter.GaussianBlur(18))).convert("RGB")

    draw = ImageDraw.Draw(card)
    draw.rectangle([sx - 3, sy - 3, sx + screen.width + 2, sy + screen.height + 2], outline=gold, width=3)
    card.paste(screen, (sx, sy))

    # left text block, vertically centered
    lx, lmax = 66, sx - 44 - 66
    # fit the tracked wordmark within the left panel (long localized wordmarks need shrinking)
    ksize = 25
    while ksize > 15 and (sum(draw.textlength(ch, font=_font(F_SANS, ksize, SANS_BOLD)) for ch in wordmark) + 5 * (len(wordmark) - 1)) > lmax:
        ksize -= 1
    kf = _font(F_SANS, ksize, SANS_BOLD)
    nfont, lines = _fit_name(draw, name, lmax)
    sub = (subtitle or "").strip()
    subsize = 29
    while sub and subsize > 20 and draw.textlength(sub, font=_font(F_SANS, subsize, SANS_ITALIC)) > lmax:
        subsize -= 1
    sff = _font(F_SANS, subsize, SANS_ITALIC)
    block = 25 + 22 + sum(nfont.size + 8 for _ in lines) + (16 + subsize if sub else 0)
    y = max(70, (H - block) // 2)
    _tracked(draw, (lx, y), wordmark, kf, gold, spacing=5)
    y += 25 + 22
    for ln in lines:
        draw.text((lx, y), ln, font=nfont, fill=ink)
        y += nfont.size + 8
    if sub:
        draw.text((lx, y + 8), sub, font=sff, fill=ink_soft)

    card.save(out, "JPEG", quality=88)
    return out


def make_all(web, data_dir, wordmark, palette, subtitle_fn, only=None, skip=DEFAULT_SKIP, out_name="og.jpg"):
    """Render og.jpg for every entry under data_dir (skips index/browse/quiz/etc.).
    out_name lets a fan-translation locale write og-es.jpg next to the shared English media."""
    only = only or []
    n = 0
    for f in sorted(glob.glob(os.path.join(data_dir, "*.json"))):
        if os.path.basename(f) in skip:
            continue
        d = json.load(open(f))
        if not (isinstance(d, dict) and d.get("id") and (d.get("hero") or {}).get("image")):
            continue
        if only and d["id"] not in only:
            continue
        out = os.path.join(os.path.dirname(os.path.join(web, d["hero"]["image"])), out_name)
        render_card(web, d["hero"]["image"], d["name"], subtitle_fn(d), wordmark, palette, out)
        n += 1
    print(f"wrote {n} OG images -> {data_dir}")
    return n
