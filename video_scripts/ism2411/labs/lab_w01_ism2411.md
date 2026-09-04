# ISM2411 Lab W01: Computer Vocabulary & File System Tour

## YouTube Metadata

**Title:** Computer Vocabulary & File System Tour — Full Lab Walkthrough | ISM2411 Lab 01
**Description:**
Step-by-step, test-as-you-go walkthrough of ISM2411 Module 1 Lab. No coding yet — this lab builds the mental model every future script depends on: tracing a real file path on your own machine, building the ism2411 project folder, defining nine core vocabulary terms, spotting automation opportunities, drawing a directory tree from three given paths, and reasoning through RAM-vs-storage scenarios.

Course page: https://markumreed.github.io/ism2411/pages/week01_lab.html
Published video: https://youtu.be/1WZVu0PDNwM

**Chapters:**
0:00 — What this lab covers — no code yet
0:40 — Exercise 1: trace a real file path on your machine
2:10 — Exercise 2: build the ism2411 project folder
3:20 — Exercise 3: nine vocabulary terms, one sentence each
5:30 — Exercise 4: automation reflection
6:50 — Exercise 5: draw the directory tree from three paths
9:00 — Exercise 6: RAM vs. storage scenarios
11:00 — Stretch A: read an unfamiliar .py file line by line
12:10 — Stretch B: research pandas memory use
13:00 — Reflection questions
13:40 — Submission checklist

**Applies to:** ISM2411 Module 01

**Tags:** file system tour, directory tree python, absolute vs relative path, python for beginners, ISM2411, USF, computer science basics, what is a file path, RAM vs storage explained

---

## How to Use This Script

Every exercise below has three parts: **SAY** — what to explain out loud before doing the exercise. **DO** — the exercise itself, worked through fully as an example. **CHECK** — how to know your answer matches what the lab expects, using the "Expected" hint from the lab page as the test.

---

## Script

### INTRO (0:00–0:40)

**SAY:** "Lab 1 — computer vocabulary and a file system tour. No Python today. Before you write a single line of code, you need a rock-solid mental model of what a file actually is, where it lives, and how the computer finds it. Everything for the rest of the semester assumes this is second nature."

---

### EXERCISE 1 — Trace a Real File Path (0:40–2:10)

**SAY:** "This one uses your actual machine, not a hypothetical example."

**DO:** Open Finder (Mac) or File Explorer (Windows). Navigate to your Downloads folder, pick any file, right-click it, and choose Properties (Windows) or Get Info (Mac). Copy the full path shown there. For example:
```
/Users/yourname/Downloads/syllabus.pdf
```
Break it into its four labeled parts:
- **Root:** `/` (the very top of the whole filesystem)
- **Directory chain:** `Users/yourname/Downloads/` (the sequence of folders you pass through)
- **Filename:** `syllabus`
- **Extension:** `.pdf` (tells the OS and applications what kind of file this is, and which program should open it)

**CHECK:** Your written answer should look like a fully labeled path — for example: "Root: `/`. Directory chain: `Users → yourname → Downloads`. Filename: `syllabus`. Extension: `.pdf`." That matches the lab's expected output: a written-out path with each component labeled.

---

### EXERCISE 2 — Map Your Project Folder (2:10–3:20)

**SAY:** "This folder is where every assignment for the rest of the semester lives — build it once, correctly, now."

**DO:** On your machine, create a folder called `ism2411` wherever you keep schoolwork. Inside it, create one subfolder per unit:
```
ism2411/
├── unit1/
├── unit2/
├── unit3/
└── ...
```

**CHECK:** Open Finder/Explorer and confirm you can see the `ism2411` folder with its numbered `unitN` subfolders inside — that's the lab's expected output: "folder structure visible in Finder/Explorer."

---

### EXERCISE 3 — Vocabulary Check (3:20–5:30)

**SAY:** "Nine terms, one sentence each, in your own words — not copied from the reading. I'll give you the one-sentence version for each; rewrite them in your own phrasing before submitting."

**DO:**
- **CPU** — the chip that executes your program's instructions, one at a time.
- **RAM** — fast, temporary memory where running programs and open files live; it clears when the computer shuts down.
- **Storage** — slower, permanent memory where files live even when the computer is off.
- **File** — a named sequence of bytes stored on disk.
- **Directory** — a container for files and other directories; also called a folder.
- **Path** — the full address of a file within the directory hierarchy.
- **Extension** — the suffix after the dot in a filename (like `.pdf` or `.py`) that tells the OS and applications what kind of file it is.
- **Program** — a set of instructions that tells the computer what to do.
- **Interpreter** — the program that reads and executes another program's instructions, one line at a time (Python code specifically, for this course).

**CHECK:** Nine one-sentence definitions, written in your own words — the lab's expected output. Read each one back out loud: if it sounds identical to a textbook sentence, rewrite it in your own phrasing.

---

### EXERCISE 4 — Automation Reflection (5:30–6:50)

**SAY:** "Discuss this one in pairs if you're in class — the goal is spotting opportunities, not solving them yet."

**DO:** Name three things you currently do in Excel that take more than 10 minutes. For example:
1. Manually copying last week's sales numbers into a summary tab every Monday morning.
2. Reformatting a CSV export from another system so the columns match your template.
3. Cross-checking two spreadsheets by eye to find rows that don't match.

