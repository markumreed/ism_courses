# ISM2411 / ISM3232 Autograder Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build two local Python CLI programs (`grade_ism2411.py`, `grade_ism3232.py`) that fetch student submissions from Canvas, run deterministic (no-LLM) checks against each course's real rubric, produce a review worksheet for the handful of criteria that genuinely need human judgment, and post final grades back to Canvas — sharing one underlying engine.

**Architecture:** A shared library package `autograder_common/` (Canvas API client, submission fetcher, mechanical checks, worksheet build/read, rubric scoring) with two thin per-course entrypoints and per-assignment YAML configs. No course-specific logic lives in `autograder_common/` — every difference between ISM2411 and ISM3232 is expressed in YAML.

**Tech Stack:** Python 3.10+, `requests` (Canvas API), `PyYAML` (config), `ruff` + `pytest` invoked as subprocesses (ISM3232 Developer Workflow checks + running against student repos), stdlib `csv`/`subprocess`/`argparse` for everything else. Test runner: `pytest`, with `unittest.mock` for Canvas API mocking — no real network calls in the test suite.

## Global Constraints

- Grading is fully deterministic — no LLM/AI judgment call anywhere in this codebase. Criteria the rubric can't mechanically check are left blank in the worksheet for the instructor to fill in by hand.
- No Canvas API token is ever written to a config file or committed — it comes only from the `CANVAS_API_TOKEN` environment variable.
- `upload` must never post a grade without either `--dry-run` output having been shown or an interactive `y/n` confirmation (or explicit `--yes`), and must refuse to run if any human-scored worksheet field is still blank.
- Midterm exams, quizzes, DataCamp completion, and Lab Participation/Portfolio are out of scope — nothing in this codebase touches them.
- Everything lives under a new top-level `autograder/` directory in this repo (sibling to `ism2411/`, `ism3232/`) — it is tooling, not course content, and is not a submodule.

---

## File Structure

```
autograder/
  requirements.txt
  README.md
  .gitignore                        # runs/ (fetched submissions + logs are local-only)
  autograder_common/
    __init__.py
    config.py                       # load_course_config, load_assignment_config
    canvas.py                       # CanvasClient
    fetch.py                        # fetch_submission (+ canvas_upload/github_url variants)
    checks.py                       # file_present, runs_without_error, ruff_check,
                                     #   pytest_check, git_log_checks
    worksheet.py                    # build_worksheet, read_worksheet, incomplete_students
    scoring.py                      # compute_score (points / capstone_levels)
    cli.py                          # cmd_fetch, cmd_check, cmd_upload, build_cli, main
  grade_ism2411.py                  # entrypoint: wires cli.main to ism2411 config/assignments
  grade_ism3232.py                  # entrypoint: wires cli.main to ism3232 config/assignments
  ism2411.config.yaml                # canvas_base_url, canvas_course_id (no secrets)
  ism3232.config.yaml
  assignments/
    ism2411/
      week03_lab.yaml               # pilot: file-upload lab, points rubric
      capstone.yaml                 # pilot: capstone_levels rubric (4 dimensions)
    ism3232/
      week07_assignment.yaml        # pilot: github_url weekly assignment, points rubric
      developer_workflow.yaml       # pilot: fully mechanical points rubric
      capstone.yaml                 # pilot: points rubric (5 components, 100 pts)
  tests/
    conftest.py                     # shared fixtures (tmp git repos, fake Canvas responses)
    test_config.py
    test_canvas.py
    test_checks.py
    test_fetch.py
    test_worksheet.py
    test_scoring.py
    test_cli.py
```

`autograder_common/cli.py` is the one file doing real integration work (wiring Canvas + checks + fetch + worksheet + scoring together); every other module has exactly one responsibility and no dependency on Canvas specifics beyond `canvas.py` and `fetch.py`'s narrow interfaces.

---

## Task 1: Project scaffolding

**Files:**
- Create: `autograder/requirements.txt`
- Create: `autograder/.gitignore`
- Create: `autograder/autograder_common/__init__.py`
- Create: `autograder/tests/__init__.py`
- Create: `autograder/tests/conftest.py`

**Interfaces:**
- Produces: an importable, empty `autograder_common` package and a working `pytest` setup that later tasks add to.

- [ ] **Step 1: Create the directory structure and requirements file**

```bash
mkdir -p /Users/markumreed/Documents/ism_courses/autograder/autograder_common
mkdir -p /Users/markumreed/Documents/ism_courses/autograder/tests
mkdir -p /Users/markumreed/Documents/ism_courses/autograder/assignments/ism2411
mkdir -p /Users/markumreed/Documents/ism_courses/autograder/assignments/ism3232
```

Create `autograder/requirements.txt`:

```
requests>=2.31
PyYAML>=6.0
pytest>=8.0
ruff>=0.6
```

Create `autograder/.gitignore`:

```
runs/
__pycache__/
*.pyc
.pytest_cache/
```

Create `autograder/autograder_common/__init__.py` (empty file — makes the directory a package):

```python
```

Create `autograder/tests/__init__.py` (empty file):

```python
```

Create `autograder/tests/conftest.py`:

```python
"""Shared pytest fixtures for the autograder test suite."""
import subprocess
from pathlib import Path

import pytest


@pytest.fixture
def git_repo(tmp_path):
    """Create an empty git repo in tmp_path/repo and return its path."""
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=repo, check=True)
    return repo


def commit(repo, message, timestamp=None, env=None):
    """Create an empty commit in repo with the given message. If timestamp
    (a unix epoch int) is given, back/forward-date the commit."""
    full_env = dict(**(env or {}))
    if timestamp is not None:
        date_str = f"{timestamp} +0000"
        full_env["GIT_AUTHOR_DATE"] = date_str
        full_env["GIT_COMMITTER_DATE"] = date_str
    subprocess.run(
        ["git", "commit", "-q", "--allow-empty", "-m", message],
        cwd=repo,
        check=True,
        env={**_full_process_env(), **full_env},
    )


def _full_process_env():
    import os
    return dict(os.environ)
```

- [ ] **Step 2: Verify the package imports and pytest runs (with zero tests)**

Run: `cd /Users/markumreed/Documents/ism_courses/autograder && python3 -c "import autograder_common; print('ok')"`
Expected: `ok`

Run: `cd /Users/markumreed/Documents/ism_courses/autograder && pip install -r requirements.txt && pytest --collect-only`
Expected: exits 0, reports "no tests collected" (no test files exist yet)

- [ ] **Step 3: Commit**

```bash
cd /Users/markumreed/Documents/ism_courses
git add autograder/requirements.txt autograder/.gitignore autograder/autograder_common/__init__.py autograder/tests/__init__.py autograder/tests/conftest.py
git commit -m "Scaffold autograder project structure"
```

---

## Task 2: Config loading (`config.py`)

**Files:**
- Create: `autograder/autograder_common/config.py`
- Test: `autograder/tests/test_config.py`

**Interfaces:**
- Produces: `ConfigError(Exception)`, `load_course_config(path) -> {"canvas_base_url": str, "canvas_course_id": int|str, "canvas_token": str}`, `load_assignment_config(path) -> dict` (the parsed YAML, validated).

- [ ] **Step 1: Write the failing tests**

Create `autograder/tests/test_config.py`:

```python
import pytest

from autograder_common.config import ConfigError, load_assignment_config, load_course_config


def test_load_course_config_reads_fields(tmp_path, monkeypatch):
    monkeypatch.setenv("CANVAS_API_TOKEN", "secret-token")
    path = tmp_path / "course.yaml"
    path.write_text("canvas_base_url: 'https://example.instructure.com/'\ncanvas_course_id: 123\n")

    config = load_course_config(path)

    assert config == {
        "canvas_base_url": "https://example.instructure.com",
        "canvas_course_id": 123,
        "canvas_token": "secret-token",
    }


def test_load_course_config_missing_field_raises(tmp_path, monkeypatch):
    monkeypatch.setenv("CANVAS_API_TOKEN", "secret-token")
    path = tmp_path / "course.yaml"
    path.write_text("canvas_base_url: 'https://example.instructure.com/'\n")

    with pytest.raises(ConfigError, match="canvas_course_id"):
        load_course_config(path)


def test_load_course_config_missing_token_raises(tmp_path, monkeypatch):
    monkeypatch.delenv("CANVAS_API_TOKEN", raising=False)
    path = tmp_path / "course.yaml"
    path.write_text("canvas_base_url: 'https://example.instructure.com/'\ncanvas_course_id: 123\n")

    with pytest.raises(ConfigError, match="CANVAS_API_TOKEN"):
        load_course_config(path)


def test_load_assignment_config_reads_fields(tmp_path):
    path = tmp_path / "week03_lab.yaml"
    path.write_text(
        "course: ism2411\nkey: week03_lab\nsubmission_type: canvas_upload\n"
        "rubric:\n  submission:\n    points: 1\n    source: mechanical\n    check: file_present\n"
    )

    config = load_assignment_config(path)

    assert config["course"] == "ism2411"
    assert config["submission_type"] == "canvas_upload"
    assert config["rubric"]["submission"]["points"] == 1


def test_load_assignment_config_bad_submission_type_raises(tmp_path):
    path = tmp_path / "bad.yaml"
    path.write_text(
        "course: ism2411\nkey: bad\nsubmission_type: carrier_pigeon\nrubric: {}\n"
    )

    with pytest.raises(ConfigError, match="submission_type"):
        load_assignment_config(path)


def test_load_assignment_config_missing_field_raises(tmp_path):
    path = tmp_path / "bad.yaml"
    path.write_text("course: ism2411\n")

    with pytest.raises(ConfigError, match="missing required field"):
        load_assignment_config(path)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /Users/markumreed/Documents/ism_courses/autograder && pytest tests/test_config.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'autograder_common.config'`

- [ ] **Step 3: Write the implementation**

Create `autograder/autograder_common/config.py`:

