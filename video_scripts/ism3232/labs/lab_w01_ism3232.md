# ISM3232 Lab W01: Developer Mindset & First Setup

## YouTube Metadata

**Title:** Developer Mindset & First Setup — Full Lab Walkthrough | ISM3232 Lab 01
**Description:**
Step-by-step, test-as-you-go walkthrough of ISM3232 Module 1 Lab — the full-class-period, midterm-eligible setup lab. Run the six environment verification commands, build the nine-folder course structure, type and run `hello_ism3232.py` (variables, f-strings, and all), answer the "what just happened" comment block, and write `README.md`.

Course page: https://markumreed.github.io/ism3232/docs/week01_lab.html

**Chapters:**
0:00 — What this lab covers and how to follow along
0:40 — Task 1: confirm you're in zsh, not bash
1:20 — Task 1: check zsh version
1:50 — Task 1: check Python 3 version
2:20 — Task 1: check Git version
2:50 — Task 1: confirm your home directory (pwd)
3:20 — Task 1: list home directory contents (ls)
3:50 — Screenshot 1 checkpoint — all six commands in one terminal
4:20 — Task 2: create the ism3232 course folder
5:20 — Task 2: create the module/data/screenshots subfolders
6:30 — Screenshot 2 checkpoint — VS Code Explorer
7:00 — Task 3: create hello_ism3232.py in module01_setup
7:50 — Task 3: type the header comment block
8:50 — Task 3: type the variables and print() lines
10:20 — Task 3: run the script and verify output
11:10 — Screenshot 3 checkpoint — script output
11:40 — Task 4: answer the "what just happened" comment block
13:00 — Task 5: create README.md and fill it in
14:40 — Final submission checklist walkthrough

**Applies to:** ISM3232 Module 01

**Tags:** developer environment setup, zsh python git verify, ISM3232, USF, python setup tutorial, first python script mac, terminal basics tutorial

---

## How to Use This Script

Every step below has three parts:

- **SAY** — what to say on camera before you type anything, so viewers know *why* they're running the command.
- **DO** — the exact command or code to type. Type it on screen; don't paste unless the step says the file is long.
- **CHECK** — the exact expected output. Read it out loud, point at the matching part of your terminal, and only move to the next step once yours matches. This is the "test" before you move on.

If a checkpoint doesn't match, each step includes a **FIX** line — say that on camera too. Debugging on camera is part of the lesson.

---

## Script

### INTRO (0:00–0:40)

**SAY:** "Lab 1 — Developer Mindset and First Setup. This is a full-class-period lab and it's midterm-eligible, so we're not rushing it. Four parts: verify your environment, build the course folder structure, write and run your first script, and document it in a README. One command at a time, and after every single one, we check the output before moving on."

---

### PART 1 — Verify Your Environment (0:40–3:50)

#### Task 1 — Run the six verification commands

**SAY:** "Open the VS Code integrated terminal. The prompt has to show a `%`, for zsh — not a `$`, which means bash. If you see `$`, stop and raise your hand before running anything else."

**DO (one command at a time):**
```bash
echo $SHELL
zsh --version
python3 --version
git --version
pwd
ls
```

**CHECK (expected output for each, in order):**
```
/bin/zsh
zsh 5.x or higher
Python 3.10 or higher
git version 2.x
/Users/yourname   (your home directory)
Desktop  Documents  Downloads  etc.
```

**FIX:** If `echo $SHELL` prints `/bin/bash`, this is the "stop and raise your hand" case from the page — don't try to fix it yourself on camera, flag it. For the version checks, anything at or above the stated minimum is fine; a lower version or "command not found" means the tool needs to be installed or updated before continuing.

---

#### Screenshot 1 checkpoint (3:50–4:20)

**SAY:** "Screenshot this entire output — all six commands and their results have to be visible in one screenshot, since that's the deliverable, not just running them."

**CHECK:** Scroll your terminal so `echo $SHELL` through `ls` and all six results are visible in a single screenshot.

---

### PART 2 — Course Folder Structure (4:20–6:30)

#### Task 2 — Create the full course folder

**SAY:** "Now we build the folder every module this semester lives in, plus its subfolders, in one shot."

**DO:**
```bash
cd ~
mkdir ism3232
cd ism3232
mkdir module01_setup module02_zsh module03_git_github \
      module04_programming module05_functions \
      module06_oop module07_final_project \
      data screenshots
ls
code .
```

