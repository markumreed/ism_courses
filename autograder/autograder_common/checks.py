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
