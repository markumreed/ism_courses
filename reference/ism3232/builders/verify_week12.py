"""Check every Week 12 page: each code block outside the quiz must appear verbatim
in a reference file (guided commit or current), a saved run, or a derived output.

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


if __name__ == "__main__":
    import week12_reading

    _, derived = week12_reading.build()
    bad = 0
    for page in sys.argv[1:]:
        missing = check_listings(DOCS / page, sources(derived))
        leaks = leaked_answers(page)
        print(page, "missing:", missing, "answer leaks:", leaks)
        bad += len(missing) + len(leaks)
    sys.exit(1 if bad else 0)
