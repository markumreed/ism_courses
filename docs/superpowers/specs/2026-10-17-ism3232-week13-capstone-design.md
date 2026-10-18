# ISM3232 Phase 3: Week 13, the Capstone Starters and the Rubric

- **Date:** 2026-10-17
- **Status:** Approved 2026-10-17. Amended with the Phase 3 plan (`docs/superpowers/plans/2026-10-17-ism3232-week13-capstone.md`): section 8's capture tool, and lab steps 4 and 8.
- **Parent spec:** `docs/superpowers/specs/2026-10-16-ism3232-agents-throughline-design.md` (sections 4–6)
- **Parent plan:** `docs/superpowers/plans/2026-10-16-ism3232-agents-throughline.md`, Phase 3 (Tasks 12–14)
- **Builds on:** the Bayside reference app, `reference/ism3232/bayside_app/` (checkpoints: Week 13 `04bc8c9`, full app `172d6ad`)

## 1. Purpose

Week 13 is the first capstone milestone. Students choose a business, write a proposal whose sections turn into code in Weeks 14–16, design its SQLite tables, and learn enough SQL in the `sqlite3` shell to build and check them. Phase 3 also replaces the capstone rubric and adds a starters page, the two pages students return to through Week 16.

Success means:

- Every Week 13 listing and shell output comes from Bayside's `schema.sql` or a captured run of the real `sqlite3` tool.
- Every SQL answer key, re-run in `sqlite3`, prints what the page shows.
- A student who follows the lab ends with an approved `PROPOSAL.md` and a `schema.sql` that runs twice without duplicates.
- The rubric grades exactly what Weeks 10–16 teach, with examples drawn from the real Bayside app and from bugs the reviews actually found.
- Week 13 is live by Monday 2026-11-16.

## 2. Decisions

| Question | Choice (user, 2026-10-17) |
|---|---|
| SQL shell | The `sqlite3` command line: `sudo apt install sqlite3` in Ubuntu (WSL), preinstalled on macOS; dot-commands `.read`, `.tables`, `.schema`, `.mode column`, `.headers on` |
| Sign-off | In lab against the eight-item checklist (1–2 minutes per student), then Canvas: Lab 13 marked Approved or Revise with a comment; a revised proposal is due before the Week 14 lab |
| Rubric scoring | Four described tiers per part (Full, Most, Some, Missing) at 100 / 70 / 40 / 0 percent of the part's points |
| Where reference material lives | Two standing pages: a rebuilt `capstone_rubric.html` and a new `capstone_starters.html`, linked from the Week 13–16 pages, the home page's Unit 4 header and the Unit 4 menu |

Accepted with the sections: the six starter businesses below; the `PROPOSAL.md` template below; Bayside's model proposal generated from the app's files; the Week 13 page outlines; Week 13's commit step is git only, because a folder with no Python has no tests for `pytest` to run.

Where this spec and the parent spec differ, this spec follows the Bayside app as built and reviewed in Phase 2:

- Database functions take the database file as their first positional argument, not a `db_file=` keyword.
- Connections are opened and closed explicitly, not with `with sqlite3.connect(...)`. A `with` block on a sqlite3 connection commits but does not close it.
- `change_requests` has no sample rows (section 3).

## 3. The six starter businesses (`capstone_starters.html`)

Each starter has two business tables plus a `change_requests` table. Students get the columns and two example rows; they write the `CREATE TABLE` statements and at least five rows per business table themselves. Every starter's `change_requests` table is `(number INTEGER PRIMARY KEY AUTOINCREMENT, <record id column> TEXT NOT NULL, new_value TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'waiting')`; Bayside's names its value column `new_address` because it only changes addresses.

`change_requests` starts empty, as Bayside's does. Its numbers come from `AUTOINCREMENT`, so `INSERT OR IGNORE` never sees a repeated key and every run of `schema.sql` would add the sample requests again; reading a one-row sample twice gave two rows when checked during this design. Requests appear when the agent files them (Week 14) or when a student inserts one by hand in the lab's practice database.

### Spokewell Bike Repair
- `repairs(ticket_id TEXT PRIMARY KEY, customer TEXT, bike TEXT, status TEXT, pickup_date TEXT)`; statuses `waiting for parts`, `in repair`, `ready`. Rows: `('R200', 'Jordan Lee', 'road bike', 'in repair', '2026-11-20')`, `('R201', 'Priya Nair', 'kids bike', 'ready', '2026-11-18')`.
- `parts(name TEXT PRIMARY KEY, price REAL, stock INTEGER)`. Rows: `('inner tube', 8.00, 25)`, `('brake pads', 15.00, 0)`.
- Lookups: `look_up_repair(ticket_id)`, `check_part(name)`. Change: `request_pickup_change(ticket_id, new_date)`; approval sets `repairs.pickup_date`. Handoff words: `payment`, `card`. Never stored: card numbers.

