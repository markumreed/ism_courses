# Video 00: Pre-Course Setup — Install Python & VS Code Before Day 1

## YouTube Metadata

**Title:** ISM2411 Pre-Course Setup — Install Python & VS Code Before Week 1
**Description:**
Everything to install before your first ISM2411 class session, done in about 30 minutes: Python 3.12, VS Code, the Python and Pylance extensions, and a hello-world script that proves the whole toolchain works together. Mac and Windows instructions are both covered. Do this before Week 1 so class time is spent writing Python, not troubleshooting installs.

Course page: https://markumreed.github.io/ism2411/pages/precourse.html

**Chapters:**
0:00 — Why do this before Week 1
1:00 — What you're installing (overview)
2:30 — Step 1: Install Python 3
5:00 — Step 2: Install VS Code
7:30 — Step 3: Python + Pylance extensions
9:00 — Step 4: Hello-world verification
11:00 — Step 5: DataCamp account (nothing to do yet)
11:30 — Common problems
13:00 — Getting help before Day 1
13:30 — Recap and checklist

**Applies to:** ISM2411 — before Module 1 / Week 1

**Tags:** ISM2411 precourse setup, install python for business, install VS Code, python extension VS Code, Pylance, USF Muma, hello world python, python setup mac windows, first day setup checklist

---

## Script

### INTRO — WHY DO THIS BEFORE WEEK 1 (0:00–1:00)

This is the one video you watch before class even starts. By the end, you'll have Python and VS Code installed, talking to each other correctly, and you'll have run one line of real Python code. That's it — about 30 minutes, done once, and Week 1 becomes about writing Python instead of fighting installers.

Everything here is free. No credit card, no paid license, nothing to buy.

---

### WHAT YOU'RE INSTALLING (1:00–2:30)

Three things:

1. **Python 3.12** — the actual programming language. This is the engine.
2. **VS Code** — the editor where you'll write every script this semester.
3. **Two VS Code extensions** — Python and Pylance, both published by Microsoft. These connect VS Code to Python so you get a run button, autocomplete, and inline type hints.

You need Python 3.10 or higher — 3.12 is what we recommend and what these instructions install.

---

### STEP 1 — INSTALL PYTHON 3 (2:30–5:00)

**Mac:**
Go to `python.org/downloads` and click the big **Download Python 3.12.x** button. That downloads a `.pkg` installer. Open it, click through the defaults — you don't need to change anything — and click Install.

Verify in Terminal (⌘Space, type "Terminal"):
```bash
python3 --version
```
Expected: `Python 3.10.x`, `3.11.x`, or `3.12.x`.

**Windows:**
Same page, same button — `python.org/downloads` → **Download Python 3.12.x**. This downloads a `.exe`.

**Critical step:** when you run the installer, the very first screen has a checkbox at the bottom labeled **"Add Python 3.12 to PATH."** Check that box *before* clicking anything else, then click **Install Now**. If you skip this, `python` will not work in your terminal at all, and you'll have to reinstall from scratch.

Verify in PowerShell (Start menu → type "PowerShell"):
```powershell
python --version
```
Expected: `Python 3.12.x`.

---

### STEP 2 — INSTALL VS CODE (5:00–7:30)

**Mac:**
Go to `code.visualstudio.com` → **Download for Mac**. This downloads a `.zip`. Open your Downloads folder, double-click to unzip, then drag `Visual Studio Code.app` into your Applications folder. Open it from Applications or Spotlight.

**Windows:**
Same site → **Download for Windows**. Run the `.exe` installer. Accept the license agreement, and on the **Select Additional Tasks** screen, check both **Add to PATH** boxes. Click through to install.

Either platform — verify VS Code opens without an error. That's the whole check for this step.

---

### STEP 3 — PYTHON + PYLANCE EXTENSIONS (7:30–9:00)

Same steps on Mac and Windows.

In VS Code, click the Extensions icon in the left sidebar — it looks like four squares — or press ⇧⌘X (Mac) / Ctrl+Shift+X (Windows).

