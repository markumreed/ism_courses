# Video 00: Pre-Course Setup Tutorial — VS Code, WSL, Python, Git, zsh & GitHub

## YouTube Metadata

**Title:** ISM3232 Pre-Course Setup Tutorial — VS Code, WSL, Python, Git, zsh & GitHub
**Description:**
Everything to install, configure, and verify before Day 1 of ISM3232 — VS Code, Python 3, Git, zsh, a GitHub account, and (Windows only) WSL with Ubuntu. Mac and Windows instructions are both covered end to end, finishing with a six-command final verification. Budget 60–90 minutes; Windows users should add 20–30 minutes for the WSL install. Week 1 opens with a live terminal session, so this has to be done before you walk in.

Course page: https://markumreed.github.io/ism3232/docs/precourse.html

**Chapters:**
0:00 — Why this has to happen before Day 1
1:30 — What you're installing (overview)
3:00 — Tool 1: VS Code + the Python extension
6:00 — Tool 2: WSL + Ubuntu (Windows only)
11:00 — Tool 3: Python 3
13:00 — Tool 4: Git
15:30 — Tool 5: zsh and the VS Code integrated terminal
17:30 — Tool 6: GitHub account
19:30 — Tool 7: tree
21:00 — Final verification — six commands
23:00 — Common problems
24:30 — Getting help before Day 1
25:00 — Recap and checklist

**Applies to:** ISM3232 — before Module 1 / Day 1

**Tags:** ISM3232 precourse setup, WSL Ubuntu install, developer environment setup, zsh setup windows mac, python git github setup, VS Code integrated terminal, tree command, USF Muma, terminal setup tutorial

---

## Script

### INTRO — WHY THIS HAS TO HAPPEN BEFORE DAY 1 (0:00–1:30)

Week 1 of this course opens with a live terminal session. If your environment isn't ready, you can't follow along — you're watching, not doing. And if something breaks during install, you need time to fix it that you won't have on the morning of the first class.

Budget 60 to 90 minutes for this. If you're on Windows, add another 20 to 30 minutes, because you have one extra piece Mac doesn't need: WSL. If anything here doesn't work, post in the discussion board with a screenshot before Day 1 — don't sit on it.

---

### WHAT YOU'RE INSTALLING — OVERVIEW (1:30–3:00)

Six things, in this order:

1. **VS Code** — your editor for every script this semester.
2. **WSL + Ubuntu** — Windows only. Gives Windows a real Linux terminal. Mac skips this entirely.
3. **Python 3** — the language. Usually pre-installed on Mac; installed via Ubuntu's package manager on Windows.
4. **Git** — version control. Every major assignment is submitted through it.
5. **zsh** — the shell this course runs in. Default on Mac since Catalina; comes from Ubuntu on Windows.
6. **A GitHub account** — where your repositories live and how you submit work.

Plus one small utility, **tree**, for visualizing folder structures.

**If you're on Windows:** make sure Windows Update is fully current before you start, and know that WSL requires administrator access and a restart partway through.

---

### TOOL 1 — VS CODE (3:00–6:00)

**Mac:** Go to `code.visualstudio.com` → **Download for Mac**. Unzip it, drag `Visual Studio Code.app` into Applications, open it.

Then install the `code` terminal command: press ⇧⌘P to open the Command Palette, type **"Shell Command: Install 'code' command in PATH,"** press Enter. That lets you type `code .` from any terminal to open VS Code there.

Verify:
```bash
code --version
```
Expected: `1.80.x` or higher.

**Windows:** Same site → **Download for Windows**. Run the installer, accept the license, and on the **Select Additional Tasks** screen check *both* **Add to PATH** boxes — without this you can't use `code` from the terminal. Install, then restart your computer.

You'll verify `code --version` after WSL is set up in the next section, since the terminal you use to check it lives inside Ubuntu.

**Both platforms — install the Python extension:** Extensions icon in the sidebar (four squares) or ⇧⌘X / Ctrl+Shift+X. Search **Python**, install the one published by **Microsoft**. This is required regardless of OS.

---

### TOOL 2 — WSL + UBUNTU (WINDOWS ONLY) (6:00–11:00)

**Mac users: skip to Tool 3.** zsh is already your default shell on Catalina and later — you don't need this section.

**What WSL actually is:** Windows Subsystem for Linux gives your Windows machine a full Ubuntu Linux terminal running alongside Windows itself. It's not a separate computer or a VM you have to babysit — it shares your files and runs natively. Every terminal command in this course runs inside this Ubuntu environment.

