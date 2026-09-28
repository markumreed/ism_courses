#!/usr/bin/env python3
"""Build an instructor PowerPoint deck from a lab facilitation guide,
using usf_template.pptx as the branded template.

Usage:
  ./build_pptx.py ism2411/lab_w04.md      # one deck  -> ism2411/slides_w04.pptx
  ./build_pptx.py                         # every lab_w*.md in ism2411/

Transform rules applied to every guide:
  - Time ranges are stripped from every heading, e.g. "(0:05-0:13, 8 min)".
  - Every "Say to the class:" quote goes into the slide's speaker notes only
    (never onto the visible slide).
  - Every "Do, live ...:" block (a live demo) produces an EMPTY slide -- the
    instructor is demoing on the projector directly, not reading a slide.
    Full detail for that demo still goes into the speaker notes.
  - Each Exercise gets exactly one slide.
  - Stretch goals are consolidated onto a single "take-home, due Sunday"
    slide -- they are not walked through live in class.
"""
from __future__ import annotations

import pathlib
import re
import sys

from pptx import Presentation
from pptx.util import Pt

HERE = pathlib.Path(__file__).resolve().parent
TEMPLATE = HERE / "usf_template.pptx"

# usf_template.pptx layout indices (see `python3 -c` dump in dev notes)
LAYOUT_TITLE = 1     # "Presentation Title - Pattern"   (Title, Subtitle)
LAYOUT_CONTENT = 3   # "Title and Content"               (Title, Content)
LAYOUT_BLANK = 19    # "Blank"                            (nothing)

MAX_BODY_LINES = 8  # keep each exercise to one slide -- cap visible bullets


# ---------------------------------------------------------------- text utils


def unescape_tex(s: str) -> str:
    """Undo pandoc/LaTeX backslash escapes (\\&, \\_, \\#, ...)."""
    return re.sub(r"\\+([&_#%$~^{}])", r"\1", s)


def strip_time(heading: str) -> str:
    """Drop a trailing time/duration parenthetical from a heading."""
    return re.sub(r"\s*\([^()]*\)\s*$", "", heading).strip()


# ------------------------------------------------------------------- guide parse


def parse_frontmatter(text: str) -> tuple[dict, str]:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    fm: dict[str, str] = {}
    if not m:
        return fm, text
    for line in m.group(1).splitlines():
        mm = re.match(r"([\w-]+):\s*(.*)", line)
        if mm:
            fm[mm.group(1)] = mm.group(2).strip().strip('"')
    return fm, text[m.end():]


def split_h(text: str, level: int) -> list[tuple[str, str]]:
    """Split on ATX headings of exactly `level` hashes, ignoring fenced code."""
    mark = "#" * level + " "
    deeper = "#" * (level + 1)
    parts: list[tuple[str, str]] = []
    head, body = None, []
    fence = ""
    for line in text.splitlines():
        f = re.match(r"^(`{3,}|~{3,})", line)
        if fence:
            if f and line.startswith(fence):
                fence = ""
        elif f:
            fence = f.group(1)
        if not fence and line.startswith(mark) and not line.startswith(deeper):
            if head is not None:
                parts.append((head, "\n".join(body)))
            head, body = line[len(mark):].strip(), []
        elif head is not None:
            body.append(line)
    if head is not None:
        parts.append((head, "\n".join(body)))
    return parts


def find_blocks(content: str) -> list[tuple[str, str]]:
    """Split `content` at each top-of-line bold label ('**Label:**' / '**Label.**'),
    ignoring inline bold used mid-sentence or mid-bullet. Returns [(label, body)]."""
    lines = content.split("\n")
    label_lines: list[tuple[int, str, str]] = []
    for idx, line in enumerate(lines):
        s = line.strip()
        m = re.match(r"^\*\*([^*]+?)\*\*[:.]?\s*(.*)$", s)
        if m:
            label_lines.append((idx, m.group(1).strip().rstrip(":."), m.group(2)))
    blocks = []
    for j, (idx, label, trailing) in enumerate(label_lines):
        end_idx = label_lines[j + 1][0] if j + 1 < len(label_lines) else len(lines)
        body_lines = ([trailing] if trailing else []) + lines[idx + 1:end_idx]
        body = "\n".join(body_lines).strip()
        body = re.split(r"\n\s*---\s*\n", body)[0].strip()
        blocks.append((label, body))
    return blocks


