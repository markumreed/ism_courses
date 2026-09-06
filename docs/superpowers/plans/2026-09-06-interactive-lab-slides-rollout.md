# Interactive Lab Slide Decks — Rollout Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Author the remaining 27 interactive reveal.js lab decks (13 ISM2411 + 14 ISM3232), on the framework and pattern validated by the two pilot decks, and ship all 29 by bumping the submodule pointers and listing the Canvas URLs.

**Architecture:** The shared framework (`assets/lab-slides.{js,css}` + `lab-shell.mjs` + `lab-widgets.mjs` + `lab-pyodide.mjs` + `lab-draw.mjs`) already exists byte-identically in both submodules on branch `interactive-lab-slides`. Each deck is a hand-authored `weekNN_lab_slides.html` that declares interactive components with data-attributes; content comes verbatim from the matching `instructor_notes/<course>/lab_wNN.md` facilitation guide; every runnable block is verified against the guide's stated output before commit (shell → the emulator in Node; Python → system `python3`, which is the same CPython 3.12 Pyodide bundles). Two small framework additions land first (honor `data-readonly` on shell blocks; a package-preload attribute for the ISM2411 pandas weeks), and the deferred whole-branch review of the pilot work runs before any new deck is built.

**Tech Stack:** reveal.js 4.6.1 (CDN), highlight.js 11.9.0, Pyodide 0.26.4 (jsdelivr, lazy), vanilla ES modules, Node 22 `node --test`, system `python3` 3.12 for verification.

**Spec:** `docs/superpowers/specs/2026-09-05-interactive-lab-slides-design.md`
**Recipe (binding how-to for every deck task):** `docs/superpowers/lab-slides-authoring.md`
**Prior plan (pilot):** `docs/superpowers/plans/2026-09-05-interactive-lab-slides.md`
**Exemplar decks:** `ism3232/docs/week02_lab_slides.html` (shell), `ism2411/pages/week03_lab_slides.html` (Python + `input()`)

## Global Constraints

- **Branch:** all submodule work continues on `interactive-lab-slides` in both `ism2411` and `ism3232` (already created, already holds the framework + 2 pilots). The parent repo stays on `instructor-lab-guides`. Do NOT merge to `main` or bump submodule pointers until the final task, and that task stops for user confirmation first.
- **Framework files stay byte-identical** across the two submodules except `lab-slides.css` (only the `--accent` line differs: `#2dd4bf` ism3232 / `#1e40af` ism2411). Any framework edit is applied to both copies in the same task and committed in both.
- **reveal.js 4.6.1** from `https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.6.1`; **highlight.js 11.9.0** `atom-one-dark`; **Pyodide 0.26.4** from `https://cdn.jsdelivr.net/pyodide/v0.26.4/full/`. No other versions or hosts.
- **Deck file locations:** ISM2411 → `ism2411/pages/weekNN_lab_slides.html`; ISM3232 → `ism3232/docs/weekNN_lab_slides.html`. `NN` is always two digits (`01`, `04`, `10`).
- **Deck `<head>`** is copied verbatim from the matching-course pilot deck's `<head>` (including the `localStorage '<course>-theme'` bootstrap IIFE, the CDN `<link>`s/`<script>`s in order, `../assets/lab-slides.css`, and `<script type="module" src="../assets/lab-slides.js"></script>` LAST).
- **Content source of truth** is `instructor_notes/<course>/lab_wNN.md`. Speaker notes (`<aside class="notes">` on every `<section>`) carry the guide's Teaching goal + the "Say to the class" quote VERBATIM + the line-by-line explanation + common mistakes + the check-for-understanding answer. Slide faces are the student view.
- **Every runnable block MUST reproduce the guide's stated output** before the deck is committed (verification method per the recipe §4, restated in the DAP below). **Every `.quiz` `data-answer` MUST match the guide's check-for-understanding parenthetical.**
- **Section classes:** `s-title s-glance s-obj s-timing s-sec s-idea s-code s-out s-quiz s-warn s-wrap s-end`.
- **`.predict` hidden `<pre class="answer" hidden>` must NOT contain an inner `<code class="language-*">`** (double-highlight warning).
- **Commits:** one per deck in its submodule on `interactive-lab-slides`; the deck file AND the one-line lab-page link edit go in the same commit. Every commit message ends with:
  ```

  Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
  Claude-Session: https://claude.ai/code/session_01PN8CuB5TvVSWeU365mCNnU
  ```
- **Deck inventory (27):**
  - ISM2411 (`pages/`, Python/Pyodide): w01, w02, w04, w05, w06, w07, w08, w10, w11, w12, w13, w14, w15
  - ISM3232 (`docs/`): shell-emulator — w01, w03, w04; Python/Pyodide — w05, w06, w07, w08, w10, w11, w12, w13, w14, w15, w16
- **Do NOT** run `npm`, install packages, or add a build step. Everything is static + CDN.

---

## Deck Authoring Procedure (DAP)

