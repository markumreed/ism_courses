# ISM3232 Lab W11: OOP II — Composition, Inheritance & SQL Mapping

## YouTube Metadata

**Title:** OOP II — Composition & the Manager Class — Full Lab Walkthrough | ISM3232 Lab 11
**Description:**
Step-by-step, test-as-you-go walkthrough of ISM3232 Module 11 Lab. Build RequestManager — a class that holds a list of BusinessRequest objects and provides add/filter/total/report methods — wire it to main.py, map the OOP design onto SQL tables and queries, write six tests covering both classes, then run the ritual and push.

Course page: https://markumreed.github.io/ism3232/docs/week11_lab.html

**Chapters:**
0:00 — What this lab covers — composition, not inheritance
0:40 — Step 1: write RequestManager's __init__ and add_request
1:40 — Step 2: write list_pending and get_by_status
2:50 — Step 3: write total_amount and summary_report
4:00 — Step 4: rewrite main.py to use the manager
5:20 — Step 5: run and verify the summary report
6:10 — Screenshot 1 checkpoint
6:30 — Step 6: fill in the OOP-to-SQL mapping table
8:10 — Step 7: write all six new tests
10:40 — Step 8: two tests worth a closer look
11:30 — Step 9: run pytest -v — old and new tests together
12:00 — Screenshot 2 checkpoint
12:20 — Step 10: the ritual and push
13:10 — Submission checklist

**Applies to:** ISM3232 Module 11

**Tags:** python composition tutorial, python has-a relationship, oop to sql mapping, python inheritance super, pytest composed classes, ISM3232, USF

---

## How to Use This Script

**SAY** it, **DO** it, **CHECK** the exact output, **FIX** it if it doesn't match — then move to the next step.

---

## Script

### INTRO (0:00–0:40)

**SAY:** "Lab 11 — OOP II, composition and the manager class. Last week, `BusinessRequest` stood alone. Today it gets a manager — a class that *holds* a list of requests. This is composition: `RequestManager` doesn't inherit from `BusinessRequest`, it *has* a collection of them. That distinction — 'has-a' versus 'is-a' — is the whole lesson today."

---

### PART 1 — Write RequestManager (0:40–4:00)

#### Step 1 — __init__ and add_request

**SAY:** "The manager starts empty — one instance attribute, an empty list — and one method to grow it."

**DO:** Append to `models.py`, below `BusinessRequest`:
```python
class RequestManager:
    """Manages a collection of business requests."""

    def __init__(self):
        self.requests = []

    def add_request(self, request):
        """Add a BusinessRequest to the collection."""
        self.requests.append(request)
```

**CHECK:** Read it out loud: "`self.requests` starts as an empty list — every `RequestManager` instance gets its own separate list, not a shared one. `add_request` takes a `BusinessRequest` object as an argument and appends it — this is composition: the manager stores *references* to request objects, it doesn't recreate them."

---

#### Step 2 — list_pending and get_by_status

**SAY:** "Two filtering methods — one hardcoded to `'Pending'`, one generalized to any status string."

**DO:**
```python
    def list_pending(self):
        """Return all requests with status Pending."""
        return [r for r in self.requests if r.status == 'Pending']

    def get_by_status(self, status):
        """Return requests matching the given status."""
        return [r for r in self.requests if r.status == status]
```

**CHECK:** Notice `list_pending()` is really just `get_by_status('Pending')` written out explicitly — say out loud why both exist: "`list_pending` reads clearly at call sites where pending is the only thing that matters; `get_by_status` is the general-purpose version for anything else."

---

#### Step 3 — total_amount and summary_report

**SAY:** "One aggregate calculation, and one method that prints a full formatted report using everything above it."

**DO:**
```python
    def total_amount(self):
        """Return the total value of all requests."""
        return sum(r.amount for r in self.requests)

    def summary_report(self):
        """Print a formatted summary of all requests by status."""
        pending  = self.list_pending()
        approved = self.get_by_status('Approved')
        print(f'Total requests: {len(self.requests)} | Total: ${self.total_amount():,.2f}')
        print(f'Pending: {len(pending)} | Approved: {len(approved)}')
        print('Pending requests:')
        for r in pending:
            print(f'  {r}')
```

**CHECK:** Say out loud: "`total_amount` uses a generator expression — `r.amount for r in self.requests` — fed straight into `sum()`. `summary_report` calls three of the manager's *own* methods — `list_pending`, `get_by_status`, `total_amount` — that's methods calling other methods on the same object, all through `self`."

---

### PART 2 — Wire the Two Classes (4:00–6:30)

#### Step 4 — Rewrite main.py

**SAY:** "Replace last week's `main.py` entirely — now it goes through the manager instead of tracking individual variables."

**DO:** Replace the contents of `main.py`:
```python
from models import BusinessRequest, RequestManager

mgr = RequestManager()
mgr.add_request(BusinessRequest(101, 'Taylor', 'Travel', 1200))
mgr.add_request(BusinessRequest(102, 'Jordan', 'Equipment', 450))
mgr.add_request(BusinessRequest(103, 'Morgan', 'Software', 3500))
mgr.add_request(BusinessRequest(104, 'Riley',  'Travel', 89))

# Approve one request
mgr.requests[0].approve()

# Print the full report
mgr.summary_report()
```

**CHECK:** Read it out loud: "Four requests get created and immediately added to `mgr` in one line each — no more separate `req_101`, `req_102` variables. `mgr.requests[0]` reaches directly into the manager's internal list to grab the first one and approve it."

---

#### Step 5 — Run and verify

