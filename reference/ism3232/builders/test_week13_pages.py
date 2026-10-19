"""Checks on what the built Week 13 and capstone pages tell students, for the
mistakes the Phase 3 final review found. Run from this folder: python -m pytest -q"""

import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import capstone_rubric
import week13_lab
import week13_lecture
import week13_reading
from pagekit import NO_SCREENSHOTS, ROOT
from week13_common import FULL_REV


def bayside_files():
    """File names in the Bayside app at the commit the rubric describes."""
    listed = subprocess.run(
        [
            "git",
            "ls-tree",
            "-r",
            "--name-only",
            FULL_REV,
            "reference/ism3232/bayside_app",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.split()
    return {Path(name).name for name in listed}


def test_week13_never_says_it_is_graded_by_running_pytest():
    for module in (week13_lab, week13_lecture):
        page, _ = module.build()
        assert NO_SCREENSHOTS not in page, module.__name__


def test_the_lab_says_how_to_get_signed_off_after_class():
    page, _ = week13_lab.build()
    assert "after class" in page


def test_the_exercise_2_key_does_not_teach_a_false_reason():
    page, _ = week13_lab.build()
    assert "compares a number with text" not in page


def test_pages_with_sqlite3_tables_say_a_mac_may_space_columns_differently():
    for module in (week13_reading, week13_lecture, week13_lab):
        page, _ = module.build()
        assert re.search(r"Mac[^.]*spac", page), module.__name__


def test_rubric_examples_name_only_real_bayside_files():
    files = bayside_files()
    for part in capstone_rubric.PARTS:
        example = part["example"]
        for name in re.findall(r"<code>([\w.]+\.py)</code>", example):
            assert name in files, (part["key"], name)
        if re.search(r"\b(its|Bayside(?:'|&rsquo;)s) README", example):
            assert "README.md" in files, (part["key"], "README.md")


def test_a_keyword_model_demo_with_a_readme_note_scores_above_some():
    live = next(part for part in capstone_rubric.PARTS if part["key"] == "live_demo")
    assert "no README note" in live["some"]
    rules = capstone_rubric.demo_section()
    assert "scores Some" not in rules
    assert "Most" in rules
