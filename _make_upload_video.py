#!/usr/bin/env python3
"""Build the ISM2411 video "Upload your lab to GitHub: drag one folder".

Writes, into OUT_DIR:
  upload_whole_folder.mp4   1280x720, 30 fps, narrated
  upload_whole_folder.srt   subtitles that match the narration
  upload_whole_folder.md    narration script, timings, YouTube title/description/chapters

    python _make_upload_video.py OUT_DIR --voice en_US-lessac-medium.onnx [--preview]

Needs pillow, numpy, imageio-ffmpeg and piper-tts. The narration is spoken by a
local piper voice (`python -m piper.download_voices en_US-lessac-medium`), so
nothing is sent anywhere. --preview writes contact sheets of still frames to
OUT_DIR/preview/ instead of encoding the video.

The screens are simplified drawings of VS Code, Finder / File Explorer, the
GitHub upload page and Canvas, using the real button labels students click.
The example lab is Lab 14 (ism2411-lab14: clean.py and data/).
"""

import argparse
import hashlib
import io
import math
import re
import subprocess
import wave
from functools import lru_cache
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1280, 720, 30
BAND_Y = 590

NOTO = Path("/usr/share/fonts/truetype/noto")
JBM = Path.home() / ".local/share/fonts/JetBrainsMono"
DEJAVU = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"  # Noto Sans has no arrow glyphs

BG = (17, 21, 34)
BAND = (10, 13, 22)
GOLD = (251, 191, 36)
GREEN = (52, 211, 153)
BLUE = (96, 165, 250)
WHITE = (241, 245, 249)
MUTED = (148, 163, 184)
DIM = (100, 116, 139)

GH_TEXT = (31, 35, 40)
GH_MUTED = (89, 99, 110)
GH_BORDER = (208, 215, 222)
GH_HEAD = (246, 248, 250)
GH_LINK = (9, 105, 218)
GH_GREEN = (31, 136, 61)
GH_FOLDER = (84, 174, 255)
GH_BLUE_BG = (221, 244, 255)

URL_REPO = "github.com/YOURUSERNAME/ism2411-lab14"
URL_UPLOAD = URL_REPO + "/upload/main"
URL_FOLDER = URL_REPO + "/tree/main/ism2411-lab14"
URL_COMMITS = URL_REPO + "/commits/main"
TAB = "YOURUSERNAME/ism2411-lab14"
LAB_PAGE = "https://markumreed.github.io/ism2411/pages/week11_lab.html#repo-setup"


# ---------------------------------------------------------------- fonts, time


@lru_cache(None)
def sans(size, bold=False):
    return ImageFont.truetype(str(NOTO / ("NotoSans-Bold.ttf" if bold else "NotoSans-Regular.ttf")), int(size))


@lru_cache(None)
def mono(size, bold=False):
    name = "JetBrainsMonoNerdFontMono-Bold.ttf" if bold else "JetBrainsMonoNerdFontMono-Regular.ttf"
    return ImageFont.truetype(str(JBM / name), int(size))


@lru_cache(None)
def arrow_font(size):
    return ImageFont.truetype(DEJAVU, int(size))


def text(d, xy, s, font, fill, anchor="lm"):
    """d.text that draws each → with DejaVu Sans. Returns the width drawn."""
    x, y = xy
    af = arrow_font(font.size)
    for i, part in enumerate(s.split("→")):
        if i:
            d.text((x, y), "→", font=af, fill=fill, anchor=anchor)
            x += af.getlength("→")
        if part:
            d.text((x, y), part, font=font, fill=fill, anchor=anchor)
            x += font.getlength(part)
    return x - xy[0]


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def smooth(p):
    p = clamp(p)
    return p * p * (3 - 2 * p)


def prog(t, t0, t1):
    if t1 <= t0:
        return float(t >= t1)
    return smooth((t - t0) / (t1 - t0))


def lerp(a, b, p):
    return a + (b - a) * p


def lerp_pt(a, b, p):
    return (lerp(a[0], b[0], p), lerp(a[1], b[1], p))


def lerp_box(a, b, p):
    return tuple(lerp(a[i], b[i], p) for i in range(4))


def along(t, keys):
    """Cursor position at time t along [(time, (x, y)), ...], eased between keys."""
    if t <= keys[0][0]:
        return keys[0][1]
    for (t0, p0), (t1, p1) in zip(keys, keys[1:]):
        if t <= t1:
            return lerp_pt(p0, p1, prog(t, t0, t1))
    return keys[-1][1]


def center(r):
    return ((r[0] + r[2]) / 2, (r[1] + r[3]) / 2)


def point_in(p, r):
    return r[0] <= p[0] <= r[2] and r[1] <= p[1] <= r[3]


def scale_box(b, s):
    cx, cy = center(b)
    hw, hh = (b[2] - b[0]) / 2 * s, (b[3] - b[1]) / 2 * s
    return (cx - hw, cy - hh, cx + hw, cy + hh)


def typed(text, t, t0, t1):
    return text[: round(len(text) * clamp((t - t0) / (t1 - t0)))]


# ---------------------------------------------------------------- primitives


def tri(d, x, y, color, size=4):
    d.polygon([(x - size, y - size / 2), (x + size, y - size / 2), (x, y + size / 2 + 1)], fill=color)


def spaced(d, xy, s, font, fill, spacing=2, align="left"):
    x, y = xy
    total = sum(font.getlength(c) for c in s) + spacing * (len(s) - 1)
    if align == "right":
        x -= total
    elif align == "center":
        x -= total / 2
    for c in s:
        d.text((x, y), c, font=font, fill=fill, anchor="lm")
        x += font.getlength(c) + spacing


def rich(d, xy, s, size, color, code_color=(253, 224, 138), code_bg=(36, 42, 60)):
    """Text where `backticked` parts render as code chips. y is the middle line."""
    x, y = xy
    for i, part in enumerate(s.split("`")):
        if not part:
            continue
        if i % 2:
            f = mono(int(size * 0.86))
            wpx = f.getlength(part)
            d.rounded_rectangle([x, y - size * 0.62, x + wpx + 14, y + size * 0.62], radius=6, fill=code_bg)
            d.text((x + 7, y), part, font=f, fill=code_color, anchor="lm")
            x += wpx + 16
        else:
            x += text(d, (x, y), part, sans(size), color)
    return x


def rich_width(text, size):
    x = 0
    for i, part in enumerate(text.split("`")):
        if part:
            x += mono(int(size * 0.86)).getlength(part) + 16 if i % 2 else sans(size).getlength(part)
    return x


def dashed(d, box, color, width=2, dash=10, gap=7, r=10):
    x0, y0, x1, y1 = box
    for cx, cy, start in ((x0 + r, y0 + r, 180), (x1 - r, y0 + r, 270), (x1 - r, y1 - r, 0), (x0 + r, y1 - r, 90)):
        d.arc([cx - r, cy - r, cx + r, cy + r], start, start + 90, fill=color, width=width)
    x = x0 + r
    while x < x1 - r:
        e = min(x + dash, x1 - r)
        d.line([(x, y0), (e, y0)], fill=color, width=width)
        d.line([(x, y1), (e, y1)], fill=color, width=width)
        x += dash + gap
    y = y0 + r
    while y < y1 - r:
        e = min(y + dash, y1 - r)
        d.line([(x0, y), (x0, e)], fill=color, width=width)
        d.line([(x1, y), (x1, e)], fill=color, width=width)
        y += dash + gap


def shadow(d, box, r=10):
    x0, y0, x1, y1 = box
    for off, col in ((10, (14, 17, 28)), (6, (11, 13, 22)), (3, (7, 9, 15))):
        d.rounded_rectangle([x0 - 2, y0 + off, x1 + 2, y1 + off], radius=r + 3, fill=col)


def folder_icon(d, x, y, w, color=BLUE):
    h = w * 0.78
    dark = tuple(int(c * 0.80) for c in color)
    light = tuple(min(255, int(c * 1.07)) for c in color)
    d.rounded_rectangle([x, y, x + w * 0.44, y + h * 0.36], radius=max(2, w * 0.07), fill=dark)
    d.rounded_rectangle([x, y + h * 0.16, x + w, y + h], radius=max(2, w * 0.09), fill=color)
    d.rounded_rectangle([x, y + h * 0.30, x + w, y + h], radius=max(2, w * 0.09), fill=light)


def file_icon(d, x, y, w, tag=None, tag_color=(34, 160, 107)):
    h = w * 1.25
    fold = w * 0.3
    d.polygon([(x, y), (x + w - fold, y), (x + w, y + fold), (x + w, y + h), (x, y + h)],
              fill=(255, 255, 255), outline=(160, 168, 180))
    d.polygon([(x + w - fold, y), (x + w - fold, y + fold), (x + w, y + fold)], fill=(222, 226, 232), outline=(160, 168, 180))
    if tag:
        th = w * 0.36
        d.rounded_rectangle([x - w * 0.12, y + h * 0.5, x + w * 0.8, y + h * 0.5 + th], radius=3, fill=tag_color)
        d.text((x + w * 0.34, y + h * 0.5 + th / 2), tag, font=sans(max(8, int(w * 0.25)), True), fill=(255, 255, 255), anchor="mm")


