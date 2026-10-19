"""Tests for verify_week14.py. Run from this folder: python -m pytest -q"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import verify_week14 as v
import week14_common as w
from pagekit import code_block, esc, expected, with_output


def warmup_page(drop=None):
    """A lab page holding the warm-up blocks and the two expected boxes."""
    files = w.warmup_files()
    parts = [
        code_block(w.LABELS["db_top"], w.warmup_database_top(), python=False),
        code_block(w.LABELS["db_find"], w.app_function("find_order"), python=False),
        code_block(w.LABELS["tools"], files["tools.py"], python=False),
        code_block(w.LABELS["test_top"], w.warmup_test_top(), python=False),
        code_block(w.LABELS["test_find"], w.warmup_find_test(), python=False),
        code_block(w.LABELS["shell"], "\n".join(w.WARMUP_SHELL), python=False),
        expected(w.warmup_shell()),
        expected(w.warmup_pytest()),
    ]
    if drop is not None:
        parts.pop(drop)
    return "\n".join(parts)


def test_a_page_that_matches_the_warmup_has_no_problems():
    assert v.warmup_problems(warmup_page()) == []


def test_a_page_missing_a_block_is_reported():
    assert v.warmup_problems(warmup_page(drop=1)) != []


def slide(code, output):
    return f'<pre><code class="language-python">{esc(with_output(code, output))}</code></pre>'


def test_a_slide_whose_output_matches_passes():
    code = w.SNIPPETS["injection"]
    assert v.slide_problems(slide(code, w.snippet_outputs()["injection"])) == []


def test_a_slide_whose_output_differs_is_reported():
    code = w.SNIPPETS["injection"]
    wrong = "6 orders from the f-string query\n6 from find_order"
    assert v.slide_problems(slide(code, wrong)) != []


def test_checkpoint_sources_include_every_app_file():
    sources = v.checkpoint_sources()
    assert w.app_file("database.py") in sources
    assert w.app_file("tests/test_tools.py") in sources