```python
"""Load course and per-assignment YAML configs."""
import os
from pathlib import Path

import yaml


class ConfigError(Exception):
    pass


REQUIRED_COURSE_FIELDS = ["canvas_base_url", "canvas_course_id"]
REQUIRED_ASSIGNMENT_FIELDS = ["course", "key", "submission_type", "rubric"]
VALID_SUBMISSION_TYPES = ("canvas_upload", "github_url")


def load_course_config(path):
    """Load a course config YAML and attach the Canvas API token from the
    CANVAS_API_TOKEN environment variable.

    Returns {"canvas_base_url": str, "canvas_course_id": ..., "canvas_token": str}.
    Raises ConfigError if a required field or the env var is missing.
    """
    path = Path(path)
    data = yaml.safe_load(path.read_text())
    if not isinstance(data, dict):
        raise ConfigError(f"{path}: expected a YAML mapping at the top level")
    missing = [f for f in REQUIRED_COURSE_FIELDS if f not in data]
    if missing:
        raise ConfigError(f"{path}: missing required field(s): {', '.join(missing)}")
    token = os.environ.get("CANVAS_API_TOKEN")
    if not token:
        raise ConfigError("CANVAS_API_TOKEN environment variable is not set")
    return {
        "canvas_base_url": data["canvas_base_url"].rstrip("/"),
        "canvas_course_id": data["canvas_course_id"],
        "canvas_token": token,
    }


def load_assignment_config(path):
    """Load and validate a per-assignment YAML config. Returns the parsed
    dict as-is (not transformed) once required fields are confirmed present."""
    path = Path(path)
    data = yaml.safe_load(path.read_text())
    if not isinstance(data, dict):
        raise ConfigError(f"{path}: expected a YAML mapping at the top level")
    missing = [f for f in REQUIRED_ASSIGNMENT_FIELDS if f not in data]
    if missing:
        raise ConfigError(f"{path}: missing required field(s): {', '.join(missing)}")
    if data["submission_type"] not in VALID_SUBMISSION_TYPES:
        raise ConfigError(
            f"{path}: submission_type must be one of {VALID_SUBMISSION_TYPES}, "
            f"got {data['submission_type']!r}"
        )
    return data
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /Users/markumreed/Documents/ism_courses/autograder && pytest tests/test_config.py -v`
Expected: 6 passed

- [ ] **Step 5: Commit**

```bash
cd /Users/markumreed/Documents/ism_courses
git add autograder/autograder_common/config.py autograder/tests/test_config.py
git commit -m "Add course/assignment config loading with validation"
```

---

## Task 3: Canvas API client (`canvas.py`)

**Files:**
- Create: `autograder/autograder_common/canvas.py`
- Test: `autograder/tests/test_canvas.py`

**Interfaces:**
- Consumes: nothing from earlier tasks.
- Produces: `CanvasError(Exception)`, `CanvasClient(base_url, course_id, token, session=None)` with methods `find_assignment_id(name) -> int`, `list_submissions(assignment_id) -> list[dict]`, `download_attachment(attachment: dict, dest_path: Path) -> None`, `get_current_grade(assignment_id, user_id) -> float|None`, `post_grade(assignment_id, user_id, score, comment=None) -> dict`.

- [ ] **Step 1: Write the failing tests**

Create `autograder/tests/test_canvas.py`:

```python
import pytest

from autograder_common.canvas import CanvasClient, CanvasError


class FakeResponse:
    def __init__(self, status_code=200, json_data=None, text="", content=b""):
        self.status_code = status_code
        self._json_data = json_data
        self.text = text
        self.content = content

    def json(self):
        return self._json_data


class FakeSession:
    def __init__(self):
        self.headers = {}
        self.get_calls = []
        self.put_calls = []
        self.get_responses = {}
        self.put_response = FakeResponse(200, json_data={"id": 1})

    def get(self, url, params=None):
        self.get_calls.append((url, params))
        for prefix, response in self.get_responses.items():
            if url.startswith(prefix):
                return response
        raise AssertionError(f"no fake response registered for GET {url}")

    def put(self, url, json=None):
        self.put_calls.append((url, json))
        return self.put_response


def make_client():
    session = FakeSession()
    client = CanvasClient("https://example.instructure.com", 10, "tok", session=session)
    return client, session


def test_find_assignment_id_matches_by_name():
    client, session = make_client()
    session.get_responses["https://example.instructure.com/api/v1/courses/10/assignments"] = FakeResponse(
        200, json_data=[{"id": 55, "name": "Lab 3: Product Pricer"}, {"id": 56, "name": "Lab 4"}]
    )

    assert client.find_assignment_id("Lab 3: Product Pricer") == 55


def test_find_assignment_id_no_match_raises():
    client, session = make_client()
    session.get_responses["https://example.instructure.com/api/v1/courses/10/assignments"] = FakeResponse(
        200, json_data=[{"id": 56, "name": "Lab 4"}]
    )

    with pytest.raises(CanvasError, match="No assignment named"):
        client.find_assignment_id("Lab 3: Product Pricer")


def test_find_assignment_id_multiple_matches_raises():
    client, session = make_client()
    session.get_responses["https://example.instructure.com/api/v1/courses/10/assignments"] = FakeResponse(
        200, json_data=[{"id": 55, "name": "Lab 3"}, {"id": 99, "name": "Lab 3"}]
    )

    with pytest.raises(CanvasError, match="Multiple assignments"):
        client.find_assignment_id("Lab 3")


def test_list_submissions_returns_json():
    client, session = make_client()
    session.get_responses[
        "https://example.instructure.com/api/v1/courses/10/assignments/55/submissions"
    ] = FakeResponse(200, json_data=[{"user_id": 1, "user": {"name": "Jane Doe"}}])

    result = client.list_submissions(55)

    assert result == [{"user_id": 1, "user": {"name": "Jane Doe"}}]


def test_get_current_grade_returns_score():
    client, session = make_client()
    session.get_responses[
        "https://example.instructure.com/api/v1/courses/10/assignments/55/submissions/1"
    ] = FakeResponse(200, json_data={"score": 8.5})

    assert client.get_current_grade(55, 1) == 8.5


def test_get_current_grade_none_when_ungraded():
    client, session = make_client()
    session.get_responses[
        "https://example.instructure.com/api/v1/courses/10/assignments/55/submissions/1"
    ] = FakeResponse(200, json_data={"score": None})

    assert client.get_current_grade(55, 1) is None


def test_post_grade_sends_put_with_score_and_comment():
    client, session = make_client()

    client.post_grade(55, 1, 9, comment="Nice work")

    assert len(session.put_calls) == 1
    url, payload = session.put_calls[0]
    assert url == "https://example.instructure.com/api/v1/courses/10/assignments/55/submissions/1"
    assert payload["submission"]["posted_grade"] == 9
    assert payload["comment"]["text_comment"] == "Nice work"


def test_post_grade_failure_raises():
    client, session = make_client()
    session.put_response = FakeResponse(422, text="validation error")

    with pytest.raises(CanvasError, match="422"):
        client.post_grade(55, 1, 9)


def test_get_failure_raises():
    client, session = make_client()
    session.get_responses["https://example.instructure.com/api/v1/courses/10/assignments"] = FakeResponse(
        403, text="forbidden"
    )

    with pytest.raises(CanvasError, match="403"):
        client.find_assignment_id("Lab 3")
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /Users/markumreed/Documents/ism_courses/autograder && pytest tests/test_canvas.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'autograder_common.canvas'`

- [ ] **Step 3: Write the implementation**

Create `autograder/autograder_common/canvas.py`:

```python
"""Minimal Canvas LMS API client covering only what the autograder needs:
listing submissions, downloading files, reading the current grade, and
posting a new grade + comment."""
import requests


class CanvasError(Exception):
    pass


class CanvasClient:
    def __init__(self, base_url, course_id, token, session=None):
        self.base_url = base_url.rstrip("/")
        self.course_id = course_id
        self.token = token
        self.session = session or requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {token}"})

    def _get(self, path, params=None):
        url = f"{self.base_url}{path}"
        resp = self.session.get(url, params=params)
        if resp.status_code != 200:
            raise CanvasError(f"GET {url} failed: {resp.status_code} {resp.text[:200]}")
        return resp.json()

    def find_assignment_id(self, assignment_name):
        """Look up a Canvas assignment_id by exact name match within the course."""
        assignments = self._get(
            f"/api/v1/courses/{self.course_id}/assignments", params={"per_page": 100}
        )
        matches = [a for a in assignments if a["name"] == assignment_name]
        if not matches:
            raise CanvasError(
                f"No assignment named {assignment_name!r} found in course {self.course_id}"
            )
        if len(matches) > 1:
            raise CanvasError(
                f"Multiple assignments named {assignment_name!r} found; "
                f"set canvas_assignment_id explicitly in the assignment config"
            )
        return matches[0]["id"]

    def list_submissions(self, assignment_id):
        """Return the list of submission dicts for the assignment (one per
        student), each including 'user' (name) via include[]=user."""
        return self._get(
            f"/api/v1/courses/{self.course_id}/assignments/{assignment_id}/submissions",
            params={"per_page": 100, "include[]": "user"},
        )

    def download_attachment(self, attachment, dest_path):
        """Download a Canvas file attachment dict (must have 'url') to dest_path."""
        resp = self.session.get(attachment["url"])
        if resp.status_code != 200:
            raise CanvasError(f"Download of {attachment['url']} failed: {resp.status_code}")
        dest_path.write_bytes(resp.content)

    def get_current_grade(self, assignment_id, user_id):
        data = self._get(
            f"/api/v1/courses/{self.course_id}/assignments/{assignment_id}/submissions/{user_id}"
        )
        return data.get("score")

    def post_grade(self, assignment_id, user_id, score, comment=None):
        url = (
            f"{self.base_url}/api/v1/courses/{self.course_id}"
            f"/assignments/{assignment_id}/submissions/{user_id}"
        )
        payload = {"submission": {"posted_grade": score}}
        if comment:
            payload["comment"] = {"text_comment": comment}
        resp = self.session.put(url, json=payload)
        if resp.status_code != 200:
            raise CanvasError(f"PUT {url} failed: {resp.status_code} {resp.text[:200]}")
        return resp.json()
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /Users/markumreed/Documents/ism_courses/autograder && pytest tests/test_canvas.py -v`
Expected: 9 passed

- [ ] **Step 5: Commit**

```bash
cd /Users/markumreed/Documents/ism_courses
git add autograder/autograder_common/canvas.py autograder/tests/test_canvas.py
git commit -m "Add Canvas API client"
```

