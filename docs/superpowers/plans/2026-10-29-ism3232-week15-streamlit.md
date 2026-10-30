# ISM3232 Phase 4b: Week 15, Streamlit Chat & Staff Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace ISM3232 Week 15 with "Streamlit Chat & Staff — Reruns, Session State & Approvals" (five pages). Capture one real browser session of the Bayside checkpoint for screenshots and quoted text, prove the lab with an unpublished Spokewell build, and wire the new title into the site.

**Architecture:** As in Weeks 12–14, Python builders in `reference/ism3232/builders/` generate every page from verified sources:
- the Bayside app at its Week 15 checkpoint `8b1b491`, quoted exactly (`app.py` in contiguous named parts);
- one headless-Chrome session of that checkpoint on the course model, saved as `runs/week15/session.txt` plus three PNGs whose SHA-256 hashes the session file records;
- warm-up apps and counter results produced by driving the page's own code through `streamlit.testing.v1.AppTest`.

A verifier proves pages equal builder output and listings are verbatim. It also re-runs the counter slides, rebuilds the warm-up from the lab page, checks the quiz and the screenshots, runs Bayside's app checks, and checks the Spokewell build.

**Tech Stack:** Python 3.12; Streamlit 1.66.0 (`AppTest`); pytest 9.1.1; ruff 0.17.1; ollama 0.6.3 with `granite4.1:3b` on the CPU; websockets 17.2 driving headless Chrome 155 over the DevTools protocol; the static ISM3232 site in the `ism3232` submodule.

**Spec:** `docs/superpowers/specs/2026-10-20-ism3232-week15-streamlit-design.md`. House style and builder skeletons: the Week 14 plan, `docs/superpowers/plans/2026-10-19-ism3232-week14-database-tools.md`.

## Probe facts (2026-10-29, this machine, checkpoint `8b1b491`, Ollama off)

- `Runtime.evaluate` focus on `[data-testid=stChatInputTextArea]`, then `Input.insertText`, then `Input.dispatchKeyEvent` `keyDown`/`keyUp` with `key="Enter"`, `code="Enter"`, `windowsVirtualKeyCode=13` submits `st.chat_input`.
- A reply is done when `[data-testid=stChatMessage]` count reaches 2 per exchange and no `[data-testid=stSpinner]` is present. Tool entries are hidden, so each exchange draws exactly two messages.
- Message text is `[data-testid=stChatMessageContent]`'s `innerText`. A whole message's `innerText` starts with its avatar icon name: `face` for the user, `smart_toy` for the assistant.
- Waiting rows are `[data-testid=stText]`, and the notice is `[data-testid=stAlert]` (`"Request 1 approved."`). `st.dataframe` draws on a canvas, and its `innerText` is empty, so read table contents from the database file.
- Clicking `[role=tab]` index 1 shows Staff. After Approve's `st.rerun()` the Staff tab stays selected (`aria-selected="true"`). Wait for `aria-selected` before a screenshot: a click sent right after a reload was lost.
- `Page.reload` starts a new session: 0 chat messages afterwards.
- The three `WARMUP` files in Task 1 pass `ruff format --check` and `ruff check --isolated` as written. Through `AppTest.from_string` they give `Count: 1` (3 clicks), `Count: 3`, `Count: 0` (0 clicks), `Count: 2` (2 clicks), and the four echo bubbles in Task 1's test. `AppTest` prints "missing ScriptRunContext" warnings on stderr; they are harmless.
- `Emulation.setDeviceMetricsOverride(width=1200, height=1000, deviceScaleFactor=2, mobile=False)` with `streamlit run … --theme.base light` gives 2400×2000 PNGs. In them the sidebar radio and caption, the four chat messages and input, and the Staff tab through "Orders by status" are all readable.

## Global Constraints

- **Dates:** Week 15 is live by Monday 2026-11-30; Lab 15 is due Sunday 2026-12-06.
- **Title and labels:**
  - Title in HTML: `Streamlit Chat &amp; Staff — Reruns, Session State &amp; Approvals`. Plain text: `Streamlit Chat & Staff — Reruns, Session State & Approvals`. Short form, where Week 14 used `Database Tools`: `Streamlit Chat &amp; Staff`.
  - Week-strip label stays `W15 Streamlit`. Eyebrow `Unit 4 · Capstone Build`, colour `#fbbf24`.
- **Listing sources:** every listing comes from the Bayside app at `8b1b491`, `reference/ism3232/runs/week15/session.txt`, or text a builder generates by running code (returned in `derived`). Never type a listing or output by hand. Terminal output Streamlit prints (the email prompt, `Local URL`) is described in prose, not shown in a block.
- **Model runs and screenshots:**
  - Everything comes from one session captured by `runs/week15/capture.sh`, with `granite4.1:3b`, the server started on the CPU only with `CUDA_VISIBLE_DEVICES=-1 ollama serve`.
  - Never use `taskset`. Stop the server with `pkill -x ollama; pkill -x llama-server`.
  - The saved Phase 2 runs (`runs/bayside_app/app_session*.txt`) are never quoted.
  - Screenshots go to `ism3232/assets/img/week15/` and are re-taken only by re-running the capture, never edited.
- **Python new this week**, each explained in one line where it first appears:
  - unpacking `chat_tab, staff_tab = st.tabs(...)` and the three names from `st.columns(...)`;
  - `with` for page layout (students know `with open` from Week 6);
  - `in`, setting an attribute and `del` on `st.session_state`;
  - keyword arguments such as `key=` and `min_value=`;
  - the backslash in `"\\$"`.

  Never taught: widget callbacks (`on_click`), `st.cache_*`, sign-in, streaming, deploying, FastAPI.
- **Lab rules:**
  - The warm-up runs in `~/ism3232/sql_practice` with the capstone venv active; students build in `~/ism3232/module07_final_project`.
  - Commit message: `lab 15: streamlit app`.
  - At least 15 tests in `tests/test_database.py`, `tests/test_tools.py` and `tests/test_agent.py`. Students write no app tests, and no test imports `app.py` or `ollama_model.py`.
- **Bayside is frozen:** nothing under `reference/ism3232/bayside_app/` changes. If a build step finds a bug in it, stop and ask the user.
- **The Spokewell build:** it lives only in git-ignored `reference/ism3232/_private/`. The parent repo is public, so nothing there is ever staged. Pages show Spokewell names only inside the lab's mapping tables (function, class and column names), never Spokewell code.
- **Privacy:** never name the midterm businesses, versions, last-name ranges or exam handling. Do not reuse Lakeshore, Stitchline or Bayside Tax Help.
- **Builders:** `build()` returns `(page, derived)` and writes only from `__main__`. Week 15 pages take their heads from the Week 14 pages. No lecture video block.
- **Lab slides:** every Streamlit block is static, `code_slide(..., readonly=True, lang="shell")`, because Pyodide has no Streamlit. A readonly Python block would get a Run button.
- **Quiz options:** no option may contain ` - `, ` -- ` or ` — `.
- **Lint:** new Python files pass `"$PY" -m ruff format --check` and `"$PY" -m ruff check --isolated`. Wrap implicit string concatenations inside lists in parentheses (ISC004).
- **Environment:**
  - Run from the parent repo root `/home/markumreed/Documents/ism_courses` unless a step says otherwise. `cd` inside a Bash call moves the session, so use `( cd … && … )` subshells.
  - `SCRATCH` is this session's scratchpad, and `PY="$SCRATCH/probe-venv/bin/python"`. If that Python is missing, run from `$SCRATCH` (uv inside the repo drops `uv.lock` at the root): `uv venv --python 3.12 probe-venv && uv pip install --python probe-venv/bin/python streamlit==1.66.0 ollama==0.6.3 websockets==17.2 pytest==9.1.1 ruff==0.17.1 pyyaml==6.0.3`.
  - `SQLITE3_CLI="$SCRATCH/sqlite3-3.45.1/unpacked/usr/bin/sqlite3"`, needed by `verify_week13.py`. Recreate it with `"$PY" -B reference/ism3232/tools/sqlite_cli.py "$SCRATCH/sqlite3-3.45.1"`.
  - Test folders run from inside themselves: `(cd reference/ism3232/builders && "$PY" -B -m pytest -q -p no:cacheprovider)`.
  - zsh: overwrite with `>|`; quote globs; never name a variable `path`; delete scratch files with `command rm -f`.
