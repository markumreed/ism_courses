# Video 22: Advanced Shell — grep, find, zoxide & fzf

## YouTube Metadata

**Title:** Advanced Shell Tools — grep, find, zoxide & fzf for Developers | ISM3232
**Description:**
Go beyond the 5 core commands. In this video you'll learn grep (search file contents), find (locate files by name or type), and two modern speed tools — zoxide (smarter cd) and fzf (fuzzy finder). These are the tools professional developers use to navigate and search large codebases instantly.

**Chapters:**
0:00 — Why search tools matter in a growing project
1:30 — grep — search inside files
5:00 — find — locate files by name/type
8:00 — Combining grep and find
9:30 — zoxide — smarter directory jumping
12:00 — fzf — interactive fuzzy finder
14:30 — Recap

**Applies to:** ISM3232 Modules 2–3

**Tags:** grep tutorial, find command, zoxide, fzf fuzzy finder, shell tools, bash zsh tools, ISM3232, developer tools, terminal search, linux commands, command line tools

---

## Script

### INTRO (0:00–1:30)

You know `cd`, `ls`, `pwd`, `mkdir`, `touch`. That's enough to navigate a small project. But by Module 4 your ISM3232 repo will have 15+ Python files across 4+ directories. When you need to find which file contains a function, or where a specific import lives, typing `ls` won't cut it.

`grep` searches inside files. `find` locates files by name or type. `zoxide` remembers where you've been and jumps there instantly. `fzf` gives you an interactive fuzzy search over anything. Together these four tools let you move through a codebase the way professional developers do.

---

### grep (1:30–5:00)

`grep` searches for a pattern inside files and prints every line that matches.

```bash
grep "def " module07_functions.py
```

Output:
```
def calculate_tax(amount, rate):
def apply_discount(subtotal, rate):
def process_order(subtotal, discount_rate, tax_rate):
```

Every function definition in the file, instantly.

**Recursive search** — search in all files in a directory:
```bash
grep -r "import" ~/ism3232/
```

Finds every file that contains an import statement.

**Case-insensitive:**
```bash
grep -i "error" logs.txt    # matches Error, ERROR, error
```

**Show line numbers:**
```bash
grep -n "def " *.py    # shows filename and line number
```

**Search for a pattern across all Python files:**
```bash
grep -rn "calculate_tax" ~/ism3232/
```

Output:
```
module07/functions.py:12:def calculate_tax(amount, rate):
module08/debugging.py:34:    result = calculate_tax(subtotal, 0.08)
tests/test_functions.py:8:    assert calculate_tax(100, 0.08) == 8.0
```

You can see every place `calculate_tax` is defined and used across the entire project. This is how you navigate a codebase.

**ripgrep (rg)** — faster modern alternative to grep, with better defaults:
```bash
# Install: brew install ripgrep (Mac) or apt install ripgrep (WSL)
rg "calculate_tax" ~/ism3232/
```

`rg` ignores `.git` and `__pycache__` automatically, respects `.gitignore`, and is significantly faster on large codebases. Prefer it over `grep` when available.

---

### find (5:00–8:00)

`find` locates files and directories by name, type, size, or modification time.

```bash
# Find all Python files in the current directory and below:
find . -name "*.py"

# Find all directories named "venv":
find . -type d -name "venv"

# Find files modified in the last 24 hours:
find . -mtime -1

# Find all .py files larger than 10KB:
find . -name "*.py" -size +10k
```

Practical uses:

```bash
# Find where you saved a specific file:
find ~ -name "requirements.txt"

# Find all test files:
find . -name "test_*.py"

# Find all Python files, excluding venv:
find . -name "*.py" -not -path "*/venv/*"
```

**Delete all `__pycache__` folders** (safe to remove, Python rebuilds them):
```bash
find . -type d -name "__pycache__" -exec rm -rf {} +
```

---

### COMBINING grep AND find (8:00–9:30)

Find Python files that contain a specific import:

```bash
# Method 1 — find all .py files, then grep each:
find . -name "*.py" -exec grep -l "import pandas" {} \;

# Method 2 — use xargs (faster for many files):
find . -name "*.py" | xargs grep -l "import pandas"

# Method 3 — just use rg:
rg --type py "import pandas"
```

Find the file where a specific function is defined:
```bash
grep -rn "^def calculate_" .
```

The `^` anchors to start of line — only matches function definitions, not calls.

---

### zoxide (9:30–12:00)

`cd` requires you to type the full path or navigate step by step. `zoxide` remembers every directory you've visited and lets you jump there with partial names.

Install:
```bash
# Mac:
brew install zoxide

# WSL:
sudo apt install zoxide
```

Add to `~/.zshrc`:
```bash
eval "$(zoxide init zsh)"
```

Reload:
```bash
source ~/.zshrc
```

Now use `z` instead of `cd`:

```bash
# First, visit directories normally so zoxide learns them:
cd ~/ism3232/module07_functions
cd ~/ism3232/module10_oop

# Now jump anywhere with partial name:
z module07     # → ~/ism3232/module07_functions
z oop          # → ~/ism3232/module10_oop
z ism3232      # → ~/ism3232
```

`zoxide` ranks directories by frequency of use. The more you visit a directory, the faster it learns to jump there from a partial name.

`zi` opens an interactive picker (requires fzf — next section):
```bash
zi   # shows recently visited dirs, fuzzy-searchable
```

---

### fzf (12:00–14:30)

`fzf` is a fuzzy finder — a tool that lets you interactively search and select from any list.

Install:
```bash
# Mac:
brew install fzf
$(brew --prefix)/opt/fzf/install   # enables key bindings

# WSL:
sudo apt install fzf
```

Add to `~/.zshrc`:
```bash
[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh
```

**Interactive file search:**
```bash
fzf
```

Typing filters the list in real time. Enter selects. Esc cancels.

**Open the selected file in VS Code:**
```bash
code $(fzf)
```

Type part of a filename, arrow to it, Enter — VS Code opens it.

**Search command history interactively:**
Press `Ctrl+R` in your terminal. Instead of scrolling through history, you get an interactive fuzzy search over every command you've ever run. Find `git commit -m` commands, `python3` runs, anything — type to filter.

**Search files with preview:**
```bash
fzf --preview "cat {}"
```

Shows file contents on the right as you navigate. Use this to quickly scan Python files before opening them.

---

### RECAP (14:30–18:00)

- `grep "pattern" file` — search inside files
- `grep -rn "pattern" directory/` — recursive, with line numbers
- `rg "pattern"` — faster modern grep, git-aware
- `find . -name "*.py"` — locate files by name or type
- `find . -name "test_*.py" | xargs grep -l "assert"` — combine find + grep
- `z directory_name` — jump to frequently-visited dirs (zoxide)
- `fzf` — interactive fuzzy search over files, history, anything
- `Ctrl+R` with fzf — fuzzy-search your command history

Install these tools at the start of the course. The time saved over 16 modules is significant.

Module 3: virtual environments and .zshrc — isolating your project dependencies.