---

## Task 4: Mechanical checks (`checks.py`)

**Files:**
- Create: `autograder/autograder_common/checks.py`
- Test: `autograder/tests/test_checks.py`

**Interfaces:**
- Consumes: `tests/conftest.py`'s `git_repo` fixture and `commit()` helper (Task 1).
- Produces: `file_present(dir, expected_files) -> dict[str, bool]`, `runs_without_error(file_path, command_template, timeout_seconds=10) -> (bool, str, str)`, `ruff_check(dir) -> (bool, str)`, `pytest_check(dir, timeout_seconds=30) -> (bool, str)`, `git_log_checks(dir) -> {"commit_count": int, "generic_message_count": int, "spans_multiple_hours": bool}`.

- [ ] **Step 1: Write the failing tests**

Create `autograder/tests/test_checks.py`:

```python
from autograder_common import checks
from tests.conftest import commit


def test_file_present_reports_each_expected_file(tmp_path):
    (tmp_path / "pricer.py").write_text("print('hi')\n")

    result = checks.file_present(tmp_path, ["pricer.py", "missing.py"])

    assert result == {"pricer.py": True, "missing.py": False}


def test_runs_without_error_success(tmp_path):
    script = tmp_path / "ok.py"
    script.write_text("print('hello world')\n")

    ok, out, err = checks.runs_without_error(script, "python3 {file}")

    assert ok is True
    assert "hello world" in out
    assert err == ""


def test_runs_without_error_failure(tmp_path):
    script = tmp_path / "broken.py"
    script.write_text("raise ValueError('boom')\n")

    ok, out, err = checks.runs_without_error(script, "python3 {file}")

    assert ok is False
    assert "ValueError" in err


def test_runs_without_error_timeout(tmp_path):
    script = tmp_path / "hangs.py"
    script.write_text("while True:\n    pass\n")

    ok, out, err = checks.runs_without_error(script, "python3 {file}", timeout_seconds=1)

    assert ok is False
    assert "Timed out" in err


def test_ruff_check_passes_on_clean_file(tmp_path):
    (tmp_path / "clean.py").write_text("def add(a, b):\n    return a + b\n")

    ok, output = checks.ruff_check(tmp_path)

    assert ok is True


def test_ruff_check_fails_on_lint_error(tmp_path):
    (tmp_path / "dirty.py").write_text("import os\n\ndef add(a, b):\n    return a + b\n")

    ok, output = checks.ruff_check(tmp_path)

    assert ok is False
    assert "os" in output


def test_pytest_check_passes(tmp_path):
    (tmp_path / "test_ok.py").write_text("def test_one():\n    assert 1 + 1 == 2\n")

    ok, output = checks.pytest_check(tmp_path)

    assert ok is True


def test_pytest_check_fails(tmp_path):
    (tmp_path / "test_bad.py").write_text("def test_one():\n    assert 1 + 1 == 3\n")

    ok, output = checks.pytest_check(tmp_path)

    assert ok is False
    assert "1 failed" in output


def test_git_log_checks_counts_commits_and_flags_generic_messages(git_repo):
    commit(git_repo, "Set up project skeleton", timestamp=1_700_000_000)
    commit(git_repo, "fix", timestamp=1_700_000_100)
    commit(git_repo, "Implement OOP II composition", timestamp=1_700_010_000)

    result = checks.git_log_checks(git_repo)

    assert result["commit_count"] == 3
    assert result["generic_message_count"] == 1
    assert result["spans_multiple_hours"] is True


def test_git_log_checks_single_commit_does_not_span_hours(git_repo):
    commit(git_repo, "Final submission", timestamp=1_700_000_000)

    result = checks.git_log_checks(git_repo)

    assert result["commit_count"] == 1
    assert result["spans_multiple_hours"] is False
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /Users/markumreed/Documents/ism_courses/autograder && pytest tests/test_checks.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'autograder_common.checks'`

- [ ] **Step 3: Write the implementation**

Create `autograder/autograder_common/checks.py`:

```python
"""Mechanical, deterministic checks run against a fetched submission
directory. No network access, no LLM calls — every function here is a
pure wrapper around a CLI tool or the filesystem."""
import subprocess
import sys
from pathlib import Path

GENERIC_COMMIT_MESSAGES = {"fix", "final", "asdf", "wip", "update", "changes", "done", "test"}


def file_present(submission_dir, expected_files):
    """Return {filename: bool} for whether each expected file exists."""
    submission_dir = Path(submission_dir)
    return {f: (submission_dir / f).is_file() for f in expected_files}


def runs_without_error(file_path, command_template, timeout_seconds=10):
    """Run command_template (containing a '{file}' placeholder) against
    file_path. Returns (success, stdout, stderr)."""
    file_path = Path(file_path)
    command = command_template.format(file=str(file_path))
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=file_path.parent,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )
        return (result.returncode == 0, result.stdout, result.stderr)
    except subprocess.TimeoutExpired as e:
        stdout = e.stdout if isinstance(e.stdout, str) else (e.stdout or b"").decode(errors="replace")
        return (False, stdout, f"Timed out after {timeout_seconds}s")


def ruff_check(submission_dir):
    """Run `ruff check .` in submission_dir. Returns (passed, output)."""
    result = subprocess.run(
        [sys.executable, "-m", "ruff", "check", "."],
        cwd=submission_dir,
        capture_output=True,
        text=True,
    )
    return (result.returncode == 0, result.stdout + result.stderr)


def pytest_check(submission_dir, timeout_seconds=30):
    """Run `pytest -q` in submission_dir. Returns (passed, output)."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "-q"],
            cwd=submission_dir,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )
        return (result.returncode == 0, result.stdout + result.stderr)
    except subprocess.TimeoutExpired:
        return (False, f"pytest timed out after {timeout_seconds}s")


def git_log_checks(repo_dir):
    """Inspect git log in repo_dir. Returns
    {"commit_count": int, "generic_message_count": int, "spans_multiple_hours": bool}."""
    result = subprocess.run(
        ["git", "log", "--pretty=format:%H|%ct|%s"],
        cwd=repo_dir,
        capture_output=True,
        text=True,
    )
    commits = []
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        parts = line.split("|", 2)
        if len(parts) == 3:
            commits.append({"hash": parts[0], "timestamp": int(parts[1]), "message": parts[2]})
    generic_count = sum(
        1 for c in commits if c["message"].strip().lower() in GENERIC_COMMIT_MESSAGES
    )
    timestamps = [c["timestamp"] for c in commits]
    spans_multiple_hours = (max(timestamps) - min(timestamps) >= 3600) if len(timestamps) > 1 else False
    return {
        "commit_count": len(commits),
        "generic_message_count": generic_count,
        "spans_multiple_hours": spans_multiple_hours,
    }
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /Users/markumreed/Documents/ism_courses/autograder && pytest tests/test_checks.py -v`
Expected: 10 passed (the timeout test takes ~1s; total runtime a few seconds)

- [ ] **Step 5: Commit**

```bash
cd /Users/markumreed/Documents/ism_courses
git add autograder/autograder_common/checks.py autograder/tests/test_checks.py
git commit -m "Add deterministic mechanical checks (file/run/ruff/pytest/git-log)"
```

---

## Task 5: Submission fetching (`fetch.py`)

**Files:**
- Create: `autograder/autograder_common/fetch.py`
- Test: `autograder/tests/test_fetch.py`

**Interfaces:**
- Consumes: nothing runtime from `canvas.py` directly (takes a canvas *client-like* object as a parameter — duck-typed, only needs `.download_attachment`).
- Produces: `FetchError(Exception)`, `fetch_canvas_upload(submission, canvas_client, dest_dir) -> list[Path]`, `fetch_github_url(submission, dest_dir) -> Path`, `fetch_submission(submission, assignment_config, canvas_client, dest_dir)` (dispatches on `assignment_config["submission_type"]`).

- [ ] **Step 1: Write the failing tests**

Create `autograder/tests/test_fetch.py`:

```python
from unittest.mock import patch

import pytest

from autograder_common.fetch import FetchError, fetch_canvas_upload, fetch_github_url, fetch_submission


class FakeCanvasClient:
    def __init__(self):
        self.downloaded = []

    def download_attachment(self, attachment, dest_path):
        self.downloaded.append((attachment, dest_path))
        dest_path.write_text("fake content")


def test_fetch_canvas_upload_downloads_each_attachment(tmp_path):
    client = FakeCanvasClient()
    submission = {"attachments": [{"filename": "pricer.py", "url": "http://x/pricer.py"}]}
    dest_dir = tmp_path / "student"

    paths = fetch_canvas_upload(submission, client, dest_dir)

    assert paths == [dest_dir / "pricer.py"]
    assert (dest_dir / "pricer.py").read_text() == "fake content"


def test_fetch_canvas_upload_no_attachments_raises(tmp_path):
    client = FakeCanvasClient()
    submission = {"attachments": []}

    with pytest.raises(FetchError, match="no attachments"):
        fetch_canvas_upload(submission, client, tmp_path / "student")


def test_fetch_github_url_invalid_url_raises(tmp_path):
    submission = {"url": "https://not-github.example.com/foo/bar"}

    with pytest.raises(FetchError, match="does not look like a GitHub link"):
        fetch_github_url(submission, tmp_path / "student")


def test_fetch_github_url_no_url_raises(tmp_path):
    with pytest.raises(FetchError, match="no URL"):
        fetch_github_url({}, tmp_path / "student")


def test_fetch_github_url_clones_with_correct_url(tmp_path):
    submission = {"url": "https://github.com/janedoe/ism3232-week07"}
    dest_dir = tmp_path / "student"

    with patch("autograder_common.fetch.subprocess.run") as fake_run:
        fake_run.return_value.returncode = 0
        result = fetch_github_url(submission, dest_dir)

    assert result == dest_dir
    args = fake_run.call_args[0][0]
    assert args[:2] == ["git", "clone"]
    assert args[-2] == "https://github.com/janedoe/ism3232-week07.git"
    assert args[-1] == str(dest_dir)


def test_fetch_github_url_clone_failure_raises(tmp_path):
    submission = {"url": "https://github.com/janedoe/private-repo"}

    with patch("autograder_common.fetch.subprocess.run") as fake_run:
        fake_run.return_value.returncode = 128
        fake_run.return_value.stderr = "repository not found"
        with pytest.raises(FetchError, match="repository not found"):
            fetch_github_url(submission, tmp_path / "student")


def test_fetch_submission_dispatches_to_canvas_upload(tmp_path):
    client = FakeCanvasClient()
    submission = {"attachments": [{"filename": "pricer.py", "url": "http://x/pricer.py"}]}
    assignment_config = {"submission_type": "canvas_upload"}

    fetch_submission(submission, assignment_config, client, tmp_path / "student")

    assert (tmp_path / "student" / "pricer.py").exists()


def test_fetch_submission_dispatches_to_github_url(tmp_path):
    submission = {"url": "https://github.com/janedoe/ism3232-week07"}
    assignment_config = {"submission_type": "github_url"}

    with patch("autograder_common.fetch.subprocess.run") as fake_run:
        fake_run.return_value.returncode = 0
        fetch_submission(submission, assignment_config, None, tmp_path / "student")

    fake_run.assert_called_once()


def test_fetch_submission_unknown_type_raises(tmp_path):
    with pytest.raises(FetchError, match="unknown submission_type"):
        fetch_submission({}, {"submission_type": "carrier_pigeon"}, None, tmp_path / "student")
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /Users/markumreed/Documents/ism_courses/autograder && pytest tests/test_fetch.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'autograder_common.fetch'`