- **Commits:**
  - Commit to the parent's `main`, locally. End messages with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.
  - Stage only this plan's files. If another session has edits in `_build_qti.py`, stage only the Week 15 line (`git hash-object -w` plus `git update-index --cacheinfo`).
  - Pages and images in `ism3232/` ship only on the user's word.
  - Rulings and deviations go in the ledger `.superpowers/sdd/2026-10-29-ism3232-week15-streamlit/progress.md` (git-ignored).

## Review Focus

1. **A screenshot and its caption from different runs, or a "model" session the keyword rules answered.** Causes: re-taking one PNG; Ollama down, so `FallbackModel` falls back without a word. Expected: the three PNGs hash to what `session.txt` records, and the session shows the course model filing the address change. Pinned by `test_the_images_are_the_ones_this_session_took` and `test_the_request_waits_with_the_customers_address` (Task 2), and by `capture.sh`'s `ollama ps` check.
2. **A warm-up that does not reproduce from the page.** Causes: a file name that differs from its label, a missing `st.session_state` start-up line, an expected box from the constants rather than the page. Expected: the page's own blocks, driven through `AppTest`, give every box. Pinned by `test_a_lab_page_missing_echo_is_reported` and `test_a_lab_page_whose_box_is_wrong_is_reported` (Task 3), and the verifier in Task 6.
3. **A student's project failing the autograder.** Causes: a test that imports `app.py` (Streamlit is blocked), fewer than 15 tests, or an edit function that changes every row. Expected: following Parts 3–8 gives a project that passes `check.py` with 15+ tests. Pinned by the Spokewell build (Task 7), including `test_set_part_stock_leaves_other_parts_alone`.
4. **Customer text formatting the Staff tab, or a double Approve changing a record twice.** Expected: Markdown, links and `$` in a typed value show as plain text, and a second Approve changes nothing. Pinned by Bayside's `test_a_typed_address_is_plain_text_on_the_staff_tab` and `test_one_approve_click_changes_the_order_once`, run by the verifier. Spokewell's `test_a_typed_value_is_plain_text_on_the_staff_tab` and `test_one_approve_click_changes_the_repair_once` pin the same (Task 7).
5. **Wiring that changes Week 14 beyond its next link, or leaves the old title behind.** Expected: the Week 14 diff shows only the next-link title, `verify_week14` passes, and no `Streamlit Interface` or `Streamlit Business Interface` is left in the files the spec names. Pinned by Task 8 Steps 2 and 5.

---

### Task 1: Week 15 facts, app parts, warm-up apps and AppTest results

**Files:**
- Create: `reference/ism3232/builders/week15_common.py`
- Test: `reference/ism3232/builders/test_week15_common.py`

**Interfaces:**
- Consumes:
  - `pagekit` (`REF`, `ROOT`, `read`, `function`, `folder_at`);
  - `week14_common.build_folder`;
  - the Bayside app at `8b1b491`.
- Produces (`week15_common`, imported as `w`):
  - constants:
    - `WEEK = "week15"`, `TITLE`, `TITLE_TEXT`, `SHORT = "Streamlit Chat &amp; Staff"`, `EYEBROW_COLOR`, `UNIT`;
    - `PREV = ("week14", "Week 14", "Database Tools — sqlite3, Placeholders &amp; Tested Tools")`, `NEXT = ("week16", "Week 16", "GenAI Feature &amp; Final Demo")`;
    - `REV = "8b1b491"`, `APP = "bayside_app/"`, `APP_FOLDER`, `RUNS = REF / "runs" / WEEK`, `IMAGES = ROOT / "ism3232" / "assets" / "img" / WEEK`;
    - `COMMIT = "lab 15: streamlit app"`, `CLICKS = 3`, `ECHO_MESSAGES = ["hello", "Where is order A100?"]`;
    - `WARMUP` (file name → text), `LABELS = {"counter": "counter.py", "counter_state": "counter_state.py", "echo": "echo.py"}`, `APP_PARTS` (part name → the text of its first line, in file order).
  - functions:
    - `app_file(name) -> str`, `app_function(name) -> str` (a function in `database.py`), `app_test(name) -> str` (a function in `tests/test_database.py`), `app_part(name) -> str`;
    - `checkpoint_folder() -> Path`;
    - `counter_after_clicks(code, clicks) -> str`, `echo_bubbles(code, messages) -> str`, `with_clicks(code, clicks, shown) -> str`, `warmup_results() -> dict[str, str]`.

- [ ] **Step 1: Write the failing tests** in `reference/ism3232/builders/test_week15_common.py` (header and `sys.path` lines as in `test_week14_common.py`):

```python
import subprocess

import week15_common as w
from pagekit import REF
from week14_common import build_folder


def test_counter_without_session_state_stays_at_one():
    assert w.counter_after_clicks(w.WARMUP["counter.py"], 3) == "Count: 1"


def test_counter_with_session_state_counts_and_a_new_session_starts_at_zero():
    code = w.WARMUP["counter_state.py"]
    assert w.counter_after_clicks(code, 3) == "Count: 3"
    assert w.counter_after_clicks(code, 0) == "Count: 0"


def test_echo_draws_four_bubbles_for_two_messages():
    assert w.echo_bubbles(w.WARMUP["echo.py"], w.ECHO_MESSAGES) == (
        "user: hello\n"
        "assistant: You said: hello\n"
        "user: Where is order A100?\n"
        "assistant: You said: Where is order A100?"
    )


def test_the_warmup_files_pass_ruff():
    folder = build_folder(w.WARMUP)
    for args in (["format", "--check", "."], ["check", "--isolated", "."]):
        result = subprocess.run(
            [sys.executable, "-m", "ruff", *args],
            cwd=folder,
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0, result.stdout


def test_app_parts_cover_app_py_in_order():
    parts = [w.app_part(name) for name in w.APP_PARTS]
    shown = [line for part in parts for line in part.split("\n") if line.strip()]
    whole = [line for line in w.app_file("app.py").split("\n") if line.strip()]
    assert shown == whole


def test_the_chat_part_draws_the_history_and_reruns():
    chat = w.app_part("chat")
    assert chat.startswith("with chat_tab:")
    assert chat.endswith("st.rerun()")


def test_bayside_app_py_has_not_changed_since_the_checkpoint():
    assert (REF / "bayside_app" / "app.py").read_text() == w.app_file("app.py")


def test_with_clicks_writes_the_slide_convention():
    assert w.with_clicks("x = 1", 3, "Count: 1") == (
        "x = 1\n\n# After 3 clicks the page shows:\n# Count: 1"
    )
```

- [ ] **Step 2: Run them to see them fail.**
Run: `(cd reference/ism3232/builders && "$PY" -B -m pytest test_week15_common.py -q -p no:cacheprovider)`
Expected: collection error `No module named 'week15_common'`.

- [ ] **Step 3: Write `reference/ism3232/builders/week15_common.py`.**
  - Its docstring and helpers follow `week14_common.py`.
  - `WARMUP` holds exactly these three files. They are page copy: what students type, and the warm-up's expected results depend on them.

```python
WARMUP = {
    "counter.py": """# counter.py
import streamlit as st

count = 0
if st.button("Add one"):
    count = count + 1
st.write(f"Count: {count}")
""",
    "counter_state.py": """# counter_state.py
import streamlit as st

if "count" not in st.session_state:
    st.session_state.count = 0
if st.button("Add one"):
    st.session_state.count = st.session_state.count + 1
st.write(f"Count: {st.session_state.count}")
""",
    "echo.py": """# echo.py
import streamlit as st

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

text = st.chat_input("Say something")
if text:
    reply = f"You said: {text}"
    st.session_state.messages.append({"role": "user", "content": text})
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()
""",
}
```

  - `APP_PARTS` tiles `app.py`. Each part runs from the line containing `first` up to, but not including, the line containing the next part's `first`; the last part runs to the end of the file. `app_part` returns the slice with trailing blank lines stripped, read with `read(APP + "app.py", REV)`.

