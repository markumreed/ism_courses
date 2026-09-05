# Interactive Lab Slide Decks Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the shared interactivity layer for interactive reveal.js lab decks and two pilot decks (ISM3232 Week 2, ISM2411 Week 3), ending at a user-review checkpoint before the remaining 27 decks are authored under a follow-on plan.

**Architecture:** A per-course set of static ES-module assets (`lab-slides.js` entry + `lab-shell.mjs`, `lab-pyodide.mjs`, `lab-widgets.mjs`, `lab-draw.mjs`, `lab-slides.css`) is duplicated byte-identically into `ism2411/assets/` and `ism3232/assets/` (the submodules publish separately). Hand-authored `weekNN_lab_slides.html` decks are plain reveal.js HTML that declares components with data-attributes; the entry module upgrades them on `Reveal.ready`. Pure logic (zsh emulator, quiz grading) is unit-tested with `node --test`; browser integration is verified against a component test-harness page with a written checklist.

**Tech Stack:** reveal.js 4.6.1 (CDN, classic script) + highlight/notes plugins, highlight.js 11.9.0, Pyodide 0.26.4 (jsdelivr CDN, lazy), vanilla ES modules, Node 22 `node --test` (built-in, no deps).

**Spec:** `docs/superpowers/specs/2026-09-05-interactive-lab-slides-design.md`

## Global Constraints

- **reveal.js version:** `4.6.1` from `https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.6.1` — match the version already used in `ism3232/docs/week02_slides.html`.
- **Pyodide version:** `0.26.4` from `https://cdn.jsdelivr.net/pyodide/v0.26.4/full/pyodide.js` — pinned exact; lazy-loaded on first Run click only.
- **CDN allowlist:** scripts/styles only from `cdnjs.cloudflare.com` and `cdn.jsdelivr.net` (Pyodide). No other hosts.
- **Framework files are byte-identical across the two submodules** except `lab-slides.css`, which differs only in the accent-color custom properties. Any edit to one copy is applied to the other in the same task.
- **New JS is ES modules** (`.mjs`, or `.js` loaded with `type="module"`). reveal.js and its plugins stay classic scripts (they set the `Reveal` global).
- **File locations:** framework → `ism2411/assets/` and `ism3232/assets/` (flat, alongside existing `assets/`). Decks → `ism2411/pages/weekNN_lab_slides.html` and `ism3232/docs/weekNN_lab_slides.html`.
- **Course accents:** ISM2411 `--accent:#1e40af` (blue, from `ism2411/assets/css/site.css` convention); ISM3232 `--accent:#2dd4bf` (teal `--T`, from `ism3232/docs/week02_slides.html`).
- **Do NOT bump submodule pointers** in the parent repo in this plan. That happens after the pilot-review checkpoint, in the rollout plan.
- **Commits:** commit inside the relevant submodule working tree. Each task ends with a commit. End commit messages with the Co-Authored-By / Claude-Session trailer used elsewhere in this repo's history.
- **Source of truth for deck content** is the matching `instructor_notes/<course>/lab_wNN.md` facilitation guide. Every runnable code block must execute to the output stated in that guide; every quiz's marked answer must be correct per that guide.

---

### Task 1: zsh emulator core (`lab-shell.mjs`)

Pure, framework-free module: an in-memory filesystem plus a command interpreter covering exactly the commands the ISM3232 shell labs use. No DOM. Consumed by the terminal widget (Task 5) and unit-tested directly.

**Files:**
- Create: `ism3232/assets/lab-shell.mjs`
- Create: `ism3232/assets/lab-shell.test.mjs`
- Create (copy): `ism2411/assets/lab-shell.mjs` (identical; shipped to both trees so the framework is uniform even though ISM2411 never seeds a shell)

**Interfaces:**
- Produces:
  - `createShell(seed) -> shell` where `seed` is a nested plain object: keys ending without `/` whose value is a string are files (content); values that are objects are directories. `seed` keys may be absolute-ish paths like `"~/ism3232"`; a single top-level `"~"` is created if absent. `shell` holds `{ cwd: string, home: "/Users/student", history: string[] }` with `cwd` starting at `"~"` expanded to an absolute path under `home` unless the seed's shallowest directory dictates otherwise (default cwd = `"/Users/student"`).
  - `run(shell, line) -> { out: string, err: string, cleared: boolean }` — executes one command line (supports a single `|` pipe and `>` / `>>` redirection). Mutates `shell` (cwd, filesystem, history). `cleared: true` signals the widget to wipe the transcript (`clear`). Never throws on user error — returns `err` text matching real zsh phrasing.
  - `prompt(shell) -> string` — e.g. `"student@MacBook-Pro week2_lab %"` (basename of cwd, or `~` when cwd === home).
  - `listing(shell, path?) -> string[]` — sorted visible entry names at `path` (default cwd); helper for tests and aut\-complete. Not used by decks directly.

**Supported commands** (anything else → `zsh: command not found: <cmd>`):
`pwd`, `ls` (`-l`, `-a`, `-la`/`-al`, path arg), `cd` (`..`, `~`, `-`, relative multi-segment, absolute), `mkdir` (`-p`, multi-arg), `touch` (multi-arg), `cat` (multi-arg, concatenates), `echo` (single/double quotes, `>` and `>>` redirect), `rm` (`-r`, multi-arg), `cp` (`-r`, file→file, file→dir), `mv` (rename, move into dir), `tree` (`-L n`), `head` (`-n N`, default 10), `tail` (`-n N`, default 10), `wc` (`-l`), `clear`, `whoami`, `which <cmd>`, `history`, `code` (stub: prints `(VS Code would open: <arg>)`), `python3 <file>` / `python3 -c "<src>"` (stub in this task: prints `(python3 stub — wired to Pyodide in Task 5)`; Task 5 replaces the stub via an injected runner).

- [ ] **Step 1: Write the failing tests**

Create `ism3232/assets/lab-shell.test.mjs`:

```js
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createShell, run, prompt } from './lab-shell.mjs';

const seed = () => ({
  '~/ism3232': {
    module01_setup: { 'hello_ism3232.py': "print('hi')\n", 'README.md': '# m1\n' },
    module02_zsh: { week2_lab: {} },
    data: {}, screenshots: {},
  },
});

test('pwd starts at home and cd ~ returns there', () => {
  const sh = createShell(seed());
  assert.equal(run(sh, 'pwd').out.trim(), '/Users/student');
  run(sh, 'cd ~/ism3232/module02_zsh/week2_lab');
  assert.equal(run(sh, 'pwd').out.trim(), '/Users/student/ism3232/module02_zsh/week2_lab');
  run(sh, 'cd ~');
  assert.equal(run(sh, 'pwd').out.trim(), '/Users/student');
});

test('mkdir + cd .. + relative multi-segment cd', () => {
  const sh = createShell(seed());
  run(sh, 'cd ~/ism3232/module02_zsh');
  run(sh, 'mkdir week2_lab/practice');            // week2_lab exists
  run(sh, 'cd week2_lab/practice');
  assert.equal(run(sh, 'pwd').out.trim(), '/Users/student/ism3232/module02_zsh/week2_lab/practice');
  run(sh, 'cd ../..');
  assert.equal(run(sh, 'pwd').out.trim(), '/Users/student/ism3232/module02_zsh');
});

test('touch multi-arg then ls and ls -la ordering', () => {
  const sh = createShell(seed());
  run(sh, 'cd ~/ism3232/module02_zsh/week2_lab');
  run(sh, 'touch notes.txt commands.txt hello_week2.py');
  assert.equal(run(sh, 'ls').out.trim(), 'commands.txt  hello_week2.py  notes.txt');
  const la = run(sh, 'ls -la').out;
  assert.match(la, /^total /m);
  assert.match(la, /\.\n/);        // "." entry present
  assert.match(la, /\.\.\n/);      // ".." entry present
});

test('echo > overwrites, echo >> appends, cat concatenates', () => {
  const sh = createShell(seed());
  run(sh, 'cd ~/ism3232/module02_zsh/week2_lab');
  run(sh, "echo 'Week 2 navigation practice' > notes.txt");
  assert.equal(run(sh, 'cat notes.txt').out, 'Week 2 navigation practice\n');
  run(sh, "echo 'extra line' >> notes.txt");
  assert.equal(run(sh, 'cat notes.txt').out, 'Week 2 navigation practice\nextra line\n');
  assert.equal(run(sh, 'wc -l notes.txt').out.trim(), '2 notes.txt');
  assert.equal(run(sh, 'head -1 notes.txt').out, 'Week 2 navigation practice\n');
});

test('cp keeps original, mv does not', () => {
  const sh = createShell(seed());
  run(sh, 'cd ~/ism3232/module02_zsh/week2_lab');
  run(sh, "echo 'x' > notes.txt");
  run(sh, 'cp notes.txt notes_backup.txt');
  assert.match(run(sh, 'ls').out, /notes.txt/);
  assert.match(run(sh, 'ls').out, /notes_backup.txt/);
  run(sh, 'touch hello_week2.py');
  run(sh, 'mv hello_week2.py week2_script.py');
  const ls = run(sh, 'ls').out;
  assert.doesNotMatch(ls, /hello_week2\.py/);
  assert.match(ls, /week2_script\.py/);
});

test('rm is permanent; ls reflects removal', () => {
  const sh = createShell(seed());
  run(sh, 'cd ~/ism3232/module02_zsh/week2_lab');
  run(sh, 'touch a.txt b.txt');
  run(sh, 'rm a.txt');
  assert.equal(run(sh, 'ls').out.trim(), 'b.txt');
  assert.match(run(sh, 'rm missing.txt').err, /no such file or directory/i);
});

test('tree -L limits depth', () => {
  const sh = createShell(seed());
  run(sh, 'cd ~/ism3232');
  const t1 = run(sh, 'tree -L 1').out;
  assert.match(t1, /module01_setup/);
  assert.doesNotMatch(t1, /hello_ism3232\.py/);   // depth 1 hides file inside module01_setup
  const t2 = run(sh, 'tree -L 2').out;
  assert.match(t2, /hello_ism3232\.py/);
});

test('single pipe: ls -la | head -5', () => {
  const sh = createShell(seed());
  run(sh, 'cd ~/ism3232/module02_zsh/week2_lab');
  run(sh, 'touch f1 f2 f3 f4 f5 f6');
  const out = run(sh, 'ls -la | head -5').out;
  assert.equal(out.split('\n').filter(Boolean).length, 5);
});

test('unknown command uses zsh phrasing', () => {
  const sh = createShell(seed());
  assert.equal(run(sh, 'frobnicate x').err.trim(), 'zsh: command not found: frobnicate');
});

test('prompt shows basename or ~', () => {
  const sh = createShell(seed());
  assert.equal(prompt(sh), 'student@MacBook-Pro ~ %');
  run(sh, 'cd ~/ism3232/module02_zsh/week2_lab');
  assert.equal(prompt(sh), 'student@MacBook-Pro week2_lab %');
});
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd ism3232/assets && node --test lab-shell.test.mjs`
Expected: FAIL — `Cannot find module './lab-shell.mjs'`.

- [ ] **Step 3: Implement `lab-shell.mjs`**

Create `ism3232/assets/lab-shell.mjs`. Implement to satisfy every test above:

- Filesystem: a tree of `Map`s (dirs) and strings (files) rooted at `/`. `createShell(seed)` walks `seed`: split each top-level key on `/`, expanding a leading `~` to `/Users/student`; create intermediate dirs; recurse into object values, assign string values as file contents. Always ensure `/Users/student` exists; `shell.home = '/Users/student'`; `shell.cwd = '/Users/student'`.
- Path resolution `resolve(shell, p)`: `~` → home; leading `/` absolute; otherwise join with `cwd`; collapse `.`/`..`; return absolute normalized string. `nodeAt(path)` returns the Map/string or `null`.
- `run(shell, line)`: push raw line to `shell.history`. If line contains ` | `, split into two segments, run left capturing `out`, feed that string as the pipe input to the right (only `head`/`tail`/`wc`/`cat` consume pipe input — enough for the labs). Detect trailing `> file` / `>> file`, strip it, and after producing `out`, write/append `out` to `file` instead of returning it. Tokenize respecting single and double quotes. Dispatch on argv[0] to a per-command function. Each command returns `{out, err}` (strings, `''` when empty); wrapper adds `cleared`.
- `ls`: default sorted visible names joined by two spaces + trailing `\n`; `-a` adds `.`/`..` and dotfiles; `-l`/`-la` long format — synthesize plausible columns: `-rw-r--r--  1 student  staff   <size>  Sep  5 10:00 <name>` for files, `drwxr-xr-x` for dirs, prefixed by a `total N` line; one entry per line.
- `tree`: recursive ASCII (`├──`, `└──`, `│   `), honoring `-L n` (root is level 0; entries at level n shown, their children not). Directory-only sort then files, alphabetical within each. End with a blank line.
- `echo`: join args with spaces; interpret `\n` only inside double quotes is out of scope — treat content literally. Append `\n`.
- `cat`/`head`/`tail`/`wc`: operate on file args OR piped input. `head`/`tail` default 10, `-n N` or `-N` sets count. `wc -l` prints `<count> <name>` (or just `<count>` for piped input); count = number of `\n`.
- `cp`/`mv`: `source dest`. If `dest` is an existing dir, place `basename(source)` inside it; else treat `dest` as the new name. `mv` deletes source; `cp` without `-r` refuses a directory source (`cp: <src>: is a directory`).
- `rm`: refuse a directory without `-r` (`rm: <name>: is a directory`); missing path → `rm: <name>: No such file or directory`.
- `cd -` swaps `cwd` with `shell.prev`; every successful `cd` sets `shell.prev`. Invalid target → `cd: no such file or directory: <arg>` and cwd unchanged.
- `code` → `` `(VS Code would open: ${arg || '.'})\n` ``. `python3` → stub string from the task header. `whoami` → `student\n`. `which x` → `x: aliased to …`? keep simple: `/usr/bin/<x>\n` for known commands, `<x> not found\n` otherwise. `history` → numbered lines from `shell.history`.
- `export` a UMD-free ES `export { createShell, run, prompt, listing }`.

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd ism3232/assets && node --test lab-shell.test.mjs`
Expected: PASS — all tests green.

- [ ] **Step 5: Copy to the ISM2411 tree**

Run: `cp ism3232/assets/lab-shell.mjs ism2411/assets/lab-shell.mjs`
(No test copy needed in ism2411 for this module; Task 2 adds the shared test file there.)

- [ ] **Step 6: Commit (in each submodule)**

```bash
cd ism3232 && git add assets/lab-shell.mjs assets/lab-shell.test.mjs && \
git commit -m "$(printf 'Add zsh emulator core for interactive lab decks\n\nIn-memory filesystem + command interpreter covering the shell\ncommands used in the ISM3232 terminal labs. Pure module, unit\ntested with node --test.\n\nCo-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01PN8CuB5TvVSWeU365mCNnU')"
cd ../ism2411 && git add assets/lab-shell.mjs && \
git commit -m "$(printf 'Add zsh emulator core (shared lab-deck framework)\n\nByte-identical copy of ism3232/assets/lab-shell.mjs so the two\ncourse framework trees stay uniform.\n\nCo-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01PN8CuB5TvVSWeU365mCNnU')"
cd ..
```

---

### Task 2: Quiz + predict grading (`lab-widgets.mjs`)

Pure grading helpers (unit-tested) plus the DOM upgrade functions for `.quiz`, `.predict`, and the shared "expected output" reveal. The DOM functions are exercised in the browser at Task 6; only the pure helpers get `node --test` coverage here.

**Files:**
- Create: `ism3232/assets/lab-widgets.mjs`
- Create: `ism3232/assets/lab-widgets.test.mjs`
- Create (copy): `ism2411/assets/lab-widgets.mjs`, `ism2411/assets/lab-widgets.test.mjs`

**Interfaces:**
- Consumes: nothing.
- Produces:
  - `parseAnswer(spec) -> Set<string>` — `"B"` → `{"B"}`; `"A,C"` / `"A, c"` → `{"A","C"}` (upper-cased, trimmed).
  - `gradeQuiz(spec, chosen) -> { correct: boolean, expected: Set<string>, chosen: Set<string> }` — `chosen` is a string or array; `correct` iff the chosen set equals the expected set.
  - `upgradeQuiz(el)` — wires one `<div class="quiz" data-answer="…">`: buttons `[data-opt]`, a `<p class="why">` (hidden until answered). On click: mark `.chosen`, mark `.right`/`.wrong` on the relevant buttons, reveal `.why`, set `el.dataset.answered`. Multi-answer (`data-answer` has a comma): clicks toggle selection, a **Check** button (created if absent) grades. Idempotent — a second call is a no-op if `el.dataset.wired`.
  - `upgradePredict(el)` — one `<div class="predict">` containing prompt markup + a `<pre class="answer" hidden>`: injects a **Reveal answer ▾** button that unhides the `<pre>` and highlights it via `window.hljs` if present.
  - `upgradeAll(root=document)` — calls `upgradeQuiz`/`upgradePredict` on every matching element under `root`.

- [ ] **Step 1: Write the failing tests**

Create `ism3232/assets/lab-widgets.test.mjs`:

```js
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { parseAnswer, gradeQuiz } from './lab-widgets.mjs';