def leading_prose(content: str) -> str:
    """Text before the first top-of-line bold label, if any."""
    first = find_blocks(content)
    lines = content.split("\n")
    for idx, line in enumerate(lines):
        if re.match(r"^\*\*([^*]+?)\*\*[:.]?\s*", line.strip()):
            return "\n".join(lines[:idx]).strip()
    return content.strip()


def to_lines(text: str) -> list[tuple[str, str]]:
    """Render a block of markdown into a flat list of (kind, text) where kind
    is 'para', 'bullet', 'code', or 'row' (a 2-col table row rendered as
    'left -- right')."""
    text = unescape_tex(text.strip())
    if not text:
        return []
    out: list[tuple[str, str]] = []
    para: list[str] = []
    fence = None
    fence_buf: list[str] = []

    def flush():
        if para:
            out.append(("para", " ".join(para)))
            para.clear()

    for raw in text.split("\n"):
        s = raw.strip()
        f = re.match(r"^(`{3,}|~{3,})", s)
        if fence:
            if f and s.startswith(fence):
                out.append(("code", "\n".join(fence_buf)))
                fence, fence_buf = None, []
            else:
                fence_buf.append(raw)
            continue
        if f:
            flush()
            fence = f.group(1)
            continue
        if not s:
            flush()
        elif s.startswith("|") and set(s) <= set("|:- "):
            pass  # table separator row (e.g. "|---|---|---|") -- not content
        elif s.startswith("|") and s.count("|") >= 2:
            flush()
            cells = [c.strip().strip("*") for c in s.strip("|").split("|")]
            if len(cells) >= 2 and cells[0].lower() not in ("term", "time", "---"):
                out.append(("row", " — ".join(cells[:2])))
        elif re.match(r"^[-*]\s+", s):
            flush()
            out.append(("bullet", re.sub(r"^[-*]\s+", "", s)))
        elif re.match(r"^\d+\.\s+", s):
            flush()
            out.append(("bullet", re.sub(r"^\d+\.\s+", "", s)))
        elif s.startswith(">"):
            flush()
            out.append(("bullet", re.sub(r"^>\s?", "", s)))
        elif re.match(r"^#{1,6}\s+", s):
            flush()
            out.append(("bullet", "**" + re.sub(r"^#{1,6}\s+", "", s) + "**"))
        else:
            para.append(s)
    flush()
    return out


def plain(s: str) -> str:
    """Strip inline markdown markers for use in speaker notes / plain text."""
    s = unescape_tex(s)
    s = re.sub(r"`([^`]+)`", r"\1", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"\1", s)
    s = re.sub(r"(?<![*\w])\*([^*\n]+)\*(?!\*)", r"\1", s)
    return s


# --------------------------------------------------------------------- pptx build


def add_runs(paragraph, text: str, mono: bool = False) -> None:
    text = unescape_tex(text)
    tokens = re.split(r"(\*\*[^*]+\*\*|`[^`]+`)", text)
    for tok in tokens:
        if not tok:
            continue
        run = paragraph.add_run()
        if tok.startswith("**") and tok.endswith("**"):
            run.text = tok[2:-2]
            run.font.bold = True
        elif tok.startswith("`") and tok.endswith("`"):
            run.text = tok[1:-1]
            run.font.name = "Consolas"
        else:
            run.text = tok
        if mono:
            run.font.name = "Consolas"


def set_title(placeholder, text: str) -> None:
    """Set a title/subtitle placeholder's text, rendering inline markdown
    (`code`, **bold**) as formatted runs instead of leaving raw markers."""
    tf = placeholder.text_frame
    tf.clear()
    add_runs(tf.paragraphs[0], text)


def set_body(placeholder, items: list[tuple[str, str]], cap: int = MAX_BODY_LINES) -> None:
    tf = placeholder.text_frame
    tf.clear()
    shown, truncated = items[:cap], len(items) > cap
    first = True
    for kind, text in shown:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        if kind == "code":
            code_lines = text.split("\n")[:6]
            for i, cl in enumerate(code_lines):
                pp = p if i == 0 else tf.add_paragraph()
                run = pp.add_run()
                run.text = cl
                run.font.name = "Consolas"
                run.font.size = Pt(16)
        else:
            add_runs(p, text)
    if truncated:
        p = tf.add_paragraph()
        run = p.add_run()
        run.text = "… see the facilitation guide for the rest"
        run.font.italic = True


NOTES_ORDER = [
    ("teaching_goal", "TEACHING GOAL"),
    ("say", "SAY TO THE CLASS"),
    ("do", "DO"),
    ("common", "COMMON STUDENT MISTAKES"),
    ("cfu", "CHECK FOR UNDERSTANDING"),
    ("extra", "EXTRA / OPTIONAL"),
]


