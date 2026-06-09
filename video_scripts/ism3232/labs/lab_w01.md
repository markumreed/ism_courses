# ISM3232 Lab W01: Developer Mindset & First Setup

## YouTube Metadata

**Title:** Developer Mindset & First Setup — Lab Walkthrough | ISM3232 Lab 01
**Description:**
Walkthrough of ISM3232 Module 1 Lab. We verify the full developer environment — zsh, Python 3, Git — create the course folder structure, write and run hello_ism3232.py, and submit a README documenting everything.

Course page: https://markumreed.github.io/ism3232/docs/week01_lab.html

**Chapters:**
0:00 — What this lab covers
0:30 — Running the six verification commands
2:30 — Creating the eight module subfolders
4:30 — Writing hello_ism3232.py with the comment block
7:00 — Writing README.md with versions and AI statement
8:30 — Submission checklist

**Applies to:** ISM3232 Module 01

**Tags:** developer environment setup, zsh python git verify, ISM3232, USF, python setup tutorial, first python script mac

---

## Script

### INTRO (0:00–0:30)

Lab 1 — Developer Mindset and First Setup. Before we write a single line of business logic, we verify the foundation is solid. Six commands, one folder structure, one Python script, one README. This setup is what everything else in the course builds on.

---

### SIX VERIFICATION COMMANDS (0:30–2:30)

Open your zsh terminal and run each one:

```bash
echo $SHELL
# /bin/zsh — confirms you're in zsh, not bash

zsh --version
# zsh 5.x.x

python3 --version
# Python 3.12.x (or later)

git --version
# git version 2.x.x

pwd
# /Users/yourname or /home/yourname

ls
# lists your home directory contents
```

Screenshot all six in a single terminal session — that's Screenshot 1.

If `python3` shows 2.x, you have Python 2 — install Python 3 from python.org. If git isn't found, install from git-scm.com. If `echo $SHELL` shows `/bin/bash`, type `zsh` to switch.

Also run:
```bash
git config --global --list
```
Confirm your `user.name` and `user.email` are set. If not:
```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

---

### COURSE FOLDER STRUCTURE (2:30–4:30)

```bash
cd ~
mkdir ism3232
cd ism3232
mkdir module01_setup module02_zsh module03_venv module04_search \
      module05_python module06_loops module07_functions module08_debug
ls
```

Screenshot the VS Code Explorer panel showing all eight subfolders — that's Screenshot 2.

Open the folder as a VS Code workspace:
```bash
code module01_setup
```

---

### HELLO_ISM3232.PY (4:30–7:00)

Create `module01_setup/hello_ism3232.py`:

```python
# hello_ism3232.py
# Name: [Your Name]
# Date: [Today's date]
# Course: ISM3232 — Business Application Development

print("Hello, ISM3232!")
print("I am building production-quality Python applications.")

# What does this script do?
# It runs a Python interpreter on a plain text file and executes each line.
# The OS loaded the Python interpreter into RAM from storage, then the
# interpreter read this file line by line and executed each print() call.

# What surprised you about running Python from the terminal?
# [Your answer here — be specific]
```

Run it:
```bash
cd ~/ism3232/module01_setup
python3 hello_ism3232.py
```

Screenshot the terminal output — Screenshot 3.

---

### README.MD (7:00–8:30)

Create `module01_setup/README.md`:

```markdown
# ISM3232 Module 01 — Developer Setup

**Name:** [Your Name]
**Date:** [Today's date]

## Environment Versions
- Shell: zsh 5.x.x
- Python: 3.12.x
- Git: 2.x.x
- OS: macOS 14.x / Ubuntu 22.x

## AI Use Statement
[Describe honestly: did you use AI assistance in this lab? What for?
E.g., "Used Claude to clarify what $SHELL prints." or "No AI used."]
```

---

### SUBMISSION CHECKLIST (8:30–10:00)

- Screenshot 1: six verification commands in one terminal session
- Screenshot 2: VS Code Explorer with all eight subfolders
- Screenshot 3: `hello_ism3232.py` output in terminal
- `hello_ism3232.py` uploaded with comment block answered
- `README.md` uploaded with versions and AI statement
- Submitted to Canvas
