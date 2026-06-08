# ISM3232 Lab W14: Python + SQL Integration

## YouTube Metadata

**Title:** Python + SQL Integration — Lab Walkthrough | ISM3232 Lab 14
**Description:**
Walkthrough of ISM3232 Module 14 Lab. We build all five database.py functions: create_table, add_record, get_all_records, update_status, and get_status_report. Every function uses ? placeholders, row_factory for dict access, and a db_file parameter for test isolation. Five pytest tests use tmp_path.

**Chapters:**
0:00 — What we're building
0:45 — The two rules: ? placeholders only, db_file parameter on every function
2:00 — create_table and add_record
4:30 — get_all_records with row_factory
6:00 — update_status and get_status_report
7:30 — Five pytest tests with tmp_path
9:30 — test_script.py and submission ritual

**Applies to:** ISM3232 Module 14

**Tags:** python sqlite3, python parameterized queries, python row_factory, pytest tmp_path, ISM3232, USF, python database functions, python SQL integration

---

## Script

### INTRO (0:00–0:45)

Lab 14 — Python + SQL Integration. We write all five `database.py` functions that your Streamlit app will call next week. Two rules apply to every function you write today.

---

### TWO NON-NEGOTIABLE RULES (0:45–2:00)

**Rule 1: Always use `?` placeholders — never f-strings in SQL.**

Wrong (SQL injection vulnerability):
```python
conn.execute(f"SELECT * FROM requests WHERE status = '{status}'")
```

Right (parameterized query):
```python
conn.execute("SELECT * FROM requests WHERE status = ?", (status,))
```

The `?` tells SQLite to treat the value as data, not SQL code. A user who enters `'; DROP TABLE requests; --` as a status gets that literal string stored — not a table drop.

**Rule 2: Every function must accept `db_file=DB_FILE`.**

This lets tests pass a temp database path instead of the development database.

---

### CREATE_TABLE AND ADD_RECORD (2:00–4:30)

```bash
cd ~/ism3232/module07_final_project
touch database.py tests/__init__.py tests/test_database.py
code database.py
```

```python
# database.py
import sqlite3

DB_FILE = "requests.db"


def create_table(db_file: str = DB_FILE) -> None:
    """Create the requests table if it does not exist."""
    with sqlite3.connect(db_file) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS requests (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                requester TEXT    NOT NULL,
                category  TEXT    NOT NULL,
                amount    REAL    NOT NULL,
                notes     TEXT    DEFAULT '',
                status    TEXT    DEFAULT 'Pending'
            )
        ''')


def add_record(requester: str, category: str, amount: float,
               notes: str = '', db_file: str = DB_FILE) -> None:
    """Insert a new request record with Pending status."""
    with sqlite3.connect(db_file) as conn:
        conn.execute(
            'INSERT INTO requests (requester, category, amount, notes) VALUES (?,?,?,?)',
            (requester, category, amount, notes)
        )
```

Test in the Python shell:
```python
>>> from database import create_table, add_record
>>> create_table()
>>> add_record("Taylor", "Travel", 1200, "Conference in Tampa")
```

---

### GET_ALL_RECORDS WITH ROW_FACTORY (4:30–6:00)

```python
def get_all_records(db_file: str = DB_FILE) -> list[dict]:
    """Return all records as a list of dicts."""
    with sqlite3.connect(db_file) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.execute('SELECT * FROM requests ORDER BY id DESC')
        return [dict(row) for row in cur.fetchall()]
```

`sqlite3.Row` is the key: without it, rows come back as tuples and you access `row[0]`, `row[1]`. With it, you get `row["requester"]`, `row["status"]` — much more readable, and it maps directly to what Streamlit's `st.dataframe()` expects.

Test in the shell:
```python
>>> from database import get_all_records
>>> records = get_all_records()
>>> records[0]["requester"]   # 'Taylor'
>>> records[0]["status"]      # 'Pending'
```

Screenshot 1: Python shell showing a record returned as a dict.

---

### UPDATE_STATUS AND GET_STATUS_REPORT (6:00–7:30)

