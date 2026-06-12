#!/usr/bin/env python3
"""Render the rubber duck debugging companion infographic (8b) with PIL.

Output:
  infographics/8b Rubber_Duck_Debugging_Guide.png            (1600x900)
  ism2411/assets/img/infographics/08b_rubber_duck_infographic.png
  ism3232/assets/img/infographics/08b_rubber_duck_infographic.png
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path("/home/markumreed/Documents/ism_courses")
S = 2  # supersample factor
W, H = 1600 * S, 900 * S

BG      = "#faf9f4"
INK     = "#1d1d2b"
MUTED   = "#5b5b70"
CARD    = "#ffffff"
BORDER  = "#e3e1d8"
YELLOW  = "#fbbf24"
ORANGE  = "#e8920f"
TEAL    = "#0d9488"
INDIGO  = "#6366f1"
ROSE    = "#e11d48"
TEALBG  = "#e7f6f3"
INDIBG  = "#eceefc"
ROSEBG  = "#fdeaee"

DEJAVU = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(f"{DEJAVU}/{name}.ttf", size * S)


F_TITLE  = font("DejaVuSans-Bold", 52)
F_SUB    = font("DejaVuSans", 21)
F_CITE   = font("DejaVuSans", 16)
F_H      = font("DejaVuSans-Bold", 26)
F_BODY   = font("DejaVuSans", 19)
F_STEPN  = font("DejaVuSans-Bold", 34)
F_LABEL  = font("DejaVuSans-Bold", 15)
F_MONO   = font("DejaVuSansMono", 19)
F_MONO_B = font("DejaVuSansMono-Bold", 19)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)


def wrap(text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def text_block(x, y, text, fnt, fill, max_w, lh):
    for i, line in enumerate(wrap(text, fnt, max_w)):
        d.text((x, y + i * lh * S), line, font=fnt, fill=fill)
    return y + len(wrap(text, fnt, max_w)) * lh * S


def rrect(box, r, fill=None, outline=None, width=1):
    d.rounded_rectangle(box, radius=r * S, fill=fill, outline=outline, width=width * S)


# ── Header ────────────────────────────────────────────────────────────────────
mx = 56 * S
d.text((mx, 44 * S), "Rubber Duck Debugging", font=F_TITLE, fill=INK)
d.text((mx, 116 * S), "Explain your code out loud, one line at a time — the bug often surfaces mid-sentence.",
       font=F_SUB, fill=MUTED)
cite = "From “The Pragmatic Programmer” — Hunt & Thomas, 1999"
cw = d.textlength(cite, font=F_CITE)
rrect((W - mx - cw - 36 * S, 52 * S, W - mx, 92 * S), 20, fill="#f1efe6")
d.text((W - mx - cw - 18 * S, 62 * S), cite, font=F_CITE, fill=MUTED)
d.line((mx, 162 * S, W - mx, 162 * S), fill=BORDER, width=2 * S)

# ── Left panel: duck + why it works ──────────────────────────────────────────
LX, LY, LW2, LH2 = mx, 196 * S, 430 * S, 560 * S
rrect((LX, LY, LX + LW2, LY + LH2), 16, fill=CARD, outline=BORDER, width=2)

# duck pond circle
pcx, pcy, pr = LX + LW2 // 2, LY + 152 * S, 112 * S
d.ellipse((pcx - pr, pcy - pr, pcx + pr, pcy + pr), fill="#fdf3d7")

# duck — body, tail, head, beak, eye, wing
bx, by = pcx - 10 * S, pcy + 30 * S
d.ellipse((bx - 78 * S, by - 48 * S, bx + 78 * S, by + 48 * S), fill=YELLOW)            # body
d.polygon([(bx + 60 * S, by - 10 * S), (bx + 102 * S, by - 52 * S), (bx + 74 * S, by + 14 * S)], fill=YELLOW)  # tail
hx, hy = bx - 44 * S, by - 74 * S
d.ellipse((hx - 46 * S, hy - 46 * S, hx + 46 * S, hy + 46 * S), fill=YELLOW)            # head
d.polygon([(hx - 44 * S, hy + 2 * S), (hx - 88 * S, hy + 10 * S), (hx - 44 * S, hy + 22 * S)], fill=ORANGE)    # beak
d.ellipse((hx - 26 * S, hy - 20 * S, hx - 8 * S, hy - 2 * S), fill=INK)                 # eye
d.ellipse((hx - 21 * S, hy - 16 * S, hx - 14 * S, hy - 9 * S), fill="#ffffff")          # eye glint
d.ellipse((bx - 30 * S, by - 22 * S, bx + 42 * S, by + 26 * S), fill="#f6ad13")         # wing
d.arc((pcx - pr + 14 * S, pcy + 64 * S, pcx + pr - 14 * S, pcy + 110 * S), 200, 340, fill="#e3d9b8", width=4 * S)  # water

# why it works
yy = LY + 296 * S
d.text((LX + 28 * S, yy), "Why talking to a toy works", font=F_H, fill=INK)
yy += 42 * S
yy = text_block(LX + 28 * S, yy,
                "A bug is a gap between what you THINK the code does and what it "
                "ACTUALLY does — and your brain fills that gap with assumptions.",
                F_BODY, MUTED, LW2 - 56 * S, 27)
yy += 10 * S
text_block(LX + 28 * S, yy,
           "Saying each line out loud forces you to state what the code "
           "literally says. The mismatch announces itself.",
           F_BODY, INK, LW2 - 56 * S, 27)

# ── Right: three step cards ───────────────────────────────────────────────────
RX = LX + LW2 + 36 * S
RW = W - mx - RX
steps = [
    (TEAL, TEALBG, "STEP 1", "State the goal",
     "Tell the duck what the code is supposed to do. One sentence."),
    (INDIGO, INDIBG, "STEP 2", "Explain every line",
     "Out loud, in order — what each line LITERALLY does, not what it should do. No skipping the “obvious” lines; that's where bugs hide."),
    (ROSE, ROSEBG, "STEP 3", "Compare",
     "The moment your explanation and the program's actual behavior disagree — that's the bug's address."),
]
sy = 196 * S
sh = 128 * S
for color, cbg, num, head, body in steps:
    rrect((RX, sy, RX + RW, sy + sh), 14, fill=CARD, outline=BORDER, width=2)
    d.rectangle((RX, sy + 14 * S, RX + 8 * S, sy + sh - 14 * S), fill=color)
    rrect((RX + 28 * S, sy + 34 * S, RX + 128 * S, sy + sh - 34 * S), 12, fill=cbg)
    nw = d.textlength(num.split()[1], font=F_STEPN)
    d.text((RX + 78 * S - nw / 2, sy + sh / 2 - 24 * S), num.split()[1], font=F_STEPN, fill=color)
    d.text((RX + 78 * S - d.textlength("STEP", font=F_LABEL) / 2, sy + 16 * S), "STEP", font=F_LABEL, fill=color)
    d.text((RX + 156 * S, sy + 22 * S), head, font=F_H, fill=INK)
    text_block(RX + 156 * S, sy + 60 * S, body, F_BODY, MUTED, RW - 190 * S, 27)
    sy += sh + 22 * S

# ── Speech bubble demo ────────────────────────────────────────────────────────
by0 = sy + 6 * S
bh = 120 * S
rrect((RX, by0, RX + RW, by0 + bh), 14, fill="#fff8e6", outline="#f2dfa8", width=2)
d.polygon([(RX + 4 * S, by0 + 50 * S), (RX - 22 * S, by0 + 70 * S), (RX + 4 * S, by0 + 78 * S)], fill="#fff8e6")
d.text((RX + 28 * S, by0 + 18 * S), "HEARD MID-SENTENCE", font=F_LABEL, fill=ORANGE)
d.text((RX + 28 * S, by0 + 44 * S),
       "“The discount is subtotal × rate… the rate is 1.10 —", font=F_MONO, fill=INK)
d.text((RX + 28 * S, by0 + 76 * S),
       "wait. That's not a discount, that's 110%.”", font=F_MONO_B, fill=ROSE)

# ── Footer band ───────────────────────────────────────────────────────────────
fy = H - 96 * S
d.line((mx, fy - 18 * S, W - mx, fy - 18 * S), fill=BORDER, width=2 * S)
d.text((mx, fy), "Duck didn't crack it?", font=F_H, fill=INK)
text_block(mx + 320 * S, fy + 4 * S,
           "You've lost two minutes and gained a perfectly rehearsed question — paste exactly what you said "
           "into the discussion board, or give it to an AI in Explainer mode.",
           F_BODY, MUTED, W - 2 * mx - 660 * S, 27)
chip = "ISM2411 Module 7  ·  ISM3232 Week 8"
cw2 = d.textlength(chip, font=F_LABEL)
rrect((W - mx - cw2 - 36 * S, fy + 6 * S, W - mx, fy + 44 * S), 19, fill="#f1efe6")
d.text((W - mx - cw2 - 18 * S, fy + 16 * S), chip, font=F_LABEL, fill=MUTED)

# ── Save ──────────────────────────────────────────────────────────────────────
final = img.resize((1600, 900), Image.LANCZOS)
out = ROOT / "infographics" / "8b Rubber_Duck_Debugging_Guide.png"
final.save(out)
for course, sub in [("ism2411", "assets/img/infographics"), ("ism3232", "assets/img/infographics")]:
    dest = ROOT / course / sub / "08b_rubber_duck_infographic.png"
    final.save(dest)
    print(f"wrote {dest}")
print(f"wrote {out}")