**Step 1 — Check your Windows version.** WSL needs Windows 10 build 19041+ or Windows 11. Press Win+R, type `winver`, press Enter. Below 19041, run Windows Update first.

**Step 2 — Open PowerShell as Administrator.** Search "PowerShell" from Start, right-click it, **Run as administrator**, accept the UAC prompt.

**Step 3 — Install WSL:**
```powershell
wsl --install
```
This installs WSL 2 and Ubuntu automatically — 5 to 15 minutes depending on your connection.

**Step 4 — Restart your computer when it finishes.** WSL will not work until after the restart.

**Step 5 — Complete Ubuntu's first-run setup.** Ubuntu opens automatically after restart and asks you to create a UNIX username and password — lowercase, no spaces. This is separate from your Windows login, and the password won't show characters as you type. That's normal.

**Step 6 — Install zsh inside Ubuntu**, one command at a time:
```bash
sudo apt update
sudo apt install zsh -y
chsh -s $(which zsh)
```
Enter your Ubuntu password when asked. Close and reopen the Ubuntu window — the prompt should change, confirming you're now in zsh.

Verify:
```bash
echo $SHELL
```
Expected: `/usr/bin/zsh` or `/bin/zsh`.

**If `wsl --install` fails with a virtualization error:** restart, enter BIOS/UEFI (usually Del or F2 at startup), find "Virtualization Technology" or "Intel VT-x," enable it, save, restart, and try `wsl --install` again.

---

### TOOL 3 — PYTHON 3 (11:00–13:00)

**Mac:** Check first — Python 3 may already be there:
```bash
python3 --version
```
3.10 or higher and you're done. If it's missing or too old, run:
```bash
xcode-select --install
```
This installs Python 3 and Git together via Xcode's Command Line Tools — 5 to 10 minutes. If that doesn't work, fall back to the `.pkg` installer at `python.org/downloads`.

**Windows (inside WSL Ubuntu):** Python 3 ships with Ubuntu. Open your Ubuntu terminal:
```bash
python3 --version
```
If it's older than 3.10:
```bash
sudo apt update
sudo apt install python3 python3-pip -y
python3 --version
```

Verify (both platforms): `python3 --version` returns `3.10.x` or higher.

---

### TOOL 4 — GIT (13:00–15:30)

**Mac:**
```bash
git --version
```
If `xcode-select --install` already ran in the previous step, Git is already there. If not, run it now — Git is bundled in.

**Windows (WSL Ubuntu):** Git is pre-installed:
```bash
git --version
```

**Both platforms — configure your identity.** This is attached to every commit you make and shows up on your GitHub profile:
```bash
git config --global user.name "Your Full Name"
git config --global user.email "you@youremail.com"
git config --global --list
```
The last command prints your config back — confirm your name and email are correct.

Verify: `git config --global user.name` returns your name exactly as you typed it.

---

### TOOL 5 — ZSH AND THE VS CODE TERMINAL (15:30–17:30)

**Mac:**
```bash
echo $SHELL
```
Expected: `/bin/zsh`. If you see `/bin/bash` instead:
```bash
chsh -s /bin/zsh
```
Enter your password, close and reopen the terminal, confirm again.

Then point VS Code's integrated terminal at zsh: Settings (⌘,) → search **"terminal default profile"** → set **Terminal > Integrated > Default Profile: Osx** to `zsh`. Close any open terminal panels and open a new one with ⌘\` — the prompt should show `%`.