def check(d, cx, cy, s=7, col=(255, 255, 255), width=3):
    d.line([(cx - s, cy), (cx - s * 0.3, cy + s * 0.7), (cx + s, cy - s * 0.7)], fill=col, width=width, joint="curve")


def clock(d, cx, cy, col=GH_MUTED):
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], outline=col, width=2)
    d.line([(cx, cy - 4), (cx, cy), (cx + 3, cy + 2)], fill=col, width=2)


def ring(d, box, t, color=GOLD, pad=6):
    a = int(150 + 105 * (0.5 + 0.5 * math.sin(t * 6.0)))
    x0, y0, x1, y1 = box
    d.rounded_rectangle([x0 - pad, y0 - pad, x1 + pad, y1 + pad], radius=10, outline=color + (a,), width=3)


def ripple(d, pos, age):
    if 0 <= age <= 0.45:
        k = age / 0.45
        r = 6 + 24 * k
        d.ellipse([pos[0] - r, pos[1] - r, pos[0] + r, pos[1] + r], outline=GOLD + (int(230 * (1 - k)),), width=3)


def badge(d, x, y, text, alpha=1.0, fill=(26, 127, 55)):
    a = int(255 * alpha)
    f = sans(15, True)
    tw = f.getlength(text)
    d.rounded_rectangle([x, y, x + tw + 54, y + 36], radius=18, fill=fill + (a,))
    d.ellipse([x + 8, y + 7, x + 30, y + 29], fill=(255, 255, 255, a))
    check(d, x + 19, y + 18, s=6, col=fill + (a,), width=3)
    d.text((x + 40, y + 18), text, font=f, fill=(255, 255, 255, a), anchor="lm")
    return x + tw + 54


def make_cursor():
    s = 1.3
    pts = [(0, 0), (0, 22), (5, 17), (9, 26), (12, 25), (8, 16), (15, 16)]
    pts = [(px * s + 3, py * s + 3) for px, py in pts]
    im = Image.new("RGBA", (40, 46), (0, 0, 0, 0))
    d = ImageDraw.Draw(im, "RGBA")
    d.polygon([(px + 1.5, py + 2.5) for px, py in pts], fill=(0, 0, 0, 90))
    d.polygon(pts, fill=(255, 255, 255, 255))
    d.line(pts + [pts[0]], fill=(0, 0, 0, 255), width=2, joint="curve")
    return im


CURSOR = make_cursor()


def draw_cursor(fr, pos):
    x = int(clamp(pos[0], 3, W - 40)) - 3
    y = int(clamp(pos[1], 3, H - 46)) - 3
    fr.paste(CURSOR, (x, y), CURSOR)


def make_ghost(kind, name):
    im = Image.new("RGBA", (150, 110), (0, 0, 0, 0))
    d = ImageDraw.Draw(im, "RGBA")
    if kind == "dir":
        folder_icon(d, 48, 10, 54)
    else:
        file_icon(d, 58, 6, 34, tag="CSV")
    f = sans(12)
    lw = f.getlength(name)
    d.rounded_rectangle([75 - lw / 2 - 6, 66, 75 + lw / 2 + 6, 86], radius=5, fill=(10, 132, 255))
    d.text((75, 76), name, font=f, fill=(255, 255, 255), anchor="mm")
    im.putalpha(im.getchannel("A").point(lambda v: int(v * 0.8)))
    return im


FOLDER_GHOST = make_ghost("dir", "ism2411-lab14")
CSV_GHOST = make_ghost("csv", "messy_sales.csv")


def ghost(fr, sprite, pos):
    fr.paste(sprite, (int(pos[0] - 75), int(pos[1] - 34)), sprite)


# ---------------------------------------------------------------- windows


def win(d, box, title, dark=False, title_h=32):
    x0, y0, x1, y1 = box
    shadow(d, box)
    body = (30, 30, 30) if dark else (255, 255, 255)
    bar = (50, 50, 51) if dark else (232, 232, 235)
    d.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=body)
    d.rounded_rectangle([x0, y0, x1, y0 + title_h], radius=10, fill=bar, corners=(True, True, False, False))
    for i in range(3):
        cx, cy = x0 + 20 + i * 18, y0 + title_h / 2
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(92, 92, 96) if dark else (198, 198, 204))
    d.text(((x0 + x1) / 2, y0 + title_h / 2), title, font=sans(13), fill=(200, 200, 200) if dark else (70, 70, 76), anchor="mm")
    return (x0, y0 + title_h, x1, y1)


def br_cb(box):
    x0, y0, x1, y1 = (int(round(v)) for v in box)
    return (x0, y0 + 83, x1, y1 - 1)


def browser(d, box, url, tab, private=False):
    x0, y0, x1, y1 = (int(round(v)) for v in box)
    shadow(d, (x0, y0, x1, y1))
    strip = (53, 54, 58) if private else (222, 225, 230)
    chrome = (32, 33, 36) if private else (255, 255, 255)
    url_bg = (53, 54, 58) if private else (241, 243, 244)
    txt = (232, 234, 237) if private else (60, 64, 67)
    d.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=(255, 255, 255))
    d.rounded_rectangle([x0, y0, x1, y0 + 40], radius=10, fill=strip, corners=(True, True, False, False))
    for i in range(3):
        cx, cy = x0 + 20 + i * 18, y0 + 20
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(110, 110, 116) if private else (190, 192, 198))
    tx0 = x0 + 84
    tw = min(250, (x1 - x0) * 0.36)
    d.rounded_rectangle([tx0, y0 + 7, tx0 + tw, y0 + 41], radius=8, fill=chrome, corners=(True, True, False, False))
    d.text((tx0 + 14, y0 + 24), tab, font=sans(12), fill=txt, anchor="lm")
    d.rectangle([x0, y0 + 40, x1, y0 + 82], fill=chrome)
    for i, ch in enumerate("‹›"):
        d.text((x0 + 22 + i * 26, y0 + 60), ch, font=sans(24), fill=(150, 150, 156), anchor="mm")
    ux0, ux1 = x0 + 76, x1 - (150 if private else 22)
    d.rounded_rectangle([ux0, y0 + 47, ux1, y0 + 75], radius=14, fill=url_bg)
    d.text((ux0 + 16, y0 + 61), url, font=sans(14), fill=txt, anchor="lm")
    if private:
        d.text((x1 - 22, y0 + 61), "Private window", font=sans(13, True), fill=txt, anchor="rm")
    d.line([(x0, y0 + 82), (x1, y0 + 82)], fill=(70, 70, 74) if private else (218, 220, 224))
    return (x0, y0 + 83, x1, y1 - 1)


@lru_cache(maxsize=32)
def bottom_round_mask(w, h, r=10):
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], radius=r, fill=255, corners=(False, False, True, True))
    return m


def paste_page(fr, cb, page, scroll=0):
    x0, y0, x1, y1 = cb
    w, h = x1 - x0, y1 - y0
    fr.paste(page.crop((0, int(scroll), w, int(scroll) + h)), (x0, y0), bottom_round_mask(w, h))


def to_screen(r, cb, scroll=0):
    return (r[0] + cb[0], r[1] + cb[1] - scroll, r[2] + cb[0], r[3] + cb[1] - scroll)


# ---------------------------------------------------------------- VS Code

CODE = (
    "import pandas as pd",
    "",
    'df = pd.read_csv("data/messy_sales.csv")',
    "print(df.shape)",
    "",
    "df = df.drop_duplicates()",
    "print(df.shape)",
    "",
    'df.to_csv("data/clean_sales.csv", index=False)',
)
TREE_1 = ((0, "dir", "data"), (0, "file", "clean.py"))
TREE_2 = ((0, "dir", "data"), (1, "file", "messy_sales.csv"), (0, "file", "clean.py"))
TREE_3 = ((0, "dir", "data"), (1, "file", "clean_sales.csv"), (1, "file", "messy_sales.csv"), (0, "file", "clean.py"))


def code_line(d, x, y, line):
    f = mono(13)
    toks = re.findall(r'"[^"]*"|#.*|\w+|\s+|[^\w\s]', line)
    for i, tok in enumerate(toks):
        if tok.startswith('"'):
            c = (206, 145, 120)
        elif tok.startswith("#"):
            c = (106, 153, 85)
        elif tok in ("import", "as", "from"):
            c = (197, 134, 192)
        elif tok in ("True", "False", "None"):
            c = (86, 156, 214)
        elif re.fullmatch(r"\w+", tok) and i + 1 < len(toks) and toks[i + 1] == "(":
            c = (220, 220, 170)
        elif re.fullmatch(r"\w+", tok):
            c = (156, 220, 254)
        else:
            c = (212, 212, 212)
        d.text((x, y), tok, font=f, fill=c, anchor="lm")
        x += f.getlength(tok)


