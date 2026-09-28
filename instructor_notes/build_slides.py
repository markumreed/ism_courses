#!/usr/bin/env python3
"""Build a reveal.js instructor projection deck from a lab facilitation guide.

Usage:
  ./build_slides.py ism2411/lab_w04.md        # one deck  -> ism2411/slides_w04.html
  ./build_slides.py                           # every lab_w*.md in ism2411/ and ism3232/

Each guide is dense Markdown with a very regular shape (Session Snapshot table,
Learning Objectives list, Timing Plan table, a "Segment-by-Segment Walkthrough"
of `## Exercise N` / `## Part N` / `## Intro` / `## Stretch` blocks, a Wrap-Up).
This reads that structure and emits a self-contained slide deck whose speaker
notes (press **S** in reveal.js) carry the facilitation detail: teaching goal,
the full "Say to the class" script, common pitfalls, and the answer to every
"Check for understanding" prompt.
"""
from __future__ import annotations

import html
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
CDN = "https://cdnjs.cloudflare.com/ajax/libs"
REVEAL = f"{CDN}/reveal.js/4.6.1"

# ---------------------------------------------------------------- inline Markdown


def unescape_tex(s: str) -> str:
    """Undo pandoc/LaTeX backslash escapes (\\&, \\\\&, \\_, \\#, ...)."""
    return re.sub(r"\\+([&_#%$~^{}])", r"\1", s)


def md(s: str) -> str:
    """Render a run of inline Markdown to HTML."""
    s = unescape_tex(s)
    s = html.escape(s, quote=False)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\*\w])\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", s)
    return s


def blocks_html(text: str) -> str:
    """Render a small block of Markdown (paragraphs + `-` bullets) to HTML."""
    text = text.strip()
    if not text:
        return ""
    out, para, bullets = [], [], []

    def flush_para():
        if para:
            out.append("<p>" + " ".join(md(x) for x in para) + "</p>")
            para.clear()

    def flush_bullets():
        if bullets:
            out.append("<ul>" + "".join(f"<li>{md(x)}</li>" for x in bullets) + "</ul>")
            bullets.clear()

    for raw in text.split("\n"):
        line = raw.strip()
        if not line:
            flush_para()
            flush_bullets()
        elif re.match(r"^[-*]\s+", line):
            flush_para()
            bullets.append(re.sub(r"^[-*]\s+", "", line))
        elif re.match(r"^\d+\.\s+", line):
            flush_para()
            bullets.append(re.sub(r"^\d+\.\s+", "", line))
        else:
            flush_bullets()
            para.append(line)
    flush_para()
    flush_bullets()
    return "".join(out)


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


def parse_table(md_text: str) -> list[list[str]]:
    rows = []
    for line in md_text.strip().splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if all(re.fullmatch(r":?-{2,}:?", c or "-") for c in cells):
            continue  # header rule
        rows.append(cells)
    return rows


def grab_para(content: str, label_re: str) -> str:
    m = re.search(
        r"\*\*(?:%s)[^:*]*:\*\*[ \t]*(.*?)(?=\n\n\*\*[A-Z]|\n\n#|\n\n---|\Z)" % label_re,
        content,
        re.S,
    )
    return m.group(1).strip() if m else ""


