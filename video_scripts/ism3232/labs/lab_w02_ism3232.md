# ISM3232 Lab W02: zsh Navigation & File Operations

## YouTube Metadata

**Title:** zsh Navigation & File Operations — Full Lab Walkthrough | ISM3232 Lab 02
**Description:**
Step-by-step, test-as-you-go walkthrough of ISM3232 Module 2 Lab. Every navigation and file-operation command is run one at a time with its exact expected output shown before the next command — pwd, ls, ls -la, cd, tree, touch, echo, cat, head, cp, mv, the rm safety ritual, then a 12+ command README reference table.

Course page: https://markumreed.github.io/ism3232/docs/week02_lab.html
Published video: https://youtu.be/yQBZqWj013E

**Chapters:**
0:00 — What this lab covers and the rm safety rule
0:35 — Setup: create week2_lab folder
1:10 — Step 1: pwd — where am I
1:30 — Step 2: ls — what's visible here
1:50 — Step 3: ls -la — including hidden files
2:20 — Step 4: cd .. and pwd — moving up
2:50 — Step 5: cd ~/ism3232 and tree -L 2
3:40 — Screenshot 1 checkpoint — tree output
4:00 — Step 6: return to week2_lab and confirm
4:20 — Step 7: create three files with touch
4:50 — Step 8: write and read notes.txt
5:40 — Step 9: cp and mv — copy then rename
6:40 — Step 10: edit and run week2_script.py
7:50 — Screenshot 2 checkpoint — ls -la + script output
8:10 — Step 11: open module02_zsh as a VS Code workspace
8:50 — Screenshot 3 checkpoint — VS Code workspace
9:10 — Step 12: the rm safety ritual, command by command
10:40 — Screenshot 4 checkpoint — before/after rm
11:00 — Step 13: write the 12+ command README table
13:00 — Stretch: pipes and append redirect
13:50 — Submission checklist

**Applies to:** ISM3232 Module 02

**Tags:** zsh navigation tutorial, terminal file operations, rm safety ritual, ISM3232, USF, command line mac, linux terminal tutorial

---

## How to Use This Script

Same format as every lab: **SAY** the line, **DO** the command, **CHECK** the exact output before moving on. **FIX** tells you what to say if the checkpoint doesn't match.

---

## Script

### INTRO (0:00–0:35)

**SAY:** "Lab 2 — zsh navigation and file operations. Before we touch `rm`, memorize the rule: before any delete, run `pwd` then `ls`. Confirm where you are and what's there. `rm` is permanent — no Trash, no undo. We'll practice that ritual explicitly later in this lab."

---

### SETUP (0:35–1:10)

#### Step 0 — Create this week's lab folder

**SAY:** "Everything today happens inside a new folder under Module 2, so it doesn't tangle with Week 1's files."

**DO:**
```bash
cd ~/ism3232/module02_zsh
mkdir week2_lab
cd week2_lab
pwd
```

**CHECK:**
```
/Users/yourname/ism3232/module02_zsh/week2_lab
```

**FIX:** If `pwd` shows a different path, you likely started from the wrong directory — run `cd ~/ism3232/module02_zsh/week2_lab` directly and re-check.

---

### PART 1 — Navigation, One Command at a Time (1:10–3:40)

#### Step 1 — pwd

**SAY:** "Where am I right now?"

**DO:**
```bash
pwd
```

**CHECK:**
```
/Users/yourname/ism3232/module02_zsh/week2_lab
```

---

#### Step 2 — ls

**SAY:** "What's visible in this folder?"

**DO:**
```bash
ls
```

**CHECK:** Empty output — the folder was just created and has nothing in it yet. That's expected, not an error.

---

#### Step 3 — ls -la

**SAY:** "Now the long listing, with hidden files — anything starting with a dot."

**DO:**
```bash
ls -la
```

**CHECK:**
```
drwxr-xr-x   2 yourname  staff   64 Aug 25 10:03 .
drwxr-xr-x   3 yourname  staff   96 Aug 25 10:03 ..
```
The two entries `.` (this folder) and `..` (its parent) always appear even in an empty folder — that's what `-a` (all) surfaces that plain `ls` hides.