def term_line(d, x, y, item, t):
    f = mono(14)
    if item[0] == "comment":
        d.text((x, y), item[1], font=f, fill=(106, 153, 85), anchor="lm")
        return
    _, prompt, text, tag, cursor = item
    d.text((x, y), prompt, font=f, fill=(78, 201, 176), anchor="lm")
    x += f.getlength(prompt)
    d.text((x, y), "$ ", font=f, fill=(204, 204, 204), anchor="lm")
    x += f.getlength("$ ")
    d.text((x, y), text, font=f, fill=(245, 245, 245), anchor="lm")
    x += f.getlength(text)
    if cursor and int(t * 2.5) % 2 == 0:
        d.rectangle([x + 1, y - 8, x + 9, y + 8], fill=(204, 204, 204))
    if tag:
        label, col = tag
        fw = sans(12, True)
        tw = fw.getlength(label) + 18
        d.rounded_rectangle([x + 24, y - 11, x + 24 + tw, y + 11], radius=11, fill=col)
        d.text((x + 24 + tw / 2, y), label, font=fw, fill=(20, 20, 24), anchor="mm")


def vscode_rows(box, tree):
    x0, y0, x1, y1 = box
    cy0 = y0 + 32
    sx0, sx1 = x0 + 46, x0 + 292
    hy = cy0 + 48
    rows = {"header": (sx0 + 6, hy - 11, sx1 - 6, hy + 11)}
    for i, (_, _, name) in enumerate(tree):
        ry = hy + 26 + i * 26
        rows[name] = (sx0, ry - 12, sx1, ry + 12)
    return rows


def vscode(d, box, tree, drop_row=None, flash=None, term=None, t=0.0):
    cx0, cy0, cx1, cy1 = win(d, box, "clean.py — ism2411-lab14", dark=True)
    d.rounded_rectangle([cx0, cy0, cx0 + 46, cy1], radius=10, fill=(51, 51, 51), corners=(False, False, False, True))
    for i in range(4):
        col = (215, 215, 215) if i == 0 else (120, 120, 120)
        d.rounded_rectangle([cx0 + 14, cy0 + 16 + i * 46, cx0 + 32, cy0 + 34 + i * 46], radius=4, outline=col, width=2)
    sx0, sx1 = cx0 + 46, cx0 + 292
    d.rectangle([sx0, cy0, sx1, cy1 - 1], fill=(37, 37, 38))
    d.text((sx0 + 18, cy0 + 20), "EXPLORER", font=sans(11), fill=(187, 187, 187), anchor="lm")
    rows = vscode_rows(box, tree)
    hy = center(rows["header"])[1]
    tri(d, sx0 + 14, hy, (204, 204, 204))
    d.text((sx0 + 24, hy), "ISM2411-LAB14", font=sans(12, True), fill=(225, 225, 225), anchor="lm")
    for indent, kind, name in tree:
        r = rows[name]
        ry = center(r)[1]
        if name == drop_row:
            d.rectangle(r, fill=(9, 71, 113), outline=(0, 127, 212))
        if flash and flash[0] == name and flash[1] > 0:
            d.rectangle(r, fill=(52, 211, 153, int(120 * flash[1])))
        ix = sx0 + 20 + indent * 18
        if kind == "dir":
            tri(d, ix, ry, (197, 197, 197))
            folder_icon(d, ix + 10, ry - 6, 15, color=(220, 182, 92))
        else:
            col = (55, 118, 171) if name.endswith(".py") else (40, 160, 90)
            d.rounded_rectangle([ix + 11, ry - 7, ix + 23, ry + 7], radius=3, fill=col)
        d.text((ix + 32, ry), name, font=sans(13), fill=(210, 210, 210), anchor="lm")
    ex0 = sx1
    d.rectangle([ex0, cy0, cx1, cy0 + 34], fill=(37, 37, 38))
    d.rectangle([ex0, cy0, ex0 + 118, cy0 + 34], fill=(30, 30, 30))
    d.text((ex0 + 16, cy0 + 17), "clean.py", font=sans(13), fill=(235, 235, 235), anchor="lm")
    ed_top = cy0 + 34
    ed_bot = cy1 - (172 if term is not None else 0)
    for i, line in enumerate(CODE):
        ly = ed_top + 24 + i * 22
        if ly > ed_bot - 12:
            break
        d.text((ex0 + 30, ly), str(i + 1), font=mono(13), fill=(110, 118, 129), anchor="rm")
        code_line(d, ex0 + 46, ly, line)
    if term is not None:
        d.line([(ex0, ed_bot), (cx1, ed_bot)], fill=(69, 69, 69))
        d.text((ex0 + 16, ed_bot + 18), "TERMINAL", font=sans(11, True), fill=(231, 231, 231), anchor="lm")
        d.line([(ex0 + 14, ed_bot + 30), (ex0 + 74, ed_bot + 30)], fill=(231, 231, 231))
        for i, item in enumerate(term):
            term_line(d, ex0 + 16, ed_bot + 56 + i * 25, item, t)
    return rows


# ---------------------------------------------------------------- Finder / File Explorer

FINDER_SB = 118
HOME_ITEMS = (("dir", "Desktop"), ("dir", "Documents"), ("dir", "Downloads"),
              ("dir", "ism2411-lab12"), ("dir", "ism2411-lab13"), ("dir", "ism2411-lab14"))
DL_ITEMS = (("csv", "retail_sales.csv"), ("csv", "sales.csv"), ("csv", "messy_sales.csv"))


