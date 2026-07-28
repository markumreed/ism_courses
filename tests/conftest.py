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
