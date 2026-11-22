# ISM2411 Whole-Folder Upload Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Labs 11–15 and the capstone tell students to drag their whole work folder onto GitHub's upload page, and nothing calls that layout wrong.

**Architecture:** Wording-only edits to static HTML in the `ism2411` submodule, on top of the uncommitted 2026-11-19 browser-upload rewrite. Lab 11's `#repo-setup` section is the hub the other labs link to, so the detailed hints live there; Labs 12–15 and the capstone get one-line instructions.

**Tech Stack:** Static HTML (inline styles, `.hint` details, `.callout` boxes). Checks with grep and Python's `html.parser`.

**Spec:** `docs/superpowers/specs/2026-11-22-ism2411-whole-folder-upload-design.md`

## Global Constraints

- Main instruction: "drag your whole `ism2411-labNN` folder" onto the upload area. Files-inside-the-folder and `git push` stay accepted, in a short side note only.
- Don't touch Labs 1–10, the terminal `<details id="terminal">` box, video scripts or the autograder.
- Finding the folder: in VS Code's terminal, `cd ~` then `open .` (Mac) or `explorer.exe .` (Windows).
- Duplicates: delete the older copy; if both stay, the most recent upload is graded.
- Keep each page's voice: short sentences, `<code>` for names, `<strong>` for UI labels, `&rarr;` / `&rsquo;` entities.

## Review Focus

1. A student whose work folder is a Git clone (Lab 11 "mkdir says the folder already exists" hint) drags a folder holding `.git`. Expect: that hint tells them to use `git push` or drag the files inside instead. (Task 1)
2. Capstone: a README.md inside the dragged folder lands one level down while the grader reads the top-level one. Expect: capstone and cheatsheet say the video link goes in the README at the top of the repo, edited with the pencil icon. (Task 3)
3. A student uploads one way, then the other, and sees two copies. Expect: a Lab 11 hint covers it. (Task 1)
4. A Windows (WSL) student can't find the home folder in File Explorer. Expect: the `explorer.exe .` hint. (Task 1)
5. Lab 15's local copy from `~/ism2411-lab14/data/clean_sales.csv` keeps working (local path, unaffected). Expect: unchanged. (Task 4 grep)

---

### Task 1: Lab 11 hub (`#repo-setup`)

**Files:**
- Modify: `ism2411/pages/week11_lab.html:306` (Step 4 drag line), `:312` (Step 5 check), `:322-330` (three hints + new duplicates hint), `:335` (mkdir hint), `:445` (Canvas Deliverable)

- [ ] **Step 1: Confirm the stale wording is there**

Run: `grep -c -E 'Drag <code>customers.py</code>|all at the top level|one level too deep|Reveal in Finder|at the top level next to' ism2411/pages/week11_lab.html`
Expected: `5`

- [ ] **Step 2: Edit**
  - Step 4: drag your whole `ism2411-lab11` folder; GitHub keeps the folder, so the file lands at `ism2411-lab11/customers.py`.
  - Step 5: repo page lists `.gitignore`, `README.md`, and an `ism2411-lab11` folder; click it to see `customers.py`.
  - Hint "how do I find my folder to drag it?": `cd ~` then `open .` / `explorer.exe .`; a window opens on the home folder showing `ism2411-lab11`; drag that folder.
  - Hint "what do I drag when a lab has folders?": the same whole folder; `data` and `charts` ride along inside it. Dragging the files and folders inside works too; use the same way every time for a lab.
  - New hint "my files show up twice": uploaded both ways; delete the older copy (open file → ··· → Delete file); if both stay, the most recent upload is graded.
  - "Wrong place" hint: generic "type the folder name and a `/` in front"; a folder drag can bring hidden files (`.DS_Store`, `.ipynb_checkpoints`) — harmless, delete if you like.
  - mkdir hint: a cloned folder holds a hidden `.git` folder; upload it with `git push` (link `#terminal`) or drag the files inside it.
  - Deliverable: `customers.py` inside your `ism2411-lab11` folder (or at the top level, if you uploaded the file itself).

- [ ] **Step 3: Re-run Step 1's grep**
Expected: `0`

### Task 2: Labs 12–15 setup cards and deliverables

**Files:**
- Modify: `ism2411/pages/week12_lab.html:292,367`, `week13_lab.html:227,321`, `week14_lab.html:134,219`, `week15_lab.html:128,210`

- [ ] **Step 1:** `grep -c -E 'folder itself|at the top level' ism2411/pages/week1[2-5]_lab.html` → each file `2`
- [ ] **Step 2: Edit.** Upload line: "drag your whole `ism2411-labNN` folder in" (keep the rest of the sentence). Deliverable: drop "at the top level"; say the data/charts folders sit next to the script or notebook.
- [ ] **Step 3:** same grep → each file `0`

### Task 3: Capstone and Unit 5 cheatsheet

**Files:**
- Modify: `ism2411/pages/week16_capstone.html:433-434`, `ism2411/pages/unit_5_cheatsheet.html:270-288`

- [ ] **Step 1:** `grep -c -E 'project folder itself|your-capstone folder itself' ism2411/pages/week16_capstone.html ism2411/pages/unit_5_cheatsheet.html` → `1` each
- [ ] **Step 2: Edit.** Capstone: drag your whole project folder; README line names the README at the top of the repo (the one GitHub shows below the file list) as the one to edit with the pencil icon and the one that holds the video link. Cheatsheet: tree labeled as your project folder (no README.md inside); upload comment "drag in your whole your-capstone folder"; "Edit README.md at the top of the repo with the pencil icon".
- [ ] **Step 3:** same grep → `0` each

### Task 4: Whole-change check

- [ ] **Step 1:** `grep -n -E 'folder itself|one level too deep|at the top level|Reveal in' ism2411/pages/week1[1-6]_*.html ism2411/pages/unit_5_cheatsheet.html` → no output
- [ ] **Step 2:** `html.parser` tag-balance check (`details`, `ul`, `ol`, `li`, `p`, `div`) on the 6 changed files → no imbalance introduced (compare with `git stash`-free baseline: counts from `git show HEAD:<file>` plus the Nov 19 diff)
- [ ] **Step 3:** `grep -c 'ism2411-lab14/data/clean_sales.csv' ism2411/pages/week15_lab.html` → unchanged from before
- [ ] **Step 4:** render Lab 11 and the capstone headless and eyeball the changed hints
- [ ] **Step 5:** commit and push only on the user's go-ahead (ism2411 on main, then the parent pointer). This also ships the Nov 19 rewrite.