```python
APP_PARTS = {
    "imports": "# app.py",
    "top": "COURSE_MODEL =",
    "sidebar": "create_tables(DB_FILE)",
    "bot": 'if "bot" not in st.session_state:',
    "tabs": "chat_tab, staff_tab = st.tabs(",
    "chat": "with chat_tab:",
    "notice": "with staff_tab:",
    "waiting": 'st.subheader("Waiting for approval")',
    "tables": 'st.subheader("Orders")',
    "restock": 'st.subheader("Restock a product")',
}
```

  `'st.subheader("Orders")'` does not match `"Orders by status"`.
  - `counter_after_clicks(code, clicks)`:
    1. `AppTest.from_string(code, default_timeout=30)`, then `run()`;
    2. `button[0].click().run()` `clicks` times;
    3. return the `.value` of every `markdown` element, joined with `"\n"`.

    Raise if `at.exception` is non-empty.
  - `echo_bubbles(code, messages)`: `from_string`, `run()`, then `chat_input[0].set_value(m).run()` for each message. Return `f"{bubble.name}: {bubble.markdown[0].value}"` per `chat_message`, joined with `"\n"`.
  - `with_clicks(code, clicks, shown)`: `code.rstrip()`, a blank line, `# After {clicks} clicks the page shows:`, then each line of `shown` prefixed `# `. This is the slide convention the verifier re-runs.
  - `warmup_results()` returns:
    - `"counter"`: `counter.py` after `CLICKS`;
    - `"counter_state"`: `counter_state.py` after `CLICKS`;
    - `"fresh"`: `counter_state.py` after 0 clicks;
    - `"echo"`: `echo.py` with `ECHO_MESSAGES`.
  - `app_test(name)` is `function(APP + "tests/test_database.py", name, REV)`; `checkpoint_folder()` is `folder_at(REV, APP_FOLDER)`.

- [ ] **Step 4: Run the tests.**
Run: the Step 2 command. Expected: `8 passed`.

- [ ] **Step 5: Lint and commit.**
```bash
git add reference/ism3232/builders/week15_common.py reference/ism3232/builders/test_week15_common.py
git commit -m "Week 15: checkpoint facts, app.py parts, warm-up apps and their AppTest results" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 2: The captured browser session

**Files:**
- Create:
  - `reference/ism3232/runs/week15/session.py` (the driver);
  - `reference/ism3232/runs/week15/capture.sh`;
  - `reference/ism3232/runs/week15/session.txt` (captured);
  - `ism3232/assets/img/week15/{chat,staff_waiting,staff_approved}.png` (captured).
- Modify: `reference/ism3232/builders/week15_common.py` (add `session_steps`, `ALT`, `figure`)
- Test: `reference/ism3232/builders/test_week15_runs.py`

**Interfaces:**
- Consumes: `w.RUNS`, `w.IMAGES` (Task 1).
- Produces:
  - `w.session_steps() -> dict[str, str]`: section name → body, from `session.txt`;
  - `w.ALT` (image name → alt text);
  - `w.figure(name, caption) -> str`: `<figure class="shot"><img src="../assets/img/week15/{name}" alt="{ALT[name]}" width="1200" height="1000" loading="lazy"><figcaption>{caption}</figcaption></figure>`.

- [ ] **Step 1: Write the failing tests** in `reference/ism3232/builders/test_week15_runs.py`:

```python
import hashlib

import week15_common as w


def test_the_request_waits_with_the_customers_address():
    assert w.session_steps()["staff waiting"] == "Request 1: A102 to 9 Pine Street, Tampa"


def test_approve_shows_the_notice_and_changes_the_order():
    steps = w.session_steps()
    assert steps["staff approved"] == "Request 1 approved."
    assert "A102 delivered 9 Pine Street, Tampa" in steps["orders"].split("\n")


def test_the_last_answer_reports_the_approval():
    last = w.session_steps()["chat after approval"].split("\n")[-1]
    assert last.startswith("Sunny: ") and "approved" in last.lower()


def test_a_refresh_clears_the_chat():
    assert w.session_steps()["after a refresh"] == "chat messages: 0"


def test_the_images_are_the_ones_this_session_took():
    for line in w.session_steps()["images"].split("\n"):
        name, digest = line.split()
        data = (w.IMAGES / name).read_bytes()
        assert hashlib.sha256(data).hexdigest() == digest
        assert data[16:24] == (2400).to_bytes(4, "big") + (2000).to_bytes(4, "big")
```

- [ ] **Step 2: Run them to see them fail.**
Run: `(cd reference/ism3232/builders && "$PY" -B -m pytest test_week15_runs.py -q -p no:cacheprovider)`
Expected: 5 failed (`AttributeError: … session_steps`).

- [ ] **Step 3: Add `session_steps()` to `week15_common.py`.** It reads `RUNS / "session.txt"` and splits on lines starting `## `; each body is stripped of surrounding newlines. Lines before the first `## ` (the header comment) are ignored.

- [ ] **Step 4: Write the driver `reference/ism3232/runs/week15/session.py`.**
  - Usage: `python session.py APP_COPY SESSION_TXT IMAGES_DIR`.
  - It writes nothing until every step succeeds. On any timeout it exits 1, naming the step.
  - It always terminates Chrome and Streamlit in a `finally`.
  - CDP plumbing as in `reference/ism3232/tools/streamlit_shots.py`, plus `js(expr)` (`Runtime.evaluate` with `returnByValue=True`) and `wait_for(expr, timeout)` (poll every 0.5 s).

  1. **Start the app.** Run Streamlit inside `APP_COPY`: `sys.executable -m streamlit run app.py --server.headless true --server.port <free> --theme.base light --browser.gatherUsageStats false`. Wait for `http://127.0.0.1:<port>/_stcore/health`.
  2. **Start Chrome.** `google-chrome --headless=new --disable-gpu --remote-debugging-port=<free> --window-size=1200,1000 --user-data-dir=<new temp dir> about:blank`.
  3. **Open the page.** `Page.enable`, `Emulation.setDeviceMetricsOverride(width=1200, height=1000, deviceScaleFactor=2, mobile=False)`, `Page.navigate`, then wait for the chat input.
  4. **Chat.** Send `"Has A101 shipped yet?"`, then `"Please change the address on order A102 to 9 Pine Street, Tampa"`, typed as in Probe facts. After exchange *k*, wait up to 300 s for `2k` messages and no spinner. Screenshot `chat.png`.
  5. **Staff, waiting.** Click tab 1, wait until its `aria-selected` is `"true"`, then 1 s more. Read the `stText` texts. Screenshot `staff_waiting.png`.
  6. **Approve.** Click the button whose trimmed `innerText` is `Approve`. Wait for an `stAlert`, then confirm tab 1 is still selected (click it and wait if not). Read the alert text. Screenshot `staff_approved.png`.
  7. **Orders.** Read the orders straight from `APP_COPY/bayside.db` with `sqlite3`: `SELECT order_id, status, address FROM orders ORDER BY order_id`, one line each, `f"{order_id} {status} {address}"`.
  8. **Ask about the request.** Click tab 0, wait for it to be selected, send `"What happened to request 1?"`, and wait for 6 messages.
  9. **Refresh.** `Page.reload`, wait for the chat input, then record the `stChatMessage` count.

  Write `SESSION_TXT` in exactly this shape. Each chat line is `You: ` or `Sunny: ` (from the avatar icon) plus the `stChatMessageContent` text. The images section holds each PNG's name and SHA-256 hex digest.

```text
# Week 15 session: Bayside app at 8b1b491, granite4.1:3b on the CPU, captured by session.py
## chat
You: Has A101 shipped yet?
Sunny: …
You: Please change the address on order A102 to 9 Pine Street, Tampa
Sunny: …
## staff waiting
Request 1: A102 to 9 Pine Street, Tampa
## staff approved
Request 1 approved.
## orders
A100 shipped 14 Bay Road
…
## chat after approval
You: What happened to request 1?
Sunny: …
## after a refresh
chat messages: 0
## images
chat.png <sha256>
staff_waiting.png <sha256>
staff_approved.png <sha256>
```

- [ ] **Step 5: Write `reference/ism3232/runs/week15/capture.sh`** (then `chmod +x` it):

```bash
#!/usr/bin/env bash
# Re-capture the Week 15 browser session from the Bayside Week 15 checkpoint.
# Start the server first, on the CPU only:  CUDA_VISIBLE_DEVICES=-1 ollama serve
# PY must point to a Python with streamlit, ollama and websockets. Run from the repository root.
set -eu
PY=${PY:?set PY to a Python that has streamlit, ollama and websockets}
ollama list | grep -q 'granite4.1:3b' || { echo "Ollama is not running, or granite4.1:3b is not pulled"; exit 1; }
COPY=$("$PY" -B -c "import sys; sys.path.insert(0,'reference/ism3232/builders'); from pagekit import folder_at; print(folder_at('8b1b491', 'reference/ism3232/bayside_app'))")
mkdir -p ism3232/assets/img/week15
"$PY" -B reference/ism3232/runs/week15/session.py "$COPY" reference/ism3232/runs/week15/session.txt ism3232/assets/img/week15
ollama ps | grep -q 'granite4.1:3b' || { echo "The course model was not loaded: the keyword rules may have answered"; exit 1; }
```

