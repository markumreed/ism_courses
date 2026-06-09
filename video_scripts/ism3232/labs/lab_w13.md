# ISM3232 Lab W13: Capstone Design & SQL Foundations

## YouTube Metadata

**Title:** Capstone Design & SQL Foundations — Lab Walkthrough | ISM3232 Lab 13
**Description:**
Walkthrough of ISM3232 Module 13 Lab. We write the capstone project proposal (PROPOSAL.md, all 10 fields), run SQL fundamentals in the sqlite3 shell, design the capstone schema in schema.sql, and add a SQL cheatsheet to README.md.

Course page: https://markumreed.github.io/ism3232/docs/week13_lab.html

**Chapters:**
0:00 — What this lab covers
0:45 — PROPOSAL.md: 10 required fields and why each matters
5:00 — SQL fundamentals in the sqlite3 shell
7:30 — schema.sql: designing your capstone table
9:00 — README.md SQL cheatsheet
9:45 — Submission checklist

**Applies to:** ISM3232 Module 13

**Tags:** python capstone proposal, SQL schema design, sqlite3 shell, SQL CREATE TABLE, ISM3232, USF, python SQL foundations, python capstone project

---

## Script

### INTRO (0:00–0:45)

Lab 13 — Capstone Design and SQL Foundations. Two things must happen today: write your capstone proposal, and get comfortable with the sqlite3 shell. The proposal requires instructor sign-off before Week 14. If you start building without it, you will be building the wrong thing.

---

### PROPOSAL.MD — ALL 10 FIELDS (0:45–5:00)

```bash
cd ~/ism3232/module07_final_project
touch PROPOSAL.md && code PROPOSAL.md
```

Fill in every field. Vague proposals get rejected:

```markdown
# ISM3232 Capstone Project Proposal

## Student Name
[Your name]

## Business Domain
[One sentence: what real-world problem does your app solve?
Example: "A purchase request tracker for small business teams."]

## Main Entity
[The primary object your app manages — what is one "record"?
Example: "A PurchaseRequest: one request from one employee for one purchase."]

## Attributes (at least 4)
[List the attributes of your main entity with types]
- requester: str — the employee making the request
- category: str — Travel, Software, Equipment, etc.
- amount: float — dollar amount
- status: str = "Pending" — workflow state

## Methods (at least 4)
[List methods your main entity class will have]
- approve() — set status to "Approved"
- reject() — set status to "Rejected"
- requires_review() -> bool — return True if amount > threshold
- __repr__() -> str — readable string for debugging

## Manager Class
[Name and purpose]
- RequestManager: holds a list of requests, provides add, filter, total, and report

## SQL Tables
[List the tables you need, with key columns]
Table: requests
  - id: INTEGER PRIMARY KEY AUTOINCREMENT
  - requester: TEXT NOT NULL
  - category: TEXT NOT NULL
  - amount: REAL NOT NULL
  - status: TEXT DEFAULT 'Pending'
  - notes: TEXT

## Streamlit Features (must be exactly 5)
1. Submit a new request (Tab 1)
2. View all requests (Tab 2)
3. Filter by status (Tab 3)
4. Update status (Tab 4)
5. Status report with counts and totals (Tab 5)

## GenAI Feature
[One-sentence description of your AI feature]
Example: "Summarise a request's notes field into a one-sentence approval recommendation."

## Scope (what you are NOT building)
[Be explicit — this prevents scope creep]
Example: "No user authentication. No email notifications. No multi-user roles."
```

**Raise your hand when PROPOSAL.md is complete.** The instructor must sign off before you write any capstone database code.

---

### SQL FUNDAMENTALS IN THE SQLITE3 SHELL (5:00–7:30)

While waiting for sign-off, run these SQL operations in the shell:

```bash
sqlite3 lab13.db
```

In the shell:

