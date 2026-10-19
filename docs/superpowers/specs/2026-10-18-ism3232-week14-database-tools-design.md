# ISM3232 Phase 4a: Week 14, Database Tools

- **Date:** 2026-10-18
- **Status:** Design approved section by section in chat; this written spec awaits review
- **Parent spec:** `docs/superpowers/specs/2026-10-16-ism3232-agents-throughline-design.md` (Week 14 section; section 8 items for Week 14)
- **Roadmap:** `docs/superpowers/plans/2026-10-16-ism3232-agents-throughline.md`, Task 15
- **Builds on:** the Bayside reference app, `reference/ism3232/bayside_app/`, Week 14 checkpoint `d44a23b`; Week 13 as shipped (ism3232 `c046b57`, parent `41376d5`)

## 1. Purpose

Week 14 turns the database students designed in Week 13 into the agent's tools. The pages teach Bayside's `database.py` and `tools.py` as "what changed since Week 12": the dictionaries became queries, the change queue became a table, the toolbox became a tools class with the same two methods, and the agent was copied over unchanged. The lab gives a short guided warm-up on Bayside, then students build the same layer for their own business in `module07_final_project`.

Success means:

- Every listing on a Week 14 page appears exactly in a file at `d44a23b`, a saved run, or output the builders generate by running that code.
- Every model output comes from a run of the checkpoint code itself with `granite4.1:3b` on the CPU.
- The lab's warm-up, rebuilt from the lab page alone, reproduces every expected box.
- A student who follows Parts 3–8 ends with their own `database.py`, `tools.py`, adapted agent and models, at least 12 passing tests that need no Ollama or Streamlit, and a terminal chat against their own database. An unpublished build of one starter proves this.
- Week 14 is live by Monday 2026-11-23; Lab 14 is due Sunday 2026-11-29.

## 2. Decisions

| Question | Choice (user, 2026-10-18) |
|---|---|
| Lab shape | A short guided warm-up on Bayside (about 30 minutes, with expected outputs: the connection helpers, `find_order`, one `tmp_path` test, one tool through `run`), then the student's own business |
| How much of `database.py` students write | Copy Bayside's three helpers (`query_all`, `query_one`, `change`) as they are; students write their business functions on top |
| Minimum tests | At least 12 across `tests/test_database.py`, `tests/test_tools.py` and `tests/test_agent.py` (at least 5, 5 and 2); the capstone rubric needs 15 by Week 16 |
| Keyword stand-in model | Students adapt `keyword_model.py` to their own tool names in Week 14, so the terminal program runs without Ollama and Week 15's model switch needs no extra step |

Accepted with the sections:

- The pages are organised as "what changed since Week 12", building up `database.py` from the connection pattern.
- The two terminal runs are recaptured from the checkpoint code, because the saved ones predate the final-review fixes.
- An unpublished Spokewell build verifies the lab, kept out of git because the parent repository is public.

## 3. What Week 14 teaches

**Title:** Database Tools — sqlite3, Placeholders & Tested Tools. The week-strip label changes from `W14 Python+SQL` to `W14 DB Tools`. Eyebrow: Unit 4 · Capstone Build.

**From Bayside, all quoted from `d44a23b`:**

- **The connection pattern and three helpers.**
  - `query_all` connects, sets `row_factory = sqlite3.Row`, executes with values, fetches all, closes, and returns `[dict(row) ...]`.
  - `query_one` returns the first row or `None`.
  - `change` executes, commits, reads `lastrowid`, and closes.