Every deck task (Tasks 4–30) executes this procedure with its own parameters
(`COURSE`, `WEEK`, `GUIDE`, `OUTPUT`, `LAB_PAGE`, `SUBTITLE`, `SPECIAL`). It is
written in full here once; a deck task's steps are this procedure plus that
task's parameter block and verification evidence. Read
`docs/superpowers/lab-slides-authoring.md` in full before the first deck; it is
the binding how-to and this is its checklist form.

**D1. Read** `GUIDE` end to end, plus recipe §1–§7, plus the same-course exemplar
deck (`ism2411/pages/week03_lab_slides.html` or `ism3232/docs/week02_lab_slides.html`).
Identify: the segment list (`## Intro` / `## Exercise N` / `## Part N` / `## Stretch …`),
each segment's "Live-code this" block, its "Expected output" / "Verified output",
its Check-for-understanding (answer in parens), its Common-mistakes list, the
Timing Plan rows, the Learning Objectives, the Session Snapshot fields, and the
Wrap-Up (reflection questions, submission checklist, next-module preview).

**D2. Create `OUTPUT`** with the `<head>` copied verbatim from the same-course
pilot, `<title>` = `<COURSE> Lab Week <WEEK> — <SUBTITLE>`, then the slide
skeleton from recipe §2:

1. `s-title` — eyebrow `<COURSE> · Week <WEEK> · <unit from guide frontmatter>`, `<h1><SUBTITLE></h1>`, a timing bar built from the guide's Timing Plan rows, the `← → · F · S · D` hint. `<aside class="notes">` = the Session Snapshot prose paragraph.
2. `s-glance` — a `.kv` list of Format / Prerequisites / Exercises-or-Parts covered / Submission, from the Session Snapshot table.
3. `s-obj` — the Learning Objectives as `<ul>`.
4. `s-timing` — the Timing Plan as `<table class="grid">`; notes = the paragraph under that table if any.
5. **Per segment** (Intro/Exercise/Part/Stretch), in guide order:
   - `s-sec` divider — chip (`Exercise N · <time range>`), headline; notes = Teaching goal + "Say to the class" verbatim.
   - `s-idea` `.concept` card when the guide states a single key idea for the segment (optional; skip if the segment is purely mechanical).
   - runnable `s-code` — a `.run` block (see D3) seeded with the guide's "Live-code this" source; notes = the line-by-line explanation.
   - `s-out` — a static `<pre>` of the guide's expected output (ALWAYS pair a runnable block with one), OR a `.predict` when the guide frames the check as "predict before running".
   - `s-quiz` — from the Check-for-understanding prompt; `data-answer` = the guide's parenthetical answer; `.why` = that answer text.
   - `s-warn` `.warn-card` — the Common-mistakes bullets.
6. Stretch segments — same sub-skeleton, lighter (divider + `s-code` + `s-out`, quiz/warn only if the guide has them).
7. `s-wrap` — reflection questions from the Wrap-Up.
8. `s-wrap` — submission checklist + the next-module preview sentence.
9. `s-end` — `<div class="sec-n"><COURSE> · Week <WEEK></div><h1>End of lab</h1>`.

Every `<section>` gets an `<aside class="notes">`.

**D3. Component markup** (copy real instances from the exemplar deck; recipe §3):
- Python: `<div class="run" data-lang="python">…source…</div>`. Add `data-stdin="l1&#10;l2"` when the source calls `input()` and the guide gives sample input. `data-readonly` for a block shown but not run. `data-packages="pandas,matplotlib"` for ISM2411 w12–w15 blocks that need them (Task 2 adds this attribute).
- Shell (ISM3232 w01/w03/w04 only): `<div class="run" data-lang="shell" data-fs='<JSON>'>…commands…</div>`. The emulator ALWAYS starts `cwd` at `/Users/student`; the first command in every block must be `cd ~/<path>`. `data-fs`: nested object = directory, string = file contents. `data-readonly` for `git …`, `python -m venv …`, `pip …` steps (these cannot run in the emulator) — Task 1 makes `data-readonly` actually suppress the editor on shell blocks; add a visible slide note "shown for reference — run on your own machine".
- Quiz: `<div class="quiz" data-answer="B"><p class="q">…</p><button data-opt="A">…</button>…<p class="why">…</p></div>`; multi-answer `data-answer="A,C"`.
- Predict: `<div class="predict">…prompt…<pre class="answer" hidden>…plain text…</pre></div>` — no inner `<code>`.

**D4. Verify every runnable block.** For each `.run` block, run its exact source
and confirm the output equals BOTH the paired `s-out` text AND the guide's stated
output for that segment:
- shell: `node --input-type=module -e 'import{createShell,run}from"./<COURSE>/assets/lab-shell.mjs";const sh=createShell(<the block's data-fs JSON>);for(const l of `<commands>`.split("\n")){const r=run(sh,l);process.stdout.write((r.out||"")+(r.err||""))}'`
- Python: write the source to a scratch file and run `printf '<stdin lines>\n' | python3 /tmp/blkN.py` (omit the `printf |` when the block has no `input()`); compare stdout, and for an error-demo block confirm the exact exception text.
- Fix the deck's seed / source / `s-out` text until every block matches. If a shell block cannot be made to match because of a genuine emulator bug (not a seed problem), fix `lab-shell.mjs` in BOTH submodules, add/adjust a `lab-shell.test.mjs` case, re-run `node --test` in both `assets/` dirs, and call it out prominently in the report as a framework change.

