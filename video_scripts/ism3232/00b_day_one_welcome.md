# Video 00b: Day One — Welcome to ISM3232

## YouTube Metadata

**Title:** ISM3232 Day One — Welcome, Course Website Tour, Syllabus, and Meet Dr. Reed
**Description:**
Your first watch for ISM3232: Business Application Development. This video walks the course website end to end, covers what's actually graded and how, and closes with a Meet Dr. Reed segment answering the questions students ask most in Week 1. Watch this before your first lab.

Course page: https://markumreed.github.io/ism3232/

**Chapters:**
0:00 — Welcome to ISM3232
1:15 — What this course is and who it's for
3:15 — Tour: the course website
8:30 — Tour: the syllabus
14:00 — Meet Dr. Reed — ask me anything
18:30 — What to do before Module 2
19:30 — Recap

**Applies to:** ISM3232 — Day 1 / Module 1, before the first lab

**Tags:** ISM3232 day one, welcome video, course orientation, USF Muma College of Business, Business Application Development syllabus, meet the instructor, course website tour

---

## Script

### WELCOME TO ISM3232 (0:00–1:15)

Hi, welcome to ISM3232, Business Application Development. I'm Dr. Reed, and I'll be teaching this course this semester.

This video is your Day One orientation. Before you open a terminal, I want you to know three things: where everything lives on the course website, what's actually graded and how work is submitted, and who's teaching this course and how to reach me. That's it — three things, about 19 minutes. Watch this in full before your first lab, and keep the course website open in a second tab while you do.

If you haven't done the Pre-Course Setup video yet — VS Code, Python, Git, zsh, GitHub, and WSL if you're on Windows — stop this video and do that first. This one assumes your environment is already installed and verified, because Week 1 opens with a live terminal session.

---

### WHAT THIS COURSE IS AND WHO IT'S FOR (1:15–3:15)

ISM3232 is the direct continuation of ISM2411. If you've already written functions, used loops and conditionals, and worked with lists and dictionaries, you're ready. If any of that feels shaky, pause and review the ISM2411 course website before you go further — this course does not re-teach Python basics.

Here's the gap this course closes: ISM2411 taught you to write scripts. This course teaches you to *build* — to design and deploy a complete, maintainable application, the way a professional developer actually works. That means a professional developer workflow from Day 1: terminal navigation, virtual environments, automated formatting with ruff, automated testing with pytest, and Git and GitHub for every single submission. Every assignment this semester is a GitHub URL, not a file upload — that mirrors how the industry actually works, and it's a deliberate choice, not a formality.

The destination is a complete, live Streamlit business application with a SQLite database backend and a controlled AI feature, built over the final four weeks and demoed live in Week 16. The GitHub portfolio you accumulate across all 16 weeks is itself a deliverable — it shows iterative development in a way a folder of uploaded files never could.

---

### TOUR: THE COURSE WEBSITE (3:15–8:30)

Pull up the course website now: **markumreed.github.io/ism3232**. Like ISM2411, this is your primary reference all semester — there is no textbook. Everything is here.

**The homepage.** The hero banner up top lists the stack for the semester: zsh, Python, Git, SQLite, Streamlit, the Anthropic API. Right below it, the **Interactive Course Map** — four units, click to expand topics, keyboard shortcuts 1 through 4.

**Pre-course setup.** First section on the page. You should already be through this — it's the tool-install checklist you needed before today.

**Unit overviews and course guide.** Skip the "For Instructors" card again — that's my own notes on assembling the course in 6, 9, or 16-week formats, not something you need. The four unit cards that matter to you:

- **Unit 1, Developer Foundations** — Modules 1 through 4: zsh navigation, virtual environments, the nine-step developer ritual, Git.
- **Unit 2, Python Foundations** — Modules 5 through 8, plus the midterm: types, control flow, functions and pytest, debugging and AI literacy.
- **Unit 3, Object-Oriented Design** — Modules 10 through 12: classes, composition, inheritance, applied design.
- **Unit 4, Capstone Build** — Modules 13 through 16: SQL foundations, Python-SQL integration, the Streamlit interface, the GenAI feature and final demo.

**Module cards.** Same three-pill system as ISM2411 — Reading, Lecture, Lab — one card per module, grouped by unit.

**Cheat sheets.** One per unit, four total. Keep these open while you work; the reference resources section below them also has a 72-term glossary, a troubleshooting page with 13 common errors and exact fixes, an Expectations page, and — worth a look — an interactive SLO mind map.

**Reference and syllabus.** The last section: the full **Syllabus**, the glossary, troubleshooting, expectations, and learning outcomes. We're going to the syllabus next.

Click through the course map and one module card yourself right now before moving on.

---

### TOUR: THE SYLLABUS (8:30–14:00)

Click into the **Syllabus** page. Read the whole thing yourself before Module 2 — here's what actually drives your week-to-week experience.

**Format.** Hybrid, same rhythm as ISM2411: reading, concept explanations, and live-coding demos online and self-paced before lab; one in-person lab per week where you apply the material with me there for real-time support. Week 1 — this week — has no in-person lab; pre-course setup and Assignment 1 are done independently online.