```python
def update_status(record_id: int, new_status: str, db_file: str = DB_FILE) -> None:
    """Update the status of a specific record."""
    with sqlite3.connect(db_file) as conn:
        conn.execute(
            'UPDATE requests SET status = ? WHERE id = ?',
            (new_status, record_id)
        )


def get_status_report(db_file: str = DB_FILE) -> list[dict]:
    """Return count and total amount grouped by status."""
    with sqlite3.connect(db_file) as conn:
        cur = conn.execute(
            'SELECT status, COUNT(*) as count, SUM(amount) as total '
            'FROM requests GROUP BY status'
        )
        return [dict(row) for row in cur.fetchall()]
```

You now have all five functions. The `get_status_report` function is a single SQL GROUP BY query — what would take a Python loop and multiple passes over the data, SQL does in one scan.

---

### FIVE PYTEST TESTS WITH TMP_PATH (7:30–9:30)

`tmp_path` is a built-in pytest fixture that creates a fresh temporary directory for each test. This means every test gets its own empty database — no test can pollute another.

```python
# tests/test_database.py
import pytest
from database import create_table, add_record, get_all_records, update_status, get_status_report


def test_add_and_retrieve(tmp_path):
    db = str(tmp_path / "test.db")
    create_table(db)
    add_record("Taylor", "Travel", 1200, db_file=db)
    records = get_all_records(db)
    assert len(records) == 1
    assert records[0]["requester"] == "Taylor"


def test_default_status_is_pending(tmp_path):
    db = str(tmp_path / "test.db")
    create_table(db)
    add_record("Jordan", "Software", 450, db_file=db)
    records = get_all_records(db)
    assert records[0]["status"] == "Pending"


def test_update_status(tmp_path):
    db = str(tmp_path / "test.db")
    create_table(db)
    add_record("Morgan", "Equipment", 3500, db_file=db)
    record_id = get_all_records(db)[0]["id"]
    update_status(record_id, "Approved", db_file=db)
    assert get_all_records(db)[0]["status"] == "Approved"


def test_multiple_records(tmp_path):
    db = str(tmp_path / "test.db")
    create_table(db)
    add_record("A", "Travel", 100, db_file=db)
    add_record("B", "Travel", 200, db_file=db)
    add_record("C", "Travel", 300, db_file=db)
    assert len(get_all_records(db)) == 3


def test_status_report_groups_correctly(tmp_path):
    db = str(tmp_path / "test.db")
    create_table(db)
    add_record("A", "T", 500, db_file=db)
    add_record("B", "T", 600, db_file=db)
    r1_id = get_all_records(db)[0]["id"]   # most recent first
    update_status(r1_id, "Approved", db_file=db)
    report = get_status_report(db)
    statuses = {row["status"] for row in report}
    assert "Pending" in statuses
    assert "Approved" in statuses
```

Run: `pytest -v` — all five green.

Screenshot 2: `pytest -v` all five green.

---

### TEST_SCRIPT.PY AND RITUAL (9:30–11:00)

Write `test_script.py` to see everything working end-to-end in the development database:

```python
# test_script.py — manual smoke test, not part of pytest
from database import create_table, add_record, get_all_records, update_status, get_status_report

create_table()
add_record("Taylor", "Travel", 1200)
add_record("Jordan", "Software", 450)
add_record("Morgan", "Equipment", 3500)

# Approve the first record
records = get_all_records()
update_status(records[-1]["id"], "Approved")   # last inserted = earliest in ORDER BY DESC list

print("\nAll records:")
for r in get_all_records():
    print(f"  {r['requester']:<12} ${r['amount']:>8,.2f}  {r['status']}")

print("\nStatus report:")
for row in get_status_report():
    print(f"  {row['status']:<12} count={row['count']}  total=${row['total']:,.2f}")
```

Run: `python3 test_script.py`

Screenshot 3: `test_script.py` output showing the status report.

Ritual:
```bash
ruff format . && ruff check . && pytest -v
git add . && git commit -m 'lab 14: Python SQL integration' && git push
```

---

### SUBMISSION CHECKLIST (10:30–11:00)

- `database.py` with all five functions: `create_table`, `add_record`, `get_all_records`, `update_status`, `get_status_report`
- Every SQL query uses `?` placeholders — no f-strings in SQL
- Every function has `db_file=DB_FILE` parameter
- `get_all_records` uses `sqlite3.Row` and returns list of dicts
- Five pytest tests with `tmp_path`, all passing
- Screenshot 1: Python shell showing dict from `get_all_records()`
- Screenshot 2: `pytest -v` all five green
- Screenshot 3: `test_script.py` output with status report
- Commit includes "lab 14", GitHub URL to Canvas
