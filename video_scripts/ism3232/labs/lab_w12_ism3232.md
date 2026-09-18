# ISM3232 Lab W12: OOP III — Applied Practice & Design

## YouTube Metadata

**Title:** OOP III — Design Your Own System — Full Lab Walkthrough | ISM3232 Lab 12
**Description:**
Step-by-step, test-as-you-go walkthrough of ISM3232 Module 12 Lab. Design a multi-class system in design.md before writing any code, then build two entity classes and a manager class using a worked expense-report example, write seven pytest tests including a boundary case, run a four-instance simulation, and push — every command run and verified one at a time.

Course page: https://markumreed.github.io/ism3232/docs/week12_lab.html

**Chapters:**
0:00 — The one enforced rule: design before code
0:45 — Step 1: create design.md
1:20 — Step 2: fill in the business domain and Entity Class 1 fields
3:00 — Step 3: fill in Entity Class 2, the manager, and business rules
4:30 — Step 4: raise your hand — instructor design review
4:50 — Step 5: build Entity Class 1 — ExpenseReport
6:30 — Step 6: build Entity Class 2 — BudgetLine
7:40 — Step 7: build the manager class — ExpenseManager
9:20 — Step 8: write all seven pytest tests
11:40 — Step 9: the boundary test, explained
12:10 — Step 10: run pytest -v and confirm all green
12:40 — Screenshot 1 checkpoint
13:00 — Step 11: write main.py — four instances, one status change
14:10 — Step 12: run and verify the full report
15:10 — Screenshot 2 checkpoint
15:30 — Step 13: the ritual and push
16:20 — Submission checklist

**Applies to:** ISM3232 Module 12

**Tags:** python OOP design, python multi-class system, python design first, python OOP applied, ISM3232, USF, python business OOP, python entity class

---

## How to Use This Script

**SAY** it, **DO** it, **CHECK** the exact output, **FIX** it if it doesn't match — then move to the next step. This lab is design-your-own-domain; I'm working an employee expense-report system as the on-camera example — **pick a different domain for your own submission**, the mechanics transfer directly.

---

## Script

### INTRO (0:00–0:45)

**SAY:** "Lab 12 — OOP III, applied practice and design. One rule the instructor enforces harder than anything else this semester: you may not open `models.py` until your design document is reviewed. Design before code. Let's write the design first."

---

### PART 1 — Write Your Design Document First (0:45–4:50)

#### Step 1 — Create design.md

**DO:**
```bash
cd ~/ism3232/module06_oop && touch design.md && code design.md
```

**CHECK:** An empty `design.md` opens in VS Code, in the same folder as your Week 10–11 `models.py` and `main.py`.

---

#### Step 2 — Business domain and Entity Class 1

**SAY:** "First the one-paragraph pitch, then the first entity class's shape — before any code exists."

**DO:**
```markdown
# OOP Lab 12 Design
# Author: [Your Name]

## Business Domain
[Describe the system you are building in 1-2 sentences]
Example: An employee expense-reporting system that tracks submissions
against a department budget and flags high-value reports for Finance review.

## Entity Class 1
Class name: ExpenseReport
Attributes (name + type):
  - report_id: int
  - employee: str
  - department: str
  - amount: float
  - status: str = "Draft"   # default value
Methods (name + what it does + return type):
  - submit(): changes status to Submitted -> None
  - needs_finance_review(): True if amount > 2500 -> bool
  - __repr__() -> str
```

**CHECK:** Read every field out loud before moving on: "Four real attributes plus a status that defaults to `'Draft'`, and at least two methods that *return* values — not print — since business logic and display are always kept separate in this course."

---

#### Step 3 — Entity Class 2, the manager, and business rules

