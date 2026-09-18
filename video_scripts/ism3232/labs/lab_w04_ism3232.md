# ISM3232 Lab W04: Search Tools, the Submission Ritual & Git

## YouTube Metadata

**Title:** Search Tools, Submission Ritual & First GitHub Push — Full Lab Walkthrough | ISM3232 Lab 04
**Description:**
Step-by-step, test-as-you-go walkthrough of ISM3232 Module 4 Lab — the most important lab of Unit 1. Search a codebase with ripgrep, find, and tree; write and pass three pytest tests; run the exact pre-submission ritual (pwd → tree → activate → ruff format → ruff check → pytest → git status/add/commit/push) that's required before every major assignment for the rest of the semester; then create a GitHub repo and push for the first time.

Course page: https://markumreed.github.io/ism3232/docs/week04_lab.html

**Chapters:**
0:00 — Why this is the most important lab of Unit 1
0:40 — Step 1: rg searches — print, def, import
1:50 — Step 2: find — locate files by name
2:30 — Step 3: tree -L 3 — full structure
2:50 — Screenshot 1 checkpoint
3:10 — Step 4: create the tests folder and test file
3:50 — Step 5: type all three tests
5:00 — Step 6: run pytest -v and confirm all three pass
5:40 — Step 7: the ritual, command by command
8:20 — Screenshot 2 checkpoint
8:40 — Step 8: create the GitHub repo and connect it
10:00 — Step 9: push and verify on GitHub.com
10:40 — Screenshot 3 checkpoint
11:00 — Step 10: verify the commit log
11:40 — Submission checklist

**Applies to:** ISM3232 Module 04

**Tags:** ripgrep python, submission ritual git, pytest tutorial, git first push github, ISM3232, USF, pre-commit workflow

---

## How to Use This Script

**SAY** it, **DO** it, **CHECK** the exact output, **FIX** it if it doesn't match — then move to the next step.

---

## Script

### INTRO (0:00–0:40)

**SAY:** "Lab 4 — search tools, the submission ritual, and Git. This is the single most important lab in Unit 1. The ritual we build today — format, lint, test, commit, push — is required before every major assignment for the rest of the semester. Instructors check your Git log. A missing `ruff` or `pytest` step is visible there, so we're building the habit correctly, right now, on camera."

---

### PART 1 — Search Tools, One Command at a Time (0:40–3:10)

#### Step 1 — Search file contents with ripgrep

**SAY:** "`rg` — ripgrep — searches inside every file's contents, fast. Let's find every `print` statement across the whole course folder."

**DO:**
```bash
cd ~/ism3232
rg 'print'
```

**CHECK:** A list of file paths and line numbers, each showing a line containing `print` — for example, the two `print()` lines from `module01_setup/hello_ism3232.py`.

**FIX:** If `rg: command not found`, install it — macOS: `brew install ripgrep`; Ubuntu: `sudo apt install ripgrep`.

---

#### Step 2 — Search for function definitions

**SAY:** "Now every function definition in the whole project, in one command."

**DO:**
```bash
rg 'def '
```

**CHECK:** Lines like `module02_zsh/tests/test_week4.py:2:def test_always_passes():` — file, line number, and the matching line itself.

---

#### Step 3 — List just the matching filenames

**SAY:** "Sometimes you don't want to see every matching line — just *which files* contain a match. That's the `-l` flag."

**DO:**
```bash
rg -l 'import'
```

**CHECK:** A short list of filenames only — no line numbers, no matched text, just paths.

---

#### Step 4 — Search by filename with find

**SAY:** "`rg` searches file *contents*. `find` searches file *names*. Three quick examples."

**DO:**
```bash
find . -name '*.py'
find . -name '*.md'
find . -name '*.txt'
```

**CHECK:** Three separate lists — every `.py` file, every `.md` file, every `.txt` file in the current tree, each printed with its relative path (e.g. `./module01_setup/hello_ism3232.py`).

---

#### Step 5 — Visualize with tree

**SAY:** "And one more look at the whole structure, three levels deep this time — deeper than the `-L 2` we used in Week 2."

**DO:**
```bash
tree -L 3
```

**CHECK:** The full `ism3232/` tree, now showing files *inside* `module01_setup`, `module02_zsh`, etc. — not just the folder names.

---

#### Screenshot 1 checkpoint (2:50–3:10)

**SAY:** "Screenshot 1 — at least two `rg` commands and their output, plus the `tree -L 3` output."

---

### PART 2 — Write a Test File (3:10–5:40)

#### Step 6 — Set up the tests folder

**SAY:** "We're adding real tests to `module02_zsh` now. Activate the venv first — pytest lives inside it, remember."

**DO:**
```bash
cd ~/ism3232/module02_zsh
source .venv/bin/activate
mkdir -p tests
touch tests/__init__.py tests/test_week4.py
code tests/test_week4.py
```

**CHECK:** Prompt shows `(.venv)`, and `ls tests/` shows two files: `__init__.py` and `test_week4.py`.

---

#### Step 7 — Type all three tests

**SAY:** "Three tests, each checking something different — a pure math fact, a string property, and a path-splitting operation. Type them in, don't paste."

**DO:**
```python
# tests/test_week4.py

def test_always_passes():
    assert 2 + 2 == 4


def test_string_is_lowercase():
    name = 'ism3232'
    assert name == name.lower()


def test_path_segments():
    path = '/Users/yourname/ism3232/module02_zsh'
    parts = path.split('/')
    assert 'ism3232' in parts
```

**CHECK:** Read each test out loud before running it: "Test one — trivially, 2 plus 2 is 4. Test two — `'ism3232'` is already all lowercase, so it equals its own `.lower()`. Test three — splitting that path on `/` gives a list of segments, and `'ism3232'` must be one of them."

