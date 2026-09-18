# ISM3232 Lab W10: OOP I — Classes & Objects

## YouTube Metadata

**Title:** OOP I — Classes & Objects — Full Lab Walkthrough | ISM3232 Lab 10
**Description:**
Step-by-step, test-as-you-go walkthrough of ISM3232 Module 10 Lab. Build the BusinessRequest class from scratch — __init__, four methods, __repr__ — create three independent instances, verify that mutating one never affects another, write seven pytest tests including a boundary case and an independence test, then run the ritual and push.

Course page: https://markumreed.github.io/ism3232/docs/week10_lab.html

**Chapters:**
0:00 — What this lab covers — no AI-generated classes
0:45 — Step 1: fresh project setup for module06_oop
1:30 — Step 2: write __init__ and the four attributes
2:50 — Step 3: write approve(), reject(), requires_review()
4:10 — Step 4: write __repr__
4:50 — Step 5: create three instances in main.py
5:50 — Step 6: print initial state — three distinct reprs
6:30 — Step 7: call methods and verify independence
7:50 — Screenshot 1 checkpoint
8:10 — Step 8: answer the five OOP reflection questions
9:50 — Step 9: write all seven pytest tests
12:00 — Step 10: the boundary test and the independence test, explained
12:50 — Step 11: run pytest -v and confirm all green
13:20 — Screenshot 2 checkpoint
13:40 — Step 12: the ritual and push
14:30 — Submission checklist

**Applies to:** ISM3232 Module 10

**Tags:** python oop classes tutorial, python __init__ self, python __repr__, pytest instance independence, ISM3232, USF, object oriented programming python

---

## How to Use This Script

**SAY** it, **DO** it, **CHECK** the exact output, **FIX** it if it doesn't match — then move to the next step.

---

## Script

### INTRO (0:00–0:45)

**SAY:** "Lab 10 — OOP I, classes and objects. First OOP lab of the semester, and one hard rule: no AI-generated classes. If you use AI for any part of this class definition, you must paste the AI output and add a comment explaining what every line does and why. You need to be able to explain every line, full stop."

---

### PART 1 — Write the Class (0:45–4:50)

#### Step 1 — Fresh project setup

**DO:**
```bash
cd ~/ism3232/module06_oop
python3 -m venv .venv && source .venv/bin/activate
pip install pytest ruff && pip freeze > requirements.txt
echo '.venv/' > .gitignore && echo '__pycache__/' >> .gitignore
touch models.py main.py && mkdir -p tests && touch tests/__init__.py tests/test_models.py
```

**CHECK:** `ls` shows `models.py`, `main.py`, `tests/`, `.venv/`, `.gitignore`, `requirements.txt`.

---

#### Step 2 — Write __init__ and the four attributes

**SAY:** "`__init__` runs automatically the moment you create an instance. `self` is the instance being built — every attribute we attach to `self` here becomes part of *that specific object*, not shared with any other."

**DO:** In `models.py`:
```python
# models.py
# Author: [Your Name]

class BusinessRequest:
    """Represents a single business purchase or travel request."""

    def __init__(self, request_id, requester, category, amount):
        self.request_id = request_id
        self.requester  = requester
        self.category   = category
        self.amount     = amount
        self.status     = 'Pending'  # default
```

**CHECK:** Read it out loud: "Four parameters come in — `request_id`, `requester`, `category`, `amount` — and get stored on `self`. `status` isn't a parameter at all — it's hardcoded to `'Pending'` for every single new request, no matter what."

---

#### Step 3 — Write approve(), reject(), requires_review()

**SAY:** "Three methods — each one operates on `self`, meaning whichever instance called it."

**DO:** Append (indented inside the class):
```python
    def approve(self):
        """Mark this request as approved."""
        self.status = 'Approved'

    def reject(self):
        """Mark this request as rejected."""
        self.status = 'Rejected'

    def requires_review(self):
        """Return True if amount exceeds 1000."""
        return self.amount > 1000
```

