"""Checks on the capstone rubric page after Week 16: the demo is a video, and the
Bayside example quotes the Week 16 run. Run from this folder: python -m pytest -q"""

import sys
from functools import cache
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).parent))

import capstone_rubric as r
import week16_common as w
from pagekit import ROOT

CONFIG = ROOT / "autograder" / "assignments" / "ism3232" / "capstone.yaml"


@cache
def page():
    return r.build()[0]


def part(key):
    return next(p for p in r.PARTS if p["key"] == key)


def test_the_rubric_quotes_the_week16_run():
    assert w.evaluation_total() in page()
    assert w.evaluation_result("price match") in page()
    assert w.evaluation_result("false closing time") in page()


def test_part_8_is_the_demo_video():
    demo = part("live_demo")
    assert demo["title"] == "Demo video"
    for phrase in ("Unlisted", "face and screen", "README"):
        assert phrase in demo["full"]
    assert "cannot be watched" in demo["missing"]


def test_part_6_names_test_cases():
    full = part("evaluation_safety")["full"]
    assert "tests/test_cases.py" in full and "cases.py" in full


def test_no_live_demo_left():
    assert "Live demo" not in page() and "live demo" not in page()


def test_keys_and_points_match_capstone_yaml():
    rubric = yaml.safe_load(CONFIG.read_text())["rubric"]
    assert [p["key"] for p in r.PARTS] == list(rubric)
    assert all(rubric[p["key"]]["points"] == p["points"] for p in r.PARTS)


def test_capstone_yaml_expects_cases_py_and_names_the_video():
    config = yaml.safe_load(CONFIG.read_text())
    assert "cases.py" in config["expected_files"]
    assert config["rubric"]["live_demo"]["prompt"].startswith("Demo video (Week 16)")
