"""Tests for check.py. Run with: python -m pytest reference/ism3232/tools -q"""

from pathlib import Path

from check import check

GOOD_CODE = '''def add(a, b):
    """Return the sum."""
    return a + b
'''

GOOD_TEST = """from adder import add


def test_add():
    assert add(2, 3) == 5
"""


def make_project(root, code=GOOD_CODE, test=GOOD_TEST):
    """Write a tiny lab folder the way students lay one out."""
    folder = Path(root) / "lab"
    (folder / "tests").mkdir(parents=True)
    (folder / "adder.py").write_text(code)
    (folder / "tests" / "__init__.py").write_text("")
    (folder / "tests" / "test_adder.py").write_text(test)
    return folder


def test_clean_project_passes(tmp_path):
    assert check(make_project(tmp_path)) == 0


def test_unformatted_code_fails(tmp_path):
    folder = make_project(tmp_path, code="def add(a,b):\n    return a+b\n")
    assert check(folder) != 0


def test_a_test_that_needs_ollama_fails(tmp_path):
    test = "import ollama\n\n\ndef test_x():\n    assert ollama\n"
    assert check(make_project(tmp_path, test=test)) != 0


def test_a_test_that_needs_streamlit_fails(tmp_path):
    test = "import streamlit\n\n\ndef test_x():\n    assert streamlit\n"
    assert check(make_project(tmp_path, test=test)) != 0


def test_the_folder_itself_is_not_changed(tmp_path):
    folder = make_project(tmp_path)
    check(folder)
    assert not (folder / ".ruff_cache").exists()
    assert not (folder / "tests" / "__pycache__").exists()