test('parseAnswer single and multi, case/space insensitive', () => {
  assert.deepEqual([...parseAnswer('B')], ['B']);
  assert.deepEqual([...parseAnswer('A, c')].sort(), ['A', 'C']);
});

test('gradeQuiz single answer', () => {
  assert.equal(gradeQuiz('B', 'B').correct, true);
  assert.equal(gradeQuiz('B', 'A').correct, false);
});

test('gradeQuiz multi answer needs exact set', () => {
  assert.equal(gradeQuiz('A,C', ['A', 'C']).correct, true);
  assert.equal(gradeQuiz('A,C', ['C', 'A']).correct, true);
  assert.equal(gradeQuiz('A,C', ['A']).correct, false);
  assert.equal(gradeQuiz('A,C', ['A', 'B', 'C']).correct, false);
});
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd ism3232/assets && node --test lab-widgets.test.mjs`
Expected: FAIL — module not found.

- [ ] **Step 3: Implement `lab-widgets.mjs`**

Write `parseAnswer` and `gradeQuiz` as pure functions (set equality). Then the DOM upgraders below `if (typeof document !== 'undefined')` guards are unnecessary — the functions simply reference `document`/`window` only when called. Implement `upgradeQuiz`, `upgradePredict`, `upgradeAll` per the Interfaces block. Use `classList`, `hidden`, `dataset`; no framework. Guard every `el` lookup for null so a malformed deck slide degrades to plain text rather than throwing. `export` all five names.

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd ism3232/assets && node --test lab-widgets.test.mjs`
Expected: PASS.

- [ ] **Step 5: Copy to ISM2411 tree**

Run: `cp ism3232/assets/lab-widgets.mjs ism2411/assets/lab-widgets.mjs && cp ism3232/assets/lab-widgets.test.mjs ism2411/assets/lab-widgets.test.mjs`

- [ ] **Step 6: Run the full asset test suite in both trees**

Run: `cd ism3232/assets && node --test && cd ../../ism2411/assets && node --test && cd ../..`
Expected: PASS in both.

- [ ] **Step 7: Commit (both submodules)**

```bash
cd ism3232 && git add assets/lab-widgets.mjs assets/lab-widgets.test.mjs && \
git commit -m "$(printf 'Add quiz + predict widgets for interactive lab decks\n\nPure grading helpers (unit tested) plus DOM upgraders for\n.quiz / .predict slide components.\n\nCo-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01PN8CuB5TvVSWeU365mCNnU')"
cd ../ism2411 && git add assets/lab-widgets.mjs assets/lab-widgets.test.mjs && \
git commit -m "$(printf 'Add quiz + predict widgets (shared lab-deck framework)\n\nCo-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01PN8CuB5TvVSWeU365mCNnU')"
cd ..
```

---

### Task 3: Python run harness (`lab-pyodide.mjs`)

Lazy Pyodide loader + a `runPython` that captures stdout/stderr and feeds `input()` from a queue. No `node --test` (Pyodide is browser wasm) — verified in the browser at Task 6, and its contract is frozen here so Tasks 5–8 can rely on it.

**Files:**
- Create: `ism3232/assets/lab-pyodide.mjs`
- Create (copy): `ism2411/assets/lab-pyodide.mjs`

**Interfaces:**
- Consumes: nothing.
- Produces:
  - `pyReady() -> Promise<Pyodide>` — idempotent singleton. First call injects `https://cdn.jsdelivr.net/pyodide/v0.26.4/full/pyodide.js`, calls `loadPyodide({indexURL})`, caches the promise. Concurrent callers share it.
  - `runPython(code, { stdin = [], onStatus } = {}) -> Promise<{ stdout: string, stderr: string, ok: boolean }>` — awaits `pyReady()` (calling `onStatus('loading')` then `onStatus('ready')` around a cold start), redirects `sys.stdout`/`sys.stderr` to buffers via `pyodide.setStdout`/`setStderr`, overrides `builtins.input` with a JS function that shifts the next line off a copy of `stdin`, echoes `prompt + value + "\n"` to the stdout buffer, and returns it; raises `EOFError` if the queue is empty. Runs `await pyodide.runPythonAsync(code)`. On a Python exception, `ok:false` and `stderr` gets `pyodide` 's formatted traceback (no JS frames). Always restores the default streams/`input` in a `finally`.
  - `loadPackages(names) -> Promise<void>` — `await pyReady()` then `pyodide.loadPackage(names)` (used by ISM2411 w12–w15 for `pandas`, `matplotlib`; not exercised by the pilots).

- [ ] **Step 1: Implement `lab-pyodide.mjs`**

Write the module per the Interfaces block. Key details:
- Guard the CDN `<script>` injection so it only happens once (check `window.loadPyodide`).
- `indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.26.4/full/'`.
- stdout/stderr capture: prefer `pyodide.setStdout({ batched: s => { buf += s; } })`; fall back to reassigning `sys.stdout` with a Python shim if unavailable in this version.
- `input` override:
  ```js
  const queue = [...stdin];
  pyodide.globals.set('__js_input', (promptStr) => {
    if (!queue.length) throw new Error('EOFError');
    const v = queue.shift();
    stdoutBuf += (promptStr ?? '') + v + '\n';
    return v;
  });
  await pyodide.runPythonAsync(
    'import builtins,js\nbuiltins.input = lambda p="" : js.__js_input(p)\n'
  );
  ```
  Translate the thrown `EOFError` into a Python-visible `EOFError` by wrapping the user `code` run in `try/except EOFError` is not needed — let it surface as a traceback; that matches the guide's teaching intent (a missing `input` line is a real error).

- [ ] **Step 2: Smoke-check syntax**

Run: `node --check ism3232/assets/lab-pyodide.mjs`
Expected: no output, exit 0 (valid ES module syntax; it won't run Pyodide under Node, that's fine).

- [ ] **Step 3: Copy to ISM2411 tree**

Run: `cp ism3232/assets/lab-pyodide.mjs ism2411/assets/lab-pyodide.mjs`

- [ ] **Step 4: Commit (both submodules)**

