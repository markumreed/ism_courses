# ISM3232 Phase 4b: Week 15, Streamlit Chat & Staff

- **Date:** 2026-10-20
- **Status:** Design approved section by section in chat; this written spec awaits review
- **Parent spec:** `docs/superpowers/specs/2026-10-16-ism3232-agents-throughline-design.md` (Week 15 section; section 8 items for Week 15)
- **Bayside spec:** `docs/superpowers/specs/2026-10-16-ism3232-bayside-app-design.md`, section 5 (the Streamlit app)
- **Builds on:** the Bayside reference app, `reference/ism3232/bayside_app/`, Week 15 checkpoint `8b1b491`; Week 14 as shipped (ism3232 `8f1ee95`, parent `6bf65ca`)

## 1. Purpose

Week 15 puts a web page in front of the agent and the database. Bayside's `app.py` has a Chat tab for customers and a Staff tab where staff approve or reject the change requests the agent filed. The pages teach it around one idea: Streamlit runs the whole script again on every click, so `st.session_state` is the only thing that survives, just as Week 11's model remembers nothing and is sent the history every time. The lab starts with a short rerun warm-up, then students build the same two tabs for their own business in `module07_final_project`.

Success means:

- Every listing on a Week 15 page appears exactly in a file at `8b1b491`, the saved session, or output the builders generate by running that code.
- Every model output and every screenshot comes from one real session of the checkpoint app, driven in headless Chrome with `granite4.1:3b` on the CPU.
- The lab's warm-up, rebuilt from the lab page alone and driven through Streamlit's test tool, gives every result the page promises.
- A student who follows Parts 3–8 ends with a working `app.py` (Chat tab, Staff tab, model switch) on their own database, and at least 15 tests in three files that need no Ollama or Streamlit. An unpublished build of one starter proves this.
- Week 15 is live by Monday 2026-11-30; Lab 15 is due Sunday 2026-12-06.

## 2. Decisions

| Question | Choice (user, 2026-10-20) |
|---|---|
| Lab shape | A short rerun warm-up (about 30 minutes, three tiny apps in the practice folder), then the student's own `app.py` built from Bayside's with a mapping table |
| The three tests between Week 14's 12 and the rubric's 15 | Added in Week 15: `tmp_path` tests for the new database functions the Staff tab needs. Students write no app tests |
| Pictures of the app | Real screenshots of Bayside, taken by a script from the checkpoint and re-takeable whenever the app changes |
| How screenshots and quoted runs are captured | One real browser session yields both the screenshots and the text the pages quote, so a picture and its caption cannot disagree |

Carried over from Bayside's build (parent spec section 8, settled in Phase 2):

- **The model switch:** a sidebar radio, "Course model, keyword rules if it is down" (`FallbackModel(OllamaModel(MODEL_NAME), KeywordModel())`, the default) or "Keyword rules only (no AI)" (`KeywordModel()`), with a caption saying the keyword rules cannot file an address change.
- **Telling a customer about a staff decision:** the customer asks the agent, which uses `check_request`; the chat never announces a decision on its own.

Carried over from Week 14:

- Pages quote the checkpoint as it is; model output comes only from runs of the checkpoint code. The saved Phase 2 app runs (`runs/bayside_app/app_session*.txt`) predate the final-review fixes and are not quoted.
- An unpublished Spokewell build in git-ignored `reference/ism3232/_private/` proves the lab.
- Students without Ollama file a change request from `python3` with their `add_change_request` to try the staff review, because the keyword model cannot file one.

## 3. What Week 15 teaches

**Title:** Streamlit Chat & Staff — Reruns, Session State & Approvals. The week-strip label stays `W15 Streamlit`. Eyebrow: Unit 4 · Capstone Build.

**The one idea.** Streamlit runs the whole script again on every click and keeps nothing between runs except `st.session_state`. Week 11 said the model remembers nothing, so the history is sent every time; Streamlit remembers nothing either. That is why Bayside creates its chatbot once and keeps it in `st.session_state.bot`. The warm-up makes students see it: a counter that stays at 1 however often they click.

**From Bayside, all quoted from `8b1b491`:**

