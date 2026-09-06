# Interactive lab-deck authoring recipe

Concrete steps for authoring the remaining **27** interactive lab slide decks. The
framework (Tasks 1–8) and two pilot decks are done:

- Pilots: `ism3232/docs/week02_lab_slides.html`, `ism2411/pages/week03_lab_slides.html`
- Framework: `ism{2411,3232}/assets/lab-slides.{css,js}` + `lab-shell.mjs` +
  `lab-widgets.mjs` + `lab-pyodide.mjs` + `lab-draw.mjs`
- Harness: `ism2411/pages/_lab_slides_harness.html`, `ism3232/docs/_lab_slides_harness.html`

**Decks still to author**

| Course | Weeks | Count |
|---|---|---|
| ISM2411 | w01, w02, w04, w05, w06, w07, w08, w10, w11, w12, w13, w14, w15 | 13 |
| ISM3232 | w01, w03, w04, w05, w06, w07, w08, w10, w11, w12, w13, w14, w15, w16 | 14 |

Deck lives next to the matching lab page: ISM2411 in `pages/`, ISM3232 in `docs/` — both
one level under the submodule root, so `../assets/…` is correct for both. Filename:
`weekNN_lab_slides.html`. **Source of truth is always the facilitation guide**
(`instructor_notes/<course>/lab_wNN.md`); the deck is a rendering of it, not a rewrite.

---

## 1. Deck `<head>` boilerplate

