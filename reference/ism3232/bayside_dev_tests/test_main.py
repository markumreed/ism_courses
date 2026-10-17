"""The staff review at the end of bayside_app/main.py (reference only)."""

import shutil
import sqlite3
import subprocess
import sys
from pathlib import Path

APP = Path(__file__).resolve().parents[1] / "bayside_app"


def run_main(tmp_path, typed):
    """Copy the app, file one waiting request, run main.py with the typed lines."""
    for path in APP.glob("*.py"):
        shutil.copy(path, tmp_path)
    shutil.copy(APP / "schema.sql", tmp_path)
    conn = sqlite3.connect(tmp_path / "bayside.db")
    conn.executescript((tmp_path / "schema.sql").read_text())
    sql = "INSERT INTO change_requests (order_id, new_address) VALUES ('A102', '9 Pine St')"
    conn.execute(sql)
    conn.commit()
    conn.close()
    result = subprocess.run(
        [sys.executable, "-B", "main.py"],
        cwd=tmp_path,
        input=typed,
        capture_output=True,
        text=True,
        check=True,
        timeout=60,
    )
    return result.stdout


def request_status(tmp_path):
    conn = sqlite3.connect(tmp_path / "bayside.db")
    row = conn.execute("SELECT status FROM change_requests WHERE number = 1").fetchone()
    conn.close()
    return row[0]


def test_an_unclear_answer_leaves_the_request_waiting(tmp_path):
    output = run_main(tmp_path, "quit\nYes\n")
    assert "Request 1 is still waiting." in output
    assert request_status(tmp_path) == "waiting"


def test_no_rejects_and_yes_approves(tmp_path):
    run_main(tmp_path, "quit\nno\n")
    assert request_status(tmp_path) == "rejected"
