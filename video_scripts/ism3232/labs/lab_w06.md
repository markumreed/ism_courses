# ISM3232 Lab W06: Conditionals, Loops & Dictionaries

## YouTube Metadata

**Title:** Conditionals, Loops & Dictionaries — Lab Walkthrough | ISM3232 Lab 06
**Description:**
Walkthrough of ISM3232 Module 6 Lab. We build a business record processor: a list of five dicts, two business rules with conditionals, a loop accumulating totals, formatted report output written to a file, and five pytest tests.

**Chapters:**
0:00 — What we're building
0:45 — List of five business record dicts
2:30 — Two business rules with conditionals
4:30 — Loop with accumulator and formatted output
6:30 — Saving the summary to a file
7:30 — Five pytest tests
8:30 — Submission checklist

**Applies to:** ISM3232 Module 06

**Tags:** python list of dicts, python conditionals loops, python accumulator, python write file, ISM3232, USF, python business record processor

---

## Script

### INTRO (0:00–0:45)

Lab 6 — Conditionals, Loops, and Dictionaries. We build a business record processor: five purchase requests as a list of dicts, two approval rules, a loop that applies those rules, and a report saved to disk. This is the full pattern behind every real data pipeline. Save as `module06_loops/week6_lab.py`.

---

### LIST OF FIVE DICTS (0:45–2:30)

```python
# week6_lab.py

requests = [
    {"name": "Taylor",  "category": "Travel",    "amount": 1200.00},
    {"name": "Jordan",  "category": "Software",  "amount": 450.00},
    {"name": "Morgan",  "category": "Equipment", "amount": 3500.00},
    {"name": "Casey",   "category": "Travel",    "amount": 89.00},
    {"name": "Riley",   "category": "Training",  "amount": 2100.00},
]
```

At least five records. Mix categories and amounts so both business rules fire.

---

### TWO BUSINESS RULES (2:30–4:30)

```python
# Business Rule 1: requests over $1000 require manager approval
# Business Rule 2: Travel category always requires approval

APPROVAL_THRESHOLD = 1000.00
ALWAYS_APPROVE_CATEGORIES = {"Equipment"}   # auto-approve hardware

def get_status(record):
    if record["amount"] > APPROVAL_THRESHOLD:
        return "Needs Approval"
    elif record["category"] == "Travel" and record["amount"] > 500:
        return "Needs Approval"
    elif record["category"] in ALWAYS_APPROVE_CATEGORIES:
        return "Pre-Approved"
    else:
        return "Auto-Approved"
```

Two distinct conditions that produce different statuses. The exact rules don't matter — what matters is that you have at least two with `elif`.

---

### LOOP WITH ACCUMULATOR AND FORMATTED OUTPUT (4:30–6:30)

```python
total_amount   = 0
approved_count = 0

print(f"\n{'Name':<10} {'Category':<12} {'Amount':>10}  Status")
print("-" * 52)

for r in requests:
    status = get_status(r)
    total_amount += r["amount"]
    if "Approved" in status:
        approved_count += 1
    print(f"  {r['name']:<10} {r['category']:<12} ${r['amount']:>8,.2f}  {status}")

print("-" * 52)
print(f"  {'TOTAL':<22} ${total_amount:>8,.2f}")
print(f"  Approved: {approved_count}/{len(requests)}")
```

Screenshot 1: this terminal output.

---

### SAVING TO A FILE (6:30–7:30)

```python
with open("summary_report.txt", "w") as f:
    f.write("Purchase Request Summary\n")
    f.write("=" * 40 + "\n")
    for r in requests:
        status = get_status(r)
        f.write(f"{r['name']:<10} ${r['amount']:>8,.2f}  {status}\n")
    f.write(f"\nTotal: ${total_amount:,.2f}\n")

print("Report saved to summary_report.txt")
```

---

### FIVE PYTEST TESTS (7:30–8:30)

```python
# tests/test_week6.py
import sys; sys.path.insert(0, "..")
from week6_lab import get_status

def test_high_amount_needs_approval():
    assert get_status({"name": "X", "category": "Software", "amount": 1500}) == "Needs Approval"

def test_low_amount_auto_approved():
    assert get_status({"name": "X", "category": "Software", "amount": 200}) == "Auto-Approved"

def test_equipment_pre_approved():
    assert get_status({"name": "X", "category": "Equipment", "amount": 800}) == "Pre-Approved"

def test_boundary_at_threshold():
    assert get_status({"name": "X", "category": "Software", "amount": 1000}) == "Auto-Approved"

def test_travel_over_500():
    assert get_status({"name": "X", "category": "Travel", "amount": 600}) == "Needs Approval"
```

Screenshot 2: `pytest -v` all five green.

---

### SUBMISSION CHECKLIST (8:30–10:00)

- List of at least five dicts
- Two distinct business rules with at least one `elif`
- Accumulator for total and count
- Formatted table output (column aligned)
- Summary saved to a `.txt` file
- Five pytest tests all passing
- Ritual run, GitHub commit includes "lab 6", URL to Canvas