def write_notes(slide, sections: dict[str, str], heading: str = "") -> None:
    tf = slide.notes_slide.notes_text_frame
    tf.clear()
    first = True
    if heading:
        p = tf.paragraphs[0]
        run = p.add_run()
        run.text = heading
        run.font.bold = True
        run.font.size = Pt(14)
        first = False
    for key, label in NOTES_ORDER:
        text = sections.get(key, "").strip()
        if not text:
            continue
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        run = p.add_run()
        run.text = label
        run.font.bold = True
        run.font.size = Pt(12)
        for line in text.split("\n"):
            if not line.strip():
                continue
            bp = tf.add_paragraph()
            run = bp.add_run()
            run.text = plain(line.strip())
            run.font.size = Pt(11)


def classify_blocks(content: str) -> dict[str, str]:
    """Pull out teaching goal / say-to-class / do / common-mistakes /
    check-for-understanding / everything-else (extra) from an exercise body."""
    goal, say, do_live, do_plain, common, cfu, extra = [], [], [], [], [], [], []
    for label, body in find_blocks(content):
        low = label.lower()
        if low.startswith("teaching goal"):
            goal.append(body)
        elif low.startswith("say to the class"):
            say.append(body)
        elif low.startswith("do"):
            (do_live if "live" in low else do_plain).append(body)
        elif low.startswith("common student") or low.startswith("common mistakes"):
            common.append(body)
        elif low.startswith("check for understanding"):
            cfu.append(body)
        else:
            b = body.lstrip(", -").strip()
            extra.append(f"{label}: {b}" if b else label)
    lead = leading_prose(content)
    if lead:
        extra.insert(0, lead)
    return {
        "goal": "\n\n".join(goal),
        "say": "\n\n".join(say),
        "do_live": "\n\n".join(do_live),
        "do_plain": "\n\n".join(do_plain),
        "common": "\n\n".join(common),
        "cfu": "\n\n".join(cfu),
        "extra": "\n\n".join(extra),
    }


def add_segment_slide(prs: Presentation, title: str, parsed: dict[str, str]) -> None:
    is_live = bool(parsed["do_live"].strip())
    if is_live:
        slide = prs.slides.add_slide(prs.slide_layouts[LAYOUT_BLANK])
        notes_heading = f"{title}  —  LIVE DEMO (nothing projected; go to the live app/terminal/browser)"
    else:
        slide = prs.slides.add_slide(prs.slide_layouts[LAYOUT_CONTENT])
        set_title(slide.placeholders[0], title)
        body_src = parsed["do_plain"] or parsed["extra"]
        set_body(slide.placeholders[1], to_lines(body_src))
        notes_heading = title

    write_notes(
        slide,
        {
            "teaching_goal": parsed["goal"],
            "say": parsed["say"],
            "do": parsed["do_live"] if is_live else "",
            "common": parsed["common"],
            "cfu": parsed["cfu"],
            "extra": parsed["extra"] if not is_live else parsed["extra"] + (
                ("\n\n" + parsed["do_plain"]) if parsed["do_plain"] and is_live else ""
            ),
        },
        heading=notes_heading,
    )


def add_stretch_slide(prs: Presentation, items: list[tuple[str, str]]) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[LAYOUT_CONTENT])
    set_title(slide.placeholders[0], "Stretch Goals — Take-Home (due Sunday)")
    tf = slide.placeholders[1].text_frame
    tf.clear()
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = "Not done live in class — students complete these on their own by Sunday."
    run.font.italic = True
    for name, content in items:
        p = tf.add_paragraph()
        parsed = classify_blocks(content)
        blurb = parsed["goal"] or leading_prose(content) or parsed["say"] or parsed["do_plain"] or parsed["do_live"]
        blurb = plain(blurb).split("\n")[0]
        if len(blurb) > 140:
            blurb = blurb[:137] + "…"
        run = p.add_run()
        run.text = name
        run.font.bold = True
        if blurb:
            run2 = p.add_run()
            run2.text = "  —  " + blurb

    notes_sections = {}
    notes_text = []
    for name, content in items:
        notes_text.append(f"{name}\n" + plain(content))
    write_notes(slide, {"extra": "\n\n".join(notes_text)}, heading="Stretch goals — full detail (reference only; take-home)")


