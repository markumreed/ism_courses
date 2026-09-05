# Interactive Lab Slide Decks — Design

**Date:** 2026-09-05
**Status:** Approved (design), pending implementation
**Scope:** ISM2411 (14 labs) + ISM3232 (15 labs) — 29 hand-authored reveal.js decks + a shared interactivity layer per course.

## Goal

Every in-class lab gets an interactive reveal.js deck that serves two audiences from
one file:

- **Students** — the slide face. Runnable code they edit and execute in the browser,
  knowledge-check questions with instant feedback, step-through reveals. Published to
  the course site and linked from Canvas so students can review after class.
- **Instructor** — the speaker notes (press **S**). Each slide's `<aside class="notes">`
  carries the facilitation detail from the lab guide: teaching goal, full "Say to the
  class" script, common pitfalls, and the answer to every check-for-understanding
  prompt. Plus a drawing overlay (press **D**) for live annotation during projection.

Source of truth for content is the instructor facilitation guides:
`instructor_notes/ism2411/lab_w*.md` and `instructor_notes/ism3232/lab_w*.md`.

## Non-goals

- No slide **generator**. Decks are hand-authored (explicit user decision). The shared
  layer is a component library, not a build step.
- Not replacing the existing `instructor_notes/build_slides.py` (untracked, never run) —
  it stays as-is; this work supersedes it in practice.
- Not touching the existing ISM3232 `weekNN_slides.html` *lecture* decks.
- No server. Everything runs client-side from GitHub Pages + CDNs.

## Architecture

### Shared interactivity layer (one pair per course)

```
ism2411/assets/lab-slides.css      ism3232/assets/lab-slides.css
ism2411/assets/lab-slides.js       ism3232/assets/lab-slides.js
```

The two CSS files are identical except for the course accent color; the two JS files
are identical. They are duplicated (not symlinked or shared) because the submodules are
independent git repos published separately. Keep them byte-identical except the CSS
accent; any change to one is applied to both.

External libs, all from CDNs already in use by the repo (`cdnjs.cloudflare.com`) plus
`cdn.jsdelivr.net` for Pyodide:

- reveal.js **4.6.1** + `plugin/highlight`, `plugin/notes`
- highlight.js 11.9.0 theme `atom-one-dark`
- Pyodide **0.26.x** from `cdn.jsdelivr.net/pyodide/` — lazy-loaded on first Run click

### Components (declarative markup → JS upgrades on `Reveal.ready`)

1. **Runnable Python** — `data-lang="python"`

   ```html
   <div class="run" data-lang="python">
   product = "Notebook"
   print(type(product))
   </div>
   ```

   Renders: editable `<textarea>` (tab-aware, monospace) + **Run ▶** button + output
   pane. First Run anywhere on the page shows a one-time "starting Python…" state
   (~4s) while Pyodide boots, then executes. Subsequent runs are instant.

   - `stdout` and `stderr` captured and shown; tracebacks shown verbatim (reading real
     tracebacks is a course learning objective).
   - `input()` support: if the source contains `input(`, a **stdin** box appears above
     the Run button. Lines typed there are fed to `input()` in order. `builtins.input`
     is overridden to pull from that queue and echo the prompt + value into output,
     mimicking a terminal.
   - `data-autorun` (optional) runs once on slide-enter.
   - `data-readonly` (optional) hides the editor, shows code + Run only.
   - Reset link restores the original source.

2. **Simulated shell** — `data-lang="shell"` (ISM3232 w01–w04 only)

   ```html
   <div class="run" data-lang="shell" data-fs='{"~/ism3232":{"notes.txt":"..."}}'>
   pwd
   ls -la
   </div>
   ```

   A mock terminal with an in-memory filesystem seeded per deck from `data-fs`
   (JSON: nested objects = dirs, strings = file contents). Prompt is
   `user@MacBook-Pro <cwd> %`. Interactive: type a command, Enter runs it; the
   pre-seeded script lines are offered as a "run all" convenience.

   Supported commands (the set the labs actually use):
   `pwd, ls [-l|-a|-la|-al], cd [dir|..|~|-], mkdir [-p], touch, cat, echo [> / >>],
   rm [-r], mv, cp [-r], tree [-L n], head [-n], tail [-n], clear, whoami, which,
   history`. Plus `python3 <file>` and `python3 -c "…"` routed through Pyodide.
   Unknown commands print `zsh: command not found: <cmd>`. No network, no `sudo`,
   no package installs (labs that need `pip`/`venv` show those as static code, not
   runnable — noted per-deck).