**D5. Verify quiz answers.** For each `.quiz`, quote the guide line its
`data-answer` comes from and confirm the marked option matches the guide's
parenthetical answer.

**D6. Structural check.** `grep -c '<section'` == `grep -c '</section>'`;
`grep -c '<aside class="notes"'` == section count; every `<div class="run"` has a
closing `</div>`; the `<head>` matches the pilot; `../assets/lab-slides.js` is the
last script and is `type="module"`.

**D7. Lab-page link.** In `LAB_PAGE`, immediately after the line
`<a href="weekNN_lab.html" class="weekjump-link current">Lab</a>` add
`<a href="weekNN_lab_slides.html" class="weekjump-link">Slides</a>` with matching
indentation. Exactly one added line; no other change to that file.

**D8. Commit** the deck file + the lab-page link edit together in the submodule,
on `interactive-lab-slides`, message `Add <COURSE> Week <WEEK> interactive lab deck`
+ the standard trailer.

**D9. Self-review** against D2–D7: skeleton present and ordered; every section has
notes carrying verbatim guide text (not paraphrase); every runnable block verified
in D4 with evidence; every quiz traced in D5; structural check clean; link added.

**D10. Report** to the task's report file: per runnable block — the verify command,
its output, the `s-out` text, and the guide line; per quiz — the prompt, the marked
answer, the guide line; the structural counts; the commit SHA; anything the recipe
did not cover, flagged as a concern.

---

### Task 1: Framework — honor `data-readonly` on shell blocks + `.predict` highlight guard

**Files:**
- Modify: `ism3232/assets/lab-slides.js` (the `buildShell` function) — and the byte-identical `ism2411/assets/lab-slides.js`
- Modify: `ism3232/assets/lab-widgets.mjs` (`upgradePredict`) — and `ism2411/assets/lab-widgets.mjs`
- Modify: `ism3232/assets/lab-widgets.test.mjs` — and `ism2411/assets/lab-widgets.test.mjs`

**Interfaces:**
- Consumes: existing `buildShell(el, …)` and `upgradePredict(el)` from the framework.
- Produces:
  - `buildShell` respects `el.hasAttribute('data-readonly')`: when set, render the command block as a static, syntax-highlightable `<pre>` + a disabled/absent input line (no "Run all", no interactive prompt) — mirroring how `buildPython` already treats `data-readonly`. The seeded `data-fs` is still parsed (harmless) but no `createShell` transcript UI is attached.
  - `upgradePredict` sets a `data-highlighted="1"` marker (or checks `dataset.highlighted`) on the answer `<pre>` before calling `window.hljs.highlightElement`, and skips the call if reveal's `RevealHighlight` already highlighted it — eliminating the "Element previously highlighted" `console.warn`.

- [ ] **Step 1: Write the failing test (predict guard)**

In `ism3232/assets/lab-widgets.test.mjs` add a test that constructs a minimal DOM double for a `.predict` element whose answer `<pre>` already has `dataset.highlighted === '1'`, calls `upgradePredict`, and asserts `window.hljs.highlightElement` (a spy) was NOT called for that node. Use a tiny hand-rolled `document`/element stub consistent with the existing test style; if the existing tests have no DOM stub, add a minimal one in this file only.

```js
test('upgradePredict does not re-highlight an already-highlighted answer', () => {
  let calls = 0;
  global.window = { hljs: { highlightElement() { calls++; } } };
  const pre = mkEl('pre', { class: 'answer' }); pre.hidden = true; pre.dataset.highlighted = '1';
  const el = mkEl('div', { class: 'predict' }); el.append(pre);
  upgradePredict(el);
  // simulate the reveal button click the upgrader wires:
  el.querySelector('button')?.click?.();
  assert.equal(calls, 0);
});
```

- [ ] **Step 2: Run it to verify it fails**

Run: `cd ism3232/assets && node --test lab-widgets.test.mjs`
Expected: FAIL — `upgradePredict` currently always calls `highlightElement`.

- [ ] **Step 3: Implement both framework changes**

