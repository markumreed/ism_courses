"""Tests for sqlite_cli.py. Run from this folder: python -m pytest -q

The transcript tests need the checked sqlite3: set SQLITE3_CLI to the path
`python sqlite_cli.py DIR` prints."""

import hashlib
import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))

import sqlite_cli

needs_cli = pytest.mark.skipif(
    not os.environ.get("SQLITE3_CLI"), reason="set SQLITE3_CLI"
)


def test_verify_accepts_the_right_hash(tmp_path):
    package = tmp_path / "x.deb"
    package.write_bytes(b"abc")
    sqlite_cli.verify_sha256(package, hashlib.sha256(b"abc").hexdigest())


def test_verify_refuses_a_wrong_hash(tmp_path):
    package = tmp_path / "x.deb"
    package.write_bytes(b"abc")
    with pytest.raises(ValueError):
        sqlite_cli.verify_sha256(package, "0" * 64)


@needs_cli
def test_the_checked_cli_is_the_version_students_install():
    assert sqlite_cli.check_version(os.environ["SQLITE3_CLI"]).startswith("3.45.1 ")


@needs_cli
def test_each_typed_line_follows_the_prompt(tmp_path):
    out = sqlite_cli.transcript(os.environ["SQLITE3_CLI"], tmp_path, ["SELECT 1 + 1;"])
    assert out.split("\n")[-2:] == ["sqlite> SELECT 1 + 1;", "2"]


@needs_cli
def test_the_banner_comes_first_and_the_last_empty_prompt_is_dropped(tmp_path):
    out = sqlite_cli.transcript(os.environ["SQLITE3_CLI"], tmp_path, ["SELECT 1;"])
    assert out.startswith("SQLite version 3.45.1 ")
    assert not out.endswith("sqlite> ")


@needs_cli
def test_an_error_appears_where_it_happened(tmp_path):
    lines = ["SELECT * FROM nope;", "SELECT 2;"]
    out = sqlite_cli.transcript(os.environ["SQLITE3_CLI"], tmp_path, lines).split("\n")
    assert out.index("Parse error: no such table: nope") < out.index(
        "sqlite> SELECT 2;"
    )