**DO:**
```markdown
## Entity Class 2
Class name: BudgetLine
Attributes:
  - department: str
  - budget: float
  - spent: float = 0.0
Methods:
  - charge(amount): adds to spent -> None
  - remaining(): budget minus spent -> float
Relationship to Entity 1: Each department's BudgetLine is charged when an
ExpenseReport for that department is approved.

## Manager Class
Class name: ExpenseManager
Holds: list of ExpenseReport
Methods:
  - add(item): adds to the list
  - list_by_status(status): filters by status
  - total(): returns sum of a numeric attribute
  - report(): prints formatted summary

## Business Rules (will become methods and test cases)
1. Amounts over $2500 require Finance review.
2. Exactly $2500 does NOT require review (boundary is strict >).
3. A report starts as "Draft" until explicitly submitted.

## Out of Scope
Multi-currency support, approval workflows beyond a single Finance reviewer,
and persistence to a database (that's Unit 4).
```

**CHECK:** Read the business rules section specifically — every rule listed here becomes a test case in Part 4, so vague rules now mean untestable code later. Confirm rule 2 states the boundary direction explicitly (`>` not `>=`), because that's exactly what you'll assert in a test.

---

#### Step 4 — Raise your hand for design review

**SAY:** "Now stop. Raise your hand. The instructor reviews `design.md` before you're allowed to open `models.py`. This is the one lab this semester where skipping ahead defeats the entire point of the exercise."

**CHECK:** Design approved — you may now proceed to Part 2.

---

### PART 2 — Build Entity Class 1 (4:50–6:30)

#### Step 5 — Write ExpenseReport in models.py

**SAY:** "Straight from the design document — nothing here should be a surprise, because we already specified every attribute and method."

**DO:** In `models.py`:
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

**CHECK:** Count against the design doc's requirements: four core attributes plus a `status` default (✓), two return-value methods — `needs_finance_review` and, arguably, none of the status-changers return anything meaningful, so this design also adds `approve()` beyond the minimum for completeness — and `__repr__` (✓).

---

### PART 3 — Build Entity Class 2 and the Manager (6:30–9:20)

#### Step 6 — Write BudgetLine

**SAY:** "A different kind of object entirely — tracks a department's budget, not an individual report."

**DO:**
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

**CHECK:** Read `charge()` out loud: "It mutates `self.spent` by adding to it — the same accumulation pattern from Week 6's `total += rec['amount']`, just living inside a method now instead of a bare loop."

---

#### Step 7 — Write ExpenseManager

**SAY:** "Same composition pattern as Week 11's `RequestManager` — a class that holds a list of the first entity class."

**DO:**
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

**CHECK:** Note the type hint `list[ExpenseReport]` on `self.reports` — this documents that the manager only ever holds `ExpenseReport` objects, even though Python won't enforce it at runtime. The `report()` method uses `<`/`>` alignment specifiers (`{r.employee:<15}`, `{r.amount:>8,.2f}`) to left- and right-justify columns into a readable table.

---

### PART 4 — Write At Least Six Tests (9:20–12:40)

#### Step 8 — Write all seven tests

**SAY:** "Required coverage: default state, each business logic method, a boundary case, and three manager behaviors — add, filter, independence. That's seven, one more than the six minimum."

**DO:** In `tests/test_models.py`:
```python
from models import ExpenseReport, ExpenseManager   # use your class names


def test_default_status():
    r = ExpenseReport(1, "Kim", "Sales", 500)
    assert r.status == "Draft"


def test_submit_changes_status():
    r = ExpenseReport(1, "Kim", "Sales", 500)
    r.submit()
    assert r.status == "Submitted"


def test_needs_finance_review_above_threshold():
    r = ExpenseReport(1, "Kim", "Sales", 3000)
    assert r.needs_finance_review() is True


def test_needs_finance_review_at_boundary():
    # $2500 exactly — does NOT require finance review
    r = ExpenseReport(1, "Kim", "Sales", 2500)
    assert r.needs_finance_review() is False


def test_manager_add():
    mgr = ExpenseManager()
    mgr.add(ExpenseReport(1, "Kim", "Sales", 500))
    assert len(mgr.reports) == 1


def test_manager_filter():
    mgr = ExpenseManager()
    r1 = ExpenseReport(1, "A", "X", 100)
    r2 = ExpenseReport(2, "B", "X", 200)
    r1.submit()
    mgr.add(r1); mgr.add(r2)
    submitted = mgr.list_by_status("Submitted")
    assert len(submitted) == 1


def test_manager_independence():
    mgr1 = ExpenseManager()
    mgr2 = ExpenseManager()
    mgr1.add(ExpenseReport(1, "A", "X", 100))
    assert len(mgr2.reports) == 0
```

