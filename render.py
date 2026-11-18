#!/usr/bin/env python3
"""Draw the news-image entry: a one-page newspaper front page for
Wednesday, 18 November 2026. Deterministic: fixed text, fixed geometry,
no randomness, no timestamps, no network. Output is a 1024x1024 PNG."""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
CREAM = (247, 242, 231)
INK = (26, 26, 26)
GRAY = (90, 86, 78)
RED = (185, 28, 28)
DARK = (24, 24, 24)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_MASTHEAD = font("DejaVuSerif-Bold.ttf", 58)
F_DATE = font("DejaVuSans-Bold.ttf", 36)
F_LABEL = font("DejaVuSans-Bold.ttf", 19)
F_HEAD = font("DejaVuSans-Bold.ttf", 29)
F_DECK = font("DejaVuSans.ttf", 20)
F_FOOT = font("DejaVuSans.ttf", 21)
F_FOOT_BOLD = font("DejaVuSans-Bold.ttf", 21)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap by pixel width; returns a list of lines."""
    words = text.split()
    lines = []
    cur = ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_tracked(draw, xy, text, fnt, fill, tracking=3):
    """Draw text with extra space between letters (for section labels)."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + tracking
    return x


# ---------------------------------------------------------------- icons ---
# Each icon draws inside a 64x64 box whose top-left is (bx, by).
# Ink + one red accent only.

def icon_burst(d, bx, by):
    import math

    cx, cy = bx + 32, by + 32
    pts = []
    for i in range(24):
        ang = math.pi * 2 * i / 24
        r = 30 if i % 2 == 0 else 16
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    d.polygon(pts, fill=RED)
    d.ellipse([cx - 11, cy - 11, cx + 11, cy + 11], fill=CREAM)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=INK)


def icon_bridge(d, bx, by):
    # Two towers, a deck with a collapsed gap, one sagging cable.
    d.line([(bx + 8, by + 52), (bx + 8, by + 16)], fill=INK, width=4)
    d.line([(bx + 56, by + 52), (bx + 56, by + 16)], fill=INK, width=4)
    d.arc([bx + 4, by - 14, bx + 60, by + 34], start=20, end=160,
          fill=INK, width=3)
    d.line([(bx + 2, by + 52), (bx + 26, by + 52)], fill=INK, width=4)
    d.line([(bx + 38, by + 52), (bx + 62, by + 52)], fill=INK, width=4)
    d.line([(bx + 26, by + 52), (bx + 32, by + 60)], fill=RED, width=4)
    d.line([(bx + 38, by + 52), (bx + 32, by + 60)], fill=RED, width=4)
    for x in (14, 24, 40, 50):
        d.line([(bx + x, by + 30), (bx + x, by + 52)], fill=GRAY, width=2)


def icon_summit(d, bx, by):
    # Three flags on poles, middle one red. Flags stay inside the box.
    for i, col in enumerate((INK, RED, INK)):
        x = bx + 6 + i * 20
        d.line([(x, by + 56), (x, by + 8)], fill=INK, width=3)
        d.polygon([(x, by + 8), (x + 14, by + 14), (x, by + 20)], fill=col)
    d.line([(bx + 2, by + 58), (bx + 58, by + 58)], fill=INK, width=3)


def icon_virus(d, bx, by):
    import math

    cx, cy = bx + 32, by + 32
    for i in range(8):
        ang = math.pi * 2 * i / 8
        x1, y1 = cx + 18 * math.cos(ang), cy + 18 * math.sin(ang)
        x2, y2 = cx + 28 * math.cos(ang), cy + 28 * math.sin(ang)
        d.line([(x1, y1), (x2, y2)], fill=INK, width=3)
        d.ellipse([x2 - 4, y2 - 4, x2 + 4, y2 + 4], fill=INK)
    d.ellipse([cx - 19, cy - 19, cx + 19, cy + 19], fill=INK)
    for dx, dy in ((-7, -5), (6, -8), (0, 7), (-8, 8), (8, 2)):
        d.ellipse([cx + dx - 3, cy + dy - 3, cx + dx + 3, cy + dy + 3],
                  fill=RED)


def icon_spots(d, bx, by):
    # Measles: a ring of red spots.
    d.ellipse([bx + 4, by + 4, bx + 60, by + 60], outline=INK, width=4)
    for cx, cy, r in ((24, 24, 8), (42, 30, 6), (28, 44, 7), (44, 46, 5),
                      (20, 36, 4), (38, 18, 4)):
        d.ellipse([bx + cx - r, by + cy - r, bx + cx + r, by + cy + r],
                  fill=RED)