**DO:**
```bash
python3 main.py
```

**CHECK:**
```
Total requests: 4 | Total: $5,239.00
Pending: 3 | Approved: 1
Pending requests:
  BusinessRequest(102, Jordan, $450, Pending)
  BusinessRequest(103, Morgan, $3500, Pending)
  BusinessRequest(104, Riley, $89, Pending)
```
Confirm the math by hand: 1200 + 450 + 3500 + 89 = 5,239. Taylor's request (101) is missing from the pending list because Step 4 approved it — only Jordan, Morgan, and Riley remain pending.

---

#### Screenshot 1 checkpoint (6:10–6:30)

**SAY:** "Screenshot 1 — the `summary_report()` output from `main.py`."

---

### PART 3 — OOP to SQL Mapping (6:30–8:10)

#### Step 6 — Fill in the mapping table

**SAY:** "This is the conceptual bridge to next month's SQL unit — every OOP concept you just built has a direct SQL equivalent. Fill in your own system's specifics in the right column."

**DO:** In `README.md`:
```markdown
## OOP to SQL Mapping

| OOP concept           | SQL equivalent         | This system         |
|-----------------------|-------------------------|----------------------|
| class BusinessRequest | table: requests         | [your table name]   |
| instance (one object) | row (one record)        | [example row]        |
| attribute: amount     | column: amount REAL     | [your type]          |
| list_pending()        | SELECT WHERE status=?   | [your query]         |
| total_amount()        | SELECT SUM(amount)      | [your aggregate]     |
```

**CHECK:** Read each row out loud and explain the equivalence in your own words before filling in the right column: "A class is a table's shape. One instance is one row. An attribute is a column. A filtering method is a `WHERE` clause. An aggregate method is a SQL aggregate function."

---

### PART 4 — Six pytest Tests (8:10–12:00)

#### Step 7 — Write all six new tests

**SAY:** "Six tests, covering `RequestManager` on its own and in combination with `BusinessRequest`. Keep every test from Week 10 — these get added alongside them, not instead of them."

**DO:** Append to `tests/test_models.py`:
```python
from models import BusinessRequest, RequestManager


def test_manager_starts_empty():
    mgr = RequestManager()
    assert len(mgr.requests) == 0


def test_add_increases_count():
    mgr = RequestManager()
    mgr.add_request(BusinessRequest(1, 'A', 'Travel', 500))
    assert len(mgr.requests) == 1


def test_list_pending_filters_correctly():
    mgr = RequestManager()
    req1 = BusinessRequest(1, 'A', 'Travel', 500)
    req2 = BusinessRequest(2, 'B', 'Travel', 600)
    mgr.add_request(req1); mgr.add_request(req2)
    req1.approve()
    pending = mgr.list_pending()
    assert len(pending) == 1
    assert pending[0].requester == 'B'


def test_total_amount_correct():
    mgr = RequestManager()
    mgr.add_request(BusinessRequest(1, 'A', 'T', 500))
    mgr.add_request(BusinessRequest(2, 'B', 'T', 750))
    assert mgr.total_amount() == 1250


def test_get_by_status():
    mgr = RequestManager()
    req1 = BusinessRequest(1, 'A', 'T', 500)
    mgr.add_request(req1)
    req1.approve()
    approved = mgr.get_by_status('Approved')
    assert len(approved) == 1


def test_independent_managers():
    mgr1 = RequestManager()
    mgr2 = RequestManager()
    mgr1.add_request(BusinessRequest(1, 'A', 'T', 500))
    assert len(mgr2.requests) == 0
```

**CHECK:** Note the second import line — `from models import BusinessRequest, RequestManager` — needs to appear only once at the top of the file. If you already had a `from models import BusinessRequest` line from Week 10, merge them into one import instead of two separate lines.

---

#### Step 8 — Two tests worth a closer look

**SAY:** "`test_list_pending_filters_correctly` builds two requests, approves one *through the object itself* (`req1.approve()`), then checks the manager's filter reflects that change — proving the manager and the objects it holds share the same live state, not a copy. `test_independent_managers` mirrors last week's instance-independence test, but one level up: two separate managers, each with their own separate list."

---

#### Step 9 — Run pytest and confirm all pass

**DO:**
```bash
pytest -v
```

**CHECK:** All Week 10 tests (`test_default_status_is_pending`, `test_approve_changes_status`, etc.) *and* all six new tests report `PASSED`, ending in:
```
======================== 13 passed in 0.01s ========================
```

**FIX:** If the total count is lower than 13, confirm you didn't accidentally delete last week's tests when editing the file — scroll up and check `test_models.py` still has both sections.

---

#### Screenshot 2 checkpoint (12:00–12:20)

**SAY:** "Screenshot 2 — `pytest -v` with all tests green, old and new together."

---

### PART 5 — Ritual and Push (12:20–13:10)

#### Step 10 — Run the ritual

**DO:**
```bash
ruff format . && ruff check . && pytest -v
git add . && git commit -m 'lab 11: OOP II RequestManager composition' && git push
```

**CHECK:** No lint errors, all 13 tests pass, push succeeds, commit message includes "lab 11."

---

### SUBMISSION CHECKLIST (13:10–end)

- [ ] Screenshot 1: `summary_report()` output from `main.py`
- [ ] Screenshot 2: `pytest -v` with all tests green (Week 10 + Week 11 combined)
- [ ] `README.md` with the OOP-to-SQL mapping table filled in
- [ ] Git commit message includes "lab 11"
- [ ] GitHub repository URL pasted into Canvas
