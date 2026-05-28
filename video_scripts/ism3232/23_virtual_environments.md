# Video 23: Virtual Environments & pip

## YouTube Metadata

**Title:** Python Virtual Environments & pip — venv, requirements.txt | ISM3232
**Description:**
A virtual environment isolates your project's Python packages from every other project on your machine. In this video you'll create a venv, activate it, install packages, freeze requirements, and customize your shell prompt in .zshrc — the professional Python workflow from day one.

**Chapters:**
0:00 — Why virtual environments exist
2:00 — Creating a venv
4:00 — Activating and deactivating
6:00 — Installing packages with pip
8:30 — requirements.txt — sharing your dependencies
11:00 — .gitignore — never commit venv
12:30 — Customizing .zshrc
15:00 — Recap

**Applies to:** ISM3232 Module 3

**Tags:** python virtual environment, python venv, pip install, requirements.txt, gitignore venv, zshrc aliases, ISM3232, python setup, python project setup, virtualenv tutorial

---

## Script

### INTRO (0:00–2:00)

Imagine you install pandas version 1.5 for one project and numpy version 1.23 for another. Six months later you start a third project and install a package that updates pandas to version 2.0 — and now your first project breaks because the API changed. This is dependency hell, and it's a real problem.

Virtual environments solve this. Each project gets its own isolated Python environment with its own packages. Installing pandas 2.0 in one project doesn't touch the others. Every ISM3232 assignment starts with creating a venv. Here's how.

---

### WHY ENVIRONMENTS EXIST (by end of intro)

Without a venv, every `pip install` goes into your global Python installation — shared across all projects. With a venv, each project has its own `site-packages` folder. Activate the venv, and Python uses that project's packages. Deactivate, and it goes back to global.

---

### CREATING A venv (2:00–4:00)

Navigate to your project folder:

```bash
cd ~/ism3232/module03_venv
```

Create the virtual environment. Call it `.venv` (the dot makes it hidden — convention in professional projects):

```bash
python3 -m venv .venv
```

This creates a `.venv/` directory containing a private Python interpreter and `pip`. Check:

```bash
ls -la
```

You'll see the `.venv/` folder.

**Why `-m venv`?** The `-m` flag runs a module as a script. `venv` is Python's built-in environment module. No installation needed — it ships with Python 3.3+.

---

### ACTIVATING AND DEACTIVATING (4:00–6:00)

Activation tells your shell to use this environment's Python and pip instead of the global ones.

**Mac/Linux:**
```bash
source .venv/bin/activate
```

**Windows (WSL):**
```bash
source .venv/bin/activate
```

After activation, your prompt changes to show `(.venv)` at the start:

```
(.venv) markum@MacBook module03_venv %
```

Verify you're using the venv's Python:
```bash
which python3    # should show .../.venv/bin/python3
python3 --version
```

To deactivate:
```bash
deactivate
```

Prompt returns to normal. **Always activate your venv before working on a project and before installing packages.**

---

### INSTALLING PACKAGES (6:00–8:30)

With the venv activated:

```bash
pip install requests
pip install black ruff   # install multiple at once
pip install pytest==7.4.3   # specific version
```

List installed packages:
```bash
pip list
```

Show details about a specific package:
```bash
pip show requests
```

Upgrade a package:
```bash
pip install --upgrade pip    # always upgrade pip first in a new venv
```

**Important:** only `pip install` with the venv active. If you install packages to the global environment, they won't be available inside the venv, and you'll get `ModuleNotFoundError` when you run your project.

---

### requirements.txt (8:30–11:00)

`requirements.txt` is a text file listing all packages your project needs. Anyone can recreate your exact environment from it.

**Generate from your current environment:**
```bash
pip freeze > requirements.txt
cat requirements.txt
```

Output:
```
black==23.11.0
certifi==2023.11.17
charset-normalizer==3.3.2
idna==3.4
pytest==7.4.3
requests==2.31.0
ruff==0.1.6
urllib3==2.1.0
```

**Recreate an environment from requirements.txt:**
```bash
# Someone else (or you on a new machine) does:
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

This is how you share projects and how deployment works. Include `requirements.txt` in your repository. Update it every time you add a package.

**Minimal requirements.txt** — for learning projects, you don't need to pin every transitive dependency. List just the packages you explicitly installed:

```
pytest==7.4.3
requests==2.31.0
ruff==0.1.6
```

---

### .gitignore — NEVER COMMIT VENV (11:00–12:30)

The `.venv/` folder is large (often 50–200 MB) and entirely reproducible from `requirements.txt`. Never commit it to git.

Create `.gitignore` in your project root:

```bash
touch .gitignore
code .gitignore
```

Minimum contents:
```
.venv/
__pycache__/
*.pyc
.DS_Store
.env
```

Check that `.venv/` is ignored:
```bash
git status
```

The `.venv/` folder should not appear in untracked files.

---

### CUSTOMIZING .zshrc (12:30–15:00)

`.zshrc` is your shell configuration file. It runs every time you open a new terminal. Use it to set aliases and customize your prompt.

```bash
code ~/.zshrc
```

Useful aliases for this course:

```bash
# Quick navigation
alias ism="cd ~/ism3232"
alias venv="source .venv/bin/activate"

# Python shortcuts
alias py="python3"
alias pip="pip3"

# Git shortcuts
alias gs="git status"
alias ga="git add ."
alias gc="git commit -m"
alias gp="git push"
alias gl="git log --oneline"

# Safety — ask before deleting
alias rm="rm -i"

# Show hidden files in ls
alias la="ls -la"
```

Save `.zshrc`. Apply changes:
```bash
source ~/.zshrc
```

Test:
```bash
ism      # should cd to ~/ism3232
venv     # should activate .venv (if in a project dir)
gs       # should run git status
```

---

### RECAP (15:00–18:00)

- `python3 -m venv .venv` — create a virtual environment
- `source .venv/bin/activate` — activate it (do this every session)
- `deactivate` — return to global environment
- `pip install package` — install into the active environment
- `pip freeze > requirements.txt` — snapshot your dependencies
- `pip install -r requirements.txt` — recreate from snapshot
- Add `.venv/` to `.gitignore` — never commit the environment folder
- `~/.zshrc` — add aliases to speed up your workflow

**The standard project startup sequence:**
```bash
cd ~/ism3232/module_name
source .venv/bin/activate   # or just: venv (if you added the alias)
code .
```

Module 4: search tools, the submission ritual, and Git/GitHub.