3. **Knowledge check** — `class="quiz"`

   ```html
   <div class="quiz" data-answer="B">
     <p class="q">What does <code>type(12.0)</code> report?</p>
     <button data-opt="A">&lt;class 'int'&gt;</button>
     <button data-opt="B">&lt;class 'float'&gt;</button>
     <button data-opt="C">&lt;class 'str'&gt;</button>
     <p class="why">The decimal point makes it a float, even though the value is whole.</p>
   </div>
   ```

   Click marks the chosen option right/wrong, reveals `.why`. Multi-answer via
   `data-answer="A,C"`. "Predict the output" variant: `class="predict"` with a hidden
   `<pre>` revealed by a **Reveal answer** button.

4. **Step-through reveals** — native reveal.js `class="fragment"`. Documented patterns
   in the framework README comment: line-by-line code build (`<span class="fragment">`
   per line inside `<pre>`), progressive list reveal, diagram assembly.

5. **Instructor annotation overlay** — ported verbatim from
   `ism3232/docs/week02_slides.html` (drawing overlay v3: fixed-canvas, BroadcastChannel
   sync to the notes popup, toolbar, press **D** to toggle). Colors keyed to the course
   accent. Disabled automatically in reveal's print/PDF export.

### Deck skeleton (all 29)

| # | Slide | Source in guide |
|---|-------|-----------------|
| 1 | Title — course · week · subtitle, timing bar, `← → · F · S · D` hint | frontmatter + Timing Plan |
| 2 | Today at a glance — format, prerequisites, exercises covered, submission | Session Snapshot table |
| 3 | Learning objectives | Learning Objectives |
| 4 | Timing plan | Timing Plan / Segments |
| 5.. | **Per exercise:** section divider → "the idea" / say-to-the-class → runnable live-code → expected output → knowledge check → ⚠ common pitfalls | Segment-by-Segment Walkthrough `## Exercise N` |
| .. | Stretch A / B sections (same sub-skeleton, lighter) | `## Stretch …` |
| n-2 | Reflection questions | Wrap-Up |
| n-1 | Submission checklist + next-module preview | Wrap-Up |
| n | End of lab | — |

Every slide: `<aside class="notes">` with teaching goal + "Say to the class" verbatim +
pitfalls + check-for-understanding answers.

Slide `<section>` classes for styling: `s-title s-glance s-obj s-timing s-sec s-idea
s-code s-out s-quiz s-warn s-wrap s-end`.

### Publishing

- Add a `▶ Interactive slides` link to each `weekNN_lab.html` page (both submodules).
- Commit inside each submodule; bump the submodule pointer in the parent repo.
- Canvas links added manually by the user — implementation ends with a printed list of
  the 29 published URLs (`https://markumreed.github.io/ism2411/pages/weekNN_lab_slides.html`
  and `.../ism3232/docs/weekNN_lab_slides.html`).

## Course-specific notes

**ISM2411** — all 14 labs are Python; Pyodide only, no shell. `input()` appears from
w03 on. w12–w15 use pandas/matplotlib: Pyodide can `micropip.install("pandas")` — decks
for those weeks pre-load the packages on first Run and bundle any sample CSV inline as a
string written to Pyodide's virtual FS. Charts render to a PNG shown in the output pane.

**ISM3232** — w01–w04 are shell/git/venv → simulated shell (git and venv shown as
static code with a note, since they can't run in the emulator). w05–w16 are Python
(variables → OOP → SQL → Streamlit) → Pyodide. w14 SQL uses `sqlite3` (bundled in
Pyodide stdlib — works). w15 Streamlit and w16 GenAI API calls can't run client-side →
those decks use `data-readonly` code + a knowledge-check / walkthrough treatment instead
of live execution, called out explicitly on the slide.

## Risks / mitigations

| Risk | Mitigation |
|---|---|
| Pyodide first load slow / blocked on lab wifi | Lazy load; every runnable slide is paired with a static "expected output" slide so the deck teaches fully with zero code execution |
| Shell emulator scope creep | Fixed command list above; anything outside it is static code with a note |
| 29 decks drift from the guides over time | Decks link their source guide in a notes comment; guides remain source of truth |
| Two copies of the framework diverge | Rule: byte-identical except CSS accent; PR checklist item |
| pandas/matplotlib in Pyodide heavy (~15MB) | Only w12–w15; shown as opt-in "Load data tools" button, not autorun |

## Implementation sequencing

1. **Framework** — `lab-slides.css` + `lab-slides.js` for both courses: reveal init,
   Python runner + Pyodide harness + `input()` shim, shell emulator, quiz/predict,
   drawing overlay, print/PDF guard. Test harness page listing every component.
2. **Two pilot decks** — ISM2411 **w03** (Pyodide + `input()` two-pass failure demo) and
   ISM3232 **w02** (shell emulator, filesystem seed). User review checkpoint.
3. **Rollout** in batches of ~4, ISM2411 w01–w15 then ISM3232 w01–w16, each deck:
   author from guide → self-check (every runnable block executes to the guide's stated
   output; every quiz answer correct) → add lab-page link.
4. **Finish** — bump both submodule pointers in parent; print the 29 Canvas URLs.
