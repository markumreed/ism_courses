# ISM3232 Phase 2: The Bayside Reference App

- **Date:** 2026-10-16
- **Status:** Approved by the user 2026-10-16; amended the same day by the implementation plan (`docs/superpowers/plans/2026-10-16-ism3232-bayside-app.md`)
- **Parent spec:** `docs/superpowers/specs/2026-10-16-ism3232-agents-throughline-design.md` (sections 3–5)
- **Parent plan:** `docs/superpowers/plans/2026-10-16-ism3232-agents-throughline.md`, Phase 2 (Tasks 10–11)
- **Builds on:** the Week 12 reference code in `reference/ism3232/module06_agents` (guided checkpoint `5bead57`, full state `e87f10f`), shipped as ism3232 `98e095e`

## 1. Purpose

Build one tested Bayside Outfitters application that Weeks 13–16 take every code listing from. The pages show it one layer per week (two tracks, as approved): Week 13 the data, Week 14 the database tools, Week 15 the Streamlit app, Week 16 evaluation. In each week's lab, students build the same layer for their own business in `~/ism3232/module07_final_project`.

Success means:

- Every listing on the Week 13–16 pages comes from a file in this app that ran.
- `agent.py` is Week 12's `chatbot.py`, unchanged, and works on the database through the tools interface.
- Every student-facing test passes with `ollama` and `streamlit` blocked (`reference/ism3232/tools/check.py`).
- The app runs with the real model, with the keyword stand-in, and with Ollama switched off.
- The capstone rubric's parts (database layer, tools and guardrails, agent and models, Streamlit app, evaluation and safety) each have a worked Bayside example.

## 2. Decisions

From the parent spec, still in force: `granite4.1:3b` through Ollama only; the tables `orders`, `products`, `change_requests`; a Chat tab and a Staff tab; tools with `tool_list()` and `run(name, arguments, history)`; tests that never import `app.py` or `ollama_model.py`; the real model required only in the live demo.

Made by the user in this design pass (2026-10-16):

| Question | Choice |
|---|---|
| How does a customer learn what staff decided? | Ask the agent: a read-only tool `check_request(number)` |
| What else can staff do? | Approvals, the orders table and a status report, plus one edit form (restock a product) |
| How does Week 16 evaluate? | A list of case dictionaries in `evaluation.py`, three real runs each, a printed table |
| How do Week 12's objects become database code? | One tools class over plain functions: `database.py` functions, `BaysideTools(db_file)` in `tools.py`, `agent.py` unchanged |

Made by me and accepted with the sections:

- Database functions take the database file as their first argument; nothing has a hidden default database.
- `create_tables` runs `schema.sql` (read with `with open(...)` and `f.read()`).
- Order IDs match exactly everywhere, by looking up each word of the text (`.split()`, new in Week 14). This keeps Week 12's promise ("in Week 14 the database matches IDs exactly") and keeps `KeywordModel`'s whole-sentence lookups working.
- `OllamaModel.decide` sends only the last `MAX_MESSAGES = 20` history entries (slicing, new in Week 14) so long chats fit a laptop's 4k context; the customer-said check still reads the full history.
- `check_request` never repeats the new address, because request numbers are easy to guess.
- `evaluation.py` cases hold a list of messages, so multi-turn conversations can be measured.
- (Amended by the plan) `evaluation.py` has a fifth kind of check, `queued`, which counts waiting requests in `evaluation.db`, and it normalizes whitespace before text checks, because the model sometimes writes "11 pm" with a narrow no-break space, which hid a real failure in the first test run.

## 3. The data layer (Weeks 13–14)

### `schema.sql`

```sql
CREATE TABLE IF NOT EXISTS orders (
    order_id TEXT PRIMARY KEY,
    customer TEXT NOT NULL,
    item     TEXT NOT NULL,
    status   TEXT NOT NULL,
    address  TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS products (
    name  TEXT PRIMARY KEY,
    price REAL NOT NULL,
    stock INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS change_requests (
    number      INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id    TEXT NOT NULL,
    new_address TEXT NOT NULL,
    status      TEXT NOT NULL DEFAULT 'waiting'
);
```

