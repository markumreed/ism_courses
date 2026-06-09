# Video 26: Testing with pytest

## YouTube Metadata

**Title:** Python Testing with pytest — Write, Run & Organize Tests | ISM3232
**Description:**
pytest is the standard Python testing framework. In this video you'll write tests for a business calculation module, run them from the terminal, understand the six required test types for ISM3232 assignments, and organize your project with proper module structure. Tests aren't extra work — they're how professionals verify correctness and catch regressions.

Course page: https://markumreed.github.io/ism3232/docs/week07_lecture.html

**Chapters:**
0:00 — Why tests?
1:30 — Project structure for testable code
3:00 — Writing your first test
5:30 — Running pytest
7:00 — The 6 required test types
11:00 — Testing edge cases and exceptions
13:30 — Test organization with fixtures
15:00 — Recap

**Applies to:** ISM3232 Module 7

**Tags:** pytest tutorial, python testing, python pytest, unit testing python, pytest fixtures, python test functions, ISM3232, python professional, test driven development, pytest edge cases

---

## Script

### INTRO (0:00–1:30)

Here's what happens to developers who don't write tests: they change one function, break three others, ship broken code, and spend hours debugging in production. Here's what happens to developers who do write tests: they change one function, run `pytest`, see which tests failed, know exactly what broke, and fix it in 10 minutes.

Tests are not extra work. They are the thing that makes refactoring safe, collaboration possible, and debugging fast. In ISM3232, every assignment from Module 7 forward requires tests. Let's build the habit right.

---

### PROJECT STRUCTURE (1:30–3:00)

Tests work best when your business logic is in its own module — separate from the script that runs it.

```
module07_functions/
├── .venv/
├── calculations.py      # your business logic functions
├── main.py              # imports from calculations.py and uses them
├── tests/
│   ├── __init__.py      # empty file — marks tests/ as a package
│   └── test_calculations.py
├── requirements.txt
└── .gitignore
```

The `__init__.py` file makes Python treat the `tests/` directory as a package. Without it, pytest can't always find your modules.

`calculations.py` — the module under test:

```python
# calculations.py

def calculate_tax(amount: float, rate: float) -> float:
    """Calculate tax on an amount at a given rate."""
    if amount < 0:
        raise ValueError("Amount cannot be negative.")
    if not 0 <= rate <= 1:
        raise ValueError("Rate must be between 0 and 1.")
    return round(amount * rate, 2)

def apply_discount(subtotal: float, rate: float) -> float:
    """Apply a discount to a subtotal. Returns discounted amount."""
    if subtotal < 0:
        raise ValueError("Subtotal cannot be negative.")
    if not 0 <= rate <= 1:
        raise ValueError("Discount rate must be between 0 and 1.")
    return round(subtotal * (1 - rate), 2)

def get_discount_rate(subtotal: float) -> float:
    """Determine discount rate based on order size."""
    if subtotal > 250:
        return 0.15
    elif subtotal > 100:
        return 0.10
    return 0.0

def process_order(subtotal: float, tax_rate: float = 0.0875) -> tuple:
    """Return (discount_rate, after_discount, tax, total)."""
    rate       = get_discount_rate(subtotal)
    discounted = apply_discount(subtotal, rate)
    tax        = calculate_tax(discounted, tax_rate)
    total      = round(discounted + tax, 2)
    return rate, discounted, tax, total
```

---

### FIRST TEST (3:00–5:30)

```python
# tests/test_calculations.py

import pytest
from calculations import calculate_tax, apply_discount, get_discount_rate, process_order

def test_calculate_tax_basic():
    """Standard tax calculation."""
    assert calculate_tax(100.00, 0.08) == 8.0

def test_calculate_tax_rounding():
    """Result rounded to 2 decimal places."""
    assert calculate_tax(33.33, 0.10) == 3.33

def test_apply_discount_ten_percent():
    """10% discount on $200."""
    assert apply_discount(200.00, 0.10) == 180.00
```

Test functions must start with `test_`. The `assert` statement checks that the expression is True — if it isn't, the test fails.

---

### RUNNING pytest (5:30–7:00)

From the project root (with venv active):

```bash
pytest -v
```

Output:
```
========================= test session starts ==========================
platform darwin -- Python 3.11.5
collected 3 items

tests/test_calculations.py::test_calculate_tax_basic     PASSED  [ 33%]
tests/test_calculations.py::test_calculate_tax_rounding  PASSED  [ 67%]
tests/test_calculations.py::test_apply_discount_ten_percent PASSED [100%]

========================== 3 passed in 0.05s ===========================
```