**CHECK:** Match each test back to the design doc's "Business Rules" section from Step 3 — this is what "design before code" buys you: every rule you wrote down now has a corresponding assertion.

---

#### Step 9 — The boundary test, explained

**SAY:** "`test_needs_finance_review_at_boundary` is the one test worth pausing on — exactly $2,500, the precise value where `needs_finance_review` switches from `False` to `True`. Because the method uses strict `>`, not `>=`, $2,500 itself stays `False`. This is exactly the class of bug that silently breaks approval workflows in real systems — get the boundary direction backwards and requests that should require review slip through, or requests that shouldn't get stuck waiting on Finance."

---

#### Step 10 — Run pytest and confirm all green

**DO:**
```bash
pytest -v
```

**CHECK:**
```
tests/test_models.py::test_default_status PASSED
tests/test_models.py::test_submit_changes_status PASSED
tests/test_models.py::test_needs_finance_review_above_threshold PASSED
tests/test_models.py::test_needs_finance_review_at_boundary PASSED
tests/test_models.py::test_manager_add PASSED
tests/test_models.py::test_manager_filter PASSED
tests/test_models.py::test_manager_independence PASSED

======================== 7 passed in 0.01s ========================
```

**FIX:** Do not write `main.py` until every test here is green — the lab requires tests to pass before the simulation step.

---

#### Screenshot 1 checkpoint (12:40–13:00)

**SAY:** "Screenshot 1 — `pytest -v` with all seven tests green."

---

### PART 5 — Main Simulation and Ritual (13:00–15:30)

#### Step 11 — Write main.py

**SAY:** "Four instances, at least one status change, and a call to `report()` — the requirements from the lab page, translated into this domain."

**DO:**
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

**CHECK:** Trace the statuses by hand before running: "Kim (101) gets submitted. Jordan (102) gets submitted, then approved — ending at `Approved`, not `Submitted`. Taylor (103) and Morgan (104) never get touched, so both stay at the default `Draft`."

---

#### Step 12 — Run and verify the full report

**DO:**
```bash
python3 main.py
```

**CHECK:**
```
ID    Employee        Dept           Amount  Status
-------------------------------------------------------
  101   Kim             Sales         $1,800.00  Submitted
  102   Jordan          Eng           $3,200.00  Approved
  103   Taylor          Sales           $450.00  Draft
  104   Morgan          Finance       $6,000.00  Draft

  Total: $11,450.00

Draft: 2
Submitted: 1
Approved: 1
```
Confirm the total by hand: 1800 + 3200 + 450 + 6000 = 11,450. Confirm the three status counts sum to 4 — every request accounted for exactly once.

---

#### Screenshot 2 checkpoint (15:10–15:30)

**SAY:** "Screenshot 2 — the `main.py` simulation output showing the full report."

---

### PART 6 — Ritual (15:30–16:20)

#### Step 13 — Run the ritual

**DO:**
```bash
ruff format . && ruff check . && pytest -v
git add . && git commit -m 'lab 12: OOP III applied practice' && git push
```

**CHECK:** No lint errors, all seven tests pass, push succeeds, commit message includes "lab 12."

---

### SUBMISSION CHECKLIST (16:20–end)

- [ ] `design.md` in the repo — all fields filled in, reviewed by the instructor before any code was written
- [ ] `models.py` with two entity classes plus one manager class
- [ ] `main.py` with 4+ instances, at least one status change, and a `report()` call
- [ ] 6+ pytest tests: default status, each business method, a boundary case, manager add, manager filter, manager independence
- [ ] Screenshot 1: `pytest -v` all green
- [ ] Screenshot 2: `main.py` output showing the report
- [ ] Git commit message includes "lab 12"
- [ ] GitHub repository URL pasted into Canvas
