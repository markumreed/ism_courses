"""Tests for week15_common.py. Run from this folder: python -m pytest -q"""

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import week15_common as w
from pagekit import REF
from week14_common import build_folder


def test_counter_without_session_state_stays_at_one():
    assert w.counter_after_clicks(w.WARMUP["counter.py"], 3) == "Count: 1"


def test_counter_with_session_state_counts_and_a_new_session_starts_at_zero():
    code = w.WARMUP["counter_state.py"]
    assert w.counter_after_clicks(code, 3) == "Count: 3"
    assert w.counter_after_clicks(code, 0) == "Count: 0"


def test_echo_draws_four_bubbles_for_two_messages():
    assert w.echo_bubbles(w.WARMUP["echo.py"], w.ECHO_MESSAGES) == (
        "user: hello\n"
        "assistant: You said: hello\n"
        "user: Where is order A100?\n"
        "assistant: You said: Where is order A100?"
    )


def test_the_warmup_files_pass_ruff():
    folder = build_folder(w.WARMUP)
    for args in (["format", "--check", "."], ["check", "--isolated", "."]):
        result = subprocess.run(
            [sys.executable, "-m", "ruff", *args],
            cwd=folder,
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0, result.stdout


def test_app_parts_cover_app_py_in_order():
    parts = [w.app_part(name) for name in w.APP_PARTS]
    shown = [line for part in parts for line in part.split("\n") if line.strip()]
    whole = [line for line in w.app_file("app.py").split("\n") if line.strip()]
    assert shown == whole


def test_the_chat_part_draws_the_history_and_reruns():
    chat = w.app_part("chat")
    assert chat.startswith("with chat_tab:")
    assert chat.endswith("st.rerun()")


def test_bayside_app_py_has_not_changed_since_the_checkpoint():
    assert (REF / "bayside_app" / "app.py").read_text() == w.app_file("app.py")


def test_with_clicks_writes_the_slide_convention():
    assert w.with_clicks("x = 1", 3, "Count: 1") == (
        "x = 1\n\n# After 3 clicks the page shows:\n# Count: 1"
    )


def test_a_typed_address_is_filed_as_request_1():
    out = w.typed_shell()
    assert w.TYPED_ADDRESS in out
    assert out.split("\n")[-2] == "1"


def test_the_staff_row_shows_the_typed_address_as_plain_text():
    assert w.staff_row() == f"Request 1: A102 to {w.TYPED_ADDRESS}"