- [ ] **Step 3: Write the implementation**

Create `autograder/autograder_common/fetch.py`:

```python
"""Resolve a Canvas submission (file upload or GitHub URL) into a local
directory containing the student's code."""
import re
import subprocess
from pathlib import Path

GITHUB_URL_RE = re.compile(r"github\.com[:/](?P<owner>[^/]+)/(?P<repo>[^/\s]+?)(?:\.git)?(?:/|$)")


class FetchError(Exception):
    pass


def fetch_canvas_upload(submission, canvas_client, dest_dir):
    """submission: a Canvas submission dict with 'attachments' (list of file
    dicts with 'filename' and 'url'). Downloads every attachment into
    dest_dir. Returns the list of downloaded file paths."""
    dest_dir = Path(dest_dir)
    attachments = submission.get("attachments") or []
    if not attachments:
        raise FetchError("no attachments on this submission")
    dest_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for att in attachments:
        dest = dest_dir / att["filename"]
        canvas_client.download_attachment(att, dest)
        paths.append(dest)
    return paths


def fetch_github_url(submission, dest_dir):
    """submission: a Canvas submission dict with 'url' (the GitHub link the
    student pasted into Canvas). Shallow-clones the repo into dest_dir.
    Returns dest_dir."""
    url = submission.get("url")
    if not url:
        raise FetchError("no URL on this submission")
    match = GITHUB_URL_RE.search(url)
    if not match:
        raise FetchError(f"URL does not look like a GitHub link: {url}")
    clone_url = f"https://github.com/{match.group('owner')}/{match.group('repo')}.git"
    dest_dir = Path(dest_dir)
    result = subprocess.run(
        ["git", "clone", "--depth", "1", clone_url, str(dest_dir)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise FetchError(f"clone of {clone_url} failed: {result.stderr.strip()}")
    return dest_dir


def fetch_submission(submission, assignment_config, canvas_client, dest_dir):
    """Dispatch to fetch_canvas_upload or fetch_github_url based on
    assignment_config['submission_type']."""
    submission_type = assignment_config["submission_type"]
    if submission_type == "canvas_upload":
        return fetch_canvas_upload(submission, canvas_client, dest_dir)
    if submission_type == "github_url":
        return fetch_github_url(submission, dest_dir)
    raise FetchError(f"unknown submission_type: {submission_type!r}")
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /Users/markumreed/Documents/ism_courses/autograder && pytest tests/test_fetch.py -v`
Expected: 9 passed

- [ ] **Step 5: Commit**

```bash
cd /Users/markumreed/Documents/ism_courses
git add autograder/autograder_common/fetch.py autograder/tests/test_fetch.py
git commit -m "Add submission fetcher (canvas_upload + github_url)"
```

---

## Task 6: Review worksheet (`worksheet.py`)

**Files:**
- Create: `autograder/autograder_common/worksheet.py`
- Test: `autograder/tests/test_worksheet.py`