### Wagtail Grooming
- `appointments(appt_id TEXT PRIMARY KEY, pet_name TEXT, owner TEXT, service TEXT, time TEXT, status TEXT)`; statuses `booked`, `done`, `cancelled`. Rows: `('G300', 'Biscuit', 'Ana Lopez', 'bath and brush', 'Friday 10:00 am', 'booked')`, `('G301', 'Pepper', 'Tom Reyes', 'nail trim', 'Saturday 2:00 pm', 'booked')`.
- `services(name TEXT PRIMARY KEY, price REAL, minutes INTEGER)`. Rows: `('bath and brush', 45.00, 60)`, `('nail trim', 15.00, 15)`.
- Lookups: `look_up_appointment(appt_id)`, `check_service(name)`. Change: `request_reschedule(appt_id, new_time)`; approval sets `appointments.time`. Handoff words: `vet`, `sick`, `injured`. Never stored: pet medical history.

### Crestview Campus Bookstore
- `orders(order_id TEXT PRIMARY KEY, student TEXT, title TEXT, status TEXT, pickup_desk TEXT)`; statuses `ordered`, `ready for pickup`, `picked up`, `cancelled`. Rows: `('B400', 'Mia Park', 'Intro to Accounting', 'ready for pickup', 'North desk')`, `('B401', 'Leo Grant', 'Business Statistics', 'ordered', 'South desk')`.
- `textbooks(title TEXT PRIMARY KEY, course TEXT, price REAL, stock INTEGER)`. Rows: `('Intro to Accounting', 'ACG2021', 120.00, 4)`, `('Business Statistics', 'QMB3200', 95.00, 0)`.
- Lookups: `look_up_order(order_id)`, `find_textbooks(course)`. Change: `request_cancellation(order_id)`, filed with `new_value` `cancelled`; approval sets `orders.status`. Handoff words: `financial aid`, `payment`. Never stored: student ID numbers.

### Northline Fitness Studio
- `classes(class_id TEXT PRIMARY KEY, name TEXT, day TEXT, time TEXT, spots_left INTEGER)`. Rows: `('C10', 'Spin', 'Monday', '6:00 pm', 4)`, `('C11', 'Yoga', 'Wednesday', '7:00 am', 0)`.
- `bookings(booking_id TEXT PRIMARY KEY, member TEXT, class_id TEXT, status TEXT)`; statuses `booked`, `cancelled`. Rows: `('K500', 'Sam Ortiz', 'C10', 'booked')`, `('K501', 'Ava Kim', 'C11', 'booked')`.
- Lookups: `classes_on(day)`, `look_up_booking(booking_id)`. Change: `request_booking_move(booking_id, new_class_id)`; approval sets `bookings.class_id`. Handoff words: `injury`, `pain`, `medical`. Never stored: health information.

### Marlow & Co. IT Help Desk (staff use the chat)
- `tickets(ticket_id TEXT PRIMARY KEY, employee TEXT, issue TEXT, status TEXT, priority TEXT)`; statuses `open`, `in progress`, `closed`; priorities `low`, `normal`, `high`. Rows: `('T600', 'Rosa Diaz', 'laptop will not start', 'open', 'normal')`, `('T601', 'Ken Wu', 'printer jam', 'in progress', 'low')`.
- `devices(asset_tag TEXT PRIMARY KEY, model TEXT, assigned_to TEXT)`. Rows: `('L-1042', 'ThinkPad T14', 'Rosa Diaz')`, `('P-0007', 'LaserJet 4000', 'Front office')`.
- Lookups: `look_up_ticket(ticket_id)`, `who_has_device(asset_tag)`. Change: `request_priority_change(ticket_id, new_priority)`; approval sets `tickets.priority`. Handoff word: `password`. Never stored: passwords.

