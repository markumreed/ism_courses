#!/usr/bin/env python3
"""Replace YouTube placeholder IDs across all course HTML files.

Fill in real YouTube IDs as videos are uploaded, then run:
    python update_video_ids.py

The YouTube video ID is the 11-character string in the URL:
    https://www.youtube.com/watch?v=XXXXXXXXXXX
                                   ^^^^^^^^^^^^ this is the ID
"""

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

# Phase 4 — ISM2411 lab video IDs (scoped to ism2411/pages/ only)
ISM2411_LAB_IDS = {
    "PLACEHOLDER_LAB_W01": "",   # ISM2411 Lab W01 — Dev Environment Setup
    "PLACEHOLDER_LAB_W02": "",   # ISM2411 Lab W02 — Python Setup & First Script
    "PLACEHOLDER_LAB_W03": "",   # ISM2411 Lab W03 — Product Pricer with F-Strings
    "PLACEHOLDER_LAB_W04": "",   # ISM2411 Lab W04 — Conditionals
    "PLACEHOLDER_LAB_W05": "",   # ISM2411 Lab W05 — For Loops
    "PLACEHOLDER_LAB_W06": "",   # ISM2411 Lab W06 — Dictionaries
    "PLACEHOLDER_LAB_W07": "",   # ISM2411 Lab W07 — Functions
    "PLACEHOLDER_LAB_W08": "",   # ISM2411 Lab W08 — Debugging
    "PLACEHOLDER_LAB_W10": "",   # ISM2411 Lab W10 — Lists & Tuples
    "PLACEHOLDER_LAB_W11": "",   # ISM2411 Lab W11 — CSV File I/O
    "PLACEHOLDER_LAB_W12": "",   # ISM2411 Lab W12 — pandas Intro
    "PLACEHOLDER_LAB_W13": "",   # ISM2411 Lab W13 — Data Cleaning
    "PLACEHOLDER_LAB_W14": "",   # ISM2411 Lab W14 — Aggregation & Charts
    "PLACEHOLDER_LAB_W15": "",   # ISM2411 Lab W15 — Capstone
}

# Phase 5 — ISM3232 lab video IDs (scoped to ism3232/docs/ only)
ISM3232_LAB_IDS = {
    "PLACEHOLDER_LAB_W01": "",   # ISM3232 Lab W01 — Dev Environment Setup
    "PLACEHOLDER_LAB_W02": "",   # ISM3232 Lab W02 — Advanced Shell Navigation
    "PLACEHOLDER_LAB_W03": "",   # ISM3232 Lab W03 — Virtual Environments & .zshrc
    "PLACEHOLDER_LAB_W04": "",   # ISM3232 Lab W04 — Search, Git & Submission Ritual
    "PLACEHOLDER_LAB_W05": "",   # ISM3232 Lab W05 — Variables, Data Types & Operators
    "PLACEHOLDER_LAB_W06": "",   # ISM3232 Lab W06 — Conditionals, Loops & Dictionaries
    "PLACEHOLDER_LAB_W07": "",   # ISM3232 Lab W07 — Functions, Modules & pytest
    "PLACEHOLDER_LAB_W08": "",   # ISM3232 Lab W08 — Debugging, AI Literacy & Midterm Review
    "PLACEHOLDER_LAB_W10": "",   # ISM3232 Lab W10 — OOP I: Classes & Objects
    "PLACEHOLDER_LAB_W11": "",   # ISM3232 Lab W11 — OOP II: Composition, Inheritance & SQL Mapping
    "PLACEHOLDER_LAB_W12": "",   # ISM3232 Lab W12 — OOP III: Applied Practice & Design
    "PLACEHOLDER_LAB_W13": "",   # ISM3232 Lab W13 — Capstone Design & SQL Foundations
    "PLACEHOLDER_LAB_W14": "",   # ISM3232 Lab W14 — Python + SQL Integration
    "PLACEHOLDER_LAB_W15": "",   # ISM3232 Lab W15 — Streamlit Business Interface
    "PLACEHOLDER_LAB_W16": "",   # ISM3232 Lab W16 — GenAI Feature & Final Demo
}

ROOT        = Path("/home/markumreed/Documents/ism_courses")
ism2411_dir = ROOT / "ism2411" / "pages"
ism3232_dir = ROOT / "ism3232" / "docs"

# Lecture videos — search all HTML files in both courses
html_files = list(ROOT.rglob("*.html"))
for placeholder, real_id in VIDEO_IDS.items():
    if not real_id:
        continue
    for path in html_files:
        content = path.read_text()
        if placeholder in content:
            path.write_text(content.replace(placeholder, real_id))
            print(f"  {path.relative_to(ROOT)}: {placeholder} → {real_id}")

# ISM2411 lab videos — scoped to ism2411/pages/
for placeholder, real_id in ISM2411_LAB_IDS.items():
    if not real_id:
        continue
    for path in ism2411_dir.glob("*.html"):
        content = path.read_text()
        if placeholder in content:
            path.write_text(content.replace(placeholder, real_id))
            print(f"  ism2411/{path.name}: {placeholder} → {real_id}")

# ISM3232 lab videos — scoped to ism3232/docs/
for placeholder, real_id in ISM3232_LAB_IDS.items():
    if not real_id:
        continue
    for path in ism3232_dir.glob("*.html"):
        content = path.read_text()
        if placeholder in content:
            path.write_text(content.replace(placeholder, real_id))
            print(f"  ism3232/{path.name}: {placeholder} → {real_id}")

print("Done.")
