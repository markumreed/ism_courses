"""Tests for week14_common.py. Run from this folder: python -m pytest -q"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import week14_common as w
from pagekit import read


def test_the_warmup_database_block_stops_before_reset_database():
    top = w.warmup_database_top()
    assert "def create_tables" in top
    assert "def reset_database" not in top
    assert w.app_file("database.py").startswith(top)


def test_the_warmup_test_passes():
    assert w.warmup_pytest() == "1 passed"


def test_the_warmup_shell_shows_a_dict_none_and_a_refusal():
    out = w.warmup_shell()
    assert "'order_id': 'A100'" in out
    assert "\nNone\n" in out
    assert "'Order A100 is shipped.'" in out
    assert "has not given that order ID" in out


def test_the_reading_shell_returns_rows_as_dictionaries():
    out = w.reading_shell()
    assert (
        "[{'name': 'day pack', 'stock': 0}, {'name': 'hiking socks', 'stock': 0}]"
        in out
    )


def test_only_the_fstring_query_lets_the_text_through():
    assert w.snippet_outputs()["injection"] == (
        "6 orders from the f-string query\nNone from find_order"
    )


def test_agent_differs_from_week12_chatbot_only_in_its_first_line():
    agent = w.app_file("agent.py").split("\n")
    chatbot = read("module06_agents/chatbot.py", w.WEEK12_REV).split("\n")
    assert agent[0] == "# agent.py" and chatbot[0] == "# chatbot.py"
    assert agent[1:] == chatbot[1:]


def test_decide_sends_only_the_last_max_messages():
    assert "MAX_MESSAGES = 20" in w.app_file("ollama_model.py")
    assert "history[-MAX_MESSAGES:]" in w.app_method("ollama_model.py", "decide")
