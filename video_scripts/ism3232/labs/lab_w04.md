# ISM3232 Lab W04: Search Tools, the Submission Ritual & Git

## YouTube Metadata

**Title:** Search Tools, Submission Ritual & First GitHub Push — Lab Walkthrough | ISM3232 Lab 04
**Description:**
Walkthrough of ISM3232 Module 4 Lab. We use rg (ripgrep), find, and tree to search a codebase, write three pytest tests, then execute the complete pre-submission ritual from start to finish before pushing to GitHub.

Course page: https://markumreed.github.io/ism3232/docs/week04_lab.html

**Chapters:**
0:00 — What this lab covers
0:45 — Search tools: rg, find, tree
3:00 — Writing three pytest tests
5:00 — The complete submission ritual step by step
7:30 — Creating the GitHub repo and first push
8:30 — Submission checklist

**Applies to:** ISM3232 Module 04

**Tags:** ripgrep python, submission ritual git, pytest tutorial, git first push github, ISM3232, USF, pre-commit workflow

---

## Script

### INTRO (0:00–0:45)

Lab 4 — Search Tools, the Submission Ritual, and Git. The ritual is the most important workflow in this course. Every assignment ends with it. By the end of this lab you'll have run it once — correctly — and pushed to GitHub. Muscle memory from here on.

---

### SEARCH TOOLS (0:45–3:00)

```bash
cd ~/ism3232

# rg (ripgrep) — search file contents
rg "def "
# Finds every function definition across all .py files

rg "import" module02_zsh/
# Searches only within that folder

rg -l "pytest"
# Lists only the filenames that match

# find — search by filename or type
find . -name "*.py"
# All Python files

find . -name "requirements.txt"
# Find a specific file

# tree — visualize structure
tree -L 3
# Three levels deep
```

Screenshot 1: two `rg` commands and `tree -L 3` output.

---

### THREE PYTEST TESTS (3:00–5:00)

Create `module02_zsh/tests/test_week4.py`:

```python
# test_week4.py

def apply_discount(price, rate):
    """Apply a discount rate and return the final price."""
    return price * (1 - rate)


def test_ten_percent_discount():
    assert apply_discount(100.00, 0.10) == 90.00


def test_zero_discount():
    assert apply_discount(50.00, 0.0) == 50.00


def test_full_discount():
    assert apply_discount(200.00, 1.0) == 0.0
```

Run them:
```bash
source .venv/bin/activate
python3 -m pytest tests/test_week4.py -v
```

All three should be green.

---

### THE COMPLETE SUBMISSION RITUAL (5:00–7:30)

Run every step in this exact order. Do not skip steps.

```bash
# 1. Confirm location
pwd
# /Users/yourname/ism3232/module02_zsh

# 2. Confirm structure
tree -L 3

# 3. Activate venv
source .venv/bin/activate

# 4. Format code
ruff format .

# 5. Lint (check for errors)
ruff check .

# 6. Run tests — must be green before committing
python3 -m pytest -v

# 7. Check git status
git status

# 8. Stage everything
git add .

# 9. Commit with a descriptive message
git commit -m "lab 4: search tools, submission ritual, and git"

# 10. Push
git push
```

Screenshot 2: the complete ritual — all steps in one terminal session.

---

### GITHUB REPO AND FIRST PUSH (7:30–8:30)

If you haven't created your repo yet:
1. GitHub.com → New repository → name `ism3232-labs`
2. Copy the remote URL
3. In terminal: `git remote add origin <URL>`
4. `git push -u origin main`

Verify on GitHub.com — your files should be visible.

Screenshot 3: your GitHub repository page showing committed files.

---

### SUBMISSION CHECKLIST (8:30–10:00)

- Screenshot 1: `rg` commands + `tree -L 3`
- Screenshot 2: complete ritual in one terminal session
- Screenshot 3: GitHub repository page with files
- `tests/test_week4.py` uploaded
- GitHub URL pasted into Canvas text box
