# ISM3232 Lab W10: OOP I — Classes & Objects

## YouTube Metadata

**Title:** OOP I: Classes & Objects — Lab Walkthrough | ISM3232 Lab 10
**Description:**
Walkthrough of ISM3232 Module 10 Lab. We build the BusinessRequest class with __init__, four methods, and __repr__, create three independent instances, verify independence, and write seven pytest tests including the boundary case at exactly $1000.

Course page: https://markumreed.github.io/ism3232/docs/week10_lab.html

**Chapters:**
0:00 — What we're building
0:45 — The BusinessRequest class: __init__ and attributes
3:00 — Four methods: approve, reject, requires_review, __repr__
5:30 — Creating three instances and verifying independence
7:00 — Seven pytest tests including the $1000 boundary
8:30 — Submission checklist

**Applies to:** ISM3232 Module 10

**Tags:** python OOP classes, python __init__, python instance methods, python OOP tutorial, ISM3232, USF, python business class, python object oriented

---

## Script

### INTRO (0:00–0:45)

Lab 10 — OOP I: Classes and Objects. We build the `BusinessRequest` class — the foundation of every remaining lab and the capstone. By the end we'll have a class with four methods, three independent instances, and seven passing tests. Save as `module10_oop1/models.py`.

---

### __INIT__ AND ATTRIBUTES (0:45–3:00)

```python
# models.py


class BusinessRequest:
    """A purchase or travel request requiring approval workflow."""

    def __init__(self, request_id: int, requester: str, category: str, amount: float):
        self.request_id = request_id
        self.requester  = requester
        self.category   = category
        self.amount     = amount
        self.status     = "Pending"   # default — always starts Pending
```

Four attributes from parameters, one default. The default status is important — the tests will check it explicitly.

---

### FOUR METHODS (3:00–5:30)

```python
    def approve(self) -> None:
        """Set status to Approved."""
        self.status = "Approved"

    def reject(self) -> None:
        """Set status to Rejected."""
        self.status = "Rejected"

    def requires_review(self) -> bool:
        """Return True if amount exceeds $1000 (manager review required)."""
        return self.amount > 1000.0

    def __repr__(self) -> str:
        """Return a readable string representation."""
        return (
            f"BusinessRequest({self.request_id}, {self.requester}, "
            f"${self.amount:,.2f}, {self.status})"
        )
```

`__repr__` is what prints when you call `print(obj)` or inspect the object in the shell. Always implement it — it makes debugging dramatically easier.

---

### THREE INSTANCES AND INDEPENDENCE (5:30–7:00)

Create `module10_oop1/main.py`:

```python
from models import BusinessRequest

req_101 = BusinessRequest(101, "Taylor", "Travel", 1200.00)
req_102 = BusinessRequest(102, "Jordan", "Equipment", 450.00)
req_103 = BusinessRequest(103, "Morgan", "Software", 3500.00)

# Verify initial state
print(req_101)   # status: Pending
print(req_102)   # status: Pending

# Change req_101 — must NOT affect req_102
req_101.approve()
print(f"req_101: {req_101.status}")   # Approved
print(f"req_102: {req_102.status}")   # Pending — unchanged

# requires_review
print(req_101.requires_review())   # True — $1200 > $1000
print(req_102.requires_review())   # False — $450 not > $1000
print(req_103.requires_review())   # True — $3500 > $1000
```

Screenshot 1: this full output.

---

### SEVEN PYTEST TESTS (7:00–8:30)

Create `module10_oop1/tests/test_models.py`:

```python
import pytest
from models import BusinessRequest

@pytest.fixture
def sample_request():
    return BusinessRequest(101, "Taylor", "Travel", 1200.00)

def test_default_status_is_pending(sample_request):
    assert sample_request.status == "Pending"

def test_approve_changes_status(sample_request):
    sample_request.approve()
    assert sample_request.status == "Approved"

def test_reject_changes_status(sample_request):
    sample_request.reject()
    assert sample_request.status == "Rejected"

def test_requires_review_over_limit(sample_request):
    assert sample_request.requires_review() is True

def test_requires_review_under_limit():
    req = BusinessRequest(102, "Jordan", "Equipment", 450.00)
    assert req.requires_review() is False

def test_requires_review_at_boundary():
    # $1000 exactly — does NOT require review (strictly greater than)
    req = BusinessRequest(103, "Casey", "Training", 1000.00)
    assert req.requires_review() is False

def test_instances_are_independent():
    req1 = BusinessRequest(7, "A", "Travel", 500.00)
    req2 = BusinessRequest(8, "B", "Travel", 500.00)
    req1.approve()
    assert req2.status == "Pending"   # req2 unchanged
```

Screenshot 2: `pytest -v` all seven green.

---

### SUBMISSION CHECKLIST (8:30–10:00)

- `models.py` with `BusinessRequest` class: `__init__`, four methods, `__repr__`
- `main.py` with three instances, method calls, independence verified
- Seven tests: default status, approve, reject, boundary at $1000, independence
- `test_requires_review_exactly_at_threshold` passes
- Ritual run, commit includes "lab 10", GitHub URL to Canvas
