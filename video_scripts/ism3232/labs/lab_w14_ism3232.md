# ISM3232 Lab W14: Python + SQL Integration

## YouTube Metadata

**Title:** Python + SQL Integration — Full Lab Walkthrough | ISM3232 Lab 14
**Description:**
Step-by-step, test-as-you-go walkthrough of ISM3232 Module 14 Lab. Build all five database.py functions — create_table, add_record, get_all_records, update_status, get_status_report — using parameterized ? queries and row_factory, test manually in a Python shell, write five pytest tests with the tmp_path fixture, then run an end-to-end test script and push.

Course page: https://markumreed.github.io/ism3232/docs/week14_lab.html

**Chapters:**
0:00 — The two rules for every line in database.py
0:50 — Step 1: project setup and create_table()
2:20 — Step 2: write add_record() with ? placeholders
3:30 — Step 3: write get_all_records() with row_factory
4:50 — Step 4: test both manually in the Python shell
6:10 — Screenshot 1 checkpoint
6:30 — Step 5: write update_status()
7:20 — Step 6: write get_status_report()
8:10 — Step 7: verify the complete file against the reference
8:40 — Step 8: write all five pytest tests with tmp_path
11:20 — Step 9: why tmp_path matters, explained
12:00 — Step 10: run pytest -v and confirm all green
12:30 — Screenshot 2 checkpoint
12:50 — Step 11: write test_script.py end to end
14:20 — Step 12: run it and verify the status report
15:10 — Screenshot 3 checkpoint
15:30 — Step 13: the ritual and push
16:10 — Submission checklist

**Applies to:** ISM3232 Module 14

**Tags:** python sqlite3 tutorial, parameterized sql queries, sqlite3 row_factory, pytest tmp_path fixture, ISM3232, USF, sql injection prevention python

---

## How to Use This Script

**SAY** it, **DO** it, **CHECK** the exact output, **FIX** it if it doesn't match — then move to the next step.

---

## Script

### INTRO (0:00–0:50)

**SAY:** "Lab 14 — Python and SQL integration. Two rules apply to every single line of `database.py` we write today. Rule one: always use `?` placeholders — never f-strings, never string concatenation, to build a SQL query. Rule two: every function accepts an optional `db_file` parameter, defaulting to a constant, so tests can point at an isolated temporary database instead of your real one. Both rules exist for the same reason — safety and testability — and we'll see exactly why as we go."

---

### PART 1 — Set Up database.py (0:50–2:20)

#### Step 1 — Create the module and write create_table()

**DO:**
```bash
cd ~/ism3232/module07_final_project
source .venv/bin/activate
mkdir -p data tests
touch database.py tests/__init__.py tests/test_database.py
code database.py
```
```python
import sqlite3

DB_FILE = 'data/requests.db'


def create_table(db_file=DB_FILE):
    """Create the main table if it does not already exist."""
    with sqlite3.connect(db_file) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS requests (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                requester TEXT    NOT NULL,
                category  TEXT    NOT NULL,
                amount    REAL,
                status    TEXT    DEFAULT 'Pending',
                notes     TEXT
            )
        ''')
```

**CHECK:** Read the signature out loud: "`db_file=DB_FILE` — that's rule two already, right in the first function. Call `create_table()` with no arguments in real use, and it writes to `data/requests.db`; call it with a different path in a test, and it writes there instead." Also note `IF NOT EXISTS` — this function is safe to call every time the app starts, even if the table already exists.

---

### PART 2 — add_record and get_all_records (2:20–6:10)

#### Step 2 — Write add_record()

**SAY:** "Rule one in action — parameterized placeholders, not an f-string."

**DO:**
```python
def add_record(requester, category, amount, notes='', db_file=DB_FILE):
    """Insert a new record. Uses ? placeholders -- never f-strings."""
    with sqlite3.connect(db_file) as conn:
        conn.execute(
            'INSERT INTO requests (requester, category, amount, notes) VALUES (?,?,?,?)',
            (requester, category, amount, notes)
        )
```

**CHECK:** Say out loud why this matters: "If I'd written `f'... VALUES ({requester}, ...)'` instead, and `requester` ever contained something like `'; DROP TABLE requests; --`, that text would execute as SQL. The four `?` placeholders and the separate tuple `(requester, category, amount, notes)` mean the database driver handles escaping — user input can never be interpreted as SQL syntax."

---

#### Step 3 — Write get_all_records()

**SAY:** "By default, SQLite returns each row as a plain tuple — no field names. `row_factory` changes that so you get dict-like access instead."