Copy verbatim from a pilot. Only the three `ism3232` / `ism2411` tokens and the `<title>`
change. Load order matters: theme bootstrap IIFE first, reveal + highlight CSS, then
`../assets/lab-slides.css`, then (at end of `<body>`) reveal/highlight/notes scripts, then
`../assets/lab-slides.js` **as `type="module"`, last**.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<script>
(function(){var t=localStorage.getItem('ism3232-theme')||(window.matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light');document.documentElement.setAttribute('data-theme',t)})();
</script>
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>ISM3232 Week 2 Lab — zsh Navigation &amp; File Operations</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.6.1/reveal.min.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.6.1/theme/moon.min.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/atom-one-dark.min.css">
<link rel="stylesheet" href="../assets/lab-slides.css">
<style>
/* Deck-local helpers not covered by lab-slides.css — copy the pilot's block verbatim:
   .eyebrow .hint .chip .kv table.grid .expect  (+ .concept.danger / .tmpl for shell decks) */
</style>
</head>
<body>
<div class="reveal"><div class="slides">

<!-- sections here -->

</div></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.6.1/reveal.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.6.1/plugin/highlight/highlight.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.6.1/plugin/notes/notes.min.js"></script>
<script type="module" src="../assets/lab-slides.js"></script>
</body>
</html>
```

For **ISM2411** decks the IIFE key is `'ism2411-theme'`; everything else is identical. Copy
the deck-local `<style>` block from `ism2411/pages/week03_lab_slides.html` (it omits
`.concept.danger` / `.tmpl`, which only shell decks use).

---

## 2. Slide skeleton

One `<section>` per slide, in this order. Every `<section>` carries an
`<aside class="notes">` — see §2a.

```
s-title      course · week · module · unit; timing bar (t-bar / t-item); "← → · F · S · D" hint
s-glance     "Today at a glance" — Format, Prerequisites, Exercises covered, Submission (kv list)
s-obj        Learning objectives (verbatim verbs from the guide)
s-timing     Timing plan table (table.grid) — Time / Segment / Min

  per exercise / part (from the guide's "## Exercise N" / "## Part N"):
  s-sec      section divider — <span class="chip">Part N · time</span> + <h1>
  s-idea     optional — "The idea" concept card (<div class="concept"> … or .concept.danger)
  s-code     runnable <div class="run" …> live-code block + <p class="expect"> note
  s-out      static expected output <pre> …  OR  a <div class="predict"> block
  s-quiz     <div class="quiz" data-answer="…"> knowledge check
  s-warn     "Common pitfalls" / "Common student mistakes" — <div class="warn-card">

  stretch sections   same sub-skeleton, lighter (often idea → code → out only)

s-wrap       Reflection questions (from the guide's Wrap-Up)
s-wrap       Submission checklist + next-module preview
s-end        <div class="sec-n"> + <h1>End of lab</h1>; notes names the source guide
```

A single exercise commonly needs two `s-code` slides (e.g. a broken pass + a fixed pass)
each with its own paired `s-out`. Pair **every** `s-code` with an `s-out` so the deck
teaches fully even if Pyodide never loads (a hard requirement from the spec's risk table).

### 2a. Speaker notes — every section

`<aside class="notes">` must carry, pulled from the guide **verbatim** where the guide
gives wording:

- **Teaching goal** for the segment
- **"Say to the class"** — the guide's script, word for word
- **Line-by-line** walkthrough of the code block
- **Common mistakes** for the segment
- The **check-for-understanding** question *and its answer* (the parenthetical in the
  guide's "Check for understanding")

The `data-answer` on the paired `s-quiz` must be the same answer as that parenthetical.

---

## 3. Component markup snippets

All copied from the two pilots. `div.run` inner text is treated as source — the browser
unescapes it, the framework `.trim()`s it. Do **not** put `<code class="language-*">`
inside a runnable block.

### Runnable Python — `data-lang="python"`

```html
<div class="run" data-lang="python">
# --- Exercise 1 ---
product = "Notebook"
unit_price = 4.99
print(type(product))
</div>
```

Modifiers (space-separated boolean attrs, or `data-stdin`):

- `data-stdin="Notebook&#10;4.99&#10;12"` — pre-fills the stdin box, one value per line
  (`&#10;` = newline). A stdin box also appears automatically if the source contains
  `input(`.
- `data-readonly` — **python:** the source renders as a static, syntax-highlighted
  `<pre>` (no editable textarea) but still gets a **Run** button and an output pane.
  **shell:** static highlighted `<pre>` only — no Run, no prompt, no transcript.
- `data-autorun` — runs once automatically when its slide becomes active. Use sparingly;
  never on a slow (pandas) block. **Python blocks only** — `buildShell` never reads it, so
  `data-autorun` on a `data-lang="shell"` block does nothing.

Broken-then-fixed pattern (ISM2411 w03 Ex 3): two `.run` blocks with the same
`data-stdin`, the first deliberately raising, each with its own `s-out`.

> **Every `.run` python block executes in its OWN fresh namespace.** Blocks do **not**
> share variables: a name defined on slide 4 is gone on slide 9. Each block must be a
> complete, self-contained runnable script — re-do the imports and re-assign any variable
> it uses. (This is deliberate: it keeps a `NameError` demo honest and keeps the
> framework's `__lab_*` helpers out of a `dir()` / `globals()` demo. The *interpreter* is
> still shared, so loaded packages and Pyodide's virtual FS persist across blocks.)

### Runnable shell — `data-lang="shell"` with a seeded FS

```html
<div class="run" data-lang="shell" data-fs='{"~/ism3232/module02_zsh/week2_lab":{"notes.txt":"Week 2 navigation practice\n","week2_script.py":"print(\"Week 2 complete\")\n"}}'>cd ~/ism3232/module02_zsh/week2_lab
touch notes.txt commands.txt
ls -la
echo 'Week 2 navigation practice' > notes.txt
cat notes.txt</div>
```

- `data-fs` is a JSON tree: object = directory, string = file contents. Keys may start
  `~/…`. Escape inner quotes and newlines for JSON (`\"`, `\n`).
- **`data-fs` is a single-quoted HTML attribute holding JSON**, so the seeded file
  contents must survive both layers. A `'` ends the attribute, and `&` / `<` start an
  entity or a tag — any of the three breaks the block (the parse fails silently and the
  shell boots with an empty FS). Keep fixture contents ASCII, quote-free and
  apostrophe-free, or escape them (`&#39;`, `&amp;`, `&lt;`).
- **The emulator always starts cwd at `/Users/student`.** Every shell block must lead with
  a `cd ~/...` to get where the guide's Setup step left the student.
- `python3 <file>` inside the emulator delegates to Pyodide; `git`, `python -m venv`,
  `pip`, `code .` do not really run (see §5, §6).

### Knowledge check — `.quiz`

```html
<div class="quiz" data-answer="B">
  <p class="q">If I write <code>quantity = "12"</code> — with quotes — what does <code>type(quantity)</code> report?</p>
  <button data-opt="A"><code>&lt;class 'int'&gt;</code></button>
  <button data-opt="B"><code>&lt;class 'str'&gt;</code></button>
  <button data-opt="C"><code>SyntaxError</code></button>
  <p class="why" hidden>The quotes make it text, not a number. …</p>
</div>
```

Multi-answer: `data-answer="A,C"` — the widget then renders a **Check** button and grades
the selected set (**Check** with nothing selected is a no-op, not a wrong answer).
`.why` is revealed after answering — always ship it with the `hidden` attribute so it
cannot flash before the widget upgrades the question. Answer letters are matched
case-insensitively against `data-opt`.

### Predict-the-output — `.predict` (a variant of `s-out`)

```html
<section class="s-out">
<h3>Predict</h3>
<div class="predict">
<p>Before running: if you ran <code>tree -L 1</code> instead of <code>-L 2</code>, what changes?</p>
<pre class="answer" hidden>Only the top-level folder names would show — none of their contents.
-L limits how DEEP tree looks, not WHICH folders appear.</pre>
</div>
</section>
```

The hidden `<pre class="answer" hidden>` is revealed by a **Reveal answer** button the
widget injects. **No inner `<code class="language-*">`** inside that `<pre>` (see §6).

### Static expected output — plain `s-out`

```html
<section class="s-out">
<h3>Expected output</h3>
<pre>&lt;class 'str'&gt;
&lt;class 'float'&gt;
&lt;class 'int'&gt;
&lt;class 'bool'&gt;</pre>
<aside class="notes">Run it live; confirm every student sees exactly this.</aside>
</section>
```

---

## 4. Verification rule — before every commit

Every runnable block must be checked against its guide's stated output *before* the deck
is committed. No exceptions.

### Shell blocks

Run the block's commands through the emulator in Node and diff against the guide's
"Verified output":

```bash
cd ism3232
node --input-type=module -e '
import { createShell, run } from "./assets/lab-shell.mjs";
const fs = {"~/ism3232/module02_zsh/week2_lab":{"notes.txt":"Week 2 navigation practice\n"}};
const sh = createShell(fs);
for (const line of [
  "cd ~/ism3232/module02_zsh/week2_lab",
  "ls",
  "cat notes.txt",
]) {
  const r = run(sh, line);
  process.stdout.write((r.out||"") + (r.err||""));
}
'
```

Use the **exact** `data-fs` JSON and the **exact** command lines from the slide. If the
emulator output diverges from the guide, fix the slide (or flag the guide) — never ship a
mismatch.

### Python blocks

Run the block's source through system `python3` (CPython 3.12 == Pyodide 0.26.4) and
compare to the guide's "Expected output" **and** to the text in the paired `s-out` slide:

```bash
printf '%s\n' 'product = "Notebook"' 'print(type(product))' | python3
# for input() blocks, pipe the data-stdin values:
printf 'Notebook\n4.99\n12\n' | python3 the_block.py
```

Tracebacks: the last line (the `TypeError: …` / `ValueError: …`) must match exactly; the
file path differs (`<exec>` in Pyodide vs a temp path under CPython) and is not
load-bearing — say so in the notes, as the w03 pilot does.

### Quizzes

Every `.quiz` `data-answer` must equal the answer in the guide's check-for-understanding
parenthetical for that segment.

---

## 5. Per-course specifics

### ISM2411 — Python/Pyodide throughout, with a shell exception in w01–w02

- `data-lang="python"` is the default for every ISM2411 deck. **w01 and w02 MAY use
  `data-lang="shell"`** for a genuine terminal sequence (the first-week folder/file setup);
  the emulator ships in `ism2411/assets/` too, so it works there identically. Everything
  else — every other week, and any block that is really Python — stays on Pyodide.
- `input()` appears from **w03 on** — those blocks need `data-stdin` seeded with the
  guide's sample answers.
- REPL demos (bare expressions that auto-echo) don't auto-echo in a `.run` block — wrap
  each line in `print(...)` and add an `expect` note explaining the REPL would show quotes
  around strings. (w03 Ex 5 does this.)
- **w12–w15 use pandas / matplotlib.** `runPython` does *not* auto-load packages from
  imports, so `import pandas` fails cold. Add the `data-packages` attribute to the block:

  ```html
  <div class="run" data-lang="python" data-packages="pandas,matplotlib">
  import pandas as pd
  df = pd.read_csv("sales.csv")
  print(df.describe())
  </div>
  ```

  - `data-packages` is a comma-separated Pyodide package list — `"pandas"` or
    `"pandas,matplotlib"`.
  - The Run button's **first** activation shows `loading packages…` and preloads them
    before the code runs. Later Runs of that block skip the load, and every other block
    on the page reuses them (the Pyodide instance is a page singleton) — one
    `data-packages` block early in the deck is enough, but repeating the attribute on
    each data block is harmless and makes a block self-contained.
  - Keep `data-packages` blocks **non-`autorun`** — the first run pays a multi-MB
    download; let the presenter click Run.
  - If the download fails (lab wifi offline), the error shows in the output pane and the
    next Run retries. If load time is prohibitive, fall back to `data-readonly` + a
    paired `s-out` (static text for a table; a committed PNG for a chart).
- **Sample data (embedded CSV):** bundle any CSV inline as a triple-quoted Python
  string and write it to Pyodide's virtual FS at the **top of the block**:

  ```python
  from pathlib import Path

  CSV = """product,price,qty
  Notebook,4.99,12
  Pen,1.99,50
  """
  Path("sales.csv").write_text(CSV)

  import pandas as pd
  df = pd.read_csv("sales.csv")
  print(df)
  ```

- **Charts (matplotlib → PNG):** when `data-packages` includes `matplotlib` the
  framework forces the headless `AGG` backend and, after your code runs, captures any
  open figure to a PNG shown in the output pane — just build the plot, no `plt.show()`
  or `plt.savefig()` needed:

  ```python
  import matplotlib.pyplot as plt

  plt.plot([1, 2, 3], [4, 9, 5])
  plt.title("Sales trend")
  ```

  A block that draws nothing is fine — no figure, no image, no error.

### ISM3232 — w01–w04 shell, w05–w16 Python

- **w01–w04** (`zsh` / git / venv): `data-lang="shell"` with a seeded `data-fs`.
  - `git`, `python -m venv`, `pip install` **cannot run** in the emulator. Show them as
    `data-readonly` static code **with a visible note on the slide** ("shown for
    reference — run this on your own machine"). `data-readonly` on a shell block gives
    exactly that: highlighted source, no Run button, no terminal (§6.1).
  - w03's `.zshrc` / `.venv` content: seed it into `data-fs` so `ls -la` / `cat` show
    something real.
- **w05–w16** Python → same as ISM2411 (`data-lang="python"`, `data-stdin` for `input()`).
- **w14 SQL** — `import sqlite3` works (Pyodide stdlib). Normal `data-lang="python"`
  runnable blocks; seed any `.db` by building it in-script or from an inline SQL string.
- **w15 Streamlit** and **w16 GenAI API calls** cannot run client-side. Those decks use a
  knowledge-check / walkthrough treatment instead of live execution, **called out
  explicitly on the slide** ("this can't run in the browser — walk through it, then run it
  locally"). Note that `data-readonly` on a *python* block still shows a Run button (§3),
  so for code that genuinely cannot run, put it in a plain `<pre><code
  class="language-python">` **outside** any `.run` div rather than in a readonly `.run`.

---

## 6. Known framework limitations — work around these

1. **`data-readonly` behaves differently per language — by design.** On a
   `data-lang="shell"` block it renders the source as a static, syntax-highlighted `<pre>`
   with **no** Run-all button, no prompt line and no emulator transcript — the right
   treatment for `git`, `python -m venv`, `pip` and `code .`, which cannot really run.
   On a `data-lang="python"` block it renders the same static `<pre>` but **keeps** the
   Run button and the output pane (the code is shown, not editable, and still runs).
   *(Resolved — rollout Task 1.)*
2. **`runPython` does not load packages from imports** — `import pandas` fails cold
   unless the package is preloaded. Add `data-packages="pandas,matplotlib"` to the
   block (§5); `buildPython` calls `loadPackages(...)` on the first Run. *(Resolved —
   this was a rollout framework fix.)*
3. **highlight.js emits a benign `console.warn`** if a `.predict` hidden `<pre>` contains
   an inner `<code class="language-*">`. Don't put one there — plain text only inside
   `<pre class="answer" hidden>`.
4. **The zsh emulator's `tree` with no path arg prints the root as `.`** — this is correct
   real `tree` behavior when run from inside the folder. Guide examples that show
   `coursename/` as the root are "illustrative"; label them so in the notes (the w02 pilot
   does).

---

## 7. Lab-page link snippet

In each `weekNN_lab.html`, inside the `.weekjump` bar, immediately **after** the current
`Lab` link, add a `Slides` link (match the surrounding indentation):

```html
<a href="weekNN_lab.html" class="weekjump-link current">Lab</a>
<a href="weekNN_lab_slides.html" class="weekjump-link">Slides</a>
```

ISM3232 example (`docs/week02_lab.html`):

```html
<a href="week02_lab.html" class="weekjump-link current">Lab</a>
<a href="week02_lab_slides.html" class="weekjump-link">Slides</a>
```

ISM2411 example (`pages/week03_lab.html`):

```html
<a href="week03_lab.html" class="weekjump-link current">Lab</a>
<a href="week03_lab_slides.html" class="weekjump-link">Slides</a>
```

---

## 8. Finish steps for the rollout (NOT done now)

After **all 29 decks** exist, each passes its per-deck verification (§4), and a full
browser pass (§9) is clean:

1. In each submodule, commit the decks + lab-page links on the `interactive-lab-slides`
   branch.
2. In the **parent repo** (branch `instructor-lab-guides`), bump both submodule pointers:

   ```bash
   git add ism2411 ism3232
   git commit -m "Bump ism2411 + ism3232: interactive lab slide decks (all weeks)"
   ```

3. Print the list of **29 Canvas URLs** for the user to add manually:

   ```
   https://markumreed.github.io/ism2411/pages/week01_lab_slides.html
   https://markumreed.github.io/ism2411/pages/week02_lab_slides.html
   … w03 … w15
   https://markumreed.github.io/ism3232/docs/week01_lab_slides.html
   https://markumreed.github.io/ism3232/docs/week02_lab_slides.html
   … w03 … w16
   ```

   (ISM2411: w01–w08, w10–w15 → 14. ISM3232: w01–w08, w10–w16 → 15. Total 29.)

Task 9 itself commits only the two lab-page links and this recipe — **no submodule
pointer bump.**

---

## 9. Browser-gate note

The interactive browser walkthrough was **not** run during framework/pilot development
(no Chrome available). Before the rollout starts it must be run **once** against
`_lab_slides_harness.html` and both pilot decks, checking:

- Pyodide actually loads and runs (cold + warm)
- the stdin box feeds `input()` correctly
- the draw overlay toggles on **D** and syncs to the notes popup
- dark / light theme both render correctly (toggle + system)
- the browser console is clean (no errors; the only acceptable warning is highlight.js on
  a malformed `.predict`, which §6 tells you to avoid)

Run it once more over the **full set of 29 decks** at the end, before the pointer bump.