def extract_items(content: str) -> list[dict]:
    """Ordered list of {kind: quote|code|output|table, label, text, lang}."""
    lines = content.split("\n")
    items: list[dict] = []
    label = ""
    i = 0
    while i < len(lines):
        line = lines[i]

        fence = re.match(r"^(`{3,})[ \t]*([\w+-]*)[ \t]*$", line)
        if fence:
            close, lang = fence.group(1), fence.group(2)
            j, buf = i + 1, []
            while j < len(lines) and not re.match(r"^" + close + r"[ \t]*$", lines[j]):
                buf.append(lines[j])
                j += 1
            is_out = bool(
                re.search(r"expected output|run it|verified output|sample run|output\b", label, re.I)
            ) and lang in ("", "text", "plaintext", "console", "output")
            items.append(
                {
                    "kind": "output" if is_out else "code",
                    "lang": (lang or "text"),
                    "text": "\n".join(buf),
                    "label": label,
                }
            )
            label = ""
            i = j + 1
            continue

        if line.strip().startswith("|") and line.strip().count("|") >= 2:
            j, buf = i, []
            while j < len(lines) and lines[j].strip().startswith("|"):
                buf.append(lines[j])
                j += 1
            if len(buf) >= 2:
                items.append({"kind": "table", "text": "\n".join(buf), "label": label, "lang": ""})
                label = ""
                i = j
                continue

        if line.lstrip().startswith(">"):
            j, buf = i, []
            while j < len(lines):
                cur = lines[j]
                if cur.lstrip().startswith(">"):
                    buf.append(re.sub(r"^[ \t]*>[ \t]?", "", cur))
                    j += 1
                elif cur.strip() == "":
                    k = j + 1
                    while k < len(lines) and lines[k].strip() == "":
                        k += 1
                    if k < len(lines) and lines[k].lstrip().startswith(">"):
                        buf.append("")
                        j = k
                    else:
                        break
                else:
                    break
            items.append({"kind": "quote", "text": "\n".join(buf).strip(), "label": label, "lang": ""})
            label = ""
            i = j
            continue

        s = line.strip()
        if s:
            m = re.match(r"^\*\*(.+?):?\*\*[ \t]*:?[ \t]*$", s)
            if m:
                label = m.group(1).strip().rstrip(":")
            elif s.endswith(":") and len(s) <= 80:
                label = re.sub(r"^\*+|\*+$", "", s[:-1]).strip()
            else:
                label = ""  # prose separates a label from a following block
        i += 1
    return items


# --------------------------------------------------------------------- rendering


def clean_label(lbl: str) -> str:
    lbl = re.sub(r"^\*+|\*+$", "", lbl or "").strip().rstrip(":").strip()
    low = lbl.lower()
    if low.startswith(("run it", "run the", "run pass", "run with", "run this")) or "expected output" in low:
        return "Expected output"
    if low.startswith(("live-code", "live code", "type this", "type the")):
        return "Live code"
    if low.startswith(("do,", "do:", "do ")) or low == "do":
        return "Do this"
    if low.startswith(("say to the class", "the connective narrative", "say ")):
        return "Say to the class"
    if low.startswith(("pass 1", "pass 2", "pass 3")):
        return lbl.split("—")[0].strip() if "—" in lbl else lbl
    if len(lbl) > 46 or lbl.endswith((".", "?")):
        return ""
    return lbl


def code_lang(lang: str) -> str:
    return {
        "py": "python",
        "zsh": "bash",
        "sh": "bash",
        "shell": "bash",
        "console": "bash",
        "": "plaintext",
        "text": "plaintext",
        "output": "plaintext",
    }.get(lang, lang)


def section(cls: str, body: str, notes: str = "") -> str:
    note = f'<aside class="notes">{notes}</aside>' if notes.strip() else ""
    return f'<section class="{cls}">{body}{note}</section>\n'


def code_slide(item: dict, notes: str) -> str:
    is_out = item["kind"] == "output"
    lbl = clean_label(item["label"]) or ("Expected output" if is_out else "Code")
    icon = "▶" if is_out else "⌨"
    accent = "var(--G)" if is_out else "var(--S)"
    lang = code_lang(item["lang"])
    body = (
        f'<h3 style="color:{accent};text-align:left;">{icon} {md(lbl)}</h3>'
        f'<pre><code class="language-{lang}" data-trim data-noescape>'
        f'{html.escape(item["text"])}</code></pre>'
    )
    return section("s-code" if not is_out else "s-code s-out", body, notes)


def table_slide(item: dict, notes: str) -> str:
    rows = parse_table(item["text"])
    if not rows:
        return ""
    head, *rest = rows
    thead = "".join(f"<th>{md(c)}</th>" for c in head)
    trows = "".join(
        "<tr>" + "".join(f"<td>{md(c)}</td>" for c in r) + "</tr>" for r in rest
    )
    lbl = clean_label(item["label"])
    cap = f"<h3>{md(lbl)}</h3>" if lbl else ""
    return section(
        "s-point",
        f'{cap}<table class="grid"><thead><tr>{thead}</tr></thead><tbody>{trows}</tbody></table>',
        notes,
    )