**DO:**
```python
def get_all_records(db_file=DB_FILE):
    """Return all records as a list of dicts."""
    with sqlite3.connect(db_file) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.execute('SELECT * FROM requests ORDER BY id DESC')
        return [dict(row) for row in cur.fetchall()]
```

**CHECK:** Read it out loud: "`conn.row_factory = sqlite3.Row` — now each row supports both index access and key access. `[dict(row) for row in cur.fetchall()]` converts every row into a real Python dict, so the rest of the app can write `records[0]['requester']` instead of `records[0][1]` and having to remember what column 1 means."

---

#### Step 4 — Test manually in the Python shell

**SAY:** "Before writing a single automated test, prove these two functions work by hand, interactively."

**DO:**
```bash
python3
```
```python
>>> from database import create_table, add_record, get_all_records
>>> create_table()
>>> add_record('Taylor', 'Travel', 1200)
>>> records = get_all_records()
>>> print(records[0])
>>> exit()
```

**CHECK:**
```
{'id': 1, 'requester': 'Taylor', 'category': 'Travel', 'amount': 1200.0, 'status': 'Pending', 'notes': ''}
```
A real Python dict, printed directly — confirming both `row_factory` and the `dict(row)` conversion worked.

---

#### Screenshot 1 checkpoint (6:10–6:30)

**SAY:** "Screenshot 1 — the Python shell showing that record retrieved as a dict."

---

### PART 3 — update_status and get_status_report (6:30–8:40)

#### Step 5 — Write update_status()

**SAY:** "Same two rules again — placeholders, and a `db_file` default."

**DO:**
```python
def update_status(record_id, new_status, db_file=DB_FILE):
    """Update status of a record by ID."""
    with sqlite3.connect(db_file) as conn:
        conn.execute('UPDATE requests SET status=? WHERE id=?', (new_status, record_id))
```

**CHECK:** Count the placeholders: two `?` marks, two values in the tuple, in the same order — `new_status` first, then `record_id`, matching `SET status=?` then `WHERE id=?` left to right.

---

#### Step 6 — Write get_status_report()

**SAY:** "This one doesn't take user-supplied values at all, so there's nothing to parameterize — it's the exact `GROUP BY` query from last week's sqlite3 shell session, now callable from Python."

**DO:**
```python
def get_status_report(db_file=DB_FILE):
    """Return count and total grouped by status."""
    with sqlite3.connect(db_file) as conn:
        cur = conn.execute('SELECT status, COUNT(*) as count, SUM(amount) as total FROM requests GROUP BY status')
        return cur.fetchall()
```

**CHECK:** Note this function does **not** set `row_factory` — it returns plain tuples, so accessing results later uses `row[0]`, `row[1]`, `row[2]` (status, count, total) rather than dict keys. That's an intentional inconsistency worth noticing, not a bug.

---

#### Step 7 — Verify the complete file

**SAY:** "Pause and check the whole file against the reference — five functions, no more, no less."

**CHECK:** `database.py` now contains exactly these five function definitions, in this order: `create_table`, `add_record`, `get_all_records`, `update_status`, `get_status_report` — every one accepting `db_file=DB_FILE` as its last parameter.

---

### PART 4 — Five pytest Tests with tmp_path (8:40–12:30)

#### Step 8 — Write all five tests

**SAY:** "`tmp_path` is a built-in pytest fixture — pytest creates a fresh, empty temporary folder for every single test function automatically, and cleans it up afterward. Pass `tmp_path / 'test.db'` as `db_file` to every call, and each test gets a completely isolated database."

**DO:** In `tests/test_database.py`:
```python
import pytest
from database import create_table, add_record, get_all_records, update_status, get_status_report


def test_add_and_retrieve(tmp_path):
    db = tmp_path / 'test.db'
    create_table(db)
    add_record('Taylor', 'Travel', 1200, db_file=db)
    records = get_all_records(db_file=db)
    assert len(records) == 1
    assert records[0]['requester'] == 'Taylor'
    assert records[0]['amount'] == 1200


def test_default_status_is_pending(tmp_path):
    db = tmp_path / 'test.db'
    create_table(db)
    add_record('Jordan', 'Equipment', 450, db_file=db)
    records = get_all_records(db_file=db)
    assert records[0]['status'] == 'Pending'


def test_update_status(tmp_path):
    db = tmp_path / 'test.db'
    create_table(db)
    add_record('Morgan', 'Software', 3500, db_file=db)
    records = get_all_records(db_file=db)
    update_status(records[0]['id'], 'Approved', db_file=db)
    updated = get_all_records(db_file=db)
    assert updated[0]['status'] == 'Approved'


def test_multiple_records(tmp_path):
    db = tmp_path / 'test.db'
    create_table(db)
    add_record('A', 'T', 500, db_file=db)
    add_record('B', 'T', 750, db_file=db)
    records = get_all_records(db_file=db)
    assert len(records) == 2


def test_status_report_groups_correctly(tmp_path):
    db = tmp_path / 'test.db'
    create_table(db)
    add_record('A', 'T', 500, db_file=db)
    add_record('B', 'T', 750, db_file=db)
    records = get_all_records(db_file=db)
    update_status(records[0]['id'], 'Approved', db_file=db)
    report = get_status_report(db_file=db)
    statuses = [row[0] for row in report]
    assert 'Pending' in statuses
    assert 'Approved' in statuses
```