Search for **Python**. Install the one published by **Microsoft** — it has millions of downloads and will be the top result. Wait for it to finish installing.

Then search for **Pylance**. Also published by Microsoft. Install it too — it gives you smarter autocomplete and inline type hints as you type.

**Check:** both Python and Pylance show a blue "Disable" button in your Installed extensions list — not "Install." If it still says "Install," the extension didn't finish.

---

### STEP 4 — HELLO-WORLD VERIFICATION (9:00–11:00)

This is the moment that proves Python, VS Code, and the extension are all talking to each other.

In VS Code: **File → New File**. Save it as `hello.py` on your Desktop (⌘S on Mac, Ctrl+S on Windows).

Type this one line — don't paste it:
```python
print("Hello, ISM2411")
```

Save the file. Right-click anywhere in the editor and choose **"Run Python File in Terminal."** A terminal panel opens at the bottom of VS Code and runs your file.

If VS Code shows a prompt like "No Python interpreter selected," or a pop-up in the bottom-right corner, click it and choose the Python 3.12.x entry from the list, then run the file again.

Expected output in the terminal panel:
```
Hello, ISM2411
```

If you see that line, your environment is fully working. You're ready for Week 1.

---

### STEP 5 — DATACAMP ACCOUNT (11:00–11:30)

Nothing to install right now. USF has a free DataCamp for Classrooms license for this course — you'll do short interactive exercises there outside of class.

You'll get an invite link from the instructor in Week 1. Accept it with your USF email. No payment, no credit card — the course license covers everything.

---

### COMMON PROBLEMS (11:30–13:00)

**`'python' is not recognized` on Windows** — you missed the "Add Python to PATH" checkbox during install. Go to Settings → Apps, uninstall Python, reinstall with that box checked.

**`command not found: python` on Mac** — on Mac the command is `python3`, not `python`. Both work fine inside VS Code once the extension is installed; in the terminal, always type `python3`.

**"No Python interpreter selected"** — press ⇧⌘P (Mac) or Ctrl+Shift+P (Windows), type **Python: Select Interpreter**, press Enter, choose the Python 3.12 entry.

**Multiple Python versions installed** — common on Mac, and not a problem by itself. As long as the interpreter VS Code is using (shown in the bottom-right corner when a `.py` file is open) is 3.10 or higher, you're fine.

**No "Run Python File in Terminal" option on right-click** — the Python extension isn't installed or isn't enabled. Open Extensions (Ctrl+Shift+X), confirm it shows "Disable," and reload VS Code.

**Terminal prints an error instead of output** — read the message. A `SyntaxError` usually means a typo — check your quotation marks. A `ModuleNotFoundError` means a missing package, which shouldn't happen at this stage.

---

### GETTING HELP BEFORE DAY 1 (13:00–13:30)

Before posting anywhere, try explaining the problem out loud to something patient — a mug, a rubber duck, anything. That's rubber duck debugging, and it catches most setup problems: say what the step is *supposed* to do, then say exactly what you typed and what actually happened. The moment those two don't match, you've found it. You'll meet this trick again properly in Module 7.

Still stuck? Post in the course discussion board with your OS and version, which step you're on, and a screenshot of the error. The instructor monitors the board before the semester starts, and the first 15 minutes of Week 1 are reserved for setup troubleshooting — bring your laptop.

---

### RECAP AND CHECKLIST (13:30–end)

- [ ] Python installed — `python3 --version` (Mac) / `python --version` (Windows) shows 3.10+
- [ ] VS Code installed and opens without errors
- [ ] Python extension installed — Microsoft, shows "Disable"
- [ ] Pylance installed — Microsoft, shows "Disable"
- [ ] Interpreter selected — bottom-right corner shows Python 3.10+ with a `.py` file open
- [ ] `hello.py` runs and prints `Hello, ISM2411`
- [ ] DataCamp — nothing to do yet; accept the invite in Week 1 with your USF email

See you in Week 1 — Module 1: what is a computer.
