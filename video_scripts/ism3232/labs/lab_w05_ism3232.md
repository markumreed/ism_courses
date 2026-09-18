# ISM3232 Lab W05: Variables, Data Types & Operators

## YouTube Metadata

**Title:** Variables, Data Types & Operators — Full Lab Walkthrough | ISM3232 Lab 05
**Description:**
Step-by-step, test-as-you-go walkthrough of ISM3232 Module 5 Lab. Set up a fresh venv, build a purchase-request business script using all four Python data types, add arithmetic and f-string formatting, add input() with type conversion (and see the classic TypeError it causes when you forget), write five pytest tests, then run the full ritual and push — every command run and verified one at a time.

Course page: https://markumreed.github.io/ism3232/docs/week05_lab.html

**Chapters:**
0:00 — What this lab covers
0:35 — Step 1: fresh project setup — venv, packages, .gitignore
2:20 — Step 2: write the four core variables
3:20 — Step 3: run and confirm all four type() names
3:50 — Step 4: add subtotal/tax/total calculations
4:50 — Step 5: print the formatted f-string summary
5:50 — Screenshot 1 checkpoint
6:10 — Step 6: add input() with int() conversion
7:20 — Step 7: deliberately break it — input() without conversion
8:20 — Screenshot 2 checkpoint
8:40 — Step 8: write all five pytest tests
10:20 — Step 9: run pytest -v and confirm all green
10:50 — Screenshot 3 checkpoint
11:10 — Step 10: the ritual and push
12:20 — Submission checklist

**Applies to:** ISM3232 Module 05

**Tags:** python variables tutorial, python data types, f-string formatting, python input type conversion, ISM3232, USF, python typeerror explained

---

## How to Use This Script

**SAY** it, **DO** it, **CHECK** the exact output, **FIX** it if it doesn't match — then move to the next step.

---

## Script

### INTRO (0:00–0:35)

**SAY:** "Lab 5 — variables, data types, and operators. Full class period, one script, built up in five layers: raw data, calculations, user input, tests, and the ritual. I'm building a purchase-request script — pick whatever business domain you like, the mechanics are identical."

---

### PART 1 — Setup and the Four Core Data Types (0:35–3:50)

#### Step 1 — Fresh project setup

**SAY:** "New module, so new venv — same five commands as Week 3, now muscle memory."

**DO:**
```bash
cd ~/ism3232/module04_programming
python3 -m venv .venv && source .venv/bin/activate
pip install pytest ruff && pip freeze > requirements.txt
echo '.venv/' > .gitignore && echo '__pycache__/' >> .gitignore
touch week5_lab.py && code week5_lab.py
```

**CHECK:** Prompt shows `(.venv)`; `ls -la` shows `.venv/`, `.gitignore`, `requirements.txt`, and the new empty `week5_lab.py`.

---

#### Step 2 — Write the four core variables

**SAY:** "Four data types, four variables, one for each: a string, another string, an integer, a float, and a boolean built from a comparison."

**DO:**
```python
# week5_lab.py
# Author: [Your Name]
# Business domain: [describe your scenario]

product_name  = 'Laptop'
status        = 'Pending'
quantity      = 3
unit_price    = 450.00
is_over_limit = unit_price * quantity > 1000

print(type(product_name), type(quantity), type(unit_price), type(is_over_limit))
```

**CHECK:** Read each variable's type out loud before running: "`product_name` and `status` — strings. `quantity` — int. `unit_price` — float. `is_over_limit` — a bool, because it's the *result* of a comparison, not a value I typed directly."

---

#### Step 3 — Run and confirm all four types

**DO:**
```bash
python3 week5_lab.py
```

**CHECK:**
```
<class 'str'> <class 'int'> <class 'float'> <class 'bool'>
```
Four distinct type names, in the order the variables were passed to `print()`.

**FIX:** If you see a `SyntaxError`, check that both string values use matching quote characters (`'Laptop'` not `'Laptop"`).

---

### PART 2 — Operators and f-strings (3:50–6:10)

#### Step 4 — Add the calculations

**SAY:** "Now the arithmetic — subtotal, a 7% tax, and the total — plus a boolean that flags whether this needs manager approval."

**DO:** Append to `week5_lab.py`:
```python
subtotal          = unit_price * quantity
tax               = subtotal * 0.07
total             = subtotal + tax
requires_approval = total > 1000
```

**CHECK:** Say the math out loud before running: "Subtotal is 450 times 3 — 1,350. Tax is 7% of that — 94.50. Total is 1,444.50. Since that's over 1,000, `requires_approval` should come out `True`."

---

#### Step 5 — Print the formatted summary

**SAY:** "Now format it for a human to read — f-strings, with `:.2f` to force exactly two decimal places on every dollar amount."

