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
    for match in re.finditer(r"<pre><code>(.*?)</code></pre>", text, re.DOTALL):
        code = html.unescape(re.sub(r"<[^>]+>", "", match.group(1)))
        if code.strip() and code not in pool:
            missing.append(code.split("\n")[0][:70])
    return missing