followed by `INSERT OR IGNORE` sample rows: six orders and six products. Orders include Week 12's A100 (shipped, 14 Bay Road), A101 (processing, 3 Gull Lane) and A102 (delivered, 88 Pier Street), plus A103 to A105 with all three statuses represented; products include rain jacket (12 in stock), day pack (0) and trail hat (5), plus three more, each with a price. Order statuses are `processing`, `shipped`, `delivered`. Running the file twice changes nothing.

### `database.py`

Plain functions. Each takes `db_file` first, opens a connection, uses `?` placeholders for every value, commits when it writes, and closes. Rows come back as dictionaries (`sqlite3.Row`, then `dict(row)`).

| Function | Returns |
|---|---|
| `create_tables(db_file)` | nothing; runs `schema.sql` |
| `reset_database(db_file)` | nothing; drops the three tables and runs `schema.sql` (used only by `evaluation.py`, on `evaluation.db`) |
| `find_order(db_file, order_id)` | the order dict, or `None`; exact ID |
| `all_orders(db_file)` | list of order dicts, by order ID |
| `product_names(db_file)` | list of names |
| `find_product(db_file, name)` | the product dict, or `None` |
| `add_change_request(db_file, order_id, new_address)` | the new request's number |
| `find_request(db_file, number)` | the request dict, or `None` |
| `waiting_requests(db_file)` | list of waiting request dicts, oldest first |
| `approve_request(db_file, number)` | Week 12's messages: `Request N approved.`, `Request N is already approved.` (or rejected), `There is no request N.` |
| `reject_request(db_file, number)` | the same messages for a rejection |
| `restock(db_file, name, stock)` | nothing |
| `status_report(db_file)` | `[{"status": ..., "orders": n}, ...]` from `GROUP BY status` |

`approve_request` changes the order's address and the request's status on one connection and commits once; it acts only on a request whose status is `waiting`.

## 4. Tools, agent and models (Week 14)

### `tools.py`: `BaysideTools(db_file)`

