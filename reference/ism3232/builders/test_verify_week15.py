"""Tests for verify_week15.py. Run from this folder: python -m pytest -q"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import verify_week15 as v
import week15_common as w
from pagekit import code_block, esc, expected


def lab_page(drop=None, wrong=False):
    """A lab page holding the three warm-up files and their four expected boxes."""
    results = w.warmup_results()
    if wrong:
        results["counter"] = "Count: 3"
    parts = [
        code_block(label, w.WARMUP[label], python=False) for label in w.LABELS.values()
    ]
    parts += [expected(text) for text in results.values()]
    if drop is not None:
        parts.pop(drop)
    return "\n".join(parts)


def test_a_lab_page_with_the_warmup_has_no_problems():
    assert v.warmup_problems(lab_page()) == []


def test_a_lab_page_missing_echo_is_reported():
    assert v.warmup_problems(lab_page(drop=2)) != []


def test_a_lab_page_whose_box_is_wrong_is_reported():
    assert v.warmup_problems(lab_page(wrong=True)) != []


def slide(code, clicks, shown):
    block = esc(w.with_clicks(code, clicks, shown))
    return f'<pre><code class="language-python">{block}</code></pre>'


def test_a_counter_slide_that_matches_passes():
    assert v.counter_slide_problems(slide(w.WARMUP["counter.py"], 3, "Count: 1")) == []


def test_a_counter_slide_that_differs_is_reported():
    assert v.counter_slide_problems(slide(w.WARMUP["counter.py"], 3, "Count: 3")) != []


def test_a_missing_screenshot_is_reported():
    assert v.image_problems('<img src="../assets/img/week15/chat.png" alt="x">') == []
    assert v.image_problems('<img src="../assets/img/week15/nope.png" alt="x">') != []