---

#### Step 4 — cd .. and pwd

**SAY:** "Up one level, and confirm it worked."

**DO:**
```bash
cd ..
pwd
```

**CHECK:**
```
/Users/yourname/ism3232/module02_zsh
```

---

#### Step 5 — Jump to the course root and visualize it

**SAY:** "Let's jump all the way to the course folder and look at the whole structure at once with `tree`."

**DO:**
```bash
cd ~/ism3232
tree -L 2
```

**CHECK:**
```
.
├── module01_setup
│   ├── README.md
│   └── hello_ism3232.py
├── module02_zsh
│   └── week2_lab
├── module03_venv
├── module04_search
├── module05_python
├── module06_loops
├── module07_functions
└── module08_debug
```
(Exact contents of `module01_setup` will match whatever you built last week; the point is the tree renders without error and `week2_lab` shows up under `module02_zsh`.)

**FIX:** If `tree: command not found`, install it — macOS: `brew install tree`; Ubuntu: `sudo apt install tree`. As a fallback you can use `ls -R module02_zsh` to see the same structure less visually.

---

#### Screenshot 1 checkpoint (3:40–4:00)

**SAY:** "Screenshot 1 — the `tree -L 2` output from `~/ism3232/`, showing the full module structure."

---

#### Step 6 — Return to the lab folder

**SAY:** "Back into today's folder before we start creating files."

**DO:**
```bash
cd module02_zsh/week2_lab
pwd
```

**CHECK:**
```
/Users/yourname/ism3232/module02_zsh/week2_lab
```

---

### PART 2 — File Operations, One Command at a Time (4:20–8:10)

#### Step 7 — Create three files at once

**SAY:** "`touch` creates empty files — no content, just the file itself. Let's create three in one line."

**DO:**
```bash
touch notes.txt commands.txt hello_week2.py
ls -la
```

**CHECK:**
```
commands.txt  hello_week2.py  notes.txt
```
(plus the usual `.` and `..` entries from `-la`)

---

#### Step 8 — Write to a file, then read it back

**SAY:** "`>` writes text into a file, overwriting anything already there. Then we read it back two different ways."

**DO:**
```bash
echo 'Week 2 navigation practice' > notes.txt
cat notes.txt
head -1 notes.txt
```

**CHECK:**
```
Week 2 navigation practice
Week 2 navigation practice
```
`cat` prints the whole file; `head -1` prints just the first line. With one line of content, both commands print the same thing — that's expected, and it's a preview of why `head` matters once files get longer.

---

#### Step 9 — Copy, then rename

**SAY:** "`cp` makes a duplicate and leaves the original in place. `mv` does the opposite — it moves or renames, and the original name is gone afterward."

**DO:**
```bash
cp notes.txt notes_backup.txt
mv hello_week2.py week2_script.py
ls -la
```

**CHECK:**
```
commands.txt  notes.txt  notes_backup.txt  week2_script.py
```
Notice `hello_week2.py` no longer appears — `mv` renamed it in place, it didn't create a copy.

---

#### Step 10 — Edit and run the script

**SAY:** "Open `week2_script.py`, add one line, save, and run it."

**DO:** In VS Code, add to `week2_script.py`:
```python
print('Week 2 complete')
```
Then in the terminal:
```bash
code week2_script.py
python3 week2_script.py
```

**CHECK:**
```
Week 2 complete
```

**FIX:** If nothing prints, confirm you saved the file (`⌘S`/`Ctrl+S`) before running it — VS Code does not auto-save by default.

---

#### Screenshot 2 checkpoint (7:50–8:10)

**SAY:** "Screenshot 2 — `ls -la` and the `python3 week2_script.py` output, both visible in the same terminal scroll."

---

### PART 3 — Open as a VS Code Workspace (8:10–8:50)

#### Step 11 — Open the whole module, not just a file

**SAY:** "This is the habit to build now: open the *project folder* as a workspace, not individual files one at a time."

**DO:**
```bash
cd ~/ism3232
code module02_zsh
```

**CHECK:** VS Code opens with `module02_zsh` as the workspace root. The Explorer panel on the left shows `week2_lab/` as a subfolder, and expanding it reveals `commands.txt`, `notes.txt`, `notes_backup.txt`, and `week2_script.py`.

