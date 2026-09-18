# ISM3232 Lab W06: Conditionals, Loops & Dictionaries

## YouTube Metadata

**Title:** Conditionals, Loops & Dictionaries — Full Lab Walkthrough | ISM3232 Lab 06
**Description:**
Step-by-step, test-as-you-go walkthrough of ISM3232 Module 6 Lab. Build a business record processor using the list-of-dicts pattern: store five records, loop and filter with conditionals, apply two business rules, write a formatted summary to both terminal and file, write five pytest tests, then run the ritual and push — every command run and verified one at a time.

Course page: https://markumreed.github.io/ism3232/docs/week06_lab.html

**Chapters:**
0:00 — What this lab covers
0:40 — Step 1: activate the venv, create week6_lab.py
1:10 — Step 2: define five records as a list of dicts
2:20 — Step 3: loop and print only pending records
3:20 — Step 4: two business rules — LIMIT and HIGH thresholds
5:00 — Step 5: build the formatted summary and write to file
6:40 — Step 6: run and verify the file was written
7:30 — Screenshot 1 checkpoint
7:50 — Step 7: write all five pytest tests
9:40 — Step 8: run pytest -v and confirm all green
10:10 — Screenshot 2 checkpoint
10:30 — Step 9: the ritual and push
11:20 — Submission checklist

**Applies to:** ISM3232 Module 06

**Tags:** python list of dicts, python conditionals loops tutorial, python business logic, python file io, ISM3232, USF, python data processing tutorial

---

## How to Use This Script

**SAY** it, **DO** it, **CHECK** the exact output, **FIX** it if it doesn't match — then move to the next step.

---

## Script

### INTRO (0:00–0:40)

**SAY:** "Lab 6 — conditionals, loops, and dictionaries. Today's pattern — a list of dictionaries — is the single most common shape of business data in this course and in real applications: rows of records, each one a dict of named fields."

---

### PART 1 — Records and Loop (0:40–3:20)

#### Step 1 — Activate and create the file

**DO:**
```bash
cd ~/ism3232/module04_programming
source .venv/bin/activate
touch week6_lab.py && code week6_lab.py
```

**CHECK:** Prompt shows `(.venv)`; `ls` shows the new empty `week6_lab.py` alongside last week's files.

---

#### Step 2 — Define five records

**SAY:** "Five records, each a dict with the same five keys — `id`, `name`, `category`, `amount`, `status`. Same shape every time is what makes looping over them possible."

**DO:**
```python
# week6_lab.py
# Author: [Your Name]

records = [
    {'id': 1, 'name': 'Taylor', 'category': 'Travel',    'amount': 1200, 'status': 'Pending'},
    {'id': 2, 'name': 'Jordan', 'category': 'Equipment', 'amount': 450,  'status': 'Pending'},
    {'id': 3, 'name': 'Morgan', 'category': 'Software',  'amount': 3500, 'status': 'Approved'},
    {'id': 4, 'name': 'Riley',  'category': 'Travel',    'amount': 89,   'status': 'Pending'},
    {'id': 5, 'name': 'Alex',   'category': 'Equipment', 'amount': 2200, 'status': 'Pending'},
]
```

**CHECK:** Count the records out loud: "Five dicts in the list, each with exactly the same five keys — that consistency is what lets every later loop assume `rec['amount']` always exists."

---

#### Step 3 — Loop and filter to pending only

**SAY:** "A `for` loop over the list, with an `if` inside it to filter to just the pending records."

**DO:**
```python
for rec in records:
    if rec['status'] == 'Pending':
        print(f"{rec['name']}: ${rec['amount']:,.2f}")
```
```bash
python3 week6_lab.py
```

**CHECK:**
```
Taylor: $1,200.00
Jordan: $450.00
Riley: $89.00
Alex: $2,200.00
```
Four names print — Morgan is missing because Morgan's status is `'Approved'`, not `'Pending'`. Confirm that's exactly what the filter excluded.

---

### PART 2 — Two Business Rules (3:20–5:00)

#### Step 4 — Replace the loop with two threshold rules

**SAY:** "Now the loop does three things at once: accumulates a running total, and sorts pending records into two separate flagged lists based on two different dollar thresholds."

**DO:** Replace the previous loop with:
```python
LIMIT = 1000
HIGH  = 2000

total = 0
flagged = []
high_value = []

for rec in records:
    if rec['status'] == 'Pending':
        total += rec['amount']
        if rec['amount'] > LIMIT:
            flagged.append(rec)
        if rec['amount'] > HIGH:
            high_value.append(rec)
```
```bash
python3 week6_lab.py
```