**Windows:** zsh was already set up inside Ubuntu back in Tool 2 — confirm it in the Ubuntu terminal:
```bash
echo $SHELL
```
Then point VS Code at WSL: Ctrl+Shift+P → **"Terminal: Select Default Profile"** → choose **Ubuntu (WSL)**. Open a new terminal with Ctrl+\` — it should open inside Ubuntu with a zsh prompt.

Verify (both): `echo $SHELL` shows `/bin/zsh` or `/usr/bin/zsh`, and it's the shell VS Code's integrated terminal opens by default.

---

### TOOL 6 — GITHUB ACCOUNT (17:30–19:30)

Go to `github.com`, click **Sign up**. Use a professional email you actually check.

**Choose your username carefully** — it appears on your capstone portfolio and every commit you make this semester. Something like firstname-lastname works well; avoid nicknames or random numbers.

Verify your email — GitHub sends a confirmation link, and you can't create repositories until you click it.

**Authentication for pushing code:** HTTPS is the simplest path for this course. The first time you push, VS Code or Git prompts you to log in. If asked for a token instead of a password, generate one at GitHub.com → Settings → Developer Settings → Personal Access Tokens → Tokens (classic) → Generate new token, with the `repo` scope checked. Paste that token when Git asks for your password.

Verify: log in at github.com and your profile page loads with your username.

---

### TOOL 7 — TREE (19:30–21:00)

A small tool that prints a visual directory tree — used in every lab and in the submission ritual.

**Mac:** Install Homebrew first if you don't have it:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
Follow the prompts — it may print one or two commands at the end to add itself to your PATH; run those. Then:
```bash
brew install tree
```

**Windows (WSL Ubuntu):**
```bash
sudo apt install tree -y
```

Verify (both): `tree --version` prints a version number.

---

### FINAL VERIFICATION — SIX COMMANDS (21:00–23:00)

Open VS Code, open the integrated terminal (⌘\` / Ctrl+\`), confirm it's running zsh, then run these six, one at a time:

```bash
echo $SHELL        # /bin/zsh (Mac) or /usr/bin/zsh (WSL)
zsh --version       # zsh 5.x or higher
python3 --version   # Python 3.10.x or higher
git --version       # git version 2.x.x
pwd                 # /Users/yourname (Mac) or /home/yourname (WSL)
ls                  # Desktop, Documents, Downloads, and other folders
```

All six need to return real output with no "command not found." If they do, you're ready for Day 1.

---

### COMMON PROBLEMS (23:00–24:30)

**Prompt shows `$` instead of `%`** — you're in bash, not zsh. Mac: `chsh -s /bin/zsh` and restart the terminal. Windows: make sure VS Code's terminal profile is set to Ubuntu (WSL), not PowerShell.

**`python3: command not found`** — Mac: run `xcode-select --install`. Windows/WSL: `sudo apt install python3 -y` inside Ubuntu.

**`git: command not found`** — Mac: `xcode-select --install`. Windows/WSL: `sudo apt install git -y`, then set your identity.

**`code: command not found` in the terminal** — ⇧⌘P (Mac) / Ctrl+Shift+P (Windows) → "Shell Command: Install 'code' command in PATH" → Enter → restart the terminal.

**WSL install fails with a virtualization error** — enable Intel VT-x / AMD-V / "Virtualization Technology" in BIOS/UEFI (Del, F2, or F10 at startup), save, restart, retry `wsl --install`.

**VS Code terminal opens PowerShell instead of WSL** — Ctrl+Shift+P → "Terminal: Select Default Profile" → Ubuntu (WSL) → open a new terminal panel.

**`brew: command not found` after installing Homebrew** — run the one or two PATH-setup commands Homebrew printed at the end of its own install, then reopen the terminal.

**`chsh: PAM authentication error` switching to zsh on WSL** — try `sudo chsh -s $(which zsh) $USER` instead. If that still fails, `wsl --unregister Ubuntu` and run `wsl --install` again.

**Python version shows 2.7 or older** — you ran `python`, not `python3`. This course always uses `python3`.

**Can't create a GitHub repository** — your email isn't verified yet. Check your inbox, or resend from github.com/settings/emails.

---

### GETTING HELP BEFORE DAY 1 (24:30–25:00)

Post in the course discussion board with: your operating system and version, which step you're stuck on, the exact command you typed, the exact error message (a screenshot is best), and what you already tried. The instructor monitors the board before the semester starts — don't wait until Day 1 to report a setup problem, because it will put you behind immediately once class starts.

---

### RECAP AND CHECKLIST (25:00–end)

- [ ] VS Code installed — opens cleanly, `code --version` returns 1.80+
- [ ] Python extension installed — Microsoft, shows "Disable"
- [ ] Windows only — WSL Ubuntu installed and zsh set as its default shell
- [ ] zsh terminal — VS Code's integrated terminal opens in zsh, not bash or PowerShell
- [ ] Python 3.10+ — `python3 --version` confirms it
- [ ] Git installed and configured — `user.name` and `user.email` both set
- [ ] tree installed — `tree --version` returns a version
- [ ] GitHub account created — professional username, email verified, can log in
- [ ] All six final-verification commands return expected output in one terminal session

Module 1: developer mindset and your first setup lab.