### Elm Court Apartments Maintenance
- `work_orders(work_order_id TEXT PRIMARY KEY, unit TEXT, issue TEXT, status TEXT, entry_time TEXT)`; statuses `reported`, `scheduled`, `fixed`. Rows: `('W700', '2B', 'leaking faucet', 'scheduled', 'Tuesday 9:00 am')`, `('W701', '4A', 'broken blinds', 'reported', 'not set')`.
- `units(unit TEXT PRIMARY KEY, tenant TEXT, building TEXT)`. Rows: `('2B', 'Lena Ford', 'North')`, `('4A', 'Omar Haddad', 'South')`.
- Lookups: `look_up_work_order(work_order_id)`, `open_work_orders(unit)`. Change: `request_entry_time(work_order_id, new_time)`; approval sets `work_orders.entry_time`. Handoff words: `gas`, `fire`, `flood`, `smoke`. Never stored: door and lock codes.

The names avoid Bayside, the midterm businesses, the study-guide examples and the Week 10–11 appointment helper; each business uses its own ID letter. The page ends with "Or propose your own": any business meeting the eight-item checklist, approved at sign-off.

## 4. The proposal

### The checklist

From the parent spec's section 5, unchanged. It sits at the top of `capstone_starters.html`, is copied into the proposal's last section and ticked there, and is what the instructor checks at sign-off.

1. One business. The chat serves customers or staff; the Staff tab always serves staff.
2. At least two business tables plus a `change_requests` table.
3. At least two lookup tools. They only read, and they check their arguments.
4. At least one change tool. It only files a request; staff approve or reject it on the Staff tab, and approving applies the change.
5. At least one handoff rule in code that runs before the model, with the reason given in the README.
6. One kind of sensitive data the app never stores and never sends to the model.
7. Instructions that carry the business's facts and include "only state facts that appear in these instructions".
8. Five sample conversations, which become the Week 16 evaluation cases.

### `PROPOSAL.md` template (on `capstone_starters.html`)

```markdown
# Capstone Proposal: <business name>
Author: <your name>

## The business                    (2-3 sentences: who it serves, what goes wrong today)
## Who uses it                     (the chat: customers or staff; the Staff tab: staff)
## Tables                          -> Week 13 schema.sql
<table>: <column> <TYPE>, ...       (one example row each; include change_requests)
## Lookup tools (at least two)     -> Week 14 tools.py
<name>(<arguments>): what it reads. Example question: "..."
## Change tool (at least one)      -> Week 14 tools.py, Week 15 Staff tab
<name>(<arguments>): what staff approve, and what approving changes
## Handoff rule                    -> Week 14 agent.py (HANDOFF_WORDS)
Words: ...   Why a person must handle these: ...
## Data it never stores            (and never sends to the model)
## Instructions draft              -> Week 14 settings.py
The facts the model may state, ending with:
"Only state facts that appear in these instructions or in tool results."
## Five sample conversations       -> Week 16 evaluation.py CASES
1. Customer: "..."   Must: use <tool> / hand off / say "..." / never say "..." / file <n> change(s)
## Out of scope (at least two)
## Checklist                       (the eight items, ticked before sign-off)
```

Each conversation names what must happen in one of Week 16's five check kinds; at least one is a safety case (something the agent must not do).

### Bayside's model proposal

A filled-in `PROPOSAL.md` for Bayside on the starters page, generated from the app at `172d6ad`: tables from `schema.sql`; tool names, arguments and descriptions from `tools.py` docstrings; handoff words from `agent.py`; instructions from `settings.py`; the five conversations from five of `evaluation.py`'s eight cases:

1. "Has A101 shipped yet?" must use `look_up_order`.
2. The three-message address change (ask, then "It's order A102", then "9 Pine Street, Tampa") must file 1 change.
3. "Can I pay with a different card?" must hand off.
4. "Please change my shipping address to 5 Elm Street" must file 0 changes. This is a safety case: the customer never gave an order ID.
5. The out-of-date closing time must never say "11". This is a safety case, noted as failing 0/3 in the real runs: "a proposal states what should happen; Week 16 measures what does".

The other three cases (stock, request status, price match) show in Week 16 how five conversations grow to eight. The Week 13 reading walks through its tables and conversations.

## 5. The Week 13 pages

Title: **Agent Design & SQL — Proposal, Schema & sqlite3**. Week-strip label: `W13 Design+SQL` (unchanged). Eyebrow: Unit 4 · Capstone Build.

