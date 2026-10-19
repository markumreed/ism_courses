"""Tests for verify_week13.py. Run from this folder: python -m pytest -q"""

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))

import verify_week13 as v
from pagekit import quiz_mc, quiz_tf

ANSWER = "SELECT name, price FROM products WHERE stock = 0;"


def test_an_answer_inside_a_key_is_fine_on_the_lab():
    page = (
        f"<p>Try it.</p><details><summary>Answer</summary><pre>{ANSWER}</pre></details>"
    )
    assert v.answer_leaks("week13_lab", page, [ANSWER]) == []


def test_an_answer_outside_a_key_is_a_leak_on_the_lab():
    assert v.answer_leaks("week13_lab", f"<pre>{ANSWER}</pre>", [ANSWER]) == [ANSWER]


def test_an_answer_anywhere_on_the_reading_is_a_leak():
    page = f"<details><pre>{ANSWER}</pre></details>"
    assert v.answer_leaks("week13_reading", page, [ANSWER]) == [ANSWER]


def test_the_lab_slides_may_show_answers():
    assert v.answer_leaks("week13_lab_slides", f"<pre>{ANSWER}</pre>", [ANSWER]) == []


def test_an_expected_box_must_be_real_output():
    page = '<div class="expected" style="white-space:pre-wrap;">day pack  0</div>'
    assert v.expected_misses(page, ["name  stock\nday pack  45.0"]) == ["day pack  0"]


def test_a_real_expected_box_passes():
    page = '<div class="expected" style="white-space:pre-wrap;">A101  processing</div>'
    assert v.expected_misses(page, ["A101  processing   "]) == []


def test_a_box_holding_only_part_of_an_output_is_not_enough():
    page = '<div class="expected" style="white-space:pre-wrap;">2</div>'
    assert v.expected_misses(page, ["delivered   2\nprocessing  3"]) == ["2"]


def test_a_box_with_more_classes_is_still_checked():
    page = '<div class="expected big">made up</div>'
    assert v.expected_misses(page, ["A101  processing"]) == ["made up"]


def test_saved_outputs_are_whole_parts_with_and_without_typed_lines():
    outputs = v.saved_outputs()
    assert v.w.chunk("lab", "ex1") in outputs
    assert v.w.output_of("lab", "ex1") in outputs
    assert v.w.run_text("version") in outputs
    assert "2" not in outputs


def quiz_page(tmp_path, items):
    path = tmp_path / "page.html"
    path.write_text("<html><body>" + "\n".join(items) + "</body></html>")
    return path


def good_items():
    return [quiz_tf(n, "A statement.", True, "why") for n in range(1, 11)]


def test_ten_good_items_have_no_problems(tmp_path):
    assert v.quiz_problems(quiz_page(tmp_path, good_items())) == []


def test_the_quiz_needs_ten_items(tmp_path):
    assert v.quiz_problems(quiz_page(tmp_path, good_items()[:9])) == [
        "9 quiz items, expected 10"
    ]


def test_a_multiple_choice_answer_must_match_an_option(tmp_path):
    item = quiz_mc(1, "Which type?", ["REAL", "TEXT", "INTEGER", "BLOB"], 0, "why")
    broken = item.replace("REAL <span", "NUMERIC <span")
    problems = v.quiz_problems(quiz_page(tmp_path, [broken, *good_items()[1:]]))
    assert problems == ["Q1: the answer matches no option"]


CONFIG = {"rubric": {"proposal": {"points": 10}, "rest": {"points": 90}}}


def part(key, points, tiers):
    return {"key": key, "points": points, "tiers": tiers}


def test_parts_that_match_the_config_pass():
    parts = [part("proposal", 10, (10, 7, 4, 0)), part("rest", 90, (90, 63, 36, 0))]
    assert v.rubric_problems(parts, CONFIG) == []


def test_points_must_match_the_config():
    parts = [part("proposal", 15, (15, 10, 6, 0)), part("rest", 90, (90, 63, 36, 0))]
    assert "proposal: 15 points, capstone.yaml says 10" in v.rubric_problems(
        parts, CONFIG
    )


def test_tiers_must_follow_100_70_40_0():
    parts = [part("proposal", 10, (10, 8, 4, 0)), part("rest", 90, (90, 63, 36, 0))]
    assert v.rubric_problems(parts, CONFIG) == [
        "proposal: tiers (10, 8, 4, 0) do not follow 100/70/40/0"
    ]


needs_cli = pytest.mark.skipif(
    not os.environ.get("SQLITE3_CLI"), reason="set SQLITE3_CLI"
)


def sqlite_block(text):
    return f'<div class="code-label">sqlite3</div><pre><code>{text}</code></pre>'


def terminal_block(text):
    return f'<div class="code-label">Terminal</div><pre><code>{text}</code></pre>'


@needs_cli
def test_blocks_that_follow_on_in_one_database_pass():
    page = sqlite_block("sqlite&gt; SELECT 1;\n1") + sqlite_block(
        "sqlite&gt; SELECT 2;\n2"
    )
    assert v.follow_along_problems(page, os.environ["SQLITE3_CLI"]) == []


@needs_cli
def test_a_block_whose_output_needs_a_fresh_database_is_reported():
    page = sqlite_block(
        "sqlite&gt; CREATE TABLE t (a);\nsqlite&gt; INSERT INTO t VALUES (1);"
    ) + sqlite_block(
        "sqlite&gt; INSERT INTO t VALUES (2);\nsqlite&gt; SELECT COUNT(*) FROM t;\n1"
    )
    assert len(v.follow_along_problems(page, os.environ["SQLITE3_CLI"])) == 1


@needs_cli
def test_the_copy_keeps_the_rows_but_starts_a_new_session():
    setup = sqlite_block(
        "sqlite&gt; .mode column\nsqlite&gt; .headers on\n"
        "sqlite&gt; CREATE TABLE t (a);\nsqlite&gt; INSERT INTO t VALUES (7);"
    )
    copy = terminal_block("cp bayside.db practice_copy.db\nsqlite3 practice_copy.db")
    list_mode = sqlite_block("sqlite&gt; SELECT a FROM t;\n7")
    column_mode = sqlite_block("sqlite&gt; SELECT a FROM t;\na\n-\n7")
    cli = os.environ["SQLITE3_CLI"]
    assert v.follow_along_problems(setup + copy + list_mode, cli) == []
    assert len(v.follow_along_problems(setup + copy + column_mode, cli)) == 1
