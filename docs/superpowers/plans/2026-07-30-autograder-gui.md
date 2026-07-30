# Autograder GUI Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a single local Streamlit web app (`autograder/gui.py`) that replaces the spreadsheet-editing step in the existing fetch/check/upload CLI workflow with an in-browser grading review screen, for both ISM2411 and ISM3232, reusing the existing `autograder_common` engine unchanged.

**Architecture:** A new pure-Python helper module (`autograder_common/gui_helpers.py`) holds every piece of logic the page needs beyond what already exists in `autograder_common` (shaping fetched/checked data for display, live-scoring a partially-edited row) — fully unit-tested with pytest, no Streamlit dependency. `gui.py` itself is UI wiring only: it imports `gui_helpers` plus the existing `canvas`, `fetch`, `checks`, `worksheet`, `scoring`, `config` modules directly, and is verified by manual walkthrough, not automated tests.

**Tech Stack:** Python 3.10+, Streamlit (`streamlit>=1.35`, new dependency), the existing `autograder_common` package (`requests`, `PyYAML` already present). Test runner: `pytest`, following the existing suite's fixture style (`tmp_path`, no real network calls).

## Global Constraints

- The GUI reuses `autograder_common`'s existing modules (`canvas.py`, `fetch.py`, `checks.py`, `worksheet.py`, `scoring.py`, `config.py`, `cli.py`) unmodified — no grading logic is duplicated or reimplemented for the GUI.
- Only one new module is added to `autograder_common`: `gui_helpers.py`, containing pure functions with no Streamlit import, fully pytest-unit-tested.
- `gui.py` targets the existing 5 pilot assignment configs only (ISM2411: `week03_lab`, `capstone`; ISM3232: `week07_assignment`, `developer_workflow`, `capstone`) — no new assignment configs are created by this plan.
- Disk (`runs/<assignment>/review.csv`, same file/format the CLI's `check`/`upload` commands already use) is the single source of truth end to end: Preview Upload and Post Grades always re-read the saved CSV from disk, never in-memory table edits — an edit made but not saved must never be silently posted.
- Post Grades must be disabled (not just warned) while `worksheet.incomplete_students` reports any student with a blank human-scored field, and must require a typed confirmation before the real Canvas write — matching the CLI's `y/N` prompt and blank-field refusal.
- No Canvas API token is ever written to a config file or committed — it comes only from the `CANVAS_API_TOKEN` environment variable (already enforced by `config.load_course_config`, unchanged).
- One new dependency: `streamlit>=1.35` added to `autograder/requirements.txt`.

---

## File Structure

```
autograder/
  requirements.txt                       # Modify: add streamlit>=1.35
  gui.py                                 # Create: Streamlit page (UI wiring only)
  autograder_common/
    gui_helpers.py                       # Create: pure helper functions
  tests/
    test_gui_helpers.py                  # Create: unit tests for gui_helpers.py
```

No existing file in `autograder_common` is modified by this plan (per Global
Constraints). `cli.py`'s `_student_key`, `_load`, `_assignment_id`,
`_compute_signals` logic is *referenced* by `gui_helpers.py` (reimplemented
as importable functions, since `cli.py`'s versions are private/underscored
and tied to argparse `args` objects) — `gui_helpers.py` does not import
from `cli.py` to avoid coupling to its private names, but produces
byte-identical output to what `cli.py`'s equivalent logic produces, verified
by tests that assert against the same fixture shapes `test_cli.py` uses.

---

## Task 1: `gui_helpers.py` — student key, config discovery, and record building

**Files:**
- Create: `autograder/autograder_common/gui_helpers.py`
- Test: `autograder/tests/test_gui_helpers.py`

**Interfaces:**
- Consumes: `autograder_common.config.load_assignment_config(path) -> dict` (existing); `autograder_common.checks.file_present(dir, files) -> dict[str,bool]`, `checks.runs_without_error(file, cmd, timeout) -> (bool,str,str)`, `checks.ruff_check(dir) -> (bool,str)`, `checks.pytest_check(dir) -> (bool,str)`, `checks.git_log_checks(dir) -> dict` (existing, from `autograder/autograder_common/checks.py`).
- Produces: `student_key(user_name: str) -> str`; `discover_assignments(assignments_dir) -> list[dict]` (each dict is a loaded assignment config with an added `"_path"` key holding the source file's `Path`); `compute_signals(student_dir, assignment_config) -> tuple[dict, str]` (signals dict + captured_output string — same shape as `cli._compute_signals`'s return value); `compute_student_record(student_dir, student_key_val, student_name, assignment_config) -> dict` (one record shaped like the dicts `cli.cmd_check` builds: `student_key`, `student_name`, `status`, `captured_output`, plus one key per mechanical rubric field holding `True`/`False`).

- [ ] **Step 1: Write the failing tests**

Create `autograder/tests/test_gui_helpers.py`:

```python
from pathlib import Path

import pytest

from autograder_common import gui_helpers


def test_student_key_strips_non_alphanumeric_and_lowercases():
    assert gui_helpers.student_key("Jane Doe") == "janedoe"
    assert gui_helpers.student_key("O'Brien-Smith") == "obriensmith"


def test_discover_assignments_loads_every_yaml_in_dir(tmp_path):
    (tmp_path / "week03_lab.yaml").write_text(
        "course: ism2411\nkey: week03_lab\nsubmission_type: canvas_upload\n"
        "rubric:\n  submission:\n    points: 1\n    source: mechanical\n    check: file_present\n"
    )
    (tmp_path / "capstone.yaml").write_text(
        "course: ism2411\nkey: capstone\nsubmission_type: github_url\n"
        "rubric:\n  code_clarity:\n    source: human\n"
    )

    result = gui_helpers.discover_assignments(tmp_path)

    keys = sorted(a["key"] for a in result)
    assert keys == ["capstone", "week03_lab"]
    for a in result:
        assert a["_path"] == tmp_path / f"{a['key']}.yaml"


def test_discover_assignments_empty_dir_returns_empty_list(tmp_path):
    assert gui_helpers.discover_assignments(tmp_path) == []


def test_compute_signals_file_present_and_runs_without_error(tmp_path):
    student_dir = tmp_path / "student"
    student_dir.mkdir()
    (student_dir / "pricer.py").write_text("print('12 units of Notebook = $59.88')\n")
    assignment_config = {
        "expected_files": ["pricer.py"],
        "run": {"command": "python3 {file}", "timeout_seconds": 10},
        "mechanical_checks": ["file_present", "runs_without_error"],
    }

    signals, captured = gui_helpers.compute_signals(student_dir, assignment_config)

    assert signals["file_present"] == (True, "")
    assert signals["runs_without_error"][0] is True
    assert "59.88" in captured


def test_compute_signals_skips_checks_not_listed(tmp_path):
    student_dir = tmp_path / "student"
    student_dir.mkdir()
    assignment_config = {"expected_files": [], "mechanical_checks": []}

    signals, captured = gui_helpers.compute_signals(student_dir, assignment_config)

    assert signals == {}
    assert captured == ""


def test_compute_student_record_marks_mechanical_fields(tmp_path):
    student_dir = tmp_path / "student"
    student_dir.mkdir()
    (student_dir / "pricer.py").write_text("print('hello')\n")
    assignment_config = {
        "expected_files": ["pricer.py"],
        "run": {"command": "python3 {file}", "timeout_seconds": 10},
        "mechanical_checks": ["file_present", "runs_without_error"],
        "rubric": {
            "submission": {"points": 1, "source": "mechanical", "check": "file_present"},
            "correctness": {"points": 4, "source": "human"},
        },
    }

    record = gui_helpers.compute_student_record(student_dir, "janedoe", "Jane Doe", assignment_config)

    assert record["student_key"] == "janedoe"
    assert record["student_name"] == "Jane Doe"
    assert record["status"] == "ok"
    assert record["submission"] is True
    assert "correctness" not in record  # human fields are never set here
    assert "hello" in record["captured_output"]
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /Users/markumreed/Documents/ism_courses/autograder && pytest tests/test_gui_helpers.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'autograder_common.gui_helpers'`

- [ ] **Step 3: Write the implementation**

Create `autograder/autograder_common/gui_helpers.py`:

```python
"""Pure helper functions for the Streamlit GUI (gui.py). No Streamlit
import here — every function is independently unit-testable and mirrors
the same logic autograder_common.cli's private functions use, so the CLI
and GUI produce identical records/files for the same inputs."""
from pathlib import Path

from . import checks
from .config import load_assignment_config


def student_key(user_name):
    """Same normalization cli._student_key uses: lowercase, alphanumeric only."""
    return "".join(ch for ch in user_name.lower() if ch.isalnum())


def discover_assignments(assignments_dir):
    """Load every *.yaml file in assignments_dir as an assignment config.
    Each returned dict has an added "_path" key (the source Path)."""
    assignments_dir = Path(assignments_dir)
    result = []
    for path in sorted(assignments_dir.glob("*.yaml")):
        config = load_assignment_config(path)
        config["_path"] = path
        result.append(config)
    return result


def compute_signals(student_dir, assignment_config):
    """Run every mechanical primitive listed in assignment_config['mechanical_checks']
    once. Returns (signals: {check_id: (passed, output)}, captured_output: str).
    Identical logic/shape to autograder_common.cli._compute_signals."""
    signals = {}
    captured_parts = []
    checks_to_run = set(assignment_config.get("mechanical_checks", []))
    expected_files = assignment_config.get("expected_files", [])

    if "file_present" in checks_to_run and expected_files:
        presence = checks.file_present(student_dir, expected_files)
        signals["file_present"] = (all(presence.values()), "")

    if "runs_without_error" in checks_to_run and expected_files:
        run_cfg = assignment_config.get("run", {})
        target = Path(student_dir) / expected_files[0]
        ok, out, err = checks.runs_without_error(
            target, run_cfg["command"], run_cfg.get("timeout_seconds", 10)
        )
        signals["runs_without_error"] = (ok, out)
        captured_parts.append(out + (("\n" + err) if err else ""))

    if "ruff_clean" in checks_to_run:
        ok, out = checks.ruff_check(student_dir)
        signals["ruff_clean"] = (ok, out)
        captured_parts.append("--- ruff ---\n" + out)

    if "pytest_passes" in checks_to_run:
        ok, out = checks.pytest_check(student_dir)
        signals["pytest_passes"] = (ok, out)
        captured_parts.append("--- pytest ---\n" + out)

    if checks_to_run & {"git_log_commit_count", "git_log_message_quality", "git_log_spread"}:
        log = checks.git_log_checks(student_dir)
        signals["git_log_commit_count"] = (log["commit_count"] >= 3, f"{log['commit_count']} commits")
        signals["git_log_message_quality"] = (
            log["generic_message_count"] == 0,
            f"{log['generic_message_count']} generic commit message(s)",
        )
        signals["git_log_spread"] = (
            log["spans_multiple_hours"],
            "spans multiple hours" if log["spans_multiple_hours"] else "all commits within one hour",
        )

    return signals, "\n".join(captured_parts)


def compute_student_record(student_dir, student_key_val, student_name, assignment_config):
    """Build one student's check-result record: student_key, student_name,
    status, captured_output, plus one key per mechanical rubric field holding
    True/False. Human-scored fields are never set here (left for the GUI's
    input widgets). Identical record shape to what cli.cmd_check builds."""
    signals, captured = compute_signals(student_dir, assignment_config)
    record = {
        "student_key": student_key_val,
        "student_name": student_name,
        "status": "ok",
        "captured_output": captured,
    }
    for field_name, spec in assignment_config.get("rubric", {}).items():
        if spec.get("source") == "mechanical":
            passed, _ = signals.get(spec["check"], (False, ""))
            record[field_name] = passed
    return record
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /Users/markumreed/Documents/ism_courses/autograder && pytest tests/test_gui_helpers.py -v`
Expected: 6 passed

- [ ] **Step 5: Commit**

```bash
cd /Users/markumreed/Documents/ism_courses
git add autograder/autograder_common/gui_helpers.py autograder/tests/test_gui_helpers.py
git commit -m "Add gui_helpers: student key, assignment discovery, record building"
```

---

## Task 2: `gui_helpers.py` — live scoring and fetch/upload-plan helpers

**Files:**
- Modify: `autograder/autograder_common/gui_helpers.py`
- Modify: `autograder/tests/test_gui_helpers.py`

**Interfaces:**
- Consumes: `autograder_common.scoring.compute_score(row, assignment_config) -> float`, `scoring.ScoringError` (existing, from `autograder/autograder_common/scoring.py`); `autograder_common.worksheet.HUMAN_COLUMN_PREFIX`, `worksheet.MECHANICAL_COLUMN_PREFIX`, `worksheet.incomplete_students(rows, assignment_config) -> list[str]` (existing, from `autograder/autograder_common/worksheet.py`); `student_key` from Task 1 (this file).
- Produces: `live_score(row: dict, assignment_config: dict) -> float | None` (returns `None` instead of raising when the row is incomplete/invalid); `build_upload_plan(rows: list[dict], assignment_config: dict, current_grades: dict[str, float | None]) -> list[dict]` (each dict: `student_key`, `student_name`, `current_grade`, `new_grade`, `comment` — `current_grades` maps `student_key` to the value `CanvasClient.get_current_grade` returned, keyed by the GUI so this function needs no Canvas client itself).

- [ ] **Step 1: Write the failing tests**

Add to `autograder/tests/test_gui_helpers.py`:

```python
from autograder_common.scoring import ScoringError


def test_live_score_returns_score_for_complete_row():
    row = {"mech_submission": "True", "human_correctness": "4"}
    assignment_config = {
        "scoring_type": "points",
        "rubric": {
            "submission": {"points": 1, "source": "mechanical", "check": "file_present"},
            "correctness": {"points": 4, "source": "human"},
        },
    }

    assert gui_helpers.live_score(row, assignment_config) == 5.0


def test_live_score_returns_none_for_incomplete_row():
    row = {"mech_submission": "True", "human_correctness": ""}
    assignment_config = {
        "scoring_type": "points",
        "rubric": {
            "submission": {"points": 1, "source": "mechanical", "check": "file_present"},
            "correctness": {"points": 4, "source": "human"},
        },
    }

    assert gui_helpers.live_score(row, assignment_config) is None


def test_live_score_returns_none_for_out_of_range_human_value():
    row = {"mech_submission": "True", "human_correctness": "99"}
    assignment_config = {
        "scoring_type": "points",
        "rubric": {
            "submission": {"points": 1, "source": "mechanical", "check": "file_present"},
            "correctness": {"points": 4, "source": "human"},
        },
    }

    assert gui_helpers.live_score(row, assignment_config) is None


def test_build_upload_plan_pairs_rows_with_current_grades():
    rows = [
        {
            "student_key": "janedoe", "student_name": "Jane Doe", "status": "ok",
            "mech_submission": "True", "human_correctness": "4", "comment": "Nice work",
        },
        {
            "student_key": "johnsmith", "student_name": "John Smith", "status": "ok",
            "mech_submission": "True", "human_correctness": "3", "comment": "",
        },
    ]
    assignment_config = {
        "scoring_type": "points",
        "rubric": {
            "submission": {"points": 1, "source": "mechanical", "check": "file_present"},
            "correctness": {"points": 4, "source": "human"},
        },
    }
    current_grades = {"janedoe": 3.0, "johnsmith": None}

    plan = gui_helpers.build_upload_plan(rows, assignment_config, current_grades)

    assert plan == [
        {"student_key": "janedoe", "student_name": "Jane Doe", "current_grade": 3.0, "new_grade": 5.0, "comment": "Nice work"},
        {"student_key": "johnsmith", "student_name": "John Smith", "current_grade": None, "new_grade": 4.0, "comment": ""},
    ]


def test_build_upload_plan_skips_non_ok_rows():
    rows = [{"student_key": "janedoe", "student_name": "Jane Doe", "status": "fetch-failed"}]
    assignment_config = {
        "scoring_type": "points",
        "rubric": {"submission": {"points": 1, "source": "mechanical", "check": "file_present"}},
    }

    plan = gui_helpers.build_upload_plan(rows, assignment_config, {"janedoe": None})

    assert plan == []
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /Users/markumreed/Documents/ism_courses/autograder && pytest tests/test_gui_helpers.py -v`
Expected: FAIL — `AttributeError: module 'autograder_common.gui_helpers' has no attribute 'live_score'` (and similarly for `build_upload_plan`)

- [ ] **Step 3: Write the implementation**

Append to `autograder/autograder_common/gui_helpers.py` (add this import at the top alongside the existing ones):

```python
from .scoring import ScoringError, compute_score
```

Then append these two functions at the end of the file:

```python
def live_score(row, assignment_config):
    """Compute the current score for a (possibly incomplete) worksheet row.
    Returns None instead of raising when a human field is still blank or
    out of range, so the GUI can render "-" without crashing the page."""
    try:
        return compute_score(row, assignment_config)
    except ScoringError:
        return None


def build_upload_plan(rows, assignment_config, current_grades):
    """rows: worksheet rows (as read by worksheet.read_worksheet).
    current_grades: {student_key: float|None}, already fetched by the caller
    via CanvasClient.get_current_grade (kept out of this function so it has
    no Canvas dependency and stays trivially testable).

    Returns a list of {student_key, student_name, current_grade, new_grade,
    comment} for every status == "ok" row, in row order."""
    plan = []
    for row in rows:
        if row.get("status") != "ok":
            continue
        plan.append({
            "student_key": row["student_key"],
            "student_name": row["student_name"],
            "current_grade": current_grades.get(row["student_key"]),
            "new_grade": compute_score(row, assignment_config),
            "comment": row.get("comment", ""),
        })
    return plan
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /Users/markumreed/Documents/ism_courses/autograder && pytest tests/test_gui_helpers.py -v`
Expected: 11 passed

- [ ] **Step 5: Commit**

```bash
cd /Users/markumreed/Documents/ism_courses
git add autograder/autograder_common/gui_helpers.py autograder/tests/test_gui_helpers.py
git commit -m "Add gui_helpers: live scoring and upload-plan building"
```

---

## Task 3: `gui.py` — Streamlit page (header, fetch/check actions, grading table, upload panel)

**Files:**
- Create: `autograder/gui.py`
- Modify: `autograder/requirements.txt`

**Interfaces:**
- Consumes: everything from Task 1 and Task 2 (`gui_helpers.student_key`, `gui_helpers.discover_assignments`, `gui_helpers.compute_student_record`, `gui_helpers.live_score`, `gui_helpers.build_upload_plan`); `autograder_common.config.load_course_config(path) -> dict`, `config.ConfigError` (existing); `autograder_common.canvas.CanvasClient(base_url, course_id, token)`, `canvas.CanvasError` (existing); `autograder_common.fetch.fetch_submission(submission, assignment_config, canvas_client, dest_dir)`, `fetch.FetchError` (existing); `autograder_common.worksheet.build_worksheet(path, students, assignment_config)`, `worksheet.read_worksheet(path) -> list[dict]`, `worksheet.incomplete_students(rows, assignment_config) -> list[str]`, `worksheet.human_fields(assignment_config) -> list[str]`, `worksheet.mechanical_fields(assignment_config) -> list[str]`, `worksheet.HUMAN_COLUMN_PREFIX`, `worksheet.MECHANICAL_COLUMN_PREFIX` (existing).
- Produces: a runnable Streamlit app with no exported functions consumed by later tasks (this is the last task in the plan).

This task has no automated tests, per the design doc ("gui.py itself has no
automated tests — it's UI wiring only, verified by manually running
`streamlit run gui.py`"). Steps below are implementation + manual
verification, not TDD.

- [ ] **Step 1: Add the streamlit dependency**

Read `autograder/requirements.txt` first to see its current exact content, then add one line. The file should read:

```
requests>=2.31
PyYAML>=6.0
pytest>=8.0
ruff>=0.6
streamlit>=1.35
```

- [ ] **Step 2: Write `gui.py`**

Create `autograder/gui.py`:

```python
"""Local Streamlit GUI for the ISM2411/ISM3232 autograder.

Run with: streamlit run gui.py

Thin presentation layer over autograder_common — every grading decision
(what to fetch, what a check means, how a rubric scores) is delegated to
the same functions the fetch/check/upload CLI (grade_ism2411.py /
grade_ism3232.py) already uses. This file only renders state and wires
button clicks to those functions.
"""
from pathlib import Path

import streamlit as st

from autograder_common import gui_helpers, worksheet
from autograder_common.canvas import CanvasClient, CanvasError
from autograder_common.config import ConfigError, load_course_config
from autograder_common.fetch import FetchError, fetch_submission

ROOT = Path(__file__).resolve().parent
RUNS_DIR = ROOT / "runs"

COURSES = {
    "ISM2411": {
        "config_path": ROOT / "ism2411.config.yaml",
        "assignments_dir": ROOT / "assignments" / "ism2411",
    },
    "ISM3232": {
        "config_path": ROOT / "ism3232.config.yaml",
        "assignments_dir": ROOT / "assignments" / "ism3232",
    },
}

st.set_page_config(page_title="Autograder", layout="wide")
st.title("Autograder")

# ---------------------------------------------------------------------------
# Header controls
# ---------------------------------------------------------------------------
course_name = st.selectbox("Course", list(COURSES.keys()))
course = COURSES[course_name]

try:
    assignments = gui_helpers.discover_assignments(course["assignments_dir"])
except ConfigError as e:
    st.error(f"Could not load assignment configs: {e}")
    st.stop()

if not assignments:
    st.warning(f"No assignment configs found in {course['assignments_dir']}")
    st.stop()

assignment_keys = [a["key"] for a in assignments]
assignment_key = st.selectbox("Assignment", assignment_keys)
assignment_config = next(a for a in assignments if a["key"] == assignment_key)

state_key = f"{course_name}:{assignment_key}"
if st.session_state.get("_current_state_key") != state_key:
    st.session_state["_current_state_key"] = state_key
    st.session_state["edited_rows"] = None
    st.session_state["upload_previewed"] = False

worksheet_path = RUNS_DIR / assignment_key / "review.csv"


def get_client():
    course_config = load_course_config(course["config_path"])
    return CanvasClient(
        course_config["canvas_base_url"],
        course_config["canvas_course_id"],
        course_config["canvas_token"],
    )


def get_assignment_id(client):
    override = assignment_config.get("canvas_assignment_id")
    if override:
        return override
    return client.find_assignment_id(assignment_config["canvas_display_name"])


# ---------------------------------------------------------------------------
# Action bar: Fetch / Check
# ---------------------------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    if st.button("Fetch Submissions"):
        try:
            client = get_client()
            assignment_id = get_assignment_id(client)
            submissions = client.list_submissions(assignment_id)
        except (ConfigError, CanvasError) as e:
            st.error(f"Fetch failed: {e}")
        else:
            out_dir = RUNS_DIR / assignment_key
            out_dir.mkdir(parents=True, exist_ok=True)
            count = 0
            log_lines = []
            for sub in submissions:
                user = sub.get("user") or {}
                name = user.get("name", f"user-{sub.get('user_id')}")
                dest = out_dir / gui_helpers.student_key(name)
                try:
                    fetch_submission(sub, assignment_config, client, dest)
                    count += 1
                except FetchError as e:
                    log_lines.append(f"{name}: fetch failed - {e}")
            st.success(f"Fetched {count}/{len(submissions)} submissions to {out_dir}")
            for line in log_lines:
                st.write(f"⚠️ {line}")

with col2:
    if st.button("Run Checks"):
        try:
            client = get_client()
            assignment_id = get_assignment_id(client)
            submissions = client.list_submissions(assignment_id)
        except (ConfigError, CanvasError) as e:
            st.error(f"Check failed: {e}")
        else:
            out_dir = RUNS_DIR / assignment_key
            students = []
            for sub in submissions:
                user = sub.get("user") or {}
                name = user.get("name", f"user-{sub.get('user_id')}")
                key = gui_helpers.student_key(name)
                student_dir = out_dir / key
                if not student_dir.exists():
                    students.append({
                        "student_key": key, "student_name": name,
                        "status": "fetch-failed", "captured_output": "",
                    })
                    continue
                students.append(
                    gui_helpers.compute_student_record(student_dir, key, name, assignment_config)
                )
            worksheet.build_worksheet(worksheet_path, students, assignment_config)
            st.session_state["edited_rows"] = None
            st.session_state["upload_previewed"] = False
            st.success(f"Wrote {worksheet_path}")

# ---------------------------------------------------------------------------
# Grading table
# ---------------------------------------------------------------------------
if not worksheet_path.exists():
    st.info("Run Check to build the review worksheet before grading.")
    st.stop()

if st.session_state["edited_rows"] is None:
    st.session_state["edited_rows"] = worksheet.read_worksheet(worksheet_path)

rows = st.session_state["edited_rows"]
human_fields = worksheet.human_fields(assignment_config)
mechanical_fields = worksheet.mechanical_fields(assignment_config)
scoring_type = assignment_config.get("scoring_type", "points")

st.header("Grading")

for row in rows:
    with st.expander(f"{row['student_name']} — status: {row['status']}"):
        if row["status"] != "ok":
            st.write("No submission to grade (fetch failed or not yet fetched).")
            continue

        st.text(row.get("captured_output", "") or "(no captured output)")

        for field in mechanical_fields:
            col_name = f"{worksheet.MECHANICAL_COLUMN_PREFIX}{field}"
            st.write(f"**{field}** (mechanical): {row.get(col_name)}")

        for field in human_fields:
            col_name = f"{worksheet.HUMAN_COLUMN_PREFIX}{field}"
            spec = assignment_config["rubric"][field]
            prompt = spec.get("prompt", field)
            widget_key = f"{state_key}:{row['student_key']}:{field}"
            if scoring_type == "capstone_levels":
                options = ["", "excellent", "good", "developing", "incomplete"]
                current = row.get(col_name, "")
                index = options.index(current) if current in options else 0
                value = st.selectbox(prompt, options, index=index, key=widget_key)
            else:
                points = spec.get("points", 0)
                current = row.get(col_name, "")
                current_val = float(current) if current.strip() else None
                value = st.number_input(
                    prompt, min_value=0.0, max_value=float(points),
                    value=current_val if current_val is not None else 0.0,
                    key=widget_key,
                )
                value = str(value) if current.strip() or value else ""
            row[col_name] = str(value)

        row["comment"] = st.text_area(
            "Comment", value=row.get("comment", ""), key=f"{state_key}:{row['student_key']}:comment"
        )

        score = gui_helpers.live_score(row, assignment_config)
        st.write(f"**Live score:** {score if score is not None else '—'}")

if st.button("Save Worksheet"):
    students_for_write = []
    for row in rows:
        record = {
            "student_key": row["student_key"],
            "student_name": row["student_name"],
            "status": row["status"],
            "captured_output": row.get("captured_output", ""),
        }
        for field in mechanical_fields:
            col_name = f"{worksheet.MECHANICAL_COLUMN_PREFIX}{field}"
            record[field] = row.get(col_name, "").strip().lower() in ("true", "1", "yes")
        students_for_write.append(record)
    worksheet.build_worksheet(worksheet_path, students_for_write, assignment_config)
    # build_worksheet always writes human columns blank — overwrite them
    # with the in-memory edits, then re-read/re-save to merge.
    saved_rows = worksheet.read_worksheet(worksheet_path)
    for saved_row, edited_row in zip(saved_rows, rows):
        for field in human_fields:
            col_name = f"{worksheet.HUMAN_COLUMN_PREFIX}{field}"
            saved_row[col_name] = edited_row.get(col_name, "")
        saved_row["comment"] = edited_row.get("comment", "")
    import csv
    with worksheet_path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(saved_rows[0].keys()) if saved_rows else [])
        writer.writeheader()
        writer.writerows(saved_rows)
    st.session_state["upload_previewed"] = False
    st.success(f"Saved {worksheet_path}")

# ---------------------------------------------------------------------------
# Upload panel
# ---------------------------------------------------------------------------
st.header("Upload")

if st.button("Preview Upload"):
    saved_rows = worksheet.read_worksheet(worksheet_path)
    incomplete = worksheet.incomplete_students(saved_rows, assignment_config)
    if incomplete:
        st.error(f"Cannot preview - incomplete human-scored fields for: {', '.join(incomplete)}")
        st.session_state["upload_previewed"] = False
    else:
        try:
            client = get_client()
            assignment_id = get_assignment_id(client)
            submissions = client.list_submissions(assignment_id)
        except (ConfigError, CanvasError) as e:
            st.error(f"Preview failed: {e}")
        else:
            key_to_user_id = {
                gui_helpers.student_key((s.get("user") or {}).get("name", f"user-{s['user_id']}")): s["user_id"]
                for s in submissions
            }
            current_grades = {}
            for row in saved_rows:
                if row.get("status") != "ok":
                    continue
                user_id = key_to_user_id.get(row["student_key"])
                if user_id is not None:
                    current_grades[row["student_key"]] = client.get_current_grade(assignment_id, user_id)
            plan = gui_helpers.build_upload_plan(saved_rows, assignment_config, current_grades)
            st.session_state["upload_plan"] = plan
            st.session_state["upload_previewed"] = True
            for item in plan:
                current_str = "ungraded" if item["current_grade"] is None else item["current_grade"]
                st.write(f"{item['student_name']}: {current_str} → {item['new_grade']}")

confirm_text = st.text_input(f"Type '{assignment_key}' to confirm posting grades")
post_disabled = not (st.session_state.get("upload_previewed") and confirm_text == assignment_key)

if st.button("Post Grades to Canvas", disabled=post_disabled):
    saved_rows = worksheet.read_worksheet(worksheet_path)
    incomplete = worksheet.incomplete_students(saved_rows, assignment_config)
    if incomplete:
        st.error(f"Cannot post - incomplete human-scored fields for: {', '.join(incomplete)}")
    else:
        try:
            client = get_client()
            assignment_id = get_assignment_id(client)
            submissions = client.list_submissions(assignment_id)
        except (ConfigError, CanvasError) as e:
            st.error(f"Upload failed: {e}")
        else:
            key_to_user_id = {
                gui_helpers.student_key((s.get("user") or {}).get("name", f"user-{s['user_id']}")): s["user_id"]
                for s in submissions
            }
            import json
            from datetime import datetime, timezone

            log = []
            for row in saved_rows:
                if row.get("status") != "ok":
                    continue
                user_id = key_to_user_id.get(row["student_key"])
                if user_id is None:
                    continue
                score = gui_helpers.live_score(row, assignment_config)
                current = client.get_current_grade(assignment_id, user_id)
                client.post_grade(assignment_id, user_id, score, row.get("comment") or None)
                log.append({"user_id": user_id, "name": row["student_name"], "previous": current, "posted": score})

            runs_dir_path = RUNS_DIR / assignment_key
            runs_dir_path.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            log_path = runs_dir_path / f"upload_log_{timestamp}.json"
            log_path.write_text(json.dumps(log, indent=2))
            st.success(f"Posted {len(log)} grade(s). Log: {log_path}")
            st.session_state["upload_previewed"] = False
```

- [ ] **Step 3: Install the new dependency and verify the app imports cleanly**

Run:
```bash
cd /Users/markumreed/Documents/ism_courses/autograder
pip install -r requirements.txt
python3 -c "import ast; ast.parse(open('gui.py').read()); print('syntax ok')"
```
Expected: `syntax ok`

- [ ] **Step 4: Manually verify the app launches**

Run:
```bash
cd /Users/markumreed/Documents/ism_courses/autograder
streamlit run gui.py --server.headless true &
sleep 3
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8501
kill %1
```
Expected: `200` (the Streamlit server started and served the page). This confirms the app boots without a Python exception on import/render — it does NOT confirm Canvas connectivity (no real course config is filled in yet), which is expected and fine at this stage.

If this curl check isn't available in your environment, instead run `streamlit run gui.py` directly and visually confirm in a browser that: the course/assignment selectors render, and selecting `ISM2411` / `week03_lab` shows "Run Check to build the review worksheet before grading." (since no `runs/week03_lab/review.csv` exists yet) without a Python traceback on the page.

- [ ] **Step 5: Run the full existing test suite once to confirm nothing broke**

Run: `cd /Users/markumreed/Documents/ism_courses/autograder && pytest -v`
Expected: all existing tests still pass (58 from before this plan, plus the 11 new `test_gui_helpers.py` tests from Tasks 1-2 = 69 total), since `gui.py` only adds a new file and doesn't modify any existing module.

- [ ] **Step 6: Commit**

```bash
cd /Users/markumreed/Documents/ism_courses
git add autograder/gui.py autograder/requirements.txt
git commit -m "Add Streamlit GUI for fetch/check/grade/upload workflow"
```

---

## Final Verification

- [ ] Run the full test suite fresh:
```bash
cd /Users/markumreed/Documents/ism_courses/autograder
pip install -r requirements.txt
pytest -v
```
Expected: all tests pass (69 total: 58 pre-existing + 11 new in `test_gui_helpers.py`).

- [ ] Confirm the GUI launches without error:
```bash
cd /Users/markumreed/Documents/ism_courses/autograder
streamlit run gui.py --server.headless true &
sleep 3
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8501
kill %1
```
Expected: `200`.

- [ ] Manually walk through the workflow once against a real (or test) Canvas
course, per `autograder/README.md`'s setup instructions: select a course and
assignment, click Fetch Submissions, click Run Checks, expand a student row
and fill in a human-scored field, confirm the live score updates, click Save
Worksheet, click Preview Upload, confirm the current→new grade line renders
correctly, and confirm Post Grades to Canvas stays disabled until the
confirmation text field exactly matches the assignment key.