In `lab-slides.js` `buildShell`: at the top, `if (el.hasAttribute('data-readonly')) { renderReadonly(el); return; }` where `renderReadonly` produces the same static `<pre><code class="language-bash">…</code></pre>` treatment `buildPython`'s readonly branch uses (factor a shared helper if the two are identical). No transcript, no input row, no "Run all".
In `lab-widgets.mjs` `upgradePredict`: guard the `hljs.highlightElement` call with `if (!pre.dataset.highlighted) { pre.dataset.highlighted = '1'; window.hljs?.highlightElement(pre); }`.
Apply each edit to BOTH submodule copies (keep byte-identical).

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd ism3232/assets && node --test && cd ../../ism2411/assets && node --test`
Expected: PASS in both (prior counts + the new predict test).
Also `node --check ism3232/assets/lab-slides.js && node --check ism2411/assets/lab-slides.js`.

- [ ] **Step 5: Confirm byte-identical**

Run: `diff ism3232/assets/lab-slides.js ism2411/assets/lab-slides.js` (no output) and `diff ism3232/assets/lab-widgets.mjs ism2411/assets/lab-widgets.mjs` (no output). `diff ism3232/assets/lab-slides.css ism2411/assets/lab-slides.css` still shows only the `--accent` line.

- [ ] **Step 6: Commit (both submodules)**

```bash
cd ism3232 && git add assets/lab-slides.js assets/lab-widgets.mjs assets/lab-widgets.test.mjs && \
git commit -m "$(printf 'Honor data-readonly on shell blocks; guard predict re-highlight\n\nbuildShell now renders a static block for data-readonly shell steps\n(git/venv/pip cannot run in the emulator). upgradePredict no longer\nre-highlights an answer reveal.js already highlighted.\n\nCo-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01PN8CuB5TvVSWeU365mCNnU')"
cd ../ism2411 && git add assets/lab-slides.js assets/lab-widgets.mjs assets/lab-widgets.test.mjs && \
git commit -m "$(printf 'Honor data-readonly on shell blocks; guard predict re-highlight (shared)\n\nCo-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01PN8CuB5TvVSWeU365mCNnU')"
cd ..
```

---

### Task 2: Framework — `data-packages` preload for ISM2411 pandas/matplotlib weeks

**Files:**
- Modify: `ism3232/assets/lab-slides.js` (`buildPython`) + byte-identical `ism2411/assets/lab-slides.js`
- Modify: `ism3232/assets/lab-slides.css` + `ism2411/assets/lab-slides.css` (a small style for the preload affordance; accent-only-diff rule still holds)

**Interfaces:**
- Consumes: `loadPackages(names)` from `lab-pyodide.mjs` (already exported: `loadPackages(['pandas','matplotlib']) -> Promise<void>`), and the existing `runPython` matplotlib story.
- Produces:
  - `buildPython` reads `el.dataset.packages` (comma-separated). When present: the Run button's first activation shows `loading packages…` and `await loadPackages(names.split(','))` before the first `runPython`; subsequent runs skip it. If load fails (offline), the output pane shows the error and the block falls back to displaying its paired `s-out` is unaffected (the `s-out` slide is separate).
  - matplotlib figures: after a run, if `sys.modules` has `matplotlib` and a figure exists, the harness already renders it — confirm the existing path; if there is none, add: run `import matplotlib; matplotlib.use('AGG')` in the preamble and after the user code do `import base64,io; buf=io.BytesIO(); import matplotlib.pyplot as _plt; _plt.savefig(buf,format='png'); ` then surface the PNG as an `<img>` in the output pane. Keep this minimal and only active when `data-packages` includes `matplotlib`.
  - CSV fixtures: document (in the recipe, Step 5) that a deck embeds sample CSV as a Python triple-quoted string and writes it to Pyodide's virtual FS with `Path("sales.csv").write_text(CSV)` at the top of the block — no framework change needed, just the pattern.

- [ ] **Step 1: Implement `data-packages` handling in `buildPython`**

Add the `dataset.packages` branch described above. Guard so a block without the attribute is completely unaffected (regression-safety for the 24 non-data decks and both pilots).

- [ ] **Step 2: Implement / confirm the matplotlib-to-PNG path**

Read the current `buildPython` + `runPython` for any existing figure handling. If present and sufficient, leave it and note so. If absent, add the minimal `AGG` + `savefig` → `<img>` path, active only when `data-packages` includes `matplotlib`.

- [ ] **Step 3: Style the preload affordance**

Add a `.run .pkg-status` rule to `lab-slides.css` (muted text, same treatment as the existing `.run .status`). Apply to both copies; re-confirm `diff` of the two CSS files is still only the `--accent` line.

- [ ] **Step 4: Syntax + regression checks**

Run: `node --check` on both `lab-slides.js`; `node --test` in both `assets/` dirs (unchanged counts — this task adds no unit test; the behavior is browser-only and is exercised by the ISM2411 w13 deck task and the final browser pass). Manually re-read the diff to confirm a no-`data-packages` block is byte-for-byte behaviourally unchanged.

- [ ] **Step 5: Update the recipe**

In `docs/superpowers/lab-slides-authoring.md` §5 (ISM2411), replace the "Load data tools" placeholder guidance with the finalized `data-packages="pandas,matplotlib"` attribute usage and the embedded-CSV `Path(...).write_text(...)` pattern. Commit this recipe edit in the parent repo (branch `instructor-lab-guides`) in its own commit.

- [ ] **Step 6: Commit (both submodules + parent)**

```bash
cd ism3232 && git add assets/lab-slides.js assets/lab-slides.css && \
git commit -m "$(printf 'Add data-packages preload + matplotlib PNG output for data decks\n\nCo-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01PN8CuB5TvVSWeU365mCNnU')"
cd ../ism2411 && git add assets/lab-slides.js assets/lab-slides.css && \
git commit -m "$(printf 'Add data-packages preload + matplotlib PNG output for data decks (shared)\n\nCo-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01PN8CuB5TvVSWeU365mCNnU')"
cd .. && git add docs/superpowers/lab-slides-authoring.md && \
git commit -m "$(printf 'Finalize data-decks guidance in the lab-slides authoring recipe\n\nCo-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01PN8CuB5TvVSWeU365mCNnU')"
```

---

### Task 3: Deferred whole-branch review of the pilot framework + decks

The pilot plan's final whole-branch review did not run (session rate limit). Run it now, before 27 more decks build on the framework.

**Files:** none created; this task produces a review and, if needed, one fix commit set.

- [ ] **Step 1: Generate the branch review package (both submodules)**

For each submodule: `git log --oneline main..HEAD`, `git diff --stat main..HEAD`, and `git diff -U10 main..HEAD` redirected into one file per submodule under the SDD workspace (`.superpowers/sdd/2026-09-06-interactive-lab-slides-rollout/`). Also include the parent's three feature commits (`460d785`, `22d991f`, `bf561f5`) and the Task 1/2 commits from this plan.

- [ ] **Step 2: Dispatch the whole-branch code reviewer**

Use `superpowers:requesting-code-review`'s `code-reviewer.md` on the most capable available model. Point it at: the package files, the spec, the recipe, and the pilot ledger's deferred-minor / parked lines (`.superpowers/sdd/2026-09-05-interactive-lab-slides/progress.md`). Scope: the whole `interactive-lab-slides` branch in both submodules + the parent feature commits. Ask it to triage which deferred minors must be fixed before the rollout proceeds.

- [ ] **Step 3: Apply fixes (one dispatch)**

If the review returns Critical/Important findings, dispatch ONE fix subagent with the complete list. Then one scoped re-review of the fix range. Adjudicate residuals per the SDD breaker rules (park with a ruling, or fix load-bearing ones). Framework fixes go to both submodule copies.

- [ ] **Step 4: Record the outcome**

Append to the SDD ledger: the review verdict, every finding and its disposition, and any commits. This gate must be GREEN (or all residuals parked with rulings) before Task 4.

---

### Tasks 4–16: ISM2411 decks

Each task executes the **DAP** with the parameters below. `COURSE=ISM2411`,
output dir `ism2411/pages/`, exemplar `ism2411/pages/week03_lab_slides.html`,
all Python/Pyodide (no shell emulator). Steps for every task: **D1 → D10** as
written in the DAP, ending with the D8 commit and the D10 report to
`.superpowers/sdd/2026-09-06-interactive-lab-slides-rollout/task-<N>-report.md`.

| Task | WEEK | GUIDE | OUTPUT | LAB_PAGE | SUBTITLE | SPECIAL |
|---|---|---|---|---|---|---|
| 4 | 01 | `instructor_notes/ism2411/lab_w01.md` | `ism2411/pages/week01_lab_slides.html` | `ism2411/pages/week01_lab.html` | *(from guide frontmatter `subtitle`, minus "— Instructor Facilitation Guide")* | "Computer Vocabulary & File System Tour" — likely conceptual + a few terminal commands. Terminal command sequences: use `data-lang="shell"` blocks (the emulator ships in `ism2411/assets/` too) leading with `cd ~/…`; if the guide's commands are pure narration (no expected output), use `data-readonly`. No `input()` yet. |
| 5 | 02 | `instructor_notes/ism2411/lab_w02.md` | `ism2411/pages/week02_lab_slides.html` | `ism2411/pages/week02_lab.html` | *(from guide)* | "First Terminal Session & First Python Script". Mix: a `data-lang="shell"` block for the terminal session (lead with `cd`), a `data-lang="python"` block for `hello.py`. |
| 6 | 04 | `instructor_notes/ism2411/lab_w04.md` | `ism2411/pages/week04_lab_slides.html` | `ism2411/pages/week04_lab.html` | *(from guide)* | "Revenue, Margin & Discount Calculator". Pure Python. Watch for `//` vs `/` and parenthesis-in-formula demos the guide calls out. |
| 7 | 05 | `instructor_notes/ism2411/lab_w05.md` | `ism2411/pages/week05_lab_slides.html` | `ism2411/pages/week05_lab.html` | *(from guide)* | "Tiered Discount Calculator" — conditionals. `input()` likely; use `data-stdin`. |
| 8 | 06 | `instructor_notes/ism2411/lab_w06.md` | `ism2411/pages/week06_lab_slides.html` | `ism2411/pages/week06_lab.html` | *(from guide)* | "Sales Loop — Sum, Average, Max" — loops. |
| 9 | 07 | `instructor_notes/ism2411/lab_w07.md` | `ism2411/pages/week07_lab_slides.html` | `ism2411/pages/week07_lab.html` | *(from guide)* | "Functions + Debug First". The guide has deliberately-broken code then a fix — author both passes as separate `s-code`/`s-out` pairs like the pilot's Exercise 3. |
| 10 | 08 | `instructor_notes/ism2411/lab_w08.md` | `ism2411/pages/week08_lab_slides.html` | `ism2411/pages/week08_lab.html` | *(from guide)* | "Your First GitHub Submission" — git workflow. `git …` commands cannot run: `data-lang="shell"` + `data-readonly` static, with a "run on your own machine" note. Any Python stays runnable. |
| 11 | 10 | `instructor_notes/ism2411/lab_w10.md` | `ism2411/pages/week10_lab_slides.html` | `ism2411/pages/week10_lab.html` | *(from guide)* | "Inventory List Manager" — lists. |
| 12 | 11 | `instructor_notes/ism2411/lab_w11.md` | `ism2411/pages/week11_lab_slides.html` | `ism2411/pages/week11_lab.html` | *(from guide)* | "Customer Dictionary & Lookup" — dicts. |
| 13 | 12 | `instructor_notes/ism2411/lab_w12.md` | `ism2411/pages/week12_lab_slides.html` | `ism2411/pages/week12_lab.html` | *(from guide)* | "Read a Sales CSV, Write a Cleaned Report". **Data week:** `data-packages` not needed for stdlib `csv`; embed the sample CSV as a triple-quoted string + `Path("sales.csv").write_text(CSV)` at the top of the block. Verify with `python3` after writing the same fixture locally. |
| 14 | 13 | `instructor_notes/ism2411/lab_w13.md` | `ism2411/pages/week13_lab_slides.html` | `ism2411/pages/week13_lab.html` | *(from guide)* | "First DataFrame — Retail Sales Explorer". **Data week:** `data-packages="pandas"` on the runnable blocks; embed the CSV fixture. If a block's Pyodide load time is prohibitive, mark it `data-readonly` and rely on the paired `s-out` (recipe §5). Verify with a local `python3` that has pandas, or if unavailable, verify the expected output by hand against the guide and note it. |
| 15 | 14 | `instructor_notes/ism2411/lab_w14.md` | `ism2411/pages/week14_lab_slides.html` | `ism2411/pages/week14_lab.html` | *(from guide)* | "Clean a Messy Sales CSV". **Data week:** `data-packages="pandas"`; embed the messy CSV fixture. Same verify note as w13. |
| 16 | 15 | `instructor_notes/ism2411/lab_w15.md` | `ism2411/pages/week15_lab_slides.html` | `ism2411/pages/week15_lab.html` | *(from guide)* | "Aggregate & Chart — Capstone Warm-up". **Data week:** `data-packages="pandas,matplotlib"`; the chart block renders a PNG via the Task 2 path; pair it with an `s-out` describing the expected chart (axis, series) since a PNG can't be diffed. |