- `make_model(choice)` and the sidebar radio with its caption.
- `show(text)`, which escapes `$` so Streamlit does not read it as math.
- `create_tables(DB_FILE)` on every run.
- The chatbot created once (`if "bot" not in st.session_state`), with `bot.model = make_model(choice)` on every run, so switching models keeps the conversation.
- `st.tabs(["Chat", "Staff"])`.
- **Chat tab:** the history drawn with `st.chat_message`, tool entries hidden; `st.chat_input`; `bot.respond()` inside `st.spinner`; `st.rerun()`.
- **Staff tab:**
  - the notice kept in `st.session_state` so a result message survives the rerun;
  - one row per waiting request in `st.columns`, shown with `st.text`, with Approve and Reject buttons keyed by request number;
  - `st.dataframe(all_orders(DB_FILE))` and `st.dataframe(status_report(DB_FILE))`;
  - the restock `st.form` with `st.selectbox`, `st.number_input` and a submit button.
- From `database.py`: `status_report` (GROUP BY, tied back to Week 13's SQL), `restock` and `product_names`.

**New Python, each explained in one line:**

- unpacking `chat_tab, staff_tab = st.tabs(...)` and the three names from `st.columns(...)`;
- `with` for page layout (students know `with open` from Week 6);
- `in`, setting an attribute and `del` on `st.session_state`;
- keyword arguments such as `key=` and `min_value=`;
- the backslash in `"\\$"`.

**Safety link.** Customer text is data. Staff rows use `st.text` and the chat escapes `$`, so a customer cannot format the staff page or plant a link in it. The pages also name the open limit: anyone who opens the app can approve, because there is no sign-in.

**Practical traps the pages cover:**

- the first `streamlit run` stops at "Welcome to Streamlit! … Email:"; press Enter to skip it (confirmed on Streamlit 1.66 with a fresh home folder);
- Ctrl+C stops the server;
- in WSL, open `http://localhost:8501` in the Windows browser;
- a browser refresh starts a new session: the chat clears, the database keeps everything.

**What this module leaves out, and why:** staff sign-in, streaming replies, deploying online, caching, and the old FastAPI material.

**Leads into Week 16:** the app runs; how often is it right?

## 4. The Week 15 pages

The five pages replace the old Week 15 pages in place: `week15_reading.html`, `week15_lecture.html`, `week15_slides.html`, `week15_lab.html` and `week15_lab_slides.html`. The old five-tab app and its video embed go; there is no video block until a new video exists.

### Reading (about 60 minutes)

1. Objective, then **Coming from Week 14**: "Staff still can't approve anything without running Python."
2. **At a glance**, then eight outcomes:
   1. run and stop a Streamlit app;
   2. explain the rerun model;
   3. keep objects between reruns with `st.session_state`;
   4. build a chat with `st.chat_message` and `st.chat_input`;
   5. lay out a page with a sidebar, tabs and columns;
   6. show records and a GROUP BY report with `st.dataframe`;
   7. use buttons and a form that change the database, then rerun;
   8. show customer text safely.
3. **What you build this week:** the Chat tab screenshot, as the hook.
4. **Streamlit runs everything again.** The counter from the warm-up, without and then with `st.session_state`, with the real results; then the Week 11 callback.
5. **The chat.** The top of `app.py` (imports, `make_model`, `show`), the chatbot kept in `session_state`, the Chat tab code, and the captured conversation quoted beside its screenshot.
6. **The Staff tab.**
   - The waiting rows and the notice that survives the rerun.
   - The orders table and `status_report`.
   - The restock form, and why `st.form` waits for its button before rerunning.
   - The Staff screenshot with a request waiting.
7. **One round trip**, from the captured session:
   1. a change filed in the chat;
   2. approved on the Staff tab (the screenshot of the notice and the updated table);
   3. "What happened to request 1?" answered in the chat.
8. **Customer text is data**: `st.text`, the `$` escape, and the "anyone can approve" limit.
9. **Running it**: `streamlit run app.py`, the email prompt, `localhost:8501` (and from WSL), Ctrl+C, refresh versus database, and what keyword-only mode can and cannot do.
10. **Why `app.py` has no tests**: the autograder runs without Streamlit, so the logic lives in the tested files and `app.py` stays thin. This motivates the week's three new database tests.
11. **What this module leaves out, and why** (section 3).
12. **Key terms**, **Before you leave**, and a 10-item quiz in the existing `.quiz-item` markup.
13. **Closing**: "The app runs. Next week: how often is it right?"

### Lecture (75 minutes)

| Minutes | Segment | What happens |
|---|---|---|
| 0–8 | Where Week 14 left off | `main.py`'s staff review in a terminal: who would use that? |
| 8–25 | Reruns, live | The counter stuck at 1; `session_state`; the Week 11 callback |
| 25–45 | The chat, live | Bayside's Chat tab on the course model; switching models keeps the chat |
| 45–60 | The Staff tab, live | Approve the request filed in the chat; the notice; the report; restock |
| 60–68 | Customer text is data | Type Markdown and a `$` into an address; why `st.text` matters |
| 68–75 | Your project | The Bayside→yours map, the three new database functions and tests, next week |

Then three discussion questions, and four misconceptions to listen for:

- "Streamlit keeps my variables between clicks";
- "the chat history is in the database" (it is in `session_state`; a refresh clears it);
- "I should test `app.py`" (the autograder cannot; keep `app.py` thin);
- "Reject deletes the request" (it marks it rejected).

### Slides

The slides follow the lecture's segments, as in Week 14.

- Code slides quote the checkpoint.
- The counter slides show results the builders produce by driving the counter through Streamlit's test tool; the verifier re-runs them.
- The three screenshots sit where the live demos go, as a fallback if a demo fails.
- Model wording appears only from the captured session.

### Lab (about 3 hours, finished at home if needed)

A box at the top for laptops that cannot run the model: Parts 1–6 and every test need no Ollama, and the sidebar's keyword-only mode runs the whole app.

| Time | Part | What students do |
|---|---|---|
| 0:00–0:05 | 1. Start | Open `module07_final_project`, activate the venv; `pytest -q` passes the Week 14 tests (12 or more); `streamlit version` works (installed in Week 13) |
| 0:05–0:35 | 2. Rerun warm-up | Three tiny apps in `~/ism3232/sql_practice`, each with its expected result |
| 0:35–1:00 | 3–4. Database additions and three tests | New functions from a mapping table, then three `tmp_path` tests: 15 or more in total |
| 1:00–1:40 | 5. `app.py`: sidebar and Chat tab | Adapt Bayside's top block, the session-state chatbot and the Chat tab; try a lookup on keyword rules |
| 1:40–2:20 | 6. The Staff tab | Plain-text waiting rows with Approve and Reject, the notice, the records table, the report, the edit form |
| 2:20–2:40 | 7. One round trip | Described below |
| 2:40–3:00 | 8. Ritual and push | With Ollama off; commit `lab 15: streamlit app` |

**Part 2, the warm-up apps** (written for the page; the builders hold their text):

1. `counter.py`: a button that adds one to a plain variable; after three clicks it still shows `Count: 1`.
2. The same app with `st.session_state`: after three clicks it shows `Count: 3`; a browser refresh resets it.
3. `echo.py`: a chat box that keeps its history in `st.session_state` and replies `You said: …`; two messages leave four chat bubbles. This is the Chat tab's pattern without the agent.

**Part 3, the database additions**, from a table:

| Bayside | Yours | Spokewell example |
|---|---|---|
| `status_report(db_file)` | a `GROUP BY` report over your main table | `repairs_by_status(db_file)` |
| `restock(db_file, name, stock)` | the one change your edit form makes | `set_part_stock(db_file, name, stock)` |
| `product_names(db_file)` | the dropdown's choices, if you do not already have such a function | `part_names(db_file)` (already written in Week 14) |

**Part 4, three tests:** the report counts correctly; the edit changes the chosen row; the edit leaves the other rows alone.

**Part 7, the round trip:**

- With Ollama: file a change in the chat, approve it on the Staff tab, then ask about it in the chat.
- Keyword-only: file the request from `python3` with `add_change_request`, as in Week 14, then approve it on the Staff tab and watch the records table change.
- Everyone refreshes the browser once: the chat clears; the decision stays in the database.

**Submission:** GitHub URL in Canvas, completion credit. The repo has `app.py`, the new database functions, and at least 15 tests in `tests/test_database.py`, `tests/test_tools.py` and `tests/test_agent.py`. No test imports `app.py` or `ollama_model.py`.

### Lab slides

The lab slides follow the parts. The warm-up results are real runs of the lab page's own blocks, and the screenshots stand in for a live demo.

## 5. Real runs, checks, wiring and shipping

**The captured session, from `8b1b491`:**

- `reference/ism3232/runs/week15/capture.sh` runs a driver script that copies the checkpoint to a temporary folder and starts `streamlit run app.py` headless on a free port.
- The driver controls headless Chrome through its remote-debugging protocol (`--remote-debugging-port`, driven with the `websockets` package; confirmed working with this machine's Chrome 155) at a fixed window size, with the course model on the CPU (`CUDA_VISIBLE_DEVICES=-1 ollama serve`).
- The session:
  1. asks "Has A101 shipped yet?";
  2. asks to change the address on order A102;
  3. screenshot of the Chat tab;
  4. opens the Staff tab; screenshot of the waiting request;
  5. clicks Approve; screenshot of the notice and the updated orders table;
  6. returns to Chat and asks "What happened to request 1?".
- Screenshots are saved as PNG files under `ism3232/assets/img/week15/`; the visible chat and staff text from the same session goes to `reference/ism3232/runs/week15/session.txt`.
- The text is read before any page quotes it, and the pages quote whatever wording the model produced. A test pins what the pages claim: the waiting request names A102 and the new address, the notice says the request was approved, and the last answer reports the approval.
- Each image has alt text that describes what it shows.

**Other real output:** the warm-up results and the counter slides come from driving the exact files the pages show through Streamlit's test tool (`streamlit.testing.v1.AppTest`); the builders return them as derived text.

**Builders and verifier.** `reference/ism3232/builders/` gets `week15_common.py`, `week15_reading.py`, `week15_lecture.py`, `week15_slides.py`, `week15_lab.py`, `week15_lab_slides.py` and `verify_week15.py`. They reuse `pagekit` and the Week 12 lab-slide helpers. `verify_week15.py` proves:

- each page on disk equals its builder's output;
- every listing appears exactly in `8b1b491`'s files, the saved session, or derived output;
- every counter slide shows what its run produced;
- the warm-up, rebuilt from the lab page into an empty folder and driven through the test tool, gives every promised result;
- the quiz imports cleanly with `_build_qti.py`;
- every screenshot a page references exists;
- Bayside's app checks (`reference/ism3232/bayside_dev_tests/test_app.py`) pass.

**The unpublished Spokewell build:**

- It lives in `reference/ism3232/_private/spokewell/` (git-ignored; the parent repository is public).
- `app.py` and the Part 3 functions are added by following Parts 3–7 as written.
- It must pass `tools/check.py`: ruff, and at least 15 tests with `ollama` and `streamlit` blocked.
- An app check, run through the test tool on the keyword model, must show: the history survives reruns; Approve changes the record once and Reject changes nothing; the edit form saves; a customer-typed value stays plain text on the Staff tab; and the Part 7 keyword round trip (a request filed with `add_change_request`, approved on the Staff tab, the records table changed).
- `verify_week15.py` runs these checks when the folder exists.

**Wiring:**

- **Week strip:** unchanged (`W15 Streamlit`).
- **The title** goes in:
  - both `site.js` menus;
  - the home page's Module 15 card (title and a new description);
  - the Week 16 pages' previous links;
  - `_build_qti.py` (`15:`);
  - the Week 15 rows in `course_guide.html`, `syllabus.html`, `slos.html` and `slo_mindmap.html`;
  - Week 14's next links, by setting `week14_common.NEXT` and rebuilding; `verify_week14` must pass and the diff must show only the link.
- **Unit 4 banners:** the banners on `unit_4_overview.html` and `unit_4_cheatsheet.html` say Weeks 13 to 15 are new.

**Before showing the user:**

- all tests and the Week 12, 13, 14 and 15 verifiers pass;
- screenshots at light, dark and phone widths, plus a console-error check on every changed page;
- the quiz builds with 10 questions;
- a fresh whole-branch review on the strongest model, then one test-first fix pass.

**Shipping, on the user's word:**

1. Commit only this work's `ism3232` files, including the new images, and push.
2. Bump the parent pointer with `_build_qti.py`, staging only Week 15's line if another session has edits in that file, then push.
3. Confirm the live pages.

## 6. Not in this phase

- Week 16.
- The Phase 5 sweep, including the Phase 4a deferred minors.
- Any change to the Bayside app. If the build finds a bug in it, stop and ask.