**CHECK:** Say it out loud: "`approve` and `reject` *mutate* — they change `self.status` on whichever object called them. `requires_review` doesn't mutate anything — it just reads `self.amount` and returns a bool."

---

#### Step 4 — Write __repr__

**SAY:** "`__repr__` controls what you see when you `print()` an instance — without it, Python shows something unhelpful like `<models.BusinessRequest object at 0x...>`."

**DO:**
```python
    def __repr__(self):
        return f'BusinessRequest({self.request_id}, {self.requester}, ${self.amount}, {self.status})'
```

**CHECK:** Confirm indentation — all four methods and `__repr__` are indented one level inside `class BusinessRequest:`, at the same level as `__init__`.

---

### PART 2 — Create Instances (4:50–7:50)

#### Step 5 — Create three instances

**SAY:** "Same class, three separate objects — this is the whole point of OOP: one blueprint, many independent instances."

**DO:** In `main.py`:
```python
from models import BusinessRequest

req_101 = BusinessRequest(101, 'Taylor', 'Travel', 1200)
req_102 = BusinessRequest(102, 'Jordan', 'Equipment', 450)
req_103 = BusinessRequest(103, 'Morgan', 'Software', 3500)
```

**CHECK:** Read it out loud: "Same `BusinessRequest(...)` call three times, with different arguments each time — three completely separate objects, each with its own copy of every attribute."

---

#### Step 6 — Print initial state

**DO:** Append:
```python
print(req_101)
print(req_102)
print(req_103)
```
```bash
python3 main.py
```

**CHECK:**
```
BusinessRequest(101, Taylor, $1200, Pending)
BusinessRequest(102, Jordan, $450, Pending)
BusinessRequest(103, Morgan, $3500, Pending)
```
Three distinct reprs, all `Pending` — that's `__repr__` and `__init__` working together correctly.

---

#### Step 7 — Call methods and verify independence

**SAY:** "Now the real test: call methods on `req_101` and `req_102` and confirm `req_103` never moves."

**DO:** Append:
```python
print(req_101.requires_review())   # True
print(req_102.requires_review())   # False

req_101.approve()
req_102.reject()

print(req_101.status)   # Approved
print(req_102.status)   # Rejected
print(req_103.status)   # Pending -- unchanged

print(req_101)
print(req_102)
```
```bash
python3 main.py
```

**CHECK:**
```
BusinessRequest(101, Taylor, $1200, Pending)
BusinessRequest(102, Jordan, $450, Pending)
BusinessRequest(103, Morgan, $3500, Pending)
True
False
Approved
Rejected
Pending
BusinessRequest(101, Taylor, $1200, Approved)
BusinessRequest(102, Jordan, $450, Rejected)
```
Confirm `req_103.status` still prints `Pending` even though `req_101` and `req_102` both changed — that's instance independence, proven, not just claimed.

---

#### Screenshot 1 checkpoint (7:50–8:10)

**SAY:** "Screenshot 1 — the complete `main.py` output showing all method calls and results."

---

### PART 3 — Verify Instance Independence (8:10–9:50)

#### Step 8 — Answer the five reflection questions

**SAY:** "Now put it in writing, at the top of `main.py`, in your own words."

**DO:** Add at the top of `main.py`:
```python
# --- OOP Lab Questions ---
# 1. After calling req_101.approve(), what is req_102.status? ___
# 2. Why doesn't approving req_101 affect req_102? ___
# 3. What does 'self' refer to inside the approve() method? ___
# 4. What is the type of req_101? ___  (hint: use type())
# 5. Where does the default status 'Pending' come from? ___
```