---

#### Screenshot 3 checkpoint (8:50–9:10)

**SAY:** "Screenshot 3 — VS Code with `module02_zsh` open as the workspace, Explorer panel visible."

---

### PART 4 — The rm Safety Ritual, Command by Command (9:10–10:40)

#### Step 12a — Confirm your location

**SAY:** "Before any delete, step one: where am I?"

**DO:**
```bash
cd ~/ism3232/module02_zsh/week2_lab
pwd
```

**CHECK:**
```
/Users/yourname/ism3232/module02_zsh/week2_lab
```

---

#### Step 12b — Confirm what's here

**SAY:** "Step two: what exactly is in this folder, so I know precisely what I'm about to delete?"

**DO:**
```bash
ls
```

**CHECK:**
```
commands.txt  notes.txt  notes_backup.txt  week2_script.py
```

---

#### Step 12c — Delete only what you intend

**SAY:** "Only now — after confirming location and contents — do we delete. We're removing `notes_backup.txt` because it was just a throwaway copy."

**DO:**
```bash
rm notes_backup.txt
```

**CHECK:** No output — `rm` is silent on success. That silence is normal, not a failure.

---

#### Step 12d — Confirm it's gone

**SAY:** "Step three: verify. Never assume a delete worked — check."

**DO:**
```bash
ls
```

**CHECK:**
```
commands.txt  notes.txt  week2_script.py
```
`notes_backup.txt` no longer appears.

**FIX:** If you deleted the wrong file, there is no undo — `rm` does not use the Trash/Recycle Bin. That's exactly why this ritual exists: say the ritual out loud every time, before you type `rm`, for the rest of the semester.

---

#### Screenshot 4 checkpoint (10:40–11:00)

**SAY:** "Screenshot 4 — all four commands from the ritual in one screenshot: `pwd`, `ls` before, `rm`, and `ls` after."

---

### PART 5 — Command Reference README (11:00–13:00)

#### Step 13 — Write the README table

**SAY:** "Now document every command from today in a table — this becomes your own personal cheat sheet for the rest of the semester."

**DO:**
```bash
cd ~/ism3232/module02_zsh
touch README.md
code README.md
```
Type:
```markdown
# ISM3232 - Module 2: zsh Navigation and File Operations

## Commands Practiced

| Command        | What it does                            |
|----------------|------------------------------------------|
| pwd            | Prints the current working directory    |
| ls             | Lists visible files and folders         |
| ls -la         | Lists all files including hidden ones   |
| [add the rest] | [your description]                      |

## AI Use Statement
I did not use AI for this lab.
```

**CHECK:** Count your table rows — the lab requires at least 12 commands documented. Go back through this script's steps (`cd`, `mkdir`, `touch`, `echo`, `cat`, `head`, `cp`, `mv`, `rm`, `tree`, `code`) and make sure each one you actually ran has its own row.

---

### STRETCH — Pipes and Append Redirect (13:00–13:50)

**SAY:** "If you finish early: two operators that come up constantly — the pipe and append redirect."

**DO:**
```bash
ls -la | head -5
echo 'extra line' >> notes.txt
cat notes.txt
wc -l notes.txt
```

**CHECK:**
```
Week 2 navigation practice
extra line
       2 notes.txt
```
`|` (pipe) feeds one command's output into the next command's input — here, `ls -la`'s output is truncated to its first 5 lines by `head`. `>>` (double arrow) *appends* to a file instead of overwriting it like the single `>` did in Step 8 — that's why `notes.txt` now has two lines instead of one.

---

### SUBMISSION CHECKLIST (13:50–end)

- [ ] Screenshot 1: `tree -L 2` output from `~/ism3232/`
- [ ] Screenshot 2: `ls -la` and `python3 week2_script.py` output
- [ ] Screenshot 3: VS Code with `module02_zsh` open as workspace
- [ ] Screenshot 4: `pwd` + `ls` before `rm`, then `ls` after — all in one screenshot
- [ ] `module02_zsh/README.md` — command reference table with at least 12 commands
- [ ] Submitted to Canvas
