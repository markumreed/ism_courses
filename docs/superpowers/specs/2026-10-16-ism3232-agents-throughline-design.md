# ISM3232 Weeks 12–16 and Capstone: One Agent Through-Line

- **Date:** 2026-10-16
- **Status:** Approved by the user 2026-10-16; amended the same day by the implementation plan (`docs/superpowers/plans/2026-10-16-ism3232-agents-throughline.md`)
- **Scope:** ISM3232 Weeks 12–16, the capstone rubric, and every page or file still keyed to the old Weeks 10–16
- **Builds on:** the agents redesign approved 2026-10-12 (Week 10 shipped as ism3232 `005902d`, Week 11 as `afeb8e4`)

## 1. Why this is needed

A review of Weeks 10–16 on 2026-10-16 found two courses joined at Week 12.

Weeks 10 and 11 are the new agent course. They share one running example (Bayside Outfitters, chatbot Sunny), one lab folder (`module06_agents`), and one teaching move (a part is handed to the chatbot through composition: first a tool, then a model). Every Week 11 page promises that Week 12 brings model-chosen tools, checks around every tool call, an approval step for anything that changes data, and tests with a fake model.

Weeks 12–16 and the capstone rubric are still the old purchase-request course:

| Where | What a student meets |
|---|---|
| Week 12, all five pages | "OOP III": entity and manager classes, `design.md`, `cd ~/ism3232/module06_oop`. Week 10 had students rename that folder to `module06_agents`, so the first lab command fails. None of Week 11's promises are kept. |
| Week 13 reading | "In Unit 3 you built RequestManager…", which these students never built. The proposal asks for entity/manager classes and "what is sent to the API". |
| Weeks 13–15 | A purchase-request tracker (Taylor, Jordan, Morgan) with a form-and-table Streamlit app. No agent. |
| Week 16 and the rubric | GenAI through the Anthropic API with `ANTHROPIC_API_KEY`, which contradicts Week 11 ("this course uses a local model", no API key). 25 rubric points for `models.py` entity/manager classes; a check that `design.md` was committed before `models.py`. |
| Unit 3/4 overviews, syllabus, home-page cards 12–16 | OOP I–III, inheritance, a Week 17, a FastAPI lecture, a screenshots folder, the Anthropic API as a required tool. |

The old pages also contain smaller errors that disappear with the rebuild: the Week 13 quiz lists ten proposal fields that differ from the template's ten; Week 14's worked example calls `add_record` with an extra argument and uses a return value the function does not give; the Week 16 quiz names a different "Control 2" from the reading.

## 2. Intent

**What the user asked for (2026-10-16):** review Week 10 through the capstone, make sure the material flows smoothly, and give it a comprehensive theme so students finish with a proper business application in Python.

**Success means:**

- Every "next week" promise on a page is kept by the following week.
- Each lab starts from the files the previous lab produced.
- The capstone rubric grades exactly what Weeks 10–16 taught, and nothing they did not.
- A student finishes with a working business application: a chat assistant for customers or staff, backed by a SQLite database, with a staff dashboard where people approve the changes the agent proposes.

**Decided earlier (2026-10-12 and 2026-10-13), still in force:**

- Agents all the way, on Ollama, course model `granite4.1:3b`, name kept in one constant. No API keys, no hosted AI service.
- Every lab works with a mock model first, so a weak laptop never blocks a student.
- Unit 4 keeps SQL and Streamlit.
- Bayside Outfitters and Sunny are the running example; students choose their own business for the capstone.
- Old pages are replaced in place.
- Due dates (Sundays): W12 Nov 15, W13 Nov 22, W14 Nov 29, W15 Dec 6, W16 Dec 13.
- The Week 11 rule order: coded rules first, the model for the rest. The payment/card handoff stays an `if` statement.

