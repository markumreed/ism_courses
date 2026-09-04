# ISM2411 Lab W02: First Terminal Session & First Python Script

## YouTube Metadata

**Title:** First Terminal Session & First Python Script — Full Lab Walkthrough | ISM2411 Lab 02
**Description:**
Step-by-step, test-as-you-go walkthrough of ISM2411 Module 2 Lab. Every terminal command run one at a time with its exact expected output — pwd, ls, mkdir, cd — verify Python and pip, write and run two hello.py scripts, deliberately break one to read a real error message, then run a script from the wrong directory to see exactly why paths matter.

Course page: https://markumreed.github.io/ism2411/pages/week02_lab.html
Published video: https://youtu.be/giKZfTMnJyE

**Chapters:**
0:00 — What this lab covers — first time in the terminal
0:40 — Exercise 1: pwd, ls, mkdir, cd — terminal warm-up
1:50 — Exercise 2: verify Python and pip
2:40 — Exercise 3: write and run hello.py
3:50 — Exercise 4: cd up and back, confirming with pwd
4:50 — Exercise 5: a second hello.py in a subfolder
5:50 — Exercise 6: break the script on purpose, read the error
7:20 — Exercise 7: run from the wrong directory
8:50 — Stretch A: the five-line intro.py
9:50 — Stretch B: install and test the requests package
10:50 — Reflection questions
11:30 — Submission checklist

**Applies to:** ISM2411 Module 02

**Tags:** first python script tutorial, terminal basics beginners, python syntaxerror explained, python nameerror explained, ISM2411, USF, python for business beginners

---

## How to Use This Script

**SAY** it, **DO** it, **CHECK** the exact output, **FIX** it if it doesn't match — then move to the next step. This is most students' first time typing real commands into a terminal, so every single command gets its own checkpoint before moving on.

---

## Script

### INTRO (0:00–0:40)

**SAY:** "Lab 2 — your first terminal session and your first Python script. This is the moment the class stops being theory and starts being hands-on. Every command I run, I'm going to show you the exact expected output before moving to the next one — that's the habit to build starting today."

---

### EXERCISE 1 — Terminal Warm-Up (0:40–1:50)

**SAY:** "Four commands: where am I, what's here, make a new folder, move into it."

**DO:**
```bash
pwd
ls
mkdir ism2411
cd ism2411
pwd
```

**CHECK:** The first `pwd` shows your current location (e.g., `/Users/yourname`). `ls` lists whatever's already there. After `mkdir ism2411` and `cd ism2411`, the second `pwd` shows the full path *ending in* `/ism2411`:
```
/Users/yourname/ism2411
```

**FIX:** If the second `pwd` doesn't end in `/ism2411`, confirm `cd ism2411` didn't error — a common typo is capitalization (`ISM2411` vs `ism2411`), and folder names are case-sensitive on Mac/Linux.

---

### EXERCISE 2 — Verify Python (1:50–2:40)

**SAY:** "Before writing any code, confirm the tools are actually there."

**DO:**
```bash
python3 --version
pip3 --version
```

**CHECK:**
```
Python 3.11.4
pip 23.x.x from ... (python 3.11)
```
Any Python `3.10` or higher is fine.

**FIX:** If you see a version below 3.10, or `command not found`, go back to the precourse setup page and reinstall Python 3 before continuing.

---

### EXERCISE 3 — Write hello.py (2:40–3:50)

**SAY:** "Your first Python file — one line, but it's the same fundamental action every script this semester will use: write text, run it, watch it print."

**DO:** In VS Code, create `hello.py` in your `ism2411` folder:
```python
print("Hello, ISM2411!")
```
Save it, then in the terminal, from the same folder:
```bash
python3 hello.py
```

**CHECK:**
```
Hello, ISM2411!
```

**FIX:** If nothing prints, confirm you saved the file first, and that you're running the command from inside the same folder where `hello.py` lives — check with `pwd`.

---

### EXERCISE 4 — Path Practice (3:50–4:50)

**SAY:** "Now practice moving between folders using only the terminal — no clicking in Finder or Explorer."

**DO:**
```bash
cd ..
pwd
cd ism2411
pwd
```

**CHECK:** The first `pwd` shows the *parent* of `ism2411` (e.g., `/Users/yourname`). The second `pwd` shows `/Users/yourname/ism2411` again — back where you started.

---

### EXERCISE 5 — Make a Sub-Project (4:50–5:50)

**SAY:** "A second script, in its own subfolder, personalized instead of generic."

**DO:**
```bash
mkdir module02
cd module02
```
Create a second `hello.py` here:
```python
print("Alex Chen — Finance major")
```
(Replace with your own name and major.)
```bash
python3 hello.py
```

