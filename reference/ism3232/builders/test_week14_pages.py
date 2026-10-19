"""Checks on what the built Week 14 pages tell students, for the mistakes the
Phase 4a final review found. Run from this folder: python -m pytest -q"""

import html
import re
import sys
from functools import cache
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import week14_lab
import week14_lab_slides


@cache
def lab_page():
    return week14_lab.build()[0]


@cache
def slides_page():
    return week14_lab_slides.build()[0]


def lab_part(number):
    """The lab page from Part number's divider to the next part's."""
    page = lab_page()
    start = page.index(f"Part {number} &mdash;")
    end = page.find(f"Part {number + 1} &mdash;", start)
    return page[start:] if end == -1 else page[start:end]


def test_part_5_asks_for_check_request():
    assert "check_request" in lab_part(5)


def test_part_5_says_lookups_find_the_id_among_the_words():
    assert "whole sentence" in lab_part(5)


def test_part_7_shows_keyword_model_users_how_to_reach_the_staff_review():
    part = lab_part(7)
    assert "lookups only" in part
    assert "add_change_request" in part


def test_the_lab_slide_quiz_has_exactly_one_right_answer():
    answer, body = re.search(
        r'<div class="quiz" data-answer="(\w)">(.*?)</div>', slides_page(), re.DOTALL
    ).groups()
    right = []
    for letter, text in re.findall(r'<button data-opt="(\w)">(.*?)</button>', body):
        value = eval(html.unescape(text), {}, {"order_id": "A100"})
        if isinstance(value, tuple) and len(value) == 1:
            right.append(letter)
    assert right == [answer]


def test_no_lab_slide_with_a_run_button_imports_sqlite3():
    runnable = re.findall(
        r'<div class="run" data-lang="python"[^>]*>(.*?)</div>',
        slides_page(),
        re.DOTALL,
    )
    assert [code[:40] for code in runnable if "import sqlite3" in code] == []
