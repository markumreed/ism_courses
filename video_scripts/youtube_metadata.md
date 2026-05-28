# YouTube Metadata — All 33 Videos

Placeholder YouTube IDs follow the format `PLACEHOLDER_VXX`.
Replace each with the actual YouTube video ID after upload.
YouTube video ID is the 11-character string in the URL:
`https://www.youtube.com/watch?v=XXXXXXXXXXX`

---

## Phase 1 — Shared Videos

| # | Placeholder ID | Title | Runtime | Courses |
|---|---|---|---|---|
| 1 | PLACEHOLDER_V01 | Python Variables & Data Types for Business — ISM2411 / ISM3232 | 15 min | Both |
| 2 | PLACEHOLDER_V02 | Python Operators for Business — Arithmetic, Comparison & Logical | 15 min | Both |
| 3 | PLACEHOLDER_V03 | Python F-String Formatting for Business Reports | 12 min | Both |
| 4 | PLACEHOLDER_V04 | Python Conditionals for Business Logic — if, elif, else | 15 min | Both |
| 5 | PLACEHOLDER_V05 | Python For Loops & Iteration — Business Data Patterns | 18 min | Both |
| 6 | PLACEHOLDER_V06 | Python Dictionaries for Business Records — The Complete Guide | 15 min | Both |
| 7 | PLACEHOLDER_V07 | Python Functions for Business — def, Parameters & Return Values | 15 min | Both |
| 8 | PLACEHOLDER_V08 | Python Debugging — How to Read Tracebacks & Fix Errors | 12 min | Both |
| 9 | PLACEHOLDER_V09 | 5 Terminal Commands Every Python Developer Needs | 12 min | Both |
| 10 | PLACEHOLDER_V10 | Git Basics for Students — Add, Commit, Push Explained | 15 min | Both |
| 11 | PLACEHOLDER_V11 | GitHub Workflow for Class — Clone, Commit, Submit | 10 min | Both |
| 12 | PLACEHOLDER_V12 | AI Literacy for Programmers — When to Use AI & When Not To | 15 min | Both |

## Phase 2 — ISM2411 Only

| # | Placeholder ID | Title | Runtime | Course |
|---|---|---|---|---|
| 13 | PLACEHOLDER_V13 | What is a Computer? CPU, RAM & Storage Explained for Programmers | 15 min | ISM2411 |
| 14 | PLACEHOLDER_V14 | Install Python & VS Code — Run Your First Script | 12 min | ISM2411 |
| 15 | PLACEHOLDER_V15 | Python Lists & Tuples for Business Data | 15 min | ISM2411 |
| 16 | PLACEHOLDER_V16 | Python File I/O & CSV Reading for Business Data | 15 min | ISM2411 |
| 17 | PLACEHOLDER_V17 | pandas for Business — Load, Inspect & Filter DataFrames | 20 min | ISM2411 |
| 18 | PLACEHOLDER_V18 | Data Cleaning & Descriptive Stats in Python pandas | 20 min | ISM2411 |
| 19 | PLACEHOLDER_V19 | pandas groupby & Business Charts with matplotlib | 20 min | ISM2411 |
| 20 | PLACEHOLDER_V20 | Python Capstone Walkthrough — End-to-End Retail Sales Analysis | 25 min | ISM2411 |

## Phase 3 — ISM3232 Only

| # | Placeholder ID | Title | Runtime | Course |
|---|---|---|---|---|
| 21 | PLACEHOLDER_V21 | Developer Environment Setup — VS Code, Python, zsh, Git | 18 min | ISM3232 |
| 22 | PLACEHOLDER_V22 | Advanced Shell Tools — grep, find, zoxide & fzf for Developers | 18 min | ISM3232 |
| 23 | PLACEHOLDER_V23 | Python Virtual Environments & pip — venv, requirements.txt | 15 min | ISM3232 |
| 24 | PLACEHOLDER_V24 | The ISM3232 Submission Ritual — 9 Steps Every Assignment | 12 min | ISM3232 |
| 25 | PLACEHOLDER_V25 | Python While Loops & Accumulators for Business Logic | 12 min | ISM3232 |
| 26 | PLACEHOLDER_V26 | Python Testing with pytest — Write, Run & Organize Tests | 15 min | ISM3232 |
| 27 | PLACEHOLDER_V27 | Python OOP Part 1 — Classes, __init__ & Instance Methods | 20 min | ISM3232 |
| 28 | PLACEHOLDER_V28 | Python OOP Part 2 — Composition & Inheritance for Business Systems | 20 min | ISM3232 |
| 29 | PLACEHOLDER_V29 | Python OOP Part 3 — Design-First Multi-Class Systems | 20 min | ISM3232 |
| 30 | PLACEHOLDER_V30 | SQL Foundations for Business Apps | 20 min | ISM3232 |
| 31 | PLACEHOLDER_V31 | Python + SQLite Integration — sqlite3, database.py & pytest | 20 min | ISM3232 |
| 32 | PLACEHOLDER_V32 | Streamlit Business App — Build 5 Required Features | 20 min | ISM3232 |
| 33 | PLACEHOLDER_V33 | Add a Controlled AI Feature to Your Streamlit App — Anthropic API | 22 min | ISM3232 |

