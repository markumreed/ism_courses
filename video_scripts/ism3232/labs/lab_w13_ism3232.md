# ISM3232 Lab W13: Capstone Design & SQL Foundations

## YouTube Metadata

**Title:** Capstone Proposal & SQL Foundations — Full Lab Walkthrough | ISM3232 Lab 13
**Description:**
Step-by-step, test-as-you-go walkthrough of ISM3232 Module 13 Lab. Complete all 10 fields of the capstone proposal, run CREATE TABLE / INSERT / SELECT / WHERE / UPDATE / GROUP BY in the sqlite3 shell one statement at a time, design your own capstone schema.sql, add a SQL cheatsheet to README.md, then commit and push.

Course page: https://markumreed.github.io/ism3232/docs/week13_lab.html

**Chapters:**
0:00 — Why the proposal needs sign-off before Week 14
0:45 — Step 1: project setup for module07_final_project
1:40 — Step 2: fill in the proposal's business problem fields
3:20 — Step 3: fill in classes, tables, and Streamlit features
5:00 — Step 4: raise your hand — proposal sign-off
5:20 — Step 5: open the sqlite3 shell and create a table
6:40 — Step 6: insert three records
7:30 — Step 7: turn on column mode and select all
8:10 — Step 8: filter with WHERE
8:40 — Step 9: update a record and re-select
9:20 — Step 10: the GROUP BY aggregate report
10:20 — Screenshot 1 checkpoint
10:40 — Step 11: write your capstone schema.sql
12:10 — Step 12: test it — read, insert, select
13:20 — Screenshot 2 checkpoint
13:40 — Step 13: add the SQL cheatsheet to README.md
14:40 — Step 14: commit and push
15:10 — Submission checklist

**Applies to:** ISM3232 Module 13

**Tags:** sqlite3 tutorial, sql create table insert select, sql where group by, python capstone proposal, ISM3232, USF, sql cheatsheet beginners

---

## How to Use This Script

**SAY** it, **DO** it, **CHECK** the exact output, **FIX** it if it doesn't match — then move to the next step.

---

## Script

### INTRO (0:00–0:45)

**SAY:** "Lab 13 — capstone design and SQL foundations. Two things happen today: you propose your capstone project, and you learn SQL for the first time by typing it directly into a live database shell. The proposal needs instructor sign-off before Week 14 — vague proposals lead to systems that are impossible to finish in four weeks, so all 10 fields get filled in honestly, right now."

---

### PART 1 — Capstone Project Proposal (0:45–5:20)

#### Step 1 — Project setup

**DO:**
```bash
cd ~/ism3232/module07_final_project
python3 -m venv .venv && source .venv/bin/activate
pip install pytest ruff && pip freeze > requirements.txt
echo '.venv/' > .gitignore && echo '__pycache__/' >> .gitignore
echo '*.db' >> .gitignore
touch PROPOSAL.md && code PROPOSAL.md
```

**CHECK:** Note the third `.gitignore` line — `*.db` — is new this week: capstone SQLite database files shouldn't be committed to Git any more than `.venv/` should, since they're generated data, not source.

---

#### Step 2 — Business problem fields

**SAY:** "First half of the proposal — what you're building and why, in plain language before any technical detail."

**DO:**
```markdown
# ISM3232 Capstone Project Proposal
# Author: [Your Name]

## Project Name
[Give your system a clear, descriptive name]

## Business Problem
[What problem does this solve? Who has this problem? 2-3 sentences.]

## Primary User
[Who will use this system? Be specific.]

## Records Stored
[What data is stored? Name every type of record.]

## Business Rules
[At least 2 explicit rules. e.g., 'Requests over $1000 require manager approval']
1.
2.
```

**CHECK:** Read your own "Business Rules" section back out loud — each rule needs to be specific enough to become a `WHERE` clause or a Python `if` statement next month. "Requests need review sometimes" is too vague; "requests over $1000 require manager approval" is exactly specific enough.

---

#### Step 3 — Classes, tables, and Streamlit features

