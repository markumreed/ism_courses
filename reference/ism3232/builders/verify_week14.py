"""Check the five Week 14 pages without changing them.

Each page on disk must be exactly what its builder makes now. Every code block
must appear verbatim in the Bayside app at the Week 14 checkpoint, a saved run,
or text a builder derived. Every slide snippet must print what its slide shows.
The lab's warm-up, rebuilt from the lab page alone, must print every expected
box. The quiz must import cleanly. When the unpublished Spokewell build exists,
it must pass check.py and its smoke test.

    python reference/ism3232/builders/verify_week14.py
"""

import html
import importlib
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import week14_common as w
from pagekit import DOCS, REF, ROOT, check_listings, run_snippet, shell
from verify_week13 import expected_misses, plain, quiz_problems

PAGES = [
    "week14_reading",
    "week14_lecture",
    "week14_slides",
    "week14_lab",
    "week14_lab_slides",
]
SPOKEWELL = REF / "_private" / "spokewell"
BLOCK = re.compile(r'<div class="cb-label">(.*?)</div><pre>(.*?)</pre>', re.DOTALL)
EXPECTED = re.compile(
    r'<div class="[^"]*\bexpected\b[^"]*"[^>]*>(.*?)</div>', re.DOTALL
)


def checkpoint_sources():
    """Every file of the Bayside app at the Week 14 checkpoint, as text."""
    names = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", w.REV, w.APP_FOLDER],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.split()
    return [
        subprocess.run(
            ["git", "show", f"{w.REV}:{name}"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout
        for name in names
    ]


def slide_problems(text):
    """Re-run every slide block that shows '# Output:' and compare what it prints."""
    wrong = []
    for match in re.finditer(
        r'<code class="language-python"[^>]*>(.*?)</code>', text, re.DOTALL
    ):
        block = html.unescape(match.group(1))
        if "\n# Output:\n" not in block:
            continue
        code, shown = block.split("\n# Output:\n")
        want = "\n".join(
            line[2:] if line.startswith("# ") else "" for line in shown.split("\n")
        )
        if run_snippet(code, w.checkpoint_folder()) != want:
            wrong.append(code.split("\n")[0][:60])
    return wrong


def warmup_problems(lab_text):
    """Rebuild the warm-up from the lab page's own blocks and compare its output
    with the page's expected boxes. tests/__init__.py exists only if the page's
    warm-up terminal block makes it."""
    found = [(plain(label), plain(code)) for label, code in BLOCK.findall(lab_text)]
    blocks = dict(found)
    missing = [key for key, label in w.LABELS.items() if label not in blocks]
    terminal = [
        code for label, code in found if label == "Terminal" and "sql_practice" in code
    ]
    if not terminal:
        missing.append("terminal")
    if missing:
        return [f"warm-up block missing from the page: {key}" for key in missing]
    get = {key: blocks[label] for key, label in w.LABELS.items()}
    files = {
        "schema.sql": w.app_file("schema.sql"),
        "database.py": get["db_top"] + "\n\n\n" + get["db_find"] + "\n",
        "tools.py": get["tools"] + "\n",
        "tests/test_database.py": get["test_top"] + "\n\n\n" + get["test_find"] + "\n",
    }
    if "touch tests/__init__.py" in terminal[0]:
        files["tests/__init__.py"] = ""
    folder = w.build_folder(files)
    outputs = [shell(get["shell"].split("\n"), folder), w.pytest_summary(folder)]
    boxes = [plain(box).rstrip() for box in EXPECTED.findall(lab_text)]
    return [
        f"no expected box shows: {out.split(chr(10))[0][:60]}"
        for out in outputs
        if out.rstrip() not in boxes
    ]


def spokewell_problems():
    """The unpublished Spokewell build passes check.py and its smoke test."""
    if not SPOKEWELL.is_dir():
        return []
    problems = []
    check = subprocess.run(
        [sys.executable, "-B", str(REF / "tools" / "check.py"), str(SPOKEWELL)],
        capture_output=True,
        text=True,
        check=False,
    )
    if check.returncode != 0:
        problems.append(
            "spokewell: check.py failed: " + check.stdout.strip().split("\n")[-1]
        )
    count = subprocess.run(
        [
            sys.executable,
            "-B",
            "-m",
            "pytest",
            "--collect-only",
            "-q",
            "-p",
            "no:cacheprovider",
        ],
        cwd=SPOKEWELL,
        capture_output=True,
        text=True,
        check=False,
    ).stdout
    found = re.search(r"(\d+) tests? collected", count)
    if not found or int(found.group(1)) < 12:
        problems.append("spokewell: fewer than 12 tests")
    smoke = subprocess.run(
        [sys.executable, "-B", "smoke.py"],
        cwd=SPOKEWELL,
        capture_output=True,
        text=True,
        check=False,
    )
    if smoke.returncode != 0:
        problems.append("spokewell: smoke.py failed: " + smoke.stdout.strip()[-200:])
    return problems


def main():
    bad, derived, texts = [], [], {}
    for name in PAGES:
        page, extra = importlib.import_module(name).build()
        derived += extra
        texts[name] = (DOCS / f"{name}.html").read_text()
        if texts[name] != page:
            bad.append(f"{name}.html differs from what its builder makes now")
    sources = [
        *checkpoint_sources(),
        *[p.read_text() for p in sorted(w.RUNS.glob("*.txt"))],
        *derived,
    ]
    for name in PAGES:
        bad += [
            f"{name}: in no source: {m}"
            for m in check_listings(DOCS / f"{name}.html", sources)
        ]
    for name in ("week14_slides", "week14_lecture"):
        bad += [
            f"{name}: slide output differs: {m}" for m in slide_problems(texts[name])
        ]
    bad += [f"week14_lab: {p}" for p in warmup_problems(texts["week14_lab"])]
    allowed = {w.warmup_shell(), w.warmup_pytest()}
    bad += [
        f"week14_lab: not real output: {m}"
        for m in expected_misses(texts["week14_lab"], allowed)
    ]
    bad += [f"week14_reading: {p}" for p in quiz_problems(DOCS / "week14_reading.html")]
    bad += spokewell_problems()
    for line in bad:
        print(line)
    print("verify_week14:", "OK" if not bad else f"{len(bad)} problem(s)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
