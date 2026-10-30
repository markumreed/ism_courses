"""Checks on what the built Week 15 lab and lab slides tell students.
Run from this folder: python -m pytest -q"""

import html
import re
import sys
from functools import cache
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import week15_lab
import week15_lab_slides


@cache
def lab_page():
    return week15_lab.build()[0]


@cache
def slides_page():
    return week15_lab_slides.build()[0]


def lab_part(number):
    """The lab page from Part number's divider to the next part's."""
    page = lab_page()
    start = page.index(f"Part {number} &mdash;")
    end = page.find(f"Part {number + 1} &mdash;", start)
    return page[start:] if end == -1 else page[start:end]


def test_part_4_names_the_three_tests():
    part = lab_part(4)
    assert "test_status_report_counts_orders" in part and "test_restock" in part
    assert "leaves the other rows alone" in part


def test_part_7_shows_keyword_users_how_to_file_a_request():
    part = lab_part(7)
    assert "add_change_request" in part and "refresh" in part.lower()


def test_no_lab_slide_with_a_run_button_uses_streamlit():
    runnable = re.findall(
        r'<div class="run" data-lang="python"[^>]*>(.*?)</div>',
        slides_page(),
        re.DOTALL,
    )
    assert [
        code[:40] for code in runnable if re.search(r"\bst\.|streamlit", code)
    ] == []


def test_the_lab_slide_quiz_has_exactly_one_right_answer():
    answer, body = re.search(
        r'<div class="quiz" data-answer="(\w)">(.*?)</div>', slides_page(), re.DOTALL
    ).groups()
    options = re.findall(r'<button data-opt="(\w)">(.*?)</button>', body)
    right = [
        letter for letter, text in options if "session_state" in html.unescape(text)
    ]
    assert right == [answer]