**How your grade breaks down:**
- Developer Workflow — 15%. Ritual adherence, ruff formatting, pytest results, and Git commit quality, assessed holistically across the whole semester.
- Weekly Assignments & Quizzes — 25%. One coding assignment per active week, submitted as a GitHub URL, lowest grade dropped.
- Midterm Practical Exam — 20%. Week 9, open notes — your own printed or handwritten materials only, no internet, no AI, no classmates. Covers Weeks 1 through 8.
- Capstone Project — 30%. Weeks 13 through 16: proposal and schema, database integration, Streamlit interface, then the AI feature and live demo.
- Portfolio — 5%. Your GitHub profile, assessed at the end of the semester.
- Lab Participation & Engagement — 5%.
- There's also an optional Automation Bonus worth up to +5% for automating part of your development workflow — details in Canvas.

**The policies most likely to affect you:**
- **The developer workflow grade** is not abstract — every submission is checked for the nine-step ritual, a clean `ruff format` and `ruff check`, a fully passing `pytest` run, descriptive commit messages, and iterative commit history, not one commit at the deadline.
- **Late work:** there is no default late window in this course. Missed or incomplete work receives a zero, with the single exception of a verified medical emergency under the Medical Excuse Policy. No rewrites or resubmissions of any kind.
- **Group work:** none, of any kind. Every assignment and assessment is individual. Sharing code by any means is reported to the Office of Student Conduct.
- **AI policy:** permitted uses are explaining a traceback, explaining what code does, suggesting test cases for code you already wrote, and understanding a concept after you've attempted it yourself. Prohibited: generating any submitted code, asking AI to fix your bugs, any AI use during the midterm, and undisclosed AI use. Week 8 teaches the required Debug-First workflow — read the traceback bottom-up, form a hypothesis, add print statements, and only after ten minutes stuck, ask AI to explain the error, not fix it — then write the fix yourself.
- **Communication:** check Canvas daily, not weekly. Email response window is 48 business hours on weekdays. Every message needs your name, U Number, section, and the reason stated in the first sentence; for code issues, also include your GitHub link and the complete traceback screenshot — incomplete messages get returned without a diagnosis.

Full detail — grading scale, the module-by-module schedule, capstone milestones, and university policies on Title IX, academic integrity, and accommodations — is on the syllabus page.

---

### MEET DR. REED — ASK ME ANYTHING (14:00–18:30)

Now, the part where you actually get to know who's teaching this.

[Instructor: open live to camera — who you are, your background, and why you teach this course the way you do. Then move into the questions below.]

**"I made it through ISM2411, but this looks like a big jump — should I be worried?"**
It is a real jump, and that's intentional — ISM2411 taught you to script, this course teaches you to build. But it's a jump the course is designed to walk you through step by step: Unit 1 rebuilds your developer habits before you write a line of new Python, and every OOP and database concept in Units 2 through 4 gets introduced with a small example before it shows up in your capstone. If Unit 1 feels slow, that's the point — it's building the foundation Units 2 through 4 lean on hard.

**"What's the best way to reach you, and how fast will you respond?"**
Canvas Mail or my USF email, with your name, U Number, section, and reason in the first sentence — for code questions, also attach your GitHub link and the complete traceback, from "Traceback (most recent call last)" to the last line. I respond within 48 business hours on weekdays; messages after 5 PM Friday get answered by end of day Monday.

**"What if I fall behind on the capstone?"**
Tell me the moment you notice it, not in Week 16. The capstone is built to be impossible to catch up on if you start late — proposal and schema in Week 13, database in Week 14, interface in Week 15, AI feature and live demo in Week 16 — each week assumes the last one is done. If Week 13 slips, come to office hours immediately; that's the only week where there's still room to recover.

**"What's your grading philosophy?"**
I grade what's actually in your Git log and your submitted repo — the developer workflow grade specifically rewards evidence of process, not just a working final product. A single commit at 11:59 PM tells a different story than ten commits across the week, and it's graded that way on purpose. If you disagree with a grade, you have one week from when it posts to raise it.

**"Office hours — when, and what should I bring?"**
Monday and Wednesday, 1:30 to 3 PM, in CIS 2070B. Can't make it in person? Check Canvas for the Teams link and join remotely. Bring your GitHub link, the complete traceback, and what you already tried. That gets you an actual answer in the time we have, instead of us spending the session just reproducing your error.

---

### WHAT TO DO BEFORE MODULE 2 (18:30–19:30)

Three things, before your first lab:
1. Read the full syllabus on the course website — there's no separate quiz to gate this one, but Module 1's ritual and Assignment 1 assume you've read the format and grading sections.
2. Confirm every tool from Pre-Course Setup verifies clean — VS Code, Python, Git, zsh, and (Windows) WSL.
3. Skim the Module 2 Reading and Lecture pages so the first in-person lab isn't the first time you're seeing zsh navigation.

Post any setup problems to the discussion board with a screenshot before Module 2 — don't walk into the first lab with a broken environment.

---

### RECAP (19:30–end)

The course website is your source of truth all semester — bookmark it. The syllabus tells you exactly what's graded, including the workflow grade most students underestimate — read it this week. And I'm one email away with a 48-hour response window, GitHub link and full traceback in hand, if anything comes up. Welcome to ISM3232 — I'll see you in Module 2.
