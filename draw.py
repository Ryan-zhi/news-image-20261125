"""Render one day's news as a single broadsheet-style front page.

Usage:  python3 draw.py <day-module> <output.png>

The day module (day25.py and friends) supplies the words: a kicker, a
dateline, one lead story, four cards and a strip of one-line briefs. This
file owns everything visual -- the page grid, the type, the red tag chips
and the little spot illustrations, all drawn with PIL primitives so the
poster needs no image assets and no network.

Design notes: the page is a 1024x1024 cream sheet. Serif bold carries the
masthead and every headline, a plain sans carries body copy, and the only
colour accents are the chip red and the spot-art palette. Every block of
text is auto-fitted: the font shrinks until the wrapped lines fit their
box, so a long headline can never push copy over a border.
"""

import importlib
import math
import sys

from PIL import Image, ImageDraw, ImageFont

PAGE = 1024
PAPER = (248, 244, 233)
INK = (20, 20, 20)
FADED = (107, 98, 82)
CHIP_RED = (165, 18, 26)
FLAME_CORE = (224, 123, 36)
PANEL_BLUE = (38, 74, 135)

SERIF_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def width_of(draw, text, fnt):
    return draw.textlength(text, font=fnt)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap measured against the real font metrics."""
    lines = []
    current = ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if width_of(draw, trial, fnt) <= max_width:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def fit(draw, text, path, size, max_width, max_lines):
    """Shrink a font until the wrapped text fits the line budget."""
    while size > 10:
        fnt = font(path, size)
        lines = wrap(draw, text, fnt, max_width)
        if len(lines) <= max_lines:
            return fnt, lines
        size -= 1
    fnt = font(path, size)
    return fnt, wrap(draw, text, fnt, max_width)


def spaced(draw, cx, y, text, fnt, tracking, fill):
    """Draw a letter-spaced line centred on cx (for the kicker)."""
    total = sum(width_of(draw, ch, fnt) for ch in text) + tracking * (len(text) - 1)
    x = cx - total / 2
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += width_of(draw, ch, fnt) + tracking


def chip(draw, x, y, label):
    """The red section tag that sits at the top-left of every story."""
    fnt = font(SANS_BOLD, 20)
    w = width_of(draw, label, fnt)
    draw.rectangle([x, y, x + w + 22, y + 32], fill=CHIP_RED)
    draw.text((x + 11, y + 5), label, font=fnt, fill=(255, 255, 255))
    return y + 32


# ---------------------------------------------------------------- spot art
# Each icon draws inside the box (x, y, w, h) it is handed. They are simple
# flat shapes on purpose: at 300px wide the poster must still read clearly.

def icon_flame(d, x, y, w, h):
    outer = [
        (x + 0.52 * w, y),
        (x + 0.64 * w, y + 0.26 * h),
        (x + 0.82 * w, y + 0.52 * h),
        (x + 0.78 * w, y + 0.85 * h),
        (x + 0.68 * w, y + h),
        (x + 0.32 * w, y + h),
        (x + 0.22 * w, y + 0.84 * h),
        (x + 0.18 * w, y + 0.52 * h),
        (x + 0.33 * w, y + 0.30 * h),
    ]
    d.polygon(outer, fill=CHIP_RED)
    inner = [
        (x + 0.52 * w, y + 0.38 * h),
        (x + 0.63 * w, y + 0.60 * h),
        (x + 0.62 * w, y + 0.88 * h),
        (x + 0.56 * w, y + h),
        (x + 0.42 * w, y + h),
        (x + 0.38 * w, y + 0.86 * h),
        (x + 0.40 * w, y + 0.58 * h),
    ]
    d.polygon(inner, fill=FLAME_CORE)
    d.rectangle([x - 0.28 * w, y + h + 10, x + 1.05 * w, y + h + 18], fill=INK)


def icon_station(d, x, y, w, h):
    mid_y = y + 0.52 * h
    # solar wings, two blue panels either side of the hull
    for px in (x, x + 0.70 * w):
        d.rectangle([px, mid_y - 0.20 * h, px + 0.30 * w, mid_y + 0.20 * h], fill=PANEL_BLUE)
        d.line([px + 0.15 * w, mid_y - 0.20 * h, px + 0.15 * w, mid_y + 0.20 * h], fill=PAPER, width=3)
    d.rectangle([x + 0.40 * w, mid_y - 0.26 * h, x + 0.60 * w, mid_y + 0.26 * h], fill=INK)
    d.rectangle([x + 0.46 * w, mid_y - 0.14 * h, x + 0.54 * w, mid_y + 0.14 * h], fill=PAPER)
    # the red arc of the orbit passing overhead
    d.arc([x + 0.05 * w, y - 0.15 * h, x + 0.95 * w, y + 0.75 * h], start=180, end=360, fill=CHIP_RED, width=6)
    d.ellipse([x + 0.46 * w, y - 0.02 * h, x + 0.54 * w, y + 0.10 * h], fill=CHIP_RED)


def icon_capitol(d, x, y, w, h):
    cx = x + 0.5 * w
    d.line([cx, y, cx, y + 0.10 * h], fill=INK, width=5)
    d.polygon(
        [(cx, y + 0.08 * h), (x + 0.80 * w, y + 0.52 * h), (x + 0.20 * w, y + 0.52 * h)],
        fill=INK,
    )
    d.rectangle([x + 0.28 * w, y + 0.58 * h, x + 0.72 * w, y + 0.78 * h], fill=INK)
    d.rectangle([x + 0.10 * w, y + 0.84 * h, x + 0.90 * w, y + 0.97 * h], fill=CHIP_RED)


def icon_globe(d, x, y, w, h):
    d.ellipse([x, y, x + w, y + h], outline=INK, width=6)
    # meridians: two ellipses pinched through the middle of the sphere
    for frac in (0.22, 0.36):
        inset = w * frac
        d.ellipse([x + inset, y, x + w - inset, y + h], outline=INK, width=4)
    d.line([x + 0.5 * w, y, x + 0.5 * w, y + h], fill=INK, width=4)
    # parallels, drawn as chords so they stay inside the circle
    for frac, half in ((0.30, 0.44), (0.50, 0.50), (0.70, 0.44)):
        yy = y + frac * h
        d.line([x + (0.5 - half) * w, yy, x + (0.5 + half) * w, yy], fill=INK, width=4)
    # a market thermometer riding the right-hand edge
    tx = x + 0.78 * w
    d.rounded_rectangle([tx, y + 0.08 * h, tx + 0.13 * w, y + 0.78 * h], radius=8, fill=CHIP_RED)
    d.ellipse([tx - 0.05 * w, y + 0.68 * h, tx + 0.18 * w, y + 0.95 * h], fill=CHIP_RED)


def icon_ship(d, x, y, w, h):
    hull = [
        (x, y + 0.38 * h),
        (x + w, y + 0.38 * h),
        (x + 0.84 * w, y + 0.66 * h),
        (x + 0.14 * w, y + 0.66 * h),
    ]
    d.polygon(hull, fill=INK)
    d.rectangle([x + 0.16 * w, y + 0.20 * h, x + 0.44 * w, y + 0.38 * h], fill=INK)
    d.rectangle([x + 0.56 * w, y + 0.12 * h, x + 0.70 * w, y + 0.38 * h], fill=CHIP_RED)
    # two gentle rows of waves under the hull
    for row, yy in enumerate((0.80, 0.92)):
        pts = []
        for i in range(17):
            px = x + (i / 16) * w
            py = y + yy * h + 5 * math.sin(i * 1.1 + row * 2.0)
            pts.append((px, py))
        d.line(pts, fill=INK, width=4)


ICONS = {
    "flame": icon_flame,
    "station": icon_station,
    "capitol": icon_capitol,
    "globe": icon_globe,
    "ship": icon_ship,
}


# ------------------------------------------------------------------- page

def masthead(d, day):
    spaced(d, PAGE / 2, 38, day.KICKER, font(SANS_BOLD, 26), 7, FADED)
    size = 58
    while width_of(d, day.DATELINE, font(SERIF_BOLD, size)) > 940 and size > 20:
        size -= 2
    fnt = font(SERIF_BOLD, size)
    w = width_of(d, day.DATELINE, fnt)
    d.text(((PAGE - w) / 2, 74), day.DATELINE, font=fnt, fill=INK)
    d.rectangle([36, 146, 988, 151], fill=INK)
    d.line([36, 157, 988, 157], fill=INK, width=2)


def lead_box(d, story):
    d.rectangle([36, 176, 988, 472], outline=INK, width=2)
    chip(d, 58, 196, story["tag"])
    ICONS[story["icon"]](d, 118, 238, 165, 190)
    title_fnt, title_lines = fit(d, story["title"], SERIF_BOLD, 50, 628, 3)
    y = 200
    for line in title_lines:
        d.text((330, y), line, font=title_fnt, fill=INK)
        y += 58
    body_fnt, body_lines = fit(d, story["body"], SANS, 25, 628, 4)
    y += 12
    for line in body_lines:
        d.text((330, y), line, font=body_fnt, fill=INK)
        y += 34


def card(d, x, y, story):
    w, h = 464, 216
    d.rectangle([x, y, x + w, y + h], outline=INK, width=2)
    chip(d, x + 18, y + 16, story["tag"])
    ICONS[story["icon"]](d, x + 22, y + 58, 104, 82)
    title_fnt, title_lines = fit(d, story["title"], SERIF_BOLD, 30, w - 158, 3)
    ty = y + 54
    for line in title_lines:
        d.text((x + 142, ty), line, font=title_fnt, fill=INK)
        ty += 35
    body_fnt, body_lines = fit(d, story["body"], SANS, 21, w - 36, 2)
    by = y + 160
    for line in body_lines:
        d.text((x + 18, by), line, font=body_fnt, fill=INK)
        by += 26


def strip(d, items):
    d.rectangle([36, 950, 988, 953], fill=INK)
    d.line([36, 958, 988, 958], fill=INK, width=1)
    d.text((36, 966), "ALSO TODAY:", font=font(SANS_BOLD, 20), fill=CHIP_RED)
    body_fnt, lines = fit(d, "  ·  ".join(items), SANS, 20, 788, 2)
    y = 966
    for line in lines:
        d.text((200, y), line, font=body_fnt, fill=INK)
        y += 24


def render(day, out_path):
    img = Image.new("RGB", (PAGE, PAGE), PAPER)
    d = ImageDraw.Draw(img)
    masthead(d, day)
    lead_box(d, day.LEAD)
    positions = [(36, 492), (524, 492), (36, 726), (524, 726)]
    for (x, y), story in zip(positions, day.CARDS):
        card(d, x, y, story)
    strip(d, day.STRIP)
    img.save(out_path)
    return out_path


if __name__ == "__main__":
    module = importlib.import_module(sys.argv[1])
    print(render(module, sys.argv[2]))