Now break a function deliberately:

```python
# In calculations.py, change:
return round(amount * rate, 2)
# to:
return amount * rate * 10   # bug!
```

Run pytest again:
```
FAILED tests/test_calculations.py::test_calculate_tax_basic
AssertionError: assert 80.0 == 8.0
```

pytest tells you exactly which test failed, the actual value, and the expected value. Fix the bug, run again.

---

### THE 6 REQUIRED TEST TYPES (7:00–11:00)

ISM3232 assignments require six categories of tests. Here they are for `calculate_tax`:

```python
# 1. HAPPY PATH — typical valid inputs
def test_calculate_tax_happy_path():
    assert calculate_tax(100.00, 0.0875) == 8.75
    assert calculate_tax(50.00,  0.06)   == 3.0

# 2. BOUNDARY VALUES — at the edges of valid ranges
def test_calculate_tax_boundaries():
    assert calculate_tax(0.0,   0.0)   == 0.0    # zero amount, zero rate
    assert calculate_tax(0.01,  0.0)   == 0.0    # minimum positive amount
    assert calculate_tax(100.0, 1.0)   == 100.0  # 100% rate (edge)

# 3. ROUNDING — correct decimal precision
def test_calculate_tax_rounding():
    assert calculate_tax(33.33, 0.10)  == 3.33
    assert calculate_tax(19.99, 0.0875) == 1.75

# 4. TYPE VALIDATION — correct return type
def test_calculate_tax_returns_float():
    result = calculate_tax(100, 0.08)
    assert isinstance(result, float)

# 5. EDGE CASES — unusual but valid inputs
def test_calculate_tax_edge_cases():
    assert calculate_tax(0.01, 0.999) == 0.01   # tiny amount, near-100% rate
    assert calculate_tax(9999.99, 0.0) == 0.0    # large amount, zero rate

# 6. ERROR CASES — invalid inputs raise correct exceptions
def test_calculate_tax_negative_amount():
    with pytest.raises(ValueError):
        calculate_tax(-100, 0.08)

def test_calculate_tax_rate_out_of_range():
    with pytest.raises(ValueError):
        calculate_tax(100, 1.5)

    with pytest.raises(ValueError):
        calculate_tax(100, -0.1)
```

---

### TESTING EXCEPTIONS (11:00–13:30)

`pytest.raises()` is a context manager that asserts an exception was raised:

```python
def test_apply_discount_negative_subtotal():
    with pytest.raises(ValueError):
        apply_discount(-50, 0.10)

def test_apply_discount_rate_over_one():
    with pytest.raises(ValueError) as exc_info:
        apply_discount(100, 1.5)
    assert "rate must be between" in str(exc_info.value).lower()
```

The `exc_info` captures the exception — you can check the message too.

Testing the full pipeline:
```python
def test_process_order_high_value():
    """Orders over $250 get 15% discount."""
    rate, discounted, tax, total = process_order(300.00)
    assert rate       == 0.15
    assert discounted == 255.00
    assert tax        == round(255.00 * 0.0875, 2)
    assert total      == round(discounted + tax, 2)
```

---

### FIXTURES (13:30–15:00)

A fixture provides shared test data. Define with `@pytest.fixture`, use by passing the name as a parameter to test functions.

```python
@pytest.fixture
def sample_orders():
    return [
        {"subtotal": 50.00,  "expected_rate": 0.00},
        {"subtotal": 150.00, "expected_rate": 0.10},
        {"subtotal": 300.00, "expected_rate": 0.15},
    ]

def test_discount_tiers(sample_orders):
    for order in sample_orders:
        rate = get_discount_rate(order["subtotal"])
        assert rate == order["expected_rate"], \
            f"Failed for subtotal={order['subtotal']}: got {rate}, expected {order['expected_rate']}"
```

Fixtures avoid copy-pasting test data. Define once, reuse in multiple tests.

---

### RECAP (15:00–18:00)

- Test files: `tests/test_*.py`; test functions: `def test_*():`
- `assert expression` — fails the test if expression is False
- `pytest -v` — run all tests with verbose output
- The 6 types: happy path, boundary, rounding, type, edge case, error
- `pytest.raises(ExceptionType)` — assert an exception is raised
- `@pytest.fixture` — shared test data, set up once, used by many tests
- Run `pytest` before every submission — all tests must pass

Tests are not optional. They are how you know your code is correct.
