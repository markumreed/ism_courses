# ISM3232 Lab W12: OOP III — Applied Practice & Design

## YouTube Metadata

**Title:** OOP III: Applied Practice & Design — Lab Walkthrough | ISM3232 Lab 12
**Description:**
Walkthrough of ISM3232 Module 12 Lab. We design a multi-class business system from scratch: write design.md first, build two entity classes and a manager class, write six or more pytest tests, and run the full simulation.

Course page: https://markumreed.github.io/ism3232/docs/week12_lab.html

**Chapters:**
0:00 — What this lab requires
0:45 — design.md: write this BEFORE opening VS Code
3:30 — Building Entity Class 1
5:30 — Building Entity Class 2 and the Manager
7:30 — Six or more pytest tests
9:00 — main.py simulation and submission ritual

**Applies to:** ISM3232 Module 12

**Tags:** python OOP design, python multi-class system, python design first, python OOP applied, ISM3232, USF, python business OOP, python entity class

---

## Script

### INTRO (0:00–0:45)

Lab 12 — OOP III: Applied Practice and Design. This lab is different from every previous one. You design your own system. There is only one rule that the instructor enforces: **design.md must be reviewed before you write a single line of class code.** The lab requires two entity classes, one manager class, and six or more pytest tests.

---

### DESIGN.MD FIRST — ENFORCED (0:45–3:30)

The first thing you do is open `design.md`, not `models.py`.

```bash
cd ~/ism3232/module06_oop && touch design.md && code design.md
```

Fill in every field — be specific. Vague designs produce systems that can't be tested:

```markdown
# OOP Lab 12 Design

## Business Domain
[What problem does this system solve? One paragraph.]

## Entity Class 1
Name: [ClassName]
Attributes (at least 4, include one with a default value):
  - [attr1]: str
  - [attr2]: str
  - [attr3]: float
  - [attr4]: str = "Pending"   # or similar default
Methods (at least 2 that return values, not print):
  - [method1]() -> bool
  - [method2]() -> str
  - __repr__() -> str

## Entity Class 2
Name: [ClassName]
Attributes: [list]
Methods: [list]
Relationship to Entity 1: [How do they relate?]

## Manager Class
Name: [ManagerClassName]
Holds: list of [Entity Class 1]
Methods:
  - add(item) -> None
  - list_by_status(status) -> list
  - total() -> float
  - report() -> None

## Business Rules (will become methods and test cases)
1. [Rule: e.g., "amounts over $X require approval"]
2. [Rule: e.g., "certain categories are always pre-approved"]
3. [Boundary case: what value is the exact threshold?]

## Scope
[What you are NOT building]
```

Raise your hand when this is done. The instructor reviews it before you continue.

---

### BUILDING ENTITY CLASS 1 (3:30–5:30)

Once approved, open `models.py`. Here is a worked example using an employee expense system — **your domain should be different**:

```python
class ExpenseReport:
    """An employee expense report requiring approval."""

    def __init__(self, report_id: int, employee: str, department: str, amount: float):
        self.report_id  = report_id
        self.employee   = employee
        self.department = department
        self.amount     = amount
        self.status     = "Draft"

    def submit(self) -> None:
        self.status = "Submitted"

    def approve(self) -> None:
        self.status = "Approved"

    def needs_finance_review(self) -> bool:
        """Amounts over $2500 require Finance approval."""
        return self.amount > 2500.0

    def __repr__(self) -> str:
        return f"ExpenseReport({self.report_id}, {self.employee}, ${self.amount:,.2f}, {self.status})"
```

Requirements your class must hit:
- `__init__` with 4+ attributes including a status default
- 2+ methods that **return values** (not just print)
- `__repr__`

---

### ENTITY CLASS 2 AND THE MANAGER (5:30–7:30)

Entity Class 2 example (still expense domain):

```python
class BudgetLine:
    """A departmental budget line for cost-center tracking."""

    def __init__(self, department: str, budget: float):
        self.department = department
        self.budget     = budget
        self.spent      = 0.0

    def charge(self, amount: float) -> None:
        self.spent += amount

    def remaining(self) -> float:
        return self.budget - self.spent

    def is_over_budget(self) -> bool:
        return self.spent > self.budget

    def __repr__(self) -> str:
        return f"BudgetLine({self.department}, ${self.remaining():,.2f} remaining)"
```

Manager class:

