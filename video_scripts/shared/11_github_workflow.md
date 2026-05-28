# Video 11: GitHub Workflow for Class Assignments

## YouTube Metadata

**Title:** GitHub Workflow for Class — Clone, Commit, Submit | ISM2411 / ISM3232
**Description:**
This video covers the exact GitHub workflow used in ISM2411 and ISM3232: creating a repository for each assignment, working locally, committing progress, pushing to GitHub, and submitting the URL on Canvas. We also cover the most common setup mistakes that cause submissions to fail.

**Chapters:**
0:00 — The assignment submission workflow
1:30 — Creating a new repo for an assignment
3:00 — Cloning to your local machine
5:00 — The work cycle: edit, add, commit, push
8:00 — Verifying your submission on GitHub
9:30 — Common setup mistakes
11:00 — .gitignore — keeping secrets out
13:00 — Recap

**Applies to:** ISM2411 Module 8 · ISM3232 Module 4

**Tags:** github workflow, github for students, git clone, github assignment, canvas submission, ISM2411, ISM3232, git push, github tutorial, python github, student workflow, github submit

---

## Script

### INTRO (0:00–1:30)

Now that you know the Git commands, let's talk about the actual workflow for class assignments. Every assignment in this course gets its own GitHub repository. You'll create it on GitHub, clone it to your computer, do your work, commit and push regularly, and submit the GitHub URL to Canvas. That's it. Let's walk through it exactly once so you never have to guess.

---

### CREATING A REPO (1:30–3:00)

For each assignment, create a new repository on GitHub:

1. github.com → click your avatar → **Your repositories** → **New**
2. **Repository name:** use a consistent pattern — `ism2411-module03-variables` or `ism3232-module05-variables`
3. **Description:** one sentence about the assignment
4. **Public** (so your instructor can see it)
5. Check **Add a README file** — this creates an initial commit so you can clone immediately
6. Click **Create repository**

You now have a remote repo. The next step is getting it onto your computer.

---

### CLONING (3:00–5:00)

Cloning downloads the repository to your machine and sets up the remote connection automatically.

On the repo page on GitHub, click the green **Code** button, then copy the HTTPS URL:
```
https://github.com/yourusername/ism2411-module03-variables.git
```

In your terminal, navigate to where you want the project:
```bash
cd ~/Documents/ism2411
git clone https://github.com/yourusername/ism2411-module03-variables.git
cd ism2411-module03-variables
ls
```

You'll see the README.md file. The folder is already a Git repo with the remote configured. No `git init`, no `git remote add` needed — `clone` handles all of it.

---

### THE WORK CYCLE (5:00–8:00)

Now you work. Create your Python files, write your code, test it.

```bash
touch variables_lab.py
code variables_lab.py
```

Write your solution, save it. Then commit:

```bash
git add .
git commit -m "Add variables lab — product record and type conversion"
git push
```

Do this every time you reach a checkpoint — not just at the end. If something breaks later, you can go back to the last good commit.

**Multiple commits on one assignment is normal and expected.** A history like this shows professional work:

```
c4a1b3e Add final summary print with formatted totals
b8e2f9a Fix type conversion bug on user input
a7d1c0e Add discount calculation and conditional logic
9f3e2b1 Add initial product record and basic print
```

A single commit called "final submission" tells your instructor you worked in one sitting without testing or iteration.

---

### VERIFYING ON GITHUB (8:00–9:30)

Before submitting, verify your work is actually on GitHub:

1. Go to your repo on github.com
2. Confirm your files are visible — click on your `.py` file and read the code
3. Check the commit count — top of the file list shows "N commits"
4. Check the latest commit message is what you expect

If your files aren't there, your push didn't work. Common causes: you were in the wrong directory, or you forgot to `git add` before committing.

Submit on Canvas: paste the full GitHub URL — e.g., `https://github.com/yourusername/ism2411-module03-variables`

---

### COMMON MISTAKES (9:30–11:00)

**"I committed but my files aren't on GitHub."** You forgot to `git push`. Commits are local until pushed.

**"I pushed but the files are empty."** You forgot to save in VS Code before committing. Save with `Cmd+S` / `Ctrl+S` before every `git add`.

**"git push says 'rejected'."** Your local is behind the remote. Pull first:
```bash
git pull
git push
```

**"I'm getting 'not a git repository'."** You're not inside the project folder. Use `pwd` to check, then `cd` into the right directory.

**Committing to the wrong repo.** Always check `git remote -v` to see which remote you're connected to:
```bash
git remote -v
```

Output:
```
origin  https://github.com/yourusername/ism2411-module03-variables.git (fetch)
origin  https://github.com/yourusername/ism2411-module03-variables.git (push)
```

---

### .gitignore — KEEPING THINGS OUT (11:00–13:00)

Some files should never go to GitHub: virtual environment folders, compiled files, API keys, `.DS_Store` (Mac finder metadata).

Create a `.gitignore` file in your project root:

```bash
touch .gitignore
code .gitignore
```

Add patterns for things Git should ignore:

```
# Virtual environment
venv/
.venv/
env/

# Python compiled files
__pycache__/
*.pyc

# Environment variables (API keys, secrets)
.env

# Mac finder
.DS_Store

# VS Code settings
.vscode/
```

After saving `.gitignore`, Git will ignore all matching files automatically. Add and commit the `.gitignore` itself:

```bash
git add .gitignore
git commit -m "Add .gitignore"
git push
```

Never put API keys, passwords, or credentials in a file you push to GitHub. Even private repos can be exposed. Store secrets in `.env` files and always include `.env` in your `.gitignore`.

---

### RECAP (13:00–14:00)

1. Create a new repo on GitHub with a README
2. `git clone URL` — downloads it and configures the remote
3. Work on your files in VS Code
4. `git add .` → `git commit -m "message"` → `git push` — regularly, not just at the end
5. Verify files are visible on github.com before submitting
6. Submit the GitHub URL to Canvas
7. Use `.gitignore` to keep `venv/`, `__pycache__/`, and `.env` off GitHub

Next video: AI literacy — using AI tools responsibly in programming coursework.
