# Autograder GUI — Design

## Problem

The autograder's `fetch`/`check`/`upload` CLI workflow (see
`docs/superpowers/specs/2026-07-27-autograder-design.md`) requires opening
`runs/<assignment>/review.csv` in a spreadsheet app to fill in human-scored
rubric fields between `check` and `upload`. That's the actual friction point
in day-to-day use — everything else about the CLI already works. We want a
local GUI that replaces the spreadsheet-editing step with an in-browser
grading review screen, while reusing 100% of the existing, already-tested
grading logic in `autograder_common`.

## Scope

**In scope:**
- A single Streamlit app (`autograder/gui.py`) covering both courses via a
  course selector, targeting the same 5 pilot assignment configs already
  shipped (ISM2411: `week03_lab`, `capstone`; ISM3232: `week07_assignment`,
  `developer_workflow`, `capstone`).
- Fetch and Check actions, a grading table for entering human-scored rubric
  fields with a live-computed total score, and an Upload panel with the same
  safety rails as the CLI (dry-run preview, blocked on incomplete fields,
  explicit confirmation before posting).
- One new small module, `autograder_common/gui_helpers.py`, holding the
  logic the page needs that doesn't already exist in `autograder_common` —
  covered by normal pytest unit tests.

**Out of scope:**
- No new assignment configs beyond the existing 5 pilots.
- No changes to `canvas.py`, `fetch.py`, `checks.py`, `worksheet.py`,
  `scoring.py`, or `cli.py` — the GUI is additive, calling their existing
  public functions as-is.
- No authentication/multi-user support — this is a local, single-instructor
  tool, same trust model as the CLI (Canvas token via `CANVAS_API_TOKEN` env
  var, same as today).

## Architecture

`gui.py` is a thin Streamlit presentation layer. It imports and calls the
same functions the CLI's `cmd_fetch`/`cmd_check`/`cmd_upload` already call:
`fetch.fetch_submission`, `checks.*` (via a small `gui_helpers` wrapper
around the same signal-computation logic `cli._compute_signals` already
implements), `worksheet.build_worksheet`/`read_worksheet`/
`incomplete_students`, `scoring.compute_score`, and `CanvasClient`. No
grading logic is reimplemented for the GUI — `gui_helpers.py` only adds
small, pure functions for shaping data for display and live-scoring a
partially-edited row, each independently unit-testable without Streamlit.

```
autograder/
  gui.py                          # Streamlit page: layout, widgets, session_state wiring
  autograder_common/
    gui_helpers.py                 # pure helper functions the page calls (new)
    cli.py                         # unchanged — cmd_fetch/cmd_check/cmd_upload's
                                    #   logic is what gui.py's actions mirror
    canvas.py, fetch.py, checks.py,
    worksheet.py, scoring.py       # unchanged
  requirements.txt                 # + streamlit>=1.35
  tests/
    test_gui_helpers.py            # new
```

## Screens & navigation

Single page, no multi-page routing — Streamlit's rerun-on-interaction model
plus `st.session_state` is enough for this app's one linear workflow.

1. **Header controls** — course selectbox (ISM2411 / ISM3232), assignment
   selectbox populated from that course's `assignments/<course>/*.yaml`
   files (via `config.load_assignment_config` on each file found by
   globbing the directory). Always visible at the top.

2. **Action bar** — "Fetch Submissions" and "Run Checks" buttons.
   - Fetch: lists Canvas submissions via `CanvasClient.list_submissions`
     (after resolving the assignment id exactly as `cli._assignment_id`
     does), calls `fetch.fetch_submission` per student into
     `runs/<assignment>/<student_key>/`, and renders a per-student
     success/failure log line (mirroring `cmd_fetch`'s stdout, as
     `st.write` lines instead of prints) so one student's `FetchError`
     doesn't hide the rest.
   - Check: computes mechanical signals per student directory (via
     `gui_helpers.compute_student_records`, a `gui_helpers.py` function
     that wraps the same signal-computation approach `cli._compute_signals`
     uses) and writes `runs/<assignment>/review.csv` via
     `worksheet.build_worksheet` — identical file, identical format to what
     the CLI's `check` command produces.