Each task's Files block: **Create** `OUTPUT`; **Modify** `LAB_PAGE` (one line);
**Report** `.superpowers/sdd/2026-09-06-interactive-lab-slides-rollout/task-<N>-report.md`.
Each task's Interfaces: **Consumes** the framework at `../assets/lab-slides.{css,js}`
(and, for data weeks, the Task 2 `data-packages` behavior); **Produces** a
published deck + a lab-page link (no interface other decks consume).

- [ ] **(per task) D1–D10 as written in the DAP, with the row's parameters.**
- [ ] **(per task) D4 evidence present in the report for every runnable block.**
- [ ] **(per task) D5 evidence present for every quiz.**
- [ ] **(per task) D6 structural check clean.**
- [ ] **(per task) D8 commit made (deck + link) on `interactive-lab-slides`.**

---

### Tasks 17–30: ISM3232 decks

Each task executes the **DAP** with the parameters below. `COURSE=ISM3232`,
output dir `ism3232/docs/`, exemplars `ism3232/docs/week02_lab_slides.html`
(shell) and `ism2411/pages/week03_lab_slides.html` (Python).

| Task | WEEK | GUIDE | OUTPUT | LAB_PAGE | SUBTITLE | SPECIAL |
|---|---|---|---|---|---|---|
| 17 | 01 | `instructor_notes/ism3232/lab_w01.md` | `ism3232/docs/week01_lab_slides.html` | `ism3232/docs/week01_lab.html` | *(from guide)* | "Developer Mindset & First Setup". **Shell week.** Setup/verify commands as `data-lang="shell"` (lead with `cd ~`); `git`, `python3 --version` checks that produce version strings the emulator can't know → `data-readonly` static with a note. |
| 18 | 03 | `instructor_notes/ism3232/lab_w03.md` | `ism3232/docs/week03_lab_slides.html` | `ism3232/docs/week03_lab.html` | *(from guide)* | "Virtual Environments & Shell Customisation". **Shell week.** `python -m venv`, `source …/activate`, `pip install`, `.zshrc` edits → all `data-lang="shell"` `data-readonly` static (Task 1 makes these render clean), each with a "run on your own machine" note. `ls -la` / `cd` / `cat ~/.zshrc` that DO work → runnable, seed a `.venv/` and `.zshrc` into `data-fs`. |
| 19 | 04 | `instructor_notes/ism3232/lab_w04.md` | `ism3232/docs/week04_lab_slides.html` | `ism3232/docs/week04_lab.html` | *(from guide)* | "Search Tools, the Submission Ritual & Git". **Shell week.** `grep`/`find`/`ripgrep` over a seeded tree → runnable if the emulator supports them; if not (check `lab-shell.mjs` command list), `data-readonly` static. `git` steps → `data-readonly` static. |
| 20 | 05 | `instructor_notes/ism3232/lab_w05.md` | `ism3232/docs/week05_lab_slides.html` | `ism3232/docs/week05_lab.html` | *(from guide)* | "Variables, Data Types & Operators". **Python week** — Pyodide from here on. |
| 21 | 06 | `instructor_notes/ism3232/lab_w06.md` | `ism3232/docs/week06_lab_slides.html` | `ism3232/docs/week06_lab.html` | *(from guide)* | "Conditionals, Loops & Dictionaries". Python. `input()` likely → `data-stdin`. |
| 22 | 07 | `instructor_notes/ism3232/lab_w07.md` | `ism3232/docs/week07_lab_slides.html` | `ism3232/docs/week07_lab.html` | *(from guide)* | "Functions, Modules & pytest". Python. `pytest` runs are NOT available in Pyodide by default — show `pytest` invocations + expected output as `data-readonly` static; the functions-under-test stay runnable. |
| 23 | 08 | `instructor_notes/ism3232/lab_w08.md` | `ism3232/docs/week08_lab_slides.html` | `ism3232/docs/week08_lab.html` | *(from guide)* | "Debugging, AI Literacy & Midterm Review". Python. Broken-then-fixed passes like the pilot Exercise 3. |
| 24 | 10 | `instructor_notes/ism3232/lab_w10.md` | `ism3232/docs/week10_lab_slides.html` | `ism3232/docs/week10_lab.html` | *(from guide)* | "OOP I — Classes & Objects". Python. |
| 25 | 11 | `instructor_notes/ism3232/lab_w11.md` | `ism3232/docs/week11_lab_slides.html` | `ism3232/docs/week11_lab.html` | *(from guide)* | "OOP II — Composition, Inheritance & SQL Mapping". Python; any SQL is conceptual here (w14 is the runnable SQL lab). |
| 26 | 12 | `instructor_notes/ism3232/lab_w12.md` | `ism3232/docs/week12_lab_slides.html` | `ism3232/docs/week12_lab.html` | *(from guide)* | "OOP III — Applied Practice & Design". Python. |
| 27 | 13 | `instructor_notes/ism3232/lab_w13.md` | `ism3232/docs/week13_lab_slides.html` | `ism3232/docs/week13_lab.html` | *(from guide)* | "Capstone Design & SQL Foundations". Python + `import sqlite3` (Pyodide stdlib — runnable). Seed any DB with `sqlite3.connect(":memory:")` + inline `CREATE`/`INSERT` at the top of the block. |
| 28 | 14 | `instructor_notes/ism3232/lab_w14.md` | `ism3232/docs/week14_lab_slides.html` | `ism3232/docs/week14_lab.html` | *(from guide)* | "Python + SQL Integration". `sqlite3` runnable; verify with local `python3` (sqlite3 is stdlib there too). |
| 29 | 15 | `instructor_notes/ism3232/lab_w15.md` | `ism3232/docs/week15_lab_slides.html` | `ism3232/docs/week15_lab.html` | *(from guide)* | "Streamlit Business Interface". Streamlit CANNOT run client-side → ALL code blocks `data-readonly` static, each with a visible "this runs with `streamlit run app.py` on your machine" note; lean on `s-out` slides describing the rendered UI, plus knowledge-check quizzes. |
| 30 | 16 | `instructor_notes/ism3232/lab_w16.md` | `ism3232/docs/week16_lab_slides.html` | `ism3232/docs/week16_lab.html` | *(from guide)* | "GenAI Feature & Final Demo". External API calls CANNOT run client-side → code blocks `data-readonly` static with a "needs an API key / runs on your machine" note; walkthrough + knowledge-check treatment. |

