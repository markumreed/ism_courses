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