**CHECK:**
```
Alex Chen — Finance major
```
(Your own name and major will print instead.)

---

### EXERCISE 6 — Deliberate Error Experiment (5:50–7:20)

**SAY:** "Now break it on purpose — reading error messages is a skill, and the only way to build it is to see real ones and read them carefully instead of panicking."

**DO:** In `hello.py`, change `print` to `primt` (a typo):
```python
primt("Alex Chen — Finance major")
```
Run it:
```bash
python3 hello.py
```

**CHECK:**
```
Traceback (most recent call last):
  File "hello.py", line 1, in <module>
    primt("Alex Chen — Finance major")
NameError: name 'primt' is not defined
```

**SAY:** "Write down three things: (a) the line number — `line 1`. (b) the error type — `NameError`. (c) what it's telling you — Python has no idea what `primt` means, because it's not a built-in function or anything you defined; it's expecting a *name* it recognizes, and `primt` isn't one."

Now try a different typo — remove the closing parenthesis:
```python
print("Alex Chen — Finance major"
```
```bash
python3 hello.py
```

**CHECK:**
```
  File "hello.py", line 1
    print("Alex Chen — Finance major"
                                      ^
SyntaxError: unexpected EOF while parsing
```
A completely different error type — `SyntaxError` instead of `NameError` — because this time Python couldn't even finish reading the line; the missing `)` means the statement is grammatically incomplete, not just referencing an unknown name.

**FIX:** Restore both fixes — `primt` back to `print`, and the closing `)` back in place. Run once more to confirm it's back to printing cleanly.

---

### EXERCISE 7 — Run from the Wrong Directory (7:20–8:50)

**SAY:** "One more experiment, and this is the single most common early mistake: running a script from the wrong folder."

**DO:**
```bash
cd ..
python3 hello.py
```

**CHECK:**
```
python3: can't open file 'hello.py': [Errno 2] No such file or directory
```

**SAY:** "Read that carefully — Python isn't complaining about your code at all. It's saying it looked for `hello.py` in the *current* folder and it simply isn't there, because you're now one level up, in `ism2411`, not `module02` where the file actually lives."

Now run it with the correct relative path:
```bash
python3 module02/hello.py
```

**CHECK:**
```
Alex Chen — Finance major
```

**SAY:** "Same file, same content, two totally different results — purely based on where you told Python to look. `module02/hello.py` tells it: go into `module02`, then find `hello.py` there. This is exactly why `pwd` before running anything is such a useful habit."

---

### STRETCH A — Multi-Print Script (8:50–9:50)

**SAY:** "If you finish early: a slightly longer script — five labeled lines about yourself."

**DO:** Create `intro.py`:
```python
print("Name: Alex Chen")
print("Major: Finance")
print("Hometown: Tampa, FL")
print("Hobby: Rock climbing")
print("Why this course: I want to automate the reports I build in my internship")
```
```bash
python3 intro.py
```

**CHECK:** Five lines print, each with a clear `Label: value` format — confirm all five required pieces of information (name, major, hometown, hobby, reason for taking the course) are present.

---

### STRETCH B — Install and Test a Package (9:50–10:50)

**SAY:** "If you finish early: install your first third-party package — something you didn't write, that other people built and shared."

**DO:**
```bash
pip3 install requests
```
Create `test_requests.py`:
```python
import requests
print("requests version:", requests.__version__)
```
```bash
python3 test_requests.py
```

**CHECK:**
```
requests version: 2.31.0
```
(Exact version number may differ.) If a real version number prints, `requests` installed correctly — you'll use this package later in the semester to pull data from the web.

---

### REFLECTION QUESTIONS (10:50–11:30)

**DO:** Answer honestly, in your own words:
1. Before today, how did you think about navigating your computer? Has using only the terminal — no GUI — changed your mental model of where files live?
2. When you hit your first error in Exercise 6, what was your instinct — read the message carefully, or start changing things randomly? What does that tell you about your current debugging habits?
3. What would you need to do differently to run a Python script reliably on a collaborator's machine — someone with a different username and a different folder structure?

**CHECK:** Question 3 is worth pausing on: the honest answer involves *relative* paths (from Exercise 7) instead of paths hardcoded to your specific username, since `/Users/alex/...` won't exist on your collaborator's machine at all.

---

### SUBMISSION CHECKLIST (11:30–end)

- [ ] Screenshot of the terminal showing both `hello.py` outputs (Exercise 3 and Exercise 5)
- [ ] Screenshot includes (or a second screenshot shows) the output of `python3 --version`
- [ ] Exercise 6's written error analysis: line number, error type, what the message meant
- [ ] Exercise 7's two attempts and an explanation of why one failed and one succeeded
- [ ] Three reflection questions answered honestly
- [ ] Submitted to Canvas
