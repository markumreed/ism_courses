"""Small helpers for generating ISM3232 weekly pages from verified files.

Every code listing on a page should come from a reference file through
`listing()`, `method()`, or `function()`, so the page can never show code
that was not run. Prose is passed in as HTML strings.
"""

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DOCS = ROOT / "ism3232" / "docs"
REF = ROOT / "reference" / "ism3232"


def esc(text):
    """Escape text for HTML element content."""
    return html.escape(text, quote=False)


def read(path, rev=None):
    """Return a reference file's text. Relative paths start at reference/ism3232.

    With `rev` (a commit in the parent repo), return the file as it was in that
    commit. Pages use this to show a guided step's code after the folder has
    moved on to the exercise answers."""
    path = Path(path)
    if not path.is_absolute():
        path = REF / path
    if rev is None:
        return path.read_text()
    import subprocess

    relative = path.relative_to(ROOT).as_posix()
    result = subprocess.run(
        ["git", "show", f"{rev}:{relative}"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


def head_from(template, title):
    """Copy the <head> of an existing page and give it a new <title>."""
    text = (DOCS / template).read_text()
    head = text[: text.index("</head>") + len("</head>")]
    return re.sub(r"<title>.*?</title>", f"<title>{esc(title)}</title>", head, count=1)


def listing(label, code):
    """A labelled code or output block in the reading-page style."""
    return f'<div class="code-label">{esc(label)}</div><pre><code>{esc(code.rstrip())}</code></pre>'


def highlight(code):
    """Return Python source as HTML with the lecture pages' span classes:
    kw (keywords and None/True/False), fn (name after def or class), str,
    comment, num. Whitespace and line breaks are kept exactly."""
    import io
    import keyword
    import tokenize

    lines = code.split("\n")
    offsets = [0]
    for line in lines:
        offsets.append(offsets[-1] + len(line) + 1)
    out, pos, after_def = [], 0, False
    try:
        tokens = list(tokenize.generate_tokens(io.StringIO(code).readline))
    except (tokenize.TokenError, IndentationError):
        return esc(code)
    fstart = getattr(tokenize, "FSTRING_START", None)
    fend = getattr(tokenize, "FSTRING_END", None)
    for index, tok in enumerate(tokens):
        if tok.type in (tokenize.ENDMARKER, tokenize.DEDENT, tokenize.INDENT):
            continue
        start = offsets[tok.start[0] - 1] + tok.start[1]
        end = offsets[tok.end[0] - 1] + tok.end[1]
        if start < pos:
            continue
        if tok.type == fstart:
            depth = 0
            for later in tokens[index:]:
                depth += (later.type == fstart) - (later.type == fend)
                if depth == 0:
                    end = offsets[later.end[0] - 1] + later.end[1]
                    break
        out.append(esc(code[pos:start]))
        text = esc(code[start:end])
        if tok.type == tokenize.COMMENT:
            text = f'<span class="comment">{text}</span>'
        elif tok.type in (tokenize.STRING, fstart):
            text = f'<span class="str">{text}</span>'
        elif tok.type == tokenize.NUMBER:
            text = f'<span class="num">{text}</span>'
        elif tok.type == tokenize.NAME:
            if after_def:
                text = f'<span class="fn">{text}</span>'
            elif keyword.iskeyword(tok.string):
                text = f'<span class="kw">{text}</span>'
        after_def = tok.type == tokenize.NAME and tok.string in ("def", "class")
        out.append(text)
        pos = end
    out.append(esc(code[pos:]))
    return "".join(out)


def code_block(label, code, python=True):
    """A labelled block in the lecture and lab style (.code-block)."""
    body = highlight(code.rstrip()) if python else esc(code.rstrip())
    return f'<div class="code-block"><div class="cb-label">{label}</div><pre>{body}</pre></div>'


def method(path, name, rev=None):
    """Return one method of a class in a reference file, exactly as written."""
    text = read(path, rev)
    pattern = rf"^    def {name}\(.*?(?=^    def |^\S|\Z)"
    match = re.search(pattern, text, re.DOTALL | re.MULTILINE)
    if match is None:
        raise ValueError(f"no method {name} in {path}")
    return match.group(0).rstrip()


def function(path, name, rev=None):
    """Return one top-level function (or class) in a reference file, exactly as written."""
    text = read(path, rev)
    pattern = rf"^(?:def|class) {name}\b.*?(?=^\S|\Z)"
    match = re.search(pattern, text, re.DOTALL | re.MULTILINE)
    if match is None:
        raise ValueError(f"no function {name} in {path}")
    return match.group(0).rstrip()


def lines_between(path, first, last, rev=None):
    """Return the lines of a reference file from the one containing `first`
    through the one containing `last`, exactly as written."""
    lines = read(path, rev).split("\n")
    start = next(i for i, line in enumerate(lines) if first in line)
    end = next(i for i in range(start, len(lines)) if last in lines[i])
    return "\n".join(lines[start : end + 1])


def callout(kind, label, body):
    """A boxed note. kind is 'concept', 'warn', or 'ok'."""
    return f'<div class="{kind}"><div class="concept-label">{label}</div>{body}</div>'


def term(word, definition):
    return f'<div class="term"><span class="term-word">{word}</span><span class="term-def">{definition}</span></div>'


def objective(text):
    return (
        '<div style="background:var(--blue-dim);border:1px solid var(--border);'
        "border-left:3px solid var(--blue);border-radius:0 8px 8px 0;padding:14px 18px;"
        'margin-bottom:28px;"><div style="font-family:var(--mono);font-size:10px;'
        "font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--blue);"
        'margin-bottom:6px;">&#x1F3AF; Learning objective</div><p style="margin:0;'
        f'font-size:15px;line-height:1.7;color:var(--text);">{text}</p></div>'
    )


def coming_from(label, text):
    return (
        '<div style="background:var(--bg2);border:1px solid var(--border);border-radius:10px;'
        'padding:18px 20px;margin-bottom:28px;"><div style="font-family:var(--mono);'
        "font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;"
        f'color:var(--muted);margin-bottom:8px;">&#x1F517; {label}</div><p style="margin:0;'
        f'font-size:14px;line-height:1.75;color:var(--text);">{text}</p></div>'
    )


def quiz_mc(number, question, options, answer_index, why):
    letters = "abcd"
    items = "\n".join(f"<li>{letters[i]}) {opt}</li>" for i, opt in enumerate(options))
    return (
        '<div class="quiz-item">\n'
        f'<div class="quiz-q">Q{number} · Multiple Choice</div>\n'
        f'<div class="quiz-question">{question}</div>\n'
        f'<ul class="quiz-options">\n{items}\n</ul>\n'
        '<details class="quiz-answer"><summary>Answer</summary><div style="margin-top:8px;">'
        f'{options[answer_index]} <span style="color:var(--muted);">— {why}</span></div></details>\n'
        "</div>"
    )


def quiz_tf(number, statement, answer, why):
    word = "True" if answer else "False"
    return (
        '<div class="quiz-item">\n'
        f'<div class="quiz-q">Q{number} · True / False</div>\n'
        f'<div class="quiz-question">{statement}</div>\n'
        '<details class="quiz-answer"><summary>Answer</summary><div style="margin-top:8px;">'
        f'{word} <span style="color:var(--muted);">— {why}</span></div></details>\n'
        "</div>"
    )


def quiz_trace(number, question, code, answer, why):
    return (
        '<div class="quiz-item">\n'
        f'<div class="quiz-q">Q{number} · Code Trace</div>\n'
        f'<div class="quiz-question">{question}</div>\n'
        f"<pre><code>{esc(code.rstrip())}</code></pre>\n"
        '<details class="quiz-answer"><summary>Answer</summary><div style="margin-top:8px;">'
        f'{answer} <span style="color:var(--muted);">— {why}</span></div></details>\n'
        "</div>"
    )


def quiz_short(number, question, answer):
    return (
        '<div class="quiz-item">\n'
        f'<div class="quiz-q">Q{number} · Short Answer</div>\n'
        f'<div class="quiz-question">{question}</div>\n'
        '<details class="quiz-answer"><summary>Answer</summary><div style="margin-top:8px;">'
        f"{answer}</div></details>\n"
        "</div>"
    )


def prev_next(prev_href, prev_week, prev_title, next_href, next_week, next_title):
    link = (
        "display:flex;align-items:center;gap:8px;text-decoration:none;color:var(--muted);"
        "font-size:13px;transition:color .15s;"
    )
    hover = "onmouseover=\"this.style.color='var(--blue)'\" onmouseout=\"this.style.color='var(--muted)'\""
    week = "font-family:var(--mono);font-size:10px;display:block;margin-bottom:2px;"
    return (
        "<!-- prev-next -->\n"
        '<div style="display:flex;justify-content:space-between;align-items:center;margin-top:48px;'
        'padding-top:24px;border-top:1px solid var(--border);">'
        f'<a href="{prev_href}" style="{link}" {hover}><span style="font-size:16px;">←</span>'
        f'<span><span style="{week}">{prev_week}</span>{prev_title}</span></a><span></span>'
        f'<a href="{next_href}" style="{link}text-align:right;" {hover}><span><span style="{week}">'
        f'{next_week}</span>{next_title}</span><span style="font-size:16px;">→</span></a></div>'
    )


def check_listings(page_path, sources):
    """Return the code blocks on a page that do not appear verbatim in any source text.

    `sources` is a list of reference-relative paths or literal strings (for
    captured outputs). Blocks inside quiz items are skipped.
    """
    text = Path(page_path).read_text()
    if '<h2 id="quiz">' in text:
        text = text[: text.index('<h2 id="quiz">')]
    texts = []
    for source in sources:
        try:
            is_file = "\n" not in source and (REF / source).is_file()
        except OSError:
            is_file = False
        texts.append((REF / source).read_text() if is_file else source)
    pool = "\n".join(texts)
    missing = []
    text = re.sub(r'<aside class="notes">.*?</aside>', "", text, flags=re.DOTALL)
    blocks = r'<pre[^>]*>(.*?)</pre>|<div class="run"[^>]*>(.*?)</div>'
    for match in re.finditer(blocks, text, re.DOTALL):
        raw = match.group(1) or match.group(2) or ""
        code = html.unescape(re.sub(r"<[^>]+>", "", raw))
        if code.strip() and code not in pool:
            missing.append(code.split("\n")[0][:70])
    return missing


# ── Lecture and lab components ────────────────────────────────────────────────

STRIP = [
    "W1 Setup",
    "W2 zsh Nav",
    "W3 venv/.zshrc",
    "W4 Search+Git",
    "W5 Variables",
    "W6 Loops+Dicts",
    "W7 Functions",
    "W8 Debug+Review",
    "W9 Midterm",
    "W10 OOP for Agents",
    "W11 Local Model",
    "W12 Tools+Guardrails",
    "W13 Design+SQL",
    "W14 DB Tools",
    "W15 Streamlit",
    "W16 GenAI+Demo",
]


def course_map(current):
    """The week strip, with the item that starts with `current` (e.g. 'W12 ') marked."""
    items = []
    for label in STRIP:
        cls = "map-item current" if label.startswith(current) else "map-item"
        items.append(f'<span class="{cls}">{esc(label)}</span>')
    return (
        '<div class="course-map">'
        + ' <span class="map-arrow">&rarr;</span> '.join(items)
        + "</div>"
    )


def section_divider(label):
    return (
        '<div class="section-divider"><div class="line"></div>'
        f'<div class="label">{label}</div><div class="line"></div></div>'
    )


def card(title, body):
    return f'<div class="card"><div class="card-title">{title}</div>{body}</div>'


def two_col(left, right):
    return f'<div class="two-col">{left}{right}</div>'


def concept_table(headers, rows):
    head = "".join(f"<th>{h}</th>" for h in headers)
    body = "".join(
        "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>" for row in rows
    )
    return f'<table class="concept-table"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>'


def callout_blue(icon, label, body):
    return (
        f'<div class="callout blue"><div class="callout-icon">{icon}</div><div>'
        f'<div class="callout-label">{label}</div><div class="callout-body">{body}</div></div></div>'
    )


def prompt_list(prompts):
    """prompts: list of (title, text, hint)."""
    items = "".join(
        f'<div class="prompt"><div class="p-num">{title}</div><div class="p-text">{text}</div>'
        f'<div class="p-hint">{hint}</div></div>'
        for title, text, hint in prompts
    )
    return f'<div class="prompt-list">{items}</div>'


def assignment(header, title, deliverables):
    """deliverables: list of (icon entity, html)."""
    items = "".join(
        f'<div class="deliverable"><div class="d-icon">{icon}</div><div class="d-text">{text}</div></div>'
        for icon, text in deliverables
    )
    return f'<div class="assignment"><div class="a-header">{header}</div><h3>{title}</h3>{items}</div>'


NO_SCREENSHOTS = (
    "<strong>No screenshots.</strong> Your GitHub repository is the entire submission &mdash; it is "
    "graded by cloning it and running your code and <code>pytest</code>. Make sure the repo is "
    "<strong>Public</strong> and every change is pushed before the deadline."
)


# ── Slides (reveal.js decks) ──────────────────────────────────────────────────


def slides_shell(template):
    """Return (before, after): the deck page around its <div class="slides"> contents."""
    text = (DOCS / template).read_text()
    start = text.index('<div class="slides">') + len('<div class="slides">')
    end = text.rindex("</section>") + len("</section>")
    return text[:start], text[end:]


def notes(text):
    return f'<aside class="notes">{esc(text)}</aside>'


def slide_title(week_label, title, timings, note):
    bar = "".join(
        f'<span class="t-item"><strong>{t}</strong> {what}</span>'
        for t, what in timings
    )
    return (
        '<section class="s-title"><p style="font-family:monospace;font-size:.5em;letter-spacing:.18em;'
        f'text-transform:uppercase;color:var(--mu);margin-bottom:.3em;">ISM3232 &nbsp;·&nbsp; {week_label}</p>'
        f'<h1>{title}</h1><div class="t-bar">{bar}</div>'
        '<p style="font-size:.38em;color:var(--mu);margin-top:.7em;">← → navigate &nbsp;·&nbsp; '
        f"F fullscreen &nbsp;·&nbsp; S notes</p>{notes(note)}</section>"
    )


def slide_section(number, title, note):
    return (
        f'<section class="s-sec"><div class="sec-n">Section {number}</div>'
        f'<h1 style="font-size:1.4em;">{title}</h1>{notes(note)}</section>'
    )


def slide_point(title, bullets, note):
    items = "".join(f"<li>{b}</li>" for b in bullets)
    return (
        f'<section class="s-point"><h2>{title}</h2><ul style="text-align:left;max-width:820px;'
        f'margin:0 auto;">{items}</ul>{notes(note)}</section>'
    )


def slide_code(title, code, note, size=".74em", lang="python"):
    return (
        f'<section class="s-code"><h3 style="color:var(--S);text-align:left;font-size:.52em;'
        f'margin-bottom:.25em;">⌨ {title}</h3><pre><code class="language-{lang}" '
        f'style="max-height:620px;font-size:{size};line-height:1.3;">{esc(code.rstrip())}</code></pre>'
        f"{notes(note)}</section>"
    )


def slide_demo(app, sub, note):
    return (
        '<section class="s-demo"><div class="demo-card"><div class="demo-lbl">⚡ Live Demo</div>'
        '<div style="font-size:2em;margin:.2em 0;">🖥</div>'
        f'<div class="demo-app">{app}</div><div class="demo-sub">{sub}</div></div>{notes(note)}</section>'
    )


def slide_chalk(title, note):
    dots = "".join(
        f'<span class="cdot{" on" if i == 0 else ""}" style="background:{c}" onclick="CC(\'{c}\',this)"></span>'
        for i, c in enumerate(["#fff", "#fcd34d", "#4ade80", "#38bdf8", "#fb7185"])
    )
    return (
        f'<section class="s-chalk"><h3 style="color:#b8921e;">✏ {title}</h3><canvas class="chalk-board"></canvas>'
        f'<div class="chalk-ctrl">{dots}&nbsp;<button class="chalk-btn on" data-sz onclick="CS(4,this)">S</button>'
        '<button class="chalk-btn" data-sz onclick="CS(8,this)">M</button><button class="chalk-btn" data-sz '
        'onclick="CS(14,this)">L</button>&nbsp;<button class="chalk-btn" onclick="CE(this)">Eraser</button>'
        f'<button class="chalk-btn" onclick="CX()">Clear</button></div>{notes(note)}</section>'
    )


# ── Running snippets against a reference folder ──────────────────────────────


def folder_at(rev, folder="reference/ism3232/module06_agents"):
    """Extract `folder` as it was in commit `rev` into a temporary directory; return its path."""
    import subprocess
    import tempfile

    target = Path(tempfile.mkdtemp(prefix="ism3232-"))
    archive = subprocess.run(
        ["git", "archive", rev, folder], cwd=ROOT, capture_output=True, check=True
    )
    subprocess.run(["tar", "-x", "-C", str(target)], input=archive.stdout, check=True)
    return target / folder


def run_snippet(code, folder, stdin=""):
    """Run a standalone snippet inside `folder` and return what it prints."""
    import subprocess
    import sys

    result = subprocess.run(
        [sys.executable, "-B", "-c", code],
        cwd=folder,
        input=stdin,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.rstrip("\n")


def with_output(code, output):
    """The slide convention: the code, a blank line, then '# Output:' and each printed line."""
    lines = "\n".join(f"# {line}" if line else "#" for line in output.split("\n"))
    return f"{code.rstrip()}\n\n# Output:\n{lines}"


SHELL_DRIVER = r"""
import code, contextlib, io, sys
console = code.InteractiveConsole()
for line in sys.stdin.read().split("\n"):
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        console.push(line)
    print(">>> " + line)
    if buffer.getvalue():
        print(buffer.getvalue(), end="")
"""


def shell(lines, folder):
    """A Python shell session as students see it: each typed line after '>>> '
    and whatever it printed, from a real run inside `folder`."""
    import subprocess
    import sys

    result = subprocess.run(
        [sys.executable, "-B", "-c", SHELL_DRIVER],
        cwd=folder,
        input="\n".join(lines),
        capture_output=True,
        text=True,
        check=True,
    )
    return "python3\n" + result.stdout.rstrip("\n") + "\n>>> exit()"


def task(number, title, body):
    return (
        f'<div class="task"><div class="task-num">{number}</div><div class="task-content">'
        f'<div class="task-title">{title}</div><div class="task-body">{body}</div></div></div>'
    )


def expected(text):
    return f'<div class="expected" style="white-space:pre-wrap;">{esc(text.rstrip())}</div>'


def hint(html_text):
    return f'<div class="hint-box">{html_text}</div>'


def callout_box(kind, icon, label, body):
    """kind: 'blue' or 'warn' (lab callouts)."""
    return (
        f'<div class="callout {kind}"><div class="callout-icon">{icon}</div><div>'
        f'<div class="callout-label">{label}</div><div class="callout-body">{body}</div></div></div>'
    )


def reveal(summary, body):
    """A click-to-reveal answer key in the lab style."""
    return (
        '<details style="margin:10px 0 4px;border:1px solid var(--border);border-radius:8px;'
        'padding:10px 14px;background:var(--bg-card);"><summary style="cursor:pointer;font-weight:700;'
        f'color:var(--text-primary);font-size:13px;">{summary}</summary><div style="margin-top:10px;">'
        f"{body}</div></details>"
    )


def check_list(items):
    return (
        '<ul class="check-list">'
        + "".join(f"<li><span>{i}</span></li>" for i in items)
        + "</ul>"
    )


def time_bar(parts):
    return (
        '<div class="time-bar">'
        + "".join(f'<span class="time-block">{p}</span>' for p in parts)
        + "</div>"
    )


def submit_box(header, title, deliverables):
    items = "".join(
        f'<div class="deliverable"><div class="d-icon">{icon}</div><div class="d-text">{text}</div></div>'
        for icon, text in deliverables
    )
    return f'<div class="submit-box"><div class="sb-header">{header}</div><h3>{title}</h3>{items}</div>'
