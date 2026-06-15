#!/usr/bin/env python3
"""Punchier YouTube thumbnail variant (v2) for all 33 lecture videos.

Same dark house palette, but bolder: an accent-tinted background, a large
accent badge holding a white per-topic vector icon, a big auto-fit
headline, eyebrow, and Part footer.

Output: ppt/thumbnails_v2/NN_slug.png
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

S = 2
W, H = 1280 * S, 720 * S
BASE, INK, MUTED = (0x14, 0x14, 0x1d), "#ffffff", "#9a9ab0"
DJ = "/usr/share/fonts/truetype/dejavu"
OUT = os.path.join(os.path.dirname(__file__), "thumbnails_v2")

GREEN, BLUE, PURPLE, ROSE, TEAL, INDIGO, GOLD = (
    "#34d399", "#60a5fa", "#c084fc", "#fb7185", "#00c9a7", "#818cf8", "#fbbf24")


def fnt(name, size):
    return ImageFont.truetype(f"{DJ}/{name}.ttf", size * S)


F_EYE = fnt("DejaVuSansMono-Bold", 28)
F_FOOT = fnt("DejaVuSansMono", 24)


def hx(c):
    c = c.lstrip("#")
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


def tint(accent, amt=0.12):
    a, b = hx(accent), BASE
    return tuple(int(b[i] + (a[i] - b[i]) * amt) for i in range(3))


# ---------- icon primitives (normalized 0..1 inside the icon box) ----------
def _xy(box, pts):
    bx, by, bw, bh = box
    return [(bx + px * bw, by + py * bh) for px, py in pts]


def _poly(d, box, pts, lw, col, closed=False):
    xy = _xy(box, pts)
    if closed:
        xy = xy + [xy[0]]
    d.line(xy, fill=col, width=lw, joint="curve")


def _dot(d, box, c, r, col):
    bx, by, bw, bh = box
    cx, cy, rr = bx + c[0] * bw, by + c[1] * bh, r * bw
    d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=col)


def _rect(d, box, p0, p1, lw, col, fill=None):
    bx, by, bw, bh = box
    xy = [bx + p0[0] * bw, by + p0[1] * bh, bx + p1[0] * bw, by + p1[1] * bh]
    d.rectangle(xy, outline=col, width=lw, fill=fill)


def _arc(d, box, p0, p1, a0, a1, lw, col):
    bx, by, bw, bh = box
    d.arc([bx + p0[0] * bw, by + p0[1] * bh, bx + p1[0] * bw, by + p1[1] * bh],
          a0, a1, fill=col, width=lw)


def draw_icon(d, kind, box, lw, col, bold):
    """Draw white topic icon inside box=(x,y,w,h)."""
    def glyph(s, scale=0.92):
        bx, by, bw, bh = box
        gf = fnt("DejaVuSans-Bold", int(bh / S * scale))
        d.text((bx + bw / 2, by + bh / 2), s, font=gf, fill=col, anchor="mm")

    if kind == "braces":
        glyph("{ }", 0.78)
    elif kind == "brackets":
        glyph("[ ]", 0.78)
    elif kind == "func":
        glyph("ƒ()", 0.7)
    elif kind == "fmt":
        glyph("$", 1.0)
    elif kind == "ops":
        glyph("×÷", 0.62)
    elif kind == "prompt":
        glyph(">_", 0.66)
    elif kind == "loop":
        _arc(d, box, (.12, .12), (.88, .88), 300, 210, lw, col)
        head = _xy(box, [(.12, .50), (.30, .40), (.30, .62)])
        d.polygon(head, fill=col)
    elif kind == "branch":
        _dot(d, box, (.5, .15), .09, col)
        _poly(d, box, [(.5, .24), (.5, .5)], lw, col)
        _poly(d, box, [(.5, .5), (.2, .78)], lw, col)
        _poly(d, box, [(.5, .5), (.8, .78)], lw, col)
        _dot(d, box, (.2, .85), .09, col)
        _dot(d, box, (.8, .85), .09, col)
    elif kind == "bug":
        _rect(d, box, (.3, .3), (.7, .8), lw, col)
        _arc(d, box, (.3, .12), (.7, .48), 180, 360, lw, col)
        for y in (.42, .58, .74):
            _poly(d, box, [(.12, y - .06), (.3, y)], lw, col)
            _poly(d, box, [(.7, y), (.88, y - .06)], lw, col)
        _poly(d, box, [(.4, .2), (.34, .06)], lw, col)
        _poly(d, box, [(.6, .2), (.66, .06)], lw, col)
    elif kind == "terminal":
        _rect(d, box, (.08, .16), (.92, .84), lw, col)
        _poly(d, box, [(.22, .42), (.36, .55), (.22, .68)], lw, col)
        _poly(d, box, [(.44, .68), (.66, .68)], lw, col)
    elif kind == "git":
        _dot(d, box, (.25, .2), .09, col)
        _dot(d, box, (.25, .8), .09, col)
        _dot(d, box, (.75, .5), .09, col)
        _poly(d, box, [(.25, .28), (.25, .72)], lw, col)
        _poly(d, box, [(.25, .5), (.66, .5)], lw, col)
        _arc(d, box, (.25, .31), (.85, .69), 270, 360, lw, col)
    elif kind == "ai":
        d.polygon(_xy(box, [(.5, .06), (.6, .4), (.94, .5), (.6, .6), (.5, .94),
                            (.4, .6), (.06, .5), (.4, .4)]), fill=col)
        _dot(d, box, (.84, .18), .055, col)
    elif kind == "gear":
        bx, by, bw, bh = box
        cx, cy, R = bx + bw / 2, by + bh / 2, bw * .34
        for k in range(8):
            ang = k * math.pi / 4
            x0, y0 = cx + math.cos(ang) * R, cy + math.sin(ang) * R
            x1, y1 = cx + math.cos(ang) * (R + bw * .14), cy + math.sin(ang) * (R + bw * .14)
            d.line([x0, y0, x1, y1], fill=col, width=lw)
        d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=col, width=lw)
        d.ellipse([cx - R * .35, cy - R * .35, cx + R * .35, cy + R * .35], outline=col, width=lw)
    elif kind == "chip":
        _rect(d, box, (.26, .26), (.74, .74), lw, col)
        _rect(d, box, (.4, .4), (.6, .6), lw, col)
        for t in (.36, .5, .64):
            _poly(d, box, [(t, .1), (t, .26)], lw, col)
            _poly(d, box, [(t, .74), (t, .9)], lw, col)
            _poly(d, box, [(.1, t), (.26, t)], lw, col)
            _poly(d, box, [(.74, t), (.9, t)], lw, col)
    elif kind == "chart":
        _poly(d, box, [(.14, .12), (.14, .86), (.9, .86)], lw, col)
        for x, h in ((.3, .55), (.48, .35), (.66, .62), (.84, .22)):
            d.rectangle(_xy(box, [(x - .06, h), (x + .06, .86)])[0]
                        + _xy(box, [(x - .06, h), (x + .06, .86)])[1], fill=col)
    elif kind == "funnel":
        _poly(d, box, [(.12, .16), (.88, .16), (.58, .52), (.58, .84),
                       (.42, .74), (.42, .52)], lw, col, closed=True)
    elif kind == "table":
        _rect(d, box, (.12, .16), (.88, .84), lw, col)
        _poly(d, box, [(.12, .39), (.88, .39)], lw, col)
        _poly(d, box, [(.12, .62), (.88, .62)], lw, col)
        _poly(d, box, [(.46, .16), (.46, .84)], lw, col)
    elif kind == "check":
        _poly(d, box, [(.16, .52), (.42, .76), (.86, .24)], lw, col)
    elif kind == "blueprint":
        _rect(d, box, (.12, .12), (.62, .62), lw, col)
        _rect(d, box, (.4, .4), (.88, .88), lw, col)
    elif kind == "database":
        _arc(d, box, (.18, .08), (.82, .32), 0, 360, lw, col)
        _poly(d, box, [(.18, .2), (.18, .8)], lw, col)
        _poly(d, box, [(.82, .2), (.82, .8)], lw, col)
        _arc(d, box, (.18, .38), (.82, .62), 0, 180, lw, col)
        _arc(d, box, (.18, .68), (.82, .92), 0, 180, lw, col)
    elif kind == "browser":
        _rect(d, box, (.1, .16), (.9, .84), lw, col)
        _poly(d, box, [(.1, .34), (.9, .34)], lw, col)
        for x in (.18, .26, .34):
            _dot(d, box, (x, .25), .03, col)
    elif kind == "cube":
        _poly(d, box, [(.5, .1), (.9, .31), (.9, .69), (.5, .9),
                       (.1, .69), (.1, .31)], lw, col, closed=True)
        _poly(d, box, [(.5, .1), (.5, .5)], lw, col)
        _poly(d, box, [(.5, .5), (.9, .31)], lw, col)
        _poly(d, box, [(.5, .5), (.1, .31)], lw, col)
    elif kind == "flag":
        _poly(d, box, [(.26, .1), (.26, .9)], lw, col)
        d.polygon(_xy(box, [(.26, .12), (.82, .26), (.26, .4)]), fill=col)


# (seq, slug, [headline lines], eyebrow, accent, part, icon)
VIDEOS = [
    (1, "variables_data_types", ["Variables &", "Data Types"], "PYTHON · FOUNDATIONS", GREEN, 1, "braces"),
    (2, "python_operators", ["Python", "Operators"], "PYTHON · OPERATORS", BLUE, 1, "ops"),
    (3, "fstrings_formatting", ["f-strings &", "Formatting"], "PYTHON · OUTPUT", BLUE, 1, "fmt"),
    (4, "if_elif_else", ["if / elif", "/ else"], "PYTHON · LOGIC", BLUE, 1, "branch"),
    (5, "for_loops", ["Python", "for Loops"], "PYTHON · ITERATION", GREEN, 1, "loop"),
    (6, "dictionaries", ["Python", "Dictionaries"], "PYTHON · DATA", PURPLE, 1, "braces"),
    (7, "functions", ["Python", "Functions"], "PYTHON · FUNCTIONS", GREEN, 1, "func"),
    (8, "reading_tracebacks", ["Reading", "Tracebacks"], "PYTHON · DEBUGGING", ROSE, 1, "bug"),
    (9, "terminal_basics", ["Terminal", "Basics"], "COMMAND LINE", TEAL, 1, "prompt"),
    (10, "git_basics", ["Git", "Basics"], "VERSION CONTROL", TEAL, 1, "git"),
    (11, "github_workflow", ["GitHub", "Workflow"], "VERSION CONTROL", TEAL, 1, "git"),
    (12, "coding_with_ai", ["Coding", "with AI"], "AI · BEST PRACTICES", GOLD, 1, "ai"),
    (13, "cpu_ram_storage", ["CPU, RAM", "& Storage"], "HOW CODE RUNS", INDIGO, 1, "chip"),
    (14, "python_setup", ["Python", "Setup"], "ENVIRONMENT", TEAL, 1, "gear"),
    (15, "lists_tuples", ["Lists &", "Tuples"], "PYTHON · DATA", PURPLE, 1, "brackets"),
    (16, "csv_file_io", ["CSV", "File I/O"], "DATA PIPELINES", BLUE, 1, "table"),
    (17, "pandas_basics", ["pandas", "Basics"], "DATA ANALYSIS", GOLD, 1, "chart"),
    (18, "data_cleaning", ["Data", "Cleaning"], "DATA ANALYSIS", GOLD, 1, "funnel"),
    (19, "groupby_charts", ["groupby &", "Charts"], "DATA ANALYSIS", GOLD, 1, "chart"),
    (20, "data_project", ["Data Analysis", "Project"], "CAPSTONE", GOLD, 1, "flag"),
    (21, "dev_environment", ["Dev", "Environment"], "SETUP", TEAL, 2, "gear"),
    (22, "advanced_shell", ["Advanced", "Shell Tools"], "COMMAND LINE", TEAL, 2, "prompt"),
    (23, "virtual_environments", ["Virtual", "Environments"], "WORKFLOW", TEAL, 2, "cube"),
    (24, "code_checklist", ["Code", "Checklist"], "WORKFLOW", INDIGO, 2, "check"),
    (25, "while_loops", ["while", "Loops"], "CONTROL FLOW", BLUE, 2, "loop"),
    (26, "testing_pytest", ["Testing", "with pytest"], "TESTING", INDIGO, 2, "check"),
    (27, "classes_oop", ["Classes", "& OOP"], "OOP · PART 1", ROSE, 2, "blueprint"),
    (28, "composition_inheritance", ["Composition", "& Inheritance"], "OOP · PART 2", ROSE, 2, "blueprint"),
    (29, "oop_design", ["OOP", "Design"], "OOP · PART 3", ROSE, 2, "blueprint"),
    (30, "sql_sqlite", ["SQL &", "SQLite"], "DATABASES", TEAL, 2, "database"),
    (31, "python_sqlite", ["Python", "+ SQLite"], "DATABASES", TEAL, 2, "database"),
    (32, "streamlit_app", ["Streamlit", "Web App"], "WEB UI", INDIGO, 2, "browser"),
    (33, "ai_feature", ["AI", "Feature"], "GENERATIVE AI", GOLD, 2, "ai"),
]


def fit_headline(d, lines, max_w):
    for size in range(108, 40, -2):
        f = fnt("DejaVuSans-Bold", size)
        if all(d.textlength(ln, font=f) <= max_w * S for ln in lines):
            return f, size
    return fnt("DejaVuSans-Bold", 40), 40


def make(seq, slug, lines, eyebrow, accent, part, icon):
    img = Image.new("RGB", (W, H), tint(accent))
    d = ImageDraw.Draw(img)
    # left accent bar
    d.rectangle([0, 0, 16 * S, H], fill=accent)
    # badge (right)
    bs = 340 * S
    bx0 = W - 110 * S - bs
    by0 = (H - bs) // 2
    d.rounded_rectangle([bx0, by0, bx0 + bs, by0 + bs], radius=int(bs * .2), fill=accent)
    # icon inside badge
    pad = int(bs * .26)
    ibox = (bx0 + pad, by0 + pad, bs - 2 * pad, bs - 2 * pad)
    lw = max(6 * S, int(bs * .035))
    draw_icon(d, icon, ibox, lw, "#14141d", True)
    # eyebrow
    d.text((96 * S, 120 * S), eyebrow, font=F_EYE, fill=accent, anchor="ls")
    # headline (auto-fit within left column)
    col_w = bx0 / S - 96 - 40
    f, size = fit_headline(d, lines, col_w)
    y = 250
    for ln in lines:
        d.text((92 * S, y * S), ln, font=f, fill=INK, anchor="ls")
        y += int(size * 1.16)
    uy = y - int(size * 0.5)
    d.rectangle([96 * S, uy * S, 300 * S, (uy + 9) * S], fill=accent)
    # footer
    d.text((96 * S, H - 64 * S), f"PYTHON FOR BUSINESS  ·  PART {part}",
           font=F_FOOT, fill=MUTED, anchor="ls")
    img = img.resize((1280, 720), Image.LANCZOS)
    img.save(os.path.join(OUT, f"{seq:02d}_{slug}.png"))


def main():
    os.makedirs(OUT, exist_ok=True)
    for v in VIDEOS:
        make(*v)
    print(f"Generated {len(VIDEOS)} v2 thumbnails in {OUT}")


if __name__ == "__main__":
    main()
