# ISM2411: drag the whole folder to GitHub (short design)

## Intent
ISM2411 students who struggle with Git should be able to get a lab or the
capstone onto GitHub by dragging one thing into the browser. Builds on the
2026-11-19 browser-upload rewrite (Labs 8, 10–15, capstone, Unit 5
cheatsheet; still uncommitted), which told students to drag the files
*inside* their work folder and never the folder itself.

## Goals
- "Drag your whole `ism2411-labNN` folder onto the upload area" is the one
  main instruction for Labs 11–15 and the capstone.
- A repo that holds the files inside that folder
  (`ism2411-lab12/csv_practice.py`) is correct, and so is one with the files
  at the top level (the old way, or `git push` from the terminal box).
- Nothing on a page says a whole-folder upload is wrong.

## Non-goals
- Labs 1–7 (Canvas upload) and Week 9 (no Git): untouched.
- Labs 8 and 10: already "drag the week07 / week10 folder". Untouched.
- The optional terminal boxes, the video scripts, the autograder (no ISM2411
  GitHub assignment checks paths; the capstone config has `expected_files: []`).

## Anti-goals
- Two equal options on every page. The side note about the old way stays short.
- A page that still says "at the top level", so a student who followed the
  main instruction looks wrong.

## Approaches
- **A. Whole folder is the main instruction; files-inside still accepted.**
  Picked by the user. One action, matches Labs 8 and 10.
- B. Keep files-inside as main and add "whole folder works too". Smaller
  diff, but two options on every page.
- Rejected: renaming work folders (churn, no gain); GitHub Desktop (a new
  install, the opposite of easier).

## Changes
- **Lab 11** (full setup review, `#repo-setup`): Step 4 drags the
  `ism2411-lab11` folder; Step 5's check expects README.md, .gitignore and
  an `ism2411-lab11` folder holding customers.py; the "find my file" hint
  becomes "find my folder"; the "labs with folders" hint says the same drag
  carries `data/` and `charts/`, and that dragging the contents also works
  if used every time; a new "my files show up twice" hint; the "wrong place"
  hint drops its top-level-only path example and notes hidden files
  (`.DS_Store`, `.ipynb_checkpoints`) a folder drag may bring along;
  submission box accepts the folder or the top level.
- **Labs 12–15** setup cards: "drag your whole `ism2411-labNN` folder in".
  Submission boxes: "data/ next to your script" instead of "at the top level".
- **Capstone**: drag your whole project folder; keep the rest.
- **Unit 5 cheatsheet**: the upload comment line.

## My calls (correctable)
- Finding the folder: in VS Code's terminal, `cd ~` then `open .` (Mac) or
  `explorer.exe .` (Windows). Windows students use WSL, where `~` is inside
  Linux and VS Code's Reveal in File Explorer may not be offered.
- Files uploaded both ways: delete the older copy; if both stay, the most
  recent upload is graded.
- README "command that runs your work" wording stays as it is.

## Left to the builder
Exact sentences, matching each page's existing voice and HTML patterns.
Verify by rendering the changed pages and re-grepping for "top level",
"folder itself" and "one level too deep".
