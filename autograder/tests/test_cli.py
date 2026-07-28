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