---

## How to Replace Placeholders After Upload

After uploading a video to YouTube, find its ID in the URL:
```
https://www.youtube.com/watch?v=dQw4w9WgXcQ
                                 ^^^^^^^^^^^^ this is the ID
```

Then search-and-replace across all HTML files:
```bash
# Example: replace V01 placeholder with real ID
find /home/markumreed/Documents/ism_courses -name "*.html" \
  -exec sed -i 's/PLACEHOLDER_V01/dQw4w9WgXcQ/g' {} \;
```

Or use the update script at the bottom of this file.

---

## Bulk Update Script

Save as `update_video_ids.py` and run after uploading videos:

```python
import subprocess
from pathlib import Path

# Fill in real YouTube IDs as videos are uploaded:
VIDEO_IDS = {
    "PLACEHOLDER_V01": "",   # Variables & Data Types
    "PLACEHOLDER_V02": "",   # Operators
    "PLACEHOLDER_V03": "",   # F-strings
    "PLACEHOLDER_V04": "",   # Conditionals
    "PLACEHOLDER_V05": "",   # For Loops
    "PLACEHOLDER_V06": "",   # Dictionaries
    "PLACEHOLDER_V07": "",   # Functions
    "PLACEHOLDER_V08": "",   # Debugging
    "PLACEHOLDER_V09": "",   # Terminal Commands
    "PLACEHOLDER_V10": "",   # Git Basics
    "PLACEHOLDER_V11": "",   # GitHub Workflow
    "PLACEHOLDER_V12": "",   # AI Literacy
    "PLACEHOLDER_V13": "",   # What is a Computer
    "PLACEHOLDER_V14": "",   # Python Setup
    "PLACEHOLDER_V15": "",   # Lists & Tuples
    "PLACEHOLDER_V16": "",   # CSV File I/O
    "PLACEHOLDER_V17": "",   # pandas Intro
    "PLACEHOLDER_V18": "",   # Data Cleaning
    "PLACEHOLDER_V19": "",   # Aggregation & Charts
    "PLACEHOLDER_V20": "",   # Capstone
    "PLACEHOLDER_V21": "",   # Dev Environment
    "PLACEHOLDER_V22": "",   # Advanced Shell
    "PLACEHOLDER_V23": "",   # Virtual Environments
    "PLACEHOLDER_V24": "",   # Submission Ritual
    "PLACEHOLDER_V25": "",   # While Loops
    "PLACEHOLDER_V26": "",   # pytest
    "PLACEHOLDER_V27": "",   # OOP I
    "PLACEHOLDER_V28": "",   # OOP II
    "PLACEHOLDER_V29": "",   # OOP III
    "PLACEHOLDER_V30": "",   # SQL Foundations
    "PLACEHOLDER_V31": "",   # Python + SQL
    "PLACEHOLDER_V32": "",   # Streamlit
    "PLACEHOLDER_V33": "",   # GenAI Feature
}

ROOT = Path("/home/markumreed/Documents/ism_courses")
html_files = list(ROOT.rglob("*.html"))

for placeholder, real_id in VIDEO_IDS.items():
    if not real_id:
        continue   # skip unassigned
    for path in html_files:
        content = path.read_text()
        if placeholder in content:
            path.write_text(content.replace(placeholder, real_id))
            print(f"  {path.name}: {placeholder} → {real_id}")

print("Done.")
```
