# ISM2411 Lab W01: Computer Vocabulary & File System Tour

## YouTube Metadata

**Title:** Computer Vocabulary & File System Tour — Lab Walkthrough | ISM2411 Lab 01
**Description:**
Walkthrough of ISM2411 Module 1 Lab. We work through the file system vocabulary exercises, practice drawing directory trees, and confirm the five required terms are solid before moving on to coding.

No Python in this lab — it's all about building the mental model of files, paths, and directories that every future script depends on.

Course page: https://markumreed.github.io/ism2411/pages/week01_lab.html

**Chapters:**
0:00 — What this lab covers
0:30 — Exercise 1: drawing a directory tree from a path
2:30 — Exercise 2: absolute vs relative paths
4:30 — Exercise 3: nine vocabulary terms
7:00 — Exercise 4: business automation discussion
9:00 — Submission checklist

**Applies to:** ISM2411 Module 01

**Tags:** file system tour, directory tree python, absolute vs relative path, python for beginners, ISM2411, USF, computer science basics, what is a file path

---

## Script

### INTRO (0:00–0:30)

This is the walkthrough for ISM2411 Lab 1 — Computer Vocabulary and File System Tour. There's no Python code today. The goal is to lock in the vocabulary: files, directories, paths, CPU, RAM, storage. Every script you write for the rest of the semester assumes you know this model cold. Let's go.

---

### EXERCISE 1 — DRAWING A DIRECTORY TREE (0:30–2:30)

The lab gives you a path and asks you to draw the directory hierarchy it implies.

Let's use `/Users/alice/ism2411/module01/notes.txt`.

Start at the root: `/`
Inside root: `Users/`
Inside Users: `alice/`
Inside alice: `ism2411/`
Inside ism2411: `module01/`
Inside module01: `notes.txt`

Draw it as a tree, indenting one level per directory:

```
/
└── Users/
    └── alice/
        └── ism2411/
            └── module01/
                └── notes.txt
```

The key insight: every path tells you exactly how to navigate from the root to the file. No guessing.

Now the other direction — the lab also asks you to write the path from a tree. Read the tree, write the path from root to file. Start at `/`, follow each branch, separate with `/`.

---

### EXERCISE 2 — ABSOLUTE VS RELATIVE PATHS (2:30–4:30)

Absolute path: starts from the root. Works from anywhere.
```
/Users/alice/ism2411/module01/notes.txt
```

Relative path: starts from where you are right now.
If you're in `/Users/alice/ism2411/`:
```
module01/notes.txt
```

If you're in `/Users/alice/`:
```
ism2411/module01/notes.txt
```

The lab asks: when would you use each? Use absolute paths when you're not sure where the script will run from. Use relative paths in your code — they work on any machine as long as the folder structure is the same.

`..` means "go up one level." So if you're in `module01/` and you want `module02/notes.txt`:
```
../module02/notes.txt
```

---

### EXERCISE 3 — NINE VOCABULARY TERMS (4:30–7:00)

The lab asks you to define these nine terms in your own words. Let me give you the one-sentence version for each — then use your own words in the submission.

- **CPU** — the chip that executes your program's instructions, one at a time.
- **RAM** — fast, temporary memory where running programs and open files live. Cleared on shutdown.
- **Storage** — slower, permanent memory where files live when the computer is off.
- **File** — a named sequence of bytes stored on disk.
- **Directory** — a container for files and other directories. Also called a folder.
- **Path** — the full address of a file in the directory hierarchy.
- **Root** — the top of the hierarchy: `/` on Mac/Linux, `C:\` on Windows.
- **Interpreter** — the program that reads and executes Python code line by line.
- **Script** — a plain text file containing Python instructions, saved with a `.py` extension.

---

### EXERCISE 4 — BUSINESS AUTOMATION DISCUSSION (7:00–9:00)

The lab asks: what tasks in your future career could be automated with Python?

Think about repetitive work: reports that get pulled manually every Monday, spreadsheets that get cleaned by hand, data that gets copied from one system to another. Any of those is a Python script waiting to happen.

You're not expected to know how to build it yet — just identify it. That's the point of the exercise: start seeing automation opportunities before you can write the code.

---

### SUBMISSION CHECKLIST (9:00–10:00)

Before you close out:
- Directory tree drawn correctly from the given path
- Absolute and relative path both written correctly for each example
- All nine vocabulary terms defined in your own words
- Business automation response written (2–3 sentences minimum)
- Submitted to Canvas

That's Lab 1. Next lab we open the terminal for real.
