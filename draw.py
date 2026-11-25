# Poster renderer for the make.fun news-image contests: draws a one-page
# "world news of the day" broadsheet (1024x1024 PNG) with PIL — a date
# banner, one lead story with an illustration, a grid of story cards with
# simple editorial icons, and an "also today" ticker strip. Story data
# lives in dayNN.py files next to this script; every headline and summary
# is written from that day's wire reports, and the PNG is checked by eye
# before it is submitted.

import sys
from PIL import Image, ImageDraw, ImageFont

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

PAPER = (247, 243, 234)
INK = (17, 17, 20)
RED = (168, 18, 32)
GRAY = (92, 88, 80)
CARD = (255, 253, 248)
LINE = (40, 38, 34)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, xy, text, fnt, fill, width, leading=1.12, max_lines=None):
    x, y = xy
    lines = wrap(draw, text, fnt, width)
    if max_lines:
        lines = lines[:max_lines]
    h = int(fnt.size * leading)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += h
    return y


# --- icons: each draws inside box (x0, y0, x1, y1) in INK with RED accents ---

def icon_chip(d, b):
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    for i in range(5):
        t = x0 + w * (0.18 + 0.16 * i)
        d.line([t, y0, t, y0 + h * 0.16], fill=INK, width=7)
        d.line([t, y1 - h * 0.16, t, y1], fill=INK, width=7)
        d.line([x0, y0 + h * (0.18 + 0.16 * i), x0 + w * 0.16, y0 + h * (0.18 + 0.16 * i)], fill=INK, width=7)
        d.line([x1 - w * 0.16, y0 + h * (0.18 + 0.16 * i), x1, y0 + h * (0.18 + 0.16 * i)], fill=INK, width=7)
    d.rectangle([x0 + w * 0.16, y0 + h * 0.16, x1 - w * 0.16, y1 - h * 0.16], outline=INK, width=9)
    d.rectangle([x0 + w * 0.36, y0 + h * 0.36, x1 - w * 0.36, y1 - h * 0.36], fill=RED)


