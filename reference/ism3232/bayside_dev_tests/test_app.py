"""Streamlit AppTest checks for bayside_app/app.py (reference only; students do not write these).

Each test copies the app into its own folder, so it gets a fresh bayside.db.
Run with a Python that has streamlit and pytest:
    python -m pytest -q reference/ism3232/bayside_dev_tests
"""

import shutil
import sys
from pathlib import Path

from streamlit.testing.v1 import AppTest

APP = Path(__file__).resolve().parents[1] / "bayside_app"
KEYWORDS_ONLY = "Keyword rules only (no AI)"


def start_app(tmp_path, monkeypatch):
    """Copy the app to tmp_path, move there, and return a fresh AppTest."""
    for path in APP.glob("*.py"):
        shutil.copy(path, tmp_path)
    shutil.copy(APP / "schema.sql", tmp_path)
    monkeypatch.chdir(tmp_path)
    monkeypatch.syspath_prepend(str(tmp_path))
    for name in ("database", "tools", "agent", "settings", "app"):
        sys.modules.pop(name, None)
    app = AppTest.from_file(str(tmp_path / "app.py"), default_timeout=30)
    return app


def test_app_starts_and_creates_the_database(tmp_path, monkeypatch):
    app = start_app(tmp_path, monkeypatch)
    app.run()
    assert not app.exception
    assert (tmp_path / "bayside.db").exists()
    assert app.title[0].value == "Bayside Outfitters"


def test_chat_history_survives_reruns(tmp_path, monkeypatch):
    app = start_app(tmp_path, monkeypatch)
    app.run()
    app.sidebar.radio[0].set_value(KEYWORDS_ONLY).run()
    app.chat_input[0].set_value("hello").run()
    app.chat_input[0].set_value("Where is order A100?").run()
    assert not app.exception
    assert len(app.session_state["bot"].history) == 5
    assert len(app.chat_message) == 4
    assert app.chat_message[3].markdown[0].value == "Order A100 is shipped."


def test_switching_the_model_keeps_the_conversation(tmp_path, monkeypatch):
    app = start_app(tmp_path, monkeypatch)
    app.run()
    app.sidebar.radio[0].set_value(KEYWORDS_ONLY).run()
    app.chat_input[0].set_value("hello").run()
    app.sidebar.radio[0].set_value("Course model, keyword rules if it is down").run()
    assert len(app.session_state["bot"].history) == 2


def test_one_approve_click_changes_the_order_once(tmp_path, monkeypatch):
    app = start_app(tmp_path, monkeypatch)
    app.run()
    import database

    database.add_change_request("bayside.db", "A102", "9 Pine Street, Tampa")
    app.run()
    app.button(key="approve1").click().run()
    assert app.success[0].value == "Request 1 approved."
    assert (
        database.find_order("bayside.db", "A102")["address"] == "9 Pine Street, Tampa"
    )
    assert database.waiting_requests("bayside.db") == []
    app.run()
    assert len(app.success) == 0
    assert database.find_request("bayside.db", 1)["status"] == "approved"


def test_reject_click_leaves_the_order_alone(tmp_path, monkeypatch):
    app = start_app(tmp_path, monkeypatch)
    app.run()
    import database

    database.add_change_request("bayside.db", "A102", "9 Pine Street, Tampa")
    app.run()
    app.button(key="reject1").click().run()
    assert app.success[0].value == "Request 1 rejected."
    assert database.find_order("bayside.db", "A102")["address"] == "88 Pier Street"


def test_restock_form_updates_the_stock(tmp_path, monkeypatch):
    app = start_app(tmp_path, monkeypatch)
    app.run()
    app.selectbox[0].set_value("day pack")
    app.number_input[0].set_value(7)
    app.button[0].click().run()
    import database

    assert database.find_product("bayside.db", "day pack")["stock"] == 7
    assert app.success[0].value == "The day pack now has 7 in stock."
