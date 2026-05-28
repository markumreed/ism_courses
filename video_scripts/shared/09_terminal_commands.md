# Video 09: 5 Core Terminal Commands

## YouTube Metadata

**Title:** 5 Terminal Commands Every Python Developer Needs | ISM2411 / ISM3232
**Description:**
Before you can run Python scripts professionally, you need to navigate the file system from the command line. This video teaches the five commands you'll use every single day: pwd, ls, cd, mkdir, and touch — through a practical project setup scenario.

You'll understand paths (absolute vs relative), learn the mental model of the directory tree, and set up a real course project folder from scratch without touching a GUI.

**Chapters:**
0:00 — Why the terminal matters
1:00 — Opening the terminal in VS Code
2:00 — pwd — where am I?
3:30 — ls — what's here?
5:00 — cd — move around
7:30 — mkdir — create folders
9:30 — touch — create files
11:00 — Absolute vs relative paths
13:00 — Putting it together: project setup
14:30 — Recap

**Applies to:** ISM2411 Module 2 · ISM3232 Module 2

**Tags:** terminal commands, command line, pwd ls cd mkdir, bash zsh terminal, python terminal, developer setup, ISM2411, ISM3232, python beginner, terminal tutorial, file system, command prompt alternative

---

## Script

### INTRO (0:00–1:00)

Every professional Python developer works from the terminal. Not because GUIs are bad — because the terminal is faster, more precise, and scriptable. When you run a Python file, install a package, or push code to GitHub, it all happens from the command line.

In this video we're going to learn five commands. That's it. Five commands are enough to navigate your entire computer, create your project structure, and run your first Python script. Let's open the terminal in VS Code.

---

### OPENING THE TERMINAL (1:00–2:00)

In VS Code: **Terminal → New Terminal** (or `` Ctrl+` `` on Windows/Linux, `` Cmd+` `` on Mac).

A terminal panel opens at the bottom. You'll see a prompt — something like:

```
markum@MacBook ~ %
```

Breaking it down: `markum` is your username. `MacBook` is the machine. `~` is your current location (home directory). `%` is the prompt character — it means "ready for your command." On some systems you'll see `$` instead. Both mean the same thing: the shell is waiting.

---

### pwd — WHERE AM I? (2:00–3:30)

`pwd` stands for **Print Working Directory**. It tells you exactly where you are in the file system.

```bash
pwd
```

Output:
```
/Users/markum
```

This is an absolute path — the full address from the root of the file system down to your current location. Think of it like a GPS coordinate: `/Users/markum` means "starting from the very top of the disk, go into `Users`, then into `markum`."

On Windows in WSL you'll see: `/home/markum` or similar.

Use `pwd` any time you feel lost. It's the "you are here" marker on the map.

---

### ls — WHAT'S HERE? (3:30–5:00)

`ls` stands for **list** — it shows you the contents of your current directory.

```bash
ls
```

Output (varies by machine):
```
Desktop   Documents   Downloads   Movies   Music   Pictures
```

Useful flags:
```bash
ls -l    # long format — shows permissions, size, date
ls -la   # long format + hidden files (files starting with .)
ls -lh   # long format + human-readable sizes (KB, MB)
```

The `-a` flag reveals hidden files — files whose names start with a dot. `.zshrc`, `.gitignore` — these are important configuration files you'll work with in ISM3232.

---

### cd — MOVE AROUND (5:00–7:30)

`cd` stands for **change directory**. It's how you move.

```bash
cd Documents
pwd
```

Output: `/Users/markum/Documents`

You just moved into Documents. To go back up one level, use `..` (two dots):

```bash
cd ..
pwd
```

Output: `/Users/markum`

`..` always means "the parent directory" — one level up.

Jump home from anywhere:
```bash
cd ~
pwd
```

Output: `/Users/markum`

`~` (tilde) is a shorthand for your home directory. `cd ~` takes you home no matter where you are.

Navigate multiple levels at once:
```bash
cd ~/Documents/ism2411
```

This goes from wherever you are, back to home, then into Documents, then into ism2411. Combine `~` with subdirectory names to jump directly to any location.

**Tab completion** — type the first few letters of a folder name and press Tab. The shell completes it for you. This is faster and eliminates typos.

```bash
cd Do[Tab]  →  cd Documents/
```

---

### mkdir — CREATE FOLDERS (7:30–9:30)

`mkdir` stands for **make directory**. It creates a new folder.

```bash
cd ~/Documents
mkdir ism2411
ls
```

You now have an `ism2411` folder in Documents. Move into it:

```bash
cd ism2411
```

Create a module subfolder:

```bash
mkdir module01_what_is_a_computer
cd module01_what_is_a_computer
pwd
```

Output: `/Users/markum/Documents/ism2411/module01_what_is_a_computer`

Create multiple folders at once:

```bash
mkdir module02_terminal module03_variables module04_operators
ls
```

---

### touch — CREATE FILES (9:30–11:00)

`touch` creates a new empty file (or updates the timestamp of an existing one).

```bash
cd ~/Documents/ism2411/module01_what_is_a_computer
touch notes.txt
touch first_script.py
ls
```

Output:
```
first_script.py   notes.txt
```

Now open the Python file in VS Code:

```bash
code first_script.py
```

This opens VS Code with the file ready to edit. Type some code, save, then run it from the terminal:

```bash
python3 first_script.py
```

This is the workflow: create with `touch`, edit with `code`, run with `python3`.

---

### ABSOLUTE VS RELATIVE PATHS (11:00–13:00)

This is the concept that confuses most beginners. Let's nail it.

An **absolute path** starts from the root (`/`). It works no matter where you currently are.

```bash
cd /Users/markum/Documents/ism2411
```

A **relative path** starts from where you currently are. It's shorter but only works correctly from the right location.

```bash
# If you're already in /Users/markum/Documents:
cd ism2411   # relative — works only from Documents

# If you're in /Users/markum/Downloads:
cd ism2411   # relative — would fail because ism2411 isn't here
```

Think of it like giving directions. "Turn left at the light" (relative — only makes sense from a specific starting point). "123 Main Street, Tampa FL" (absolute — works from anywhere).

In Python scripts, **use relative paths for files in your project** so the script works on any machine:

```python
# Relative — works anywhere the script is run from the project root:
with open("data/sales.csv") as f:
    ...

# Absolute — only works on your specific machine:
with open("/Users/markum/Documents/ism2411/data/sales.csv") as f:
    ...
```

---

### PUTTING IT TOGETHER (13:00–14:30)

Full project setup from scratch — one command per line:

```bash
cd ~/Documents
mkdir ism2411
cd ism2411
mkdir module01 module02 module03 module04
cd module01
touch hello_business.py
code hello_business.py
```

In VS Code, type:

```python
print("ISM2411 — Python for Business")
print("Terminal setup complete.")
```

Save. Back in the terminal:

```bash
python3 hello_business.py
```

Output:
```
ISM2411 — Python for Business
Terminal setup complete.
```

You navigated with `cd`, checked location with `pwd`, created structure with `mkdir`, created files with `touch`, and ran Python. That's the complete workflow.

---

### RECAP (14:30–15:00)

- `pwd` — where am I?
- `ls` — what's in this directory? (`ls -la` for all files)
- `cd folder` — move into folder
- `cd ..` — go up one level
- `cd ~` — go home from anywhere
- `mkdir name` — create a directory
- `touch file.py` — create an empty file
- **Absolute paths** start with `/` — work from anywhere
- **Relative paths** start from current location — shorter, more portable
- Tab completion is your friend

Next video: Git basics — tracking your code changes with `git add`, `git commit`, and `git push`.
