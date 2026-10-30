"""Tests for the saved Week 15 browser session. Run from this folder: python -m pytest -q"""

import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import week15_common as w


def test_the_request_waits_with_the_customers_address():
    assert (
        w.session_steps()["staff waiting"] == "Request 1: A102 to 9 Pine Street, Tampa"
    )


def test_approve_shows_the_notice_and_changes_the_order():
    steps = w.session_steps()
    assert steps["staff approved"] == "Request 1 approved."
    assert "A102 delivered 9 Pine Street, Tampa" in steps["orders"].split("\n")


def test_the_last_answer_reports_the_approval():
    last = w.session_steps()["chat after approval"].split("\n")[-1]
    assert last.startswith("Sunny: ") and "approved" in last.lower()


def test_a_refresh_clears_the_chat():
    assert w.session_steps()["after a refresh"] == "chat messages: 0"


def test_the_images_are_the_ones_this_session_took():
    for line in w.session_steps()["images"].split("\n"):
        name, digest = line.split()
        data = (w.IMAGES / name).read_bytes()
        assert hashlib.sha256(data).hexdigest() == digest
        assert data[16:24] == (2400).to_bytes(4, "big") + (2000).to_bytes(4, "big")