For each, ask: could a program that runs in a few seconds do this instead?

**CHECK:** Three tasks described, each with a brief explanation of why it could (or couldn't yet) be automated — the lab's expected output. You are not expected to know *how* to automate it yet — only to recognize *that* it could be.

---

### EXERCISE 5 — Draw the Directory Tree (6:50–9:00)

**SAY:** "Now the reverse direction from Exercise 1 — given paths, draw the tree they imply."

**DO:** Given these three paths:
```
/home/alice/projects/q1_report/data/sales.csv
/home/alice/projects/q1_report/scripts/summary.py
/home/alice/projects/q2_report/data/sales.csv
```
Draw the tree, merging shared folders and branching where paths diverge:
```
/home/alice/projects/
├── q1_report/
│   ├── data/
│   │   └── sales.csv
│   └── scripts/
│       └── summary.py
└── q2_report/
    └── data/
        └── sales.csv
```

**CHECK:** Notice `q1_report` and `q2_report` both branch off the same `projects/` folder — that's the key insight this exercise tests: shared path prefixes mean shared parent folders. Now write one *relative* path from `scripts/summary.py` to `q2_report/data/sales.csv`:
```
../../q2_report/data/sales.csv
```
Read it out loud: "Starting in `scripts/`, `..` goes up to `q1_report/`, a second `..` goes up to `projects/`, then back down into `q2_report/data/sales.csv`." That's the lab's expected output: a tree diagram plus that exact relative path.

---

### EXERCISE 6 — RAM vs. Storage Scenarios (9:00–11:00)

**SAY:** "Three scenarios, and for each one: is this a RAM problem, a storage problem, or something else?"

**DO:**

**(a)** You edited a spreadsheet for an hour and your laptop died. When you restart, your changes are gone.
— This is a **RAM** problem: your unsaved edits existed only in fast, temporary memory. Since you never saved (wrote them to storage), losing power erased them completely.

**(b)** You try to open a CSV file and get an error saying the file cannot be found.
— This is a **storage** problem: either the file's path is wrong, or the file itself doesn't exist where you're looking — nothing to do with RAM at all.

**(c)** Your Python script is running slowly when processing a 2 GB file.
— This is a **storage I/O or RAM capacity** problem: reading 2 GB off disk takes real time, and if your machine doesn't have enough RAM to hold the whole file while processing it, the OS has to shuffle data back and forth between RAM and storage, which is much slower than RAM alone.

**CHECK:** Your three answers should match: (a) RAM — changes not saved to storage; (b) storage — file path wrong or file missing; (c) storage I/O or RAM capacity. That's the lab's expected output.

---

### STRETCH A — Read an Unfamiliar .py File (11:00–12:10)

**SAY:** "If you finish early: find any short Python script online — 5 to 15 lines — and explain it line by line, even if you're guessing at some of it."

**DO:** Search for a short `.py` file (a simple example script from documentation works well). Open it in a text editor. For each line, write one sentence explaining what it does — for example: "Line 1 imports the `math` library so the script can use functions like `sqrt`." "Line 3 defines a variable called `radius` and sets it to `5`."

**CHECK:** Every line has a one-sentence explanation, even lines you're not 100% sure about — the point of this exercise is practicing the skill of reading unfamiliar code, which you'll do constantly in your career, long before you can write everything from scratch yourself.

---

### STRETCH B — Research: How Much RAM Do Real Workloads Need? (12:10–13:00)

**SAY:** "If you finish early: a short research question connecting today's vocabulary to real data-analysis work."

**DO:** Look up: how much RAM does Python typically use to hold a pandas DataFrame with 1 million rows and 10 columns of floats? Write 3–4 sentences explaining why this matters for analysts working with large datasets.

**CHECK:** Your answer should connect back to today's vocabulary — RAM is the fast, temporary memory that has to hold the *entire* dataset while you're working with it, so a dataset that's larger than your available RAM will be slow or will fail to load at all, which is exactly why data analysts care about file size and available memory before they even open a large CSV.

---

### REFLECTION QUESTIONS (13:00–13:40)

**SAY:** "Three self-assessment questions — no code, just honest reflection before you submit."

**DO:** Answer, in your own words:
1. Before this module, how would you have explained what happens when you open an Excel file? How has your answer changed?
2. Which of the nine vocabulary terms from Exercise 3 are you least confident about? What would help you solidify that concept?
3. The business discussion (Exercise 4) asked about tasks you could automate. What would you need to learn — beyond this module — to actually build that automation?

**CHECK:** Each answer is a few honest sentences, not a restatement of the definitions — this is where you notice which concepts didn't quite stick yet, before the course moves on.

---

### SUBMISSION CHECKLIST (13:40–end)

**SAY:** "No code submission this module — bring these to class instead."

- [ ] Written, labeled file path from Exercise 1 (root, directory chain, filename, extension)
- [ ] `ism2411/` folder with one subfolder per unit, visible in Finder/Explorer
- [ ] All nine vocabulary terms defined in your own words
- [ ] Three automation examples from Exercise 4, with explanations
- [ ] Directory tree drawn from Exercise 5's three paths, plus the relative path
- [ ] All three RAM-vs-storage scenarios from Exercise 6 answered with reasoning
- [ ] Three reflection questions answered honestly
- [ ] Brought to class (no Canvas code submission this week)
