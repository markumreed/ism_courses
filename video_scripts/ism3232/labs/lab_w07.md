# ISM3232 Lab W07: Functions, Modules & pytest

## YouTube Metadata

**Title:** Functions, Modules & pytest — Lab Walkthrough | ISM3232 Lab 07
**Description:**
Walkthrough of ISM3232 Module 7 Lab. We write four business functions in a separate module with docstrings and type hints, import them in main.py, and write eight pytest tests including boundary cases.

**Chapters:**
0:00 — What we're building
0:45 — Four functions in business_rules.py with type hints
4:00 — Importing and calling them in main.py
5:30 — Eight pytest tests: happy path and boundary cases
8:00 — Submission checklist

**Applies to:** ISM3232 Module 07

**Tags:** python functions modules, python type hints, pytest boundary testing, python import module, ISM3232, USF, python docstrings, python business functions

---

## Script

### INTRO (0:00–0:45)

Lab 7 — Functions, Modules, and pytest. We write four clean business functions in `business_rules.py`, import them into `main.py`, then write eight tests — four happy-path tests and four boundary cases. The boundary cases are what separate good tests from obvious ones.

---

### FOUR FUNCTIONS IN BUSINESS_RULES.PY (0:45–4:00)

Create `module07_functions/business_rules.py`:

```python
# business_rules.py


def calculate_total(price: float, quantity: int) -> float:
    """Return the total cost for a line item.

    Args:
        price: Unit price (must be non-negative)
        quantity: Number of units (must be positive)
    Returns:
        Total cost as a float
    """
    return price * quantity


def apply_discount(total: float, rate: float) -> float:
    """Apply a discount rate and return the discounted price.

    Args:
        total: Original total
        rate: Discount rate between 0.0 and 1.0
    Returns:
        Discounted price
    """
    return total * (1 - rate)


def requires_approval(amount: float, threshold: float = 1000.0) -> bool:
    """Return True if the amount exceeds the approval threshold.

    Args:
        amount: Transaction amount
        threshold: Approval threshold (default $1000)
    Returns:
        True if amount > threshold
    """
    return amount > threshold


def format_currency(amount: float, label: str = "") -> str:
    """Return a formatted currency string with optional label.

    Args:
        amount: Dollar amount
        label: Optional prefix label
    Returns:
        Formatted string like 'Total: $1,234.56'
    """
    prefix = f"{label}: " if label else ""
    return f"{prefix}${amount:,.2f}"
```

---

### MAIN.PY (4:00–5:30)

Create `module07_functions/main.py`:

```python
from business_rules import (
    calculate_total,
    apply_discount,
    requires_approval,
    format_currency,
)

price    = 299.99
quantity = 5
discount = 0.15

total      = calculate_total(price, quantity)
discounted = apply_discount(total, discount)
approval   = requires_approval(discounted)

print(format_currency(total, "Subtotal"))
print(format_currency(discounted, "After discount"))
print(f"Requires approval: {approval}")
```

Screenshot 1: `main.py` output showing all four function results.

---

### EIGHT PYTEST TESTS (5:30–8:00)

Create `module07_functions/tests/test_business_rules.py`:

```python
from business_rules import (
    calculate_total, apply_discount, requires_approval, format_currency
)

# Happy path
def test_calculate_total_basic():
    assert calculate_total(10.0, 5) == 50.0

def test_apply_discount_ten_percent():
    assert apply_discount(100.0, 0.10) == 90.0

def test_requires_approval_above_threshold():
    assert requires_approval(1500.0) is True

def test_format_currency_with_label():
    assert format_currency(1234.56, "Total") == "Total: $1,234.56"

# Boundary cases
def test_calculate_total_zero_quantity():
    assert calculate_total(99.99, 0) == 0.0

def test_apply_discount_zero_rate():
    assert apply_discount(200.0, 0.0) == 200.0

def test_requires_approval_exactly_at_threshold():
    # $1000 exactly does NOT require approval — must be strictly greater
    assert requires_approval(1000.0) is False

def test_requires_approval_one_cent_over():
    assert requires_approval(1000.01) is True
```

The last two are the important ones. `requires_approval(1000.0)` should be `False` because the condition is `>`, not `>=`. Boundary tests catch off-by-one errors that happy-path tests miss.

Screenshot 2: `pytest -v` all eight green.

---

### SUBMISSION CHECKLIST (8:00–10:00)

- `business_rules.py` with four functions, type hints, docstrings
- `main.py` importing and calling all four, showing output
- Eight tests: four happy path + four boundary
- `test_requires_approval_exactly_at_threshold` specifically tests the edge
- Ritual run, commit includes "lab 7", GitHub URL to Canvas
