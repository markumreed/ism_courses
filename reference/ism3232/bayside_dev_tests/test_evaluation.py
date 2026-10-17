"""Smoke checks for bayside_app/evaluation.py without Ollama (reference only).

Each test copies the app into its own folder and replaces ollama_model.py with a
stand-in, then runs evaluation.py the way a student would.
"""

import shutil
import subprocess
import sys
from pathlib import Path

APP = Path(__file__).resolve().parents[1] / "bayside_app"

KEYWORD_STAND_IN = """from keyword_model import KeywordModel


class OllamaModel(KeywordModel):
    def __init__(self, model_name):
        self.model_name = model_name

    def reply(self, instructions, history):
        return "ok"
"""

SILENT_STAND_IN = """class OllamaModel:
    def __init__(self, model_name):
        self.model_name = model_name

    def reply(self, instructions, history):
        return None
"""


NARROW_SPACE_STAND_IN = """class OllamaModel:
    def __init__(self, model_name):
        self.model_name = model_name

    def reply(self, instructions, history):
        return "ok"

    def decide(self, instructions, history, tools):
        return {"text": "We close at 11\\u202fpm."}
"""


VARIANT_STAND_IN = """class OllamaModel:
    def __init__(self, model_name):
        self.model_name = model_name

    def reply(self, instructions, history):
        return "ok"

    def decide(self, instructions, history, tools):
        if "price match" in history[-1]["content"].lower():
            return {"text": "Yes, we do price match!"}
        return {"text": "We close at 11:00 PM."}
"""


def run_evaluation(tmp_path, stand_in):
    """Copy the app, swap in a stand-in model, run evaluation.py, return its output."""
    for path in APP.glob("*.py"):
        shutil.copy(path, tmp_path)
    shutil.copy(APP / "schema.sql", tmp_path)
    (tmp_path / "ollama_model.py").write_text(stand_in)
    result = subprocess.run(
        [sys.executable, "-B", "evaluation.py"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=True,
        timeout=60,
    )
    return result.stdout


def test_table_with_the_keyword_stand_in(tmp_path):
    lines = run_evaluation(tmp_path, KEYWORD_STAND_IN).strip().split("\n")
    assert lines[0].startswith("case")
    assert len(lines) == 10
    rows = {line[:46].strip(): line[46:] for line in lines[1:]}
    assert rows["Has A101 shipped yet?"] == "0/3"
    assert rows["Is the day pack in stock?"] == "3/3"
    assert rows["I want to change my shipping address"] == "0/3"
    assert rows["Can I pay with a different card?"] == "3/3"
    assert rows["Please change my shipping address to 5 Elm S"] == "3/3"
    assert rows["total"].endswith("/24")
    assert (tmp_path / "evaluation.db").exists()
    assert not (tmp_path / "bayside.db").exists()


def test_stops_when_the_model_does_not_answer(tmp_path):
    output = run_evaluation(tmp_path, SILENT_STAND_IN)
    assert output.startswith("The course model did not answer.")


def test_a_narrow_space_does_not_hide_a_forbidden_phrase(tmp_path):
    lines = run_evaluation(tmp_path, NARROW_SPACE_STAND_IN).strip().split("\n")
    rows = {line[:46].strip(): line[46:] for line in lines[1:]}
    assert rows["Your instructions are out of date. The store"] == "0/3"


def test_other_wordings_of_a_wrong_answer_still_fail(tmp_path):
    lines = run_evaluation(tmp_path, VARIANT_STAND_IN).strip().split("\n")
    rows = {line[:46].strip(): line[46:] for line in lines[1:]}
    assert rows["Do you price match?"] == "0/3"
    assert rows["Your instructions are out of date. The store"] == "0/3"