def finder_cells(box, items):
    x0, y0, x1, y1 = box
    gx0, gy0 = x0 + FINDER_SB + 12, y0 + 32 + 14
    cw, ch = 108, 102
    cols = max(1, int((x1 - gx0 - 4) // cw))
    out = {}
    for i, (kind, name) in enumerate(items):
        cx, cy = gx0 + (i % cols) * cw, gy0 + (i // cols) * ch
        out[name] = {"kind": kind, "cell": (cx, cy, cx + cw, cy + ch),
                     "center": (cx + cw / 2, cy + 34), "rect": (cx + 12, cy + 2, cx + cw - 12, cy + 90)}
    return out


def finder(d, box, title, items, selected=None, side_sel=None):
    x0, y0, x1, y1 = box
    d.text((x0 + 4, y0 - 14), "Finder (Mac) · File Explorer (Windows)", font=sans(13), fill=MUTED, anchor="lm")
    cx0, cy0, cx1, cy1 = win(d, box, title)
    d.rounded_rectangle([cx0, cy0, cx0 + FINDER_SB, cy1], radius=10, fill=(244, 244, 246), corners=(False, False, False, True))
    d.line([(cx0 + FINDER_SB, cy0), (cx0 + FINDER_SB, cy1 - 1)], fill=(226, 226, 230))
    d.text((cx0 + 14, cy0 + 18), "Favorites", font=sans(11, True), fill=(140, 140, 148), anchor="lm")
    for i, s in enumerate(("Home", "Desktop", "Documents", "Downloads")):
        sy = cy0 + 44 + i * 28
        if s == side_sel:
            d.rounded_rectangle([cx0 + 6, sy - 12, cx0 + FINDER_SB - 6, sy + 12], radius=6, fill=(216, 219, 226))
        folder_icon(d, cx0 + 14, sy - 6, 15)
        d.text((cx0 + 36, sy), s, font=sans(13), fill=(40, 40, 46), anchor="lm")
    for name, c in finder_cells(box, items).items():
        cx, cy, cx2, _ = c["cell"]
        mid = (cx + cx2) / 2
        if name == selected:
            d.rounded_rectangle([mid - 38, cy + 2, mid + 38, cy + 64], radius=8, fill=(224, 227, 233))
        if c["kind"] == "dir":
            folder_icon(d, mid - 27, cy + 13, 54)
        else:
            file_icon(d, mid - 17, cy + 8, 34, tag="CSV")
        f = sans(12)
        ly = cy + 78
        lw = f.getlength(name)
        if name == selected:
            d.rounded_rectangle([mid - lw / 2 - 6, ly - 10, mid + lw / 2 + 6, ly + 10], radius=5, fill=(10, 132, 255))
            d.text((mid, ly), name, font=f, fill=(255, 255, 255), anchor="mm")
        else:
            d.text((mid, ly), name, font=f, fill=(30, 30, 36), anchor="mm")


# ---------------------------------------------------------------- GitHub pages

ROWS_START = (("file", ".gitignore", "Initial commit", "3 hours ago"),
              ("file", "README.md", "Update README.md", "3 hours ago"))
ROWS_AFTER = (("dir", "ism2411-lab14", "Add files via upload", "now"),) + ROWS_START
ROWS_FOLDER = (("dir", "data", "Add files via upload", "now"), ("file", "clean.py", "Add files via upload", "now"))
UPLOAD_FILES = ("ism2411-lab14/clean.py", "ism2411-lab14/data/clean_sales.csv", "ism2411-lab14/data/messy_sales.csv")
COMMITS = (("Add files via upload", "2 hours ago", "7b41d0a"),
           ("Update README.md", "3 hours ago", "c90e1f2"),
           ("Initial commit", "3 hours ago", "3f9c2e1"))
NEW_COMMIT = ("Add files via upload", "now", "e52a9c4")


def gh_btn(d, box, label, primary=False, caret=True, pressed=False):
    fill = ((26, 112, 52) if pressed else GH_GREEN) if primary else (246, 248, 250)
    d.rounded_rectangle(box, radius=6, fill=fill, outline=(26, 127, 55) if primary else GH_BORDER)
    col = (255, 255, 255) if primary else GH_TEXT
    f = sans(14, True)
    tw = f.getlength(label) + (16 if caret else 0)
    x = (box[0] + box[2]) / 2 - tw / 2
    y = (box[1] + box[3]) / 2
    d.text((x, y), label, font=f, fill=col, anchor="lm")
    if caret:
        tri(d, x + f.getlength(label) + 10, y, col)


def gh_folder(d, x, cy):
    d.rounded_rectangle([x, cy - 7, x + 7, cy - 2], radius=1, fill=GH_FOLDER)
    d.rounded_rectangle([x, cy - 5, x + 16, cy + 7], radius=2, fill=GH_FOLDER)


def gh_file(d, x, cy):
    d.polygon([(x + 1, cy - 8), (x + 10, cy - 8), (x + 14, cy - 4), (x + 14, cy + 8), (x + 1, cy + 8)], outline=GH_MUTED)
    d.line([(x + 10, cy - 8), (x + 10, cy - 4), (x + 14, cy - 4)], fill=GH_MUTED)


def new_page(w, h=1100):
    im = Image.new("RGB", (w, h), (255, 255, 255))
    return im, ImageDraw.Draw(im, "RGBA")


@lru_cache(maxsize=64)
def gh_repo(w, rows, last_msg, commits, folder=False, readme=True, hover=None):
    im, d = new_page(w, 900)
    pad = 28
    R = {}
    y = 30
    x = pad
    d.rounded_rectangle([x, y - 9, x + 13, y + 9], radius=2, outline=GH_MUTED, width=2)
    x += 24
    f, fb = sans(18), sans(18, True)
    d.text((x, y), "YOURUSERNAME", font=f, fill=GH_LINK, anchor="lm")
    x += f.getlength("YOURUSERNAME") + 8
    d.text((x, y), "/", font=f, fill=GH_MUTED, anchor="lm")
    x += 16
    d.text((x, y), "ism2411-lab14", font=fb, fill=GH_LINK, anchor="lm")
    x += fb.getlength("ism2411-lab14") + 12
    fs = sans(12)
    bw = fs.getlength("Public") + 18
    d.rounded_rectangle([x, y - 10, x + bw, y + 10], radius=10, outline=GH_BORDER)
    d.text((x + bw / 2, y), "Public", font=fs, fill=GH_MUTED, anchor="mm")
    y += 32
    d.line([(0, y), (w, y)], fill=GH_BORDER)
    y += 20
    bh = 32
    if folder:
        fx = pad
        for i, part in enumerate(("ism2411-lab14", "ism2411-lab14")):
            ff = sans(16, i == 1)
            d.text((fx, y + bh / 2), part, font=ff, fill=GH_LINK if i == 0 else GH_TEXT, anchor="lm")
            fx += ff.getlength(part) + 7
            d.text((fx, y + bh / 2), "/", font=sans(16), fill=GH_MUTED, anchor="lm")
            fx += 16
    else:
        gh_btn(d, (pad, y, pad + 92, y + bh), "main")
    code_box = (w - pad - 88, y, w - pad, y + bh)
    add_box = (code_box[0] - 112, y, code_box[0] - 8, y + bh)
    gh_btn(d, add_box, "Add file")
    gh_btn(d, code_box, "Code", primary=True)
    R["add_file"] = add_box
    y += bh + 16
    tx0, tx1 = pad, w - pad
    head_h, row_h = 46, 40
    th = head_h + row_h * len(rows)
    d.rounded_rectangle([tx0, y, tx1, y + th], radius=6, fill=(255, 255, 255), outline=GH_BORDER)
    d.rounded_rectangle([tx0, y, tx1, y + head_h], radius=6, fill=GH_HEAD, outline=GH_BORDER, corners=(True, True, False, False))
    d.ellipse([tx0 + 14, y + 13, tx0 + 34, y + 33], fill=(175, 184, 193))
    fu = sans(14, True)
    d.text((tx0 + 44, y + 23), "YOURUSERNAME", font=fu, fill=GH_TEXT, anchor="lm")
    d.text((tx0 + 54 + fu.getlength("YOURUSERNAME"), y + 23), last_msg, font=sans(14), fill=GH_MUTED, anchor="lm")
    if commits:
        d.text((tx1 - 16, y + 23), commits, font=fu, fill=GH_TEXT, anchor="rm")
        clock(d, tx1 - 30 - fu.getlength(commits), y + 23)
    for i, (kind, name, msg, when) in enumerate(rows):
        ry = y + head_h + i * row_h
        if i:
            d.line([(tx0 + 1, ry), (tx1 - 1, ry)], fill=(216, 222, 228))
        if hover == name:
            d.rectangle([tx0 + 1, ry + 1, tx1 - 1, ry + row_h - 1], fill=(246, 248, 250))
        ix = tx0 + 16
        (gh_folder if kind == "dir" else gh_file)(d, ix, ry + row_h / 2)
        d.text((ix + 28, ry + row_h / 2), name, font=sans(14), fill=GH_LINK if hover == name else GH_TEXT, anchor="lm")
        d.text((tx0 + int((tx1 - tx0) * 0.42), ry + row_h / 2), msg, font=sans(14), fill=GH_MUTED, anchor="lm")
        d.text((tx1 - 16, ry + row_h / 2), when, font=sans(14), fill=GH_MUTED, anchor="rm")
        R["row:" + name] = (tx0, ry, tx1, ry + row_h)
    R["table"] = (tx0, y, tx1, y + th)
    y += th + 18
    if readme:
        rh = 156
        d.rounded_rectangle([tx0, y, tx1, y + rh], radius=6, outline=GH_BORDER)
        d.text((tx0 + 16, y + 20), "README", font=sans(14, True), fill=GH_TEXT, anchor="lm")
        d.line([(tx0, y + 40), (tx1, y + 40)], fill=GH_BORDER)
        d.text((tx0 + 20, y + 68), "ISM2411 Lab 14 — Clean a Messy Sales CSV", font=sans(22, True), fill=GH_TEXT, anchor="lm")
        d.line([(tx0 + 20, y + 90), (tx1 - 20, y + 90)], fill=(216, 222, 228))
        d.text((tx0 + 20, y + 110), "Your Name", font=sans(14), fill=GH_TEXT, anchor="lm")
        d.text((tx0 + 20, y + 134), "python3 clean.py", font=mono(13), fill=GH_TEXT, anchor="lm")
    return im, R


@lru_cache(maxsize=128)
def gh_upload(w, drag_over=False, files=(), progress=1.0, pressed=False):
    im, d = new_page(w)
    pad = 28 if w > 900 else 22
    R = {}
    y = 30
    f = sans(18)
    d.text((pad, y), "ism2411-lab14", font=f, fill=GH_LINK, anchor="lm")
    d.text((pad + f.getlength("ism2411-lab14") + 8, y), "/", font=f, fill=GH_MUTED, anchor="lm")
    y += 34
    zh = 220 if not files else 132
    zone = (pad, y, w - pad, y + zh)
    if drag_over:
        d.rounded_rectangle(zone, radius=10, fill=GH_BLUE_BG)
        dashed(d, zone, GH_LINK)
    else:
        dashed(d, zone, (175, 184, 193))
    zx, zy = w / 2, y + zh / 2
    if not files:
        file_icon(d, zx - 26, zy - 76, 30)
        file_icon(d, zx - 6, zy - 68, 30)
        ty = zy + 16
    else:
        ty = zy - 10
    msg = "Drop to upload your files" if drag_over else "Drag files here to add them to your repository"
    d.text((zx, ty), msg, font=sans(19, True), fill=GH_TEXT, anchor="mm")
    if not drag_over:
        fo = sans(15)
        a, b = "Or ", "choose your files"
        sx = zx - fo.getlength(a + b) / 2
        d.text((sx, ty + 30), a, font=fo, fill=GH_MUTED, anchor="lm")
        d.text((sx + fo.getlength(a), ty + 30), b, font=fo, fill=GH_LINK, anchor="lm")
    R["zone"] = zone
    y += zh + 18
    n = len(files)
    for i, path in enumerate(files):
        ry = y + i * 38
        gh_file(d, pad + 6, ry + 19)
        d.text((pad + 32, ry + 19), path, font=sans(15), fill=GH_TEXT, anchor="lm")
        bx1 = w - pad - 8
        bx0 = bx1 - 150
        p = clamp(progress * n - i)
        d.rounded_rectangle([bx0, ry + 15, bx1, ry + 23], radius=4, fill=(234, 238, 242))
        if p > 0:
            d.rounded_rectangle([bx0, ry + 15, bx0 + max(8, (bx1 - bx0) * p), ry + 23], radius=4, fill=GH_GREEN)
        if i < n - 1:
            d.line([(pad, ry + 38), (w - pad, ry + 38)], fill=(234, 238, 242))
    if n:
        R["list"] = (pad, y, w - pad, y + n * 38)
    y += n * 38 + (28 if n else 10)
    R["form_top"] = y
    d.text((pad, y + 12), "Commit changes", font=sans(20, True), fill=GH_TEXT, anchor="lm")
    y += 40
    R["msg"] = (pad, y, w - pad, y + 38)
    d.rounded_rectangle(R["msg"], radius=6, outline=GH_BORDER, fill=(255, 255, 255))
    d.text((pad + 12, y + 19), "Add files via upload", font=sans(15), fill=(110, 119, 129), anchor="lm")
    y += 52
    d.rounded_rectangle([pad, y, w - pad, y + 92], radius=6, outline=GH_BORDER, fill=(255, 255, 255))
    d.text((pad + 12, y + 20), "Add an optional extended description…", font=sans(15), fill=(110, 119, 129), anchor="lm")
    y += 110
    d.ellipse([pad, y, pad + 16, y + 16], outline=GH_LINK, width=5)
    d.text((pad + 26, y + 8), "Commit directly to the main branch.", font=sans(15), fill=GH_TEXT, anchor="lm")
    y += 36
    R["commit"] = (pad, y, pad + 160, y + 36)
    gh_btn(d, R["commit"], "Commit changes", primary=True, caret=False, pressed=pressed)
    gh_btn(d, (pad + 172, y, pad + 252, y + 36), "Cancel", caret=False)
    return im, R


@lru_cache(maxsize=64)
def gh_commits(w, entries, new_p=1.0, fresh=False):
    im, d = new_page(w, 900)
    pad = 28
    R = {}
    y = 34
    d.text((pad, y), "Commits", font=sans(24, True), fill=GH_TEXT, anchor="lm")
    y += 34
    gh_btn(d, (pad, y, pad + 92, y + 32), "main")
    y += 52
    row_h = 64
    R["box"] = (pad, y, w - pad, y + row_h * len(entries))
    d.rounded_rectangle(R["box"], radius=6, outline=GH_BORDER)
    for i, (msg, when, sha) in enumerate(entries):
        ry = y + i * row_h
        is_new = fresh and i == 0
        if fresh and i > 0:
            ry -= (1 - new_p) * row_h
        a = int(255 * new_p) if is_new else 255
        if is_new:
            d.rounded_rectangle([pad + 1, ry + 1, w - pad - 1, ry + row_h - 1], radius=5, fill=(255, 248, 197, int(230 * new_p)))
        if i:
            d.line([(pad + 1, ry), (w - pad - 1, ry)], fill=(216, 222, 228))
        d.text((pad + 16, ry + 22), msg, font=sans(16, True), fill=GH_TEXT + (a,), anchor="lm")
        d.ellipse([pad + 16, ry + 37, pad + 32, ry + 53], fill=(175, 184, 193, a))
        d.text((pad + 40, ry + 45), f"YOURUSERNAME committed {when}", font=sans(13), fill=GH_MUTED + (a,), anchor="lm")
        d.text((w - pad - 16, ry + row_h / 2), sha, font=mono(13), fill=GH_MUTED + (a,), anchor="rm")
        R[f"entry{i}"] = (pad, ry, w - pad, ry + row_h)
    return im, R


def menu_box(add):
    return (add[2] - 214, add[3] + 6, add[2], add[3] + 6 + 84)


def menu_item(menu, i):
    return (menu[0] + 6, menu[1] + 6 + i * 36, menu[2] - 6, menu[1] + 6 + (i + 1) * 36)


def draw_menu(d, menu, hover=None):
    x0, y0, x1, y1 = menu
    d.rounded_rectangle([x0 + 2, y0 + 5, x1 + 2, y1 + 6], radius=10, fill=(0, 0, 0, 40))
    d.rounded_rectangle(menu, radius=10, fill=(255, 255, 255), outline=GH_BORDER)
    for i, label in enumerate(("Create new file", "Upload files")):
        it = menu_item(menu, i)
        cy = center(it)[1]
        if hover == i:
            d.rounded_rectangle(it, radius=6, fill=(234, 238, 242))
        ix = it[0] + 14
        if i == 0:
            d.line([(ix, cy), (ix + 12, cy)], fill=GH_MUTED, width=2)
            d.line([(ix + 6, cy - 6), (ix + 6, cy + 6)], fill=GH_MUTED, width=2)
        else:
            d.line([(ix + 6, cy - 6), (ix + 6, cy + 4)], fill=GH_MUTED, width=2)
            d.line([(ix + 1, cy - 1), (ix + 6, cy - 6), (ix + 11, cy - 1)], fill=GH_MUTED, width=2)
            d.line([(ix, cy + 7), (ix + 12, cy + 7)], fill=GH_MUTED, width=2)
        d.text((ix + 24, cy), label, font=sans(14), fill=GH_TEXT, anchor="lm")


# ---------------------------------------------------------------- layout

VS_BOX = (48, 28, 880, 566)
FD_BOX = (742, 96, 1232, 406)
FH_POP = (716, 120, 1232, 446)
BR_FULL = (60, 20, 1220, 572)
BR_RIGHT = (452, 20, 1256, 572)
FH_LEFT = (24, 96, 438, 448)
FH_OFF = (-450, 96, -36, 448)


def upload_geom(box, **kw):
    cb = br_cb(box)
    _, R = gh_upload(cb[2] - cb[0], **kw)
    return cb, R


def repo_geom(box, rows, last, commits, **kw):
    cb = br_cb(box)
    _, R = gh_repo(cb[2] - cb[0], rows, last, commits, **kw)
    return cb, R


def scene4_end():
    cb, R = repo_geom(BR_FULL, ROWS_START, "Update README.md", "2 commits")
    return center(menu_item(menu_box(to_screen(R["add_file"], cb)), 1))


def drop_point():
    cb, R = upload_geom(BR_RIGHT)
    return center(to_screen(R["zone"], cb))


def commit_scroll():
    cb, R = upload_geom(BR_FULL, files=UPLOAD_FILES, progress=1.0)
    target = R["form_top"] - 20
    return cb, R, target


# ---------------------------------------------------------------- scenes


def sc_title(fr, d, t, S, dur):
    spaced(d, (W / 2, 150), "ISM2411 · LABS 11–15 AND THE CAPSTONE", mono(18, True), GOLD, spacing=3, align="center")
    d.text((W / 2, 228), "Upload your lab to GitHub", font=sans(62, True), fill=WHITE, anchor="mm")
    d.text((W / 2, 296), "Drag one folder. No Git commands needed.", font=sans(28), fill=MUTED, anchor="mm")
    bx = (700, 380, 1040, 600)
    win(d, bx, "github.com", title_h=26)
    zone = (728, 424, 1012, 578)
    t0 = S[1][0]
    p = prog(t, t0, t0 + 1.7)
    done = t >= t0 + 1.7
    if done:
        d.rounded_rectangle(zone, radius=10, fill=(220, 252, 231))
        dashed(d, zone, GH_GREEN)
        cx, cy = center(zone)
        d.ellipse([cx - 24, cy - 40, cx + 24, cy + 8], fill=GH_GREEN)
        check(d, cx, cy - 16, s=11, width=5)
        d.text((cx, cy + 34), "ism2411-lab14 uploaded", font=sans(16, True), fill=GH_GREEN, anchor="mm")
    else:
        if p > 0.62:
            d.rounded_rectangle(zone, radius=10, fill=GH_BLUE_BG)
            dashed(d, zone, GH_LINK)
        else:
            dashed(d, zone, (175, 184, 193))
        d.text((870, 501), "Drop it here", font=sans(17, True), fill=GH_MUTED, anchor="mm")
        start, end = (300, 470), (870, 488)
        x, y = lerp_pt(start, end, p)
        y -= math.sin(math.pi * p) * 80
        size = lerp(100, 66, p)
        folder_icon(d, x - size / 2, y - size * 0.39, size)
        f = sans(int(lerp(17, 13, p)))
        lw = f.getlength("ism2411-lab14")
        ly = y + size * 0.39 + 18
        d.rounded_rectangle([x - lw / 2 - 8, ly - 12, x + lw / 2 + 8, ly + 12], radius=6, fill=(10, 132, 255))
        d.text((x, ly), "ism2411-lab14", font=f, fill=(255, 255, 255), anchor="mm")
    a = prog(t, 0, 0.5)
    if a < 1:
        d.rectangle([0, 0, W, H], fill=BG + (int(255 * (1 - a)),))


def sc_folder(fr, d, t, S, dur):
    rows = vscode(d, VS_BOX, TREE_1, t=t)
    if S[0][0] + 0.2 < t < S[1][0] - 0.15:
        ring(d, rows["header"], t)
    elif t >= S[1][0] - 0.15:
        a, b = rows["data"], rows["clean.py"]
        ring(d, (a[0] + 4, a[1], b[2] - 4, b[3]), t)


def sc_download(fr, d, t, S, dur):
    s1 = S[1][0]
    t_press, t_drop = s1 + 0.55, s1 + 2.0
    cells = finder_cells(FD_BOX, DL_ITEMS)
    rows = vscode_rows(VS_BOX, TREE_1)
    src = cells["messy_sales.csv"]["center"]
    dst = center(rows["data"])
    pos = along(t, [(s1 - 0.4, (560, 300)), (t_press - 0.05, src), (t_drop, dst), (t_drop + 0.6, (dst[0] + 60, dst[1] + 90))])
    dragging = t_press <= t < t_drop
    over = dragging and point_in(pos, rows["data"])
    dropped = t >= t_drop
    flash = ("messy_sales.csv", 1 - clamp((t - t_drop - 0.3) / 1.5)) if dropped else None
    vscode(d, VS_BOX, TREE_2 if dropped else TREE_1, drop_row="data" if over else None, flash=flash, t=t)
    finder(d, FD_BOX, "Downloads", DL_ITEMS, selected="messy_sales.csv" if t >= t_press - 0.05 else None, side_sel="Downloads")
    if S[0][0] + 1.4 < t < t_press - 0.15:
        ring(d, cells["messy_sales.csv"]["rect"], t)
    if dragging:
        ghost(fr, CSV_GHOST, pos)
    ripple(d, src, t - t_press)
    draw_cursor(fr, pos)


def sc_find(fr, d, t, S, dur):
    s1, s2, s3 = S[1][0], S[2][0], S[3][0]
    term = [("cmd", "~/ism2411-lab14 ", typed("cd ~", t, s1 + 0.2, s1 + 0.7), None, t < s1 + 0.8)]
    if t >= s1 + 0.8:
        term.append(("cmd", "~ ", typed("open .", t, s1 + 1.0, s1 + 1.6), ("Mac", GOLD) if t >= s1 + 1.8 else None, t < s2 + 0.1))
    if t >= s2 + 0.1:
        term.append(("comment", "# or, on Windows:"))
        term.append(("cmd", "~ ", typed("explorer.exe .", t, s2 + 0.5, s2 + 1.6), ("Windows", BLUE) if t >= s2 + 1.8 else None, t < s3))
    flash = ("clean_sales.csv", 1 - clamp((t - 0.6) / 1.8)) if t < 2.4 else None
    vscode(d, VS_BOX, TREE_3, term=term, flash=flash, t=t)
    if t >= s3:
        finder(d, scale_box(FH_POP, lerp(0.9, 1.0, prog(t, s3, s3 + 0.3))), "Home", HOME_ITEMS, side_sel="Home")
        if t >= s3 + 0.8:
            ring(d, finder_cells(FH_POP, HOME_ITEMS)["ism2411-lab14"]["rect"], t)


def sc_repo(fr, d, t, S, dur):
    cb, R = repo_geom(BR_FULL, ROWS_START, "Update README.md", "2 commits")
    add = to_screen(R["add_file"], cb)
    menu = menu_box(add)
    up_item = menu_item(menu, 1)
    s1 = S[1][0]
    t_c1, t_c2 = s1 + 0.75, s1 + 1.75
    pos = along(t, [(s1 - 0.2, (720, 330)), (t_c1 - 0.05, center(add)), (t_c1 + 0.3, center(add)), (t_c2 - 0.05, center(up_item))])
    if t < t_c2 + 0.12:
        browser(d, BR_FULL, URL_REPO, TAB)
        page, _ = gh_repo(cb[2] - cb[0], ROWS_START, "Update README.md", "2 commits")
        paste_page(fr, cb, page)
        if S[0][0] + 0.8 < t < t_c1 - 0.1:
            ring(d, add, t)
        if t >= t_c1:
            draw_menu(d, menu, hover=1 if point_in(pos, up_item) else None)
    else:
        browser(d, BR_FULL, URL_UPLOAD, TAB)
        page, _ = gh_upload(cb[2] - cb[0])
        paste_page(fr, cb, page)
    ripple(d, center(add), t - t_c1)
    ripple(d, center(up_item), t - t_c2)
    draw_cursor(fr, pos)


def sc_drag(fr, d, t, S, dur):
    p = prog(t, S[0][0], S[0][0] + 0.9)
    brb, fhb = lerp_box(BR_FULL, BR_RIGHT, p), lerp_box(FH_OFF, FH_LEFT, p)
    cb = br_cb(brb)
    s1 = S[1][0]
    t_grab, t_drop = s1 + 0.7, s1 + 2.3
    cbF, RF = upload_geom(BR_RIGHT)
    zone = to_screen(RF["zone"], cbF)
    cells = finder_cells(FH_LEFT, HOME_ITEMS)
    src, dst = cells["ism2411-lab14"]["center"], center(zone)
    pos = along(t, [(S[0][0] + 0.9, scene4_end()), (t_grab - 0.05, src), (t_drop, dst), (t_drop + 0.6, (dst[0] + 120, dst[1] + 150))])
    dragging = t_grab <= t < t_drop
    over = dragging and point_in(pos, zone)
    dropped = t >= t_drop
    progress = round(clamp((t - t_drop - 0.15) / 1.3), 2) if dropped else 0.0
    browser(d, brb, URL_UPLOAD, TAB)
    page, R = gh_upload(cb[2] - cb[0], drag_over=over, files=UPLOAD_FILES if dropped else (), progress=progress)
    paste_page(fr, cb, page)
    finder(d, fhb, "Home", HOME_ITEMS, selected="ism2411-lab14" if t >= t_grab - 0.05 else None, side_sel="Home")
    if s1 - 0.3 < t < t_grab - 0.15:
        ring(d, cells["ism2411-lab14"]["rect"], t)
    if dropped and t >= S[2][0] - 0.2 and "list" in R:
        ring(d, to_screen(R["list"], cb), t, color=GREEN)
    if dragging:
        ghost(fr, FOLDER_GHOST, pos)
    ripple(d, src, t - t_grab)
    draw_cursor(fr, pos)


def sc_commit(fr, d, t, S, dur):
    p = prog(t, 0.0, 0.6)
    brb, fhb = lerp_box(BR_RIGHT, BR_FULL, p), lerp_box(FH_LEFT, FH_OFF, p)
    cb = br_cb(brb)
    cbF, RF, target = commit_scroll()
    scroll = int(lerp(0, target, prog(t, 0.6, 1.5)))
    s1 = S[1][0]
    t_click = s1 + 1.1
    browser(d, brb, URL_UPLOAD, TAB)
    page, _ = gh_upload(cb[2] - cb[0], files=UPLOAD_FILES, progress=1.0, pressed=t >= t_click)
    paste_page(fr, cb, page, scroll)
    if fhb[2] > 0:
        finder(d, fhb, "Home", HOME_ITEMS, selected="ism2411-lab14", side_sel="Home")
    msg = to_screen(RF["msg"], cbF, target)
    btn = to_screen(RF["commit"], cbF, target)
    if 1.6 < t < s1:
        ring(d, msg, t)
    start = (drop_point()[0] + 120, drop_point()[1] + 150)
    pos = along(t, [(s1 - 0.1, start), (t_click - 0.05, center(btn))])
    ripple(d, center(btn), t - t_click)
    draw_cursor(fr, pos)


def sc_check(fr, d, t, S, dur):
    cb, RA = repo_geom(BR_FULL, ROWS_AFTER, "Add files via upload", "3 commits")
    row = to_screen(RA["row:ism2411-lab14"], cb)
    s1, s2 = S[1][0], S[2][0]
    t_click = s1 + 0.9
    cbF, RF, target = commit_scroll()
    start = center(to_screen(RF["commit"], cbF, target))
    target_pt = (row[0] + 110, center(row)[1])
    pos = along(t, [(s1 - 0.1, start), (t_click - 0.05, target_pt)])
    w = cb[2] - cb[0]
    if t < t_click + 0.12:
        browser(d, BR_FULL, URL_REPO, TAB)
        page, _ = gh_repo(w, ROWS_AFTER, "Add files via upload", "3 commits", hover="ism2411-lab14" if point_in(pos, row) else None)
        paste_page(fr, cb, page)
        if S[0][0] + 0.4 < t < s1 + 0.3:
            ring(d, row, t)
    else:
        browser(d, BR_FULL, URL_FOLDER, TAB)
        page, R = gh_repo(w, ROWS_FOLDER, "Add files via upload", "", folder=True, readme=False)
        paste_page(fr, cb, page)
        if t >= s2 - 0.3:
            tbl = to_screen(R["table"], cb)
            ring(d, tbl, t, color=GREEN)
            badge(d, tbl[0], tbl[3] + 24, "This is what your instructor expects", alpha=prog(t, s2 - 0.3, s2))
    ripple(d, target_pt, t - t_click)
    draw_cursor(fr, pos)


def sc_repeat(fr, d, t, S, dur):
    cb = br_cb(BR_FULL)
    w = cb[2] - cb[0]
    t_new = S[0][0] + 1.3
    browser(d, BR_FULL, URL_COMMITS, TAB)
    if t < t_new:
        page, R = gh_commits(w, COMMITS)
    else:
        page, R = gh_commits(w, (NEW_COMMIT,) + COMMITS, round(prog(t, t_new, t_new + 0.7), 2), True)
    paste_page(fr, cb, page)
    if t >= S[1][0] - 0.2:
        ring(d, to_screen(R["box"], cb), t)


def card(d, box, alpha=1.0):
    a = int(255 * alpha)
    x0, y0, x1, y1 = box
    d.rounded_rectangle([x0 - 2, y0 + 6, x1 + 2, y1 + 10], radius=14, fill=(0, 0, 0, int(70 * alpha)))
    d.rounded_rectangle(box, radius=12, fill=(255, 255, 255, a), outline=GH_BORDER + (a,))
    return a


def sc_submit(fr, d, t, S, dur):
    cb, R = repo_geom(BR_FULL, ROWS_AFTER, "Add files via upload", "4 commits")
    s0, s1, s2 = S[0][0], S[1][0], S[2][0]
    browser(d, BR_FULL, URL_REPO, TAB, private=True)
    page, _ = gh_repo(cb[2] - cb[0], ROWS_AFTER, "Add files via upload", "4 commits")
    paste_page(fr, cb, page)
    if s0 + 1.0 <= t < s2:
        msg = "You can see it, so your instructor can too"
        bw = sans(15, True).getlength(msg) + 54
        badge(d, cb[2] - bw - 28, cb[1] + 12, msg, alpha=prog(t, s0 + 1.0, s0 + 1.3))
    if s1 <= t < s2:
        a = card(d, (690, 170, 1190, 400), prog(t, s1, s1 + 0.3))
        d.text((722, 230), "404", font=sans(56, True), fill=GH_TEXT + (a,), anchor="lm")
        d.text((860, 220), "See a 404 page instead?", font=sans(18, True), fill=GH_TEXT + (a,), anchor="lm")
        d.text((860, 246), "Your repo is Private.", font=sans(15), fill=GH_MUTED + (a,), anchor="lm")
        steps = ("On GitHub, open Settings → General,", "scroll to Danger Zone, click", "Change visibility, and pick Public.")
        for i, line in enumerate(steps):
            text(d, (722, 300 + i * 26), line, sans(16), GH_TEXT + (a,))
    if t >= s2:
        k = prog(t, s2, s2 + 0.3)
        d.rectangle([0, 0, W, BAND_Y], fill=(0, 0, 0, int(110 * k)))
        a = card(d, (230, 150, 1050, 470), k)
        d.text((270, 196), "Canvas", font=sans(15, True), fill=(80, 90, 104, a), anchor="lm")
        d.text((270, 236), "Lab 14 · Submit Assignment", font=sans(26, True), fill=GH_TEXT + (a,), anchor="lm")
        d.line([(270, 266), (1010, 266)], fill=GH_BORDER + (a,))
        d.text((270, 300), "Website URL", font=sans(15, True), fill=GH_TEXT + (a,), anchor="lm")
        field = (270, 320, 1010, 362)
        d.rounded_rectangle(field, radius=6, fill=(255, 255, 255, a), outline=(140, 150, 160, a))
        if t >= s2 + 0.7:
            url = "https://" + URL_REPO
            d.text((284, 341), url, font=sans(16), fill=GH_TEXT + (a,), anchor="lm")
            cx = 284 + sans(16).getlength(url) + 3
            if int(t * 2.5) % 2 == 0:
                d.line([(cx, 330), (cx, 352)], fill=GH_TEXT + (a,), width=2)
        btn = (790, 392, 1010, 436)
        pressed = t >= S[2][1] + 0.25
        d.rounded_rectangle(btn, radius=6, fill=((2, 92, 145) if pressed else (3, 116, 181)) + (a,))
        d.text(center(btn), "Submit Assignment", font=sans(16, True), fill=(255, 255, 255, a), anchor="mm")
        pos = along(t, [(s2 + 0.1, (700, 520)), (s2 + 0.55, center(field)), (S[2][1] + 0.2, center(btn))])
        ripple(d, center(field), t - (s2 + 0.6))
        ripple(d, center(btn), t - (S[2][1] + 0.25))
        draw_cursor(fr, pos)


def sc_end(fr, d, t, S, dur):
    spaced(d, (W / 2, 104), "THAT'S IT", mono(18, True), GOLD, spacing=3, align="center")
    d.text((W / 2, 166), "Drag one folder.", font=sans(54, True), fill=WHITE, anchor="mm")
    items = (
        "Find your folder: `cd ~`, then `open .` (Mac) or `explorer.exe .` (Windows)",
        "On your repo page: Add file → Upload files, then drag the whole folder in",
        "Click Commit changes. The default message is fine.",
        "Check it in a private window, then paste the URL into Canvas",
    )
    x0 = 190
    for i, s in enumerate(items):
        y = 262 + i * 66
        d.ellipse([x0, y - 19, x0 + 38, y + 19], fill=GOLD)
        d.text((x0 + 19, y), str(i + 1), font=sans(20, True), fill=(20, 20, 24), anchor="mm")
        rich(d, (x0 + 58, y), s, 24, WHITE)
        a = prog(t, 0.3 + i * 0.3, 0.7 + i * 0.3)
        if a < 1:
            d.rectangle([x0 - 4, y - 26, W - 60, y + 26], fill=BG + (int(255 * (1 - a)),))
    foot = "Stuck? The setup section in Lab 11 has hints for the usual problems."
    d.text((W / 2, 556), foot, font=sans(22), fill=MUTED, anchor="mm")
    spaced(d, (W / 2, 640), "ISM2411 · PYTHON FOR BUSINESS", mono(15, True), DIM, spacing=3, align="center")
    a = prog(t, dur - 0.8, dur)
    if a > 0:
        d.rectangle([0, 0, W, H], fill=BG + (int(255 * a),))


def caption_band(d, eyebrow, caption):
    d.rectangle([0, BAND_Y, W, H], fill=BAND)
    d.line([(0, BAND_Y), (W, BAND_Y)], fill=(38, 44, 62))
    d.rectangle([56, BAND_Y + 30, 60, BAND_Y + 102], fill=GOLD)
    spaced(d, (78, BAND_Y + 40), eyebrow, mono(15, True), GOLD, spacing=2)
    rich(d, (78, BAND_Y + 84), caption, 28, WHITE)
    spaced(d, (W - 56, BAND_Y + 40), "ISM2411", mono(14, True), DIM, spacing=2, align="right")


# ---------------------------------------------------------------- script

SCENES = [
    dict(key="title", draw=sc_title, band=None, chapter="Your lab folder",
         say=["Here's the easiest way to get a lab onto GitHub.", "You drag one folder into your browser."],
         extra={1: 0.9}),
    dict(key="folder", draw=sc_folder, band=("YOUR LAB FOLDER", "Each lab lives in one folder, such as `ism2411-lab14`"),
         say=["Each lab lives in one folder on your laptop.", "For Lab 14, it holds your script and a data folder."]),
    dict(key="download", draw=sc_download, band=("DATA FILES", "Drag the CSV from Downloads onto the `data` folder in VS Code"),
         say=["When a lab gives you a CSV file, your browser saves it in your Downloads folder.",
              "Drag it onto the data folder in VS Code's sidebar, and VS Code copies it in."],
         extra={1: 0.8}),
    dict(key="find", draw=sc_find, chapter="Find your folder",
         band=("STEP 1 · FIND YOUR FOLDER", "In VS Code's terminal: `cd ~`, then `open .` (Mac) or `explorer.exe .` (Windows)"),
         say=["Finished an exercise or two? Time to upload.",
              "In VS Code's terminal, type the two commands on the screen.",
              "The second one is different on a Mac and on Windows.",
              "A window opens on your home folder, and your lab folder is right there."],
         extra={1: 0.6, 2: 0.8, 3: 0.8}),
    dict(key="repo", draw=sc_repo, chapter="Upload the whole folder",
         band=("STEP 2 · OPEN THE UPLOAD PAGE", "On your repo page, click Add file → Upload files"),
         say=["Now open your repo on GitHub.", "Click Add file, then Upload files."], extra={1: 0.8}),
    dict(key="drag", draw=sc_drag, band=("STEP 3 · DRAG THE WHOLE FOLDER", "Drag your whole `ism2411-lab14` folder onto the box"),
         say=["Put the two windows side by side.", "Drag your whole lab folder onto the box, and let go.",
              "GitHub lists every file inside it."], extra={0: 0.4, 1: 0.5, 2: 0.8}),
    dict(key="commit", draw=sc_commit, chapter="Commit and check",
         band=("STEP 4 · COMMIT", "Click Commit changes. The default message is fine."),
         say=["Scroll down. GitHub's default message is fine.", "Click the green Commit changes button."], extra={0: 0.3, 1: 0.8}),
    dict(key="check", draw=sc_check, band=("STEP 5 · CHECK", "Your lab folder sits next to `README.md`, with your files inside"),
         say=["Your repo now shows your lab folder next to the readme.",
              "Click it to check that your script and data folder are inside.",
              "That's exactly what your instructor expects."], extra={1: 0.3, 2: 0.8}),
    dict(key="repeat", draw=sc_repeat, chapter="Upload again, check, submit",
         band=("EVERY EXERCISE OR TWO", "Drag the same folder again. Every upload is saved."),
         say=["After each exercise or two, drag the same folder in again.",
              "Files with the same name are replaced, and every upload is saved in your history."], extra={1: 0.5}),
    dict(key="submit", draw=sc_submit, band=("BEFORE YOU SUBMIT", "Check it in a private window, then paste the URL into Canvas"),
         say=["Before you submit, open your repo in a private window.",
              ("If you see a four oh four page, your repo is private. Switch it to Public in Settings.",
               "If you see a 404 page, your repo is private. Switch it to Public in Settings."),
              "Then paste your repo's address into Canvas."], extra={1: 0.6, 2: 1.0}),
    dict(key="end", draw=sc_end, band=None,
         say=["That's it. If anything goes wrong, the setup section in Lab 11 has hints for the usual problems."],
         extra={0: 1.6}),
]

LEAD, GAP, TAIL = 0.5, 0.35, 0.7


def synth_all(voice_path, cache_dir):
    from piper import PiperVoice, SynthesisConfig

    voice = PiperVoice.load(str(voice_path))
    cfg = SynthesisConfig(length_scale=1.08)
    sr = voice.config.sample_rate
    cache_dir.mkdir(parents=True, exist_ok=True)
    for sc in SCENES:
        sc["lines"] = []
        for item in sc["say"]:
            spoken, shown = (item, item) if isinstance(item, str) else item
            key = hashlib.sha1(f"{voice_path.name}|1.08|{spoken}".encode()).hexdigest()[:16]
            path = cache_dir / f"{key}.npy"
            if path.exists():
                audio = np.load(path)
            else:
                bio = io.BytesIO()
                with wave.open(bio, "wb") as wf:
                    voice.synthesize_wav(spoken, wf, syn_config=cfg)
                bio.seek(0)
                with wave.open(bio, "rb") as rf:
                    audio = np.frombuffer(rf.readframes(rf.getnframes()), dtype=np.int16).copy()
                np.save(path, audio)
            sc["lines"].append((spoken, shown, audio))
    return sr


def plan_timing(sr):
    start_frames = 0
    for sc in SCENES:
        t = LEAD
        sc["S"] = []
        for i, (_, _, audio) in enumerate(sc["lines"]):
            n = len(audio) / sr
            sc["S"].append((t, t + n))
            t += n + GAP + sc.get("extra", {}).get(i, 0.0)
        sc["frames"] = round((t - GAP + TAIL) * FPS)
        sc["dur"] = sc["frames"] / FPS
        sc["start"] = start_frames / FPS
        start_frames += sc["frames"]
    return start_frames


def render(sc, t):
    fr = Image.new("RGB", (W, H), BG)  # RGB + an RGBA Draw = translucent fills blend
    d = ImageDraw.Draw(fr, "RGBA")
    sc["draw"](fr, d, t, sc["S"], sc["dur"])
    if sc["band"]:
        caption_band(d, *sc["band"])
    return fr


def stamp(sec, srt=True):
    ms = round(sec * 1000)
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}" if srt else f"{m}:{s:02}"


def write_text_outputs(out):
    srt, n = [], 1
    for sc in SCENES:
        for (_, shown, _), (a, b) in zip(sc["lines"], sc["S"]):
            srt.append(f"{n}\n{stamp(sc['start'] + a)} --> {stamp(sc['start'] + b + 0.25)}\n{shown}\n")
            n += 1
    (out / "upload_whole_folder.srt").write_text("\n".join(srt))
    total = sum(sc["dur"] for sc in SCENES)
    chapters = [f"{stamp(sc['start'], False)} {sc['chapter']}" for sc in SCENES if sc.get("chapter")]
    md = [
        "# Upload Your Lab to GitHub: Drag One Folder (ISM2411)",
        "",
        f"Built by `_make_upload_video.py` (parent repo). Length {stamp(total, False)}. "
        "Narration is a local piper voice (en_US-lessac-medium); the on-screen screens are simplified drawings "
        "of VS Code, Finder / File Explorer, GitHub's upload page and Canvas with the real button labels. "
        "Example lab: Lab 14 (`ism2411-lab14`: `clean.py` and `data/`).",
        "",
        "Goes in: ISM2411 Lab 11 `#repo-setup` (the hub the later labs link to), and optionally the upload line "
        "of Labs 14–15 and the capstone. Inline short-video pattern: a `<strong>Watch it (N minutes):</strong>` "
        "caption paragraph + `video-embed`, no Lab Walkthrough divider.",
        "",
        "## YouTube",
        "",
        "**Title:** Upload Your Lab to GitHub: Drag One Folder (ISM2411)",
        "",
        "**Description:**",
        "",
        "```",
        "The easiest way to get an ISM2411 lab onto GitHub: drag your whole lab folder into the browser. "
        "No Git commands needed. Works for Labs 11-15 and the capstone.",
        "",
        "Hints for the usual problems (Lab 11 setup):",
        LAB_PAGE,
        "",
        *chapters,
        "```",
        "",
        "Upload `upload_whole_folder.srt` as the English subtitles.",
        "",
        "## Script",
        "",
    ]
    for i, sc in enumerate(SCENES):
        head = sc["band"][0].title() if sc["band"] else ("Title" if i == 0 else "End card")
        md.append(f"### {stamp(sc['start'], False)} · {head}")
        md.append("")
        if sc["band"]:
            md.append(f"On screen: {sc['band'][1]}")
            md.append("")
        for spoken, shown, _ in sc["lines"]:
            md.append(f"> {shown}")
        md.append("")
    (out / "upload_whole_folder.md").write_text("\n".join(md))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out", type=Path)
    ap.add_argument("--voice", type=Path, required=True)
    ap.add_argument("--preview", action="store_true")
    args = ap.parse_args()
    out = args.out
    out.mkdir(parents=True, exist_ok=True)
    sr = synth_all(args.voice, out / ".tts_cache")
    total_frames = plan_timing(sr)
    write_text_outputs(out)
    if args.preview:
        pv = out / "preview"
        pv.mkdir(exist_ok=True)
        for i, sc in enumerate(SCENES):
            times = []
            for a, b in sc["S"]:
                times += [a + 0.05, (a + b) / 2, b]
            times += [sc["dur"] - 0.05]
            times = times[:8]
            sheet = Image.new("RGB", (1280, 360 * ((len(times) + 1) // 2)), (0, 0, 0))
            for k, tt in enumerate(times):
                sheet.paste(render(sc, tt).resize((640, 360)), ((k % 2) * 640, (k // 2) * 360))
            sheet.save(pv / f"scene_{i:02}_{sc['key']}.png")
        print(f"preview: {len(SCENES)} sheets in {pv}; total {total_frames / FPS:.1f}s")
        return
    audio = np.zeros(round(total_frames / FPS * sr), dtype=np.int16)
    for sc in SCENES:
        for (_, _, clip), (a, _) in zip(sc["lines"], sc["S"]):
            o = round((sc["start"] + a) * sr)
            audio[o:o + len(clip)] = (clip[: max(0, len(audio) - o)] * 0.89).astype(np.int16)  # -1 dB: AAC headroom
    wav_path = out / ".narration.wav"
    with wave.open(str(wav_path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(audio.tobytes())
    import imageio_ffmpeg

    mp4 = out / "upload_whole_folder.mp4"
    cmd = [imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-loglevel", "error",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-i", str(wav_path), "-c:v", "libx264", "-preset", "slow", "-tune", "animation", "-crf", "18",
           "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-ar", "44100", "-movflags", "+faststart", str(mp4)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for sc in SCENES:
        for k in range(sc["frames"]):
            proc.stdin.write(render(sc, k / FPS).tobytes())
    proc.stdin.close()
    if proc.wait() != 0:
        raise SystemExit("ffmpeg failed")
    print(f"wrote {mp4} ({total_frames / FPS:.1f}s, {mp4.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
