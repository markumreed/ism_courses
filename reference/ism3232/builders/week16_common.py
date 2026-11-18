"""Facts shared by the Week 16 page builders: titles and links, the Bayside
checkpoint the pages quote (cases.py, evaluation.py, tests/test_cases.py and
README.md), readers for the saved CPU runs, and real pytest output made by
running the checkpoint's tests, including one deliberately weak check."""

import ast
import os
import re
import subprocess
import sys

import runs
from pagekit import REF, folder_at, function, read
from week14_common import pytest_summary

WEEK = "week16"
TITLE = "Evaluation, Safety &amp; Demo — Test Cases, Safety Checks &amp; a Demo Video"
TITLE_TEXT = "Evaluation, Safety & Demo — Test Cases, Safety Checks & a Demo Video"
SHORT = "Evaluation, Safety &amp; Demo"
EYEBROW_COLOR = "#fbbf24"
UNIT = "Unit 4 · Capstone Build"
PREV = (
    "week15",
    "Week 15",
    "Streamlit Chat &amp; Staff — Reruns, Session State &amp; Approvals",
)
NEXT = ("capstone_rubric", "Capstone", "Capstone Rubric")
REV = "4fd7aeb"  # Bayside app, Week 16 checkpoint (tested checks)
OLD_REV = "172d6ad"  # Week 16's first checkpoint; Week 13's proposal reads its cases
APP = "bayside_app/"
APP_FOLDER = "reference/ism3232/bayside_app"
RUNS = REF / "runs" / WEEK
COMMIT = "lab 16: evaluation and safety"

CASE_NAMES = [
    "order lookup",
    "stock check",
    "address change",
    "request status",
    "payment handoff",
    "price match",
    "no order ID",
    "false closing time",
]
WEAK_VALUE = "11 pm"
# The first line of every block that shows the weak check's real pytest output.
WEAK_MARK = '# With "value": "11 pm" in the closing-time case:'
# The keys of runs/week16/safety.py's TRIES, in order. The first five are the
# checklist tries the model answers; the last two are the evidence transcripts.
SAFETY_KEYS = [
    "payment",
    "no_order_id",
    "other_order",
    "closing_time",
    "manager",
    "price_match",
    "address_change",
]

THUMBNAIL = (
    "[![Demo video](https://img.youtube.com/vi/VIDEO_ID/0.jpg)]"
    "(https://www.youtube.com/watch?v=VIDEO_ID)"
)
README_TEMPLATE = f"""# <Business> Support Agent

{THUMBNAIL}

## What it does
## How to run it
## Tools and approvals
## Safety checklist
## Evaluation results
## Limitations
## AI use
"""
SHOTS = [
    "the business problem (about 30 seconds)",
    "a question the agent answers with a tool",
    "a change filed in the chat, approved on the Staff tab, then asked about in the chat",
    "one evaluation failure from the README table, and why it fails",
    "one file explained line by line",
]

BLOCKED_PYTEST = (
    "import sys; sys.modules['ollama'] = None; sys.modules['streamlit'] = None; "
    "import pytest; sys.exit(pytest.main({args!r}))"
)


def app_file(name):
    """A Bayside app file as it was at the Week 16 checkpoint."""
    return read(APP + name, REV)


def app_function(file, name):
    """One top-level function of an app file at the checkpoint, exactly as written."""
    return function(APP + file, name, REV)


def checkpoint_folder():
    """A temporary copy of the Bayside app as it was at the Week 16 checkpoint."""
    return folder_at(REV, APP_FOLDER)


def case_dicts(rev):
    """The CASES list at rev: in cases.py, or in evaluation.py before the split."""
    for name in ("cases.py", "evaluation.py"):
        try:
            text = read(APP + name, rev)
        except subprocess.CalledProcessError:
            continue
        for node in ast.parse(text).body:
            if (
                isinstance(node, ast.Assign)
                and getattr(node.targets[0], "id", None) == "CASES"
            ):
                return ast.literal_eval(node.value)
    raise ValueError(f"no CASES at {rev}")


def blocked_pytest(folder, args):
    """Run pytest in folder with ollama and streamlit blocked, as the autograder
    does; return its output."""
    code = BLOCKED_PYTEST.format(args=["-q", "-p", "no:cacheprovider", *args])
    # A fixed, wide terminal so pytest does not cut the FAILED line short.
    env = {**os.environ, "COLUMNS": "120"}
    result = subprocess.run(
        [sys.executable, "-B", "-c", code],
        cwd=folder,
        capture_output=True,
        text=True,
        check=False,
        env=env,
    )
    return result.stdout


def weak_check_pytest():
    """The real pytest output when the closing-time case says never_says "11 pm":
    the FAILED line(s) and the summary line, without the timing."""
    folder = checkpoint_folder()
    cases = folder / "cases.py"
    text = cases.read_text()
    strong = '"value": "11",'
    if text.count(strong) != 1:
        raise ValueError("expected exactly one closing-time value line")
    cases.write_text(text.replace(strong, f'"value": "{WEAK_VALUE}",'))
    lines = blocked_pytest(folder, ["tests/test_cases.py"]).strip().split("\n")
    failed = [line for line in lines if line.startswith("FAILED ")]
    summary = re.sub(r" in [\d.]+s$", "", lines[-1])
    return "\n".join([*failed, summary])


def checkpoint_pytest():
    """The last line of a real pytest run of the whole checkpoint, without timing."""
    return pytest_summary(checkpoint_folder())


def evaluation_lines():
    return (RUNS / "evaluation.txt").read_text().rstrip().split("\n")


def evaluation_rows():
    """Case name -> 'p/3' from the saved CPU evaluation run."""
    rows = {}
    for line in evaluation_lines()[1:-1]:
        rows[line[:20].strip()] = line[20:].strip()
    return rows


def evaluation_result(name):
    """'p of 3' for one case, from the saved run."""
    passed, runs_count = evaluation_rows()[name].split("/")
    return f"{passed} of {runs_count}"


def evaluation_total():
    """'N of 24' from the saved run's total line."""
    passed, runs_count = evaluation_lines()[-1][20:].strip().split("/")
    return f"{passed} of {runs_count}"


def case_count():
    return len(case_dicts(REV))


def safety_runs(key):
    """The three saved runs of one safety-checklist try."""
    return runs.load(WEEK, f"safety_{key}.txt")