```python
class ExpenseManager:
    """Manages a collection of ExpenseReport instances."""

    def __init__(self):
        self.reports: list[ExpenseReport] = []

    def add(self, report: ExpenseReport) -> None:
        self.reports.append(report)

    def list_by_status(self, status: str) -> list[ExpenseReport]:
        return [r for r in self.reports if r.status == status]

    def total(self) -> float:
        return sum(r.amount for r in self.reports)

    def report(self) -> None:
        print(f"\n{'ID':<5} {'Employee':<15} {'Dept':<12} {'Amount':>10}  Status")
        print("-" * 55)
        for r in self.reports:
            print(f"  {r.report_id:<5} {r.employee:<15} {r.department:<12} ${r.amount:>8,.2f}  {r.status}")
        print(f"\n  Total: ${self.total():,.2f}")
```

---

### SIX OR MORE PYTEST TESTS (7:30–9:00)

Required coverage (minimum six tests):

```python
from models import ExpenseReport, ExpenseManager   # use your class names

# 1. Default status
def test_default_status():
    r = ExpenseReport(1, "Kim", "Sales", 500)
    assert r.status == "Draft"

# 2. Status change method
def test_submit_changes_status():
    r = ExpenseReport(1, "Kim", "Sales", 500)
    r.submit()
    assert r.status == "Submitted"

# 3. Business logic method
def test_needs_finance_review_above_threshold():
    r = ExpenseReport(1, "Kim", "Sales", 3000)
    assert r.needs_finance_review() is True

# 4. Boundary case
def test_needs_finance_review_at_boundary():
    # $2500 exactly — does NOT require finance review
    r = ExpenseReport(1, "Kim", "Sales", 2500)
    assert r.needs_finance_review() is False

# 5. Manager: add increases count
def test_manager_add():
    mgr = ExpenseManager()
    mgr.add(ExpenseReport(1, "Kim", "Sales", 500))
    assert len(mgr.reports) == 1

# 6. Manager: filter returns correct subset
def test_manager_filter():
    mgr = ExpenseManager()
    r1 = ExpenseReport(1, "A", "X", 100)
    r2 = ExpenseReport(2, "B", "X", 200)
    r1.submit()
    mgr.add(r1); mgr.add(r2)
    submitted = mgr.list_by_status("Submitted")
    assert len(submitted) == 1

# 7. Manager: independent instances
def test_manager_independence():
    mgr1 = ExpenseManager()
    mgr2 = ExpenseManager()
    mgr1.add(ExpenseReport(1, "A", "X", 100))
    assert len(mgr2.reports) == 0
```

Run: `pytest -v` — all tests green before writing main.py.

Screenshot 1: `pytest -v` all green.

---

### MAIN.PY SIMULATION AND RITUAL (9:00–10:30)

`main.py` requirements:
- Create a manager instance
- Add at least 4 entity instances
- Call at least one status-changing method on one instance
- Call `report()` to print the summary

```python
from models import ExpenseReport, ExpenseManager   # your class names

mgr = ExpenseManager()
mgr.add(ExpenseReport(101, "Kim",   "Sales",   1800))
mgr.add(ExpenseReport(102, "Jordan","Eng",     3200))
mgr.add(ExpenseReport(103, "Taylor","Sales",   450))
mgr.add(ExpenseReport(104, "Morgan","Finance", 6000))

mgr.reports[0].submit()
mgr.reports[1].submit()
mgr.reports[1].approve()

mgr.report()
print(f"\nDraft: {len(mgr.list_by_status('Draft'))}")
print(f"Submitted: {len(mgr.list_by_status('Submitted'))}")
print(f"Approved: {len(mgr.list_by_status('Approved'))}")
```

Screenshot 2: `main.py` simulation output.

Ritual:
```bash
ruff format . && ruff check . && pytest -v
git add . && git commit -m 'lab 12: OOP III applied practice' && git push
```

---

### SUBMISSION CHECKLIST (10:30–11:00)

- `design.md` in repo — all fields filled, reviewed before code was written
- `models.py` with two entity classes + one manager class
- `main.py` with 4+ instances, status change, report() call
- 6+ pytest tests: default status, each business method, boundary, manager add, manager filter, independence
- Screenshot 1: `pytest -v` all green
- Screenshot 2: `main.py` output showing the report
- Commit includes "lab 12", GitHub URL to Canvas
