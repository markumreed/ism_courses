"""Check every Week 12 page without changing it: the page on disk must be exactly
what its builder makes now, and each code block outside the quiz must appear
verbatim in a reference file (guided commit or current), a saved run, or a
derived output.

    python reference/ism3232/builders/verify_week12.py week12_reading.html ...
"""

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import week12_common as w
from pagekit import DOCS, ROOT, check_listings


def sources(extra):
    files = [p for p in w.FOLDER.rglob("*.py") if "__pycache__" not in p.parts]
    current = [f"module06_agents/{p.relative_to(w.FOLDER)}" for p in files]
    listed = subprocess.run(
        [
            "git",
            "ls-tree",
            "-r",
            "--name-only",
            w.GUIDED,
            "reference/ism3232/module06_agents",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.split()
    guided = [
        subprocess.run(
            ["git", "show", f"{w.GUIDED}:{name}"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout
        for name in listed
    ]
    runs = [f"runs/week12/{p.name}" for p in (w.REF / "runs" / "week12").glob("*.txt")]
    return current + guided + runs + list(extra)


# Exercise and mini-project answers: only the lab page (inside its answer keys)
# and the lab slides may show these.
ANSWERS = [
    "check_return",
    "FallbackModel",
    "BookingQueue",
    "AppointmentToolbox",
    "add_booking",
]


def leaked_answers(page):
    if "lab" in page:
        return []
    text = (DOCS / page).read_text()
    return [name for name in ANSWERS if name in text]


def slide_outputs_match(page):
    """Re-run every slide block that shows '# Output:' and compare what it prints."""
    import html
    import re

    from pagekit import folder_at, run_snippet

    text = (DOCS / page).read_text()
    folder = folder_at(w.GUIDED)
    wrong = []
    for match in re.finditer(
        r'<code class="language-python"[^>]*>(.*?)</code>', text, re.DOTALL
    ):
        block = html.unescape(match.group(1))
        if "\n# Output:\n" not in block:
            continue
        code, shown = block.split("\n# Output:\n")
        expected = "\n".join(
            line[2:] if line.startswith("# ") else "" for line in shown.split("\n")
        )
        if run_snippet(code, folder) != expected:
            wrong.append(code.split("\n")[0][:60])
    return wrong


def lab_slide_outputs_match(page):
    """Run each browser-runnable block with CPython in an empty folder and compare
    with the <pre> on the output slide that follows it."""
    import html
    import re
    import tempfile

    from pagekit import run_snippet

    text = (DOCS / page).read_text()
    empty = Path(tempfile.mkdtemp(prefix="ism3232-run-"))
    wrong = []
    for match in re.finditer(
        r'<div class="run" data-lang="python">(.*?)</div>', text, re.DOTALL
    ):
        code = html.unescape(match.group(1))
        shown = re.search(r"<pre>(.*?)</pre>", text[match.end() :], re.DOTALL)
        if shown is None or run_snippet(code, empty) != html.unescape(shown.group(1)):
            wrong.append(code.split("\n")[0][:60])
    return wrong


if __name__ == "__main__":
    import importlib

    derived = []
    stale = []
    for name in (
        "week12_reading",
        "week12_lecture",
        "week12_slides",
        "week12_lab",
        "week12_lab_slides",
    ):
        try:
            module = importlib.import_module(name)
        except ModuleNotFoundError:
            continue
        page, extra = module.build()
        derived += extra
        if (DOCS / f"{name}.html").read_text() != page:
            stale.append(f"{name}.html")
    bad = 0
    if stale:
        print("pages on disk that differ from what their builder makes now:", stale)
        bad += len(stale)
    for page in sys.argv[1:]:
        missing = check_listings(DOCS / page, sources(derived))
        leaks = leaked_answers(page)
        if page.endswith("lab_slides.html"):
            mismatched = lab_slide_outputs_match(page)
            print(page, "runnable blocks whose output slide differs:", mismatched)
            bad += len(mismatched)
        elif "slides" in page:
            mismatched = slide_outputs_match(page)
            print(page, "slide outputs that differ when run:", mismatched)
            bad += len(mismatched)
        print(page, "missing:", missing, "answer leaks:", leaks)
        bad += len(missing) + len(leaks)
    sys.exit(1 if bad else 0)