---

#### Step 8 — Run pytest and confirm all three pass

**SAY:** "Moment of truth — run it."

**DO:**
```bash
pytest -v
```

**CHECK:**
```
tests/test_week4.py::test_always_passes PASSED
tests/test_week4.py::test_string_is_lowercase PASSED
tests/test_week4.py::test_path_segments PASSED

======================== 3 passed in 0.01s ========================
```

**FIX:** If `test_path_segments` fails, print the actual `parts` list with a debug `print(parts)` above the `assert` and re-run with `pytest -v -s` (the `-s` flag lets `print()` output show) to see exactly what `.split('/')` produced.

---

### PART 3 — Pre-Submission Ritual, Step by Step (5:40–8:40)

**SAY:** "Here is the ritual. Ten steps, always in this order, for the rest of the semester. I'm going to run every single one and show you the checkpoint for each before moving to the next."

#### Step 9a — Confirm location

**DO:**
```bash
pwd
```

**CHECK:**
```
/Users/yourname/ism3232/module02_zsh
```

---

#### Step 9b — Confirm structure

**DO:**
```bash
tree -L 3
```

**CHECK:** Full structure including `.venv/`, `tests/`, `requirements.txt`, `.gitignore` — a snapshot of exactly what exists before you touch Git.

---

#### Step 9c — Activate the venv

**DO:**
```bash
source .venv/bin/activate
```

**CHECK:** `(.venv)` prefix appears in the prompt.

---

#### Step 9d — Format the code

**SAY:** "`ruff format` rewrites your files to a consistent style automatically — spacing, quote style, line length."

**DO:**
```bash
ruff format .
```

**CHECK:**
```
2 files reformatted, 1 file left unchanged
```
(Exact counts vary — the key output is that it ran without error.)

---

#### Step 9e — Lint the code

**SAY:** "`ruff check` looks for actual problems — unused imports, undefined names — not just style."

**DO:**
```bash
ruff check .
```

**CHECK:**
```
All checks passed!
```

**FIX:** If it lists errors instead, read the file:line references and fix each one before continuing — do not commit with lint errors present.

---

#### Step 9f — Run the tests

**DO:**
```bash
pytest
```

**CHECK:**
```
3 passed in 0.01s
```

**FIX:** If anything fails here, stop — go back and fix it before touching Git. Never commit on a red test suite.

---

#### Step 9g — Check git status

**DO:**
```bash
git status
```

**CHECK:** A list of untracked/modified files — `tests/`, any reformatted files, etc. — none of them should be `.venv/` (that's what your Week 3 `.gitignore` prevents).

---

#### Step 9h — Stage everything

**DO:**
```bash
git add .
```

**CHECK:** No output. Re-run `git status` mentally in your head — everything just staged should now show green/staged in a follow-up `git status` if you want to double check.

---

#### Step 9i — Commit with a descriptive message

**DO:**
```bash
git commit -m 'lab 4: search ritual and git'
```

**CHECK:**
```
[main abc1234] lab 4: search ritual and git
 4 files changed, 32 insertions(+)
```

---

#### Step 9j — Push

**DO:**
```bash
git push
```

**CHECK:** Output ending in something like `main -> main` with no errors. (If this is your very first push, see Part 4 below first — you need a remote configured before `push` works.)

**Ritual complete when:** `ruff check` returns no errors, `pytest` returns all passed, and `git status` says "nothing to commit" right after the push.

---

#### Screenshot 2 checkpoint (8:20–8:40)

**SAY:** "Screenshot 2 — the entire ritual, from `pwd` through `git push`, visible in one terminal session."

---

### PART 4 — First GitHub Push (8:40–11:00)

#### Step 10 — Create the GitHub repo and connect it

**SAY:** "If Step 9j just failed because there's no remote yet, here's the one-time setup."

**DO:** On github.com: New repository → name it `ism3232-module02` → set Private → do **not** initialize with a README. Then back in the terminal:
```bash
git remote add origin https://github.com/YOURUSERNAME/ism3232-module02.git
git branch -M main
git push -u origin main
```

**CHECK:** Push output shows your objects being uploaded and ending with a line establishing `main` tracks `origin/main`.

**FIX:** If you get "repository not found," double check the URL matches exactly what GitHub showed you after creating the repo — case and spelling both matter.

---

#### Step 11 — Verify on GitHub.com

**SAY:** "Don't trust the terminal alone — open the actual repository page in a browser."

**DO:** Navigate to `https://github.com/YOURUSERNAME/ism3232-module02` in Chrome.

**CHECK:** Your files — `tests/test_week4.py`, `requirements.txt`, `.gitignore`, `README.md` — are all listed, and the latest commit message (`lab 4: search ritual and git`) shows at the top.

---

#### Screenshot 3 checkpoint (10:40–11:00)

**SAY:** "Screenshot 3 — your GitHub repository page, showing the committed files."

---

#### Step 12 — Verify the commit log

**SAY:** "One last check — the commit history itself, because this log is part of your grade."

**DO:**
```bash
git log --oneline
git status
```

**CHECK:**
```
abc1234 lab 4: search ritual and git
```
and
```
nothing to commit, working tree clean
```

**FIX:** If your commit message just says "final" or "update," rewrite future commits to be descriptive — that's explicitly graded from here forward.

---

### SUBMISSION CHECKLIST (11:40–end)

- [ ] Screenshot 1: two `rg` commands and `tree -L 3` output
- [ ] Screenshot 2: the complete pre-submission ritual — all steps in one terminal session
- [ ] Screenshot 3: your GitHub repository page showing committed files
- [ ] `module02_zsh/tests/test_week4.py` uploaded
- [ ] Your GitHub repository URL pasted into the Canvas text box