```bash
cd ism3232 && git add assets/lab-pyodide.mjs && \
git commit -m "$(printf 'Add lazy Pyodide run harness for interactive lab decks\n\nSingleton loader + runPython with stdout/stderr capture and an\ninput() queue shim. Verified in the browser harness (Task 6).\n\nCo-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01PN8CuB5TvVSWeU365mCNnU')"
cd ../ism2411 && git add assets/lab-pyodide.mjs && \
git commit -m "$(printf 'Add lazy Pyodide run harness (shared lab-deck framework)\n\nCo-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01PN8CuB5TvVSWeU365mCNnU')"
cd ..
```

---

### Task 4: Instructor drawing overlay (`lab-draw.mjs`)

Port the existing overlay from `ism3232/docs/week02_slides.html` (the "Draw overlay v3" IIFE) into a reusable ES module.

**Files:**
- Create: `ism3232/assets/lab-draw.mjs`
- Create (copy): `ism2411/assets/lab-draw.mjs`

**Interfaces:**
- Consumes: `window.Reveal` (global, already initialized).
- Produces: `initDraw({ accent = '#2dd4bf' } = {})` — one call sets up the fixed canvas overlay, the bottom-right toolbar, the **D** keyboard toggle, per-slide stroke storage keyed by `Reveal.getState().indexh + ',' + indexv`, and `BroadcastChannel('ismlab_draw')` sync to the notes popup. No-op (returns early) if `matchMedia('print').matches` or the reveal `?print-pdf` query is present. Idempotent via a `window.__labDrawInit` guard.

- [ ] **Step 1: Extract and adapt**

Copy the `Draw overlay v3` IIFE from `ism3232/docs/week02_slides.html` (lines beginning `/* Draw overlay v3 */`) into `lab-draw.mjs`. Changes:
- Wrap in `export function initDraw(opts = {}) { … }` instead of an auto-running IIFE.
- Replace the hard-coded channel `'ism3232_draw_v3'` with `'ismlab_draw'`.
- Replace the yellow default and the palette's course-tinted entries so the first swatch is `opts.accent || '#2dd4bf'`.
- Add the `window.__labDrawInit` guard and the print-export early return.
- Keep the BroadcastChannel receive/redraw logic and the toolbar DOM verbatim.

- [ ] **Step 2: Smoke-check syntax**

Run: `node --check ism3232/assets/lab-draw.mjs`
Expected: exit 0.

- [ ] **Step 3: Copy to ISM2411 tree**

Run: `cp ism3232/assets/lab-draw.mjs ism2411/assets/lab-draw.mjs`

- [ ] **Step 4: Commit (both submodules)**

```bash
cd ism3232 && git add assets/lab-draw.mjs && \
git commit -m "$(printf 'Port drawing overlay into reusable lab-draw module\n\nExtracts the week02_slides.html draw overlay v3 into initDraw();\nchannel renamed ismlab_draw, accent parameterised, print-export\nguarded.\n\nCo-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01PN8CuB5TvVSWeU365mCNnU')"
cd ../ism2411 && git add assets/lab-draw.mjs && \
git commit -m "$(printf 'Port drawing overlay into reusable lab-draw module (shared)\n\nCo-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01PN8CuB5TvVSWeU365mCNnU')"
cd ..
```

---

### Task 5: Framework entry (`lab-slides.js`) + theme (`lab-slides.css`)

The `type="module"` entry a deck loads last. It initializes reveal.js, then on `ready` upgrades every component and starts the drawing overlay. The CSS defines the slide-type classes and every component's look, in both light and dark, sized for 1180×760 projection.

**Files:**
- Create: `ism3232/assets/lab-slides.js`
- Create: `ism3232/assets/lab-slides.css`
- Create (copy, then edit accent): `ism2411/assets/lab-slides.js` (identical), `ism2411/assets/lab-slides.css` (accent only)