def add_wrapup_slide(prs: Presentation, wrap_content: str) -> None:
    reflections = []
    for it in re.findall(r"^\d+\.\s+(.*)$", wrap_content, re.M):
        m = re.match(r"\*([^*]+)\*", it.strip())
        reflections.append(plain(m.group(1) if m else re.split(r"\s[—-]\s", it)[0]))
    checklist = [plain(c) for c in re.findall(r"^-\s*\[[ x]\]\s+(.*)$", wrap_content, re.M)]

    slide = prs.slides.add_slide(prs.slide_layouts[LAYOUT_CONTENT])
    set_title(slide.placeholders[0], "Wrap-Up")
    tf = slide.placeholders[1].text_frame
    tf.clear()
    first = True

    def heading_para(text):
        nonlocal first
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        run = p.add_run()
        run.text = text
        run.font.bold = True
        return p

    if reflections:
        heading_para("Reflection questions")
        for r in reflections[:4]:
            p = tf.add_paragraph()
            run = p.add_run()
            run.text = r
    if checklist:
        heading_para("Submission checklist")
        for c in checklist[:6]:
            p = tf.add_paragraph()
            run = p.add_run()
            run.text = c

    write_notes(slide, {"extra": plain(wrap_content)}, heading="Wrap-Up — full detail")


def add_title_slide(prs: Presentation, course: str, week_no: str, unit: str, subtitle: str) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[LAYOUT_TITLE])
    set_title(slide.placeholders[0], subtitle)
    sub = f"{course} · Week {week_no}" + (f" · {unit}" if unit else "")
    if 1 in [ph.placeholder_format.idx for ph in slide.placeholders]:
        slide.placeholders[1].text = sub


def add_objectives_slide(prs: Presentation, objectives: list[str]) -> None:
    if not objectives:
        return
    slide = prs.slides.add_slide(prs.slide_layouts[LAYOUT_CONTENT])
    set_title(slide.placeholders[0], "Learning Objectives")
    set_body(slide.placeholders[1], [("bullet", plain(o)) for o in objectives], cap=len(objectives))


# ------------------------------------------------------------------------ main


def remove_all_slides(prs: Presentation) -> None:
    xml_slides = prs.slides._sldIdLst
    for sld in list(xml_slides):
        prs.part.drop_rel(sld.rId)
        xml_slides.remove(sld)


def build_deck(path: pathlib.Path) -> Presentation:
    fm, body = parse_frontmatter(path.read_text())
    body = body.replace("\\newpage", "")

    title = fm.get("title", path.stem)
    course = (re.search(r"[A-Z]{2,4}\s?\d{4}", title) or ["Course"])[0].replace(" ", "")
    week = re.search(r"Week\s*(\d+)", title, re.I) or re.search(r"w(\d+)", path.stem)
    week_no = week.group(1) if week else "?"
    subtitle = unescape_tex(re.sub(r"\s*[—-]\s*Instructor.*$", "", fm.get("subtitle", ""))).strip()
    unit = fm.get("date", "")

    l1 = split_h(body, 1)
    get = lambda pfx: next((c for h, c in l1 if h.lower().startswith(pfx)), "")

    objectives = [plain(o) for o in re.findall(r"^\d+\.\s+(.*)$", get("learning objectives"), re.M)]

    walk = get("segment-by-segment") or get("segment by segment")
    segments = split_h(walk, 2)

    wrap = get("wrap-up") or get("wrap up")

    prs = Presentation(TEMPLATE)
    remove_all_slides(prs)

    add_title_slide(prs, course, week_no, unit, subtitle or title)
    add_objectives_slide(prs, objectives)

    stretch_items: list[tuple[str, str]] = []
    for head, content in segments:
        name = strip_time(head)
        if name.lower().startswith("stretch"):
            stretch_items.append((name, content))
            continue
        parsed = classify_blocks(content)
        add_segment_slide(prs, name, parsed)

    if stretch_items:
        add_stretch_slide(prs, stretch_items)

    if wrap.strip():
        add_wrapup_slide(prs, wrap)

    return prs


def main(argv: list[str]) -> int:
    targets = [pathlib.Path(a) for a in argv[1:]]
    if not targets:
        targets = sorted(HERE.glob("ism2411/lab_w*.md"))
    for src in targets:
        src = src if src.is_absolute() else (HERE / src)
        if not src.exists():
            print(f"!! missing {src}")
            continue
        out = src.with_name(src.name.replace("lab_", "slides_")).with_suffix(".pptx")
        prs = build_deck(src)
        prs.save(out)
        print(f"  {src.relative_to(HERE)}  ->  {out.relative_to(HERE)}  ({len(prs.slides)} slides)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
