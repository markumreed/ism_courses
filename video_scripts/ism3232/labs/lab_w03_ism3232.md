# ISM3232 Lab W03: Virtual Environments & Shell Customisation

## YouTube Metadata

**Title:** Virtual Environments & .zshrc Aliases — Full Lab Walkthrough | ISM3232 Lab 03
**Description:**
Step-by-step, test-as-you-go walkthrough of ISM3232 Module 3 Lab. Create and activate a venv, confirm isolation from a second terminal, install pytest and ruff, freeze requirements.txt, write .gitignore, add 9 required aliases plus the mkcd function to .zshrc, and deactivate cleanly — every command run and verified one at a time.

Course page: https://markumreed.github.io/ism3232/docs/week03_lab.html

**Chapters:**
0:00 — What this lab covers — the "private room" mental model
0:40 — Step 1: create the venv
1:20 — Step 2: activate it and confirm the prompt changes
2:00 — Step 3: which python3 — confirm it points inside .venv
2:40 — Step 4: pip list — confirm a minimal package set
3:10 — Screenshot 1 checkpoint
3:30 — Step 5: install pytest and ruff
4:10 — Step 6: freeze requirements.txt and confirm its contents
5:00 — Screenshot 2 checkpoint
5:20 — Step 7: verify isolation from a second, non-venv terminal
6:30 — Step 8: write .gitignore, line by line
7:40 — Step 9: confirm with ls -la
8:00 — Screenshot 3 checkpoint
8:20 — Step 10: open ~/.zshrc and add the 9 required aliases
10:30 — Step 11: add the mkcd function
11:10 — Step 12: source ~/.zshrc and test each alias
12:40 — Screenshot 4 checkpoint
13:00 — Step 13: pytest --collect-only, then deactivate cleanly
14:00 — Step 14: add the Week 3 README section
14:50 — Submission checklist

**Applies to:** ISM3232 Module 03

**Tags:** python virtual environment, python venv tutorial, zshrc aliases, pip install requirements, ISM3232, USF, python venv mac, zsh customization

---

## How to Use This Script

**SAY** it, **DO** it, **CHECK** the exact output, **FIX** it if it doesn't match — then move to the next step.

---

## Script

### INTRO (0:00–0:40)

**SAY:** "Lab 3 — virtual environments and shell customization. Here's the mental model before we type anything: a venv is a private room for each project. Activate it and you walk in — every package you install stacks up on that room's shelves. Deactivate and you walk out — other projects are completely unaffected. Let's build one."

---

### PART 1 — Virtual Environment Workflow (0:40–5:20)

#### Step 1 — Create the venv

**SAY:** "One command creates the whole isolated environment as a folder called `.venv`."

**DO:**
```bash
cd ~/ism3232/module02_zsh
python3 -m venv .venv
```

