"""Tests for the saved Week 14 model runs. Run from this folder: python -m pytest -q"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import week14_common as w


def test_the_first_run_rejects_and_keeps_the_old_address():
    first = w.run_text("main_first_run.txt")
    assert "Request 1: A102 to 9 Pine Street, Tampa" in first
    assert "Request 1 rejected." in first
    assert "A102 88 Pier Street" in first


def test_the_second_run_finds_the_decision_still_in_the_database():
    second = w.run_text("main_second_run.txt")
    reply = next(line for line in second.split("\n") if "Sunny:" in line)
    assert "reject" in reply.lower()
    assert "Request 1:" not in second