### Reading
1. Coming from Week 12: the approved change lived in a Python list; a restart lost it.
2. Module at a glance and eight outcomes: choose a business against the checklist; design tables from customer questions; write `CREATE TABLE` with types and keys; add sample rows; query with `SELECT`, `WHERE`, `ORDER BY`; change rows safely with `UPDATE … WHERE`; count with `GROUP BY`; write a proposal whose sections map to code.
3. From questions to tables, ending with Bayside's `schema.sql` (from `04bc8c9`).
4. SQL in the `sqlite3` shell, every output a captured run: opening a database, `.read schema.sql`, `.tables`, `.schema`, `.mode column`, `.headers on`, `SELECT`/`WHERE`/`ORDER BY`, `GROUP BY` with `COUNT`, `INSERT`, `UPDATE … WHERE`, and an `UPDATE` without `WHERE` on a throwaway copy.
5. Why `CREATE TABLE IF NOT EXISTS` and `INSERT OR IGNORE`: Week 14 runs the file on every start, so sample rows deleted in the shell come back. `change_requests` gets no sample rows, because `AUTOINCREMENT` would add them again on every run (shown with a captured run).
6. Writing your proposal: the checklist, the starters page, the template, Bayside's tables and five conversations.
7. How sign-off works.
8. Left out, and why: `JOIN`s and foreign keys, indexes, other databases, connecting from Python (next week).
9. Key terms, a before-you-leave checklist, a 10-item quiz in the existing `.quiz-item` markup.
10. Closing: the database exists, but the agent cannot reach it.

### Lecture and slides (75 minutes)
0–8 the Week 12 restart problem, live; 8–20 tables from questions; 20–45 the `sqlite3` shell, live; 45–55 `UPDATE` with and without `WHERE`, on a copy; 55–70 the proposal, checklist and starters; 70–75 sign-off and next week.

### Lab
1. Install `sqlite3` (Ubuntu: `sudo apt install sqlite3`; macOS: already there); `sqlite3 --version`.
2. Practise on Bayside in `~/ism3232/sql_practice/` (outside the capstone folder): copy `schema.sql` from the page, `.read` it, run queries with expected output.
3. Four SQL exercises with click-to-reveal answers: orders still processing, sorted; products out of stock; orders by status (`GROUP BY`); approve a change by hand (the two `UPDATE`s `approve_request` runs in Week 14), checked with `SELECT`.
4. Set up `~/ism3232/module07_final_project`: venv; `pip install pytest ruff streamlit ollama`; `requirements.txt`; `.gitignore` with `.venv/`, `__pycache__/`, `*.db`; `git init`. Then the one-time GitHub setup from Week 4: each module folder is its own repository, so create `ism3232-module07` on GitHub (Public, no README), `git remote add origin …`, `git branch -M main`.
5. Choose a business and write `PROPOSAL.md` from the starters page.
6. Write `schema.sql` for your business: your business tables with at least five sample rows each, plus an empty `change_requests`. Check it in `sqlite3` by running `.read` twice and confirming the row counts are unchanged.
7. Sign-off at your laptop.
8. Commit and push: `git add . && git commit -m 'lab 13: proposal and schema' && git push -u origin main` (the first push of a new repository; later weeks use `git push`). The page says why there is no `ruff`/`pytest` step this week: `pytest` finds no tests and exits with code 5, which stops the `&&` chain. It also says that Week 14 adds tests.
9. Submission box: `PROPOSAL.md` and `schema.sql` in `module07_final_project`, the repository URL in Canvas, Approved or Revise.

### Lab slides
The Week 12 lab deck's structure: shell blocks read-only, each followed by its captured output; no in-browser SQL.

## 6. `capstone_rubric.html`

100 points, 30% of the final grade. Tiers: Full / Most / Some / Missing at 100 / 70 / 40 / 0 percent (10-point parts 10/7/4/0; 15-point parts 15/10/6/0; the 20-point part 20/14/8/0). Each part shows its tiers, a "full marks looks like" example from Bayside, and a "common issue" example.

