"""Tests for verify_week13.py. Run from this folder: python -m pytest -q"""

import sys
from pathlib import Path

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
    assert v.expected_misses(page, "name  stock\nday pack  45.0") == ["day pack  0"]


def test_a_real_expected_box_passes():
    page = '<div class="expected" style="white-space:pre-wrap;">A101  processing</div>'
    assert v.expected_misses(page, "sqlite> x\nA101  processing\n") == []


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