def quote_slide(item: dict, label: str, notes: str) -> str:
    paras = "".join(
        f"<p>{md(p)}</p>" for p in re.split(r"\n\s*\n", item["text"]) if p.strip()
    )
    body = (
        f'<div class="say"><div class="say-lbl">{md(label)}</div>{paras}</div>'
    )
    return section("s-point s-say", body, notes)


def build_deck(path: pathlib.Path) -> str:
    fm, body = parse_frontmatter(path.read_text())
    body = body.replace("\\newpage", "")

    title = fm.get("title", path.stem)
    course = (re.search(r"[A-Z]{2,4}\s?\d{4}", title) or ["Course"])[0].replace(" ", "")
    week = (re.search(r"Week\s*(\d+)", title, re.I) or re.search(r"w(\d+)", path.stem))
    week_no = week.group(1) if week else "?"
    subtitle = unescape_tex(
        re.sub(r"\s*[—-]\s*Instructor.*$", "", fm.get("subtitle", ""))
    ).strip()
    unit = fm.get("date", "")

    l1 = split_h(body, 1)
    get = lambda pfx: next((c for h, c in l1 if h.lower().startswith(pfx)), "")

    snap_rows = parse_table(get("session snapshot"))
    snap: dict[str, str] = {}
    for row in snap_rows:
        if len(row) == 2:
            snap[re.sub(r"[*]", "", row[0]).strip()] = row[1]
    snap_prose = re.sub(r"(?s)^.*?\|\n\n", "", get("session snapshot")).strip()

    objectives = re.findall(r"^\d+\.\s+(.*)$", get("learning objectives"), re.M)

    timing_sec = get("timing plan")
    timing_rows = [r for r in parse_table(timing_sec) if len(r) == 3]
    if timing_rows and timing_rows[0][0].strip().lower() in ("time", "slot"):
        timing_rows = timing_rows[1:]
    timing_prose = re.sub(r"(?s)^.*\|\n", "", timing_sec).strip()
    timing_prose = "\n\n".join(
        p for p in re.split(r"\n\s*\n", timing_prose) if not p.strip().startswith("|")
    )

    walk = get("segment-by-segment") or get("segment by segment")
    segments = split_h(walk, 2)

    wrap = get("wrap-up") or get("wrap up")
    reflections = []
    for it in re.findall(r"^\d+\.\s+(.*)$", wrap, re.M):
        m = re.match(r"\*([^*]+)\*", it.strip())
        reflections.append(m.group(1) if m else re.split(r"\s[—-]\s", it)[0])
    checklist = re.findall(r"^-\s*\[[ x]\]\s+(.*)$", wrap, re.M)
    preview = grab_para(wrap, r"Preview")

    # ---- assemble slides ---------------------------------------------------
    S: list[str] = []

    tbar = "".join(
        f'<span class="t-item"><strong>{md(t)}</strong> {md(seg)}</span>'
        for t, seg, _ in timing_rows
    )
    S.append(
        section(
            "s-title",
            f'<p class="eyebrow">{md(course)} &nbsp;·&nbsp; Week {week_no}'
            f'{("  ·  " + md(unit)) if unit else ""}</p>'
            f"<h1>{md(subtitle or title)}</h1>"
            f'<div class="t-bar">{tbar}</div>'
            f'<p class="hint">&larr; &rarr; navigate &nbsp;·&nbsp; F fullscreen &nbsp;·&nbsp; S speaker notes</p>',
            blocks_html(snap_prose),
        )
    )

    glance_keys = ["Format", "Prerequisites", "Exercises covered", "Submission", "Class length"]
    kv = "".join(
        f'<div class="kv"><span>{md(k)}</span><p>{md(snap[k])}</p></div>'
        for k in glance_keys
        if snap.get(k)
    )
    if kv:
        S.append(section("s-point", f"<h2>Today at a glance</h2>{kv}", ""))

    if objectives:
        lis = "".join(f"<li>{md(o)}</li>" for o in objectives)
        S.append(
            section(
                "s-point",
                f"<h2>Learning objectives</h2><ul>{lis}</ul>",
                "By the end of the session students should be able to do each of these.",
            )
        )

    if timing_rows:
        trs = "".join(
            f"<tr><td>{md(t)}</td><td>{md(seg)}</td><td>{md(mins)}</td></tr>"
            for t, seg, mins in timing_rows
        )
        S.append(
            section(
                "s-point",
                f"<h2>Timing plan</h2><table class='grid'><thead><tr>"
                f"<th>Time</th><th>Segment</th><th>Min</th></tr></thead><tbody>{trs}</tbody></table>",
                blocks_html(timing_prose),
            )
        )

    for head, content in segments:
        m = re.match(r"^(.*?)\s*\(([^()]*(?:\([^()]*\)[^()]*)*)\)\s*$", head)
        name, timing = (m.group(1).strip(), m.group(2).strip()) if m else (head, "")
        chip_m = re.match(r"^(Exercise\s+[\w&]+|Part\s+\d+|Intro|Stretch(?:\s+[A-Z](?:\s*&\s*[A-Z])?)?|Wrap-Up)", name)
        chip = chip_m.group(1) if chip_m else "Segment"
        headline = re.sub(
            r"^(?:Exercise\s+[\w&]+|Part\s+\d+|Stretch\s+[A-Z](?:\s*&\s*[A-Z])?)\s*[—-]\s*",
            "",
            name,
        )
        if headline == name and name in ("Intro", "Wrap-Up"):
            headline = "Kickoff" if name == "Intro" else name

        goal = grab_para(content, r"Teaching goal")
        goal_shown = False
        common = grab_para(content, r"Common student (?:mistakes|confusion)|Common mistakes")
        cfu = grab_para(content, r"Check for understanding")

        divider_notes = blocks_html(goal) or ""
        if timing:
            divider_notes = f'<p><em>{md(timing)}</em></p>' + divider_notes
        S.append(
            section(
                "s-sec",
                f'<div class="sec-n">{md(chip)}{("  ·  " + md(timing)) if timing else ""}</div>'
                f'<h1>{md(headline)}</h1>',
                divider_notes,
            )
        )

        items = extract_items(content)
        first_code_note = blocks_html(grab_para(content, r"Line-by-line explanation"))
        used_first = False
        for it in items:
            if it["kind"] == "quote":
                lbl = clean_label(it["label"]) or "Say to the class"
                note = ""
                if goal and not goal_shown:
                    note = "<strong>Teaching goal</strong>" + blocks_html(goal)
                    goal_shown = True
                S.append(quote_slide(it, lbl, note))
            elif it["kind"] == "table":
                S.append(table_slide(it, ""))
            elif it["kind"] == "output":
                S.append(
                    code_slide(
                        it,
                        "Run this live. Confirm every student sees this exact output before moving on."
                        + (("<hr>" + "<strong>Common pitfalls</strong>" + blocks_html(common)) if common else ""),
                    )
                )
                common = ""  # attach pitfalls once per segment
            else:  # code
                note = ""
                if not used_first and first_code_note:
                    note = first_code_note
                    used_first = True
                elif not used_first:
                    note = "Type this with the class, line by line. Do not paste."
                    used_first = True
                S.append(code_slide(it, note))

        if not items:  # prose-only segment (e.g. a take-home Stretch)
            prose = content
            for lab in ("Teaching goal", "Say to the class", "Common student mistakes to watch for",
                        "Common student confusion to watch for", "Check for understanding",
                        "Frame it", "Line-by-line explanation"):
                prose = re.sub(
                    r"\*\*%s[^:*]*:\*\*.*?(?=\n\n\*\*[A-Z]|\n\n#|\Z)" % re.escape(lab),
                    "", prose, flags=re.S,
                )
            prose = re.sub(r"^\s*---\s*$", "", prose, flags=re.M).strip()
            if prose:
                S.append(section("s-point", f"<h2>{md(headline)}</h2>{blocks_html(prose)}",
                                 blocks_html(goal)))

        if common:  # no output slide carried it
            S.append(
                section(
                    "s-warn",
                    f'<div class="warn"><div class="warn-lbl">⚠ Common pitfalls</div>{blocks_html(common)}</div>',
                    "Watch for these as you walk the room.",
                )
            )

        if cfu:
            S.append(
                section(
                    "s-point s-cfu",
                    f'<div class="concept"><div class="concept-lbl">Check for understanding</div>'
                    f"{blocks_html(cfu)}</div>",
                    "The parenthetical is the answer / what a strong response sounds like — keep it for yourself.",
                )
            )

    # ---- wrap-up ---------------------------------------------------------
    if reflections:
        lis = "".join(f"<li>{md(r)}</li>" for r in reflections)
        S.append(
            section(
                "s-point",
                f"<h2>Reflection</h2><ul>{lis}</ul>",
                blocks_html(wrap.split("submission checklist")[0]),
            )
        )
    if checklist:
        lis = "".join(f'<li>{md(c)}</li>' for c in checklist)
        S.append(
            section(
                "s-point s-check",
                f"<h2>Submission checklist</h2><ul class='chk'>{lis}</ul>",
                blocks_html("**Next module:** " + preview) if preview else "",
            )
        )
    S.append(
        section(
            "s-sec",
            f'<div class="sec-n">{md(course)} · Week {week_no}</div><h1>End of lab</h1>',
            "",
        )
    )

    return PAGE.format(
        title=html.escape(f"{course} Lab W{week_no} — {subtitle or title}"),
        course=html.escape(course),
        slides="".join(S),
        reveal=REVEAL,
        cdn=CDN,
    )


