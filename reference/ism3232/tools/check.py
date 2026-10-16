"""Run the ISM3232 lab ritual on one folder the way the autograder sees it.

Usage: python reference/ism3232/tools/check.py <folder>

The folder is copied to a temporary directory first, so no config file in
this repo changes the result and nothing is written into the folder. Then:
ruff format --check, ruff check (both with ruff's default rules), and
pytest with the ollama and streamlit packages blocked, so a test that
needs either one fails here just as it would in the autograder.
Run it with a Python that has ruff and pytest installed.
"""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

BLOCKED_PYTEST = (
    "import sys; sys.modules['ollama'] = None; sys.modules['streamlit'] = None; "
    "import pytest; sys.exit(pytest.main(['-q', '-p', 'no:cacheprovider']))"
)
SKIP = shutil.ignore_patterns(".venv", "__pycache__", ".ruff_cache", ".pytest_cache")


def check(folder):
    """Return 0 if the folder passes every step, otherwise the failing exit code."""
    with tempfile.TemporaryDirectory() as temp:
        copy = Path(temp) / Path(folder).name
        shutil.copytree(folder, copy, ignore=SKIP)
        steps = [
            [sys.executable, "-m", "ruff", "format", "--isolated", "--check", "."],
            [sys.executable, "-m", "ruff", "check", "--isolated", "--no-cache", "."],
            [sys.executable, "-B", "-c", BLOCKED_PYTEST],
        ]
        for step in steps:
            result = subprocess.run(
                step, cwd=copy, capture_output=True, text=True, check=False
            )
            print(result.stdout + result.stderr)
            if result.returncode != 0:
                return result.returncode
    return 0


if __name__ == "__main__":
    sys.exit(check(sys.argv[1]))
