"""Tests for week13_proposal.py. Run from this folder: python -m pytest -q"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import week13_proposal as p
from week13_starters import TEMPLATE, headings

TEXT = p.bayside_proposal()


def test_headings_follow_the_template_in_order():
    assert headings(TEXT) == headings(TEMPLATE)


def test_every_tool_the_app_offers_is_listed():
    for name in [
        "look_up_order",
        "check_stock",
        "check_request",
        "request_address_change",
    ]:
        assert f"\n{name}(" in TEXT


def test_the_instructions_are_copied_exactly():
    assert p.literal("settings.py", "INSTRUCTIONS") in TEXT


def test_five_conversations_and_two_are_safety_cases():
    conversations = re.findall(r"^\d\. Customer: .*$", TEXT, re.MULTILINE)
    assert len(conversations) == 5
    assert sum("(safety:" in line for line in conversations) == 2


def test_change_requests_has_no_sample_row():
    after = TEXT.split("\nchange_requests: ")[1].split("\n")[1]
    assert "no sample rows" in after


def test_the_approval_column_comes_from_approve_request():
    assert p.approval_target() == "orders.address"


def test_bayside_numbers_come_from_the_saved_run():
    assert p.evaluation_result(7) == "0 of 3"
    assert p.evaluation_total() == "19 of 24"
    assert p.case_count() == 8


def test_section_returns_one_section():
    tables = p.section(TEXT, "Tables")
    assert tables.startswith("## Tables")
    assert "## Lookup tools" not in tables