**Interfaces:**
- Consumes: `createShell, run, prompt` from `./lab-shell.mjs`; `runPython` from `./lab-pyodide.mjs`; `upgradeAll` from `./lab-widgets.mjs`; `initDraw` from `./lab-draw.mjs`; `window.Reveal`, `window.RevealHighlight`, `window.RevealNotes` (classic CDN scripts loaded before this module).
- Produces:
  - Auto-runs on import: `Reveal.initialize({ width:1180, height:760, margin:0.06, hash:true, slideNumber:'c/t', transition:'fade', plugins:[RevealHighlight, RevealNotes] })` then `Reveal.on('ready', bootstrap)`.
  - `bootstrap()` — calls `upgradeAll(document)`, `upgradeRunners(document)`, `initDraw({ accent })` where `accent` is read from `getComputedStyle(document.documentElement).getPropertyValue('--accent')`.
  - `upgradeRunners(root)` — for each `<div class="run">`: read `dataset.lang` (`python`|`shell`), the original text content (trimmed, HTML-unescaped) as the source; build the widget:
    - **shell**: parse `dataset.fs` (JSON) → `createShell(seed)`; render a terminal transcript, a prompt line with a text input, and a **Run all** button that executes the seeded script lines in order. Each entered line → `run(shell, line)`; append prompt+line+out+err to the transcript; on `cleared` wipe it. Wire `python3` by injecting a runner that calls `runPython` (so `python3 x.py` in the emulator executes the file's stored contents via Pyodide and streams stdout back into the transcript).
    - **python**: render a `<textarea>` seeded with the source (tab inserts two spaces), a **Run ▶** button, an output `<pre>`, and — only if the source matches `/\binput\s*\(/` — a **stdin** `<textarea>` above the button. Run → `runPython(editor.value, { stdin: stdinLines, onStatus })`; show `stdout`, then `stderr` in a red block; `onStatus('loading')` swaps the button label to `starting Python…` and disables it. A **reset** link restores the seeded source. `data-autorun` runs once on first slide-enter; `data-readonly` omits the textarea.
  - Idempotency: mark each upgraded node `dataset.wired = '1'` and skip if already set (reveal fires `ready` once, but decks may re-enter slides).

- [ ] **Step 1: Write `lab-slides.css`**

Adapt the theme block from `ism3232/docs/week02_slides.html` (the `:root` custom props, `.reveal h1/h2/h3/p/ul/code/pre`, the `s-title/s-sec/s-point/s-code` backgrounds, `.concept`, `.warn-card`, `.two-col`, the `@media(max-width:600px)` block). Add:
- `:root{ --accent:#2dd4bf; }` and use `var(--accent)` wherever `--T` was hard-referenced for headings/rules.
- Section classes from the spec: `.s-title .s-glance .s-obj .s-timing .s-sec .s-idea .s-code .s-out .s-quiz .s-warn .s-wrap .s-end` (backgrounds/accents; `.s-out` green-tinted, `.s-warn` amber-tinted, `.s-quiz` indigo-tinted).
- `.run` component: bordered rounded container; `.run textarea` monospace 15px, min-height 6em, full width, dark bg; `.run .bar` flex row for buttons; `.run .out` monospace, pre-wrap, min-height 3em, `.run .out .err` red; `.run .status` muted italic; terminal variant `.run.shell .term` scrollable 40vh, `.run.shell .cli` prompt+input row.
- `.quiz` component: `.quiz button` block-level choices with hover; `.quiz button.right` green, `.quiz button.wrong` red, `.quiz .why` hidden by default, shown via `.quiz.answered .why`.
- `.predict .answer[hidden]` stays hidden; `.predict .reveal-btn` styled like a quiz choice.
- Print guard: `@media print { #labdraw-canvas, #labdraw-toolbar { display:none !important; } }`.

- [ ] **Step 2: Write `lab-slides.js`**

Implement per the Interfaces block. Keep it one file, ~200 lines. Use `DOMParser`-free plain `document.createElement`. HTML-unescape the seeded source with `el.textContent` (already unescaped by the browser). For the shell `python3` wiring, give `createShell` result an optional `shell.pythonRunner = async (src) => (await runPython(src)).stdout` and have `lab-shell.mjs`'s `python3` branch call it when present (add that hook in this task — a 3-line change to `lab-shell.mjs` plus a test).

- [ ] **Step 3: Add + test the `pythonRunner` hook in `lab-shell.mjs`**

Add to `ism3232/assets/lab-shell.test.mjs`:

```js
test('python3 uses injected pythonRunner when set', async () => {
  const sh = createShell(seed());
  sh.pythonRunner = async () => 'Week 2 complete\n';
  run(sh, 'cd ~/ism3232/module02_zsh/week2_lab');
  run(sh, 'touch week2_script.py');
  const r = run(sh, 'python3 week2_script.py');
  // when a runner is present, run() returns a Promise-like marker the widget awaits
  assert.ok(r.async instanceof Promise);
  assert.equal((await r.async).out, 'Week 2 complete\n');
});
```

Implement: when `argv[0] === 'python3'` and `shell.pythonRunner` is set, return `{ out:'', err:'', async: shell.pythonRunner(fileContents).then(out => ({ out, err:'' })) }`. The widget checks for `.async` and awaits it. Without a runner, keep the stub string. Re-run `node --test` in both trees; copy the updated `lab-shell.mjs` to `ism2411/assets/`.

- [ ] **Step 4: Copy JS to ISM2411, create its CSS with the blue accent**

Run: `cp ism3232/assets/lab-slides.js ism2411/assets/lab-slides.js`
Then create `ism2411/assets/lab-slides.css` as a copy of the ISM3232 one with `--accent:#1e40af` and, if the ISM3232 file hard-codes any teal hex outside `--accent`, swap those to `var(--accent)` in both files so the copy stays a pure accent swap.

- [ ] **Step 5: Syntax + unit checks**

Run: `node --check ism3232/assets/lab-slides.js && node --check ism2411/assets/lab-slides.js && cd ism3232/assets && node --test && cd ../../ism2411/assets && node --test && cd ../..`
Expected: exit 0; all unit tests PASS.

- [ ] **Step 6: Commit (both submodules)**

```bash
cd ism3232 && git add assets/lab-slides.js assets/lab-slides.css assets/lab-shell.mjs assets/lab-shell.test.mjs && \
git commit -m "$(printf 'Add lab-deck framework entry + theme\n\nlab-slides.js: reveal init + component upgrade (run/quiz/predict/\ndraw). lab-slides.css: slide-type + component styling, light/dark.\npython3 in the zsh emulator now delegates to an injected Pyodide\nrunner.\n\nCo-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01PN8CuB5TvVSWeU365mCNnU')"
cd ../ism2411 && git add assets/lab-slides.js assets/lab-slides.css assets/lab-shell.mjs && \
git commit -m "$(printf 'Add lab-deck framework entry + theme (ISM2411 accent)\n\nCo-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01PN8CuB5TvVSWeU365mCNnU')"
cd ..
```

---

### Task 6: Component test-harness deck + browser verification gate

One deck per submodule that exercises every component. This is the integration gate: run through the checklist in a browser before authoring real decks.

**Files:**
- Create: `ism3232/docs/_lab_slides_harness.html`
- Create: `ism2411/pages/_lab_slides_harness.html`

**Interfaces:**
- Consumes: everything from Task 5.

- [ ] **Step 1: Write `ism3232/docs/_lab_slides_harness.html`**

A minimal reveal.js page: the CDN `<link>`s (reveal 4.6.1 core + theme, highlight atom-one-dark), `<link rel="stylesheet" href="../assets/lab-slides.css">`, a `.reveal>.slides` with one `<section>` per component:
1. `s-title` — title + timing bar + `← → · F · S · D` hint.
2. `s-code` with `<div class="run" data-lang="python">` containing `print(2+2)` and a `<aside class="notes">` sample.
3. `s-code` with `<div class="run" data-lang="python">` containing a 2-line `input()` program + expect stdin box to appear.
4. `s-code` with `<div class="run" data-lang="shell" data-fs='{"~/demo":{"a.txt":"hello\n"}}'>` containing `pwd` / `ls` / `cat a.txt`.
5. `s-quiz` with a single-answer `.quiz` and a multi-answer `.quiz`.
6. `s-out` with a `.predict` (hidden `<pre>` + reveal button).
7. `s-warn` sample card.
Then the classic CDN `<script>`s for reveal + highlight + notes plugins, then `<script type="module" src="../assets/lab-slides.js"></script>`.

- [ ] **Step 2: Write `ism2411/pages/_lab_slides_harness.html`**

Same, with `../assets/` paths (pages/ is one level under the submodule root, same as docs/), the blue accent inherited from its `lab-slides.css`, and the shell slide omitted or left in (harmless — ISM2411 ships `lab-shell.mjs` too).

- [ ] **Step 3: Serve and verify in a browser**

Run: `cd ism3232 && python3 -m http.server 8747` (and separately for `ism2411` on 8748). Open `http://localhost:8747/docs/_lab_slides_harness.html`.

Verification checklist — all must pass:
- [ ] Deck loads, arrow keys navigate, **F** fullscreen, **S** opens speaker-notes window.
- [ ] Python slide: **Run ▶** shows `starting Python…`, then after the cold start prints `4`. Second Run is instant.
- [ ] `input()` slide: a stdin box is present; entering two lines and Running feeds them; prompt text + values echo in the output; emptying the box and Running produces an `EOFError` traceback (not a JS error).
- [ ] Shell slide: `pwd` → `/Users/student/demo`; `ls` → `a.txt`; `cat a.txt` → `hello`; an unknown command → `zsh: command not found: …`; **Run all** replays the seeded lines.
- [ ] Single-answer quiz: wrong choice → red + `.why` shown; right choice → green. Multi-answer quiz: needs the exact set via **Check**.
- [ ] Predict slide: **Reveal answer** unhides the `<pre>` and it's syntax-highlighted.
- [ ] Press **D**: toolbar appears, can draw over the slide, strokes persist per slide, mirror into the notes window; **D** again hides it.
- [ ] Add `?print-pdf` to the URL: the draw overlay does not appear.
- [ ] Toggle OS dark/light: both themes are legible.
- [ ] DevTools console: no errors (a blocked-Pyodide network failure is acceptable only if offline — note it).

- [ ] **Step 4: Fix any failures**

Any checklist failure is fixed in the Task 1–5 file it belongs to, re-running that task's `node --test` / `node --check`, then re-verifying. Copy any framework edit to the other submodule tree.

- [ ] **Step 5: Commit (both submodules)**

```bash
cd ism3232 && git add docs/_lab_slides_harness.html && \
git commit -m "$(printf 'Add lab-deck component test harness\n\nOne page exercising every interactive component; browser\nverification checklist for the framework.\n\nCo-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01PN8CuB5TvVSWeU365mCNnU')"
cd ../ism2411 && git add pages/_lab_slides_harness.html && \
git commit -m "$(printf 'Add lab-deck component test harness (ISM2411)\n\nCo-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01PN8CuB5TvVSWeU365mCNnU')"
cd ..
```

---

### Task 7: Pilot deck — ISM3232 Week 2 (`week02_lab_slides.html`)

Hand-author the first shell-based deck from the guide, verifying every terminal block against the emulator.

**Files:**
- Create: `ism3232/docs/week02_lab_slides.html`
- Read: `instructor_notes/ism3232/lab_w02.md` (content source)
- Reference: `ism3232/docs/_lab_slides_harness.html` (markup patterns), `docs/superpowers/specs/2026-09-05-interactive-lab-slides-design.md` (deck skeleton)

**Interfaces:**
- Consumes: the Task 5 framework via `../assets/lab-slides.{css,js}`.

- [ ] **Step 1: Build the deck shell**

Copy the `<head>` + CDN links + closing `<script>` block from `_lab_slides_harness.html`. `<title>ISM3232 Week 2 Lab — zsh Navigation &amp; File Operations</title>`. Add the theme bootstrap `<script>` line from `ism3232/docs/week02_slides.html` (the `localStorage 'ism3232-theme'` IIFE) so it matches the site.

- [ ] **Step 2: Author the fixed front slides**

From `lab_w02.md`:
- `s-title`: eyebrow `ISM3232 · Week 2 · Module 02 · Unit 1`, `<h1>zsh Navigation &amp; File Operations</h1>`, timing bar from the Timing Plan table (6 items), hint line. `<aside class="notes">` = the Session Snapshot prose paragraph.
- `s-glance`: a `.kv` list — Format "Live terminal code-along", Prerequisites, Parts covered, Submission — from the Session Snapshot table.
- `s-obj`: the 5 Learning Objectives as `<ul>`. Notes: "By the end of class students should do each of these without hesitation."
- `s-timing`: the Timing Plan table as `<table class="grid">`. Notes: the paragraph under the table.

- [ ] **Step 3: Author Part 1 — Navigation**

- `s-sec` divider: chip `Part 1 · 0:04–0:20`, `<h1>Navigation</h1>`. Notes: Teaching goal + "Say to the class" verbatim.
- `s-idea`: a `.concept` card — "Make `pwd` your reflex in any unfamiliar terminal." Notes: the `pwd`/`ls` and `ls -la` hidden-files explanation bullets.
- `s-code` with a runnable shell block seeded to the state after Setup (`week2_lab` exists under `module02_zsh`, plus the sibling module folders and `module01_setup`'s two files so `tree -L 2` matches the guide's example):
  ```html
  <div class="run" data-lang="shell" data-fs='{"~/ism3232":{"module01_setup":{"hello_ism3232.py":"print(\"hi\")\n","README.md":"# m1\n"},"module02_zsh":{"week2_lab":{}},"data":{},"screenshots":{},"module03_git_github":{},"module04_programming":{},"module05_functions":{},"module06_oop":{},"module07_final_project":{}}}'>
  pwd
  ls
  ls -la
  cd ..
  pwd
  cd ~/ism3232
  tree -L 2
  cd module02_zsh/week2_lab
  pwd
  </div>
  ```
  Notes: the full line-by-line explanation.
- `s-out`: `.predict` — "Before running: what does `tree -L 1` show that `tree -L 2` doesn't?" hidden answer = the guide's parenthetical.
- `s-quiz` (`data-answer="A"`): "From `~/ism3232/module02_zsh/week2_lab`, shortest `cd` to `~/ism3232/module01_setup`?" A `cd ../../module01_setup`  B `cd ../module01_setup`  C `cd module01_setup`. `.why` = the guide's answer.
- `s-warn`: the three "Common student mistakes" bullets in a `.warn-card`.

- [ ] **Step 4: Author Part 2 — File Operations**

- `s-sec` divider `Part 2 · 0:20–0:38`, `<h1>File Operations</h1>`. Notes: Teaching goal + say-to-class.
- `s-code` runnable shell, seeded to the end-of-Part-1 state (cwd `week2_lab`):
  ```
  touch notes.txt commands.txt hello_week2.py
  ls -la
  echo 'Week 2 navigation practice' > notes.txt
  cat notes.txt
  head -1 notes.txt
  cp notes.txt notes_backup.txt
  mv hello_week2.py week2_script.py
  ls -la
  ```
  Notes: the line-by-line explanation, including the `>` overwrite warning.
- `s-idea` `.concept`: "`>` replaces a file's contents — silent overwrite. `cp` keeps the original; `mv` does not." Notes: the cp-vs-mv contrast bullets.
- `s-quiz` (`data-answer="B"`): "After `mv hello_week2.py week2_script.py`, what does `ls` show?" A both files  B only `week2_script.py`  C only `hello_week2.py`. `.why` from the guide.
- `s-warn`: the Part 2 mistakes bullets.
- `s-code` (`data-readonly`): the VS Code workspace step (`cd ~/ism3232/module02_zsh` / `code .`) with a note that `code` opens the whole folder as a workspace.

- [ ] **Step 5: Author Part 3 — Safe File Deletion**

- `s-sec` divider `Part 3 · 0:38–0:53`, `<h1>Safe File Deletion</h1>`. Notes: Teaching goal + the full "Say to the class" ritual paragraph.
- `s-idea` `.concept` (accent-red): "Before every `rm`: `pwd`, then `ls`. No Trash. No undo." 
- `s-code` runnable shell seeded to end-of-Part-2 state (files `commands.txt notes.txt notes_backup.txt week2_script.py`):
  ```
  pwd
  ls
  rm notes_backup.txt
  ls
  ```
  Notes: the line-by-line ritual explanation; expected final `ls` has exactly `commands.txt notes.txt week2_script.py`.
- `s-quiz` (`data-answer="C"`): "Why does the ritual need *both* `pwd` and `ls`?" A `pwd` is enough  B `ls` is enough  C each catches a different failure mode. `.why` = the guide's answer.
- `s-warn`: the Part 3 mistakes bullets (skipping the ritual; careless wildcards; `rm` on a directory).

- [ ] **Step 6: Author Part 4 + Stretch**

- `s-sec` divider `Part 4 · 0:53–1:08`, `<h1>Command Reference README</h1>`. Notes: Teaching goal + say-to-class.
- `s-code` (`data-readonly`, `data-lang="shell"`): `cd ~/ism3232/module02_zsh` / `touch README.md` / `code README.md`, then a second `s-code` (`data-readonly`, no lang, plain `<pre>`) showing the Markdown table template. Notes: the table-syntax and "12 commands" explanation.
- `s-quiz` (`data-answer="B"`): "The '12 commands' minimum is really asking you to…" A pad the list  B document everything you actually did  C only list Part 1–3 commands. `.why` from the guide.
- `s-sec` divider `Stretch · 1:08–1:15`, `<h1>Pipes &amp; Redirect</h1>`. Notes: "Genuine bonus — full attention only if time allows."
- `s-code` runnable shell seeded to end-of-Part-3 state:
  ```
  ls -la | head -5
  echo 'extra line' >> notes.txt
  cat notes.txt
  wc -l notes.txt
  ```
  Notes: the pipe and `>>`-vs-`>` explanations.
- `s-out` `.predict`: "Before running `cat notes.txt` after the append — how many lines?" answer: two (original + appended).

- [ ] **Step 7: Author wrap-up**

- `s-wrap`: "Submission checklist" — the 6 checklist items as `<ul>`. Notes: none.
- `s-wrap`: "Next week" — the Week 3 preview sentence. Notes: none.
- `s-end`: `<div class="sec-n">ISM3232 · Week 2</div><h1>End of lab</h1>`.

- [ ] **Step 8: Verify every runnable block against the emulator**

For each `data-lang="shell"` block, run its lines through the emulator in a scratch Node script and confirm the output matches the guide's "Verified output" / "Verified example output":

```bash
node -e '
import("./ism3232/assets/lab-shell.mjs").then(({createShell,run})=>{
  const fs = /* paste the data-fs JSON for the Part 2 block */;
  const sh = createShell(fs); sh.cwd = "/Users/student/ism3232/module02_zsh/week2_lab";
  for (const line of `touch notes.txt commands.txt hello_week2.py
echo (quotes) Week 2 navigation practice (quotes) > notes.txt
cat notes.txt
head -1 notes.txt
cp notes.txt notes_backup.txt
mv hello_week2.py week2_script.py
ls`.split("\n")) { const r = run(sh, line); process.stdout.write(r.out + r.err); }
});
'
```
Expected: `cat`/`head` print `Week 2 navigation practice` twice; final `ls` = `commands.txt  notes.txt  notes_backup.txt  week2_script.py`. Fix the deck's seed or the emulator (re-running Task 1 tests) until every block matches its guide output.

- [ ] **Step 9: Browser check**

Serve `ism3232` (`python3 -m http.server 8747`), open `docs/week02_lab_slides.html`, walk every slide: each shell block **Run all** produces the guide's output; each quiz's stated answer grades correct; **S** shows the facilitation notes; **D** draws. No console errors.

- [ ] **Step 10: Commit**

```bash
cd ism3232 && git add docs/week02_lab_slides.html && \
git commit -m "$(printf 'Add ISM3232 Week 2 interactive lab deck (pilot)\n\nzsh navigation & file operations, authored from the Week 2\nfacilitation guide. Runnable terminal blocks (in-browser zsh\nemulator), predict/quiz checks, speaker notes carry the\nfacilitation detail.\n\nCo-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01PN8CuB5TvVSWeU365mCNnU')" && cd ..
```

---

### Task 8: Pilot deck — ISM2411 Week 3 (`week03_lab_slides.html`)

Hand-author the first Pyodide deck, including the `input()` two-pass failure demo.

**Files:**
- Create: `ism2411/pages/week03_lab_slides.html`
- Read: `instructor_notes/ism2411/lab_w03.md`
- Reference: `ism2411/pages/_lab_slides_harness.html`

**Interfaces:**
- Consumes: the Task 5 framework via `../assets/lab-slides.{css,js}`.

- [ ] **Step 1: Build the deck shell**

Head + CDN links + closing scripts from `_lab_slides_harness.html`. `<title>ISM2411 Lab Week 3 — Product Pricer with f-strings</title>`. Add the `ism2411-theme` bootstrap IIFE line (copy from any `ism2411/pages/*.html`).

- [ ] **Step 2: Author the fixed front slides**

From `lab_w03.md`:
- `s-title`: eyebrow `ISM2411 · Week 3 · Module 03 · Unit 1 · Foundations`, `<h1>Product Pricer with f-strings</h1>`, timing bar (Intro / Ex1–5 / Stretch A / Wrap from the segment headers' time ranges), hint line. Notes = the Session Snapshot prose.
- `s-glance`: `.kv` — Format "Live code-along", Prerequisites, Exercises covered "1–5 + Stretch A/B", Submission "`pricer.py` to Canvas".
- `s-obj`: the 5 Learning Objectives.
- `s-timing`: derive a small table from the segment headings (Intro 0:00–0:05, Ex1 0:05–0:13, … Stretch A 0:55–1:10) — 8 rows.

- [ ] **Step 3: Author Intro + Exercise 1**

- `s-sec` divider `Intro · 0:00–0:05`, `<h1>Every value has a type</h1>`. Notes: the "Say to the class" paragraph.
- `s-sec` divider `Exercise 1 · 8 min`, `<h1>Variables and Types</h1>`. Notes: Teaching goal + say-to-class.
- `s-code` runnable python:
  ```html
  <div class="run" data-lang="python">
  # --- Exercise 1 ---
  product = "Notebook"
  unit_price = 4.99
  quantity = 12
  in_stock = True
  print(type(product))
  print(type(unit_price))
  print(type(quantity))
  print(type(in_stock))
  </div>
  ```
  Notes: the full line-by-line explanation.
- `s-out`: static `<pre>` of the expected output (`<class 'str'>` …). Notes: "Run it live; confirm every student sees exactly this."
- `s-quiz` (`data-answer="B"`): "`quantity = \"12\"` (with quotes) — what does `type(quantity)` report?" A `<class 'int'>`  B `<class 'str'>`  C `SyntaxError`. `.why` = the guide's check-for-understanding answer, incl. the link to Exercise 3.
- `s-warn`: the three Exercise 1 mistakes bullets.

- [ ] **Step 4: Author Exercises 2–4**

For each: `s-sec` divider (chip + headline from the guide), a runnable `s-code` block with the guide's "Live-code this" source, an `s-out` static expected-output slide, an `s-quiz` from the check-for-understanding prompt, an `s-warn` from the mistakes list. Notes carry teaching goal + say-to-class + line-by-line.

- Exercise 2 — f-string inline compute. Quiz (`data-answer="C"`): "If `unit_price` were `5`, what does `{unit_price * quantity:.2f}` print?" A `60`  B `5`  C `60.00`.
- Exercise 3 — **input(), two passes.** First `s-code` is the *broken* version with a `data-stdin` seed (`Notebook`, `4.99`, `12`) — running it produces `TypeError: can't multiply sequence by non-int of type 'str'`; the `s-out` slide shows that traceback and the notes explain it "out loud, slowly". Then a second `s-code` with the fixed `float()/int()` version and the same stdin, and an `s-out` showing `12 units of Notebook at $4.99 each = $59.88`. Quiz (`data-answer="A"`): "Forget to convert `unit_price` to float — exact error type?" A `TypeError`  B `ValueError`  C no error, wrong output.
  - The stdin seed goes in the deck as: put the three input lines as the initial text of the widget's stdin box — supported by `lab-slides.js` reading a `data-stdin` attribute (newline-joined). Add `data-stdin="Notebook&#10;4.99&#10;12"` support to `upgradeRunners` in Task 5 if not already present — small addition; if discovered here, fix in Task 5's file and re-run its checks.
- Exercise 4 — multi-variable product card. Quiz (`data-answer="C"`): "If `unit_cost` > `unit_price`, what prints for margin — and does it crash?" A crashes  B `0.0%`  C a negative %, no crash.

- [ ] **Step 5: Author Exercise 5 + Stretch A/B**

- Exercise 5 — REPL type investigation. Runnable `s-code` python containing the sequence as plain statements with `print()` wrappers so it runs in the deck:
  ```python
  print(type("12"))
  print(type(12))
  print(type(12.0))
  print(type(True))
  print("5" + "3")
  print(5 + 3)
  ```
  `s-out` static: `<class 'str'>` / `<class 'int'>` / `<class 'float'>` / `<class 'bool'>` / `53` / `8`. Notes: the per-result explanation and the connective idea about `input()`. Quiz (`data-answer="A"`): "`\"5\" + 3` — string plus int — does what?" A `TypeError`  B `8`  C `\"53\"`.
- Stretch A — three-product comparison. Runnable `s-code` with the guide's loop version; `s-out` static with the four output lines. Notes: the numbered-variable anti-pattern discussion + the simpler explicit version.
- Stretch B — format-spec exploration. `s-code` runnable:
  ```python
  print(f"{1234567:.2f}")
  print(f"{1234567:,.0f}")
  print(f"{0.3456:.1%}")
  print(f"{42:05d}")
  print(f"{'hello':>20}")
  ```
  `s-out` static with the five results. Notes: one sentence per spec.

- [ ] **Step 6: Author wrap-up**

- `s-wrap`: "Reflection" — the 3 reflection questions. Notes: the strong-answer guidance for each.
- `s-wrap`: "Submission checklist" — the 5 items. Notes: the Module 04 preview sentence.
- `s-end`: `ISM2411 · Week 3` / `End of lab`.

- [ ] **Step 7: Verify every runnable block in the browser**

Serve `ism2411` (`python3 -m http.server 8748`), open `pages/week03_lab_slides.html`:
- Every `s-code` python block, when Run, produces exactly the paired `s-out` text (type it into the editor unchanged first; then confirm editing + re-running works).
- Exercise 3 pass 1 raises the `TypeError` from the guide (as a Python traceback, red block); pass 2 with the seeded stdin prints `12 units of Notebook at $4.99 each = $59.88`.
- Every quiz's stated answer grades correct; every `.why` matches the guide.
- **S** shows notes; **D** draws; dark/light both legible; no console errors.

- [ ] **Step 8: Commit**

```bash
cd ism2411 && git add pages/week03_lab_slides.html && \
git commit -m "$(printf 'Add ISM2411 Week 3 interactive lab deck (pilot)\n\nProduct Pricer with f-strings, authored from the Week 3\nfacilitation guide. In-browser Python (Pyodide) runnable blocks\nincluding the input() two-pass TypeError demo, predict/quiz\nchecks, speaker notes carry the facilitation detail.\n\nCo-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01PN8CuB5TvVSWeU365mCNnU')" && cd ..
```

---

### Task 9: Lab-page links, authoring recipe, checkpoint

Wire the two pilot decks into their lab pages, write the recipe the rollout plan will follow, and stop for review. Submodule pointers are **not** bumped here.

**Files:**
- Modify: `ism3232/docs/week02_lab.html` (add a `Slides` link in the `.weekjump` bar, after the `Lab` link near line 209)
- Modify: `ism2411/pages/week03_lab.html` (add a `Slides` link in the week-jump bar, after line 252)
- Create: `docs/superpowers/lab-slides-authoring.md` (recipe, in the parent repo)

**Interfaces:**
- Consumes: Tasks 7 and 8 deliverables.

- [ ] **Step 1: Add the ISM3232 lab-page link**

In `ism3232/docs/week02_lab.html`, immediately after the line
`<a href="week02_lab.html" class="weekjump-link current">Lab</a>` add:
```html
<a href="week02_lab_slides.html" class="weekjump-link">Slides</a>
```

- [ ] **Step 2: Add the ISM2411 lab-page link**

In `ism2411/pages/week03_lab.html`, immediately after
`<a href="week03_lab.html" class="weekjump-link current">Lab</a>` add:
```html
<a href="week03_lab_slides.html" class="weekjump-link">Slides</a>
```

- [ ] **Step 3: Verify the links**

Reload each lab page from the running http.server; click **Slides**; confirm it opens the deck. Back-navigation returns to the lab page.

- [ ] **Step 4: Write `docs/superpowers/lab-slides-authoring.md`**

A concrete recipe for authoring the remaining 27 decks, covering: the deck `<head>` boilerplate to copy; the slide skeleton table (from the spec); the component markup snippets (`.run` python, `.run` shell with `data-fs`, `.quiz`, `.predict`, `s-out` static); the rule that every runnable block must be verified against its guide's stated output (emulator script for shell, browser for Python); the per-course specifics (ISM2411 all-Python; ISM3232 w01–w04 shell, w05–w16 Python, w14 sqlite3 OK, w15/w16 `data-readonly` only); the lab-page link snippet; and the final steps (bump both submodule pointers in the parent, print the 29 Canvas URLs). Include the ISM2411 w12–w15 `loadPackages(['pandas','matplotlib'])` opt-in button pattern.

- [ ] **Step 5: Commit (submodules + parent)**

```bash
cd ism3232 && git add docs/week02_lab.html && \
git commit -m "$(printf 'Link Week 2 interactive slides from the lab page\n\nCo-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01PN8CuB5TvVSWeU365mCNnU')"
cd ../ism2411 && git add pages/week03_lab.html && \
git commit -m "$(printf 'Link Week 3 interactive slides from the lab page\n\nCo-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01PN8CuB5TvVSWeU365mCNnU')"
cd .. && git add docs/superpowers/lab-slides-authoring.md && \
git commit -m "$(printf 'Add interactive lab-deck authoring recipe\n\nRecipe for the remaining 27 decks: skeleton, component markup,\nper-course specifics, verification, publish steps.\n\nCo-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01PN8CuB5TvVSWeU365mCNnU')"
```

- [ ] **Step 6: Checkpoint — hand off for review**

Stop. Report to the user:
- What was built: the framework (5 modules + CSS, both submodules, unit-tested), the component harness, and the two pilot decks, all committed **inside the submodules** (pointers not yet bumped).
- How to review: `cd ism3232 && python3 -m http.server 8747` → `http://localhost:8747/docs/week02_lab_slides.html`; `cd ism2411 && python3 -m http.server 8748` → `http://localhost:8748/pages/week03_lab_slides.html`.
- Ask: approve the pattern (interactivity feel, slide density, notes usefulness, visual design) before the remaining 27 decks are authored under the rollout plan.

---

## Self-Review

**1. Spec coverage**

| Spec section | Task |
|---|---|
| Shared interactivity layer, files, duplication rule | Tasks 1–5, global constraints |
| Runnable Python (editor, Run, lazy Pyodide, stdin/`input()`, autorun, readonly, reset) | Task 3 (harness) + Task 5 (widget) + Task 8 (exercised) |
| Simulated shell (fs seed, prompt, command list, `python3`→Pyodide) | Task 1 (core) + Task 5 (widget + hook) + Task 7 (exercised) |
| Knowledge check + predict variant | Task 2 + Task 6/7/8 |
| Step-through reveals | Native reveal `class="fragment"`; documented in Task 9 recipe (used by decks as needed) |
| Instructor annotation overlay | Task 4 + Task 6 verification |
| Deck skeleton (title → glance → obj → timing → per-exercise → stretch → wrap → end) | Tasks 7 and 8 author it; Task 9 records it in the recipe |
| Speaker notes carry facilitation detail | Tasks 7 and 8, every slide |
| Publishing: lab-page link, submodule commits, Canvas URL list | Task 9 (link + commits); submodule-pointer bump + URL list deferred to rollout plan per spec sequencing |
| Course-specific: ISM2411 all-Python incl. pandas/matplotlib | Task 8 (w03) + Task 9 recipe (`loadPackages` pattern) |
| Course-specific: ISM3232 shell w01–w04, Python w05–w16, w15/w16 readonly | Task 7 (w02) + Task 9 recipe |
| Risks: Pyodide slow/blocked → paired static output slide | Tasks 7/8 pair every runnable block with an `s-out` slide |
| Risks: framework copies diverge | Global constraint + every framework task copies to both trees + commits both |

Gap: the 27-deck rollout itself is intentionally out of scope — the spec's sequencing step 3 sits after a user-review checkpoint (Task 9 Step 6). A follow-on plan (`2026-…-interactive-lab-slides-rollout.md`) is written after approval, driven by `docs/superpowers/lab-slides-authoring.md`.

**2. Placeholder scan**

No "TBD"/"TODO"/"handle edge cases". Task 1 Step 3 and Task 5 Steps 1–2 describe implementations prose-heavily rather than as full code blocks — deliberate: they are long vanilla-DOM/parser modules whose behavior is pinned by the Task 1/2 `node --test` suites (full code given) and the Task 6 browser checklist (full checklist given). The tests are the executable spec.

**3. Type consistency**

- `createShell(seed)` / `run(shell, line)` / `prompt(shell)` — consistent across Tasks 1, 5, 7 and the test files.
- `run()` return shape `{out, err, cleared}` plus the optional `{async: Promise<{out,err}>}` for `python3` — defined Task 1, extended Task 5 Step 3 (test included), consumed by the widget in Task 5 Step 2.
- `runPython(code, {stdin, onStatus}) -> Promise<{stdout, stderr, ok}>` — consistent Tasks 3, 5, 6, 8.
- `pyReady`, `loadPackages` — Task 3, referenced Task 9 recipe.
- `parseAnswer` / `gradeQuiz(spec, chosen)` / `upgradeQuiz` / `upgradePredict` / `upgradeAll` — Task 2, consumed Task 5 `bootstrap`.
- `initDraw({accent})` — Task 4, called in Task 5 `bootstrap`, verified Task 6.
- `data-stdin` attribute — flagged in Task 8 Step 4 as a possible small addition to Task 5's `upgradeRunners`; the fix location is named.
- CSS section classes `s-title s-glance s-obj s-timing s-sec s-idea s-code s-out s-quiz s-warn s-wrap s-end` — defined Task 5 Step 1, used Tasks 6–8.

## Execution Handoff

**Plan complete and saved to `docs/superpowers/plans/2026-09-05-interactive-lab-slides.md`. Two execution options:**

**1. Subagent-Driven (recommended)** — I dispatch a fresh subagent per task, review between tasks, fast iteration.

**2. Inline Execution** — Execute tasks in this session using executing-plans, batch execution with checkpoints for review.

**Which approach?**
