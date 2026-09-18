# ISM3232 Lab W07: Functions, Modules & pytest

## YouTube Metadata

**Title:** Functions, Modules & pytest — Full Lab Walkthrough | ISM3232 Lab 07
**Description:**
Step-by-step, test-as-you-go walkthrough of ISM3232 Module 7 Lab. Split business logic into a separate business_rules.py module — four functions, each with a docstring, type hints, and a return value (never a print) — import them into main.py, write eight pytest tests including two boundary cases, then run the ritual and push.

Course page: https://markumreed.github.io/ism3232/docs/week07_lab.html

**Chapters:**
0:00 — What this lab covers — why functions never print
0:45 — Step 1: fresh project + required file structure
2:00 — Step 2: write calculate_total and requires_review
3:10 — Step 3: write get_approval_tier and apply_discount
4:30 — Step 4: write main.py and import all four functions
5:40 — Step 5: run main.py and verify all four results
6:30 — Screenshot 1 checkpoint
6:50 — Step 6: write all eight pytest tests
9:20 — Step 7: the two boundary-case tests, explained
10:10 — Step 8: run pytest -v and confirm all eight green
10:40 — Screenshot 2 checkpoint
11:00 — Step 9: the ritual and push
11:50 — Submission checklist

**Applies to:** ISM3232 Module 07

**Tags:** python functions tutorial, python modules import, pytest boundary testing, type hints python, ISM3232, USF, python doctest tutorial

---

## How to Use This Script

**SAY** it, **DO** it, **CHECK** the exact output, **FIX** it if it doesn't match — then move to the next step.

---

## Script

### INTRO (0:00–0:45)

**SAY:** "Lab 7 — functions, modules, and pytest. One hard rule today: no `print()` at the module level inside `business_rules.py`. Functions return values. `main.py` calls them and prints the results. Tests assert the return values. Separating 'compute' from 'display' is the single biggest structural upgrade in this course so far."

---

### PART 1 — Required Project Structure (0:45–2:00)

#### Step 1 — Fresh setup and required files

**DO:**
```bash
cd ~/ism3232/module05_functions
python3 -m venv .venv && source .venv/bin/activate
pip install pytest ruff && pip freeze > requirements.txt
echo '.venv/' > .gitignore && echo '__pycache__/' >> .gitignore
touch business_rules.py main.py
mkdir -p tests && touch tests/__init__.py tests/test_business_rules.py
```

**CHECK:**
```bash
ls
```
shows `business_rules.py`, `main.py`, `tests/`, `.venv/`, `.gitignore`, `requirements.txt` — four separate pieces before you've written a single line of logic.

---

### PART 2 — Write the Functions (2:00–4:30)

#### Step 2 — calculate_total and requires_review

**SAY:** "Every function here gets three things: a type-hinted signature, a docstring explaining what it returns, and a `return` statement — never a `print`."

**DO:** In `business_rules.py`:
```python
# business_rules.py
# Author: [Your Name]

APPROVAL_LIMIT = 1000


def calculate_total(price: float, quantity: int) -> float:
    """Return total cost including 7% tax."""
    return price * quantity * 1.07


def requires_review(amount: float) -> bool:
    """Return True if amount exceeds the approval limit."""
    return amount > APPROVAL_LIMIT
```

**CHECK:** Read the type hints out loud: "`price: float, quantity: int) -> float` — two typed parameters in, one float out. These hints don't change how Python runs the code, but they document intent and let editors catch mismatches."

---

#### Step 3 — get_approval_tier and apply_discount

**SAY:** "Two more functions — one with a three-way branch, one that takes a percentage."

**DO:** Append:
```python
def get_approval_tier(amount: float) -> str:
    """Return the approval routing tier."""
    if amount <= 500:    return 'auto'
    elif amount <= 2000: return 'manager'
    else:                return 'director'


def apply_discount(price: float, pct: float) -> float:
    """Return price after discount. pct is 0-100."""
    return price * (1 - pct / 100)
```

**CHECK:** Trace the three branches out loud before moving on: "500 or under — `'auto'`. Between 500 and 2000 — `'manager'`. Above 2000 — `'director'`. Notice both boundary comparisons use `<=`, so exactly 500 lands in `'auto'`, and exactly 2000 lands in `'manager'`, not the tier above."

---

### PART 3 — Import and Call in main.py (4:30–6:30)

#### Step 4 — Write main.py

