# Video 21: Setting Up Your Developer Environment

## YouTube Metadata

**Title:** Developer Environment Setup — VS Code, Python, zsh, Git | ISM3232
**Description:**
Build a professional development environment from scratch: install VS Code, Python 3, Git, and verify zsh is your shell. We'll create your course folder structure, run the 6 verification commands, and write your first ISM3232 Python script — all from the terminal.

Course page: https://markumreed.github.io/ism3232/docs/week01_lecture.html

**Chapters:**
0:00 — What a developer environment is and why it matters
1:30 — zsh — your shell
3:00 — VS Code installation and Python extension
5:00 — Python 3 installation and verification
7:00 — Git installation and configuration
9:00 — The 6 verification commands
11:00 — Course folder structure
13:00 — First script: hello_ism3232.py
15:00 — Recap and assignment

**Applies to:** ISM3232 Module 1

**Tags:** developer environment setup, VS Code Python, zsh setup, python install, git configuration, ISM3232, USF, terminal setup, python developer environment, zsh tutorial

---

## Script

### INTRO (0:00–1:30)

In most intro programming courses, the first thing you do is write `print("Hello World")`. In ISM3232, we start with your environment — because a poorly configured environment causes more bugs, more frustration, and more wasted time than any Python mistake you'll make this semester.

Professional developers spend real time getting their environment right because a good environment makes everything downstream easier. Today we build yours.

---

### zsh — YOUR SHELL (1:30–3:00)

zsh is the program that reads the commands you type and executes them. On macOS it's the default since Catalina. On Linux it may need to be installed.

Open your terminal. Your prompt should end with `%`. If it ends with `$`, you're in bash — switch to zsh:

```bash
chsh -s $(which zsh)
# Close and reopen your terminal
echo $SHELL   # should show /bin/zsh
```

On Windows: use WSL (Windows Subsystem for Linux). The pre-course tutorial covers WSL setup. Do not use Command Prompt or PowerShell for this course.

The `%` prompt is your indicator that zsh is running. Every command we type this semester goes to zsh.

---

### VS CODE (3:00–5:00)

Download from code.visualstudio.com. Install. Open.

**Required extensions:**
- Python (by Microsoft) — syntax highlighting, linting, run button
- Pylance — type checking and autocomplete
- GitLens (optional but useful) — inline Git blame and history

Install Python extension: Extensions sidebar (Ctrl+Shift+X / Cmd+Shift+X) → search "Python" → install.

Enable the `code` command in terminal: Command Palette (Cmd+Shift+P) → "Shell Command: Install 'code' command in PATH". This lets you type `code filename.py` to open files in VS Code from the terminal.

Verify:
```bash
code --version
```

---

### PYTHON 3 (5:00–7:00)

**Mac:** Download installer from python.org → Python 3.11 or higher. Run it. Verify:
```bash
python3 --version   # Python 3.11.x
```

**WSL:**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
python3 --version
```

**Critical:** always use `python3`, never `python`. On many systems `python` is Python 2 (deprecated and unsupported).

---

### GIT (7:00–9:00)

**Mac:** `xcode-select --install` installs git along with developer tools.
**WSL:** `sudo apt install git`

After installing, configure your identity — git uses this for commit messages:

```bash
git config --global user.name "Your Full Name"
git config --global user.email "your.email@example.com"
git config --global init.defaultBranch main
```

Verify:
```bash
git --version
git config --global user.name   # should print your name
```

Create a GitHub account at github.com if you don't have one. You'll push every assignment there.

---

### 6 VERIFICATION COMMANDS (9:00–11:00)

Run all six in one terminal window. Screenshot the output — this is Assignment 1, Deliverable 1.

```bash
echo $SHELL       # /bin/zsh
zsh --version     # zsh 5.x or higher
python3 --version # Python 3.10 or higher
git --version     # git version 2.x
pwd               # your home directory
ls                # Desktop, Documents, etc.
```

Every line must produce output without "command not found". If any fail:

- `command not found: python3` → Python not installed or not in PATH
- `command not found: git` → Git not installed
- `$SHELL` shows `/bin/bash` → switch to zsh with `chsh -s $(which zsh)`

---

### COURSE FOLDER STRUCTURE (11:00–13:00)

```bash
cd ~
mkdir ism3232
cd ism3232
mkdir module01_setup
cd module01_setup
pwd
```

Output: `/Users/yourname/ism3232/module01_setup`

This is your course root. Every module gets its own subfolder. Assignment files go inside the module folder.

---

### FIRST SCRIPT (13:00–15:00)

```bash
touch hello_ism3232.py
code hello_ism3232.py
```

Type this — do not paste:

```python
# hello_ism3232.py
# ISM3232 — Business Application Development
# Module 1 — Environment Verification

print("Hello, ISM3232!")

course_name  = "Business Application Development"
credit_hours = 3
weekly_hours = credit_hours * 2

print(f"Course: {course_name}")
print(f"Expected weekly hours: {weekly_hours}")
print("Environment verified. Module 1 complete.")
```

Save. Run from terminal:

```bash
python3 hello_ism3232.py
```

Expected output:
```
Hello, ISM3232!
Course: Business Application Development
Expected weekly hours: 6
Environment verified. Module 1 complete.
```

If you see those four lines, your environment works. Screenshot it — Deliverable 2 for Assignment 1.

---

### RECAP (15:00–18:00)

- **zsh** is your shell — prompt ends with `%`
- **VS Code** is your editor — install Python and Pylance extensions
- **Python 3** — always `python3`, not `python`
- **Git** — configure name and email immediately
- **6 verification commands** — run all six, screenshot in one window
- **Course folder:** `~/ism3232/module01_setup/`
- **Run scripts:** `python3 filename.py` from the same directory as the file

Module 2: zsh navigation — `pwd`, `ls`, `cd`, `mkdir`, file operations.
