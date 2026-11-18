"""Checks on what the built Week 16 pages tell students.
Run from this folder: python -m pytest -q"""

import html
import re
import sys
from functools import cache
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import week16_common as w
import week16_reading

OLD_COURSE = ["Anthropic", "ai_feature", "GenAI", "ANTHROPIC_API_KEY", "models.py"]


@cache
def reading_page():
    return week16_reading.build()[0]


def built_pages():
    """Every Week 16 page whose builder exists so far."""
    pages = [reading_page()]
    for name in ("week16_lecture", "week16_slides", "week16_lab", "week16_lab_slides"):
        try:
            module = __import__(name)
        except ModuleNotFoundError:
            continue
        pages.append(module.build()[0])
    return pages


def section(page, heading):
    """The page from the <h2> that starts with heading to the next <h2>."""
    start = page.index(f"<h2>{heading}")
    end = page.find("<h2", start + 4)
    return page[start:] if end == -1 else page[start:end]


def test_reading_lists_eight_outcomes():
    outcomes = section(reading_page(), "Module at a glance")
    listed = outcomes[outcomes.index("<ol>") : outcomes.index("</ol>")]
    assert listed.count("<li>") == 8


def test_reading_shows_the_saved_table():
    table = (w.RUNS / "evaluation.txt").read_text().rstrip()
    assert html.escape(table, quote=False) in reading_page()


def test_reading_explains_every_failing_case():
    running = section(reading_page(), "Running it")
    failing = [name for name, result in w.evaluation_rows().items() if result != "3/3"]
    assert failing
    for name in failing:
        assert name in running
        assert w.evaluation_result(name) in running


def test_reading_safety_table_has_six_tries():
    checklist = section(reading_page(), "The safety checklist")
    body = checklist[checklist.index("<tbody>") : checklist.index("</tbody>")]
    assert body.count("<tr>") == 6


def test_reading_has_ten_quiz_items():
    assert reading_page().count('<div class="quiz-item">') == 10


def test_week16_pages_leave_the_old_course_behind():
    for page in built_pages():
        for word in OLD_COURSE:
            assert word not in page, word


def test_reading_quiz_answers_are_spread():
    letters = set()
    for item in reading_page().split('<div class="quiz-item">')[1:]:
        if "Multiple Choice" not in item:
            continue
        options = re.findall(r"<li>([abcd])\) (.*?)</li>", item)
        answer = re.search(r'<div style="margin-top:8px;">(.*?) <span', item).group(1)
        letters |= {letter for letter, text in options if text == answer}
    assert len(letters) >= 3
