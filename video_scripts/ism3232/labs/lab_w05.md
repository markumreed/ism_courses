# ISM3232 Lab W05: Variables, Data Types & Operators

## YouTube Metadata

**Title:** Variables, Data Types & Operators — Lab Walkthrough | ISM3232 Lab 05
**Description:**
Walkthrough of ISM3232 Module 5 Lab. We write a business data script covering all four Python data types, arithmetic and comparison operators, f-string formatting, and user input — then write five pytest tests and run the full submission ritual.

**Chapters:**
0:00 — What we're building
0:45 — Four data types and business operators
3:00 — F-string formatting with two decimal places
5:00 — User input with type conversion
6:30 — Writing five pytest tests
8:30 — Submission ritual and checklist

**Applies to:** ISM3232 Module 05

**Tags:** python variables data types, python operators, python f-strings, pytest basics, ISM3232, USF, python business script

---

## Script

### INTRO (0:00–0:45)

Lab 5 — Variables, Data Types, and Operators. This is the first Python coding lab in ISM3232. We write a business data script, add user input, format output professionally, and finish with five passing pytest tests and a clean ritual. Save as `module05_python/week5_lab.py`.

---

### FOUR DATA TYPES AND OPERATORS (0:45–3:00)

```python
# week5_lab.py

# Four data types
company_name  = "Acme Solutions"     # str
employee_count = 142                 # int
revenue        = 3_850_000.00        # float  (underscores for readability)
is_profitable  = True                # bool

# Arithmetic operators
annual_revenue   = revenue
monthly_avg      = annual_revenue / 12
quarterly        = annual_revenue / 4
revenue_per_head = annual_revenue / employee_count

# Comparison operators
is_large_company   = employee_count > 100    # True
exceeds_target     = revenue > 4_000_000     # False

# Logical operators
qualifies_for_tier = is_profitable and is_large_company   # True
```

---

### F-STRING FORMATTING (3:00–5:00)

```python
print(f"Company:           {company_name}")
print(f"Employees:         {employee_count:,}")
print(f"Annual Revenue:    ${annual_revenue:,.2f}")
print(f"Monthly Average:   ${monthly_avg:,.2f}")
print(f"Revenue/Employee:  ${revenue_per_head:,.2f}")
print(f"Profitable:        {is_profitable}")
print(f"Qualifies for tier: {qualifies_for_tier}")
```

Screenshot 1: this formatted output in the terminal.

`:,` adds thousands separator. `:.2f` rounds to two decimal places. `{:,.2f}` does both — standard for financial figures.

---

### USER INPUT (5:00–6:30)

```python
# Get a budget from the user
budget = float(input("\nEnter Q1 budget: $"))
variance = revenue / 4 - budget
pct_variance = variance / budget

print(f"\nQ1 Revenue:   ${revenue/4:,.2f}")
print(f"Q1 Budget:    ${budget:,.2f}")
print(f"Variance:     ${variance:,.2f}")
print(f"Variance %:   {pct_variance:.1%}")
```

Screenshot 2: output including the input prompt.

---

### FIVE PYTEST TESTS (6:30–8:30)

Create `module05_python/tests/test_week5.py`:

```python
def calculate_monthly_avg(annual_revenue):
    return annual_revenue / 12

def calculate_revenue_per_head(revenue, headcount):
    return revenue / headcount

def qualifies_for_tier(is_profitable, is_large):
    return is_profitable and is_large


def test_monthly_avg():
    assert round(calculate_monthly_avg(1_200_000), 2) == 100_000.00

def test_revenue_per_head():
    assert round(calculate_revenue_per_head(1_000_000, 100), 2) == 10_000.00

def test_tier_both_true():
    assert qualifies_for_tier(True, True) is True

def test_tier_one_false():
    assert qualifies_for_tier(True, False) is False

def test_tier_both_false():
    assert qualifies_for_tier(False, False) is False
```

Run with `python3 -m pytest -v`. All five green.

Screenshot 3: `pytest -v` with all five tests green.

---

### SUBMISSION RITUAL AND CHECKLIST (8:30–10:00)

Run the full ritual before pushing.

- Screenshot 1: formatted business summary output
- Screenshot 2: output including input prompt
- Screenshot 3: `pytest -v` all five green
- Commit message includes "lab 5"
- GitHub URL pasted to Canvas