**CHECK:** `ls` lists `module01_setup`, `module02_zsh`, `module03_git_github`, `module04_programming`, `module05_functions`, `module06_oop`, `module07_final_project`, `data`, and `screenshots`. `code .` opens VS Code with `ism3232` as the workspace root.

**FIX:** If `mkdir` errors with "File exists," a folder from a previous attempt is already there — that's fine, `mkdir` skips it; re-run the command and confirm all nine folders are present.

---

#### Screenshot 2 checkpoint (6:30–7:00)

**SAY:** "Screenshot 2: confirm all eight module folders appear in the VS Code Explorer panel on the left side."

**CHECK:** The Explorer panel shows the module subfolders alongside `data` and `screenshots`.

---

### PART 3 — First Python Script (7:00–11:40)

#### Task 3 — Create and run hello_ism3232.py

**SAY:** "Everything for this lab's script lives in `module01_setup`. Navigate in, create the file, and — don't copy-paste this — type every character."

**DO:**
```bash
cd ~/ism3232/module01_setup
touch hello_ism3232.py
code hello_ism3232.py
```

Type into `hello_ism3232.py`:
```python
# hello_ism3232.py
# ISM3232 - Business Application Development
# Author: [Your Name]

print('Hello, ISM3232!')

course_name   = 'Business Application Development'
credit_hours  = 3
weekly_hours  = credit_hours * 2

print(f'Course: {course_name}')
print(f'Expected weekly hours: {weekly_hours}')
print('Environment verified. Week 1 complete.')
```

Save with `⌘S` (Mac) or `Ctrl+S` (Windows), then run:
```bash
python3 hello_ism3232.py
```

**CHECK:**
```
Hello, ISM3232!
Course: Business Application Development
Expected weekly hours: 6
Environment verified. Week 1 complete.
```

**FIX:** If `weekly_hours` doesn't print `6`, check that `credit_hours * 2` was typed exactly — `3 * 2` — and not accidentally changed while typing.

---

#### Screenshot 3 checkpoint (11:10–11:40)

**SAY:** "Screenshot 3: the terminal showing this script's output."

**CHECK:** Terminal shows the `python3 hello_ism3232.py` command and all four output lines.

---

### PART 4 — Explanation and README (11:40–15:00)

#### Task 4 — Explain what just happened

**SAY:** "Before we move on, add a comment block below the existing header and answer these four questions about what actually happened when Python ran this file."

**DO:** Append to `hello_ism3232.py`:
```python
# --- What happened when I ran this script? ---
# 1. The shell found the python3 interpreter at: ___
# 2. Python read the file from top to bottom: True / False
# 3. The f-string on line 11 evaluated {weekly_hours} to: ___
# 4. The output appeared in: the editor / the terminal / both
```

**CHECK:** All four blanks are filled in with real answers — question 3's answer should be `6`, matching the `weekly_hours` value printed in Task 3. Save the file.

---

#### Task 5 — Create README.md

**SAY:** "Still inside `module01_setup`, one README documenting what you verified and what you did."

**DO:**
```bash
touch README.md
code README.md
```

Type:
```markdown
# ISM3232 - Module 1: Course Setup

**Name:** [Your Name]
**Date:** [Today's Date]

## What I Did
- Verified zsh, Python 3, and Git versions
- Created the ism3232/ course folder structure
- Wrote and ran hello_ism3232.py from the terminal

## Verification Results

| Tool     | Version |
|----------|---------|
| zsh      |         |
| Python 3 |         |
| Git      |         |

## AI Use Statement
I did not use AI for this lab.
```

**CHECK:** The version-number blanks in the table are filled in with the real output from Task 1's `zsh --version`, `python3 --version`, and `git --version` — not left blank, and not generic placeholders.

---

### FINAL SUBMISSION CHECKLIST (15:00–end)

**SAY:** "This is completion credit, due by the end of class — walk through this list on camera before uploading."

- [ ] Screenshot 1: all six verification commands and their output in the zsh terminal
- [ ] Screenshot 2: VS Code Explorer panel showing all module subfolders
- [ ] Screenshot 3: terminal showing the output of `hello_ism3232.py`
- [ ] `module01_setup/hello_ism3232.py` uploaded — including your answers in the comment block
- [ ] `module01_setup/README.md` uploaded — with name, date, versions filled in, and an AI use statement
- [ ] All files submitted to Canvas by end of class
