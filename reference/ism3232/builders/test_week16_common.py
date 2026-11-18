"""Tests for week16_common.py. Run from this folder: python -m pytest -q"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import week16_common as w
from pagekit import REF


def test_the_proposal_cases_match_the_week13_checkpoint_apart_from_names():
    from week13_proposal import CONVERSATIONS

    new = [
        {k: v for k, v in case.items() if k != "name"} for case in w.case_dicts(w.REV)
    ]
    old = w.case_dicts(w.OLD_REV)
    assert [new[i] for i in CONVERSATIONS] == [old[i] for i in CONVERSATIONS]
    changed = [w.CASE_NAMES[i] for i in range(len(old)) if new[i] != old[i]]
    assert changed == ["price match"]
    assert [case["name"] for case in w.case_dicts(w.REV)] == w.CASE_NAMES


def test_the_weak_value_fails_its_test():
    out = w.weak_check_pytest()
    assert (
        "FAILED tests/test_cases.py::test_closing_time_case_fails_other_wordings" in out
    )
    assert out.endswith("1 failed, 3 passed")


def test_the_checkpoint_passes_all_its_tests():
    assert w.checkpoint_pytest() == "43 passed"


def test_evaluation_rows_cover_every_case_and_add_up():
    rows = w.evaluation_rows()
    assert list(rows) == w.CASE_NAMES
    passed = sum(int(r.split("/")[0]) for r in rows.values())
    assert w.evaluation_total() == f"{passed} of 24"


def test_the_readme_table_is_the_saved_run():
    table = (w.RUNS / "evaluation.txt").read_text().rstrip()
    assert table in w.app_file("README.md")


def test_each_safety_try_has_three_runs():
    for key in w.SAFETY_KEYS:
        assert len(w.safety_runs(key)) == 3


def test_the_template_starts_with_the_thumbnail_line():
    assert w.README_TEMPLATE.split("\n")[2] == w.THUMBNAIL
    assert w.THUMBNAIL.count("VIDEO_ID") == 2


def test_bayside_files_have_not_changed_since_the_checkpoint():
    for name in ("cases.py", "evaluation.py", "tests/test_cases.py", "README.md"):
        assert (REF / "bayside_app" / name).read_text() == w.app_file(name)
