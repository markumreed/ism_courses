"""Check the five Week 15 pages without changing them.

Each page on disk must be exactly what its builder makes now. Every code block
must appear verbatim in the Bayside app at the Week 15 checkpoint, the saved
browser session, or text a builder derived. Every counter slide must show what
its app shows after that many clicks. The lab's warm-up, rebuilt from the lab
page alone and driven through Streamlit's test tool, must give every expected
box. Every screenshot a page shows must exist. The quiz must import cleanly.
Bayside's app checks must pass, and when the unpublished Spokewell build
exists, it must pass check.py, its smoke test and its app checks.

    python reference/ism3232/builders/verify_week15.py
"""

import html
import importlib
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import week15_common as w
from pagekit import DOCS, REF, ROOT, check_listings, files_at
from verify_week13 import expected_misses, plain, quiz_problems
from verify_week14 import BLOCK, EXPECTED

PAGES = [
    "week15_reading",
    "week15_lecture",
    "week15_slides",
    "week15_lab",
    "week15_lab_slides",
]
SPOKEWELL = REF / "_private" / "spokewell"
SPOKEWELL_TESTS = REF / "_private" / "spokewell_dev_tests"
CLICKS_MARK = re.compile(r"\n# After (\d+) clicks the page shows:\n")


def run(args, cwd):
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True, check=False)


def counter_slide_problems(text):
    """Re-run every slide block that shows what a page looks like after clicks."""
    wrong = []
    for match in re.finditer(
        r'<code class="language-python"[^>]*>(.*?)</code>', text, re.DOTALL
    ):
        block = html.unescape(match.group(1))
        mark = CLICKS_MARK.search(block)
        if mark is None:
            continue
        code, shown = block[: mark.start()], block[mark.end() :]
        want = "\n".join(line[2:] for line in shown.split("\n"))
        if w.counter_after_clicks(code, int(mark.group(1))) != want:
            wrong.append(code.split("\n")[0][:60])
    return wrong


def warmup_problems(lab_text):
    """Rebuild the warm-up from the lab page's own blocks, drive each app with
    the test tool, and compare the results with the page's expected boxes."""
    blocks = {plain(label): plain(code) for label, code in BLOCK.findall(lab_text)}
    missing = [label for label in w.LABELS.values() if label not in blocks]
    if missing:
        return [f"warm-up block missing from the page: {label}" for label in missing]
    counter, kept = blocks["counter.py"], blocks["counter_state.py"]
    results = [
        w.counter_after_clicks(counter, w.CLICKS),
        w.counter_after_clicks(kept, w.CLICKS),
        w.counter_after_clicks(kept, 0),
        w.echo_bubbles(blocks["echo.py"], w.ECHO_MESSAGES),
    ]
    boxes = [plain(box).rstrip() for box in EXPECTED.findall(lab_text)]
    return [
        f"no expected box shows: {result.split(chr(10))[0][:60]}"
        for result in results
        if result.rstrip() not in boxes
    ]


def image_problems(text):
    """Every Week 15 screenshot a page shows must exist."""
    names = re.findall(r'src="\.\./assets/img/week15/([^"]+)"', text)
    return [
        f"missing screenshot: {name}"
        for name in names
        if not (w.IMAGES / name).is_file()
    ]


def page_problems(name):
    """Every check that concerns one page, each problem prefixed with its name."""
    page, derived = importlib.import_module(name).build()
    path = DOCS / f"{name}.html"
    on_disk = path.read_text() if path.is_file() else ""
    bad = []
    if on_disk != page:
        bad.append("differs from what its builder makes now")
    sources = [
        *files_at(w.REV, w.APP_FOLDER),
        (w.RUNS / "session.txt").read_text(),
        *derived,
    ]
    bad += [f"in no source: {m}" for m in check_listings(path, sources)]
    bad += image_problems(on_disk)
    if name in ("week15_slides", "week15_lecture"):
        bad += [f"counter slide differs: {m}" for m in counter_slide_problems(on_disk)]
    if name == "week15_lab":
        bad += warmup_problems(on_disk)
        allowed = set(w.warmup_results().values())
        bad += [f"not real output: {m}" for m in expected_misses(on_disk, allowed)]
    if name == "week15_reading":
        bad += quiz_problems(path)
    return [f"{name}: {problem}" for problem in bad]


def bayside_app_problems():
    """Bayside's Streamlit app checks pass (run from the repo root, as their
    docstring says)."""
    tests = REF / "bayside_dev_tests" / "test_app.py"
    result = run(
        [
            sys.executable,
            "-B",
            "-m",
            "pytest",
            "-q",
            "-p",
            "no:cacheprovider",
            str(tests),
        ],
        ROOT,
    )
    if result.returncode != 0:
        return ["bayside app checks failed: " + result.stdout.strip().split("\n")[-1]]
    return []


def spokewell_problems():
    """The unpublished Spokewell build passes check.py with 15+ tests, its smoke
    test, and its app checks."""
    if not SPOKEWELL.is_dir():
        return []
    problems = []
    check = run(
        [sys.executable, "-B", str(REF / "tools" / "check.py"), str(SPOKEWELL)], ROOT
    )
    if check.returncode != 0:
        problems.append(
            "spokewell: check.py failed: " + check.stdout.strip().split("\n")[-1]
        )
    count = run(
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
        SPOKEWELL,
    ).stdout
    found = re.search(r"(\d+) tests? collected", count)
    if not found or int(found.group(1)) < 15:
        problems.append("spokewell: fewer than 15 tests")
    smoke = run([sys.executable, "-B", "smoke.py"], SPOKEWELL)
    if smoke.returncode != 0:
        problems.append("spokewell: smoke.py failed: " + smoke.stdout.strip()[-200:])
    apps = run(
        [
            sys.executable,
            "-B",
            "-m",
            "pytest",
            "-q",
            "-p",
            "no:cacheprovider",
            str(SPOKEWELL_TESTS),
        ],
        ROOT,
    )
    if apps.returncode != 0:
        problems.append(
            "spokewell: app checks failed: " + apps.stdout.strip().split("\n")[-1]
        )
    return problems


def main():
    bad = []
    for name in PAGES:
        bad += page_problems(name)
    bad += bayside_app_problems()
    bad += spokewell_problems()
    for line in bad:
        print(line)
    print("verify_week15:", "OK" if not bad else f"{len(bad)} problem(s)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