- [ ] **Step 6: Debug on the GPU, then capture on the CPU.**
  1. While writing the driver, run it against a normal `ollama serve`, which is fast. Those files are drafts; delete them with `command rm -f`.
  2. Then `pkill -x ollama; pkill -x llama-server`, start `(CUDA_VISIBLE_DEVICES=-1 ollama serve >| "$SCRATCH/ollama15.log" 2>&1 &)`, and wait in a background until-loop for `ollama list` to succeed.
  3. Run `PY="$PY" reference/ism3232/runs/week15/capture.sh`, then stop the server.

  Read `session.txt` in full and look at all three PNGs.
  - Keep whatever the model said, true or false; the pages quote real runs.
  - If the model did not file the request (no waiting row), run the capture once more. If it fails again, stop and ask the user; do not change the customer's wording.

- [ ] **Step 7: Add `ALT` and `figure` to `week15_common.py`.** Write each alt text after looking at its image: what the screen shows, including the Staff tab's waiting row and the notice. Do not repeat Sunny's wording.

- [ ] **Step 8: Run the tests, then commit** (the PNGs stay uncommitted in `ism3232/` until shipping):
Run: the Step 2 command. Expected: `5 passed`.
```bash
git add reference/ism3232/runs/week15 reference/ism3232/builders/week15_common.py reference/ism3232/builders/test_week15_runs.py
git commit -m "Week 15 real session: Bayside 8b1b491 in headless Chrome on the CPU, three screenshots" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 3: The Week 15 verifier

**Files:**
- Modify: `reference/ism3232/builders/pagekit.py` (add `files_at`)
- Create: `reference/ism3232/builders/verify_week15.py`
- Test: `reference/ism3232/builders/test_verify_week15.py`

**Interfaces:**
- Consumes:
  - `week15_common` (Tasks 1–2);
  - `verify_week13` (`plain`, `expected_misses`, `quiz_problems`);
  - `verify_week14` (`BLOCK`, `EXPECTED`);
  - `pagekit` (`DOCS`, `REF`, `ROOT`, `check_listings`).
- Produces:
  - `pagekit.files_at(rev, folder) -> list[str]`: every file under `folder` at `rev`, as text. It is the body of `verify_week14.checkpoint_sources` with `rev` and `folder` as parameters; `verify_week14` itself is not touched;
  - `verify_week15`:
    - `PAGES`, `SPOKEWELL`, `SPOKEWELL_TESTS`;
    - `counter_slide_problems(text) -> list`, `warmup_problems(lab_text) -> list`, `image_problems(text) -> list`;
    - `page_problems(name) -> list`: every check that concerns one page, used by Tasks 4–6 as each page is built;
    - `bayside_app_problems() -> list`, `spokewell_problems() -> list`;
    - `main() -> int`.

- [ ] **Step 1: Write the failing tests** in `reference/ism3232/builders/test_verify_week15.py`:

```python
import verify_week15 as v
import week15_common as w
from pagekit import code_block, esc, expected


def lab_page(drop=None, wrong=False):
    """A lab page holding the three warm-up files and their four expected boxes."""
    results = w.warmup_results()
    if wrong:
        results["counter"] = "Count: 3"
    parts = [code_block(label, w.WARMUP[label], python=False) for label in w.LABELS.values()]
    parts += [expected(text) for text in results.values()]
    if drop is not None:
        parts.pop(drop)
    return "\n".join(parts)


def test_a_lab_page_with_the_warmup_has_no_problems():
    assert v.warmup_problems(lab_page()) == []


def test_a_lab_page_missing_echo_is_reported():
    assert v.warmup_problems(lab_page(drop=2)) != []


def test_a_lab_page_whose_box_is_wrong_is_reported():
    assert v.warmup_problems(lab_page(wrong=True)) != []


def slide(code, clicks, shown):
    return f'<pre><code class="language-python">{esc(w.with_clicks(code, clicks, shown))}</code></pre>'


def test_a_counter_slide_that_matches_passes():
    assert v.counter_slide_problems(slide(w.WARMUP["counter.py"], 3, "Count: 1")) == []


def test_a_counter_slide_that_differs_is_reported():
    assert v.counter_slide_problems(slide(w.WARMUP["counter.py"], 3, "Count: 3")) != []


def test_a_missing_screenshot_is_reported():
    assert v.image_problems('<img src="../assets/img/week15/chat.png" alt="x">') == []
    assert v.image_problems('<img src="../assets/img/week15/nope.png" alt="x">') != []
```

- [ ] **Step 2: Run them to see them fail.**
Run: `(cd reference/ism3232/builders && "$PY" -B -m pytest test_verify_week15.py -q -p no:cacheprovider)`
Expected: collection error `No module named 'verify_week15'`.

- [ ] **Step 3: Write `verify_week15.py`** on `verify_week14.py`'s structure. The docstring lists what it proves (spec section 5).
  - `counter_slide_problems(text)`:
    1. For every `<code class="language-python">` block holding `"\n# After N clicks the page shows:\n"`, take `N` and the shown lines without their `# `.
    2. Compare them with `w.counter_after_clicks(code, N)`.
    3. Return the first line of each block that differs.
  - `warmup_problems(lab_text)`:
    1. Find the blocks labelled with `w.LABELS` values (`BLOCK`, `plain`); report any that are missing.
    2. Compute the four results from the page's own code, as `warmup_results()` does from `WARMUP`.
    3. Report each result that matches no `EXPECTED` box (`plain(box).rstrip()`).
  - `image_problems(text)`: every `src="../assets/img/week15/<name>"` must exist in `w.IMAGES`.
  - `bayside_app_problems()`: run `"$PY" -B -m pytest -q -p no:cacheprovider reference/ism3232/bayside_dev_tests/test_app.py` from `ROOT`, the way its docstring says. Report the last output line on failure.
  - `spokewell_problems()`: return `[]` when `SPOKEWELL` (`REF/"_private"/"spokewell"`) is absent. Otherwise, as in Week 14:
    - `check.py` passes;
    - at least **15** tests are collected;
    - `smoke.py` exits 0;
    - and, new, `pytest -q -p no:cacheprovider` on `SPOKEWELL_TESTS` (`REF/"_private"/"spokewell_dev_tests"`) passes.
  - `page_problems(name)` builds the page with its builder, then checks:
    1. the page on disk equals the builder's output;
    2. `check_listings` against `files_at(w.REV, w.APP_FOLDER)`, `session.txt`'s text and the page's `derived`;
    3. `image_problems`;
    4. `counter_slide_problems`, for `week15_slides` and `week15_lecture`;
    5. `warmup_problems` and `expected_misses(page, set(w.warmup_results().values()))`, for `week15_lab`;
    6. `quiz_problems`, for `week15_reading`.

    Each problem is prefixed with the page name.
  - `main()`: `page_problems` for each of `PAGES`, then `bayside_app_problems()` and `spokewell_problems()`. Print each problem, then `verify_week15: OK` or the count; exit 1 on problems.

- [ ] **Step 4: Run the tests.** Expected: `6 passed`.

