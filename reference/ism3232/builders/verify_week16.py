"""Check the five Week 16 pages without changing them.

Each page on disk must be exactly what its builder makes now. Every code block
must appear verbatim in the Bayside app at the Week 16 checkpoint, a saved run
in runs/week16, or text a builder derived. Every block that shows the weak
check's pytest output must show what pytest really prints. The lab's own
cases.py, tests/test_cases.py and evaluation.py blocks, dropped into the Week 15
Bayside app, must pass ruff and pytest with ollama and streamlit blocked. The
quiz must import cleanly. Bayside must pass check.py and its evaluation checks,
and when the unpublished Spokewell build exists, so must it.

    python reference/ism3232/builders/verify_week16.py
"""

import importlib
import importlib.util
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import week16_common as w
from pagekit import DOCS, REF, ROOT, check_listings, files_at, folder_at
from verify_week13 import BLOCK, expected_misses, plain, quiz_problems

PAGES = [
    "week16_reading",
    "week16_lecture",
    "week16_slides",
    "week16_lab",
    "week16_lab_slides",
]
LAB_FILES = ["cases.py", "tests/test_cases.py", "evaluation.py"]
WEEK15_REV = "8b1b491"  # the Bayside app before evaluation.py existed
SPOKEWELL = REF / "_private" / "spokewell"
PRE = re.compile(r"<pre[^>]*>(.*?)</pre>", re.DOTALL)


def run(args, cwd):
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True, check=False)


def last_line(text):
    lines = text.strip().split("\n")
    return lines[-1] if lines else ""


def lint_and_test_problems(folder):
    """ruff format, ruff check and blocked pytest in folder, as tools/check.py runs
    them; each failing step is reported by name with its last line."""
    steps = [
        (
            "ruff format",
            [sys.executable, "-m", "ruff", "format", "--isolated", "--check", "."],
        ),
        (
            "ruff check",
            [sys.executable, "-m", "ruff", "check", "--isolated", "--no-cache", "."],
        ),
    ]
    for name, args in steps:
        result = run(args, folder)
        if result.returncode != 0:
            return [f"{name} failed: {last_line(result.stdout + result.stderr)}"]
    last = last_line(w.blocked_pytest(folder, []))
    if "failed" in last or "error" in last or not re.search(r"\d+ passed", last):
        return [f"pytest failed: {last}"]
    return []


def lab_rebuild_problems(lab_text):
    """Drop the lab page's three blocks into the Week 15 Bayside app and run the
    autograder's checks there."""
    blocks = {plain(label): plain(code) for label, code in BLOCK.findall(lab_text)}
    missing = [name for name in LAB_FILES if name not in blocks]
    if missing:
        return [f"lab block missing from the page: {name}" for name in missing]
    folder = folder_at(WEEK15_REV, w.APP_FOLDER)
    for name in LAB_FILES:
        (folder / name).write_text(blocks[name].rstrip() + "\n")
    return [f"lab rebuild: {problem}" for problem in lint_and_test_problems(folder)]


def weak_output_problems(text):
    """Every block that starts with the weak-check marker must continue with the
    real pytest output."""
    want = w.weak_check_pytest()
    wrong = []
    for raw in PRE.findall(text):
        block = plain(raw)
        shown = block[len(w.WEAK_MARK) + 1 :].rstrip()
        if block.startswith(w.WEAK_MARK + "\n") and shown != want:
            wrong.append("weak-check output differs from what pytest prints")
    return wrong


def run_sources():
    return [path.read_text() for path in sorted(w.RUNS.glob("*.txt"))]


def page_problems(name):
    """Every check that concerns one page, each problem prefixed with its name."""
    page, derived = importlib.import_module(name).build()
    path = DOCS / f"{name}.html"
    on_disk = path.read_text() if path.is_file() else ""
    bad = []
    if on_disk != page:
        bad.append("differs from what its builder makes now")
    sources = [*files_at(w.REV, w.APP_FOLDER), *run_sources(), *derived]
    bad += [f"in no source: {m}" for m in check_listings(path, sources)]
    if name in ("week16_reading", "week16_lecture", "week16_slides"):
        bad += weak_output_problems(on_disk)
    if name == "week16_lab":
        bad += lab_rebuild_problems(on_disk)
        allowed = {w.weak_check_pytest(), w.checkpoint_pytest(), *derived}
        bad += [f"not real output: {m}" for m in expected_misses(on_disk, allowed)]
    if name == "week16_reading":
        bad += quiz_problems(path)
    return [f"{name}: {problem}" for problem in bad]


def bayside_problems():
    """Bayside passes check.py and its evaluation checks."""
    problems = []
    check = run(
        [
            sys.executable,
            "-B",
            str(REF / "tools" / "check.py"),
            str(REF / "bayside_app"),
        ],
        ROOT,
    )
    if check.returncode != 0:
        problems.append("bayside: check.py failed: " + last_line(check.stdout))
    tests = REF / "bayside_dev_tests" / "test_evaluation.py"
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
        problems.append(
            "bayside: evaluation checks failed: " + last_line(result.stdout)
        )
    return problems


def spokewell_problems():
    """The unpublished Spokewell build follows Lab 16: check.py passes with 20+
    tests, 8+ cases, 3+ case tests, evaluation.py imports cases, smoke.py runs."""
    if not SPOKEWELL.is_dir():
        return []
    problems = []
    check = run(
        [sys.executable, "-B", str(REF / "tools" / "check.py"), str(SPOKEWELL)], ROOT
    )
    if check.returncode != 0:
        problems.append("spokewell: check.py failed: " + last_line(check.stdout))
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
    if not found or int(found.group(1)) < 20:
        problems.append("spokewell: fewer than 20 tests")
    cases_file = SPOKEWELL / "cases.py"
    if not cases_file.is_file():
        problems.append("spokewell: no cases.py")
    else:
        sys.path.insert(0, str(SPOKEWELL))
        try:
            spec = importlib.util.spec_from_file_location("spokewell_cases", cases_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if len(module.CASES) < 8:
                problems.append("spokewell: fewer than 8 cases")
        finally:
            sys.path.remove(str(SPOKEWELL))
    test_file = SPOKEWELL / "tests" / "test_cases.py"
    if not test_file.is_file() or test_file.read_text().count("\ndef test_") < 3:
        problems.append("spokewell: fewer than 3 tests in tests/test_cases.py")
    evaluation = SPOKEWELL / "evaluation.py"
    if not evaluation.is_file() or "from cases import" not in evaluation.read_text():
        problems.append("spokewell: evaluation.py does not import cases")
    smoke = run([sys.executable, "-B", "smoke.py"], SPOKEWELL)
    if smoke.returncode != 0:
        problems.append("spokewell: smoke.py failed: " + smoke.stdout.strip()[-200:])
    return problems


def main():
    bad = []
    for name in PAGES:
        bad += page_problems(name)
    bad += bayside_problems()
    bad += spokewell_problems()
    for line in bad:
        print(line)
    print("verify_week16:", "OK" if not bad else f"{len(bad)} problem(s)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
