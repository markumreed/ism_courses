# ISM3232 Lab W08: Debugging, AI Literacy & Midterm Review

## YouTube Metadata

**Title:** Debugging, Tracebacks & AI Literacy — Full Lab Walkthrough | ISM3232 Lab 08
**Description:**
Step-by-step, test-as-you-go walkthrough of ISM3232 Module 8 Lab. Run a deliberately buggy script, read the traceback bottom-up, rubber-duck the broken function before touching AI, fix two bugs with print() debugging, write five pytest tests for the fixed code, and complete an honest AI literacy reflection — debug first, then ask.

Course page: https://markumreed.github.io/ism3232/docs/week08_lab.html

**Chapters:**
0:00 — The rule: debug first, then ask
0:45 — Step 1: set up and type the buggy script exactly
2:00 — Step 2: run it and read the traceback bottom-up
3:20 — Step 3: rubber-duck get_total() before touching code
4:30 — Step 4: start debug_log.md — Bug 1 section
5:20 — Step 5: add a DEBUG print inside get_total()
6:20 — Step 6: spot and fix the typo, remove the print
7:00 — Step 7: a new error appears — read Bug 2's traceback
7:50 — Step 8: rubber-duck the type comparison, fix it
8:40 — Screenshot 1 checkpoint — correct final output
9:00 — Step 9: write all five pytest tests for the fixed code
10:40 — Step 10: run pytest -v and confirm all green
11:10 — Screenshot 2 checkpoint
11:30 — Step 11: complete the AI literacy reflection honestly
12:30 — Step 12: the ritual and push
13:20 — Submission checklist

**Applies to:** ISM3232 Module 08

**Tags:** python debugging traceback, python print debugging, python AI literacy, pytest fixed code, ISM3232, USF, python debugging tutorial, rubber duck debugging

---

## How to Use This Script

**SAY** it, **DO** it, **CHECK** the exact output, **FIX** it if it doesn't match — then move to the next step. This lab is graded on *process*, not just working code, so every step here includes what to write in `debug_log.md`, not just what to type in the terminal.

---

## Script

### INTRO (0:00–0:45)

**SAY:** "Lab 8 — debugging, tracebacks, and AI literacy. The rule for today: debug first, then ask. Attempt to fix each bug yourself using the traceback and `print()` before touching any AI tool. Document what you tried in `debug_log.md` *before* you ask AI anything. Let's go."

---

### PART 1 — Set Up and Read the First Traceback (0:45–3:20)

#### Step 1 — Set up and type the buggy script exactly

**SAY:** "Type this script exactly as shown — it has three bugs, and yes, we're introducing them on purpose."

**DO:**
```bash
cd ~/ism3232/module05_functions
source .venv/bin/activate
touch week8_buggy.py debug_log.md
```
Type into `week8_buggy.py`:
```python
# week8_buggy.py  -- three bugs -- do not fix yet

records = [
    {'id': 1, 'name': 'Taylor', 'amout': 1200},
    {'id': 2, 'name': 'Jordan', 'amount': 450},
    {'id': 3, 'name': 'Morgan', 'amount': 3500},
]


def get_total(records):
    total = 0
    for rec in records:
        total += rec['amount']
    return total


def is_over_limit(amount):
    return amount > '1000'


def format_summary(total, count):
    return f'Total: ${total:.2f} across {count} records'


total = get_total(records)
print(format_summary(total, len(records)))
print(is_over_limit(total))
```

**CHECK:** Don't fix anything yet — even the `'amout'` typo on line 4 (missing the second `n`) stays exactly as typed. That typo *is* Bug 1.

---

#### Step 2 — Run it and read the traceback bottom-up

**DO:**
```bash
python3 week8_buggy.py
```

**CHECK:** A `KeyError: 'amount'` traceback, ending in something like:
```
Traceback (most recent call last):
  File "week8_buggy.py", line 20, in <module>
    total = get_total(records)
  File "week8_buggy.py", line 12, in get_total
    total += rec['amount']
KeyError: 'amount'
```

