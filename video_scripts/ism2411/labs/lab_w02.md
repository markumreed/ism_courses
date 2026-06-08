# ISM2411 Lab W02: First Terminal Session & First Python Script

## YouTube Metadata

**Title:** First Terminal Session & First Python Script — Lab Walkthrough | ISM2411 Lab 02
**Description:**
Walkthrough of ISM2411 Module 2 Lab. We open the terminal for the first time, run the five core commands, install Python and VS Code, and execute hello.py from the command line.

**Chapters:**
0:00 — What this lab covers
0:30 — Opening the terminal and running pwd, ls, cd, mkdir
3:00 — Creating the ism2411 project folder structure
5:00 — Installing Python and VS Code (verify versions)
6:30 — Writing and running hello.py
8:30 — Submission checklist

**Applies to:** ISM2411 Module 02

**Tags:** python terminal tutorial, first python script, vs code python setup, command line basics, ISM2411, USF, python for beginners, terminal commands mac

---

## Script

### INTRO (0:00–0:30)

Lab 2 — First Terminal Session and First Python Script. By the end of this we'll have Python and VS Code installed, a project folder set up, and a working hello.py running from the terminal. Let's go.

---

### FIVE CORE COMMANDS (0:30–3:00)

Open your terminal. On Mac: Spotlight → Terminal. On Windows: search for "PowerShell" or install Windows Terminal.

The five commands you need:

```bash
pwd        # where am I?
ls         # what's here?
cd folder  # move into folder
mkdir name # create a new folder
cd ..      # go up one level
```

Let's use them. Open a terminal and follow along:

```bash
pwd
# output: /Users/yourname  (or wherever your home directory is)

ls
# output: Desktop  Documents  Downloads  ...

mkdir ism2411
ls
# ism2411 is now in the list

cd ism2411
pwd
# /Users/yourname/ism2411

mkdir module01 module02 module03
ls
# module01  module02  module03
```

Practice going up:
```bash
cd ..
pwd
# back to /Users/yourname
```

This is the whole navigation model. You'll use these same commands every single lab.

---

### PROJECT FOLDER STRUCTURE (3:00–5:00)

The lab asks you to build this structure:

```
ism2411/
├── module01/
├── module02/
└── module03/
```

Build it entirely from the terminal — no drag-and-drop, no Finder/Explorer. That's the point.

```bash
cd ism2411
mkdir module01 module02 module03
ls
```

Verify with `ls` at each level. If you make a mistake with a folder name, `mv oldname newname` renames it.

---

### INSTALLING PYTHON AND VS CODE (5:00–6:30)

If you haven't installed yet:

**Python:** Download from python.org. On Mac, you can also use `brew install python3`. Verify:
```bash
python3 --version
# Python 3.x.x
```

**VS Code:** Download from code.visualstudio.com. Install the Python extension from the Extensions sidebar.

The lab's verification step:
```bash
python3 --version
code --version
```

Both should print version numbers without errors.

---

### HELLO.PY (6:30–8:30)

In VS Code, create a new file. Save it as `hello.py` inside `ism2411/module02/`.

```python
# hello.py
print("Hello, ISM2411!")
print("My name is [Your Name]")
print("Python is running.")
```

Now run it from the terminal:
```bash
cd ~/ism2411/module02
python3 hello.py
```

Output:
```
Hello, ISM2411!
My name is [Your Name]
Python is running.
```

If you get a `command not found` error on `python3`, try `python` (no 3). If that fails, Python isn't on your PATH — reinstall and restart the terminal.

The most common mistake: running the script from the wrong directory. Always `cd` to the folder containing the file first, then run `python3 filename.py`.

---

### SUBMISSION CHECKLIST (8:30–10:00)

- Five commands practiced: `pwd`, `ls`, `cd`, `mkdir`, `cd ..`
- `ism2411/` folder with at least three subfolders created from terminal only
- Python and VS Code installed, both version-checked
- `hello.py` created with your name, runs without errors
- Submitted to Canvas

Lab 2 done. Next lab we write our first real program.
