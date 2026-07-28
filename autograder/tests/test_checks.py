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
