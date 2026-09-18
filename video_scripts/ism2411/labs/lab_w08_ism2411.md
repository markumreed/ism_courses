# ISM2411 Lab W08: Your First GitHub Submission

## YouTube Metadata

**Title:** Your First GitHub Submission — Full Lab Walkthrough | ISM2411 Lab 08
**Description:**
Step-by-step, test-as-you-go walkthrough of ISM2411 Module 8 Lab. Create a GitHub account and your first repo, add a Python-and-OS .gitignore before anything else, add your Module 7 functions.py, write a README with markdown headings and a module list, and make three separate descriptive commits.

Course page: https://markumreed.github.io/ism2411/pages/week08_lab.html

**Chapters:**
0:00 — What this lab covers — the workflow for every remaining assignment
0:45 — Exercise 1: create your GitHub account
1:30 — Exercise 2: create and clone the ism2411 repo
2:50 — Exercise 3: .gitignore before anything else
4:20 — Exercise 4: add Module 7's functions.py
5:50 — Exercise 5: write the README
7:20 — Exercise 6: three separate, descriptive commits
8:50 — Reflection questions
9:40 — Submission checklist

**Applies to:** ISM2411 Module 08

**Tags:** github first repo tutorial, git clone add commit push, gitignore python template, git log oneline, ISM2411, USF, python for business beginners

---

## How to Use This Script

**SAY** it, **DO** it, **CHECK** the exact output, **FIX** it if it doesn't match — then move to the next step. This lab establishes the exact workflow you'll repeat for every remaining assignment this semester.

---

## Script

### INTRO (0:00–0:45)

**SAY:** "Lab 8 — your first GitHub submission. Starting today, every assignment for the rest of the semester gets submitted this way: a Git repo, a `.gitignore` set up before anything else, descriptive commits, and a URL pasted into Canvas instead of a file upload. Let's build that workflow once, correctly."

---

### EXERCISE 1 — Create the Account (0:45–1:30)

**SAY:** "If you don't already have one, this is where your professional developer identity starts — pick the username carefully, since it'll be on your portfolio."

**DO:** Go to github.com and create an account using your USF email. Choose a professional username. While you're in account settings, enable two-factor authentication.

**CHECK:** You can log in at github.com and see your own profile page.

---

### EXERCISE 2 — New Repo (1:30–2:50)

**SAY:** "One repository for the whole semester — every module gets its own folder inside it."

**DO:** On github.com, click **New repository**. Name it `ism2411`. Set it **Public**. Check "Add a README." Create it, then clone it locally:
```bash
git clone https://github.com/YOURUSERNAME/ism2411.git
cd ism2411
git status
```

**CHECK:**
```
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

**FIX:** If `git clone` fails with a permissions or authentication error, confirm the URL matches exactly what GitHub showed you, including your actual username in place of `YOURUSERNAME`.

---

### EXERCISE 3 — Add a .gitignore (2:50–4:20)

**SAY:** "This is the one file that goes in *before* any real code — same principle as ISM3232's venv rule: never let generated junk or OS clutter get tracked by Git in the first place."

**DO:** Create `.gitignore` in the repo root:
```gitignore
# Python
__pycache__/
*.pyc
*.pyo
.env
*.egg-info/

# OS
.DS_Store
Thumbs.db

# Editors
.vscode/
.idea/
```
Commit and push it, before adding anything else:
```bash
git add .gitignore
git commit -m "add .gitignore for Python and OS files"
git push
```

**CHECK:**
```
[main abc1234] add .gitignore for Python and OS files
 1 file changed, 11 insertions(+)
```
followed by a successful push with no errors.

---

### EXERCISE 4 — Add Module 7 Work (4:20–5:50)

**SAY:** "Now the first real code — last week's `functions.py`, moved into its own dated folder."

**DO:** From inside `ism2411/`:
```bash
mkdir week07
cp /path/to/your/functions.py week07/
git status
```

**CHECK:**
```
Untracked files:
  (use "git add <file>..." to include in what will be committed)
        week07/functions.py
```
Confirm Git sees exactly the new file, nothing else unexpected.

**DO:**
```bash
git add week07/
git commit -m "add module 7 functions: calculate_tax, apply_discount, final_price"
git push
```

**CHECK:** Visit `https://github.com/YOURUSERNAME/ism2411` in a browser — the `week07/` folder is visible, and the latest commit message matches exactly what you typed.

---

### EXERCISE 5 — Write a README (5:50–7:20)

**SAY:** "The README is the front door to your repo — anyone who lands on it, including a future employer, should immediately understand what this is and how to run it."

**DO:** Open `README.md`:
```markdown
# ISM2411 — Python for Business

**Name:** Your Name Here
**Semester:** Fall 2025
**Instructor:** [Course Instructor]

## About This Repo
This repository contains my weekly lab submissions for ISM2411.
Each folder corresponds to one module.

## Modules
- `week05/` — Conditionals: tiered discount calculator
- `week06/` — Loops: sales report with sum, average, max
- `week07/` — Functions: calculate_tax, apply_discount
- `week08/` — Git: first GitHub submission

## How to Run
Each script is standalone. Open a terminal and run:
```
python week07/functions.py
```
```
```bash
git add README.md
git commit -m "add README with module listing and run instructions"
git push
```

**CHECK:** On github.com, the README renders below the file list with proper headings (`#`, `##`) and a bulleted module list — not raw `#` characters, confirming the markdown syntax is valid.

---

### EXERCISE 6 — Three Commits (7:20–8:50)

**SAY:** "Look back at what you just did — that was already three separate, coherent commits: the `.gitignore`, the functions, and the README. That's exactly the pattern this exercise asks for: one commit per distinct change, never 'update everything at once.'"

**DO:**
```bash
git log --oneline
```

**CHECK:**
```
a3f1b2c add module 7 functions: calculate_tax, apply_discount, final_price
9d4e1a0 add .gitignore for Python and OS files
f7c2b3e add README with module listing and run instructions
```
(Your actual commit hashes will differ — the important thing is three distinct entries, each with a message describing one coherent change, not a vague one like "update stuff.")

---

**SAY:** "Confirm all three commits also show up on github.com — click into the repo's commit history and match it against your local `git log --oneline` output."

---

### REFLECTION QUESTIONS (8:50–9:40)

**DO:** Answer honestly:
1. Run `git log --oneline` in your repo and copy the output here as a comment in your submitted file. Look at your commit messages — if you were hiring someone and saw this history, what would it tell you about how they work?
2. Describe in 2–3 sentences how using Git changes (or should change) how you approach making edits to a working script. What would you do differently now compared to before this module?
3. What is one thing you would add to your `.gitignore` that's specific to your own machine or workflow, not in the starter template? Why shouldn't that file be tracked?

**CHECK:** Question 1's honest answer should reflect specifically on message *quality* — commits like "add .gitignore for Python and OS files" read very differently to a hiring manager than a history full of "fix," "update," "stuff."

---

### SUBMISSION CHECKLIST (9:40–end)

- [ ] GitHub account created, two-factor authentication enabled
- [ ] `ism2411` repository created, public, cloned locally
- [ ] `.gitignore` committed and pushed before any other files
- [ ] `week07/functions.py` added, committed, and pushed
- [ ] `README.md` with title, name, semester, description, and module list
- [ ] At least 3 separate, descriptive commits — confirmed with `git log --oneline` and on GitHub.com
- [ ] Three reflection questions answered honestly
- [ ] GitHub repository URL submitted to Canvas