- [ ] **Step 5: Lint and commit.**
```bash
git add reference/ism3232/builders/pagekit.py reference/ism3232/builders/verify_week15.py reference/ism3232/builders/test_verify_week15.py
git commit -m "Week 15 verifier: stale pages, listings, counter slides, warm-up rebuilt from the lab page, quiz, screenshots, app checks, Spokewell" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 4: Week 15 reading

**Files:**
- Create: `reference/ism3232/builders/week15_reading.py`
- Writes: `ism3232/docs/week15_reading.html`

**Interfaces:**
- Consumes: `week15_common` (Tasks 1–2); the `pagekit` reading helpers `week14_reading.py` uses.
- Produces: `build() -> (page, derived)`. `derived` holds `warmup_results()` values and every typed command block. Its 10 `.quiz-item` blocks become the Week 15 Canvas quiz.

- [ ] **Step 1: Write the builder** on `week14_reading.py`'s skeleton:
  - `head_from("week14_reading.html", f"ISM3232 Week 15 — {w.TITLE_TEXT}")`;
  - eyebrow `Unit 4 · Capstone Build · Module 15 · Reading`;
  - deck: "Put a web page in front of your agent: a Chat tab for customers and a Staff tab where people approve what the agent asked for.";
  - weekjump to `week15_reading/lecture/lab.html`;
  - footer `ISM3232 · Week 15 · {w.TITLE}`;
  - a page-local style `.shot{margin:18px 0}.shot img{max-width:100%;height:auto;border:1px solid var(--border);border-radius:8px}.shot figcaption{font-size:13px;color:var(--muted);margin-top:6px}`.

  Sections, following spec section 4 "Reading":
  1. **Objective**, then **Coming from Week 14**: "Staff still can't approve anything without running Python."
  2. **At a glance**: reading about 60 minutes, lecture 75, lab about 3 hours. Prerequisites: Week 14's tests passing. Then the spec's eight outcomes as an `<ol>`.
  3. **What you build this week:** `w.figure("chat.png", …)`.
  4. **Streamlit runs everything again:**
     - `listing("counter.py", WARMUP["counter.py"])` and `listing("After 3 clicks", results["counter"])`;
     - the same for `counter_state.py`, with `results["counter_state"]` and, after a refresh, `results["fresh"]`;
     - the Week 11 callback paragraph: the model remembers nothing, so the history is sent every time; Streamlit remembers nothing either;
     - one line each on `in`, setting an attribute, and `del`.
  5. **The chat:**
     - `app_part("imports")`, then `app_part("top")`, with one line on the backslash in `"\\$"`;
     - `app_part("sidebar")` and `app_part("bot")`, explaining that `bot.model = make_model(choice)` runs on every rerun, so switching models keeps the conversation;
     - `app_part("tabs")`, with the unpacking line;
     - `app_part("chat")`, with `with` for layout;
     - `listing("The chat in the session", session_steps()["chat"])`, beside the figure from section 3.
  6. **The Staff tab:**
     - `app_part("notice")` and `app_part("waiting")`, with `st.columns` unpacking and `key=`, and `figure("staff_waiting.png", …)`;
     - `app_part("tables")` with `app_function("status_report")`, tied to Week 13's GROUP BY;
     - `app_part("restock")` with `app_function("restock")` and `app_function("product_names")`, and why `st.form` waits for its button before rerunning.
  7. **One round trip:**
     1. the `chat` step;
     2. `figure("staff_approved.png", …)` with the `staff approved` and `orders` steps;
     3. the `chat after approval` step;
     4. the `after a refresh` step: "the chat is gone; the address change is still in `bayside.db`."
  8. **Customer text is data:** `st.text` on staff rows and the `$` escape. A `callout("warn", …)` names the open limit: anyone who opens the app can approve, because there is no sign-in.
  9. **Running it:**
     - `streamlit run app.py` (typed block);
     - the first-run "Welcome to Streamlit!" email prompt (press Enter), in prose;
     - `http://localhost:8501`, and from WSL in the Windows browser;
     - Ctrl+C stops the server;
     - refresh versus database;
     - keyword-only mode: lookups work, filing a change does not.
  10. **Why `app.py` has no tests:** the autograder runs without Streamlit, so the logic lives in the tested files and `app.py` stays thin. Name `app_test("test_status_report_counts_orders")` and `app_test("test_restock")` as the models for this week's tests.
  11. **What this module leaves out, and why:**
      - staff sign-in (accounts and passwords are a course of their own, so the pages name the limit instead);
      - streaming replies;
      - deploying online (the model runs on your laptop);
      - caching (the Staff tab must always show fresh data);
      - the old FastAPI material (the capstone has no second program to talk to).
  12. **Key terms:** rerun, session state, widget, chat message, tab, column, form, dataframe, widget key. Then **Before you leave**, and the **Module Quiz** (`<h2 id="quiz">`) with exactly these 10 items:
      1. `quiz_mc` "A counter shows Count: 1 after three clicks. Why?"
         - Options: "Streamlit runs the whole script again on every click, so count = 0 runs again"; "The button works only once"; "st.write keeps the first value it showed"; "The browser ignores repeated clicks".
         - Answer 0; why "Every click reruns the script from the top. Only st.session_state keeps a value between runs."
      2. `quiz_tf` "Refreshing the browser clears the chat but keeps an approved change." True; "The chat lives in st.session_state, which starts empty in a new session. The decision is in the database."
      3. `quiz_trace` "What does the page show after two clicks?"
         - Code: `WARMUP["counter_state.py"]`. Answer: `counter_after_clicks(that code, 2)`.
         - Why "st.session_state.count survives each rerun, so each click adds one to the kept value."
      4. `quiz_mc` "Why does app.py create the chatbot inside if "bot" not in st.session_state?"
         - Options: "So the same chatbot, with its history, is used on every rerun"; "So the chatbot answers faster"; "Because a SupportChatbot can only be created once"; "So the database is created only once".
         - Answer 0; why "Without it, every rerun would build a new chatbot with an empty history."
      5. `quiz_mc` "Why does the Staff tab show each request with st.text?"
         - Options: "So text a customer typed cannot format the page or add a link"; "st.text is faster than st.markdown"; "st.markdown cannot show numbers"; "st.text saves the request".
         - Answer 0; why "Customer text is data. st.text shows it exactly as typed."
      6. `quiz_tf` "Clicking Reject deletes the change request." False; "It marks the request rejected. The order does not change, and the request cannot be approved later."
      7. `quiz_mc` "Why does app.py have no tests?"
         - Options: "The autograder runs without Streamlit, so the logic lives in tested files and app.py stays thin"; "Streamlit apps cannot be tested at all"; "app.py never changes"; "pytest cannot import a file named app.py".
         - Answer 0.
      8. `quiz_mc` "What does st.form change about the restock inputs?"
         - Options: "Nothing reruns until the form's submit button is pressed"; "The inputs are saved to the database by themselves"; "The form clears the table first"; "The form keeps its values after a refresh".
         - Answer 0; why "Changing the dropdown or the number waits; Save sends both at once."
      9. `quiz_trace` "What does Bayside's show() pass to st.markdown for this text?"
         - Code: `show("Total: $5 and $6")`. The answer is computed in the builder as `"Total: $5 and $6".replace("$", "\\$")`, which is the expression in `show`.
         - Why "Each $ gets a backslash, so Streamlit shows a dollar sign instead of reading $5 and $6 as math."
      10. `quiz_short` "Anyone who opens the Bayside app can approve a request. What would a real business add, and why does Week 15 leave it out?" Answer: "A staff sign-in, so only staff can open the Staff tab and approve. It is left out to keep the course on the agent and its data, and the pages name it as the app's open limit."
  13. **Closing:** "The app runs. Next week: how often is it right?" Then `prev_next` with `w.PREV` / `w.NEXT` (`week14_reading.html` / `week16_reading.html`) and the footer.

- [ ] **Step 2: Build and check.**
Run: `"$PY" -B reference/ism3232/builders/week15_reading.py && "$PY" -B -c "import sys; sys.path.insert(0,'reference/ism3232/builders'); import verify_week15 as v; print(v.page_problems('week15_reading'))"`
Expected: `[]`.
- [ ] **Step 3: Look at it** in light, dark and 390 px width (`"$PY" -m http.server 8815` from inside `ism3232`, in the background, stopped by its PID). Then run `python3 _build_qti.py`. Expected: the ISM3232 Week 15 quiz has 10 questions.
- [ ] **Step 4: Lint and commit** `week15_reading.py` ("Week 15 reading builder").

### Task 5: Week 15 lecture and slides

**Files:**
- Create: `reference/ism3232/builders/week15_lecture.py`, `reference/ism3232/builders/week15_slides.py`
- Writes: `ism3232/docs/week15_lecture.html`, `ism3232/docs/week15_slides.html`

**Interfaces:**
- Consumes: as Task 4, plus the lecture and slide helpers `week14_lecture.py` and `week14_slides.py` use.
- Produces: `build() -> (page, derived)` for each page.

