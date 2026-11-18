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


def test_lecture_timings_follow_the_spec():
    import week16_lecture

    page = week16_lecture.build()[0]
    for minutes in [
        "0&ndash;8",
        "8&ndash;22",
        "22&ndash;35",
        "35&ndash;48",
        "48&ndash;62",
    ]:
        assert f"<td>{minutes}</td>" in page
    assert "<td>62&ndash;75</td>" in page


def test_lecture_names_the_four_misconceptions():
    import week16_lecture

    page = week16_lecture.build()[0]
    for phrase in [
        "passed once",
        "higher pass count",
        "should be in pytest",
        "admitting failure",
    ]:
        assert phrase in page


def test_slides_weak_output_is_real():
    import week16_slides

    page = week16_slides.build()[0]
    shown = html.escape(f"{w.WEAK_MARK}\n{w.weak_check_pytest()}", quote=False)
    assert shown in page


@cache
def lab_page():
    import week16_lab

    return week16_lab.build()[0]


def lab_part(number):
    """The lab page from Part number's divider to the next part's."""
    page = lab_page()
    start = page.index(f"Part {number} &mdash;")
    end = page.find(f"Part {number + 1} &mdash;", start)
    return page[start:] if end == -1 else page[start:end]


def test_lab_parts_come_in_order_with_the_time_bar():
    page = lab_page()
    starts = [page.index(f"Part {n} &mdash;") for n in range(1, 10)]
    assert starts == sorted(starts)
    bar = page[page.index('<div class="time-bar">') :]
    bar = bar[: bar.index("</div>")]
    assert bar.count('<span class="time-block">') == 9


def test_lab_shows_the_three_files_from_the_checkpoint():
    from verify_week13 import BLOCK, plain

    blocks = {plain(label): plain(code) for label, code in BLOCK.findall(lab_page())}
    for name in ("cases.py", "tests/test_cases.py", "evaluation.py"):
        assert blocks[name].rstrip() == w.app_file(name).rstrip()


def test_part_3_states_the_test_rule():
    part = lab_part(3)
    assert "at least three" in part
    assert "every <code>says</code> or <code>never_says</code> case" in part


def test_the_thumbnail_line_is_the_one_line_everywhere():
    for page in built_pages():
        if "img.youtube.com" in page:
            assert html.escape(w.THUMBNAIL, quote=False) in page
    part = lab_part(9)
    assert "both <code>VIDEO_ID</code>s" in part
    assert "?si=" in part


def test_part_9_has_the_shot_list_and_the_private_window_check():
    part = lab_part(9)
    positions = [
        part.index(shot[1:]) for shot in w.SHOTS
    ]  # first letter may be a capital
    assert positions == sorted(positions)
    for phrase in ("Unlisted", "private window", "8 minutes"):
        assert phrase in part


def test_submission_box_is_the_capstone():
    page = lab_page()
    box = page[page.index('<div class="submit-box">') :]
    for phrase in ("Capstone", "GitHub", "tests/test_cases.py", w.COMMIT):
        assert phrase in box


def test_lab_slide_blocks_are_static():
    import week16_lab_slides

    page = week16_lab_slides.build()[0]
    assert 'data-lang="python"' not in page
    assert 'class="run"' in page