**CHECK:** No output yet (we haven't printed anything from these variables) — but before moving on, trace it by hand on camera: "Pending records are Taylor 1200, Jordan 450, Riley 89, Alex 2200. Total should be 3,939. Over `LIMIT` (1000): Taylor and Alex — 2 flagged. Over `HIGH` (2000): only Alex — 1 high-value." You'll confirm these numbers in the next step's printed output.

---

### PART 3 — Formatted Summary and File Output (5:00–7:30)

#### Step 5 — Build the summary and write it to a file

**SAY:** "Print the summary to the terminal *and* save the same lines to a file — a pattern you'll reuse constantly once we get to Streamlit later in the course."

**DO:**
```python
import os
os.makedirs('data', exist_ok=True)

lines = [
    f'Pending total:   ${total:,.2f}',
    f'Needs review:    {len(flagged)}',
    f'High-value:      {len(high_value)}',
]
for line in lines:
    print(line)

with open('data/week6_summary.txt', 'w') as f:
    f.write('\n'.join(lines) + '\n')

print('\nRecords needing review:')
for r in flagged:
    print(f"  ID {r['id']}: {r['name']} - ${r['amount']:,.2f}")
```

**CHECK:** Read what `os.makedirs('data', exist_ok=True)` does before running: "Creates a `data/` folder if it doesn't already exist, and `exist_ok=True` means it won't crash if I run this script twice."

---

#### Step 6 — Run and verify the file was written

**DO:**
```bash
python3 week6_lab.py
```

**CHECK:**
```
Pending total:   $3,939.00
Needs review:    2
High-value:      1

Records needing review:
  ID 1: Taylor - $1,200.00
  ID 5: Alex - $2,200.00
```
Confirm this matches the hand-traced numbers from Step 4 exactly: total 3,939, 2 flagged, 1 high-value.

Now confirm the file itself exists with real content:
```bash
cat data/week6_summary.txt
```

**CHECK:**
```
Pending total:   $3,939.00
Needs review:    2
High-value:      1
```

**FIX:** If `cat` shows "No such file or directory," confirm you're running `python3 week6_lab.py` from `module04_programming`, not from inside `data/` — relative paths are relative to *where you run the script from*, not where the script file lives.

---

#### Screenshot 1 checkpoint (7:30–7:50)

**SAY:** "Screenshot 1 — the complete terminal output of `week6_lab.py`."

---

### PART 4 — pytest (7:50–10:10)

#### Step 7 — Write all five tests

**SAY:** "Five tests, each isolating one piece of the logic — accumulation, filtering by amount, filtering by status, dict key access, and list length — all with small inline data, not the real `records` list."

**DO:**
```bash
touch tests/test_week6.py
code tests/test_week6.py
```
```python
def test_accumulator():
    amounts = [500, 1500, 200]
    total = sum(a for a in amounts)
    assert total == 2200

def test_flag_filter():
    records = [{'amount': 500}, {'amount': 1500}, {'amount': 800}]
    flagged = [r for r in records if r['amount'] > 1000]
    assert len(flagged) == 1

def test_status_filter():
    records = [{'amount': 500, 'status': 'Pending'}, {'amount': 1000, 'status': 'Approved'}]
    pending = [r for r in records if r['status'] == 'Pending']
    assert len(pending) == 1

def test_dict_key_access():
    rec = {'id': 1, 'amount': 750, 'status': 'Pending'}
    assert rec['amount'] == 750

def test_list_of_dicts_length():
    data = [{'x': 1}, {'x': 2}, {'x': 3}]
    assert len(data) == 3
```

**CHECK:** Point out `test_flag_filter` and `test_status_filter` use *list comprehensions* — the same filtering logic as the `if rec['amount'] > LIMIT` check in the real script, just written as a one-line expression instead of a loop with `.append()`.

---

#### Step 8 — Run pytest and confirm all green

**DO:**
```bash
pytest -v
```

**CHECK:**
```
tests/test_week6.py::test_accumulator PASSED
tests/test_week6.py::test_flag_filter PASSED
tests/test_week6.py::test_status_filter PASSED
tests/test_week6.py::test_dict_key_access PASSED
tests/test_week6.py::test_list_of_dicts_length PASSED

======================== 5 passed in 0.01s ========================
```

---

#### Screenshot 2 checkpoint (10:10–10:30)

**SAY:** "Screenshot 2 — `pytest -v` with all five tests green."

---

### PART 5 — Ritual and Push (10:30–11:20)

#### Step 9 — Run the ritual

**DO:**
```bash
ruff format . && ruff check . && pytest
git add . && git commit -m 'lab 6: conditionals loops dicts' && git push
```

**CHECK:** `ruff check` reports no errors, `pytest` shows `5 passed`, and the push completes. Commit message includes "lab 6" exactly, since that's what's graded.

---

### SUBMISSION CHECKLIST (11:20–end)

- [ ] Screenshot 1: complete terminal output of `week6_lab.py`
- [ ] Screenshot 2: `pytest -v` with all five tests green
- [ ] Git commit message includes "lab 6"
- [ ] GitHub repository URL pasted into Canvas