Same per-task checkboxes as Tasks 4–16 (D1–D10, D4/D5/D6/D8 evidence).

---

### Task 31: Full browser pass, submodule pointer bump, Canvas URL list

**Files:**
- Modify (parent, `instructor-lab-guides`): the `ism2411` and `ism3232` submodule pointers (a normal `git add <submodule>` in the parent).

- [ ] **Step 1: Serve and browser-verify all 29 decks + both harness pages**

`cd ism3232 && python3 -m http.server 8747` and `cd ism2411 && python3 -m http.server 8748`. In a real browser (Chrome with the automation extension, or by hand), for `_lab_slides_harness.html` and every `weekNN_lab_slides.html` in both courses, confirm the recipe §9 checklist: Pyodide cold start executes and prints; `data-stdin` / `input()` boxes feed correctly and an empty queue shows `EOFError`; shell blocks run against the emulator; `data-readonly` blocks show no Run affordance; `data-packages` blocks load pandas/matplotlib and a chart PNG renders; quizzes mark right/wrong; predicts reveal; **D** draws and syncs to the notes window; `?print-pdf` hides the overlay; dark and light are both legible; the console has no errors (the only tolerated warning is highlight.js on a code block, and Task 1 should have removed even that for predicts). Record pass/fail per deck in the task report; any failure routes to a fix in the owning deck or framework file, re-verified.

