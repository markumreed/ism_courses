"""Tests for week13_starters.py. Run from this folder: python -m pytest -q"""

import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import week13_starters as s

MONEY = {"price"}
COUNTS = {"stock", "spots_left", "minutes"}


def schema(starter):
    """CREATE TABLE and INSERT OR IGNORE statements for one starter, the way a
    student's schema.sql would write them, plus an empty change_requests."""
    statements = []
    for table in starter["tables"]:
        columns = ", ".join(f"{name} {kind}" for name, kind in table["columns"])
        statements.append(
            (f"CREATE TABLE IF NOT EXISTS {table['name']} ({columns})", ())
        )
        marks = ", ".join("?" for _ in table["columns"])
        for row in table["rows"]:
            statements.append(
                (f"INSERT OR IGNORE INTO {table['name']} VALUES ({marks})", row)
            )
    record = starter["change"][1][0]
    statements.append(
        (
            (
                "CREATE TABLE IF NOT EXISTS change_requests (number INTEGER PRIMARY KEY "
                f"AUTOINCREMENT, {record} TEXT NOT NULL, new_value TEXT NOT NULL, "
                "status TEXT NOT NULL DEFAULT 'waiting')"
            ),
            (),
        )
    )
    return statements


def table(starter, name):
    return next(t for t in starter["tables"] if t["name"] == name)


def test_six_starters_with_two_tables_of_two_rows():
    assert len(s.STARTERS) == 6
    for starter in s.STARTERS:
        assert len(starter["tables"]) == 2, starter["name"]
        for t in starter["tables"]:
            assert len(t["rows"]) == 2, t["name"]
            assert all(len(row) == len(t["columns"]) for row in t["rows"]), t["name"]


def test_the_first_column_is_the_primary_key():
    for starter in s.STARTERS:
        for t in starter["tables"]:
            assert t["columns"][0][1] == "TEXT PRIMARY KEY", t["name"]


def test_money_is_real_and_counts_are_integers():
    for starter in s.STARTERS:
        for t in starter["tables"]:
            for name, kind in t["columns"]:
                if name in MONEY:
                    assert kind == "REAL", (t["name"], name)
                if name in COUNTS:
                    assert kind == "INTEGER", (t["name"], name)


def test_reading_the_schema_twice_changes_nothing():
    for starter in s.STARTERS:
        conn = sqlite3.connect(":memory:")
        for _ in range(2):
            for sql, values in schema(starter):
                conn.execute(sql, values)
        for t in starter["tables"]:
            count = conn.execute(f"SELECT COUNT(*) FROM {t['name']}").fetchone()[0]
            assert count == 2, (starter["name"], t["name"])
        assert conn.execute("SELECT COUNT(*) FROM change_requests").fetchone()[0] == 0
        conn.close()


def test_lookup_arguments_name_columns():
    for starter in s.STARTERS:
        for tool, arguments, table_name, _ in starter["lookups"]:
            columns = [name for name, _ in table(starter, table_name)["columns"]]
            assert all(arg in columns for arg in arguments), tool


def test_the_change_names_its_record_and_the_column_it_changes():
    for starter in s.STARTERS:
        tool, arguments, table_name, column, _ = starter["change"]
        columns = [name for name, _ in table(starter, table_name)["columns"]]
        assert arguments[0] == columns[0], tool
        assert column in columns, tool


def test_example_questions_use_the_sample_rows():
    for starter in s.STARTERS:
        examples = [(t, q) for _, _, t, q in starter["lookups"]]
        examples.append((starter["change"][2], starter["change"][4]))
        for table_name, question in examples:
            values = [
                str(v).lower()
                for row in table(starter, table_name)["rows"]
                for v in row
            ]
            assert any(v in question.lower() for v in values), question


def test_example_questions_do_not_trip_the_handoff():
    for starter in s.STARTERS:
        questions = [q for _, _, _, q in starter["lookups"]] + [starter["change"][4]]
        for question in questions:
            for word in starter["handoff"]:
                assert word not in question.lower(), (question, word)


def test_id_letters_belong_to_one_business_each():
    letters = {"A": "Bayside"}
    for starter in s.STARTERS:
        mine = set()
        for t in starter["tables"]:
            if t["columns"][0][0].endswith("_id"):
                mine |= {str(row[0])[0] for row in t["rows"]}
        for letter in mine:
            assert letter not in letters, (starter["name"], letter, letters.get(letter))
            letters[letter] = starter["name"]


def test_the_template_has_the_eleven_sections_in_order():
    assert s.headings(s.TEMPLATE) == [
        "The business",
        "Who uses it",
        "Tables",
        "Lookup tools (at least two)",
        "Change tool (at least one)",
        "Handoff rule",
        "Data it never stores",
        "Instructions draft",
        "Five sample conversations",
        "Out of scope (at least two)",
        "Checklist",
    ]


def test_the_checklist_has_eight_items():
    assert len(s.CHECKLIST) == 8