def icon_globe(d, b):
    x0, y0, x1, y1 = b
    cx, cy, r = (x0 + x1) // 2, (y0 + y1) // 2, (x1 - x0) // 2 - 4
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=8)
    d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=INK, width=5)
    d.line([cx - r, cy, cx + r, cy], fill=INK, width=5)
    d.arc([cx - r, cy - r * 2 // 3, cx + r, cy + r // 3], 0, 180, fill=INK, width=5)
    d.arc([cx - r, cy - r // 3, cx + r, cy + r * 2 // 3], 180, 360, fill=INK, width=5)
    # thermometer of a warming world, in red
    tx = x1 - 26
    d.rounded_rectangle([tx - 9, y0 + 8, tx + 9, y1 - 34], 9, fill=RED)
    d.ellipse([tx - 17, y1 - 52, tx + 17, y1 - 18], fill=RED)


def icon_capitol(d, b):
    x0, y0, x1, y1 = b
    cx = (x0 + x1) // 2
    d.polygon([(cx, y0 + 6), (x0 + 30, y0 + (y1 - y0) // 3), (x1 - 30, y0 + (y1 - y0) // 3)], fill=INK)
    d.line([cx, y0, cx, y0 - 2], fill=INK, width=6)
    base = y0 + (y1 - y0) // 3 + 8
    d.rectangle([x0 + 16, base, x1 - 16, base + 10], fill=INK)
    for i in range(5):
        px = x0 + 30 + i * (x1 - x0 - 60) // 4
        d.rectangle([px - 6, base + 16, px + 6, y1 - 26], fill=INK)
    d.rectangle([x0 + 8, y1 - 22, x1 - 8, y1 - 8], fill=RED)


def icon_ship(d, b):
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    mid = y0 + h * 3 // 5
    d.polygon([(x0 + 6, mid), (x1 - 6, mid), (x1 - 22, y1 - 26), (x0 + 22, y1 - 26)], fill=INK)
    d.rectangle([x0 + w * 28 // 100, mid - 22, x0 + w * 46 // 100, mid], fill=INK)
    d.rectangle([x0 + w * 52 // 100, mid - 14, x0 + w * 68 // 100, mid], fill=RED)
    # drone above
    dx, dy = x0 + w * 72 // 100, y0 + 14
    d.ellipse([dx - 7, dy - 7, dx + 7, dy + 7], fill=RED)
    for sx, sy in ((-16, -8), (16, -8), (-16, 8), (16, 8)):
        d.line([dx, dy, dx + sx, dy + sy], fill=INK, width=4)
        d.ellipse([dx + sx - 5, dy + sy - 5, dx + sx + 5, dy + sy + 5], outline=INK, width=3)
    for i in range(3):
        wx = x0 + 4 + i * (w - 30) // 2
        d.arc([wx, y1 - 18, wx + 26, y1 - 4], 0, 180, fill=INK, width=4)
        d.arc([wx + 13, y1 - 18, wx + 39, y1 - 4], 180, 360, fill=INK, width=4)


def icon_trophy(d, b):
    x0, y0, x1, y1 = b
    cx = (x0 + x1) // 2
    w = x1 - x0
    d.polygon([(x0 + w // 4, y0 + 6), (x1 - w // 4, y0 + 6), (x1 - w // 4 - 8, y0 + (y1 - y0) // 2), (cx + 14, y0 + (y1 - y0) // 2 + 12), (cx - 14, y0 + (y1 - y0) // 2 + 12), (x0 + w // 4 + 8, y0 + (y1 - y0) // 2)], fill=INK)
    d.arc([x0 + 2, y0 + 4, x0 + w // 3, y0 + (y1 - y0) // 2], 90, 300, fill=INK, width=7)
    d.arc([x1 - w // 3, y0 + 4, x1 - 2, y0 + (y1 - y0) // 2], 240, 90, fill=INK, width=7)
    d.rectangle([cx - 9, y0 + (y1 - y0) // 2 + 12, cx + 9, y1 - 30], fill=INK)
    d.rectangle([cx - 34, y1 - 28, cx + 34, y1 - 12], fill=RED)
    d.ellipse([cx - 15, y0 + 22, cx + 15, y0 + 52], fill=PAPER, outline=RED, width=4)


def icon_flame(d, b):
    x0, y0, x1, y1 = b
    cx = (x0 + x1) // 2
    d.polygon([(cx, y0 + 2), (cx + 30, y0 + 52), (cx + 40, y0 + 92), (cx + 26, y1 - 14), (cx - 26, y1 - 14), (cx - 40, y0 + 92), (cx - 28, y0 + 50), (cx - 12, y0 + 66), (cx - 6, y0 + 40)], fill=RED)
    d.polygon([(cx, y0 + 52), (cx + 16, y0 + 88), (cx + 12, y1 - 16), (cx - 12, y1 - 16), (cx - 16, y0 + 88)], fill=(240, 140, 40))
    d.rectangle([x0 + 8, y1 - 8, x1 - 8, y1 - 2], fill=INK)


def icon_satellite(d, b):
    x0, y0, x1, y1 = b
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.rectangle([cx - 22, cy - 18, cx + 22, cy + 18], fill=INK)
    d.rectangle([x0 + 4, cy - 26, cx - 34, cy + 26], fill=(52, 84, 150))
    d.rectangle([cx + 34, cy - 26, x1 - 4, cy + 26], fill=(52, 84, 150))
    for gx in range(3):
        d.line([x0 + 16 + gx * 22, cy - 26, x0 + 16 + gx * 22, cy + 26], fill=PAPER, width=3)
        d.line([cx + 46 + gx * 22, cy - 26, cx + 46 + gx * 22, cy + 26], fill=PAPER, width=3)
    d.ellipse([cx - 6, cy - 30, cx + 6, cy - 18], fill=RED)
    d.arc([x0 - 6, y0 + 16, x1 + 6, y1 + 30], 200, 330, fill=RED, width=5)


def icon_gamepad(d, b):
    x0, y0, x1, y1 = b
    cy = (y0 + y1) // 2
    d.rounded_rectangle([x0 + 4, cy - 34, x1 - 4, cy + 34], 30, fill=INK)
    d.line([x0 + 34, cy - 12, x0 + 34, cy + 12], fill=PAPER, width=8)
    d.line([x0 + 22, cy, x0 + 46, cy], fill=PAPER, width=8)
    for dx, dy in ((0, -12), (12, 0), (0, 12), (-12, 0)):
        d.ellipse([x1 - 44 + dx - 6, cy + dy - 6, x1 - 44 + dx + 6, cy + dy + 6], fill=RED if dy == 0 else PAPER)
    # gavel slash: sentence bar
    d.rectangle([x0 + 10, y1 - 16, x1 - 10, y1 - 6], fill=RED)


def icon_jet(d, b):
    x0, y0, x1, y1 = b
    cy = (y0 + y1) // 2
    d.polygon([(x1 - 6, cy), (x0 + 52, cy - 10), (x0 + 30, cy - 30), (x0 + 16, cy - 28), (x0 + 26, cy - 6), (x0 + 10, cy), (x0 + 26, cy + 6), (x0 + 16, cy + 28), (x0 + 30, cy + 30), (x0 + 52, cy + 10)], fill=INK)
    d.ellipse([x1 - 44, cy - 6, x1 - 26, cy + 6], fill=RED)
    for i, ln in enumerate((44, 64, 84)):
        d.line([x0 + 2, cy - 20 + i * 20, x0 + 2 + ln // 3, cy - 20 + i * 20], fill=GRAY, width=5)


def icon_phone_ban(d, b):
    x0, y0, x1, y1 = b
    cx = (x0 + x1) // 2
    d.rounded_rectangle([cx - 30, y0 + 4, cx + 30, y1 - 4], 10, outline=INK, width=8)
    d.line([cx - 12, y1 - 18, cx + 12, y1 - 18], fill=INK, width=6)
    r = (x1 - x0) // 2 - 2
    ccx, ccy = (x0 + x1) // 2, (y0 + y1) // 2
    d.ellipse([ccx - r, ccy - r, ccx + r, ccy + r], outline=RED, width=10)
    d.line([ccx - r * 7 // 10, ccy + r * 7 // 10, ccx + r * 7 // 10, ccy - r * 7 // 10], fill=RED, width=10)


def icon_document(d, b):
    x0, y0, x1, y1 = b
    d.polygon([(x0 + 14, y0 + 2), (x1 - 40, y0 + 2), (x1 - 12, y0 + 30), (x1 - 12, y1 - 2), (x0 + 14, y1 - 2)], fill=CARD, outline=INK, width=0)
    d.rectangle([x0 + 14, y0 + 2, x1 - 12, y1 - 2], outline=INK, width=7)
    for i in range(3):
        yy = y0 + 34 + i * 26
        d.line([x0 + 30, yy, x1 - 30, yy], fill=GRAY, width=6)
    d.text(((x0 + x1) // 2, y1 - 52), "500,000", font=font(SANS_B, 30), fill=RED, anchor="mm")


def icon_wheat(d, b):
    x0, y0, x1, y1 = b
    cx = (x0 + x1) // 2
    d.line([cx, y1 - 4, cx, y0 + 30], fill=(176, 124, 32), width=7)
    for i in range(4):
        yy = y0 + 20 + i * 26
        d.polygon([(cx, yy + 18), (cx - 24, yy - 6), (cx - 4, yy - 10)], fill=(206, 152, 44))
        d.polygon([(cx, yy + 18), (cx + 24, yy - 6), (cx + 4, yy - 10)], fill=(206, 152, 44))


ICONS = {
    "chip": icon_chip, "globe": icon_globe, "capitol": icon_capitol,
    "ship": icon_ship, "trophy": icon_trophy, "flame": icon_flame,
    "satellite": icon_satellite, "gamepad": icon_gamepad, "jet": icon_jet,
    "phone": icon_phone_ban, "document": icon_document, "wheat": icon_wheat,
}


def chip_tag(d, xy, text):
    x, y = xy
    f = font(SANS_B, 19)
    w = d.textlength(text, font=f) + 18
    d.rectangle([x, y, x + w, y + 28], fill=RED)
    d.text((x + 9, y + 4), text, font=f, fill=(255, 255, 255))
    return w


def render(day, out_path):
    img = Image.new("RGB", (1024, 1024), PAPER)
    d = ImageDraw.Draw(img)
    # header
    d.text((512, 30), "T H E   W O R L D   I N   O N E   P I C T U R E", font=font(SANS_B, 25), fill=GRAY, anchor="ma")
    d.text((512, 62), day["date_line"], font=font(SERIF_B, 56), fill=INK, anchor="ma")
    d.line([36, 140, 988, 140], fill=INK, width=5)
    d.line([36, 148, 988, 148], fill=INK, width=2)
    # lead story
    lead = day["lead"]
    d.rectangle([36, 162, 988, 470], fill=CARD, outline=LINE, width=2)
    chip_tag(d, (64, 180), lead["tag"])
    ICONS[lead["icon"]](d, (64, 222, 292, 450))
    tx = 324
    y = text_block(d, (tx, 182), lead["headline"], font(SERIF_B, 46), INK, 636, 1.08, 3)
    text_block(d, (tx, y + 12), lead["summary"], font(SANS, 24), (40, 40, 44), 636, 1.22, 4)
    # grid of four
    cards = day["cards"]
    gx, gy, gw, gh, gap = 36, 486, 468, 226, 16
    for i, card in enumerate(cards):
        x = gx + (i % 2) * (gw + gap)
        yy = gy + (i // 2) * (gh + gap)
        d.rectangle([x, yy, x + gw, yy + gh], fill=CARD, outline=LINE, width=2)
        chip_tag(d, (x + 16, yy + 12), card["tag"])
        ICONS[card["icon"]](d, (x + 16, yy + 52, x + 126, yy + 162))
        text_block(d, (x + 140, yy + 50), card["headline"], font(SERIF_B, 29), INK, gw - 156, 1.1, 3)
        text_block(d, (x + 16, yy + 170), card["summary"], font(SANS, 20), (40, 40, 44), gw - 32, 1.18, 2)
    # ticker
    ty = 962
    d.line([36, ty, 988, ty], fill=INK, width=3)
    d.text((36, ty + 8), "ALSO TODAY:", font=font(SANS_B, 19), fill=RED)
    text_block(d, (196, ty + 9), "  ·  ".join(day["ticker"]), font(SANS, 19), (40, 40, 44), 792, 1.18, 2)
    img.save(out_path)
    return out_path


if __name__ == "__main__":
    mod = __import__(sys.argv[1])
    render(mod.DAY, sys.argv[2])
    print("wrote", sys.argv[2])