```sql
-- Create a practice table
CREATE TABLE employees (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    name      TEXT    NOT NULL,
    dept      TEXT    NOT NULL,
    salary    REAL    NOT NULL,
    status    TEXT    DEFAULT 'Active'
);

-- Insert five rows
INSERT INTO employees (name, dept, salary) VALUES ('Taylor', 'Sales',   72000);
INSERT INTO employees (name, dept, salary) VALUES ('Jordan', 'Eng',     95000);
INSERT INTO employees (name, dept, salary) VALUES ('Morgan', 'Sales',   68000);
INSERT INTO employees (name, dept, salary) VALUES ('Casey',  'Finance', 81000);
INSERT INTO employees (name, dept, salary) VALUES ('Riley',  'Eng',     110000);

-- Read all rows
SELECT * FROM employees;

-- Filter
SELECT name, salary FROM employees WHERE dept = 'Eng';

-- Aggregate
SELECT dept, COUNT(*) as count, SUM(salary) as total, AVG(salary) as avg
FROM employees
GROUP BY dept;

-- Update one row
UPDATE employees SET status = 'Inactive' WHERE id = 3;
SELECT * FROM employees WHERE status = 'Inactive';

-- Delete one row (and verify)
DELETE FROM employees WHERE id = 5;
SELECT COUNT(*) FROM employees;

.quit
```

Screenshot: the sqlite3 shell showing the GROUP BY result.

Important syntax rules:
- SQL keywords are UPPERCASE by convention (not required)
- `?` placeholders are used in Python, not here in the shell
- `INTEGER PRIMARY KEY AUTOINCREMENT` is the standard pattern for ID columns
- `DEFAULT 'Pending'` means new rows get that value if you don't specify one

---

### SCHEMA.SQL FOR YOUR CAPSTONE (7:30–9:00)

```bash
touch schema.sql && code schema.sql
```

Write the CREATE TABLE statement for your actual capstone domain. Example:

```sql
-- schema.sql
CREATE TABLE IF NOT EXISTS requests (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    requester  TEXT    NOT NULL,
    category   TEXT    NOT NULL,
    amount     REAL    NOT NULL,
    notes      TEXT,
    status     TEXT    DEFAULT 'Pending',
    created_at TEXT    DEFAULT (datetime('now'))
);
```

`IF NOT EXISTS` is important — it means running the file twice won't error.

Test it:

```bash
sqlite3 capstone.db
.read schema.sql
.schema
INSERT INTO requests (requester, category, amount) VALUES ('Taylor', 'Travel', 1200);
SELECT * FROM requests;
.quit
```

Screenshot: the sqlite3 shell showing `.schema` output + test INSERT/SELECT.

---

### README.MD SQL CHEATSHEET (9:00–9:45)

Create `README.md` with a SQL reference section:

```markdown
# ISM3232 Capstone Project

## SQL Quick Reference

| Operation         | SQL                                              |
|-------------------|--------------------------------------------------|
| Create table      | CREATE TABLE IF NOT EXISTS t (id INTEGER PK)     |
| Insert row        | INSERT INTO t (col1, col2) VALUES (?, ?)         |
| Read all          | SELECT * FROM t ORDER BY id DESC                 |
| Filter            | SELECT * FROM t WHERE status = ?                 |
| Update            | UPDATE t SET status = ? WHERE id = ?             |
| Delete            | DELETE FROM t WHERE id = ?                       |
| Count per group   | SELECT status, COUNT(*) FROM t GROUP BY status   |
| Sum per group     | SELECT status, SUM(amount) FROM t GROUP BY status|
```

---

### SUBMISSION CHECKLIST (9:45–11:00)

- `PROPOSAL.md` in repo, all 10 fields completed, instructor sign-off obtained
- `schema.sql` with `CREATE TABLE IF NOT EXISTS` for your capstone
- `README.md` with SQL cheatsheet
- Screenshot: sqlite3 shell showing GROUP BY report from the practice table
- Screenshot: sqlite3 shell showing `.schema` + test INSERT/SELECT on capstone schema
- Commit includes "lab 13", GitHub URL to Canvas
