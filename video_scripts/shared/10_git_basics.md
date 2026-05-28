# Video 10: Git Basics — Add, Commit, Push

## YouTube Metadata

**Title:** Git Basics for Students — Add, Commit, Push Explained | ISM2411 / ISM3232
**Description:**
Git is the version control system used by every professional software team. In this video you'll learn the three commands you need every time you save work: git add, git commit, and git push — through a practical script-writing scenario.

You'll understand what Git is actually tracking, why commit messages matter, and how to set up a repository and push to GitHub. No prior Git experience required.

**Chapters:**
0:00 — What Git does and why it matters
1:30 — git init — start tracking a project
3:00 — git status — what has changed?
4:30 — git add — stage your changes
6:30 — git commit — save a snapshot
9:00 — git log — view your history
10:30 — Connecting to GitHub
12:00 — git push — upload your work
13:30 — The daily workflow
14:30 — Recap

**Applies to:** ISM2411 Module 8 · ISM3232 Module 4

**Tags:** git tutorial, git basics, git add commit push, git for beginners, github tutorial, version control, ISM2411, ISM3232, git init, git status, git log, python git, student git tutorial

---

## Script

### INTRO (0:00–1:30)

Imagine you're working on a Python script for your capstone project. You make a change, it breaks everything, and you can't remember what it looked like before. Or you accidentally delete a file. Or your laptop crashes.

Git prevents all of this. Git is a version control system — it takes snapshots of your code over time so you can always go back to a working version. It's also how you submit work to GitHub and collaborate with teammates. Every professional software team uses it. Starting now, so do you.

---

### git init (1:30–3:00)

`git init` turns a regular folder into a Git repository — a folder that Git is now tracking.

```bash
cd ~/Documents/ism2411/module01
git init
```

Output:
```
Initialized empty Git repository in /Users/markum/Documents/ism2411/module01/.git/
```

Git created a hidden `.git` folder inside your project folder. That's where Git stores all the snapshots. You don't touch it directly — Git manages it.

Verify:
```bash
ls -la
```

You'll see the `.git` folder. This folder is the entire history of your project.

---

### git status (3:00–4:30)

`git status` shows you what's changed since your last snapshot.

```bash
git status
```

If you have files that Git doesn't know about yet:

```
On branch main

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	hello_business.py
	notes.txt

nothing added to commit but untracked files present
```

**Untracked** means Git sees the file but isn't watching it yet. You need to tell Git to include it. That's `git add`.

---

### git add (4:30–6:30)

`git add` stages changes — it says "include this in the next snapshot."

Add a specific file:
```bash
git add hello_business.py
```

Add all changed files at once:
```bash
git add .
```

The `.` means "everything in the current directory and below."

Check status again:
```bash
git status
```

Output:
```
On branch main

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
	new file:   hello_business.py
	new file:   notes.txt
```

Now the files are **staged** — queued up for the next snapshot. Staged files are listed in green (in most terminals). Unstaged changes are red.

Staging is a two-step process: `add` to stage, then `commit` to save. This lets you group related changes into one commit even if you have unrelated files modified at the same time.

---

### git commit (6:30–9:00)

`git commit` takes the snapshot. It permanently saves everything that's staged.

```bash
git commit -m "Add hello_business.py with first print statement"
```

The `-m` flag lets you write the commit message inline. Always include a message — it's the label on this snapshot.

Output:
```
[main (root-commit) a3f9c12] Add hello_business.py with first print statement
 2 files changed, 5 insertions(+)
 create mode 100644 hello_business.py
 create mode 100644 notes.txt
```

**Writing good commit messages.** The message should complete the sentence "This commit will ___":
- `"Add order calculation function"` ✓
- `"Fix discount rate bug in calculate_total"` ✓
- `"Update"` ✗ — too vague
- `"asdfg"` ✗ — useless

Good messages make your history readable. Six months from now you'll thank yourself.

Make a change and commit again:

```python
# In hello_business.py, add:
product = "Laptop Bag"
price = 49.99
print(f"Product: {product}, Price: ${price:.2f}")
```

```bash
git add hello_business.py
git commit -m "Add product variable and formatted print"
```

---

### git log (9:00–10:30)

`git log` shows your commit history.

```bash
git log
```

Output:
```
commit b7e2a14 (HEAD -> main)
Author: Markum Reed <markum@example.com>
Date:   Wed May 28 10:30:00 2024

    Add product variable and formatted print

commit a3f9c12
Author: Markum Reed <markum@example.com>
Date:   Wed May 28 10:15:00 2024

    Add hello_business.py with first print statement
```

Each commit has a unique hash (the long alphanumeric string), the author, the date, and the message.

Compact view:
```bash
git log --oneline
```

Output:
```
b7e2a14 (HEAD -> main) Add product variable and formatted print
a3f9c12 Add hello_business.py with first print statement
```

`HEAD` points to your most recent commit — where you currently are in the history.

---

### CONNECTING TO GITHUB (10:30–12:00)

GitHub is a website that stores your Git repositories online. It's the remote — the backup and the submission point.

1. Go to github.com, sign in, click **New repository**.
2. Name it (e.g., `ism2411-module01`), leave it public, click **Create repository**.
3. GitHub gives you a remote URL: `https://github.com/yourusername/ism2411-module01.git`

Connect your local repo to GitHub:

```bash
git remote add origin https://github.com/yourusername/ism2411-module01.git
git branch -M main
```

You only do this once per project. After that, `git push` sends to this remote automatically.

---

### git push (12:00–13:30)

`git push` uploads your local commits to GitHub.

First push (sets up the tracking relationship):
```bash
git push -u origin main
```

Output:
```
Enumerating objects: 4, done.
Counting objects: 100% (4/4), done.
Writing objects: 100% (4/4), 382 bytes | 382.00 KiB/s, done.
To https://github.com/yourusername/ism2411-module01.git
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'
```

After the first push, just:
```bash
git push
```

Go to your GitHub profile — you'll see your commits there. This is your submission and your portfolio.

---

### THE DAILY WORKFLOW (13:30–14:30)

Every time you work on a project, this is the sequence:

```bash
# 1. Make changes to your files in VS Code

# 2. See what changed:
git status

# 3. Stage everything:
git add .

# 4. Commit with a message:
git commit -m "Describe what you did"

# 5. Push to GitHub:
git push
```

Commit often — not just when you finish. Commit every time you reach a point where things are working. Small commits are easier to read and easier to undo than one giant commit at the end.

---

### RECAP (14:30–15:00)

- `git init` — start tracking a folder
- `git status` — see what's changed (run this constantly)
- `git add .` — stage everything
- `git add filename` — stage a specific file
- `git commit -m "message"` — save a snapshot with a description
- `git log --oneline` — view history
- `git remote add origin URL` — connect to GitHub (once per project)
- `git push` — upload commits to GitHub
- **Commit early, commit often** — small commits are better than big ones

Next video: GitHub workflow for class assignments — forking, cloning, and submitting.
