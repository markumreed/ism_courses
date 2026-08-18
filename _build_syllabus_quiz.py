#!/usr/bin/env python3
"""Build the First-Day-Attendance / Syllabus Quiz QTI package for both
courses — required by USF policy to confirm enrollment, distinct from the
weekly content quizzes _build_qti.py builds from reading-page content.

Output: quiz_exam_fa26/
  ism2411_syllabus_quiz.zip
  ism3232_syllabus_quiz.zip
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "quiz_exam_fa26"

# Reuse the QTI XML builders from _build_qti.py (up through write_zip) rather
# than duplicating them — _build_qti.py's own weekly-quiz build is top-level
# code below the "# ── main" marker, so only exec the reusable header above it.
_src = (ROOT / "_build_qti.py").read_text(encoding="utf-8")
_header = _src[: _src.index("# ── main")]
_ns = {"__file__": str(ROOT / "_build_qti.py")}
exec(_header, _ns)
write_zip = _ns["write_zip"]

ISM2411_ITEMS = [
    {
        "type_label": "Q1 · Multiple Choice",
        "question": "What must you complete by the end of Week 1 to confirm your enrollment?",
        "options": ["The Module 1 Syllabus Quiz", "The pre-course DataCamp track", "An email to the instructor", "The Week 1 lab"],
        "answer": "The Module 1 Syllabus Quiz",
    },
    {
        "type_label": "Q2 · Multiple Choice",
        "question": "Weekly Labs are due when?",
        "options": ["Friday at 5:00 PM", "Sunday at 11:59 PM", "Monday before lab", "Whenever you finish"],
        "answer": "Sunday at 11:59 PM",
    },
    {
        "type_label": "Q3 · True / False",
        "question": "You get unlimited free extensions on weekly labs.",
        "answer": "False — you get one 48-hour no-questions-asked extension per semester, and it can't be used on the midterm or capstone.",
        "options": [],
    },
    {
        "type_label": "Q4 · Multiple Choice",
        "question": "Which AI use requires disclosure in your submission comment?",
        "options": [
            "Asking AI to explain a concept you don't understand",
            "Asking AI to explain what went wrong after an error",
            "Using AI-generated code you understand and can explain",
            "None of the above ever need disclosure",
        ],
        "answer": "Using AI-generated code you understand and can explain",
    },
    {
        "type_label": "Q5 · Multiple Choice",
        "question": "Is group work allowed on labs?",
        "options": [
            "Yes, labs may be submitted as a group",
            "No — all work is individual",
            "Only for the capstone",
            "Only with instructor permission each time",
        ],
        "answer": "No — all work is individual",
    },
    {
        "type_label": "Q6 · True / False",
        "question": "Missing the Module 1 Syllabus Quiz deadline can get you dropped from the course per USF policy.",
        "answer": "True — first day attendance quizzes confirm active participation, and USF policy allows dropping students who don't complete them by the deadline.",
        "options": [],
    },
]

ISM3232_ITEMS = [
    {
        "type_label": "Q1 · Multiple Choice",
        "question": "What must you complete to confirm your enrollment?",
        "options": ["The First Day Attendance Quiz", "Assignment 1", "The pre-course setup guide", "A syllabus email"],
        "answer": "The First Day Attendance Quiz",
    },
    {
        "type_label": "Q2 · Multiple Choice",
        "question": "How is every assignment submitted in this course?",
        "options": ["Uploaded as a .zip file", "A GitHub URL, not a file upload", "Emailed to the instructor", "Pasted into a Canvas text box"],
        "answer": "A GitHub URL, not a file upload",
    },
    {
        "type_label": "Q3 · True / False",
        "question": "Late work can be resubmitted for a revised grade.",
        "answer": "False — no rewrites or resubmissions of any assignment are permitted in this course.",
        "options": [],
    },
    {
        "type_label": "Q4 · Multiple Choice",
        "question": "What must you do before asking AI to help with a bug?",
        "options": [
            "Nothing — ask AI first, then verify",
            "Attempt at least one fix yourself first (Debug First, Then Ask)",
            "Wait for office hours",
            "Ask a classmate to fix it with you",
        ],
        "answer": "Attempt at least one fix yourself first (Debug First, Then Ask)",
    },
    {
        "type_label": "Q5 · True / False",
        "question": "Group work is permitted on weekly assignments.",
        "answer": "False — all assignments and assessments must be completed individually.",
        "options": [],
    },
    {
        "type_label": "Q6 · Multiple Choice",
        "question": "What's assessed in the Developer Workflow grade (15%)?",
        "options": [
            "Only whether the code produces the correct output",
            "Ritual adherence, ruff formatting, pytest results, and commit quality",
            "Attendance in the weekly lab only",
            "The number of commits, regardless of content",
        ],
        "answer": "Ritual adherence, ruff formatting, pytest results, and commit quality",
    },
]

OUT.mkdir(parents=True, exist_ok=True)

print("Building Syllabus Quiz QTI files → quiz_exam_fa26/\n")

write_zip(OUT / "ism2411_syllabus_quiz.zip", "ism2411_syllabus_quiz", "ISM2411 — Module 1 Syllabus Quiz", ISM2411_ITEMS)
write_zip(OUT / "ism3232_syllabus_quiz.zip", "ism3232_syllabus_quiz", "ISM3232 — First Day Attendance Quiz", ISM3232_ITEMS)

print("\nDone.")