**CHECK:** Notice every single test takes `tmp_path` as a parameter — pytest recognizes the name and injects a fresh path automatically; you never create or import it yourself.

---

#### Step 9 — Why tmp_path matters, explained

**SAY:** "Without `tmp_path`, every test would write to the same `data/requests.db` — the real development database. Run the tests twice and `test_add_and_retrieve`'s `assert len(records) == 1` would fail the second time, because the first run's data is still sitting there. `tmp_path` gives every test a brand-new, empty, disposable database, so test order and repetition never matter."

---

#### Step 10 — Run pytest and confirm all green

**DO:**
```bash
pytest -v
```

**CHECK:**
```
tests/test_database.py::test_add_and_retrieve PASSED
tests/test_database.py::test_default_status_is_pending PASSED
tests/test_database.py::test_update_status PASSED
tests/test_database.py::test_multiple_records PASSED
tests/test_database.py::test_status_report_groups_correctly PASSED

======================== 5 passed in 0.03s ========================
```

---

#### Screenshot 2 checkpoint (12:30–12:50)

**SAY:** "Screenshot 2 — `pytest -v` with all five tests green."

---

### PART 5 — Test Script and Ritual (12:50–15:30)

#### Step 11 — Write test_script.py

**SAY:** "One more check, outside pytest — a plain script exercising all five functions end to end, against the real `data/requests.db` this time, not a temp one."

**DO:**
```python
from database import create_table, add_record, get_all_records, update_status, get_status_report

create_table()
add_record('Taylor', 'Travel', 1200)
add_record('Jordan', 'Equipment', 450)
add_record('Morgan', 'Software', 3500)

records = get_all_records()
print(f'Records: {len(records)}')

update_status(records[0]['id'], 'Approved')

report = get_status_report()
print('\nStatus report:')
for row in report:
    print(f'  {row[0]}: {row[1]} records, ${row[2]:,.2f}')
```

**CHECK:** Before running, trace it by hand: "Three inserts — Taylor, Jordan, Morgan, all defaulting to Pending. `get_all_records()` orders by `id DESC`, so `records[0]` is the *most recently inserted* — Morgan, since Morgan was added last. So `update_status` approves Morgan, not Taylor."

---

#### Step 12 — Run and verify the status report

**DO:**
```bash
python3 test_script.py
```

**CHECK:**
```
Records: 3

Status report:
  Approved: 1 records, $3,500.00
  Pending: 2 records, $1,650.00
```
Confirm this matches the hand trace: Morgan (3500) is the lone Approved record; Taylor (1200) plus Jordan (450) sum to 1,650 and both remain Pending.

**FIX:** If this is not your first run of the script, `data/requests.db` already has old rows in it from a previous run — that's expected, since `test_script.py` writes to the real database, not a temp one. Delete `data/requests.db` and re-run if you want a clean count of exactly 3.

---

#### Screenshot 3 checkpoint (15:10–15:30)

**SAY:** "Screenshot 3 — the `test_script.py` output showing the status report."

---

### PART 6 — Ritual (15:30–16:10)

#### Step 13 — Run the ritual

**DO:**
```bash
ruff format . && ruff check . && pytest -v
git add . && git commit -m 'lab 14: Python SQL integration' && git push
```

**CHECK:** No lint errors, all five tests pass, push succeeds, commit message includes "lab 14."

---

### SUBMISSION CHECKLIST (16:10–end)

- [ ] Screenshot 1: Python shell showing a record retrieved as a dict from `get_all_records()`
- [ ] Screenshot 2: `pytest -v` with all five tests green
- [ ] Screenshot 3: `test_script.py` output showing the status report
- [ ] `database.py` uses `?` placeholders on every query — never f-strings or concatenation
- [ ] Every function in `database.py` accepts an optional `db_file` parameter
- [ ] Git commit message includes "lab 14"
- [ ] GitHub repository URL pasted into Canvas