**CHECK:** Answer each one out loud before typing it, using what you just observed in Step 7: "Question 1 — `req_102.status` is still `Rejected`, because we called `req_102.reject()` on it directly, and it stays that way regardless of what happens to `req_101`. Question 2 — each instance has its own separate `self.status`; there's no shared storage between them. Question 3 — inside `approve()`, `self` refers to whichever specific object the method was called on — `req_101` in that call. Question 4 — `type(req_101)` is `<class 'models.BusinessRequest'>`. Question 5 — it's hardcoded inside `__init__`, so every new instance starts there regardless of what arguments you passed."

---

### PART 4 — Seven pytest Tests (9:50–13:20)

#### Step 9 — Write all seven tests

**SAY:** "Seven tests — covering the default state, both status-changing methods, three variations on `requires_review`, and one dedicated independence test."

**DO:** In `tests/test_models.py`:
```python
from models import BusinessRequest


def test_default_status_is_pending():
    req = BusinessRequest(1, 'Test', 'Travel', 500)
    assert req.status == 'Pending'


def test_approve_changes_status():
    req = BusinessRequest(2, 'Test', 'Travel', 500)
    req.approve()
    assert req.status == 'Approved'


def test_reject_changes_status():
    req = BusinessRequest(3, 'Test', 'Travel', 500)
    req.reject()
    assert req.status == 'Rejected'


def test_requires_review_over_limit():
    req = BusinessRequest(4, 'Test', 'Travel', 1500)
    assert req.requires_review() is True


def test_requires_review_under_limit():
    req = BusinessRequest(5, 'Test', 'Travel', 500)
    assert req.requires_review() is False


def test_requires_review_at_boundary():
    req = BusinessRequest(6, 'Test', 'Travel', 1000)
    assert req.requires_review() is False  # > not >=


def test_instances_are_independent():
    req1 = BusinessRequest(7, 'A', 'Travel', 500)
    req2 = BusinessRequest(8, 'B', 'Travel', 500)
    req1.approve()
    assert req2.status == 'Pending'
```

**CHECK:** Count seven `def test_` functions.

---

#### Step 10 — The boundary test and the independence test, explained

**SAY:** "Two tests deserve a closer look. `test_requires_review_at_boundary` — exactly 1000 — checks that `requires_review` uses strict `>`, so an amount at the exact limit does *not* trigger review, matching what we wrote in Step 3. `test_instances_are_independent` builds two *brand-new* objects inside the test itself — separate from `req_101`/`req_102`/`req_103` in `main.py` — and proves the same independence property holds for any two instances, not just the specific three we happened to create."

---

#### Step 11 — Run pytest and confirm all green

**DO:**
```bash
pytest -v
```

**CHECK:**
```
tests/test_models.py::test_default_status_is_pending PASSED
tests/test_models.py::test_approve_changes_status PASSED
tests/test_models.py::test_reject_changes_status PASSED
tests/test_models.py::test_requires_review_over_limit PASSED
tests/test_models.py::test_requires_review_under_limit PASSED
tests/test_models.py::test_requires_review_at_boundary PASSED
tests/test_models.py::test_instances_are_independent PASSED

======================== 7 passed in 0.01s ========================
```

---

#### Screenshot 2 checkpoint (13:20–13:40)

**SAY:** "Screenshot 2 — `pytest -v` with all seven tests green."

---

### PART 5 — Ritual and Push (13:40–14:30)

#### Step 12 — Run the ritual

**DO:**
```bash
ruff format . && ruff check . && pytest -v
git add . && git commit -m 'lab 10: OOP I BusinessRequest class' && git push
```

**CHECK:** No lint errors, `7 passed`, push succeeds, commit message includes "lab 10."

---

### SUBMISSION CHECKLIST (14:30–end)

- [ ] Screenshot 1: complete `main.py` output showing all method calls and results
- [ ] Screenshot 2: `pytest -v` with all seven tests green
- [ ] Comment block with all five OOP reflection questions answered
- [ ] Git commit message includes "lab 10"
- [ ] GitHub repository URL pasted into Canvas