**SAY:** "Read it bottom-up, out loud, three questions: One — what's the error type on the last line? `KeyError`. Two — which file and line is highlighted? `week8_buggy.py`, line 12, inside `get_total`. Three — what does `KeyError` mean? Python tried to look up a dictionary key that doesn't exist on *that particular* dict."

---

#### Step 3 — Rubber-duck get_total() before touching code

**SAY:** "Before changing a single character, explain `get_total()` to the duck — out loud, one line at a time, saying what each line *literally* does, not what it's supposed to do. This is rubber duck debugging, from *The Pragmatic Programmer* (Hunt & Thomas, 1999)."

**DO:** Out loud: "Line 1 sets `total` to zero. Line 2 loops over every dict in `records`. Line 3 adds `rec['amount']` to the running total... wait — the first record's key is `'amout'`, not `'amount'`. That's it. That's the bug."

**CHECK:** You should be able to point at the exact dict literal (`{'id': 1, 'name': 'Taylor', 'amout': 1200}`) and the exact key name that's misspelled, purely from reading the code out loud — before running anything else.

---

#### Step 4 — Start debug_log.md, Bug 1 section

**SAY:** "Everything we just said out loud goes into the log now, before we touch the fix."

**DO:** In `debug_log.md`:
```markdown
# debug_log.md
# Author: [Your Name]

## Bug 1
Error type: KeyError
File + line: week8_buggy.py, line 12, in get_total
What the error means: Tried to access a dict key that doesn't exist on that record
What I told the duck: get_total loops over records and adds rec['amount'] each time —
  but the first record's key is spelled 'amout', not 'amount'
What I tried: (fill in after Step 5)
How I fixed it: (fill in after Step 6)
```

---

### PART 2 — Fix Bug 1 (5:20–7:00)

#### Step 5 — Add a DEBUG print inside get_total()

**SAY:** "Even though we already spotted it by reading, let's confirm with `print()` debugging — the habit matters more than this one easy case."

**DO:**
```python
def get_total(records):
    total = 0
    for rec in records:
        print(f'DEBUG: rec = {rec}')   # add this
        total += rec['amount']
    return total
```
```bash
python3 week8_buggy.py
```

**CHECK:**
```
DEBUG: rec = {'id': 1, 'name': 'Taylor', 'amout': 1200}
```
The crash happens right after printing that first record — confirming the bad key is on the *first* record, exactly as suspected.

---

#### Step 6 — Fix the typo, remove the print, confirm

**DO:** In the `records` list, fix `'amout'` → `'amount'`. Remove the `DEBUG` print line from `get_total`. Run again:
```bash
python3 week8_buggy.py
```

**CHECK:** Bug 1 is gone — the script now progresses further (it will hit Bug 2 next, which is expected). Update `debug_log.md`: "What I tried: added a DEBUG print of each record. How I fixed it: corrected the key from `'amout'` to `'amount'` in the first record."

---

### PART 3 — Fix Bug 2 (7:00–8:40)

#### Step 7 — A new error appears — read Bug 2's traceback

**DO:**
```bash
python3 week8_buggy.py
```

**CHECK:**
```
Total: $5150.00 across 3 records
Traceback (most recent call last):
  File "week8_buggy.py", line 22, in <module>
    print(is_over_limit(total))
  File "week8_buggy.py", line 16, in is_over_limit
    return amount > '1000'
TypeError: '>' not supported between instances of 'float' and 'str'
```

**SAY:** "Notice `format_summary` already printed correctly — Bug 1 really is fixed. This new error is entirely separate: `TypeError`, comparing a float to a string with `>`."

---

#### Step 8 — Rubber-duck the comparison, fix it without AI

**SAY:** "Say out loud what type each side of the `>` actually is, before reaching for AI or even changing the code."

**DO:** Out loud: "`amount` comes in as a float — it's `total` from `get_total`, which summed numbers. The right side, `'1000'`, is a string — it's in quotes. Python won't compare a float to a string with `>`. The fix: drop the quotes so `'1000'` becomes the number `1000`."