- [ ] **Step 2: Confirm every lab page links its deck**

For NN in every week of each course: `grep -c 'weekNN_lab_slides.html' <course>/<dir>/weekNN_lab.html` == 1. Fix any missing link (one-line edit + commit in that submodule).

- [ ] **Step 3: Fast-forward each submodule's `main` — STOP for user confirmation first**

Present to the user: the full `git log --oneline main..interactive-lab-slides` for each submodule, the deck count, and the browser-pass result. Ask for explicit confirmation to integrate. On yes: in each submodule `git checkout main && git merge --ff-only interactive-lab-slides` (or a non-ff merge if the user prefers a merge commit). If `--ff-only` fails because `main` moved, rebase `interactive-lab-slides` on `main` first and re-run the browser pass on anything affected.

- [ ] **Step 4: Bump the submodule pointers in the parent**

```bash
cd /Users/markumreed/Documents/ism_courses
git add ism2411 ism3232
git commit -m "$(printf 'Publish interactive lab slide decks for all ISM2411 + ISM3232 labs\n\n29 hand-authored reveal.js decks (in-browser Python via Pyodide,\nzsh emulator, knowledge checks, instructor draw overlay), one per\nin-class lab, linked from each lab page.\n\nCo-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01PN8CuB5TvVSWeU365mCNnU')"
```