- [ ] **Step 1: Write `week15_lecture.py`** on `week14_lecture.py`'s skeleton:
  - `head_from("week14_lecture.html", …)`, `course_map("W15 ")`;
  - prev/next to `week14_lecture.html` and `week16_lecture.html`;
  - no video block.

  Then the session-plan table and six sections, from the spec's lecture table:
  1. **0–8, Where Week 14 left off.** `main.py`'s staff review in a terminal: who would use that? Prose only.
  2. **8–25, Reruns, live.** The two counters as `code_block` with their results (derived), and the Week 11 callback.
  3. **25–45, The chat, live.** `app_part("bot")` and `app_part("chat")`, plus a card: switch the sidebar model mid-chat and the conversation stays.
  4. **45–60, The Staff tab, live.** `app_part("waiting")`, the session's `staff waiting` and `staff approved` steps, and `figure("staff_approved.png", …)`. Add the page-local `.shot` style from Task 4.
  5. **60–68, Customer text is data.** Type `[click me](https://example.com) $5 and $6` as an address from `python3` with `add_change_request` (a typed block) and show where it lands, as plain text; this is Bayside's own app-check value. Then `app_part("top")` for `show`.
  6. **68–75, Your project.** The Bayside → yours map from the lab's Part 3, the three new tests, and "next week: how often is it right?"

  Three discussion questions (`prompt_list`):
  - "Which of your records should staff change on the Staff tab, and which should change only through a request?"
  - "What would go wrong if the chatbot were created outside session_state?"
  - "Who should be able to open your Staff tab, and how would a real business make sure?"

  A misconceptions card with the spec's four. The Lab 15 deliverables come from `assignment`, ending with `NO_SCREENSHOTS`.
- [ ] **Step 2: Write `week15_slides.py`** on `week14_slides.py`'s skeleton:
  - `slides_shell("week14_slides.html")`, `<title>` set to Week 15;
  - `slide_title` with the six timings, then one `slide_section` per segment.
  - **Counter slides:** `slide_code(title, w.with_clicks(code, 3, result), note)` for both counters, so `counter_slide_problems` re-runs them.
  - **App listings:** `slide_code(..., lang="python")` for the app parts.
  - **Session text:** `slide_code(..., lang="plaintext")` for the session steps.
  - **Demos:** `slide_demo` for each live demo. Each demo is followed by a slide holding its screenshot (`<img src="../assets/img/week15/…" alt="…" style="max-height:62vh;width:auto">`) as the fallback.
  - Every slide has notes. The deck ends on "Next week: how often is it right?"
- [ ] **Step 3: Build and check.** Run both builders, then `print(v.page_problems('week15_lecture'), v.page_problems('week15_slides'))` as in Task 4 Step 2.
Expected: `[] []`.
- [ ] **Step 4: Look at both** (slides over `http.server` with `--virtual-time-budget=6000`). Lint and commit both builders ("Week 15 lecture and slides builders").

### Task 6: Week 15 lab and lab slides

**Files:**
- Create:
  - `reference/ism3232/builders/week15_lab.py`;
  - `reference/ism3232/builders/week15_lab_slides.py`;
  - `reference/ism3232/builders/test_week15_pages.py`.
- Writes: `ism3232/docs/week15_lab.html`, `ism3232/docs/week15_lab_slides.html`

**Interfaces:**
- Consumes:
  - `week15_common`;
  - `week14_lab` (`STYLE` imports and `block`);
  - `week12_lab_slides` (`sec`, `code_slide`, `out_slide`, `idea`, `warn`, `quiz`, `divider`, `SHOWN`).
- Produces: `build() -> (page, derived)`. The warm-up blocks use exactly the `w.LABELS` values as labels. Every expected box holds a `warmup_results()` value.

- [ ] **Step 1: Write the failing page tests** in `test_week15_pages.py`. Its `lab_part(n)` and `slides_page()` helpers are as in `test_week14_pages.py`.

```python
def test_part_4_names_the_three_tests():
    part = lab_part(4)
    assert "test_status_report_counts_orders" in part and "test_restock" in part
    assert "leaves the other rows alone" in part


def test_part_7_shows_keyword_users_how_to_file_a_request():
    part = lab_part(7)
    assert "add_change_request" in part and "refresh" in part.lower()


def test_no_lab_slide_with_a_run_button_uses_streamlit():
    runnable = re.findall(
        r'<div class="run" data-lang="python"[^>]*>(.*?)</div>', slides_page(), re.DOTALL
    )
    assert [code[:40] for code in runnable if re.search(r"\bst\.|streamlit", code)] == []


def test_the_lab_slide_quiz_has_exactly_one_right_answer():
    answer, body = re.search(
        r'<div class="quiz" data-answer="(\w)">(.*?)</div>', slides_page(), re.DOTALL
    ).groups()
    options = re.findall(r'<button data-opt="(\w)">(.*?)</button>', body)
    right = [letter for letter, text in options if "session_state" in html.unescape(text)]
    assert right == [answer]
```

  Run them. Expected: they fail, because the pages do not exist yet.
- [ ] **Step 2: Write `week15_lab.py`** on `week14_lab.py`'s skeleton:
  - `course_map("W15 ")`;
  - prev/next to `week14_lab.html` and `week16_lab.html`;
  - `time_bar`: `Part 1: Start · Part 2: Rerun warm-up (30) · Parts 3–4: database + tests · Part 5: sidebar + Chat · Part 6: Staff tab · Part 7: round trip · Part 8: ritual + push`;
  - a warn callout at the top: Parts 1–6 and every test need no Ollama, and the sidebar's keyword-only mode runs the whole app.

  Parts:
  1. **Start:** `cd ~/ism3232/module07_final_project && source .venv/bin/activate`, `pytest -q` (the Week 14 tests, 12 or more) and `streamlit version` (installed in Week 13).
  2. **Rerun warm-up:**
     1. `cd ~/ism3232/sql_practice`.
     2. Each file is `block(LABELS[key], WARMUP[name])`, followed by its run command. `streamlit run counter.py`: open `http://localhost:8501`, click Add one three times, `expected(results["counter"])`, then Ctrl+C.
     3. `counter_state.py`: `expected(results["counter_state"])`; refresh: `expected(results["fresh"])`.
     4. `echo.py`: type the two `ECHO_MESSAGES`, then `expected(results["echo"])`. A hint: "This is the Chat tab's pattern without the agent."

     A hint covers the first-run email prompt and WSL's browser.
  3. **Database additions**, from a `concept_table`:

     | Bayside | Yours | Spokewell example |
     |---|---|---|
     | `status_report(db_file)` | a `GROUP BY` report over your main table | `repairs_by_status(db_file)` |
     | `restock(db_file, name, stock)` | the one change your edit form makes | `set_part_stock(db_file, name, stock)` |
     | `product_names(db_file)` | the dropdown's choices, if you do not already have such a function | `part_names(db_file)` (already written in Week 14) |

     Show `app_function("status_report")` and `app_function("restock")`.
  4. **Three tests:**
     - `block` of `app_test("test_status_report_counts_orders")` and `app_test("test_restock")` as models;
     - a third test, in prose: "copy your edit test, and assert that another row is still what `schema.sql` says: the edit leaves the other rows alone";
     - run `pytest -q`: 15 or more.
  5. **`app.py`: sidebar and Chat tab.**
     - `block`s of `app_part` `imports`, `top`, `sidebar`, `bot`, `tabs` and `chat`.
     - A `concept_table` mapping Bayside → yours → Spokewell:

       | Bayside | Yours | Spokewell example |
       |---|---|---|
       | `st.title("Bayside Outfitters")` | your business name | Spokewell Bike Repair |
       | `BaysideTools(DB_FILE)` | your tools class | `SpokewellTools(DB_FILE)` |
       | `"Sunny"` | your assistant's name | `"Spoke"` |
       | the caption's "address change" | your change | "pickup change" |
       | `all_orders` | your list function | `all_repairs` |
       | `request['order_id']`, `request['new_address']` | your request columns | `request['ticket_id']`, `request['new_value']` |
       | `status_report` / `restock` / `product_names` | Part 3 | `repairs_by_status` / `set_part_stock` / `part_names` |

     - Run it and try a lookup on keyword rules.
  6. **The Staff tab:** `block`s of `app_part` `notice`, `waiting`, `tables` and `restock`, adapted with the table above.
  7. **One round trip:**
     - With Ollama: file a change in the chat, approve it on Staff, then ask about it in the chat.
     - Keyword-only: in `python3`, `from database import add_change_request`, then `add_change_request("<yours>.db", "<an ID>", "<new value>")` (a typed block in `derived`). Then rerun the page (press R, or click any widget), approve, and watch the records table change.
     - Everyone refreshes once: the chat clears, and the decision stays.
  8. **Ritual and push** with Ollama off: `block("Terminal", "ruff format . && ruff check . && pytest -v\ngit add . && git commit -m 'lab 15: streamlit app' && git push")`.

  **Submission box:**
  - `app.py`, the new database functions, and 15+ tests in the three files;
  - no test imports `app.py` or `ollama_model.py`;
  - the URL in Canvas, completion credit;
  - `NO_SCREENSHOTS` (graded by cloning).