3. **Grading table** — once a `review.csv` exists for the selected
   assignment (freshly written by Check, or pre-existing from a prior CLI
   or GUI session), render one row per student via
   `worksheet.read_worksheet`: name, status, an expandable captured-output
   panel, and one input widget per rubric field.
   - Mechanical fields render read-only (already computed).
   - Human fields render as: `st.number_input` (0..points) for
     `scoring_type: points` rubrics, or `st.selectbox` with
     excellent/good/developing/incomplete for `scoring_type:
     capstone_levels` rubrics — driven by `assignment_config["rubric"][name]`
     the same way `scoring.compute_score` branches on `scoring_type`.
   - Each row shows a live total via `gui_helpers.live_score(row,
     assignment_config)` — a thin wrapper that fills in the widget's
     current in-memory value and calls the real `scoring.compute_score`,
     catching `ScoringError` (e.g. still-blank fields) and rendering "—"
     instead of erroring the page.
   - "Save Worksheet" writes the current in-memory edits back to
     `review.csv` (same file, same format `build_worksheet` produces) so
     the CLI can pick up GUI edits and vice versa.

4. **Upload panel** — always reads the *saved* `review.csv` from disk (not
   in-memory table state), so what can be posted is provably whatever was
   last saved.
   - "Preview Upload" — calls `worksheet.incomplete_students` first; if
     any, lists them and disables further action. Otherwise computes
     current→new grade per student exactly as `cmd_upload`'s dry-run branch
     does (`CanvasClient.get_current_grade` + `scoring.compute_score`) and
     renders it as a table, posting nothing.
   - "Post Grades to Canvas" — disabled until Preview Upload has been run
     for the current saved worksheet state and `incomplete_students`
     returns empty; requires typing the assignment's key as a literal
     confirmation string (mirroring the CLI's `y/N` prompt, adapted for a
     button-driven UI) before calling `CanvasClient.post_grade` per student
     and writing the same `upload_log_<timestamp>.json` audit file
     `cmd_upload` writes.

## State, data flow & safety

`st.session_state`, keyed by `(course, assignment)`, holds: the in-memory
edited worksheet rows (before Save), the fetch/check log lines, and whether
Preview Upload has been run since the last save (gating the Post button).
Switching the assignment selector clears/reloads this state from disk so
edits never bleed across assignments.

Disk is the single source of truth end to end: Fetch writes to
`runs/<assignment>/<student_key>/`; Check reads those directories and
writes `runs/<assignment>/review.csv`; the grading table reads that CSV,
lets you edit in memory, and only Save Worksheet persists changes back to
it; Preview/Post Upload always re-read the saved CSV from disk, never the
in-memory table — so an edit made but not saved can never be silently
posted. Both hard CLI safety constraints carry over unweakened: Post is
disabled (not just warned) while any human field is blank, and requires a
typed confirmation before the real Canvas write.

Errors (bad token, network failure, wrong course/assignment id, a
`CanvasError`/`FetchError`/`ScoringError` bubbling up from any called
function) surface as an inline `st.error` with the exception's message —
same visibility the CLI gets from an uncaught exception and stack trace,
just formatted for the page.

## Testing & scope

`gui_helpers.py` functions (`compute_student_records`, `live_score`, and any
small formatting helpers the page needs) get normal pytest unit tests in
`autograder/tests/test_gui_helpers.py`, following the same fixture-based,
no-real-network style as the existing test suite. `gui.py` itself has no
automated tests — it's UI wiring only, verified by manually running
`streamlit run gui.py` against the pilot configs and walking through
fetch → check → edit → save → preview → (dry-run, not a real post) upload.

One new dependency: `streamlit>=1.35` added to `autograder/requirements.txt`.
No changes to any existing `autograder_common` module.