Fix it:
```python
def is_over_limit(amount):
    return amount > 1000
```

**CHECK:**
```bash
python3 week8_buggy.py
```
```
Total: $5150.00 across 3 records
True
```

Update `debug_log.md`'s Bug 2 section with the same structure as Bug 1: error type `TypeError`, file/line, what it means, what you told the duck, and the fix (`'1000'` → `1000`, removing the string quotes).

---

#### Screenshot 1 checkpoint (8:40–9:00)

**SAY:** "Screenshot 1 — the correct final output, both bugs fixed: `Total: $5150.00 across 3 records` followed by `True`."

---

### PART 4 — Write Tests for the Fixed Code (9:00–11:10)

#### Step 9 — Write all five tests

**SAY:** "Now that both bugs are fixed, lock in that behavior with tests, so nobody — including future you — reintroduces either bug silently."

**DO:**
```bash
touch tests/test_week8.py
code tests/test_week8.py
```
```python
from week8_buggy import get_total, is_over_limit, format_summary


def test_get_total_correct():
    recs = [{'amount': 100}, {'amount': 200}]
    assert get_total(recs) == 300


def test_is_over_limit_true():
    assert is_over_limit(1500) is True


def test_is_over_limit_false():
    assert is_over_limit(500) is False


def test_is_over_limit_boundary():
    assert is_over_limit(1000) is False


def test_format_summary():
    result = format_summary(1234.56, 3)
    assert '1234.56' in result
    assert '3' in result
```

**CHECK:** Notice `test_is_over_limit_boundary` — exactly the kind of edge case that would have caught Bug 2 immediately if it existed *before* the bug was introduced: comparing `1000` (int) against the fixed `1000` (also now an int) works because both sides are the same type.

---

#### Step 10 — Run pytest and confirm all green

**DO:**
```bash
pytest -v
```

**CHECK:**
```
tests/test_week8.py::test_get_total_correct PASSED
tests/test_week8.py::test_is_over_limit_true PASSED
tests/test_week8.py::test_is_over_limit_false PASSED
tests/test_week8.py::test_is_over_limit_boundary PASSED
tests/test_week8.py::test_format_summary PASSED

======================== 5 passed in 0.01s ========================
```

---

#### Screenshot 2 checkpoint (11:10–11:30)

**SAY:** "Screenshot 2 — `pytest -v` with all five tests green."

---

### PART 5 — AI Reflection and Push (11:30–13:20)

#### Step 11 — Complete the AI literacy reflection honestly

**SAY:** "Last section of `debug_log.md`. Be honest, not aspirational — if you didn't need AI for this lab, say so and say why."

**DO:** In `debug_log.md`:
```markdown
## After Fixing Both Bugs
Final output: Total: $5150.00 across 3 records / True
Did pytest pass? Yes

## AI Literacy Reflection
Did I use AI? [Yes / No]
If yes -- exact prompt I used: [paste it exactly]
What AI explained: [in your own words]
What I changed myself: [be specific]
Can I explain every fixed line? Yes

## What I learned
[2-3 honest sentences]
```

**CHECK:** Read your own reflection back out loud — if you used AI, confirm you pasted the *exact* prompt, not a paraphrase, and that you can explain every line of the fix without looking at the AI's response again.

---

#### Step 12 — Run the ritual

**DO:**
```bash
ruff format . && ruff check . && pytest
git add . && git commit -m 'lab 8: debugging ai literacy' && git push
```

**CHECK:** No lint errors, `5 passed`, push succeeds, commit message includes "lab 8."

---

### SUBMISSION CHECKLIST (13:20–end)

- [ ] Screenshot 1: correct final output after both bugs are fixed
- [ ] Screenshot 2: `pytest -v` showing all five tests passing
- [ ] `debug_log.md` — all sections completed, including the AI reflection
- [ ] Git commit message includes "lab 8"
- [ ] GitHub repository URL pasted into Canvas
