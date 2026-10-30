"""Checks on what the built Week 15 lab and lab slides tell students.
Run from this folder: python -m pytest -q"""

import html
import re
import sys
from collections import Counter
from functools import cache
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import week15_lab
import week15_lab_slides
import week15_reading


@cache
def lab_page():
    return week15_lab.build()[0]


@cache
def slides_page():
    return week15_lab_slides.build()[0]


@cache
def reading_page():
    return week15_reading.build()[0]


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


def test_part_6_shows_how_to_edit_text_and_prices():
    part = lab_part(6)
    assert "st.text_input" in part and "step=0.01" in part
    assert "no new value" in part


def test_part_6_ends_with_running_the_staff_tab_and_saving_the_form():
    part = lab_part(6)
    assert "streamlit run app.py" in part and "Nothing is waiting." in part


def test_part_7_keyword_path_starts_in_the_project_folder():
    part = lab_part(7)
    assert part.index("cd ~/ism3232/module07_final_project") < part.index(
        "add_change_request"
    )


def test_no_rerun_step_clicks_a_button_or_presses_r():
    for page in (lab_part(7), slides_page()):
        assert "click any button" not in page and "press R" not in page


def test_the_reading_explains_the_dollar_escape_and_step_correctly():
    page = reading_page()
    assert "$60.00 would come out garbled" not in page
    assert "two prices, like $5 and $6" in page
    assert "stop the number going below zero" not in page
    assert "<code>step=1</code> makes it count in whole numbers" in page


def test_the_quiz_answers_are_spread_over_the_options():
    letters = []
    for item in reading_page().split('<div class="quiz-item">')[1:]:
        if "Multiple Choice" not in item:
            continue
        options = re.findall(r"<li>(\w)\) (.*?)</li>", item)
        answer = re.search(r'margin-top:8px;">(.*?) <span', item).group(1)
        letters += [letter for letter, text in options if text == answer]
    assert len(letters) == 5
    assert max(Counter(letters).values()) <= 2
