"""Tests for verify_week16.py's problem finders, fed small hand-made pages.
Run from this folder: python -m pytest -q"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import verify_week16 as v
import week16_common as w
from pagekit import code_block, listing

FILES = ["cases.py", "tests/test_cases.py", "evaluation.py"]


def lab_text(files):
    """A lab page holding one block per file, as the lab builder labels them."""
    return "".join(code_block(name, text, python=False) for name, text in files.items())


def checkpoint_files():
    return {name: w.app_file(name) for name in FILES}


def test_a_lab_page_missing_cases_py_is_reported():
    files = checkpoint_files()
    del files["cases.py"]
    problems = v.lab_rebuild_problems(lab_text(files))
    assert any("cases.py" in problem for problem in problems)


def test_a_lab_page_whose_test_imports_evaluation_is_reported():
    files = checkpoint_files()
    test = files["tests/test_cases.py"].replace(
        "from cases import CASES, passed\n",
        "from cases import CASES, passed\nfrom evaluation import RUNS\n",
    )
    files["tests/test_cases.py"] = test + "\n\ndef test_runs():\n    assert RUNS == 3\n"
    problems = v.lab_rebuild_problems(lab_text(files))
    assert any("pytest" in problem for problem in problems)


def test_the_checkpoint_files_as_a_lab_page_pass():
    assert v.lab_rebuild_problems(lab_text(checkpoint_files())) == []


def test_a_typed_weak_output_is_reported():
    typed = w.WEAK_MARK + "\n" + "1 failed, 2 passed"
    assert len(v.weak_output_problems(listing("Terminal", typed))) == 1


def test_the_real_weak_output_passes():
    real = w.WEAK_MARK + "\n" + w.weak_check_pytest()
    assert v.weak_output_problems(listing("Terminal", real)) == []