- **The business functions:**
  - `create_tables` reads `schema.sql` with `with open(...)` and runs it with `executescript`;
  - lookups: `find_order` (exact IDs), `all_orders`, `product_names`, `find_product`;
  - change requests: `add_change_request`, `find_request`, `waiting_requests`;
  - staff decisions: `approve_request` (Week 13 Exercise 4's two `UPDATE`s, now with placeholders) and `reject_request`.
- **The functions for Week 15.** `reset_database` sits right after `create_tables`, and `restock` and `status_report` are at the bottom of the checkpoint's file. The pages label all three "for Week 15's Staff tab" and do not teach them. The warm-up's first block (the import, the helpers and `create_tables`) ends before `reset_database`.
- **Placeholders.** A captured run puts `A100' OR '1'='1` through two queries:
  - an f-string query returns all 6 orders;
  - `find_order` with `?` returns `None`.

  This matters more than in a form app, because the model writes the arguments and a customer can steer the model.
- **`tools.py`.** `BaysideTools(db_file)` keeps Week 12's `tool_list()` and `run(name, arguments, history)`.
  - The tool methods call the database functions.
  - `check_request` lets customers ask what staff decided.
  - `customer_said` now matches whole words through `words()`, because Week 12's substring check let `A100` count when the customer typed `A1000`. This fix came from an automated security review of this app.
- **The agent and models.**
  - `agent.py` is Week 12's `chatbot.py`, with only its first line changed.
  - `ollama_model.py` adds `MAX_MESSAGES = 20` and sends `history[-MAX_MESSAGES:]`.
  - `settings.py` holds `DB_FILE`, `MODEL_NAME` and `INSTRUCTIONS`.
  - `main.py` is the terminal chat plus the staff review, now writing to the database.
- **Tests.** `make_db(tmp_path)` gives each test its own database. Bayside's database, tool and agent tests serve as models.

**New Python, each explained in one line where it first appears:**

- `import sqlite3`, `connect`, `execute`, `fetchall`, `commit`, `close`, `lastrowid`;
- tuples, including the one-item `(order_id,)` with its trailing comma;
- `row_factory` and `dict(row)`;
- reading a file with `with open(...)` (Week 6's lab only wrote one);
- `executescript`;
- `.split()` and `" ".join(...)` in `words()`;
- `tmp_path / "test.db"`.

**Left out, and why:**

- JOINs: each capstone question is answered from one table.
- The `with sqlite3.connect(...)` shortcut: it saves changes but does not close the connection.
- ORMs and migrations: beyond a one-file SQLite app.
- Two people using the app at once: Week 15.

**A student's `module07_final_project` after Lab 14:**

- From Week 13: `PROPOSAL.md`, `schema.sql`, `requirements.txt`, `.gitignore`.
- Written this week:
  - `database.py`: the three helpers and `create_tables` copied, plus their own functions;
  - `tools.py`: their tools class, with `clean`, `words` and `customer_said` copied from Bayside;
  - `settings.py`;
  - `main.py`.
- Copied from their Week 12 folder: `agent.py` (from `chatbot.py`, with their `HANDOFF_WORDS`), `fake_model.py`, `fallback_model.py`, and `ollama_model.py` with `MAX_MESSAGES` added.
- Copied and adapted: `keyword_model.py`.
- At least 12 tests in the three test files, passing with `ollama` and `streamlit` blocked.

## 4. The Week 14 pages

### Reading (about 60 minutes)

1. Objective, then **Coming from Week 13**: "The database exists, but the agent cannot reach it."
2. **At a glance**, then eight outcomes:
   1. connect to SQLite from Python;
   2. pass values safely with `?`;
   3. get rows back as dicts;
   4. write database functions;
   5. test them with `tmp_path`;
   6. build tools on database functions;
   7. explain why the door matches whole words;
   8. plug in the unchanged agent.
3. **From a list to a table.** A table maps each Week 12 piece to its Week 14 replacement:

   | Week 12 | Week 14 |
   |---|---|
   | `OrderLookup` and `StockLookup` dictionaries | `database.py` queries |
   | `ChangeQueue.requests` | `change_requests` |
   | `Toolbox` | `BaysideTools` |
   | `chatbot.py` | `agent.py`, unchanged |
4. **Python talks to SQLite.**
   - `query_all`, explained line by line;
   - a real Python shell session showing rows as dicts;
   - `query_one`, then `change` with `commit` and `lastrowid`.
5. **The business functions.**
   - `find_order`, `product_names` and `find_product`;
   - the three change-request functions;
   - `approve_request`, tied back to Week 13's Exercise 4;
   - `create_tables`, where Week 13's `IF NOT EXISTS` and `INSERT OR IGNORE` pay off.
6. **Placeholders**: the captured f-string versus `?` run.
7. **Testing with `tmp_path`**:
   - `make_db`;
   - three Bayside tests: reading the schema twice adds no duplicates, exact IDs, SQL in an order ID;
   - run `pytest` from the project folder, because `create_tables` opens `schema.sql` there.
8. **`tools.py`**: the class, two tool methods, the `run` door, `words` and `customer_said`, and the A100/A1000 story.
9. **The agent doesn't notice**:
   - `agent.py`'s one-line difference;
   - `MAX_MESSAGES`;
   - `settings.py` and `main.py`;
   - the two recaptured runs, in which a request decided in the first run is still in the database in the second.
10. **What this module leaves out, and why** (section 3).
11. **Key terms**, **Before you leave**, and a 10-item quiz in the existing `.quiz-item` markup.
12. **Closing**: "Staff still can't approve anything without running Python."

### Lecture (75 minutes)

| Minutes | Segment | What happens |
|---|---|---|
| 0–8 | Where Week 13 left off | The Week 12→14 map |
| 8–25 | The connection pattern, live | `query_all` in a Python shell; dict rows |
| 25–35 | Placeholders, live | The injection demo; "the model writes the arguments" |
| 35–50 | Same door, whole words | `run`, `customer_said`, the A1000 test; run the tests |
| 50–65 | The agent doesn't notice | `main.py` with Ollama, run twice; the data lasts |
| 65–75 | Your project | What to copy, what to write, 12 tests; next week |

Then three discussion questions, and four misconceptions to listen for:

- "the database saves on its own" (it needs `commit`);
- "an f-string is fine if the value looks safe";
- "`(order_id)` is a tuple";
- "`tmp_path` tests touch my real database".

There is no video block until a new video exists.

### Slides

The slides follow the lecture's segments, as in Week 12. Code slides with output are standalone snippets run against the checkpoint folder; the verifier re-runs each one. Model output appears only as the saved runs.

### Lab

**Where students start:** `module07_final_project` with the proposal approved and a `schema.sql` that reads twice cleanly, plus their Week 12 `module06_agents` passing its tests. A box covers laptops that cannot run the model: Parts 2 to 6 and every test need no Ollama, and Part 7 can run on the keyword model.

1. **Start**: activate the capstone venv.
2. **Bayside warm-up** (about 30 minutes) in `~/ism3232/sql_practice`, outside the capstone repository, with the capstone venv active.
   - `database.py` gets two verbatim blocks: the import, three helpers and `create_tables`, then `find_order`. `tools.py` is Bayside's whole file.
   - Python shell checks, with expected output from real runs:
     - `create_tables("warmup.db")`;
     - `find_order("warmup.db", "A100")` returns a dict;
     - `find_order("warmup.db", "A100' OR '1'='1")` returns `None`;
     - `BaysideTools("warmup.db").run("look_up_order", {"order_id": "A100"}, history)` answers when the history has the customer typing A100, and refuses when it does not.
   - `tests/__init__.py` and `tests/test_database.py` hold `make_db` and the find-order test. Expected: `1 passed`.
3. **Your `database.py`**: copy the helpers and `create_tables`, then write your functions from your `schema.sql`:
   - a lookup for each business table;
   - add, find and waiting for change requests;
   - approve and reject.

   A table maps each Bayside function to its counterpart; for example `find_order` becomes `find_repair` for Spokewell. `approve_request` follows Week 13's Exercise 4.
4. **`tests/test_database.py`**: at least 5 `tmp_path` tests, modelled on Bayside's:
   - creating the tables twice adds no duplicates;
   - lookups need exact IDs;
   - SQL text in an ID is just text;
   - a filed change waits;
   - approve changes the record once, and reject leaves it alone.
5. **`tools.py` and `tests/test_tools.py`**: a class named for your business, taking `db_file`, with:
   - `tool_list`;
   - your lookup and change tool methods, each with an `Args:` docstring;
   - the `run` door, with `clean`, `words` and `customer_said` copied from Bayside.

   At least 5 tests, including a refused made-up value.
6. **Agent and models**:
   - copy `chatbot.py` as `agent.py` and set `HANDOFF_WORDS` from the proposal;
   - copy `fake_model.py`, `fallback_model.py`, and `ollama_model.py` with `MAX_MESSAGES` added;
   - adapt `keyword_model.py` to your tool names and keywords;
   - write `settings.py` from the proposal's instructions draft;
   - `tests/test_agent.py` adapts at least 2 of Bayside's agent tests, using `FakeModel`.
7. **`main.py`**: the terminal chat and the staff review, adapted. Run it with the real model, or with the keyword model by changing one line. Run it twice and see that the data lasts.
8. **Ritual and push**: quit Ollama, run `ruff format . && ruff check . && pytest -v`, then `git add . && git commit -m 'lab 14: database tools' && git push`.

**Submission box:** the files above with at least 12 tests passing, and the repository URL in Canvas, for completion credit. There are no separate exercises or mini-project: the capstone is the exercise.

### Lab slides

The lab slides use the Week 12 lab deck's structure: the warm-up's shell blocks and real outputs, then the steps for each part, the checks, and instructor notes.

## 5. Real runs, checks, wiring and shipping

**Real output, all from `d44a23b`:**

- The Python shell sessions and the placeholder snippet are generated by running them in a copy of the checkpoint folder. The builders return them as derived text.
- The warm-up's `pytest` summary comes from a real run in a folder built from the lab page.
- The two `main.py` runs are recaptured.
  - They use the course model on the CPU (`CUDA_VISIBLE_DEVICES=-1 ollama serve`) and the same typed inputs as Phase 2.
  - They are saved under `reference/ism3232/runs/bayside_app/`, with `capture.sh` updated to run the checkpoint commit.
  - They are read before any page quotes them, and the pages quote whatever wording the model produced.

**Builders and verifier.** `reference/ism3232/builders/` gets `week14_common.py`, `week14_reading.py`, `week14_lecture.py`, `week14_slides.py`, `week14_lab.py`, `week14_lab_slides.py` and `verify_week14.py`. They reuse `pagekit` and the Week 12 lab-slide helpers. `verify_week14.py` proves:

- each page on disk equals its builder's output;
- every listing appears exactly in `d44a23b`'s files, a saved run, or derived output;
- every slide snippet prints what its slide shows;
- every lab expected box equals a real output;
- the quiz imports cleanly with `_build_qti.py`;
- the warm-up, rebuilt from the lab page into an empty folder and run, reproduces every expected box.

**The unpublished Spokewell build.**

- It lives in `reference/ism3232/_private/spokewell/`, a folder added to the parent `.gitignore` so it never reaches the public repository.
- It is built by following Parts 3–8 as written, using Spokewell's starter data.
- It must pass `tools/check.py`: ruff, and at least 12 tests with `ollama` and `streamlit` blocked.
- Its `main.py`, running on the adapted keyword model, must answer a lookup, file a change, and apply the change when staff approve it.
- `verify_week14.py` runs these checks when the folder exists.

**Wiring:**

- **Week strip:** `W14 Python+SQL` becomes `W14 DB Tools`.
  - Change it in `pagekit.STRIP` and rebuild the Week 12 and 13 pages with their builders; both verifiers must pass, and the diff must show only the strip.
  - Use counted replacements on the other pages that carry the strip.
- **The title** goes in:
  - both `site.js` menus;
  - the home page's Module 14 card (title and a new description);
  - the Week 15 pages' previous links;
  - `_build_qti.py` (`14:`);
  - the Week 14 rows in `course_guide.html`, `syllabus.html`, `slos.html` and `slo_mindmap.html`;
  - Week 13's next links, by setting `week13_common.NEXT` and rebuilding.
- **Unit 4 banners:** the banners on `unit_4_overview.html` and `unit_4_cheatsheet.html` say Weeks 13 and 14 are new.

**Before showing the user:**

- all tests and both the Week 13 and Week 14 verifiers pass;
- screenshots at light, dark and phone widths, plus a console-error check on every changed page;
- the quiz builds with 10 questions;
- a fresh whole-branch review on the strongest model, then one test-first fix pass.

**Shipping, on the user's word:**

1. Commit only this work's `ism3232` files and push.
2. Bump the parent pointer with `_build_qti.py`, staging only Week 14's line if another session has edits in that file, then push.
3. Confirm the live pages.

## 6. Not in this phase

- Weeks 15 and 16.
- The Phase 5 sweep, including the course guide's stale capstone percentage.
- The Phase 3 deferred minors.
- Any change to the Bayside app.