**DO:**
```markdown
## OOP Classes
[List each class with key attributes and methods]
- Class 1: [name] | attributes: [...] | methods: [...]
- Class 2: [name] | attributes: [...] | methods: [...]

## SQL Tables
[List each table with columns and types]
- Table 1: [name] | columns: [...]

## Streamlit Features
1. Add a record
2. View all records
3. Filter records
4. Update status
5. Display a report

## GenAI Feature
[What will AI do? e.g., 'Summarise a request description in one sentence']

## Out of Scope
[What are you explicitly NOT building?]
```

**CHECK:** Cross-reference your "OOP Classes" section against Module 12's design.md format — the classes you propose here are the ones you'll actually build in the coming weeks, so if a class here doesn't map to a clear attribute list and method list, that's a sign the proposal needs another pass before sign-off.

---

#### Step 4 — Raise your hand for sign-off

**SAY:** "Now stop and raise your hand. All 10 fields need instructor review before you're cleared to start building capstone code in Week 14."

**CHECK:** Proposal signed off.

---

### PART 2 — SQL Fundamentals (5:20–10:20)

#### Step 5 — Open the shell and create a table

**SAY:** "Now, completely separate from the proposal — first contact with SQL, live, in a real database shell."

**DO:**
```bash
sqlite3 lab13.db
```
Inside the shell:
```sql
CREATE TABLE requests (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    requester TEXT    NOT NULL,
    category  TEXT    NOT NULL,
    amount    REAL,
    status    TEXT    DEFAULT 'Pending'
);
```

**CHECK:** No output on success — SQLite is quiet the same way `mkdir` was back in Week 1. Read the column definitions out loud: "`id` auto-increments and is the primary key. `requester` and `category` are required text — `NOT NULL`. `amount` is a real number. `status` defaults to `'Pending'` if you don't specify one — same default behavior as `BusinessRequest.status` back in Week 10, just enforced by the database instead of `__init__`."

**FIX:** If `sqlite3: command not found`, install it — macOS ships it by default; Ubuntu: `sudo apt install sqlite3`.

---

#### Step 6 — Insert three records

**DO:**
```sql
INSERT INTO requests (requester, category, amount) VALUES ('Taylor', 'Travel', 1200);
INSERT INTO requests (requester, category, amount) VALUES ('Jordan', 'Equipment', 450);
INSERT INTO requests (requester, category, amount) VALUES ('Morgan', 'Software', 3500);
```

**CHECK:** No output — three silent inserts. Note that `id` and `status` were never specified — `id` auto-increments to 1, 2, 3, and `status` falls back to its `'Pending'` default for all three.

---

#### Step 7 — Turn on column mode and select all

**SAY:** "By default the shell's output is cramped — two settings fix that before we look at any data."

**DO:**
```sql
.mode column
.headers on
SELECT * FROM requests;
```

**CHECK:**
```
id  requester  category   amount  status
--  ---------  ---------  ------  -------
1   Taylor     Travel     1200.0  Pending
2   Jordan     Equipment  450.0   Pending
3   Morgan     Software   3500.0  Pending
```
Aligned columns with a header row — confirms all three inserts landed with the expected auto-generated `id` values and default `status`.

---

#### Step 8 — Filter with WHERE

**SAY:** "`WHERE` is SQL's version of the `if rec['amount'] > LIMIT` filter from Week 6 — but the database does the filtering, not a Python loop."

**DO:**
```sql
SELECT * FROM requests WHERE amount > 1000;
```

**CHECK:**
```
id  requester  category  amount  status
--  ---------  --------  ------  -------
1   Taylor     Travel    1200.0  Pending
3   Morgan     Software  3500.0  Pending
```
Only Taylor and Morgan — Jordan's $450 doesn't clear the threshold.

---

#### Step 9 — Update a record and re-select

**SAY:** "`UPDATE` changes existing rows — the SQL equivalent of calling `.approve()` on a `BusinessRequest` instance, except this mutates a row in a table instead of an attribute on an object."

**DO:**
```sql
UPDATE requests SET status = 'Approved' WHERE id = 1;
SELECT * FROM requests;
```

**CHECK:**
```
id  requester  category   amount  status
--  ---------  ---------  ------  --------
1   Taylor     Travel     1200.0  Approved
2   Jordan     Equipment  450.0   Pending
3   Morgan     Software   3500.0  Pending
```
Only row 1's status changed — the `WHERE id = 1` clause scoped the update to exactly one row, the same way a specific object reference scoped `.approve()` to exactly one instance back in Week 10.

