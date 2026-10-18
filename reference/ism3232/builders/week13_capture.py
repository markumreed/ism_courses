"""Save every Week 13 sqlite3 session, and the version line, to runs/week13/.

SQLITE3_CLI=<checked sqlite3> python reference/ism3232/builders/week13_capture.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import week13_common as w
from sqlite_cli import check_version, cli_from_env


def main():
    cli = cli_from_env()
    w.RUNS.mkdir(exist_ok=True)
    (w.RUNS / "version.txt").write_text(check_version(cli) + "\n")
    for name in w.SESSIONS:
        (w.RUNS / f"{name}.txt").write_text(w.run_session(cli, name) + "\n")
        print("saved", name)


if __name__ == "__main__":
    main()
