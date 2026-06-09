# ISM3232 Lab W03: Virtual Environments & Shell Customisation

## YouTube Metadata

**Title:** Virtual Environments & Shell Customisation — Lab Walkthrough | ISM3232 Lab 03
**Description:**
Walkthrough of ISM3232 Module 3 Lab. We create a virtual environment, install pytest and ruff, freeze requirements, write a .gitignore, and add 10+ aliases and a mkcd function to .zshrc.

Course page: https://markumreed.github.io/ism3232/docs/week03_lab.html

**Chapters:**
0:00 — What this lab covers
0:30 — Creating and activating the virtual environment
2:30 — Installing packages and freezing requirements
4:00 — Writing .gitignore for the venv
5:30 — Adding aliases and mkcd to .zshrc
8:00 — Submission checklist

**Applies to:** ISM3232 Module 03

**Tags:** python virtual environment, python venv tutorial, zshrc aliases, pip install requirements, ISM3232, USF, python venv mac, zsh customization

---

## Script

### INTRO (0:00–0:30)

Lab 3 — Virtual Environments and Shell Customisation. Two things that change how you work for the rest of the course: isolated Python environments per project, and a customized shell that saves keystrokes every day.

---

### CREATE AND ACTIVATE VENV (0:30–2:30)

```bash
cd ~/ism3232/module02_zsh
python3 -m venv .venv
```

`.venv` is the convention — the dot makes it hidden in `ls` output (use `ls -la` to see it), and `.venv` is the name most editors auto-detect.

Activate it:
```bash
source .venv/bin/activate
```

Your prompt changes:
```
(.venv) yourname@machine module02_zsh %
```

The `(.venv)` prefix confirms the environment is active. Now check which Python is running:
```bash
which python3
# /Users/yourname/ism3232/module02_zsh/.venv/bin/python3
```

It points inside `.venv` — not the system Python. This is isolation working correctly.

Screenshot 1: `(.venv)` prompt and `which python3` output.

---

### INSTALL PACKAGES AND FREEZE (2:30–4:00)

```bash
pip install pytest ruff
pip list
# Both pytest and ruff should appear

pip freeze > requirements.txt
cat requirements.txt
```

`requirements.txt` records the exact versions. Any collaborator can reproduce your environment:
```bash
pip install -r requirements.txt
```

Screenshot 2: `pip install` and `cat requirements.txt` output.

---

### .GITIGNORE (4:00–5:30)

Create `module02_zsh/.gitignore`:

```gitignore
# Virtual environment
.venv/

# Python cache
__pycache__/
*.pyc
*.pyo

# macOS
.DS_Store

# IDE
.vscode/
```

Verify with `git status` — `.venv/` should not appear as an untracked file. If it does, your `.gitignore` isn't in the right directory.

Screenshot 3: `ls -la` showing `.venv/` and `.gitignore`.

---

### ZSHRC ALIASES AND MKCD (5:30–8:00)

Open `~/.zshrc` in VS Code:
```bash
code ~/.zshrc
```

Add at least 10 aliases plus the `mkcd` function:

```bash
# --- ISM3232 aliases ---
alias ll='ls -la'
alias gs='git status'
alias ga='git add .'
alias gc='git commit -m'
alias gp='git push'
alias gl='git log --oneline'
alias venv='source .venv/bin/activate'
alias pytest='python3 -m pytest -v'
alias ruff='python3 -m ruff'
alias cdism='cd ~/ism3232'

# mkcd — make directory and cd into it in one step
mkcd() {
    mkdir -p "$1" && cd "$1"
}
```

Reload the shell:
```bash
source ~/.zshrc
```

Test all your aliases:
```bash
ll          # should show long listing
gs          # should show git status
mkcd test_dir   # should create and enter test_dir
pwd         # confirms you're inside test_dir
cd ..
```

Screenshot 4: `ll`, `gs`, and `mkcd` working after `source ~/.zshrc`.

---

### SUBMISSION CHECKLIST (8:00–10:00)

- Screenshot 1: `(.venv)` prompt + `which python3`
- Screenshot 2: `pip install` + `cat requirements.txt`
- Screenshot 3: `ls -la` showing `.venv/` and `.gitignore`
- Screenshot 4: aliases and `mkcd` working
- `requirements.txt` uploaded
- `.gitignore` uploaded
- `README.md` with Week 3 section added, uploaded
- Submitted to Canvas
