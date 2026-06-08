# ISM3232 Lab W02: zsh Navigation & File Operations

## YouTube Metadata

**Title:** zsh Navigation & File Operations — Lab Walkthrough | ISM3232 Lab 02
**Description:**
Walkthrough of ISM3232 Module 2 Lab. We master the zsh file system: pwd, ls -la, cd, mkdir, cp, mv, cat, wc, and the rm safety ritual. Submitting a README documenting 12+ commands.

**Chapters:**
0:00 — What this lab covers
0:30 — Core navigation: pwd, ls -la, cd, mkdir
2:30 — File operations: cp, mv, cat, wc
4:30 — The rm safety ritual
6:30 — Opening VS Code as a workspace
7:30 — Writing the README command reference
8:30 — Submission checklist

**Applies to:** ISM3232 Module 02

**Tags:** zsh navigation tutorial, terminal file operations, rm safety ritual, ISM3232, USF, command line mac, linux terminal tutorial

---

## Script

### INTRO (0:00–0:30)

Lab 2 — zsh Navigation and File Operations. The goal: get completely comfortable moving around the file system and manipulating files without a GUI. Every developer workflow assumes you can do this without thinking.

---

### CORE NAVIGATION (0:30–2:30)

```bash
pwd
# Print Working Directory — where am I right now?

ls
# List contents

ls -la
# Long listing with hidden files (files starting with .) and permissions

cd module02_zsh
# Change into directory

mkdir week2_lab
cd week2_lab

# Create some files to work with
touch notes.txt script.py config.json

tree -L 2
# Shows a tree of the current directory up to 2 levels deep
```

Screenshot 1: `tree -L 2` output from `~/ism3232/`.

---

### FILE OPERATIONS (2:30–4:30)

```bash
# Write content to a file
echo "# Week 2 Notes" > notes.txt
echo "Terminal commands are the universal dev interface." >> notes.txt

# Read it back
cat notes.txt

# Count lines/words
wc -l notes.txt    # line count
wc -w notes.txt    # word count

# Copy a file
cp notes.txt notes_backup.txt
ls

# Rename (move within same directory)
mv notes_backup.txt archive_notes.txt

# Move to a different directory
mkdir archive
mv archive_notes.txt archive/
ls archive/
```

Screenshot 2: `ls -la` and `python3 week2_script.py` output.

---

### THE RM SAFETY RITUAL (4:30–6:30)

Never delete without confirming first. The three-step ritual:

```bash
# Step 1: confirm your location
pwd
# /Users/yourname/ism3232/module02_zsh/week2_lab

# Step 2: confirm what is here
ls
# notes.txt  script.py  config.json  archive/

# Step 3: delete only what you intend
rm config.json

# Confirm it's gone
ls
# notes.txt  script.py  archive/
```

Screenshot 4: `pwd` + `ls` before rm, then `ls` after — all in one screenshot.

Never use `rm -rf` on a directory until you have confirmed with `ls` exactly what's inside. Many lost-work stories start with `rm -rf` in the wrong directory.

---

### OPEN AS VS CODE WORKSPACE (6:30–7:30)

```bash
cd ~/ism3232
code module02_zsh
```

VS Code opens with `module02_zsh` as the root workspace. This is how you work — not by opening individual files, but by opening the project folder. The file tree on the left shows all files.

Screenshot 3: VS Code with `module02_zsh` open as workspace.

---

### README COMMAND REFERENCE (7:30–8:30)

In `module02_zsh/README.md`, document at least 12 commands in a table:

```markdown
# Module 02 — zsh Command Reference

| Command | What it does | Example |
|---------|-------------|---------|
| `pwd` | Print working directory | `pwd` |
| `ls` | List directory contents | `ls` |
| `ls -la` | Long list with hidden files | `ls -la` |
| `cd folder` | Change directory | `cd module02_zsh` |
| `cd ..` | Go up one level | `cd ..` |
| `mkdir name` | Create directory | `mkdir week2_lab` |
| `touch file` | Create empty file | `touch notes.txt` |
| `cat file` | Print file contents | `cat notes.txt` |
| `cp src dst` | Copy file | `cp notes.txt backup.txt` |
| `mv src dst` | Move or rename | `mv backup.txt archive/` |
| `rm file` | Delete file | `rm config.json` |
| `wc -l file` | Count lines | `wc -l notes.txt` |
| `tree -L 2` | Show directory tree | `tree -L 2` |
```

---

### SUBMISSION CHECKLIST (8:30–10:00)

- Screenshot 1: `tree -L 2` from `~/ism3232/`
- Screenshot 2: `ls -la` and Python script output
- Screenshot 3: VS Code workspace open
- Screenshot 4: `pwd` + `ls` before and after `rm`
- `README.md` with 12+ commands in a table uploaded
- Submitted to Canvas