**Interfaces:**
- Consumes: an `assignment_config["rubric"]` dict shaped like `{name: {"points": int, "source": "mechanical"|"human", "check": str, ...}}` (Task 2's `load_assignment_config`).
- Produces: `MECHANICAL_COLUMN_PREFIX = "mech_"`, `HUMAN_COLUMN_PREFIX = "human_"`, `human_fields(assignment_config) -> list[str]`, `mechanical_fields(assignment_config) -> list[str]`, `build_worksheet(path, students, assignment_config)`, `read_worksheet(path) -> list[dict]`, `incomplete_students(rows, assignment_config) -> list[str]`.

- [ ] **Step 1: Write the failing tests**

Create `autograder/tests/test_worksheet.py`:

```python
from autograder_common.worksheet import (
    build_worksheet,
    human_fields,
    incomplete_students,
    mechanical_fields,
    read_worksheet,
)

ASSIGNMENT_CONFIG = {
    "rubric": {
        "submission": {"points": 1, "source": "mechanical", "check": "file_present"},
        "correctness": {"points": 4, "source": "human", "prompt": "Compare output"},
        "code_quality": {"points": 2, "source": "human", "prompt": "Readable?"},
    }
}


def test_human_and_mechanical_fields_split_by_source():
    assert human_fields(ASSIGNMENT_CONFIG) == ["correctness", "code_quality"]
    assert mechanical_fields(ASSIGNMENT_CONFIG) == ["submission"]


def test_build_and_read_worksheet_round_trip(tmp_path):
    path = tmp_path / "review.csv"
    students = [
        {
            "student_key": "janedoe",
            "student_name": "Jane Doe",
            "status": "ok",
            "submission": True,
            "captured_output": "hello world",
        },
        {
            "student_key": "johnsmith",
            "student_name": "John Smith",
            "status": "fetch-failed",
        },
    ]

    build_worksheet(path, students, ASSIGNMENT_CONFIG)
    rows = read_worksheet(path)

    assert len(rows) == 2
    assert rows[0]["student_key"] == "janedoe"
    assert rows[0]["mech_submission"] == "True"
    assert rows[0]["human_correctness"] == ""
    assert rows[0]["human_code_quality"] == ""
    assert rows[0]["captured_output"] == "hello world"
    assert rows[1]["status"] == "fetch-failed"


def test_incomplete_students_flags_blank_human_fields(tmp_path):
    path = tmp_path / "review.csv"
    students = [
        {"student_key": "janedoe", "student_name": "Jane Doe", "status": "ok", "submission": True},
        {"student_key": "johnsmith", "student_name": "John Smith", "status": "ok", "submission": True},
    ]
    build_worksheet(path, students, ASSIGNMENT_CONFIG)
    rows = read_worksheet(path)
    # instructor fills in Jane's fields but not John's
    rows[0]["human_correctness"] = "4"
    rows[0]["human_code_quality"] = "2"

    result = incomplete_students(rows, ASSIGNMENT_CONFIG)

    assert result == ["johnsmith"]


def test_incomplete_students_skips_fetch_failed_rows(tmp_path):
    path = tmp_path / "review.csv"
    students = [
        {"student_key": "janedoe", "student_name": "Jane Doe", "status": "fetch-failed"},
    ]
    build_worksheet(path, students, ASSIGNMENT_CONFIG)
    rows = read_worksheet(path)

    assert incomplete_students(rows, ASSIGNMENT_CONFIG) == []
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /Users/markumreed/Documents/ism_courses/autograder && pytest tests/test_worksheet.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'autograder_common.worksheet'`

- [ ] **Step 3: Write the implementation**

Create `autograder/autograder_common/worksheet.py`:

```python
"""Build and read the review worksheet CSV: mechanical results auto-filled,
human-scored rubric fields left blank for the instructor to complete."""
import csv
from pathlib import Path

MECHANICAL_COLUMN_PREFIX = "mech_"
HUMAN_COLUMN_PREFIX = "human_"


def human_fields(assignment_config):
    """Rubric field names whose source is 'human' (need instructor input),
    in the order they appear in the config."""
    return [
        name for name, spec in assignment_config["rubric"].items()
        if spec.get("source") == "human"
    ]


def mechanical_fields(assignment_config):
    """Rubric field names whose source is 'mechanical'."""
    return [
        name for name, spec in assignment_config["rubric"].items()
        if spec.get("source") == "mechanical"
    ]


def build_worksheet(path, students, assignment_config):
    """Write the review worksheet CSV.

    students: list of dicts, each with at least student_key, student_name,
    status, and (for mechanical fields) that field's already-computed value
    keyed directly on the dict, e.g. {"submission": True, ...}.
    Human-scored fields are always written blank.
    """
    human = human_fields(assignment_config)
    mechanical = mechanical_fields(assignment_config)
    fieldnames = (
        ["student_key", "student_name", "status"]
        + [f"{MECHANICAL_COLUMN_PREFIX}{f}" for f in mechanical]
        + [f"{HUMAN_COLUMN_PREFIX}{f}" for f in human]
        + ["captured_output", "comment"]
    )
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for student in students:
            row = {
                "student_key": student["student_key"],
                "student_name": student["student_name"],
                "status": student["status"],
                "captured_output": student.get("captured_output", ""),
                "comment": "",
            }
            for f in mechanical:
                row[f"{MECHANICAL_COLUMN_PREFIX}{f}"] = student.get(f, "")
            for f in human:
                row[f"{HUMAN_COLUMN_PREFIX}{f}"] = ""
            writer.writerow(row)


def read_worksheet(path):
    """Read a worksheet CSV back into a list of dicts (all values strings,
    as written by csv.DictReader)."""
    path = Path(path)
    with path.open(newline="") as fh:
        return list(csv.DictReader(fh))


def incomplete_students(rows, assignment_config):
    """Return the student_keys (for rows with status == 'ok') whose
    human-scored fields are still blank."""
    human = human_fields(assignment_config)
    incomplete = []
    for row in rows:
        if row.get("status") != "ok":
            continue
        for f in human:
            if not row.get(f"{HUMAN_COLUMN_PREFIX}{f}", "").strip():
                incomplete.append(row["student_key"])
                break
    return incomplete
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /Users/markumreed/Documents/ism_courses/autograder && pytest tests/test_worksheet.py -v`
Expected: 4 passed

- [ ] **Step 5: Commit**

```bash
cd /Users/markumreed/Documents/ism_courses
git add autograder/autograder_common/worksheet.py autograder/tests/test_worksheet.py
git commit -m "Add review worksheet build/read"
```

---

## Task 7: Rubric scoring (`scoring.py`)

**Files:**
- Create: `autograder/autograder_common/scoring.py`
- Test: `autograder/tests/test_scoring.py`

**Interfaces:**
- Consumes: `worksheet.MECHANICAL_COLUMN_PREFIX`, `worksheet.HUMAN_COLUMN_PREFIX` (Task 6); a worksheet row (`dict[str, str]`, from `read_worksheet`) and an `assignment_config` (Task 2).
- Produces: `ScoringError(Exception)`, `compute_points_score(row, assignment_config) -> float`, `compute_capstone_score(row, assignment_config) -> float`, `compute_score(row, assignment_config) -> float` (dispatches on `assignment_config.get("scoring_type", "points")`).

- [ ] **Step 1: Write the failing tests**

Create `autograder/tests/test_scoring.py`:

```python
import pytest

from autograder_common.scoring import (
    ScoringError,
    compute_capstone_score,
    compute_points_score,
    compute_score,
)

POINTS_CONFIG = {
    "scoring_type": "points",
    "rubric": {
        "submission": {"points": 1, "source": "mechanical", "check": "file_present"},
        "correctness": {"points": 4, "source": "human"},
        "code_quality": {"points": 2, "source": "human"},
    },
}

CAPSTONE_CONFIG = {
    "scoring_type": "capstone_levels",
    "rubric": {
        "code_clarity": {"source": "human"},
        "visualizations": {"source": "human"},
        "insight_quality": {"source": "human"},
        "communication": {"source": "human"},
    },
}


def test_compute_points_score_sums_mechanical_and_human():
    row = {
        "mech_submission": "True",
        "human_correctness": "4",
        "human_code_quality": "1",
    }

    assert compute_points_score(row, POINTS_CONFIG) == 6.0


def test_compute_points_score_mechanical_not_earned_scores_zero():
    row = {
        "mech_submission": "False",
        "human_correctness": "4",
        "human_code_quality": "2",
    }

    assert compute_points_score(row, POINTS_CONFIG) == 6.0


def test_compute_points_score_missing_human_field_raises():
    row = {"mech_submission": "True", "human_correctness": "4", "human_code_quality": ""}

    with pytest.raises(ScoringError, match="code_quality"):
        compute_points_score(row, POINTS_CONFIG)


def test_compute_points_score_human_value_out_of_range_raises():
    row = {"mech_submission": "True", "human_correctness": "40", "human_code_quality": "2"}

    with pytest.raises(ScoringError, match="outside 0..4"):
        compute_points_score(row, POINTS_CONFIG)


def test_compute_capstone_score_averages_levels_times_25():
    row = {
        "human_code_clarity": "excellent",
        "human_visualizations": "good",
        "human_insight_quality": "good",
        "human_communication": "excellent",
    }
    # levels: 4, 3, 3, 4 -> avg 3.5 -> 3.5 * 25 = 87.5
    assert compute_capstone_score(row, CAPSTONE_CONFIG) == 87.5


def test_compute_capstone_score_all_incomplete_is_25():
    row = {
        "human_code_clarity": "incomplete",
        "human_visualizations": "incomplete",
        "human_insight_quality": "incomplete",
        "human_communication": "incomplete",
    }
    assert compute_capstone_score(row, CAPSTONE_CONFIG) == 25.0


def test_compute_capstone_score_invalid_level_raises():
    row = {
        "human_code_clarity": "amazing",
        "human_visualizations": "good",
        "human_insight_quality": "good",
        "human_communication": "good",
    }
    with pytest.raises(ScoringError, match="code_clarity"):
        compute_capstone_score(row, CAPSTONE_CONFIG)


def test_compute_score_dispatches_points():
    row = {"mech_submission": "True", "human_correctness": "4", "human_code_quality": "2"}
    assert compute_score(row, POINTS_CONFIG) == 7.0


def test_compute_score_dispatches_capstone_levels():
    row = {
        "human_code_clarity": "good",
        "human_visualizations": "good",
        "human_insight_quality": "good",
        "human_communication": "good",
    }
    assert compute_score(row, CAPSTONE_CONFIG) == 75.0


def test_compute_score_defaults_to_points_when_scoring_type_absent():
    config = {"rubric": POINTS_CONFIG["rubric"]}
    row = {"mech_submission": "True", "human_correctness": "4", "human_code_quality": "2"}
    assert compute_score(row, config) == 7.0
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /Users/markumreed/Documents/ism_courses/autograder && pytest tests/test_scoring.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'autograder_common.scoring'`

- [ ] **Step 3: Write the implementation**

Create `autograder/autograder_common/scoring.py`:

```python
"""Convert a completed worksheet row into a final numeric grade, per an
assignment's rubric config."""
from .worksheet import HUMAN_COLUMN_PREFIX, MECHANICAL_COLUMN_PREFIX

LEVEL_VALUES = {"excellent": 4, "good": 3, "developing": 2, "incomplete": 1}


class ScoringError(Exception):
    pass


def compute_points_score(row, assignment_config):
    """Points-based rubric (labs, weekly assignments, developer workflow,
    ISM3232 capstone): sum each rubric field's points.

    Mechanical fields: row['mech_<field>'] is 'True' (earned, full points)
    or anything else (not earned, 0 points).
    Human fields: row['human_<field>'] is a number from 0..points, entered
    directly by the instructor (supports partial credit).
    """
    total = 0.0
    for name, spec in assignment_config["rubric"].items():
        points = spec["points"]
        if spec["source"] == "mechanical":
            raw = row.get(f"{MECHANICAL_COLUMN_PREFIX}{name}", "")
            earned = raw.strip().lower() in ("true", "1", "yes")
            total += points if earned else 0
        else:
            raw = row.get(f"{HUMAN_COLUMN_PREFIX}{name}", "").strip()
            if not raw:
                raise ScoringError(
                    f"human field {name!r} is blank for {row.get('student_key')}"
                )
            value = float(raw)
            if value < 0 or value > points:
                raise ScoringError(
                    f"human field {name!r} for {row.get('student_key')} is {value}, "
                    f"outside 0..{points}"
                )
            total += value
    return total


def compute_capstone_score(row, assignment_config):
    """Level-based rubric (ISM2411 capstone): each dimension in
    assignment_config['rubric'] is source: human, and the instructor enters
    one of excellent/good/developing/incomplete into human_<dimension>.
    Final score = average(level value 1-4 across dimensions) * 25.
    """
    dimensions = list(assignment_config["rubric"].keys())
    values = []
    for name in dimensions:
        raw = row.get(f"{HUMAN_COLUMN_PREFIX}{name}", "").strip().lower()
        if raw not in LEVEL_VALUES:
            raise ScoringError(
                f"dimension {name!r} for {row.get('student_key')} must be one of "
                f"{sorted(LEVEL_VALUES)}, got {raw!r}"
            )
        values.append(LEVEL_VALUES[raw])
    return (sum(values) / len(values)) * 25


def compute_score(row, assignment_config):
    """Dispatch to compute_points_score or compute_capstone_score based on
    assignment_config.get('scoring_type', 'points')."""
    scoring_type = assignment_config.get("scoring_type", "points")
    if scoring_type == "points":
        return compute_points_score(row, assignment_config)
    if scoring_type == "capstone_levels":
        return compute_capstone_score(row, assignment_config)
    raise ScoringError(f"unknown scoring_type: {scoring_type!r}")
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /Users/markumreed/Documents/ism_courses/autograder && pytest tests/test_scoring.py -v`
Expected: 10 passed

- [ ] **Step 5: Commit**

```bash
cd /Users/markumreed/Documents/ism_courses
git add autograder/autograder_common/scoring.py autograder/tests/test_scoring.py
git commit -m "Add rubric scoring (points and capstone-level formulas)"
```

---

## Task 8: CLI integration (`cli.py`)

**Files:**
- Create: `autograder/autograder_common/cli.py`
- Test: `autograder/tests/test_cli.py`

**Interfaces:**
- Consumes: `config.load_course_config`, `config.load_assignment_config` (Task 2); `canvas.CanvasClient` (Task 3); `checks.*` (Task 4); `fetch.fetch_submission`, `fetch.FetchError` (Task 5); `worksheet.build_worksheet`, `worksheet.read_worksheet`, `worksheet.incomplete_students` (Task 6); `scoring.compute_score` (Task 7).
- Produces: `cmd_fetch(args, course_config_path, assignments_dir, runs_dir)`, `cmd_check(...)`, `cmd_upload(...)`, `build_cli(course_config_path, assignments_dir, runs_dir="runs") -> argparse.ArgumentParser`, `main(course_config_path, assignments_dir, argv=None)`.

- [ ] **Step 1: Write the failing tests**

Create `autograder/tests/test_cli.py`:

```python
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from autograder_common import cli


def write_course_config(tmp_path, monkeypatch):
    monkeypatch.setenv("CANVAS_API_TOKEN", "tok")
    path = tmp_path / "course.yaml"
    path.write_text("canvas_base_url: 'https://example.instructure.com'\ncanvas_course_id: 10\n")
    return path


def write_assignment_config(assignments_dir, name, body):
    assignments_dir.mkdir(parents=True, exist_ok=True)
    (assignments_dir / f"{name}.yaml").write_text(body)


LAB_CONFIG_BODY = """
course: ism2411
key: week03_lab
canvas_display_name: 'Lab 3'
submission_type: canvas_upload
expected_files: ['pricer.py']
run:
  command: "python3 {file}"
  timeout_seconds: 10
mechanical_checks: ['file_present', 'runs_without_error']
scoring_type: points
rubric:
  submission:
    points: 1
    source: mechanical
    check: file_present
  correctness:
    points: 4
    source: human
"""


def test_cmd_fetch_downloads_each_submission(tmp_path, monkeypatch):
    course_config_path = write_course_config(tmp_path, monkeypatch)
    assignments_dir = tmp_path / "assignments"
    write_assignment_config(assignments_dir, "week03_lab", LAB_CONFIG_BODY)

    fake_client = MagicMock()
    fake_client.find_assignment_id.return_value = 42
    fake_client.list_submissions.return_value = [
        {"user_id": 1, "user": {"name": "Jane Doe"}, "attachments": [{"filename": "pricer.py", "url": "u"}]},
    ]

    with patch.object(cli, "CanvasClient", return_value=fake_client), \
         patch.object(cli.fetch, "fetch_submission") as fake_fetch:
        args = SimpleNamespace(assignment="week03_lab")
        cli.cmd_fetch(args, course_config_path, assignments_dir, tmp_path / "runs")

    fake_fetch.assert_called_once()
    dest_dir_arg = fake_fetch.call_args[0][3]
    assert dest_dir_arg == tmp_path / "runs" / "week03_lab" / "janedoe"


def test_cmd_check_builds_worksheet_with_mechanical_results(tmp_path, monkeypatch):
    course_config_path = write_course_config(tmp_path, monkeypatch)
    assignments_dir = tmp_path / "assignments"
    write_assignment_config(assignments_dir, "week03_lab", LAB_CONFIG_BODY)

    student_dir = tmp_path / "runs" / "week03_lab" / "janedoe"
    student_dir.mkdir(parents=True)
    (student_dir / "pricer.py").write_text("print('12 units of Notebook at $4.99 each = $59.88')\n")

    fake_client = MagicMock()
    fake_client.find_assignment_id.return_value = 42
    fake_client.list_submissions.return_value = [
        {"user_id": 1, "user": {"name": "Jane Doe"}},
    ]

    with patch.object(cli, "CanvasClient", return_value=fake_client):
        args = SimpleNamespace(assignment="week03_lab")
        cli.cmd_check(args, course_config_path, assignments_dir, tmp_path / "runs")

    rows = cli.worksheet.read_worksheet(tmp_path / "runs" / "week03_lab" / "review.csv")
    assert rows[0]["student_key"] == "janedoe"
    assert rows[0]["mech_submission"] == "True"
    assert "59.88" in rows[0]["captured_output"]
    assert rows[0]["human_correctness"] == ""


def test_cmd_upload_blocks_on_incomplete_worksheet(tmp_path, monkeypatch, capsys):
    course_config_path = write_course_config(tmp_path, monkeypatch)
    assignments_dir = tmp_path / "assignments"
    write_assignment_config(assignments_dir, "week03_lab", LAB_CONFIG_BODY)

    worksheet_path = tmp_path / "runs" / "week03_lab" / "review.csv"
    cli.worksheet.build_worksheet(
        worksheet_path,
        [{"student_key": "janedoe", "student_name": "Jane Doe", "status": "ok", "submission": True}],
        cli.load_assignment_config(assignments_dir / "week03_lab.yaml"),
    )

    fake_client = MagicMock()
    with patch.object(cli, "CanvasClient", return_value=fake_client):
        args = SimpleNamespace(assignment="week03_lab", dry_run=False, yes=False)
        with pytest.raises(SystemExit):
            cli.cmd_upload(args, course_config_path, assignments_dir, tmp_path / "runs")

    fake_client.post_grade.assert_not_called()
    assert "janedoe" in capsys.readouterr().out


def test_cmd_upload_dry_run_does_not_post(tmp_path, monkeypatch, capsys):
    course_config_path = write_course_config(tmp_path, monkeypatch)
    assignments_dir = tmp_path / "assignments"
    write_assignment_config(assignments_dir, "week03_lab", LAB_CONFIG_BODY)

    worksheet_path = tmp_path / "runs" / "week03_lab" / "review.csv"
    cli.worksheet.build_worksheet(
        worksheet_path,
        [{"student_key": "janedoe", "student_name": "Jane Doe", "status": "ok", "submission": True}],
        cli.load_assignment_config(assignments_dir / "week03_lab.yaml"),
    )
    rows = cli.worksheet.read_worksheet(worksheet_path)
    rows[0]["human_correctness"] = "4"
    _rewrite_csv(worksheet_path, rows)

    fake_client = MagicMock()
    fake_client.find_assignment_id.return_value = 42
    fake_client.list_submissions.return_value = [{"user_id": 1, "user": {"name": "Jane Doe"}}]
    fake_client.get_current_grade.return_value = None

    with patch.object(cli, "CanvasClient", return_value=fake_client):
        args = SimpleNamespace(assignment="week03_lab", dry_run=True, yes=False)
        cli.cmd_upload(args, course_config_path, assignments_dir, tmp_path / "runs")

    fake_client.post_grade.assert_not_called()
    assert "Dry run" in capsys.readouterr().out


def test_cmd_upload_posts_and_writes_log(tmp_path, monkeypatch, capsys):
    course_config_path = write_course_config(tmp_path, monkeypatch)
    assignments_dir = tmp_path / "assignments"
    write_assignment_config(assignments_dir, "week03_lab", LAB_CONFIG_BODY)

    worksheet_path = tmp_path / "runs" / "week03_lab" / "review.csv"
    cli.worksheet.build_worksheet(
        worksheet_path,
        [{"student_key": "janedoe", "student_name": "Jane Doe", "status": "ok", "submission": True}],
        cli.load_assignment_config(assignments_dir / "week03_lab.yaml"),
    )
    rows = cli.worksheet.read_worksheet(worksheet_path)
    rows[0]["human_correctness"] = "4"
    _rewrite_csv(worksheet_path, rows)

    fake_client = MagicMock()
    fake_client.find_assignment_id.return_value = 42
    fake_client.list_submissions.return_value = [{"user_id": 1, "user": {"name": "Jane Doe"}}]
    fake_client.get_current_grade.return_value = 3

    with patch.object(cli, "CanvasClient", return_value=fake_client):
        args = SimpleNamespace(assignment="week03_lab", dry_run=False, yes=True)
        cli.cmd_upload(args, course_config_path, assignments_dir, tmp_path / "runs")

    fake_client.post_grade.assert_called_once_with(42, 1, 5.0, None)
    log_files = list((tmp_path / "runs" / "week03_lab").glob("upload_log_*.json"))
    assert len(log_files) == 1


def _rewrite_csv(path, rows):
    import csv
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /Users/markumreed/Documents/ism_courses/autograder && pytest tests/test_cli.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'autograder_common.cli'`

- [ ] **Step 3: Write the implementation**

Create `autograder/autograder_common/cli.py`:

```python
"""Shared CLI scaffolding: fetch / check / upload subcommands, parameterized
by a course's Canvas config and its assignments directory."""
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from . import checks, fetch, scoring, worksheet
from .canvas import CanvasClient
from .config import load_assignment_config, load_course_config


def _student_key(user_name):
    return "".join(ch for ch in user_name.lower() if ch.isalnum())


def _load(course_config_path, assignments_dir, assignment_key):
    course_config = load_course_config(course_config_path)
    assignment_config = load_assignment_config(
        Path(assignments_dir) / f"{assignment_key}.yaml"
    )
    client = CanvasClient(
        course_config["canvas_base_url"],
        course_config["canvas_course_id"],
        course_config["canvas_token"],
    )
    return course_config, assignment_config, client


def _assignment_id(assignment_config, client):
    override = assignment_config.get("canvas_assignment_id")
    if override:
        return override
    return client.find_assignment_id(assignment_config["canvas_display_name"])


def cmd_fetch(args, course_config_path, assignments_dir, runs_dir):
    _, assignment_config, client = _load(course_config_path, assignments_dir, args.assignment)
    assignment_id = _assignment_id(assignment_config, client)
    submissions = client.list_submissions(assignment_id)
    out_dir = Path(runs_dir) / args.assignment
    out_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    for sub in submissions:
        user = sub.get("user") or {}
        name = user.get("name", f"user-{sub.get('user_id')}")
        dest = out_dir / _student_key(name)
        try:
            fetch.fetch_submission(sub, assignment_config, client, dest)
            count += 1
        except fetch.FetchError as e:
            print(f"  {name}: fetch failed - {e}")
    print(f"Fetched {count}/{len(submissions)} submissions to {out_dir}")


def _compute_signals(student_dir, assignment_config):
    """Run every mechanical primitive listed in assignment_config['mechanical_checks']
    once. Returns (signals: {check_id: (passed, output)}, captured_output: str)."""
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


def cmd_check(args, course_config_path, assignments_dir, runs_dir):
    _, assignment_config, client = _load(course_config_path, assignments_dir, args.assignment)
    assignment_id = _assignment_id(assignment_config, client)
    submissions = client.list_submissions(assignment_id)
    out_dir = Path(runs_dir) / args.assignment

    students = []
    for sub in submissions:
        user = sub.get("user") or {}
        name = user.get("name", f"user-{sub.get('user_id')}")
        key = _student_key(name)
        student_dir = out_dir / key
        if not student_dir.exists():
            students.append({
                "student_key": key, "student_name": name,
                "status": "fetch-failed", "captured_output": "",
            })
            continue

        signals, captured = _compute_signals(student_dir, assignment_config)
        record = {"student_key": key, "student_name": name, "status": "ok", "captured_output": captured}
        for field_name, spec in assignment_config["rubric"].items():
            if spec.get("source") == "mechanical":
                passed, _ = signals.get(spec["check"], (False, ""))
                record[field_name] = passed
        students.append(record)

    worksheet_path = out_dir / "review.csv"
    worksheet.build_worksheet(worksheet_path, students, assignment_config)
    print(f"Wrote {worksheet_path}")


def cmd_upload(args, course_config_path, assignments_dir, runs_dir):
    course_config, assignment_config, client = _load(course_config_path, assignments_dir, args.assignment)
    assignment_id = _assignment_id(assignment_config, client)

    worksheet_path = Path(runs_dir) / args.assignment / "review.csv"
    rows = worksheet.read_worksheet(worksheet_path)
    incomplete = worksheet.incomplete_students(rows, assignment_config)
    if incomplete:
        print("Cannot upload - these students have incomplete human-scored fields:")
        for key in incomplete:
            print(f"  {key}")
        sys.exit(1)

    submissions = client.list_submissions(assignment_id)
    key_to_user_id = {
        _student_key((s.get("user") or {}).get("name", f"user-{s['user_id']}")): s["user_id"]
        for s in submissions
    }

    plan = []
    for row in rows:
        if row.get("status") != "ok":
            continue
        user_id = key_to_user_id.get(row["student_key"])
        if user_id is None:
            print(f"  {row['student_name']}: no matching Canvas submission, skipping")
            continue
        score = scoring.compute_score(row, assignment_config)
        current = client.get_current_grade(assignment_id, user_id)
        plan.append((user_id, row["student_name"], current, score, row.get("comment", "")))

    for _, name, current, new, _ in plan:
        current_str = "ungraded" if current is None else current
        print(f"  {name}: {current_str} -> {new}")

    if args.dry_run:
        print(f"Dry run - {len(plan)} grade(s) would be posted, nothing sent.")
        return

    if not args.yes:
        answer = input(f"Post {len(plan)} grade(s) for {args.assignment}? [y/N] ")
        if answer.strip().lower() != "y":
            print("Aborted.")
            return

    log = []
    for user_id, name, current, new, comment in plan:
        client.post_grade(assignment_id, user_id, new, comment or None)
        log.append({"user_id": user_id, "name": name, "previous": current, "posted": new})

    runs_dir_path = Path(runs_dir) / args.assignment
    runs_dir_path.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    log_path = runs_dir_path / f"upload_log_{timestamp}.json"
    log_path.write_text(json.dumps(log, indent=2))
    print(f"Posted {len(log)} grade(s). Log: {log_path}")


def build_cli(course_config_path, assignments_dir, runs_dir="runs"):
    """Build an argparse.ArgumentParser with fetch/check/upload subcommands
    wired to one course's config + assignments directory."""
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    fetch_p = sub.add_parser("fetch")
    fetch_p.add_argument("--assignment", required=True)
    fetch_p.set_defaults(func=lambda a: cmd_fetch(a, course_config_path, assignments_dir, runs_dir))

    check_p = sub.add_parser("check")
    check_p.add_argument("--assignment", required=True)
    check_p.set_defaults(func=lambda a: cmd_check(a, course_config_path, assignments_dir, runs_dir))

    upload_p = sub.add_parser("upload")
    upload_p.add_argument("--assignment", required=True)
    upload_p.add_argument("--dry-run", action="store_true")
    upload_p.add_argument("--yes", action="store_true")
    upload_p.set_defaults(func=lambda a: cmd_upload(a, course_config_path, assignments_dir, runs_dir))

    return parser


def main(course_config_path, assignments_dir, argv=None):
    parser = build_cli(course_config_path, assignments_dir)
    args = parser.parse_args(argv)
    args.func(args)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /Users/markumreed/Documents/ism_courses/autograder && pytest tests/test_cli.py -v`
Expected: 5 passed

- [ ] **Step 5: Run the full test suite**

Run: `cd /Users/markumreed/Documents/ism_courses/autograder && pytest -v`
Expected: all tests across every module pass (config, canvas, checks, fetch, worksheet, scoring, cli)

- [ ] **Step 6: Commit**

```bash
cd /Users/markumreed/Documents/ism_courses
git add autograder/autograder_common/cli.py autograder/tests/test_cli.py
git commit -m "Add fetch/check/upload CLI wiring the full engine together"
```

---

## Task 9: Course entrypoints and course configs

**Files:**
- Create: `autograder/grade_ism2411.py`
- Create: `autograder/grade_ism3232.py`
- Create: `autograder/ism2411.config.yaml`
- Create: `autograder/ism3232.config.yaml`

**Interfaces:**
- Consumes: `autograder_common.cli.main` (Task 8).
- Produces: two runnable CLI scripts.

- [ ] **Step 1: Create the course config templates**

Create `autograder/ism2411.config.yaml`:

```yaml
# Fill in your institution's real Canvas details before running fetch/upload.
# canvas_base_url is your Canvas instance's root URL (e.g. the URL you see
# when logged into Canvas, without any /courses/... path).
# canvas_course_id is the number in the course's Canvas URL:
#   https://YOUR_INSTITUTION.instructure.com/courses/12345
#                                                     ^^^^^ this
canvas_base_url: "https://YOUR_INSTITUTION.instructure.com"
canvas_course_id: 0
```

Create `autograder/ism3232.config.yaml` (same shape):

```yaml
# Fill in your institution's real Canvas details before running fetch/upload.
canvas_base_url: "https://YOUR_INSTITUTION.instructure.com"
canvas_course_id: 0
```

- [ ] **Step 2: Create the entrypoint scripts**

Create `autograder/grade_ism2411.py`:

```python
#!/usr/bin/env python3
"""ISM2411 autograder CLI. See README.md for setup and usage.

Usage:
    python grade_ism2411.py fetch  --assignment week03_lab
    python grade_ism2411.py check  --assignment week03_lab
    python grade_ism2411.py upload --assignment week03_lab --dry-run
    python grade_ism2411.py upload --assignment week03_lab
"""
from pathlib import Path

from autograder_common.cli import main

ROOT = Path(__file__).resolve().parent

if __name__ == "__main__":
    main(
        course_config_path=ROOT / "ism2411.config.yaml",
        assignments_dir=ROOT / "assignments" / "ism2411",
    )
```

Create `autograder/grade_ism3232.py`:

```python
#!/usr/bin/env python3
"""ISM3232 autograder CLI. See README.md for setup and usage.

Usage:
    python grade_ism3232.py fetch  --assignment week07_assignment
    python grade_ism3232.py check  --assignment week07_assignment
    python grade_ism3232.py upload --assignment week07_assignment --dry-run
    python grade_ism3232.py upload --assignment week07_assignment
"""
from pathlib import Path

from autograder_common.cli import main

ROOT = Path(__file__).resolve().parent

if __name__ == "__main__":
    main(
        course_config_path=ROOT / "ism3232.config.yaml",
        assignments_dir=ROOT / "assignments" / "ism3232",
    )
```

- [ ] **Step 3: Verify both entrypoints load and show usage without a real Canvas token**

Run: `cd /Users/markumreed/Documents/ism_courses/autograder && python3 grade_ism2411.py --help`
Expected: argparse usage output listing `{fetch,check,upload}` subcommands, exit code 0

Run: `cd /Users/markumreed/Documents/ism_courses/autograder && python3 grade_ism3232.py --help`
Expected: same, exit code 0

- [ ] **Step 4: Commit**

```bash
cd /Users/markumreed/Documents/ism_courses
git add autograder/grade_ism2411.py autograder/grade_ism3232.py autograder/ism2411.config.yaml autograder/ism3232.config.yaml
git commit -m "Add grade_ism2411.py and grade_ism3232.py entrypoints"
```

---

## Task 10: ISM2411 pilot assignment configs

**Files:**
- Create: `autograder/assignments/ism2411/week03_lab.yaml`
- Create: `autograder/assignments/ism2411/capstone.yaml`

**Interfaces:**
- Consumes: `config.load_assignment_config` (Task 2) as the validator.

- [ ] **Step 1: Create the week03_lab pilot config**

Create `autograder/assignments/ism2411/week03_lab.yaml`:

```yaml
course: ism2411
key: week03_lab
# Exact Canvas assignment name to look up via the API. Set
# canvas_assignment_id below instead if the name lookup is ambiguous or the
# real Canvas assignment is named differently.
canvas_display_name: "Lab 3: Product Pricer with F-Strings"
canvas_assignment_id: null
submission_type: canvas_upload
expected_files: ["pricer.py"]
run:
  command: "python3 {file}"
  timeout_seconds: 10
mechanical_checks: ["file_present", "runs_without_error"]
scoring_type: points
# Matches the syllabus's fixed 10-point Lab Grading Rubric
# (see syllabi/ism2411_simple_syllabus.md), applied identically to every lab.
rubric:
  submission:
    points: 1
    source: mechanical
    check: file_present
  correctness:
    points: 4
    source: human
    prompt: >-
      Compare the captured stdout to each exercise's stated "Expected: ..."
      output on ism2411/pages/week03_lab.html (exercises 1-4).
  completion:
    points: 3
    source: human
    prompt: "Are exercises 1-4 all attempted and present in the file?"
  code_quality:
    points: 2
    source: human
    prompt: "Meaningful variable names, no unneeded repetition, readable code."
```

- [ ] **Step 2: Create the ISM2411 capstone pilot config**

Create `autograder/assignments/ism2411/capstone.yaml`:

```yaml
course: ism2411
key: capstone
canvas_display_name: "Capstone Project"
canvas_assignment_id: null
submission_type: github_url
expected_files: []
mechanical_checks: ["file_present", "runs_without_error"]
scoring_type: capstone_levels
# Matches the 4-dimension rubric in ism2411/pages/capstone_rubric.html,
# each 25% of the capstone grade. Enter one of
# excellent/good/developing/incomplete per dimension; the final score is
# average(level 1-4) * 25, exactly as the rubric page states.
rubric:
  code_clarity:
    source: human
    prompt: >-
      Can someone else read this code and understand what it does? See the
      Code Clarity rubric cell on capstone_rubric.html for level definitions.
  visualizations:
    source: human
    prompt: "Do the charts communicate, or do they just exist? See Visualizations rubric cell."
  insight_quality:
    source: human
    prompt: "See Insight Quality rubric cell on capstone_rubric.html."
  communication:
    source: human
    prompt: "See Communication rubric cell on capstone_rubric.html."
```

- [ ] **Step 3: Verify both configs load and validate**

Run:
```bash
cd /Users/markumreed/Documents/ism_courses/autograder
python3 -c "
from autograder_common.config import load_assignment_config
c1 = load_assignment_config('assignments/ism2411/week03_lab.yaml')
c2 = load_assignment_config('assignments/ism2411/capstone.yaml')
assert c1['submission_type'] == 'canvas_upload'
assert c2['scoring_type'] == 'capstone_levels'
print('ok')
"
```
Expected: `ok`

- [ ] **Step 4: Commit**

```bash
cd /Users/markumreed/Documents/ism_courses
git add autograder/assignments/ism2411/week03_lab.yaml autograder/assignments/ism2411/capstone.yaml
git commit -m "Add ISM2411 pilot assignment configs (week03 lab + capstone)"
```

---

## Task 11: ISM3232 pilot assignment configs

**Files:**
- Create: `autograder/assignments/ism3232/week07_assignment.yaml`
- Create: `autograder/assignments/ism3232/developer_workflow.yaml`
- Create: `autograder/assignments/ism3232/capstone.yaml`

**Interfaces:**
- Consumes: `config.load_assignment_config` (Task 2) as the validator.

- [ ] **Step 1: Create the week07 pilot config**

Create `autograder/assignments/ism3232/week07_assignment.yaml`:

```yaml
course: ism3232
key: week07_assignment
canvas_display_name: "Assignment 7: Functions, Modules & pytest"
canvas_assignment_id: null
submission_type: github_url
expected_files: ["main.py"]
run:
  command: "python3 {file}"
  timeout_seconds: 10
mechanical_checks: ["file_present", "runs_without_error", "pytest_passes"]
scoring_type: points
# Point split is a template default (15 total) - adjust to match the real
# Canvas assignment's configured point value once known. Correctness is
# still human-scored: ism3232/docs/week07_lab.html asks for
# "pytest -v with all eight tests green" via screenshot, which the
# instructor confirms visually rather than trusting a student-authored
# suite as ground truth (captured pytest output is shown for reference).
rubric:
  submission:
    points: 2
    source: mechanical
    check: file_present
  correctness:
    points: 10
    source: human
    prompt: >-
      Compare captured main.py output and pytest results to the deliverables
      listed on ism3232/docs/week07_lab.html.
  code_quality:
    points: 3
    source: human
    prompt: "Meaningful names, docstrings/comments where useful, readable code."
```

- [ ] **Step 2: Create the Developer Workflow pilot config**

Create `autograder/assignments/ism3232/developer_workflow.yaml`:

```yaml
course: ism3232
key: developer_workflow
# Developer Workflow is assessed "holistically across all submissions
# throughout the semester" per the syllabus (15% of the final grade), not
# tied to one week's deliverable. Point this at a running "Developer
# Workflow" gradebook column you create in Canvas, and re-run
# fetch/check/upload against whichever repo state you want to score.
canvas_display_name: "Developer Workflow"
canvas_assignment_id: null
submission_type: github_url
expected_files: []
mechanical_checks:
  - ruff_clean
  - pytest_passes
  - git_log_commit_count
  - git_log_message_quality
  - git_log_spread
scoring_type: points
# Translates the syllabus's 5 assessed criteria (Developer Workflow Grade,
# 15%) into a 5x3-point breakdown. Fully mechanical - no human input.
rubric:
  ritual_evidence:
    points: 3
    source: mechanical
    check: git_log_commit_count
  ruff_clean:
    points: 3
    source: mechanical
    check: ruff_clean
  pytest_green:
    points: 3
    source: mechanical
    check: pytest_passes
  commit_message_quality:
    points: 3
    source: mechanical
    check: git_log_message_quality
  commit_history_iterative:
    points: 3
    source: mechanical
    check: git_log_spread
```

- [ ] **Step 3: Create the ISM3232 capstone pilot config**

Create `autograder/assignments/ism3232/capstone.yaml`:

```yaml
course: ism3232
key: capstone
canvas_display_name: "Capstone Project"
canvas_assignment_id: null
submission_type: github_url
expected_files: []
mechanical_checks: ["file_present", "runs_without_error", "pytest_passes"]
scoring_type: points
# Matches the 5-component, 100-point rubric in
# ism3232/docs/capstone_rubric.html exactly (each component's point tiers
# are discrete: e.g. OOP Design is 25/18/12/6/0, not a continuous scale).
# The instructor enters the tier's point value directly for each component.
rubric:
  proposal_design:
    points: 15
    source: human
    prompt: "Proposal & Design Document - see capstone_rubric.html component 1 (15/10/5/0 tiers)."
  oop_design:
    points: 25
    source: human
    prompt: "OOP Design (models.py) - see capstone_rubric.html component 2 (25/18/12/6/0 tiers)."
  database_layer:
    points: 20
    source: human
    prompt: "Database Layer (database.py) - see capstone_rubric.html component 3 (20/14/8/4/0 tiers)."
  streamlit_interface:
    points: 25
    source: human
    prompt: "Streamlit Interface (app.py) - see capstone_rubric.html component 4 (25/.../0 tiers)."
  genai_feature:
    points: 15
    source: human
    prompt: "GenAI Feature (ai_feature.py) - see capstone_rubric.html component 5 (15/.../0 tiers)."
```

- [ ] **Step 4: Verify all three configs load and validate**

Run:
```bash
cd /Users/markumreed/Documents/ism_courses/autograder
python3 -c "
from autograder_common.config import load_assignment_config
c1 = load_assignment_config('assignments/ism3232/week07_assignment.yaml')
c2 = load_assignment_config('assignments/ism3232/developer_workflow.yaml')
c3 = load_assignment_config('assignments/ism3232/capstone.yaml')
assert c1['submission_type'] == 'github_url'
assert sum(f['points'] for f in c2['rubric'].values()) == 15
assert sum(f['points'] for f in c3['rubric'].values()) == 100
print('ok')
"
```
Expected: `ok`

- [ ] **Step 5: Commit**

```bash
cd /Users/markumreed/Documents/ism_courses
git add autograder/assignments/ism3232/week07_assignment.yaml autograder/assignments/ism3232/developer_workflow.yaml autograder/assignments/ism3232/capstone.yaml
git commit -m "Add ISM3232 pilot assignment configs (week07, developer workflow, capstone)"
```

---

## Task 12: Setup documentation

**Files:**
- Create: `autograder/README.md`

**Interfaces:**
- Consumes: nothing (documentation only).

- [ ] **Step 1: Write the README**

Create `autograder/README.md`:

```markdown
# ISM2411 / ISM3232 Autograder

Two local CLI programs that fetch student submissions from Canvas, run
deterministic checks against each course's rubric, and post grades back to
Canvas. No LLM/AI is used anywhere in the grading path — criteria the rubric
can't check mechanically are left blank in a review worksheet for you to
fill in by hand.

Design doc: `docs/superpowers/specs/2026-07-27-autograder-design.md`.

## Setup

1. **Install dependencies:**
   ```bash
   cd autograder
   pip install -r requirements.txt
   ```

2. **Get a Canvas API token:** in Canvas, go to Account -> Settings ->
   scroll to "Approved Integrations" -> "+ New Access Token". Copy the token
   immediately (Canvas only shows it once).

3. **Export the token as an environment variable** (never put it in a config
   file or commit it):
   ```bash
   export CANVAS_API_TOKEN="paste-your-token-here"
   ```

4. **Find your course ID:** open the course in Canvas; the URL looks like
   `https://YOUR_INSTITUTION.instructure.com/courses/12345` — `12345` is the
   course ID.

5. **Fill in `ism2411.config.yaml` and `ism3232.config.yaml`** with your real
   `canvas_base_url` and `canvas_course_id`.

## Usage

Per assignment, per course:

```bash
python grade_ism2411.py fetch   --assignment week03_lab
python grade_ism2411.py check   --assignment week03_lab
# Opens runs/week03_lab/review.csv in a spreadsheet app - fill in the blank
# human_* columns (each has a "prompt" in the assignment's YAML config
# telling you what to judge), save.
python grade_ism2411.py upload  --assignment week03_lab --dry-run
# Review the current -> new grade for every student, confirm nothing looks wrong.
python grade_ism2411.py upload  --assignment week03_lab
# Type 'y' to confirm. Posts grades + comments to Canvas, writes a local
# audit log to runs/week03_lab/upload_log_<timestamp>.json.
```

Same for `grade_ism3232.py`, using assignment keys from
`assignments/ism3232/`.

## Adding a new assignment

Copy an existing YAML file in `assignments/ism2411/` or
`assignments/ism3232/` as a template — the field names are the same across
every assignment (`submission_type`, `expected_files`, `run`,
`mechanical_checks`, `scoring_type`, `rubric`). See
`docs/superpowers/specs/2026-07-27-autograder-design.md` for the full config
schema and what each `mechanical_checks` value does.

Currently configured (pilot set):
- ISM2411: `week03_lab`, `capstone`
- ISM3232: `week07_assignment`, `developer_workflow`, `capstone`

The remaining labs/weekly assignments for both courses follow the same
template and can be added the same way.

## Running the test suite

```bash
cd autograder
pytest -v
```

No test hits the real Canvas API — everything is mocked. Before trusting
`upload` against a real assignment, run `fetch` and `check` (with
`upload --dry-run`) against one real, low-stakes assignment first.
```

- [ ] **Step 2: Commit**

```bash
cd /Users/markumreed/Documents/ism_courses
git add autograder/README.md
git commit -m "Add autograder setup and usage README"
```

---

## Final Verification

- [ ] Run the full test suite one more time from a clean checkout state:

```bash
cd /Users/markumreed/Documents/ism_courses/autograder
pip install -r requirements.txt
pytest -v
```

Expected: every test across `test_config.py`, `test_canvas.py`,
`test_checks.py`, `test_fetch.py`, `test_worksheet.py`, `test_scoring.py`,
and `test_cli.py` passes, with zero real network or Canvas calls made.

- [ ] Confirm both entrypoints show usage:

```bash
python3 grade_ism2411.py --help
python3 grade_ism3232.py --help
```

- [ ] Confirm all 5 pilot assignment configs load without error (command from
Tasks 10-11, repeated together):

```bash
python3 -c "
from autograder_common.config import load_assignment_config
for path in [
    'assignments/ism2411/week03_lab.yaml',
    'assignments/ism2411/capstone.yaml',
    'assignments/ism3232/week07_assignment.yaml',
    'assignments/ism3232/developer_workflow.yaml',
    'assignments/ism3232/capstone.yaml',
]:
    load_assignment_config(path)
print('all configs valid')
"
```