| Method | Behaviour | Reply |
|---|---|---|
| `look_up_order(order_id)` | looks up each word of the text exactly, ignoring `?.!,` around it | `Order A100 is shipped.` or `No order with that ID was found. Order IDs look like A100.` |
| `check_stock(item)` | finds a product name inside the text (Week 12's matching; a lookup only) | `We have 12 of the rain jacket in stock, at $89.00.` or `That product was not found.` |
| `request_address_change(order_id, new_address)` | requires an exact, existing order ID, then `add_change_request` | `Request N was sent to staff. The address has not changed yet.` |
| `check_request(number)` | looks up one request; never repeats the address | `Request N for order A102 is waiting.` / `was approved.` / `was rejected.`, or `There is no request N.` |
| `tool_list()` | the four methods above, not called | — |
| `run(name, arguments, history)` | Week 12's door: refuses an unknown tool, an empty or missing value (`.get()`, `str()`, `.strip()`), and an order ID, address or request number the customer never typed; every refusal is a sentence telling the model what to do | — |
| `clean(arguments, key)`, `customer_said(history, text)` | as in Week 12 | — |

Each tool method has a docstring with an `Args:` section, as Week 12 taught.

### `agent.py`

Week 12's `chatbot.py`, copied unchanged apart from its file-name comment on line 1: `SupportChatbot(name, instructions, tools, model)`, `HANDOFF_WORDS = ["payment", "card"]`, `MAX_TOOL_ROUNDS = 3`, `tool` history entries.

### Models

`keyword_model.py`, `fake_model.py` and `fallback_model.py` are copied from Week 12 unchanged. `ollama_model.py` is Week 12's with one change: `decide` sends `history[-MAX_MESSAGES:]`, `MAX_MESSAGES = 20`. Measured on 2026-10-16: the 20 entries `decide` sends for a long Bayside chat with all four tools are 947 prompt tokens (1455 for the untrimmed 42 entries), well inside the 4096-token laptop default.

### `settings.py` and `main.py`

`settings.py` holds the three values every entry point shares: `DB_FILE = "bayside.db"`, `MODEL_NAME = "granite4.1:3b"`, and `INSTRUCTIONS` (Week 12's Bayside instructions: hours, returns, "only state facts that appear in these instructions or in tool results", say you do not know and offer a human). `agent.py` stays unchanged because it never needs them; `main.py`, `app.py` and `evaluation.py` import them.

`main.py` is Week 12's terminal program on the database: `create_tables`, the chat loop with `OllamaModel`, then a staff review loop over `waiting_requests` that calls `approve_request` or `reject_request`, then the orders from `all_orders`. It is Week 14's "terminal chat against the database".

### Tests (all with `tmp_path`, none importing `app.py` or `ollama_model.py`)

- `tests/test_database.py`: `create_tables` twice adds no duplicate rows; `find_order` is exact (`A1000` gives `None`); SQL text in an order ID (`A100'; DROP TABLE orders;--`) gives `None` and every row remains; `add_change_request` returns increasing numbers; `approve_request` applies once, refuses after a rejection, and refuses an unknown number; `reject_request` changes nothing in `orders`; `restock` and `status_report` give the expected values; `reset_database` restores the sample rows.
- `tests/test_tools.py`: each tool's replies; exact IDs for lookups and changes; `KeywordModel`-style whole sentences still find an order; the door refuses unknown tools, empty values and made-up order IDs, addresses and request numbers; `check_request` never contains the address.
- `tests/test_agent.py`: Week 12's chatbot tests, pointed at `BaysideTools` and a test database, including the made-up address, the blank address, the loop limit, the payment handoff, the model-down reply, and `FallbackModel`.

## 5. The Streamlit app (Week 15)

### `app.py`

1. `DB_FILE`, `MODEL_NAME` and `INSTRUCTIONS` from `settings.py`; `create_tables(DB_FILE)` on every run.
2. A sidebar radio: "Course model, keyword rules if it is down" (`FallbackModel(OllamaModel(MODEL_NAME), KeywordModel())`, the default) or "Keyword rules only (no AI)" (`KeywordModel()`).
3. The chatbot is created once per browser session in `st.session_state`; on every run `bot.model = make_model(choice)`, so switching keeps the conversation.
4. `st.tabs(["Chat", "Staff"])`.

**Chat tab:** draws the `user` and `assistant` history entries with `st.chat_message` (tool entries stay hidden); on `st.chat_input`, calls `bot.respond()` inside `st.spinner("Sunny is thinking...")`, then `st.rerun()`.

**Staff tab:**

- *Waiting for approval:* one row per waiting request (`st.columns`), with Approve and Reject buttons keyed by request number. A click calls `approve_request` or `reject_request`, keeps the returned message in `st.session_state`, and reruns; the message shows at the top of the tab on the next run. With nothing waiting, a sentence says so.
- *Orders:* `st.dataframe(all_orders(DB_FILE))`.
- *Orders by status:* `st.dataframe(status_report(DB_FILE))`.
- *Restock a product:* `st.form` with `st.selectbox` (from `product_names`), `st.number_input` (whole numbers, 0 or more) and a submit button calling `restock`.

### `reference/ism3232/bayside_dev_tests/` (reference only)

These live beside the app, not inside it: inside `bayside_app/`, `pytest` (and the autograder) would collect them and fail without Streamlit. Streamlit `AppTest` checks, run by the builders and not by `check.py`, each in a temporary folder with its own database: the app starts with no database file and creates it; two chat messages (keyword model) leave at least four entries in the stored history; one Approve click changes the order once and removes the request from the waiting list; a further rerun changes nothing; the restock form updates the stock. Students do not write app tests.

### Named on the Week 15 page as out of scope

Signing staff in (anyone who opens the app can approve), streaming replies, deploying the app online. Week 15 covers running Streamlit inside WSL and opening `localhost:8501` in the Windows browser.

## 6. Evaluation (Week 16)

### `evaluation.py`

- `CASES`: a list of dictionaries, each with `messages` (a list of one or more customer messages), `expect` (`tool`, `handoff`, `says`, or `never_says`) and, except for `handoff`, a `value`.
- `RUNS = 3`. For each case and run: `reset_database("evaluation.db")`, a new `SupportChatbot` with `BaysideTools("evaluation.db")` and `OllamaModel(MODEL_NAME)` (no fallback), send every message in order, then check:
  - `tool`: a `tool` history entry has `tool_name == value`;
  - `handoff`: the last reply contains `human agent`;
  - `says` / `never_says`: `value` does / does not appear in the last reply, ignoring capitals, after the reply's whitespace is normalized (`" ".join(reply.split())`);
  - `queued`: the number of waiting requests in `evaluation.db` equals `value`.
- Before the cases, one call checks the model answers; if not, the script prints that Ollama is not running and how to start it, and stops.
- Output: one row per case (the first message, shortened, and passes out of 3) and a total line. Students paste it into their README.
- Bayside's eight cases cover the lookup and stock tools, the three-turn address change (`queued` 1), `check_request`, the payment handoff, a question the instructions do not answer ("Do you price match?", `never_says` "we price match"), and the safety checklist: an address change with no order named (`queued` 0) and the false closing time (expected to fail). SQL text in an order ID is pinned by unit tests instead, because it does not depend on the model.

## 7. Checkpoints, real runs and how the pages use the app

The app lives in `reference/ism3232/bayside_app/`. Each week's layer ends in a checkpoint commit that the week's page builders read from, as Week 12 did:

| Week | Checkpoint adds |
|---|---|
| 13 | `schema.sql` (the model `PROPOSAL.md` is added in Phase 3, after the proposal template is settled) |
| 14 | `database.py`, `tools.py`, `agent.py`, `settings.py`, `main.py`, the four model files, `tests/` |
| 15 | `app.py` (its checks are in `bayside_dev_tests/`) |
| 16 | `evaluation.py` |

`*.db` files are gitignored (`reference/ism3232/**/*.db` in the parent `.gitignore`).

Real runs, on the CPU only (`CUDA_VISIBLE_DEVICES=-1 ollama serve`), saved under `reference/ism3232/runs/bayside_app/` with a `capture.sh`: a terminal conversation through `agent.py` and the database (Week 14), the app's chat and an approval round trip driven by `AppTest` with the course model (Week 15), the model-down path, the measured prompt size for 20 messages, and the full `evaluation.py` table (Week 16).

## 8. Checks for Phase 2

- `check.py` on `bayside_app` passes with `ollama` and `streamlit` blocked, under ruff 0.17.1 defaults.
- `bayside_dev_tests/` pass under the scratch environment with Streamlit 1.66.
- `agent.py` matches `module06_agents/chatbot.py` at `5bead57` apart from line 1; the three stand-in model files are byte-identical to Week 12's.
- Every listing a later page will need exists as a function, method or whole file, so builders can quote it with `pagekit.method`, `function` or `read`.
- The final whole-branch review of Phase 2 checks Review Focus items 4 and 5 from the parent plan against SQLite and Streamlit.

## 9. Left to later design passes

- **Week 13 (Phase 3):** the six starter businesses' names and sample data, the exact `PROPOSAL.md` template, Bayside's model proposal, how sign-off happens, the rubric's point tiers.
- **Weeks 14–16 (Phase 4):** each week's page outline, exercises and lab steps for students' own businesses.

## 10. Not in this phase

The Week 13–16 pages, the capstone rubric page, the starter menu, and the site sweep (Phases 3–5).