**Decided 2026-10-16 (the user's choices in this design session):**

| Question | Choice |
|---|---|
| What is the finished capstone? | Chat tab plus staff dashboard |
| How do students choose a business? | A menu of six starter businesses, or their own idea if it meets the same checklist |
| Does the real model have to work? | Grading by cloning stays model-free; the live demo must run on the real model (a student without a capable laptop demos on a classmate's laptop or a lab machine and says so in the README) |
| How do Bayside and the capstone share Weeks 12–16? | Two tracks: readings and lectures build Bayside one layer a week; Labs 13–16 apply each layer to the student's own business |

## 3. The finished application

**Theme: one agent, one new layer each week.** The `SupportChatbot` students write in Week 10 is never thrown away. It gains tools (W12), lasting data (W13–14), a web interface (W15), and measurement (W16), and ends as a small business application used by customers and staff.

**Final capstone repo**, `~/ism3232/module07_final_project`. Bayside is the reference version shown on the pages; a student's version has the same files for their own business.

```
PROPOSAL.md  schema.sql  README.md  requirements.txt  .gitignore
database.py      W14  plain functions; ? placeholders; db_file= parameter for tests
tools.py         W14  what the model may ask for; checks arguments; returns text
agent.py         W12  the chatbot class: rules first, model, tool loop, history
keyword_model.py W12  keyword-rule stand-in; runs the app without Ollama
fake_model.py    W12  scripted model (it can ask for a tool), used by tests
fallback_model.py W12 real model first, keyword model when it is down
ollama_model.py  W11  the real model, now also sent the tool list
app.py           W15  Streamlit: Chat tab and Staff tab
evaluation.py    W16  fixed conversations run against the real model
tests/           test_database.py  test_tools.py  test_agent.py
```

**How a message flows:**

```
customer -> Chat tab -> agent.respond()
              |- payment/card? -> handoff (an if statement; never reaches the model)
              '- model + tool list
                   |- text -----------------------------------------> reply
                   '- asks for a tool -> agent checks name and arguments
                                      -> tools.py -> database.py -> SQLite
                                      <- result text goes back to the model
lookups read data; changes only file a request (status 'waiting')
staff -> Staff tab -> Approve / Reject -> database applies the change
```

**Five ideas every week reinforces.** Each already appears in Weeks 10–11.

1. **Facts come from data, not the model.** Lookups answer from SQLite.
2. **The model proposes; people approve.** A change tool can only add a row to the approval queue.
3. **Some things never reach the model.** Payment/card is a coded handoff, and card numbers are never stored.
4. **Everything is testable without a model.** Fake models in pytest, so a cloned repo grades the same on any laptop.
5. **Measure; don't assume.** Week 16 runs the real model on fixed conversations and reports how often it was right.

**One deliberate change to Weeks 10–11.** An address change stops being a dead-end handoff ("I'm passing you to a human agent"). From Week 12 the agent collects the new address and files a change request that staff approve. A person still decides, so the Week 11 principle holds (the model is never the only thing between a customer and an action); the mechanism changes, and Week 12 says so explicitly.

## 4. Week by week

Each week ends by naming the problem the next week solves.

### Week 12 · Tools and Guardrails

Due Nov 15. Lab on Bayside in `module06_agents`, closing Unit 3.

- **Starts from:** Week 11's open problems. Keyword rules miss "Has my package A101 shipped?" and catch "Do you sell gift cards?" (because of "card"). The model once claimed A101 had shipped when it had not. Every reply in the history has role `assistant`, whoever produced it.
- **Teaches:** what a tool call is (the model asks; your code decides whether to run it); tool descriptions written as docstrings; the tool loop (ask, check, run, send the result back, ask again), capped at three rounds; argument checks (an unknown tool, a blank argument, or an unknown order ID gets an explanation, never a crash); a `tool` role in the history.
- **Bayside code added:** a new model method, `decide(instructions, history, tools)`, returns a dict, `{"text": ...}` or `{"tool": ..., "arguments": {...}}`, or `None` when the model is down. The Week 11 `reply()` stays unchanged, because the Week 11 mini-project in the same folder still calls it. `FakeModel` plays back scripted decisions for tests; `KeywordModel` carries the old keyword rules so the chatbot runs without Ollama; `FallbackModel` asks the real model first and the keyword model when it has no answer. A `Toolbox` with `tool_list()` and `run(name, arguments, history)` is the one place tool requests are checked. A `ChangeQueue` class (a list of dicts with `status: "waiting"`): `request_address_change` can only add to it, and `approve()` is the one place `orders` changes. The order and stock keyword rules are removed; the payment/card handoff stays.
- **Shown with real runs:** the Week 11 failures run again, showing what was fixed and what was not.
- **Leads into Week 13:** approved changes live in a Python list, so a restart loses them. A business needs data that lasts.

### Week 13 · Agent Design & SQL

Due Nov 22. First capstone milestone, in `module07_final_project`.

- **Teaches:** choosing a business from the menu (or proposing one) and checking it against the checklist (section 5). `PROPOSAL.md` for an agent: users, tables, lookup tools, change tools, coded handoff, data never stored, instructions draft, out of scope, and five sample conversations, which return in Week 16 as evaluation cases.
- **SQL in the `sqlite3` shell**, demonstrated on `bayside.db` (`orders`, `products`, `change_requests`): CREATE TABLE, INSERT, SELECT with WHERE, UPDATE with WHERE, ORDER BY, GROUP BY with COUNT. Kept from the old Week 13: column types, dot commands, the UPDATE-without-WHERE warning.
- **Lab:** venv and `.gitignore` (including `*.db`), `PROPOSAL.md`, `schema.sql` with sample rows, run in the shell, instructor sign-off.
- **Leads into Week 14:** the database exists, but the agent cannot reach it.

### Week 14 · Database Tools

Due Nov 29.

- **Teaches:** `database.py` with `with sqlite3.connect(...)`, `?` placeholders, rows as dicts, a `db_file=` parameter, and `tmp_path` tests. `tools.py` wraps those functions with argument checks and returns text. Tool names match Week 12's, and the tools class has the same two methods as Week 12's `Toolbox`, `tool_list()` and `run(name, arguments, history)`, so `agent.py` is copied over and works unchanged: the list became a table and the agent did not notice.
- **Safety link:** placeholders matter more here than in a form app, because the model writes the arguments and a customer can steer the model.
- **Lab:** the student's `database.py`, `tools.py`, adapted `agent.py`, tests, and a terminal chat loop against their database.
- **Leads into Week 15:** staff cannot approve anything without running Python.

### Week 15 · Streamlit Chat & Staff Dashboard

Due Dec 6.

- **Teaches:** Streamlit reruns the whole script on every click. This mirrors Week 11: the model has no memory, Streamlit has none either, and `st.session_state` keeps the agent and its history between clicks. `st.chat_input` and `st.chat_message`. The Staff tab: waiting requests with Approve/Reject buttons, the records table, a GROUP BY report. A sidebar switch between the fake and the real model, and a "model is down" message.
- **Dropped:** the FastAPI lecture.
- **Lab:** the student's `app.py` with both tabs.
- **Leads into Week 16:** the app runs; how often is it right?

### Week 16 · Evaluation, Safety & Demo

Due Dec 13.

- **Teaches:** `evaluation.py` runs the five proposal conversations and more, three times each, on the real model, and counts whether it chose the right tool, handed off, or declined. It is kept outside pytest because results vary and it needs Ollama. A safety checklist students try against their own agent: the false-closing-time trick from Week 11, asking to change someone else's order, SQL in an order ID, payment questions. The final README: run steps, tools and approvals, safety decisions, evaluation results, specific limitations, an AI-use statement.
- **Demo, about five minutes:** the business problem; the live workflow check (venv active, ruff, pytest, git log); a real-model chat including one full approval round trip through the Staff tab; one evaluation failure and how it was handled; one file explained line by line.

## 5. Capstone: checklist, starter menu, rubric

### Checklist

Every capstone meets this, from the menu or not. The instructor checks it at proposal sign-off, and the rubric grades against it.

1. One business. The chat serves customers or staff; the Staff tab always serves staff.
2. At least two business tables plus a `change_requests` table.
3. At least two lookup tools. They only read, and they check their arguments.
4. At least one change tool. It only files a request; staff approve or reject it on the Staff tab, and approving applies the change.
5. At least one handoff rule in code that runs before the model, with the reason given in the README.
6. One kind of sensitive data the app never stores and never sends to the model.
7. Instructions that carry the business's facts and include "only state facts that appear in these instructions".
8. Five sample conversations, which become the Week 16 evaluation cases.

### Starter menu

Six businesses chosen to stay clear of Bayside, the midterm businesses, the study-guide examples, and the Week 10 appointment helper. Fictional names and sample data are set when Week 13 is built.

| Business | Tables | Lookups | Change needing approval | Coded handoff | Never stored |
|---|---|---|---|---|---|
| Bike repair shop | repairs, parts | repair status; part in stock | move the pickup date | payment/card | card numbers |
| Dog grooming salon | appointments, services | appointment; service price and length | reschedule | pet health questions | pet medical history |
| Campus bookstore | orders, textbooks | order status; textbooks for a course | cancel an order | financial aid, payment | student ID numbers |
| Fitness studio | classes, bookings | classes on a day; booking status | move a booking | injury or medical advice | health information |
| IT help desk (staff-facing) | tickets, devices | ticket status; who has a device | raise ticket priority | password resets | passwords |
| Apartment maintenance | requests, units | request status; a unit's open requests | schedule an entry time | emergencies (gas, fire, flood) | door and lock codes |

### Rubric

100 points, 30% of the final grade. Each part maps to the week that taught it. Point tiers within each part are written when the rubric page is built.

| Part | Points | Full marks means |
|---|---|---|
| Proposal (W13) | 10 | Checklist met; five conversations; signed off before Week 14 code |
| Database layer (W14) | 15 | Correct column types; `?` in every query; rows as dicts; `db_file=`; `tmp_path` tests |
| Tools & guardrails (W12, W14) | 20 | Lookups check arguments; change tools only file requests; unknown tools refused; loop capped; handoff runs before the model |
| Agent & models (W10–12) | 10 | Model and tools passed in; history with roles; safe reply when the model is down; fake and real models interchangeable |
| Streamlit app (W15) | 15 | Chat history kept in `session_state`; Approve applies the change and Reject does not; records table and report; model switch |
| Evaluation & safety (W16) | 10 | At least 8 cases including the five; results and safety-checklist findings in the README; specific limitations |
| Tests & workflow | 10 | ruff clean; at least 15 tests across three files that pass without Ollama or Streamlit installed; a real commit history; README run steps |
| Live demo (W16) | 10 | Real model; one approval round trip; one file explained line by line; AI-use statement |

The "without Ollama or Streamlit installed" rule follows from the autograder, which runs `python -m pytest -q` with its own interpreter, no installs, no network, and a 30-second timeout. Tests may import `agent.py`, `tools.py`, `database.py`, `fake_model.py`, `keyword_model.py`, and `fallback_model.py`, never `app.py` or `ollama_model.py`.

Removed from the old rubric: `models.py` entity/manager classes, the `design.md`-before-code timestamp check, the Anthropic API and its key, and `unittest.mock.patch` (students write their own fake model instead).

## 6. Everything else that still describes the old course

Found by searching every ISM3232 page and the parent repo for the old names, not counting the Week 12–16 pages themselves.

| Area | Files | Change |
|---|---|---|
| Navigation | `index.html` cards 12–16; `site.js` (two menus); the week strip on 31 pages | New titles and descriptions, updated as each week ships (as done for Week 11) |
| Unit pages | `unit_3_overview`, `unit_3_cheatsheet`, `unit_4_overview`, `unit_4_cheatsheet`, `unit_all_overview` | Rewrite the bodies; remove Week 17, FastAPI, `models.py`, `ai_feature.py`; replace the "being rebuilt" banners |
| Course pages | `syllabus`, `slos`, `slo_mindmap`, `course_map`, `course_guide` | Schedule rows, SLO wording, tools list (Anthropic API out, Ollama in, Streamlit stays) |
| Help pages | `glossary`, `troubleshooting` | Glossary: drop RequestManager and BusinessRequest; add tool call, tool loop, guardrail, approval queue, session state, evaluation. Troubleshooting: Anthropic and `ai_feature` cards become Ollama, tool, and Streamlit cards |
| Stray mentions | `week07_reading` (`models.py`); FastAPI in `unit_1_overview`, `unit_2_overview`, `week08_reading`, `week09_lecture`, `week09_slides` | One-line fixes |
| Week 1 folder name | `module06_oop` on `week01_lab`, `week01_lab_slides`, `week01_lecture`, `week01_slides`, `week02_lab_slides`, `week04_lecture`, `week04_slides`, `unit_1_overview`, `unit_all_overview` | Change to `module06_agents` for next term. This term's students already created `module06_oop`, so Week 10's `mv` step stays |
| Parent repo | `_build_qti.py` titles 12–16; `autograder/assignments/ism3232/capstone.yaml` (five old parts become the eight above); `autograder/tests/ism3232_due_dates.xlsx` titles; `canvas_builder/ism3232_manifest.yaml`, front page, syllabus; `syllabi/ism3232_simple_syllabus.md` | Rerun `python3 _build_qti.py`; the user re-imports the Week 12–16 quiz zips |
| Videos | `video_scripts/ism3232/27`–`33`; `labs/lab_w12`–`lab_w16` | Rewrite scripts to match the new pages; recording stays with the user |

## 7. Build order and checks

| Step | What | Live by |
|---|---|---|
| 1 | Week 12: its own design pass with the user, then build, then show | Mon Nov 9 |
| 2 | The Bayside reference app (database, tools, agent, Streamlit app, evaluation), written and run once | Before step 3 |
| 3 | Week 13, the capstone rubric page, and the starter menu | Mon Nov 16 |
| 4 | Weeks 14, 15, 16, one at a time, each shown before the next | Nov 23, Nov 30, Dec 7 |
| 5 | The sweep in section 6 | With Week 16 |

All four Unit 4 weeks take their listings from the step 2 app, so Week 15's `app.py` cannot drift from the `database.py` Week 14 taught.

**Checks for every week** (the ones that held for Weeks 10–11):

- Write and run the real code first; generate page listings from the verified files.
- Rebuild the lab folder from the finished page and run `ruff format . && ruff check . && pytest` with current ruff defaults (0.16+ enables I001 and SIM rules).
- Run pytest with `sys.modules['ollama'] = None` and Streamlit absent, matching the autograder.
- Every model reply on a page is a captured real run of `granite4.1:3b` on the CPU only (`CUDA_VISIBLE_DEVICES=-1 ollama serve`, Ollama's default 4k context); every "5 out of 5" comes from five actual runs. Do not pin the server to a few cores with taskset: llama-server still starts one thread per physical core and each reply then takes minutes.
- Streamlit: Streamlit's `AppTest` for automated checks, plus a browser check. Lab slides previewed over `python3 -m http.server`. Quiz items parsed by `_build_qti.py`.
- Reuse each existing page's `<head>`; keep the lecture `.code-block` classes and the `.expected` `white-space: pre-wrap` fix.
- Commit and push to `main` (the live site) only when the user says so; stage only this work's files.

## 8. Settled in each week's own design pass

These are deliberately left to the per-week design step, as for Weeks 10–11. Each is a detail inside a week, not a change to this through-line.

- **Week 12:** the exact reply dict and `FakeModel` interface; how tools are handed to Ollama (plain functions or bound methods; confirm how the `ollama` package builds tool descriptions from signatures and docstrings); how far the handoff rule's word matching goes on the gift-cards problem; which Python is new this week.
- **Week 13:** fictional names and sample data for the six starter businesses; the exact `PROPOSAL.md` template; how sign-off happens.
- **Week 14:** Bayside's `database.py` function names; how `tools.py` receives the database path so tests can use `tmp_path`.
- **Week 15:** the model-switch control; whether the chat tells a customer when staff act on their request.
- **Week 16:** number of evaluation cases and repeats; the evaluation report format; demo length and scheduling.
- **Rubric:** point tiers within each of the eight parts.

## 9. Not changing

- Weeks 1–11 content, apart from the stray mentions and folder-name fixes in section 6.
- The Week 9 midterm and its private materials.
- ISM2411.
- Left out of the course on purpose: hosted AI services and API keys, streaming replies, FastAPI, inheritance, cloud deployment.
