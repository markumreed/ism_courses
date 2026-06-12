# ISM3232 Lab W08: Debugging, AI Literacy & Midterm Review

## YouTube Metadata

**Title:** Debugging, AI Literacy & Midterm Review — Lab Walkthrough | ISM3232 Lab 08
**Description:**
Walkthrough of ISM3232 Module 8 Lab. We fix two deliberate bugs using traceback reading and print() debugging, document the process in debug_log.md, write five pytest tests, and complete the AI reflection before the midterm.

Course page: https://markumreed.github.io/ism3232/docs/week08_lab.html

**Chapters:**
0:00 — What this lab covers
0:45 — Reading the traceback without fixing anything first
2:30 — Adding print() statements to locate the bug
4:30 — Documenting the fix in debug_log.md
6:30 — Five pytest tests for the fixed code
8:00 — AI reflection and midterm prep
9:00 — Submission checklist

**Applies to:** ISM3232 Module 08

**Tags:** python debugging traceback, python print debugging, python AI literacy, pytest fixed code, ISM3232, USF, python debugging tutorial

---

## Script

### INTRO (0:00–0:45)

Lab 8 — Debugging, AI Literacy, and Midterm Review. The lab gives you a script with two deliberate bugs. The workflow is strict: read the traceback first, add print() statements second, only then use AI as an explainer — not a fixer. Document every step in `debug_log.md`.

---

### STEP 1: READ THE TRACEBACK WITHOUT FIXING (0:45–2:30)

Run the buggy script first. Read every line of the output before touching the code.

A typical traceback:
```
Traceback (most recent call last):
  File "week8_buggy.py", line 14, in <module>
    result = process_order(price, qty)
  File "week8_buggy.py", line 6, in process_order
    return price * quantity
TypeError: can't multiply sequence by non-int of type 'float'
```

What you know from the traceback alone:
- Line 6 in `process_order`
- `price` is a sequence (string), not a number
- `quantity` is a float, not an int — or vice versa
- Root cause: likely missing type conversion on input

Now explain `process_order` to the duck — out loud, one line at a time, saying what each line *literally* does. This is rubber duck debugging, from *The Pragmatic Programmer* (Hunt & Thomas, 1999), and it's how you write the hypothesis: *"Line 6 multiplies price by quantity. Price came from input()... which returns a string. You can't multiply a string by a float."* What you just said to the duck goes straight into the log.

Write this analysis in `debug_log.md` before changing a single line of code.

```markdown
## Bug 1

**Error type:** TypeError
**Line:** 6 in process_order
**Error message:** can't multiply sequence by non-int of type 'float'
**What I told the duck:**
  line 6 multiplies price by quantity — but price came from input(), which returns str
**What I think the bug is (before fixing):**
  price is a string — probably came from input() without float() conversion
```

---

### STEP 2: PRINT() DEBUGGING (2:30–4:30)

Add print statements just before the crash:

```python
def process_order(price, quantity):
    print(f"DEBUG: price={price!r}, type={type(price)}")
    print(f"DEBUG: quantity={quantity!r}, type={type(quantity)}")
    return price * quantity
```

Run again. The output confirms:
```
DEBUG: price='49.99', type=<class 'str'>
DEBUG: quantity=3.0, type=<class 'float'>
```

Now you know exactly what's wrong. Remove the debug prints after fixing.

---

### STEP 3: AI AS EXPLAINER, NOT FIXER (4:30–5:30)

Paste only the error message into Claude or ChatGPT:
```
TypeError: can't multiply sequence by non-int of type 'float'
```

Ask: "What does this error mean in Python?"

Do NOT paste your code. Do NOT ask "fix this." The AI's explanation helps you understand the error class; you apply the fix yourself.

---

### DEBUG_LOG.MD (5:30–6:30)

Complete documentation for both bugs:

```markdown
# Debug Log — Week 8

## Bug 1

**Error type:** TypeError
**Line:** 6 in process_order
**Error message:** can't multiply sequence by non-int of type 'float'
**What I tried:** Added print() before line 6 — confirmed price was a str
**Root cause:** Input read with input() but not converted with float()
**Fix applied:** price = float(input("Enter price: "))
**AI use:** Asked Claude what TypeError means. Did not ask for fix.

## Bug 2

[Same structure — fill in for the second bug]

## AI Reflection

[Honest account: did AI help you understand or shortcut your understanding?
Would you have found the bug without it? What does that tell you?]
```

---

### FIVE PYTEST TESTS (6:30–8:00)

Write tests for the *fixed* code:

```python
# tests/test_week8.py
from week8_fixed import process_order, calculate_total, apply_tax

def test_process_order_basic():
    assert process_order(49.99, 3) == pytest.approx(149.97, rel=1e-3)

def test_process_order_zero_quantity():
    assert process_order(49.99, 0) == 0.0

def test_calculate_total_with_discount():
    assert calculate_total(100.0, 2, 0.10) == pytest.approx(180.0)

def test_apply_tax():
    assert apply_tax(100.0, 0.07) == pytest.approx(107.0)

def test_apply_tax_zero():
    assert apply_tax(100.0, 0.0) == 100.0
```

Screenshot 2: `pytest -v` all five green.

---

### SUBMISSION CHECKLIST (8:00–10:00)

- `debug_log.md` with both bugs documented in full (error, what you tried, root cause, fix, AI use)
- Fixed script with bugs corrected
- Five pytest tests all passing
- AI reflection section written honestly
- Screenshot 1: correct final output after both bugs fixed
- Screenshot 2: `pytest -v` all five green
- Ritual run, commit includes "lab 8", GitHub URL to Canvas
