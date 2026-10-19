"""Tests for week13_common.py. Run from this folder: python -m pytest -q"""

import os
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))

import week13_common as w

TEXT = """SQLite version 3.45.1 2024-01-30 16:01:20
Enter ".help" for usage hints.
sqlite> SELECT 1;
1
sqlite> SELECT 1;
1
sqlite> SELECT 2;
2"""
PARTS = [("first", ["SELECT 1;"]), ("again", ["SELECT 1;"]), ("last", ["SELECT 2;"])]


def test_each_part_starts_where_its_first_line_was_typed():
    pieces = w.split(TEXT, PARTS)
    assert pieces == {
        "first": "sqlite> SELECT 1;\n1",
        "again": "sqlite> SELECT 1;\n1",
        "last": "sqlite> SELECT 2;\n2",
    }


def test_the_banner_is_in_no_part():
    assert all("SQLite version" not in piece for piece in w.split(TEXT, PARTS).values())


def test_every_session_starts_by_reading_a_schema_file():
    for name, parts in w.SESSIONS.items():
        assert parts[0][1][0].startswith(".read "), name


def test_answers_are_typed_only_in_the_lab_session():
    for name in w.SESSIONS:
        if name != "lab":
            assert not set(w.ANSWERS) & set(w.session_lines(name)), name


def test_the_gitignore_line_writes_three_entries(tmp_path):
    subprocess.run(["bash", "-c", w.GITIGNORE_LINE], cwd=tmp_path, check=True)
    assert (tmp_path / ".gitignore").read_text() == ".venv/\n__pycache__/\n*.db\n"


def test_saved_version_is_the_one_students_install():
    assert w.run_text("version").startswith("3.45.1 ")


def test_every_part_is_in_its_saved_transcript():
    for name, parts in w.SESSIONS.items():
        assert set(w.split(w.run_text(name), parts)) == {p for p, _ in parts}, name


def test_output_of_drops_the_typed_lines():
    assert "sqlite> " not in w.output_of("lab", "ex1")
    assert "A101" in w.output_of("lab", "ex1")


@pytest.mark.skipif(not os.environ.get("SQLITE3_CLI"), reason="set SQLITE3_CLI")
def test_saved_sessions_match_a_fresh_run():
    for name in w.SESSIONS:
        assert w.run_session(os.environ["SQLITE3_CLI"], name) == w.run_text(name), name


def test_slide_code_can_mark_sql():
    from pagekit import slide_code

    assert 'class="language-sql"' in slide_code("t", "SELECT 1;", "n", lang="sql")
    assert 'class="language-python"' in slide_code("t", "x = 1", "n")


def test_a_plain_insert_schema_errors_on_the_second_read_but_counts_match():
    first = w.output_of("plain_twice", "first")
    again = w.output_of("plain_twice", "again")
    assert "UNIQUE constraint failed" not in first
    assert "UNIQUE constraint failed" in again
    assert first.split("\n")[-1] == again.split("\n")[-1]