def icon_dome(d, bx, by):
    # Capitol dome: dome, drum, columns, base.
    d.pieslice([bx + 12, by + 10, bx + 52, by + 50], start=180, end=360,
               fill=INK)
    d.rectangle([bx + 16, by + 32, bx + 48, by + 40], fill=INK)
    d.line([(bx + 32, by + 10), (bx + 32, by + 2)], fill=INK, width=3)
    d.polygon([(bx + 32, by + 2), (bx + 42, by + 6), (bx + 32, by + 10)],
              fill=RED)
    for x in (16, 26, 36, 46):
        d.line([(bx + x, by + 42), (bx + x, by + 54)], fill=INK, width=3)
    d.line([(bx + 8, by + 56), (bx + 56, by + 56)], fill=INK, width=4)
    d.line([(bx + 12, by + 60), (bx + 52, by + 60)], fill=INK, width=2)


STORIES = [
    ("GULF", "U.S. strikes Iran's Qeshm Island",
     "Iran fires drones at Bahrain and Kuwait; U.S. jets hit a "
     "Revolutionary Guard missile site.", icon_burst),
    ("UKRAINE", "Kerch Bridge span collapses",
     "Ukraine hits the Crimea bridge for a second day with drones "
     "and missiles.", icon_bridge),
    ("SUMMIT", "APEC opens in Shenzhen",
     "Trump, Xi and Putin to meet Thursday in a first-ever "
     "trilateral summit.", icon_summit),
    ("EBOLA", "Ebola cases double in Congo",
     "11,000+ cases, 5,400 dead, the UN says; 3 in 4 infected "
     "children under 5 die.", icon_virus),
    ("MEASLES", "U.S. loses measles-free status",
     "After 26 years: 5,400+ cases and 10 deaths, the most since "
     "the early 1990s.", icon_spots),
    ("SENATE", "Democrats reach 56 Senate seats",
     "Mary Peltola wins Alaska's Senate race.", icon_dome),
]

FOOTER = ("Also: 19 dead as Russian military plane crashes in Siberia "
          "\u2022 M6.0 quake hits Papua New Guinea \u2022 Category 5 "
          "Cyclone Xavier strikes Northern Cook Islands")


def main():
    out_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "entry.png")

    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # Outer double border.
    d.rectangle([14, 14, W - 15, H - 15], outline=INK, width=3)
    d.rectangle([22, 22, W - 23, H - 23], outline=INK, width=1)

    # Masthead.
    name = "THE WORLD IN ONE PAGE"
    nw = d.textlength(name, font=F_MASTHEAD)
    d.text(((W - nw) / 2, 34), name, font=F_MASTHEAD, fill=INK)
    d.line([(36, 116), (W - 36, 116)], fill=INK, width=4)
    d.line([(36, 124), (W - 36, 124)], fill=INK, width=1)

    # Date band: the day, large and unmissable.
    d.rectangle([36, 136, W - 36, 194], fill=INK)
    date = "Wednesday, 18 November 2026"
    dw = d.textlength(date, font=F_DATE)
    d.text(((W - dw) / 2, 148), date, font=F_DATE, fill=CREAM)
    d.line([(36, 206), (W - 36, 206)], fill=INK, width=1)

    # Story grid: 2 columns x 3 rows.
    grid_top = 220
    grid_bottom = 902
    row_h = (grid_bottom - grid_top) // 3
    col_w = (W - 72) // 2
    mid_x = 36 + col_w + 12

    # Dividers.
    for r in (1, 2):
        y = grid_top + r * row_h
        d.line([(36, y), (W - 36, y)], fill=GRAY, width=1)
    d.line([(mid_x, grid_top + 8), (mid_x, grid_bottom - 8)],
           fill=GRAY, width=1)

    for i, (label, head, deck, icon) in enumerate(STORIES):
        row, col = divmod(i, 2)
        x0 = 36 if col == 0 else mid_x + 12
        y0 = grid_top + row * row_h
        text_x = x0 + 80
        text_w = (col_w - 12) - 80 if col == 0 else (W - 36 - x0) - 80

        # Icon, vertically centred against the text block.
        icon(d, x0 + 4, y0 + 52)

        # Red section label with a red square bullet.
        d.rectangle([text_x, y0 + 18, text_x + 11, y0 + 29], fill=RED)
        draw_tracked(d, (text_x + 20, y0 + 12), label, F_LABEL, RED)

        # Headline, wrapped to at most 2 lines.
        lines = wrap(d, head, F_HEAD, text_w)[:2]
        hy = y0 + 42
        for ln in lines:
            d.text((text_x, hy), ln, font=F_HEAD, fill=INK)
            hy += 35

        # Deck, wrapped.
        dy = hy + 6
        for ln in wrap(d, deck, F_DECK, text_w):
            d.text((text_x, dy), ln, font=F_DECK, fill=GRAY)
            dy += 26

    # Footer strip.
    d.rectangle([36, 916, W - 36, 988], fill=DARK)
    foot_lines = wrap(d, FOOTER, F_FOOT, W - 72 - 32)
    fy = 928
    for ln in foot_lines:
        lw = d.textlength(ln, font=F_FOOT)
        d.text(((W - lw) / 2, fy), ln, font=F_FOOT, fill=CREAM)
        fy += 28

    img.save(out_path, format="PNG", optimize=False)
    print("wrote", out_path, img.size)


if __name__ == "__main__":
    main()
