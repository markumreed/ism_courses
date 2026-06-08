# ISM3232 Lab W11: OOP II — Composition, Inheritance & SQL Mapping

## YouTube Metadata

**Title:** OOP II: Composition, Inheritance & SQL Mapping — Lab Walkthrough | ISM3232 Lab 11
**Description:**
Walkthrough of ISM3232 Module 11 Lab. We add the RequestManager class to models.py, wire it to BusinessRequest in main.py, complete the OOP-to-SQL mapping table in README.md, and write six new pytest tests covering both classes.

**Chapters:**
0:00 — What we're building
0:45 — RequestManager class: __init__, add, filter, total, report
4:00 — Wiring both classes together in main.py
6:00 — OOP-to-SQL mapping in README.md
7:30 — Six new pytest tests covering composition
9:00 — Stretch: TravelRequest subclass
9:30 — Submission checklist

**Applies to:** ISM3232 Module 11

**Tags:** python composition, python manager class, python OOP composition, python SQL mapping, ISM3232, USF, python inheritance, python OOP design

---

## Script

### INTRO (0:00–0:45)

Lab 11 — OOP II: Composition and the Manager Class. We add `RequestManager` to `models.py` — it owns a list of `BusinessRequest` objects and exposes add, filter, total, and report methods. Then we map the OOP design to SQL concepts. This is the pattern that every database-backed application uses at its core.

---

### REQUESTMANAGER CLASS (0:45–4:00)

Open `models.py` and add below the existing `BusinessRequest` class:

```python
class RequestManager:
    """Manages a collection of BusinessRequest instances."""

    def __init__(self):
        self.requests: list[BusinessRequest] = []

    def add_request(self, req: BusinessRequest) -> None:
        """Add a BusinessRequest to the collection."""
        self.requests.append(req)

    def list_pending(self) -> list[BusinessRequest]:
        """Return all requests with status 'Pending'."""
        return [r for r in self.requests if r.status == "Pending"]

    def get_by_status(self, status: str) -> list[BusinessRequest]:
        """Return all requests matching a given status."""
        return [r for r in self.requests if r.status == status]

    def total_amount(self) -> float:
        """Return the sum of all request amounts."""
        return sum(r.amount for r in self.requests)

    def summary_report(self) -> None:
        """Print a formatted summary of all requests."""
        print(f"\n{'ID':<5} {'Requester':<12} {'Category':<12} {'Amount':>10}  Status")
        print("-" * 55)
        for r in self.requests:
            print(f"  {r.request_id:<5} {r.requester:<12} {r.category:<12} ${r.amount:>8,.2f}  {r.status}")
        print("-" * 55)
        print(f"  TOTAL{' ':<29} ${self.total_amount():>8,.2f}")
        print(f"  Pending: {len(self.list_pending())}/{len(self.requests)}")
```

Two key design decisions here: `list_pending` is a special case of `get_by_status("Pending")` — you could implement one in terms of the other, but the explicit method is more readable.

---

### WIRING BOTH CLASSES IN MAIN.PY (4:00–6:00)

Replace `main.py` with:

```python
from models import BusinessRequest, RequestManager

mgr = RequestManager()
mgr.add_request(BusinessRequest(101, "Taylor", "Travel", 1200))
mgr.add_request(BusinessRequest(102, "Jordan", "Equipment", 450))
mgr.add_request(BusinessRequest(103, "Morgan", "Software", 3500))
mgr.add_request(BusinessRequest(104, "Riley",  "Travel", 89))

# Approve two requests
mgr.requests[0].approve()    # Taylor
mgr.requests[2].approve()    # Morgan

mgr.summary_report()

print(f"\nPending requests: {len(mgr.list_pending())}")
print(f"Total portfolio: ${mgr.total_amount():,.2f}")
```

Run: `python3 main.py`

Screenshot 1: the summary_report() output showing mixed statuses.

---

### OOP-TO-SQL MAPPING (6:00–7:30)

Create or update `README.md` with this table — fill in the right column with your own system's design:

```markdown
## OOP to SQL Mapping

| OOP concept           | SQL equivalent           | This system                   |
|-----------------------|--------------------------|-------------------------------|
| class BusinessRequest | table: requests          | requests table                |
| instance attribute    | column                   | requester, category, amount   |
| self.status           | status column w/ DEFAULT | DEFAULT 'Pending'             |
| list of instances     | all rows                 | SELECT * FROM requests        |
| total_amount()        | SELECT SUM(amount)       | SUM(amount) aggregate         |
| get_by_status()       | WHERE status = ?         | WHERE status = 'Pending'      |
```

This mapping is not just documentation — it tells you exactly what your SQL schema should look like when you build the database layer in Lab 14.

---

### SIX PYTEST TESTS (7:30–9:00)

Add to `tests/test_models.py` (keep your seven W10 tests):

```python
from models import BusinessRequest, RequestManager

def test_manager_starts_empty():
    mgr = RequestManager()
    assert len(mgr.requests) == 0

def test_add_increases_count():
    mgr = RequestManager()
    mgr.add_request(BusinessRequest(1, "A", "Travel", 500))
    assert len(mgr.requests) == 1

def test_list_pending_filters_correctly():
    mgr = RequestManager()
    req1 = BusinessRequest(1, "A", "Travel", 500)
    req2 = BusinessRequest(2, "B", "Travel", 600)
    req2.approve()
    mgr.add_request(req1)
    mgr.add_request(req2)
    assert len(mgr.list_pending()) == 1
    assert mgr.list_pending()[0].request_id == 1

def test_total_amount_correct():
    mgr = RequestManager()
    mgr.add_request(BusinessRequest(1, "A", "T", 500))
    mgr.add_request(BusinessRequest(2, "B", "T", 750))
    assert mgr.total_amount() == 1250.0

def test_get_by_status():
    mgr = RequestManager()
    req1 = BusinessRequest(1, "A", "T", 500)
    req1.approve()
    mgr.add_request(req1)
    mgr.add_request(BusinessRequest(2, "B", "T", 600))
    assert len(mgr.get_by_status("Approved")) == 1
    assert len(mgr.get_by_status("Pending")) == 1

def test_independent_managers():
    mgr1 = RequestManager()
    mgr2 = RequestManager()
    mgr1.add_request(BusinessRequest(1, "A", "T", 500))
    assert len(mgr2.requests) == 0
```

Run: `pytest -v` — all 13 tests (7 from W10 + 6 new) must pass.

Screenshot 2: `pytest -v` with all tests green.

---

### STRETCH: TRAVELREQUEST SUBCLASS (9:00–9:30)

```python
# Add at the bottom of models.py
class TravelRequest(BusinessRequest):
    """A travel request with a lower review threshold."""

    def requires_review(self) -> bool:
        """Travel requests require review above $500 (not $1000)."""
        return self.amount > 500
```

Write a test:
```python
def test_travel_request_lower_threshold():
    req = TravelRequest(99, "Alex", "Travel", 750)
    assert req.requires_review() is True   # $750 > $500 for travel

def test_regular_request_unchanged():
    req = BusinessRequest(98, "Alex", "Software", 750)
    assert req.requires_review() is False  # $750 < $1000 for regular
```

---

### SUBMISSION CHECKLIST (9:30–11:00)

- `models.py` with both `BusinessRequest` and `RequestManager` classes
- `main.py` using the manager: adds requests, calls summary_report()
- `README.md` with OOP-to-SQL mapping table filled in
- All tests passing (7 from W10 + 6 new = 13 minimum)
- Screenshot 1: summary_report() output
- Screenshot 2: `pytest -v` all green
- Commit includes "lab 11", GitHub URL to Canvas
