#!/usr/bin/env python3
"""Generate a 1200x630 social-share (Open Graph) image for each animal so a shared link
shows that animal. Design: the original 1994 screen framed on a blurred, darkened backdrop
of itself, with the "Dangerous Creatures" wordmark + the animal's name on the left.
-> web/assets/<slug>/og.jpg  (JPEG, for WhatsApp/Facebook/Twitter compatibility).

Run with the project venv python (needs Pillow). Set OG_ONLY=lion[,gwsh] for a preview.
"""
import os, glob, json
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.abspath(os.path.join(HERE, "..", "web"))
LOCALE = os.environ.get("LOCALE", "")          # "" = English, "es" = Castilian
DATA = os.path.join(WEB, "data", "es") if LOCALE == "es" else os.path.join(WEB, "data")
ASSETS = os.path.join(WEB, "assets")
WORDMARK = "ANIMALES PELIGROSOS" if LOCALE == "es" else "DANGEROUS CREATURES"
ONLY = [s.strip() for s in os.environ.get("OG_ONLY", "").split(",") if s.strip()]

W, H = 1200, 630
# Dangerous Creatures palette
INK = (244, 236, 224)
INK_SOFT = (205, 191, 169)
GOLD = (232, 163, 61)

F_DISPLAY = "/System/Library/Fonts/Supplemental/Papyrus.ttc"   # site hero font
F_SANS = "/System/Library/Fonts/Avenir Next.ttc"               # body font
SANS_BOLD, SANS_ITALIC = 0, 4                                  # .ttc indices


def font(path, size, index=0):
    return ImageFont.truetype(path, size, index=index)


def cover(img, w, h):
    s = max(w / img.width, h / img.height)
    r = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    x, y = (r.width - w) // 2, (r.height - h) // 2
    return r.crop((x, y, x + w, y + h))


def fit_height(img, h):
    return img.resize((round(img.width * h / img.height), h), Image.LANCZOS)


def wrap(draw, text, f, maxw):
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


def fit_name(draw, text, maxw, start=96, lo=46):
    """Largest Papyrus size (<=2 lines) that fits maxw."""
    size = start
    while size >= lo:
        f = font(F_DISPLAY, size)
        if len(wrap(draw, text, f, maxw)) <= 2 and all(draw.textlength(l, font=f) <= maxw for l in wrap(draw, text, f, maxw)):
            return f, wrap(draw, text, f, maxw)
        size -= 3
    f = font(F_DISPLAY, lo)
    return f, wrap(draw, text, f, maxw)


def tracked(draw, xy, text, f, fill, spacing=6):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=f, fill=fill)
        x += draw.textlength(ch, font=f) + spacing


def make(slug, d):
    src = Image.open(os.path.join(WEB, d["hero"]["image"])).convert("RGB")

    # backdrop: blurred + darkened cover of the screen itself
    card = Image.blend(cover(src, W, H).filter(ImageFilter.GaussianBlur(22)),
                       Image.new("RGB", (W, H), (12, 10, 8)), 0.58)

    # right: the framed screen
    screen = fit_height(src, 452)
    sx, sy = W - 46 - screen.width, (H - screen.height) // 2

    # left gradient scrim so the name stays legible over the backdrop
    scrim = Image.new("L", (W, H), 0)
    sd = ImageDraw.Draw(scrim)
    for x in range(sx):
        sd.line([(x, 0), (x, H)], fill=int(205 * (1 - x / sx)))
    card = Image.composite(Image.new("RGB", (W, H), (8, 7, 5)), card, scrim)

    # screen shadow
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rectangle([sx - 8, sy - 8, sx + screen.width + 8, sy + screen.height + 8], fill=(0, 0, 0, 170))
    card = Image.alpha_composite(card.convert("RGBA"), sh.filter(ImageFilter.GaussianBlur(18))).convert("RGB")

    draw = ImageDraw.Draw(card)
    draw.rectangle([sx - 3, sy - 3, sx + screen.width + 2, sy + screen.height + 2], outline=GOLD, width=3)
    card.paste(screen, (sx, sy))

    # left text block, vertically centered
    lx, lmax = 66, sx - 44 - 66
    kf = font(F_SANS, 25, SANS_BOLD)
    nfont, lines = fit_name(draw, d["name"], lmax)
    sci = d.get("scientificName", "")
    sff = font(F_SANS, 29, SANS_ITALIC)
    block = 25 + 22 + sum(nfont.size + 8 for _ in lines) + (16 + 29 if sci else 0)
    y = max(70, (H - block) // 2)
    tracked(draw, (lx, y), WORDMARK, kf, GOLD, spacing=5)
    y += 25 + 22
    for ln in lines:
        draw.text((lx, y), ln, font=nfont, fill=INK)
        y += nfont.size + 8
    if sci:
        draw.text((lx, y + 8), sci, font=sff, fill=INK_SOFT)

    out = os.path.join(os.path.dirname(os.path.join(WEB, d["hero"]["image"])), "og.jpg")
    card.save(out, "JPEG", quality=88)
    return out


def main():
    n = 0
    for f in sorted(glob.glob(os.path.join(DATA, "*.json"))):
        if os.path.basename(f) in ("index.json", "browse.json", "quiz.json", "credits.json", "games_eyes.json"):
            continue
        d = json.load(open(f))
        if not (isinstance(d, dict) and d.get("id") and d.get("hero", {}).get("image")):
            continue
        if ONLY and d["id"] not in ONLY:
            continue
        make(d["id"], d)
        n += 1
    print(f"wrote {n} OG images -> web/assets/*/og.jpg")


if __name__ == "__main__":
    main()
