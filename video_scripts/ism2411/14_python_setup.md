# Video 14: Python Setup & Running Your First Script

## YouTube Metadata

**Title:** Install Python & VS Code — Run Your First Script | ISM2411
**Description:**
Get Python, VS Code, and your terminal working correctly in under 15 minutes. This video walks through installation on Mac and Windows (WSL), verifies each tool, creates the course folder structure, and runs a first Python script from the terminal — the professional way.

**Chapters:**
0:00 — What we're installing and why
1:30 — Installing VS Code
3:00 — Installing Python 3
5:00 — Verifying your setup (6 commands)
7:30 — Creating your course folder
9:00 — Writing and running your first script
11:00 — Common setup problems
13:00 — Recap

**Applies to:** ISM2411 Module 2

**Tags:** install python, python setup, VS Code setup, python for beginners, ISM2411, USF, run python script, terminal python, python tutorial, python environment setup

---

## Script

### INTRO (0:00–1:30)

The goal of this video is simple: by the end, you'll type six verification commands in your terminal, see all green, and run a Python script. That's the deliverable for Module 2's lab. Let's get there.

If you're on Mac, your terminal already runs zsh and you're almost ready. If you're on Windows, you need to install WSL — Windows Subsystem for Linux — before this video makes sense. The pre-course setup tutorial covers WSL installation. Come back here once WSL is running.

---

### INSTALL VS CODE (1:30–3:00)

Go to code.visualstudio.com. Download for your operating system. Install it. Open it.

VS Code is your editor — where you write Python. But you'll also use its integrated terminal to run scripts. That keeps everything in one window.

Inside VS Code, install the Python extension: left sidebar → Extensions (the puzzle piece icon) → search "Python" → install the one by Microsoft. This gives you syntax highlighting, autocomplete, and the ability to run scripts directly.

---

### INSTALL PYTHON 3 (3:00–5:00)

**Mac:** Python 3 may already be installed. Check:
```bash
python3 --version
```
If you see `Python 3.10.x` or higher, you're good. If not, go to python.org, download the macOS installer, run it.

**Windows (WSL):** Inside your WSL terminal:
```bash
sudo apt update
sudo apt install python3 python3-pip
python3 --version
```

**Important:** always use `python3`, not `python`. On many systems, `python` refers to the old Python 2 which is no longer supported.

Install Git if not present:
```bash
git --version   # check first
# If not installed on Mac: xcode-select --install
# If not installed on WSL: sudo apt install git
```

---

### VERIFYING YOUR SETUP (5:00–7:30)

Run these six commands. All six should produce output without errors.

```bash
echo $SHELL       # should show /bin/zsh (Mac) or /bin/bash (WSL)
python3 --version # Python 3.10.x or higher
git --version     # git version 2.x.x
pwd               # shows your home directory
ls                # lists files — Desktop, Documents, etc.
code --version    # VS Code version number
```

If any command fails:
- `command not found: python3` — Python isn't installed or isn't in your PATH
- `command not found: git` — Git isn't installed
- `command not found: code` — VS Code CLI isn't enabled (VS Code → Command Palette → "Shell Command: Install 'code' command in PATH")

Screenshot all six outputs in a single terminal window. This is your Assignment 2, deliverable 1.

---

### CREATE THE COURSE FOLDER (7:30–9:00)

```bash
cd ~/Documents
mkdir ism2411
cd ism2411
mkdir module01 module02 module03 module04 module05
cd module02
pwd
```

Output: `/Users/yourname/Documents/ism2411/module02`

You now have the folder structure for the first five modules.

---

### FIRST SCRIPT (9:00–11:00)

Create a Python file:
```bash
touch hello_ism2411.py
code hello_ism2411.py
```

VS Code opens the file. Type this — do not paste, type it so your fingers learn the syntax:

```python
# hello_ism2411.py
# ISM2411 — Python for Business
# Module 2 — environment verification

print("Hello, ISM2411!")

course  = "Python for Business"
modules = 16
credit_hours = 3

print(f"Course: {course}")
print(f"Modules: {modules}")
print(f"Expected weekly hours: {credit_hours * 2}")
print("Environment verified. Module 2 complete.")
```

Save (`Cmd+S` / `Ctrl+S`). Return to the terminal:

```bash
python3 hello_ism2411.py
```

Output:
```
Hello, ISM2411!
Course: Python for Business
Modules: 16
Expected weekly hours: 6
Environment verified. Module 2 complete.
```

If you see that output, your environment is working correctly.

---

### COMMON PROBLEMS (11:00–13:00)

**`python3: command not found`** — Python isn't in your PATH. On Mac, try reinstalling from python.org. On WSL, run `sudo apt install python3`.

**`SyntaxError` immediately** — you have a typo. Read the error message: it gives you the line number. Check that line for missing colons, unclosed quotes, or mismatched parentheses.

**Script runs but nothing prints** — you forgot to save the file before running. Save with `Cmd+S`/`Ctrl+S`, then run again.

**`No such file or directory`** — your terminal isn't in the same folder as your `.py` file. Use `pwd` to check where you are, and `cd` to navigate to the right folder.

**Wrong Python version** — `python3 --version` shows 3.8 or lower. Update Python from python.org.

---

### RECAP (13:00–14:00)

- Install VS Code from code.visualstudio.com
- Install Python 3.10+ from python.org (or via apt on WSL)
- Install the Python extension in VS Code
- Run the 6 verification commands — screenshot them all in one window
- Create your course folder structure with `mkdir`
- Write your first script with `touch` + `code`, run with `python3`
- Always use `python3`, not `python`
- Always save before running

Module 3: variables, data types, and your first real business script.