- [ ] **Step 5: Print the 29 Canvas URLs**

Emit the list for the user to add to Canvas manually:
```
ISM2411:  https://markumreed.github.io/ism2411/pages/weekNN_lab_slides.html   for NN in 01 02 03 04 05 06 07 08 10 11 12 13 14 15
ISM3232:  https://markumreed.github.io/ism3232/docs/weekNN_lab_slides.html    for NN in 01 02 03 04 05 06 07 08 10 11 12 13 14 15 16
```
Expanded to all 29 explicit URLs in the task report.

---

## Self-Review

**1. Spec coverage.** The spec's deck inventory is 29 (14 ISM2411 + 15 ISM3232); 2 are the pilots, 27 are Tasks 4–30 here — every remaining week has exactly one task (cross-checked against `ls instructor_notes/*/lab_w*.md`). Spec "Course-specific notes": ISM2411 data weeks w12–w15 → Task 2 framework support + Tasks 13–16 use it; ISM3232 shell w01/w03/w04 → Tasks 17–19 + Task 1 framework support; ISM3232 w14 sqlite3 runnable → Task 28; w15/w16 readonly → Tasks 29–30. Spec "Publishing" (lab-page link, submodule commit, pointer bump, Canvas URL list) → DAP D7/D8 per deck + Task 31. Spec "Risks" (Pyodide slow/blocked → paired static `s-out`) → DAP D2 step 5 mandates an `s-out` for every runnable block. The deferred pilot whole-branch review → Task 3.

**2. Placeholder scan.** No "TBD"/"TODO". The `SUBTITLE` column says "*(from guide frontmatter)*" — this is a concrete instruction (the `subtitle:` field, minus the "— Instructor Facilitation Guide" suffix), the same derivation the two shipped pilots used, not a blank to fill. Tasks 4–30 do not inline each deck's slide text because the binding content is the guide file named in the row plus the recipe plus the two committed exemplar decks — the same inputs the pilot tasks used successfully; the DAP is the fully-written procedure. Per-week SPECIAL notes capture the deviations known without reading all 27 guides; the DAP requires anything else to surface as a report concern (which the controller adjudicates), not a guess.

**3. Type / interface consistency.** `data-readonly` (shell) and `data-packages` are introduced in Tasks 1–2 and consumed by name in the DAP D3 and the Tasks 13–16 / 17–19 / 29–30 SPECIAL notes. `createShell` / `run` (Task 3 pilot review may touch `lab-shell.mjs`; DAP D4 calls them with the same `{out,err}` shape the pilot plan established). `loadPackages(names)` — the name and signature match `lab-pyodide.mjs`'s existing export. Output path pattern `week<NN>_lab_slides.html` and link target `week<NN>_lab_slides.html` are consistent between DAP D2, D7, and Task 31 Steps 2 and 5. Branch name `interactive-lab-slides` and the commit trailer are identical to the pilot plan and to every row here.

**4. Ordering.** Task 1 (shell `data-readonly`) precedes Tasks 17–19 which need it. Task 2 (`data-packages`) precedes Tasks 13–16 which need it. Task 3 (pilot review) precedes all deck tasks. Tasks 4–30 are mutually independent (different files, no shared state) but must run one at a time per submodule to avoid commit races — the executor serializes them. Task 31 is last and is the only task that writes the parent repo's submodule pointers or touches `main`.

## Execution Handoff

**Plan complete and saved to `docs/superpowers/plans/2026-09-06-interactive-lab-slides-rollout.md`. Two execution options:**

**1. Subagent-Driven (recommended)** — fresh subagent per task, review between tasks, fast iteration. For the 27 near-identical deck tasks the controller may step the reviewer model down once several in a course have cleared cleanly.

**2. Inline Execution** — execute tasks in this session using executing-plans, batch execution with checkpoints.

**Which approach?**