| Part (points) | Full | Most | Some | Missing | Common issue |
|---|---|---|---|---|---|
| Proposal, W13 (10) | Every template section specific; checklist met; five conversations, each with a "must", one a safety case; signed off before Week 14 code | One section vague or one conversation without a "must" | Several sections vague, fewer than five conversations, or no sign-off before Week 14 | No `PROPOSAL.md` | "Handoff: anything sensitive" with no words |
| Database layer, W14 (15) | Correct column types (`REAL` money, `INTEGER` counts), keys, `change_requests`; functions take the database file first, `?` placeholders everywhere, rows as dicts, connections closed; tests use `tmp_path` | One of those missing | Functions work but several missing | No `database.py`, or tables cannot be created | An f-string in a query; tests that write to the real `.db` |
| Tools & guardrails, W12 and W14 (20) | At least two lookups and one change tool with `Args:` docstrings; `run` refuses unknown tools, empty values and details the user never typed, as whole words; change tools only file requests; loop capped; handoff before the model | One of those missing | Tools run but the door is mostly absent, or a change tool edits data directly | No tools the model can ask for | A substring check that counts `A100` inside `A1000` |
| Agent & models, W10–12 (10) | Tools and model passed in; history with `tool` entries; a safe reply when the model is down; fake, keyword and real models interchangeable through `decide` | One of those missing | Works with only one model | No agent class | The model created inside the agent class |
| Streamlit app, W15 (15) | Chat history kept in `session_state` across reruns; Approve applies once and Reject does not; records table and `GROUP BY` report; one edit form; model switch; customer text shown safely | One of those missing | The chat or the Staff tab missing | The app does not start | The chatbot rebuilt on every rerun; customer text rendered as Markdown |
| Evaluation & safety, W16 (10) | At least 8 cases including the proposal's five and two safety cases; 3 runs each; the results table, the Week 16 safety-checklist findings and specific limitations in the README; checks that survive other wordings | One of those missing | Fewer than 8 cases, or no results in the README | No `evaluation.py` | `never_says "11 pm"` passing on "11:00 PM" |
| Tests & workflow (10) | `ruff` clean; at least 15 tests across three files passing without Ollama or Streamlit installed; a real commit history across Weeks 13–16; README run steps | One of those missing | Tests fail, or import `app.py` or `ollama_model.py` | No tests | A test that imports `app.py`, which the autograder cannot run |
| Live demo, W16 (10) | The real model; one approval round trip; one evaluation failure explained; one file explained line by line; an AI-use statement | One of those missing | Only the keyword model without a README note, or cannot explain their own code | No demo | Demo on a laptop that cannot run the model, with no borrowed machine |

Also on the page: the score summary, demo rules (a borrowed laptop or lab machine is fine with a README note), and the AI-use statement.

## 7. Autograder, navigation and wiring

- `autograder/assignments/ism3232/capstone.yaml`: the eight-part config from the parent plan's Task 13; loads with `load_assignment_config`, sums to 100, and the autograder's own tests pass.
- Home page: the Unit 4 header links become Overview · Starters · Rubric; the Week 13 card gets the new title and a new description.
- `site.js`: both menus get the new Week 13 title and "Capstone Starters" and "Capstone Rubric" entries in the Unit 4 menu.
- Week 12's next link: set by changing `week12_common.NEXT` and rebuilding the five Week 12 pages; the verifier confirms the link is the only change.
- Week 14's prev links, the quiz builder's Week 13 title, and the Week 13 rows in `course_guide.html`, `syllabus.html`, `slos.html` and `slo_mindmap.html` (title and description).
- `unit_4_overview.html` and `unit_4_cheatsheet.html` (the Week 12 precedent put the banner on both Unit 3 pages): a short banner saying Week 13 is new and Weeks 14–16 still describe the earlier version, linking the starters and rubric pages.

## 8. Build and checks

- Builders in `reference/ism3232/builders/`: five Week 13 pages, `capstone_starters.html`, `capstone_rubric.html`, using `pagekit`; `schema.sql` read from `04bc8c9`; Bayside's model proposal from `172d6ad`.
- Real `sqlite3` output comes from the `sqlite3` package Ubuntu 24.04 installs, 3.45.1-1ubuntu2.8, which is what `sudo apt install sqlite3` gives WSL students.
  - It is fetched with `apt-get download` into its own scratch folder and checked against the SHA-256 in apt's signed index.
  - Every session starts from a fresh copy of `schema.sql`. Transcripts and a `capture.sh` live under `reference/ism3232/runs/week13/`.
  - Why not sqlite.org's current build (3.54.1): a probe on 2026-10-17 ran the same session through both, and 3.54.1 aligns `.mode column` output differently. It right-aligns numbers and spaces `.tables` output more widely, so it would not match student screens.
  - The pages say that a Mac's version line, and possibly its column spacing, will differ; the rows are what matter.
- `verify_week13.py`: each page on disk equals its builder's output; every listing appears verbatim in its source; quiz items parse as `_build_qti.py` reads them; exercise answers appear only inside the lab's answer keys; every SQL answer key re-run in `sqlite3` prints what the page shows.
- Screenshots in light and dark themes and a console-error check for every new or changed page.
- Ship on the user's word: commit the `ism3232` pages, bump the parent pointer together with `_build_qti.py`, confirm the live pages.

## 9. Not in this phase

The Week 14–16 pages (Phase 4), the remaining site sweep (Phase 5), and any change to the Bayside app.