---

#### Step 10 — The GROUP BY aggregate report

**SAY:** "Last SQL statement for today — an aggregate report, grouped by status, computing a count and a sum per group in one query."

**DO:**
```sql
SELECT status, COUNT(*) as count, SUM(amount) as total FROM requests GROUP BY status;
```

**CHECK:**
```
status    count  total
--------  -----  ------
Approved  1      1200.0
Pending   2      3950.0
```
Two groups — confirm the math: Pending's total is Jordan (450) plus Morgan (3500), which is 3,950. This single `SELECT ... GROUP BY` line is doing the same job as `RequestManager.total_amount()` plus `list_by_status()` combined from Week 11 — SQL aggregates in one line what took several lines of Python.

Exit the shell:
```sql
.quit
```

---

#### Screenshot 1 checkpoint (10:20–10:40)

**SAY:** "Screenshot 1 — the sqlite3 shell showing the final `SELECT` and the `GROUP BY` report."

---

### PART 3 — Design Your Capstone Schema (10:40–13:40)

#### Step 11 — Write schema.sql

**SAY:** "Now design the real thing — the table(s) your actual capstone will use, based on the 'SQL Tables' field you filled in during the proposal."

**DO:**
```bash
touch schema.sql && code schema.sql
```
Write your own `CREATE TABLE` statement(s), using appropriate types (`TEXT`, `INTEGER`, `REAL`), `NOT NULL` where required, and a `status` column with a default value — following the exact pattern from Step 5's `requests` table.

**CHECK:** Read your schema back out loud and confirm every column has an explicit type, and that any column your business rules depend on (like a status or amount field) is present and correctly typed.

---

#### Step 12 — Test it — read, insert, select

**DO:**
```bash
sqlite3 capstone.db
```
```sql
.read schema.sql
.schema
INSERT INTO [yourtable] ([cols]) VALUES ([values]);
SELECT * FROM [yourtable];
.quit
```

**CHECK:** `.schema` prints back your `CREATE TABLE` statement exactly as written in `schema.sql` — confirming the file is valid SQL. The `INSERT` followed by `SELECT` proves the table actually accepts and stores a row correctly, not just that it was created.

**FIX:** If `.read schema.sql` produces no output and `.schema` shows nothing, check for a missing semicolon at the end of your `CREATE TABLE` statement.

---

#### Screenshot 2 checkpoint (13:20–13:40)

**SAY:** "Screenshot 2 — the sqlite3 shell showing your schema, a test insert, and the select."

---

### PART 4 — sqlite3 Shell Reference (13:40–14:40)

#### Step 13 — Add the SQL cheatsheet to README.md

**SAY:** "One line per operation — your own reference for the rest of the SQL unit, same pattern as the command-reference README from Week 2."

**DO:** In `README.md`:
```markdown
## SQL Reference

- `CREATE TABLE`  — define a table
- `INSERT INTO`   — add a record
- `SELECT *`      — retrieve all records
- `WHERE`         — filter records
- `UPDATE ... SET`— change a value
- `ORDER BY`      — sort results
- `GROUP BY`      — aggregate by column
- `COUNT / SUM / AVG` — aggregate functions
```

**CHECK:** Confirm all eight operations from today's shell session are represented — that's every SQL keyword you actually typed in Part 2.

---

### PART 5 — Ritual and Push (14:40–15:10)

#### Step 14 — Commit and push

**SAY:** "No `ruff`/`pytest` step this week — there's no Python logic to lint or test yet, just the proposal and the schema."

**DO:**
```bash
git add . && git commit -m 'lab 13: proposal and SQL schema' && git push
```

**CHECK:** Push completes without error, commit message includes "lab 13."

---

### SUBMISSION CHECKLIST (15:10–end)

- [ ] `PROPOSAL.md` — all 10 fields completed, with instructor sign-off
- [ ] `schema.sql` — the `CREATE TABLE` statement for your capstone
- [ ] Screenshot: sqlite3 shell showing your schema, a test insert, and the `GROUP BY` report
- [ ] `README.md` SQL cheatsheet with all eight operations
- [ ] Git commit message includes "lab 13"
- [ ] GitHub repository URL pasted into Canvas