**CHECK:** No output on success, and a new hidden `.venv/` folder now exists — confirm with `ls -la` (the leading dot means plain `ls` won't show it).

---

#### Step 2 — Activate it

**SAY:** "Activating doesn't install anything — it just tells the shell 'use this room's Python from now on.'"

**DO:**
```bash
source .venv/bin/activate
```

**CHECK:** Your prompt now shows a `(.venv)` prefix:
```
(.venv) yourname@machine module02_zsh %
```

**FIX:** If you don't see `(.venv)`, confirm you ran the command from inside `module02_zsh` and that `.venv/bin/activate` exists via `ls .venv/bin`.

---

#### Step 3 — Confirm which Python is active

**SAY:** "Let's prove the isolation is real, not just cosmetic — which `python3` binary is actually running now?"

**DO:**
```bash
which python3
```

**CHECK:**
```
/Users/yourname/ism3232/module02_zsh/.venv/bin/python3
```
It points *inside* `.venv`, not at the system Python — that's isolation working.

---

#### Step 4 — Check installed packages

**SAY:** "A fresh venv starts almost empty — let's see."

**DO:**
```bash
pip list
```

**CHECK:**
```
Package    Version
---------- -------
pip        24.x
```
Just `pip` itself (and maybe `setuptools`) — nothing else yet.

---

#### Screenshot 1 checkpoint (3:10–3:30)

**SAY:** "Screenshot 1 — the `(.venv)` prefix in the prompt, plus the `which python3` output."

---

#### Step 5 — Install packages

**SAY:** "Now we furnish the room — installing the two tools this course uses everywhere: `pytest` for testing, `ruff` for linting."

**DO:**
```bash
pip install pytest ruff
pip list
```

**CHECK:** The second `pip list` now includes both:
```
pytest     8.x.x
ruff       0.x.x
```
plus their dependencies.

---

#### Step 6 — Freeze requirements

**SAY:** "`pip freeze` writes down every installed package and its exact version, so anyone — including future you — can rebuild this exact environment."

**DO:**
```bash
pip freeze > requirements.txt
cat requirements.txt
```

**CHECK:** File contents list `pytest==8.x.x`, `ruff==0.x.x`, and their dependencies, each pinned to an exact version number.

---

#### Screenshot 2 checkpoint (5:00–5:20)

**SAY:** "Screenshot 2 — the `pip install` output and `cat requirements.txt` output."

---

#### Step 7 — Verify isolation from a second terminal

**SAY:** "The real test: open a brand-new terminal tab — do *not* activate the venv in it — and check the same two things."

**DO:** In a new terminal tab (venv **not** activated):
```bash
which python3
pip list
```

**CHECK:**
```
/usr/bin/python3
```
and a `pip list` that does **not** include `pytest` or `ruff`.

This confirms the venv only affects the terminal session where you activated it — that's what "isolated" means in practice. Switch back to your original, activated terminal before continuing.

---

### PART 2 — .gitignore (6:30–8:20)

#### Step 8 — Write .gitignore line by line

**SAY:** "The `.venv/` folder can be hundreds of megabytes and is entirely reproducible from `requirements.txt` — it should never be committed to Git. Let's write the rule before we ever run `git add`."

**DO:**
```bash
cd ~/ism3232/module02_zsh
echo '.venv/' > .gitignore
echo '__pycache__/' >> .gitignore
echo '*.pyc' >> .gitignore
cat .gitignore
```

**CHECK:**
```
.venv/
__pycache__/
*.pyc
```
Note the first line used `>` (create/overwrite) and the next two used `>>` (append) — using `>` again on lines 2 or 3 would have erased line 1.

---

#### Step 9 — Confirm both files exist

**SAY:** "One more check — both the environment and the ignore rule for it should be sitting side by side."

**DO:**
```bash
ls -la
```

**CHECK:** Output includes both `.venv` and `.gitignore` in the listing (along with `requirements.txt` from Step 6).

---

#### Screenshot 3 checkpoint (8:00–8:20)

**SAY:** "Screenshot 3 — `ls -la` showing both `.venv/` and `.gitignore`."

---

### PART 3 — .zshrc Aliases and Functions (8:20–12:40)

#### Step 10 — Open .zshrc and add the required aliases

**SAY:** "Now we customize the shell itself. `.zshrc` runs every time you open a new terminal — anything defined here is available everywhere, in every project."

**DO:**
```bash
code ~/.zshrc
```
Add these lines at the end of the file — **do not delete anything already there**:
```bash
# ISM3232 required aliases
alias ll='ls -la'
alias c='clear'
alias py='python3'
alias gs='git status'
alias ga='git add .'
alias gcmsg='git commit -m'
alias gp='git push'
alias gl='git log --oneline'
alias tree2='tree -L 2'
```

**CHECK:** Nine `alias` lines are now in `~/.zshrc`, each mapping a short name to a longer command you'll type constantly this semester.

---

#### Step 11 — Add the mkcd function

**SAY:** "One more addition — a shell *function*, not just an alias, because it needs to take an argument: a folder name."

**DO:** Directly below the aliases:
```bash
# Required shell function
mkcd() { mkdir -p "$1" && cd "$1" }
```
Save the file.

**CHECK:** Read the function back on camera: "`mkcd` takes one argument, `$1`, makes that directory — including any missing parent folders because of `-p` — and if that succeeds, changes into it. One command instead of two."

---

#### Step 12 — Reload and test every alias

**SAY:** "New config in `.zshrc` doesn't apply automatically to an already-open terminal — we have to reload it."

**DO:**
```bash
source ~/.zshrc
ll
gs
mkcd testdir
pwd
```

**CHECK:**
- `ll` prints a long listing (same as `ls -la`)
- `gs` prints `git status` output for the current repo (or "not a git repository" if you're outside one — either confirms the alias works)
- `mkcd testdir` produces no output but changes directory
- `pwd` confirms you're now inside `testdir`:
```
/Users/yourname/ism3232/module02_zsh/testdir
```

**FIX:** If `source ~/.zshrc` throws a syntax error, check for a missing quote or brace on the `mkcd` line — the braces `{ }` must both be present with a space after `{`.

---

#### Screenshot 4 checkpoint (12:40–13:00)

**SAY:** "Screenshot 4 — `ll`, `gs`, and `mkcd` all working, right after `source ~/.zshrc`."

---

### PART 4 — Practice and Deactivate (13:00–14:00)

#### Step 13 — Quick pytest sanity check, then deactivate

**SAY:** "Before we leave the venv, one quick test that the tooling itself works, even with zero test files yet."

**DO:**
```bash
cd ~/ism3232/module02_zsh
source .venv/bin/activate
pytest --collect-only
```

**CHECK:**
```
no tests found
```
(or similar language — pytest confirming it looked and found nothing yet, which is correct since we haven't written test files).

Now leave the room:
```bash
deactivate
which python3
```

**CHECK:**
```
/usr/bin/python3
```
Back to the system Python, and the `(.venv)` prefix is gone from the prompt.

---

#### Step 14 — Add the Week 3 README section

**SAY:** "Same README from last week, one more section appended — never delete previous weeks' work."

**DO:**
```bash
cd ~/ism3232/module02_zsh
code README.md
```
Add:
```markdown
## Week 3: Virtual Environments and .zshrc

- `python3 -m venv .venv` — creates an isolated environment
- `source .venv/bin/activate` — activates it (shows `(.venv)` in prompt)
- `pip install <package>` — installs into the active venv only
- `pip freeze > requirements.txt` — records exact installed versions
- `deactivate` — leaves the venv, returns to system Python
- 9 required aliases and `mkcd` added to `~/.zshrc`
```

**CHECK:** `README.md` now has two sections — the Week 1/2 content from before, plus this new `## Week 3` heading — nothing earlier was overwritten.

---

### SUBMISSION CHECKLIST (14:50–end)

- [ ] Screenshot 1: `(.venv)` prompt and `which python3` output
- [ ] Screenshot 2: `pip install` output and `cat requirements.txt`
- [ ] Screenshot 3: `ls -la` showing `.venv/` and `.gitignore`
- [ ] Screenshot 4: `ll`, `gs`, and `mkcd` working after `source ~/.zshrc`
- [ ] `module02_zsh/requirements.txt` uploaded
- [ ] `module02_zsh/.gitignore` uploaded
- [ ] `README.md` with Week 3 section added, uploaded
- [ ] Submitted to Canvas