- [ ] **Step 3: Write `week15_lab_slides.py`** on `week14_lab_slides.py`'s skeleton:
  - every Streamlit block uses `code_slide(..., readonly=True, lang="shell")`;
  - the warm-up results appear as `out_slide`s of `warmup_results()` values;
  - the three screenshots stand in for demos;
  - add one idea slide ("Streamlit remembers nothing; session_state does") and one quiz, "Which line keeps the chatbot between reruns?". Options: `bot = SupportChatbot("Sunny", INSTRUCTIONS, tools, KeywordModel())`, `if "bot" not in st.session_state:` (the answer), `bot.model = make_model(choice)`, `st.rerun()`. Only the answer may mention `session_state`;
  - `derived` includes `SHOWN` and every typed block.
- [ ] **Step 4: Build and check, including the warm-up rebuilt from the page.** Run both builders, `test_week15_pages.py` (expected: `4 passed`), then `print(v.page_problems('week15_lab'), v.page_problems('week15_lab_slides'))` as in Task 4 Step 2. `page_problems` includes the warm-up rebuild for the lab. Expected: `[] []`.
- [ ] **Step 5: Look at both** in light, dark and phone widths. Lint and commit the three files ("Week 15 lab and lab slides builders").

### Task 7: The unpublished Spokewell build

**Files (none committed):**
- Modify: `reference/ism3232/_private/spokewell/database.py`, `tests/test_database.py`
- Create: `reference/ism3232/_private/spokewell/app.py`, `reference/ism3232/_private/spokewell_dev_tests/test_app.py`

**Interfaces:**
- Consumes: the built `week15_lab.html` (Parts 3–7, read as a student would) and the existing Week 14 Spokewell build (14 tests, `smoke.py`).
- Produces: a project that `verify_week15.spokewell_problems()` passes.

- [ ] **Step 1: Confirm the folder is ignored and starts green.** `git check-ignore reference/ism3232/_private/spokewell_dev_tests/x.py` prints the path. `"$PY" -B reference/ism3232/tools/check.py reference/ism3232/_private/spokewell` passes with 14 tests.
- [ ] **Step 2: Follow Parts 3–4 as written.**
  - Add `repairs_by_status(db_file)` (`SELECT status, COUNT(*) AS repairs FROM repairs GROUP BY status ORDER BY status`) and `set_part_stock(db_file, name, stock)`.
  - Add `test_repairs_by_status_counts_repairs`. Expected: `[{"status": "in repair", "repairs": 2}, {"status": "ready", "repairs": 2}, {"status": "waiting for parts", "repairs": 1}]`.
  - Add `test_set_part_stock` (`saddle` to 4) and `test_set_part_stock_leaves_other_parts_alone` (`chain` still 6).
  - Wherever the page is unclear, wrong or missing a step, stop. Fix the lab builder (Task 6), rebuild, re-run Task 6 Step 4, and ledger the gap. Do not work around it from outside knowledge.
- [ ] **Step 3: Follow Parts 5–6 as written** to make `app.py`: `SpokewellTools`, `"Spoke"`, `all_repairs`, `repairs_by_status`, `part_names`, `set_part_stock`, waiting rows with `ticket_id` and `new_value`, and a caption naming the pickup change.
- [ ] **Step 4: Write `_private/spokewell_dev_tests/test_app.py`** on `bayside_dev_tests/test_app.py`'s shape. `start_app` copies `spokewell/*.py` and `schema.sql`, and each test uses keyword-only mode. Tests:
  - `test_chat_history_survives_reruns`: two lookups give 4 chat messages.
  - `test_one_approve_click_changes_the_repair_once`: filed with `add_change_request`; after the click `pickup_date` changes, the notice is `Request 1 approved.`, and nothing is waiting.
  - `test_reject_click_leaves_the_repair_alone`.
  - `test_edit_form_saves`: `saddle` to 4.
  - `test_a_typed_value_is_plain_text_on_the_staff_tab`, with the value `[click me](https://example.com) $5 and $6`.
  - `test_keyword_round_trip`: a request filed from Python, approved by click; the records `dataframe`'s `R200` row shows the new date.
- [ ] **Step 5: Check it.**
Run: `"$PY" -B reference/ism3232/tools/check.py reference/ism3232/_private/spokewell && (cd reference/ism3232/_private/spokewell && "$PY" -B smoke.py) && "$PY" -B -m pytest -q -p no:cacheprovider reference/ism3232/_private/spokewell_dev_tests`
Expected:
- `check.py` passes with 17 tests;
- `smoke ok`;
- `6 passed`.

Confirm `git status --short reference/ism3232/_private` prints nothing. Ledger the results. Any lab fixes are committed as Task 6 follow-ups.

### Task 8: Week 14's next link and the site wiring

**Files:**
- Modify: `reference/ism3232/builders/week14_common.py` (`NEXT`)
- Create: `reference/ism3232/builders/wire_week15.py`
- Rewrites through builders: `ism3232/docs/week14_{reading,lecture,lab,slides,lab_slides}.html`
- Edits through the wiring script:
  - `ism3232/site.js`, `ism3232/index.html`;
  - `ism3232/docs/week16_{reading,lecture,lab}.html`;
  - `ism3232/docs/{course_guide,syllabus,slos,slo_mindmap,unit_4_overview,unit_4_cheatsheet}.html`;
  - `_build_qti.py`.

**Interfaces:**
- Consumes: the Week 14 builders and `verify_week14`.
- Produces: a site where every Week 15 link, menu and row names the new title.

- [ ] **Step 1: Baseline.** `verify_week14.py` prints `verify_week14: OK`.
- [ ] **Step 2: Week 14's next link.**
  - Set `NEXT = ("week15", "Week 15", "Streamlit Chat &amp; Staff — Reruns, Session State &amp; Approvals")` in `week14_common.py`, then run the five Week 14 builders.
  - Run `git -C ism3232 diff -U0 -- 'docs/week14_*.html' | grep '^[-+][^-+]'`. Expected: only next-link lines, with `Streamlit Interface` changed to the new title.
  - Confirm with a small Python check that swapping that one string is the whole difference. `verify_week14.py` still prints OK.
- [ ] **Step 3: Write `wire_week15.py`** with `wire_week14.py`'s structure: counts first, `--write` to apply, nothing written unless every count is right. Set `NEW_TITLE = "Streamlit Chat &amp; Staff — Reruns, Session State &amp; Approvals"` and `SHORT = "Streamlit Chat &amp; Staff"`. The replacements, each old string copied from the live files on 2026-10-29:

```python
REPLACEMENTS = [
    (["site.js"], "Module 15 · Streamlit Interface", "Module 15 · " + NEW_TITLE, 2),
    (
        ["index.html"],
        '<div class="wc-title">Streamlit Business Interface</div>',
        f'<div class="wc-title">{NEW_TITLE}</div>',
        1,
    ),
    (
        ["index.html"],
        "Streamlit widgets, layout, and session state. Connect your app to SQLite. Build an "
        "interactive business dashboard that runs in a browser.",
        "A web page for the agent: a Chat tab for customers and a Staff tab that approves the "
        "change requests it files. Streamlit reruns, st.session_state, tabs and forms.",
        1,
    ),
    (
        [f"docs/week16_{kind}.html" for kind in ("reading", "lecture", "lab")],
        ">Week 15</span>Streamlit Interface</span>",
        f">Week 15</span>{NEW_TITLE}</span>",
        3,
    ),
    (
        ["docs/course_guide.html"],
        '<span class="mod-title">Streamlit Business Interface</span>',
        f'<span class="mod-title">{NEW_TITLE}</span>',
        1,
    ),
    (
        ["docs/course_guide.html"],
        "Streamlit widgets, layout, session state. Connect to SQLite. Build an interactive "
        "business dashboard in a browser.",
        "Bayside's app.py: Streamlit's rerun model, st.session_state, a Chat tab over the agent, "
        "and a Staff tab that approves or rejects change requests, shows a GROUP BY report, and "
        "edits the database.",
        1,
    ),
    (
        ["docs/course_guide.html"],
        '<span class="mt">Streamlit Business Interface</span><span class="ms">Morning — '
        "widgets, layout, session state, connect to SQLite</span>",
        f'<span class="mt">{NEW_TITLE}</span><span class="ms">Morning — reruns, '
        "session_state, Chat tab, Staff approvals</span>",
        1,
    ),
    (
        ["docs/course_guide.html"],
        '<span class="mt">Streamlit Business Interface</span><span class="ms">Full week — '
        "widgets, layout, session state, connect SQLite to Streamlit</span>",
        f'<span class="mt">{NEW_TITLE}</span><span class="ms">Full week — reruns and '
        "session_state, a Chat tab over the agent, a Staff tab with approvals and a "
        "report</span>",
        1,
    ),
    (
        ["docs/course_guide.html"],
        '<span class="mt">Streamlit Business Interface</span><span class="ms">Widgets, layout, '
        "session state; connect SQLite to Streamlit</span>",
        f'<span class="mt">{NEW_TITLE}</span><span class="ms">Reruns and session_state; Chat '
        "and Staff tabs; approvals, report, edit form</span>",
        1,
    ),
    (
        ["docs/course_guide.html"],
        "<p>Weeks 12 to 14 have been rebuilt as well (see below). Week 13 starts the agent "
        "capstone with a proposal, a starter business, and the new capstone rubric; Week 14 "
        "turns its database into the agent's tools; Weeks 15 and 16 are being rebuilt in the "
        "same direction, toward a chat page and a staff dashboard.",
        "<p>Weeks 12 to 15 have been rebuilt as well (see below). Week 13 starts the agent "
        "capstone with a proposal, a starter business, and the new capstone rubric; Week 14 "
        "turns its database into the agent's tools; Week 15 puts a Chat tab and a Staff tab in "
        "front of them; Week 16 is being rebuilt in the same direction.",
        1,
    ),
    (
        ["docs/syllabus.html"],
        '<td style="font-weight:600;">Streamlit Interface</td>\n'
        '      <td style="font-size:12px;color:var(--muted);">Rerun model · 5 tabs · '
        "Submit/View/Filter/Update/Report</td>\n"
        '      <td style="font-size:12px;font-family:var(--mono);color:var(--muted);">Capstone: '
        "app.py</td>",
        f'<td style="font-weight:600;">{SHORT}</td>\n'
        '      <td style="font-size:12px;color:var(--muted);">Rerun model · session_state · '
        "chat_message · tabs · approve/reject</td>\n"
        '      <td style="font-size:12px;font-family:var(--mono);color:var(--muted);">Lab 15: '
        "app.py + 15 tests</td>",
        1,
    ),
    (
        ["docs/slos.html"],
        'vertical-align:top;">Streamlit Interface</td>',
        f'vertical-align:top;">{SHORT}</td>',
        1,
    ),
    (
        ["docs/slos.html"],
        "Explain Streamlit&#x27;s rerun execution model; implement all five required tabs "
        "(Submit, View All, Filter, Update Status, Report) wired to the live database; call "
        "create_table() before any widget.",
        "Explain Streamlit&#x27;s rerun model and keep objects in st.session_state; build a Chat "
        "tab over the agent and a Staff tab that approves or rejects change requests, shows "
        "records and a GROUP BY report, and edits the database; show customer text safely.",
        1,
    ),
    (
        ["docs/slo_mindmap.html"],
        "tooltip_title:'Week 15 — Streamlit Interface',",
        "tooltip_title:'Week 15 — Streamlit Chat & Staff',",
        1,
    ),
    (
        ["docs/slo_mindmap.html"],
        "tooltip_body:'Explain Streamlit\\'s rerun model; implement all five required tabs "
        "wired to the live database.'}",
        "tooltip_body:'Explain the rerun model; keep the agent in session_state; build Chat and "
        "Staff tabs that approve change requests.'}",
        1,
    ),
    (
        ["docs/unit_4_overview.html", "docs/unit_4_cheatsheet.html"],
        'Weeks 13 and 14 are new: <a href="week13_reading.html">Agent Design &amp; SQL</a> and '
        '<a href="week14_reading.html">Database Tools</a>, with the',
        'Weeks 13 to 15 are new: <a href="week13_reading.html">Agent Design &amp; SQL</a>, '
        '<a href="week14_reading.html">Database Tools</a> and '
        f'<a href="week15_reading.html">{SHORT}</a>, with the',
        2,
    ),
    (
        ["docs/unit_4_overview.html", "docs/unit_4_cheatsheet.html"],
        "The rest of this page, and Weeks 15 and 16, still describe",
        "The rest of this page, and Week 16, still describe",
        2,
    ),
    (
        ["../_build_qti.py"],
        '    15: "Streamlit Business Interface",',
        '    15: "Streamlit Chat & Staff — Reruns, Session State & Approvals",',
        1,
    ),
]
```

  Names resolve against `ism3232/`. There is no strip group, because the label `W15 Streamlit` stays.
- [ ] **Step 4: Check, then apply.** Run `wire_week15.py`. Expected: every line `ok`; fix any mismatched old string against the file, never the count. Then run it with `--write`. Expected: `Wrote 12 files.`: site.js, index.html, the three Week 16 pages, course_guide, syllabus, slos, slo_mindmap, unit_4_overview, unit_4_cheatsheet and `_build_qti.py`.
- [ ] **Step 5: Leftovers.**
Run: `grep -ln 'Streamlit Interface\|Streamlit Business Interface' ism3232/site.js ism3232/index.html ism3232/docs/week14_*.html ism3232/docs/week16_{reading,lecture,lab}.html ism3232/docs/{course_guide,syllabus,slos,slo_mindmap}.html _build_qti.py`
Expected: only `course_guide.html`, for its compressed-schedule label `Week 8 — Streamlit Interface (W15)`, which names the topic, not the module. Read that hit and ledger it. Ledger Week 16's own mentions of a "five-tab Streamlit app" for Phase 4c.
- [ ] **Step 6: Lint and commit** `week14_common.py` and `wire_week15.py` ("Week 15 wiring: Week 14 next link, counted site replacements").

### Task 9: Final checks and show the user

- [ ] **Step 1: All tests.** Tools (12) and builders, including all Week 15 tests, must pass with `SQLITE3_CLI` set.
- [ ] **Step 2: All verifiers.** `verify_week12.py`, `verify_week13.py`, `verify_week14.py` and `verify_week15.py` each print OK or exit 0. `verify_week15` includes the Bayside app checks and Spokewell.
- [ ] **Step 3: Screenshots and console.** Cover the five Week 15 pages, `index.html`, one Week 14 page and one Week 16 page, in light, dark and 390 px widths; the decks need `--virtual-time-budget=6000`. Run the console-error check on every changed page and read every image. Check that the screenshots read well on a phone page. Stop the server by its PID.
- [ ] **Step 4: Quiz build.** Run `python3 _build_qti.py`. Expected: ISM3232 Week 15 has 10 questions under the new title.
- [ ] **Step 5: Final review.**
  - A fresh reviewer on the strongest model checks the whole branch. Give it the spec, this plan, the Review Focus verbatim, and the ledger's rulings, for the range from the commit that added this plan to `HEAD`.
  - It also reads the built pages and images in the `ism3232` working tree, and is told `_private/` must never be committed.
  - Then one fix pass, test first.
- [ ] **Step 6: Show the user** the pages (local URLs), `session.txt` and the three screenshots, the verifier output, the Spokewell result, and the review findings with what was fixed. Wait for their decision.

### Task 10: Ship on the user's word

- [ ] **Step 1: Only after "commit and push":** in `ism3232`, check `git status --short`, then stage only this work's files:
  - `docs/week15_{reading,lecture,slides,lab,lab_slides}.html` and `assets/img/week15/*.png`;
  - `docs/week14_{reading,lecture,lab,slides,lab_slides}.html` (only those that changed);
  - `docs/week16_{reading,lecture,lab}.html`, `site.js`, `index.html`;
  - `docs/{course_guide,syllabus,slos,slo_mindmap,unit_4_overview,unit_4_cheatsheet}.html`.

  Commit `Week 15 rebuilt: Streamlit Chat & Staff`, then push `main`.
- [ ] **Step 2:** In the parent:
  - stage the `ism3232` pointer and `_build_qti.py`, only the Week 15 line if the file has other edits;
  - commit `Bump ism3232 submodule pointer: Week 15 rebuilt as Streamlit Chat & Staff`, and push `main`;
  - confirm `git status` shows nothing under `reference/ism3232/_private`.
- [ ] **Step 3:** Confirm the live pages with a background until-loop: `https://markumreed.github.io/ism3232/docs/week15_reading.html` (new title and the three images), the lab, the home page's Module 15 card, and a Week 16 previous link.
- [ ] **Step 4:** Remind the user to re-import the Week 15 quiz zip and record the Week 15 lecture video.