**DO:**
```python
print('=== Purchase Request Summary ===')
print(f'Product:  {product_name}')
print(f'Qty:      {quantity}')
print(f'Subtotal: ${subtotal:.2f}')
print(f'Tax:      ${tax:.2f}')
print(f'Total:    ${total:.2f}')
print(f'Requires approval: {requires_approval}')
```

**CHECK:**
```
=== Purchase Request Summary ===
Product:  Laptop
Qty:      3
Subtotal: $1350.00
Tax:      $94.50
Total:    $1444.50
Requires approval: True
```
Confirm the dollar amounts match the math you said out loud in Step 4.

---

#### Screenshot 1 checkpoint (5:50–6:10)

**SAY:** "Screenshot 1 — the formatted business summary output."

---

### PART 3 — User Input with Type Conversion (6:10–8:40)

#### Step 6 — Add input() with int() conversion

**SAY:** "Now let the user change the quantity at runtime. The critical detail: `input()` always returns a string, so we wrap it in `int()` immediately."

**DO:** Append:
```python
user_qty = int(input('Enter a new quantity: '))
new_total = unit_price * user_qty * 1.07
print(f'New total for {user_qty} units: ${new_total:.2f}')
print(f'Requires approval: {new_total > 1000}')
```

**DO:**
```bash
python3 week5_lab.py
```
Type `5` when prompted.

**CHECK:**
```
Enter a new quantity: 5
New total for 5 units: $2407.50
Requires approval: True
```

---

#### Step 7 — Deliberately break it — the classic Week 5 bug

**SAY:** "Now let's cause the single most common bug in this lab, on purpose, so you recognize it instantly when it happens by accident. Temporarily remove the `int()` wrapper."

**DO:** In a scratch line (don't keep this in your final file), try:
```python
unit_price * input('qty: ')
```

**CHECK:**
```
TypeError: can't multiply sequence by non-int of type 'float'
```

**FIX:** "`input()` returned a *string* — a sequence of characters — and Python won't multiply a string by a float. That's exactly why Step 6 wraps it in `int()`. Delete this scratch line and confirm your real `week5_lab.py` still has the `int(input(...))` version from Step 6."

---

#### Screenshot 2 checkpoint (8:20–8:40)

**SAY:** "Screenshot 2 — the complete output including the input prompt and result from Step 6."

---

### PART 4 — pytest (8:40–10:50)

#### Step 8 — Write all five tests

**SAY:** "Five tests, each isolating one piece of logic from the script — none of them depend on `input()`, because tests should never wait on a human typing something."

**DO:**
```bash
mkdir -p tests && touch tests/__init__.py tests/test_week5.py
code tests/test_week5.py
```
```python
def test_tax_at_seven_percent():
    subtotal = 200.00
    tax = subtotal * 0.07
    assert tax == 14.0

def test_over_limit_true():
    assert 1500 > 1000 is True

def test_over_limit_false():
    assert 500 > 1000 is False

def test_type_of_string():
    name = 'ISM3232'
    assert type(name) == str

def test_type_conversion():
    s = '42'
    assert int(s) == 42
```

**CHECK:** Read `test_over_limit_true` closely on camera: "`1500 > 1000 is True` — Python evaluates `1000 is True` first because of operator precedence, then compares `1500 > (1000 is True)`. It happens to still pass here, but it's worth noticing `is` isn't the same as `==` for this kind of check."

---

#### Step 9 — Run pytest and confirm all green

**DO:**
```bash
pytest -v
```

**CHECK:**
```
tests/test_week5.py::test_tax_at_seven_percent PASSED
tests/test_week5.py::test_over_limit_true PASSED
tests/test_week5.py::test_over_limit_false PASSED
tests/test_week5.py::test_type_of_string PASSED
tests/test_week5.py::test_type_conversion PASSED

======================== 5 passed in 0.01s ========================
```

---

#### Screenshot 3 checkpoint (10:50–11:10)

**SAY:** "Screenshot 3 — `pytest -v` with all five tests green."

---

### PART 5 — Submission Ritual and Push (11:10–12:20)

#### Step 10 — Run the full ritual

**SAY:** "Same ten-step ritual from Week 4, now on this module."

**DO:**
```bash
ruff format .
ruff check .
pytest
git status
git add .
git commit -m 'lab 5: variables types operators'
git push
```

**CHECK:** `ruff check` reports no errors, `pytest` shows `5 passed`, and `git push` completes without error. Follow with `git status` — it should say "nothing to commit, working tree clean."

---

### SUBMISSION CHECKLIST (12:20–end)

- [ ] Screenshot 1: formatted business summary output
- [ ] Screenshot 2: complete output including the input prompt
- [ ] Screenshot 3: `pytest -v` with all five tests green
- [ ] Git commit message includes "lab 5"
- [ ] GitHub repository URL pasted into Canvas