# ------------------------------------------------------------------- HTML shell

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{title}</title>
<link rel="stylesheet" href="{reveal}/reveal.min.css">
<link rel="stylesheet" href="{reveal}/theme/black.min.css">
<link rel="stylesheet" href="{cdn}/highlight.js/11.9.0/styles/atom-one-dark.min.css">
<style>
:root{{--T:#2dd4bf;--I:#818cf8;--A:#fbbf24;--G:#4ade80;--R:#fb7185;--S:#38bdf8;
  --bg:#0d1117;--bg2:#161b22;--bd:#30363d;--tx:#e6edf3;--mu:#8b949e;}}
.reveal{{font-family:"Segoe UI",system-ui,sans-serif;}}
.reveal .slides{{text-align:left;}}
.reveal h1{{font-size:1.7em;color:var(--T);font-weight:800;letter-spacing:-.02em;line-height:1.15;}}
.reveal h2{{font-size:1.15em;color:var(--I);font-weight:700;margin-bottom:.5em;}}
.reveal h3{{font-size:.6em;color:var(--mu);font-weight:600;text-transform:uppercase;
  letter-spacing:.13em;margin-bottom:.5em;}}
.reveal p{{font-size:.82em;color:var(--tx);line-height:1.7;margin:.3em 0;}}
.reveal ul{{list-style:none;padding:0;margin:.4em 0;}}
.reveal ul li{{font-size:.8em;color:var(--tx);padding:.28em 0;line-height:1.55;}}
.reveal ul li::before{{content:"\\25b8 ";color:var(--T);font-weight:700;}}
.reveal strong{{color:var(--A);}} .reveal em{{color:var(--mu);}}
.reveal code{{font-family:"Fira Code",ui-monospace,monospace;color:var(--S);
  background:rgba(56,189,248,.12);padding:2px 7px;border-radius:4px;font-size:.9em;}}
.reveal pre{{width:100%;font-size:.46em;margin:.3em 0;border-radius:8px;border:1px solid var(--bd);
  max-height:76vh;overflow:auto;box-shadow:none;}}
.reveal pre code{{padding:1em 1.2em;background:#0a0a12;border-radius:8px;}}
.reveal table.grid{{font-size:.62em;border-collapse:collapse;width:100%;}}
.reveal table.grid th{{color:var(--I);text-align:left;border-bottom:2px solid var(--I);padding:.4em .6em;}}
.reveal table.grid td{{border-bottom:1px solid var(--bd);padding:.4em .6em;vertical-align:top;color:var(--tx);}}

.s-title{{background:linear-gradient(135deg,#060c14,#0d1117);text-align:center;}}
.s-title h1{{text-align:center;margin:.2em auto .1em;}}
.s-sec{{background:linear-gradient(135deg,#080e18,#0d1117);}}
.s-out pre code{{background:#081208;}}
.s-say .say{{background:rgba(45,212,191,.08);border:1px solid rgba(45,212,191,.25);
  border-left:4px solid var(--T);border-radius:0 10px 10px 0;padding:.8em 1.2em;}}
.s-say .say p{{font-style:italic;font-size:.92em;color:#dfeceb;}}
.say-lbl,.concept-lbl,.warn-lbl{{font-family:ui-monospace,monospace;font-size:.5em;font-weight:700;
  letter-spacing:.12em;text-transform:uppercase;color:var(--T);margin-bottom:.4em;}}
.concept{{background:rgba(129,140,248,.09);border:1px solid rgba(129,140,248,.25);
  border-left:4px solid var(--I);border-radius:0 10px 10px 0;padding:.8em 1.2em;}}
.concept-lbl{{color:var(--I);}}
.concept p{{font-size:.92em;}}
.warn{{background:rgba(251,191,36,.08);border:1px solid rgba(251,191,36,.25);
  border-left:4px solid var(--A);border-radius:0 10px 10px 0;padding:.8em 1.2em;}}
.warn-lbl{{color:var(--A);}}
.eyebrow{{font-family:ui-monospace,monospace;font-size:.5em;letter-spacing:.18em;
  text-transform:uppercase;color:var(--mu);margin-bottom:.4em;}}
.hint{{font-size:.38em;color:var(--mu);margin-top:1em;}}
.t-bar{{display:flex;gap:.45em;flex-wrap:wrap;justify-content:center;margin:.6em auto 0;max-width:80%;}}
.t-item{{font-family:ui-monospace,monospace;font-size:.4em;padding:.3em .8em;border-radius:5px;
  background:rgba(255,255,255,.06);color:var(--mu);border:1px solid var(--bd);}}
.t-item strong{{color:var(--tx);}}
.sec-n{{font-family:ui-monospace,monospace;font-size:.5em;font-weight:700;letter-spacing:.14em;
  text-transform:uppercase;color:var(--I);opacity:.75;margin-bottom:.3em;}}
.kv{{display:grid;grid-template-columns:9em 1fr;gap:.4em 1.2em;align-items:baseline;
  border-bottom:1px solid var(--bd);padding:.45em 0;}}
.kv span{{font-family:ui-monospace,monospace;font-size:.58em;text-transform:uppercase;
  letter-spacing:.1em;color:var(--I);}}
.kv p{{margin:0;font-size:.72em;}}
ul.chk li::before{{content:"\\2610 ";color:var(--G);}}
.reveal .slide-number{{font-size:.5em;}}
</style>
</head>
<body>
<div class="reveal"><div class="slides">
{slides}
</div></div>
<script src="{reveal}/reveal.min.js"></script>
<script src="{reveal}/plugin/notes/notes.min.js"></script>
<script src="{reveal}/plugin/highlight/highlight.min.js"></script>
<script>
Reveal.initialize({{
  width: 1180, height: 760, margin: 0.06,
  hash: true, slideNumber: 'c/t', transition: 'fade',
  plugins: [ RevealNotes, RevealHighlight ]
}});
</script>
</body>
</html>
"""


def main(argv: list[str]) -> int:
    targets = [pathlib.Path(a) for a in argv[1:]]
    if not targets:
        targets = sorted(HERE.glob("ism2411/lab_w*.md")) + sorted(HERE.glob("ism3232/lab_w*.md"))
    for src in targets:
        src = src if src.is_absolute() else (HERE / src)
        if not src.exists():
            print(f"!! missing {src}")
            continue
        out = src.with_name(src.name.replace("lab_", "slides_")).with_suffix(".html")
        out.write_text(build_deck(src))
        print(f"  {src.relative_to(HERE)}  ->  {out.relative_to(HERE)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