**SAY:** "`main.py` is the only file that imports and calls the business logic, and the only file allowed to `print`."

**DO:**
```python
# main.py
from business_rules import calculate_total, requires_review, get_approval_tier, apply_discount

price, qty = 450.00, 3
total = calculate_total(price, qty)

print(f'Total:          ${total:.2f}')
print(f'Requires review: {requires_review(total)}')
print(f'Approval tier:   {get_approval_tier(total)}')
print(f'10% discount:    ${apply_discount(price, 10):.2f}')
```

**CHECK:** Read the import line out loud: "One line pulls all four functions from `business_rules` — Python finds it because it's a `.py` file sitting right next to `main.py` in the same folder."

---

#### Step 5 — Run and verify

**DO:**
```bash
python3 main.py
```

**CHECK:**
```
Total:          $1444.50
Requires review: True
Approval tier:   manager
10% discount:    $405.00
```

**FIX:** If you get `ModuleNotFoundError: No module named 'business_rules'`, confirm you're running `python3 main.py` from inside `module05_functions` — the same folder that contains `business_rules.py` — with `pwd`.

---

#### Screenshot 1 checkpoint (6:30–6:50)

**SAY:** "Screenshot 1 — the `main.py` output showing all four function results."

---

### PART 4 — Write Eight pytest Tests (6:50–10:40)

#### Step 6 — Write all eight tests

**SAY:** "Eight tests this week, up from five — because we're deliberately including boundary cases: the exact edge value where a rule's behavior changes."

**DO:** In `tests/test_business_rules.py`:
```python
from business_rules import calculate_total, requires_review, get_approval_tier, apply_discount


def test_total_includes_tax():
    assert round(calculate_total(100.00, 2), 2) == 214.00


def test_requires_review_over():
    assert requires_review(1500) is True


def test_requires_review_under():
    assert requires_review(500) is False


def test_boundary_at_limit():
    # Exactly at 1000 should NOT require review (> not >=)
    assert requires_review(1000) is False


def test_tier_auto():
    assert get_approval_tier(400) == 'auto'


def test_tier_boundary_500():
    assert get_approval_tier(500) == 'auto'  # exactly at limit


def test_tier_manager():
    assert get_approval_tier(1500) == 'manager'


def test_discount_ten():
    assert apply_discount(100.00, 10) == 90.0
```

**CHECK:** Count: eight `def test_` functions.

---

#### Step 7 — The two boundary cases, explained

**SAY:** "Look specifically at `test_boundary_at_limit` and `test_tier_boundary_500` before running anything. `requires_review` uses `>`, so an amount of *exactly* 1000 does **not** require review — only strictly greater than. `get_approval_tier` uses `<=`, so an amount of *exactly* 500 **is** still `'auto'`. These two tests exist specifically to catch the classic off-by-one mistake of writing `>=` when the rule means `>`, or vice versa."

---

#### Step 8 — Run pytest and confirm all eight green

**DO:**
```bash
pytest -v
```

**CHECK:**
```
tests/test_business_rules.py::test_total_includes_tax PASSED
tests/test_business_rules.py::test_requires_review_over PASSED
tests/test_business_rules.py::test_requires_review_under PASSED
tests/test_business_rules.py::test_boundary_at_limit PASSED
tests/test_business_rules.py::test_tier_auto PASSED
tests/test_business_rules.py::test_tier_boundary_500 PASSED
tests/test_business_rules.py::test_tier_manager PASSED
tests/test_business_rules.py::test_discount_ten PASSED

======================== 8 passed in 0.01s ========================
```

---

#### Screenshot 2 checkpoint (10:40–11:00)

**SAY:** "Screenshot 2 — `pytest -v` with all eight tests green."

---

### PART 5 — Ritual and Push (11:00–11:50)

#### Step 9 — Run the ritual

**DO:**
```bash
ruff format . && ruff check . && pytest -v
git add . && git commit -m 'lab 7: functions modules pytest' && git push
```

**CHECK:** No lint errors, `8 passed`, push succeeds, commit message includes "lab 7."

---

### SUBMISSION CHECKLIST (11:50–end)

- [ ] Screenshot 1: `main.py` output showing all four function results
- [ ] Screenshot 2: `pytest -v` with all eight tests green
- [ ] `business_rules.py` has zero `print()` calls at the module level
- [ ] Git commit message includes "lab 7"
- [ ] GitHub repository URL pasted into Canvas
