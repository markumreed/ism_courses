# ISM2411 Lab W08: Your First GitHub Submission

## YouTube Metadata

**Title:** Your First GitHub Submission — Lab Walkthrough | ISM2411 Lab 08
**Description:**
Walkthrough of ISM2411 Module 8 Lab. We create a GitHub repository, push our Module 7 work, write a README, and establish the exact git workflow that every remaining assignment uses.

Course page: https://markumreed.github.io/ism2411/pages/week08_lab.html

**Chapters:**
0:00 — What this lab covers
0:45 — Creating a GitHub repo and cloning it locally
2:30 — Adding your files and writing a useful .gitignore
4:30 — The three git commands: add, commit, push
6:30 — Writing a good README.md
8:30 — Submission checklist

**Applies to:** ISM2411 Module 08

**Tags:** github tutorial beginners, git add commit push, python github workflow, git for students, ISM2411, USF, github first repo

---

## Script

### INTRO (0:00–0:45)

Lab 8 — Your First GitHub Submission. Everything from here on gets submitted via GitHub. This lab locks in the workflow: create a repo, add files, commit, push. You'll repeat these four steps every single remaining lab.

---

### CREATE THE REPO (0:45–2:30)

On GitHub.com: New repository → name it `ism2411-labs` → add a README → Create.

Now clone it:
```bash
cd ~
git clone https://github.com/yourusername/ism2411-labs.git
cd ism2411-labs
ls
# README.md
```

Move your Module 7 files in (or copy them):
```bash
mkdir module07
cp ~/ism2411/module07/*.py module07/
ls module07/
# business_tools.py  main.py  buggy.py
```

---

### .GITIGNORE (2:30–4:30)

Create `.gitignore` before your first commit:
```bash
# .gitignore
__pycache__/
*.pyc
.venv/
.DS_Store
```

These files don't belong in the repo. `__pycache__/` is Python's compiled bytecode — generated automatically, never needs to be tracked. `.venv/` is your virtual environment — hundreds of files, reproduced instantly with `pip install -r requirements.txt`.

Verify git is ignoring them:
```bash
git status
# Should NOT show __pycache__/ or .pyc files
```

---

### ADD, COMMIT, PUSH (4:30–6:30)

```bash
git add module07/
git add .gitignore
git status
# Shows staged files in green

git commit -m "Add module07 business tools and debug exercise"
git push origin main
```

Go to GitHub.com. Refresh your repo. Files are there.

The commit message should describe *what you did*, not "lab 8 submission." A year from now, `git log` should tell the story of what changed and why.

The `git log --oneline` command shows your history:
```
a3f9b1c Add module07 business tools and debug exercise
b2e8a0d Initial commit
```

Exercise 1 asks you to copy this output. If your messages are `"asdf"` or `"done"` or `"final_FINAL"` — that's the answer to whether you're treating version control seriously.

---

### README.MD (6:30–8:30)

Every repo needs a README. At minimum:

```markdown
# ISM2411 Labs — [Your Name]

Python for Business — USF Muma College of Business

## Labs
- **Module 01:** Computer Vocabulary & File System Tour
- **Module 02:** First Terminal Session & First Python Script
- **Module 03:** Product Pricer with F-Strings
- ...

## Setup
1. Clone this repo
2. `cd ism2411-labs`
3. `python3 module07/main.py`
```

A README tells anyone who clones your repo what's inside and how to run it.

---

### SUBMISSION CHECKLIST (8:30–10:00)

- GitHub repo created, files pushed
- `.gitignore` includes `__pycache__/`, `*.pyc`, `.venv/`
- Commit message is descriptive
- `README.md` updated with lab list
- `git log --oneline` output copied into Exercise 1 response
- GitHub URL pasted into Canvas
