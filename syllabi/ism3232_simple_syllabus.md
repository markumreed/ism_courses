# SimpleSyllabus Content — ISM3232: Business Application Development
# USF Muma College of Business
#
# Sections marked [PRIVATE] are visible only to enrolled students and admin users.
# Sections marked [PUBLIC] appear on the public-facing syllabus.
# Sections marked [OPTIONAL] can be hidden if unused.

---

## COURSE PURPOSE [PRIVATE]

ISM3232: Business Application Development is a required upper-division course in the Information Systems major at USF's Muma College of Business. It is the direct continuation of ISM2411 (Python for Business) and a prerequisite for upper-level IS electives in data engineering, systems analysis, and enterprise application development.

The course addresses a persistent gap in business IS education: most students learn to write scripts, but few learn to build — that is, to design and deploy a complete, maintainable application. ISM3232 closes that gap by moving students from scripting (which they developed in ISM2411) to professional software development practice: object-oriented design, automated testing, database integration, web-based interfaces, and a controlled AI feature. The course is structured around the same workflow professional developers use, so that students graduate with transferable skills, not just course-specific knowledge.

The final product of the course is a complete, live Streamlit business application with a SQLite database backend and an AI-powered feature. Students demo the working application in the final week. The GitHub portfolio accumulated across all 16 weeks is itself a deliverable — it demonstrates iterative development in a way that a collection of uploaded files never could. This course is core to the IS curriculum, not an elective.

---

## COURSE FORMAT [PUBLIC]

ISM3232 is offered in-person with a hybrid option. Class sessions run once or twice weekly (check your section schedule in Canvas). Each session combines: (1) reading review and extension by the instructor, (2) live coding demonstrations with student participation, and (3) in-class lab practice. Discussion is occasional; the primary learning mode is coding — students are expected to have VS Code and a terminal open during every session.

The course uses a professional developer workflow from Day 1: terminal navigation, virtual environments, automated code formatting (ruff), automated testing (pytest), and version control (Git and GitHub). Every assignment is submitted as a GitHub URL, not a file upload. This mirrors industry practice and is a deliberate design decision — employers recognize GitHub-based portfolios in a way they do not recognize Canvas assignment archives.

Learning is assessed through weekly coding assignments (25%), developer workflow adherence (15%), a practical midterm exam (20%), a four-week capstone project (30%), a GitHub portfolio (5%), and participation (5%).

---

## STUDENT LEARNING OUTCOMES [PUBLIC]

Students who complete ISM3232 will be able to:

1. **(SLO-1)** Develop the skills needed to develop software — including command-line proficiency, virtual environment management, automated linting and testing, and professional version control with Git and GitHub.

2. **(SLO-2)** Understand necessary techniques for effective software development — including object-oriented design with classes, composition and inheritance, modular architecture, relational database integration, and systematic debugging.

3. **(SLO-3)** Examine and apply various programming methodologies using a modern programming language:
   - **(SLO-3a)** Apply software development methodologies including design-first OOP, iterative development with frequent commits, and test-driven development with pytest.
   - **(SLO-3b)** Apply programming techniques including class design, composition, inheritance, SQL integration with the Python sqlite3 module, and multi-tab web application development with Streamlit.
   - **(SLO-3c)** Build and deploy a complete business application using Python, SQLite, Streamlit, and the Anthropic API with appropriate safety and access controls.

---

## COURSE OBJECTIVES [PUBLIC]

Students will work toward the learning outcomes above through the following course objectives:

1. Configure and use a professional developer environment: zsh shell, VS Code, Python virtual environments (venv + pip), ruff, and pytest
2. Execute the nine-step pre-submission ritual consistently — confirming directory, structure, virtual environment, formatting, linting, tests, and version control before every major push
3. Write Python functions with type hints and passing pytest tests; structure code in modules with clear separation of concerns
4. Design object-oriented systems using classes, the `__init__` method, composition, and inheritance; write a design document before writing code
5. Design and implement a relational database schema using SQLite; write Python code with the sqlite3 module to perform all five CRUD operations with parameterized queries
6. Build a multi-tab, interactive Streamlit web application with full Create, Read, Update, and Delete (CRUD) functionality backed by a SQLite database
7. Integrate a controlled AI feature into a Python application using the Anthropic API, applying all six required safety controls
8. Use Git and GitHub to track iterative development with descriptive commit messages across a full semester-long project, resulting in a professional GitHub portfolio

---

## REQUIRED TEXTS AND COURSE MATERIALS [PUBLIC]

**Course Website:** The course website (link provided in Canvas) is the primary reference for this course. All readings, lecture notes, lab instructions, slides, unit overviews, cheat sheets, and the pre-course setup guide are on the course website. There is no textbook to purchase.

**Pre-Course Setup Guide:** Available on the course website. Must be completed before Week 1. Covers installation and verification of every required tool. Students who arrive without a working environment in Week 1 fall behind immediately.

All resources are free.

### Supplementary (Optional) Texts and Materials

The following resources were used in developing course content and are recommended for deeper study:

- *Think Python, 3rd edition* — Allen Downey (free at allendowney.github.io/ThinkPython) — recommended companion for Units 1–2
- Official Python documentation — docs.python.org — authoritative reference for built-in functions and modules
- Streamlit documentation — docs.streamlit.io — widget reference and execution model; required reading for Week 15
- SQLite documentation — sqlite.org/docs.html — SQL syntax reference; required for Weeks 13–14
- Anthropic API documentation — docs.anthropic.com — Messages API reference; required for Week 16
- ruff documentation — docs.astral.sh/ruff — linting rule reference for when ruff flags unfamiliar code
- GitHub documentation — docs.github.com — Git and GitHub reference
- *Python Object-Oriented Programming* — Steven Lott & Dusty Phillips
- *Architecture Patterns with Python* — Harry Percival & Bob Gregory

---

## HOW TO SUCCEED IN THIS COURSE [PUBLIC]

ISM3232 is a hands-on, professional-track course. Students who succeed treat it like a job: they show up, they practice, and they commit code regularly.

**Complete the Pre-Course Setup before Week 1.** Students who arrive without Python, VS Code, Git, and a GitHub account installed fall behind immediately. The pre-course setup guide on the course website walks through every step with verification checks. Do not skip this.

**Do the reading before each session.** The instructor builds on the reading — not from scratch. Arriving unprepared wastes your class time and everyone else's.

**Commit code frequently, not all at once.** The instructor reads your Git log as part of grading. One commit at 11:55 PM tells a very different story from ten commits across a week. Commit every time something meaningful works.

**Run ruff and pytest before every submission.** Never push code that fails either check. This is not a suggestion — it is a professional standard and is explicitly part of the Developer Workflow grade (15% of your semester).

**Start the capstone early.** The final four weeks build incrementally: proposal and SQL schema (Week 13), database integration (Week 14), Streamlit interface (Week 15), AI feature and demo (Week 16). Students who fall behind in Week 13 cannot recover by Week 16.

**Use office hours for stuck debugging.** Bring your GitHub link, the complete traceback, and a description of what you already tried. You will leave understanding something you did not understand before.

**What you need coming in:** This course requires ISM2411 or equivalent prior Python experience. You should be comfortable writing functions, using loops and conditionals, and working with lists and dictionaries before Week 1. If you feel shaky on any of these, review the ISM2411 course website before class begins.

---

## COMMUNICATION [PUBLIC]

All course announcements are posted in Canvas. Check Canvas daily — not weekly.

For individual questions, use Canvas Mail or your USF email. Every message must include: your full name and U Number, your course and section number, and the specific reason for your message stated in the first sentence.

For coding issues, also include: your GitHub repository link and a complete screenshot of the full traceback — from "Traceback (most recent call last)" to the final error line. Incomplete messages (missing GitHub link, missing full traceback, outdated repository) will be returned without a diagnosis.

The instructor will respond within **48 business hours** (Monday–Friday). Messages received after 5 PM on Friday receive a response by end of business on Monday. The instructor does not routinely reply on weekends.

**Professional standards for all communications:**

| Standard | Correct | Incorrect |
|----------|---------|-----------|
| Greeting | "Dear Professor [Last Name]," or "Dear Dr. [Last Name]," | "Hey," / "Hi," / no greeting |
| Sign-off | "Sincerely, [Full Name] / U Number: U12345678" | "Thanks" / first name only |
| Tone | Respectful, specific, professional | Demanding, vague, or overly casual |

Messages that do not meet professional standards will be returned without a response.

---

## GRADING SCALE [PUBLIC]

| Grade | Range (%) | Grade | Range (%) | Grade | Range (%) |
|-------|-----------|-------|-----------|-------|-----------|
| A     | 93–100    | B     | 83–86     | C     | 73–76     |
| A−    | 90–92     | B−    | 80–82     | C−    | 70–72     |
| B+    | 87–89     | C+    | 77–79     | D     | 60–69     |
|       |           |       |           | F     | 0–59      |

---

## GRADE CATEGORIES AND WEIGHTS [PUBLIC]

| Component | Weight | Details |
|-----------|--------|---------|
| Developer Workflow | 15% | Ritual adherence, ruff formatting, pytest results, and Git commit quality — assessed holistically across all submissions throughout the semester. |
| Weekly Assignments & Quizzes | 25% | One coding assignment per active week, submitted as a GitHub URL. Lowest grade dropped. Quizzes are completed in Canvas and tied to the assigned reading. |
| Midterm Practical Exam | 20% | Week 9. Open notes (own printed or handwritten materials only — no internet, no AI, no classmates). Covers Weeks 1–8: tracing code, fixing bugs, and writing functions. |
| Capstone Project | 30% | Weeks 13–16. Includes: proposal and SQL schema (Week 13), database integration (Week 14), Streamlit interface (Week 15), AI feature and live demo (Week 16). Submitted as a GitHub repository URL. |
| Portfolio | 5% | GitHub profile reflecting 16 weeks of iterative, committed development. Assessed at end of semester. |
| Participation | 5% | In-class engagement, discussion board contributions, peer feedback, and demonstration of professional effort. |
| **Total** | **100%** | |
| Automation Bonus | Up to +5% | Optional: automate a meaningful part of your development workflow. Details provided in Canvas. |

### Developer Workflow Grade (15%) — What Is Assessed

Every submission is reviewed for:
1. The nine-step pre-submission ritual was followed (evidence in Git log and terminal output)
2. `ruff format .` and `ruff check .` pass with zero errors
3. `pytest` passes with all tests green
4. Git commit messages are descriptive (not "fix," "final," "asdf")
5. Commit history shows iterative work — not a single commit at the deadline

---

## INSTRUCTOR FEEDBACK POLICY AND GRADE DISSEMINATION [OPTIONAL]

The instructor will respond to course-related email within 48 business hours (Monday–Friday). Feedback on weekly assignments will be posted in Canvas within one week of the submission deadline. Capstone milestone feedback will be provided within 72 hours of each milestone deadline. Final capstone grades and written feedback will be posted within two weeks of the final demo session.

You can view your grades at any time in Canvas under Grades. Grade disputes must be submitted within one week of receiving the grade. After this window, the grade is considered accepted and no further discussion will be possible.

---

## MAJOR TOPICS AND COURSE SCHEDULE [PUBLIC]

**Note: This schedule is tentative and subject to revision at the instructor's discretion. All changes will be announced in Canvas. The Final Exam is scheduled per the USF Final Examination calendar.**

| Week | Unit | Topic | Key Content | Deliverable |
|------|------|-------|-------------|-------------|
| 1 | U1 | Developer Mindset & Setup | VS Code · zsh · Python verify · first script · AI policy | Assignment 1: Setup screenshots |
| 2 | U1 | zsh Navigation & File Ops | pwd · ls · cd · tree · cp · mv · rm · ritual intro | Assignment 2: Terminal screenshots |
| 3 | U1 | Virtual Environments & .zshrc | venv · pip · requirements.txt · .gitignore · aliases | Assignment 3: venv + .zshrc |
| 4 | U1 | Search, Ritual & Git | ripgrep · nine-step ritual · git init / commit / push | Assignment 4: Ritual + GitHub URL |
| 5 | U2 | Variables, Data Types & Operators | str · int · float · bool · operators · input() · f-strings | Assignment 5: business_data.py |
| 6 | U2 | Conditionals, Loops & Dictionaries | if/elif/else · for loops · accumulator · list-of-dicts | Assignment 6: record_processor.py |
| 7 | U2 | Functions, Modules & pytest | def · return · type hints · scope · modules · 6 test types | Assignment 7: business_rules.py |
| 8 | U2 | Debugging & AI Literacy | Tracebacks · print() debugging · Debug-First workflow | Assignment 8: Fixed code + reflection |
| ★ 9 | U2 | **Midterm Practical Exam** | Open notes · Weeks 1–8 · Trace + Fix bug + Write code | Midterm exam |
| 10 | U3 | OOP I — Classes & Objects | class · `__init__` · self · methods · `__repr__` | Assignment 10: models.py |
| 11 | U3 | OOP II — Composition | Composition · manager class · inheritance · OOP → SQL bridge | Assignment 11: entity + manager |
| 12 | U3 | OOP III — Design & Practice | design.md first · 2 entities · 1 manager · 6 tests | Assignment 12: design.md + models |
| 13 | U4 | Capstone Design & SQL | PROPOSAL.md · CREATE · INSERT · SELECT · UPDATE · DELETE | Capstone: proposal + schema.sql |
| 14 | U4 | Python + SQL Integration | sqlite3 · ? placeholders · row_factory · tmp_path fixture | Capstone: database.py |
| 15 | U4 | Streamlit Interface | Rerun model · 5 tabs · Submit/View/Filter/Update/Report | Capstone: app.py |
| 16 | U4 | GenAI Feature & Final Demo | 6 controls · ai_feature.py · repo polish · live demo | Capstone: full repo + live demo |

★ Week 9 Midterm: open notes (own materials only). No internet access, no AI tools, no collaboration.

**University-Scheduled Final Exam:** [Date and time per USF Final Examination calendar — posted in Canvas.]

---

## COURSE POLICIES: GRADES [PUBLIC]

### First Day Attendance Policy
Students must complete the **First Day Attendance Quiz** on Canvas by the stated deadline. This quiz confirms your enrollment and active participation in the course. Students who do not complete the quiz by the deadline are subject to being dropped from the course per USF policy.

### Late Work Policy
All work is due at the stated deadline. There are no opportunities to make up missed assignments, quizzes, labs, or the midterm exam — except under the Medical Excuse Policy below. Missed or incomplete work receives a zero with no exceptions. There are also no opportunities to resubmit any work for a revised grade.

### Make-up Exams Policy
There is no default makeup window for the midterm practical exam. If you cannot attend the midterm due to a verified medical emergency, you must email the instructor **before the exam begins**. A verification-of-care letter from Student Health Services is required upon your return. Make-up exams, if granted, are given at the instructor's convenience.

### Medical Excuse Policy
Students should not attend class if ill, particularly with fever, gastrointestinal symptoms, or respiratory symptoms. Contact Student Health Services immediately:
- Tampa & Sarasota-Manatee: (813) 974-2331
- St. Petersburg: (727) 873-4422

A verification-of-care letter must be presented to the instructor upon the student's return to class.

### Extra Credit Policy
There are no extra credit opportunities in this course beyond the optional Automation Bonus (+5%). The bonus supplements — it does not replace — primary coursework. No other extra credit will be offered under any circumstances.

### Rewrite Policy
No rewrites, resubmissions, or revisions of any assignments are permitted in this course.

### Exam Retention Policy
Midterm exams are retained for one semester following the current semester and then destroyed. Students who wish to review their exam may do so during office hours within the one-week grade dispute window.

### Grade Dispute Policy
If you wish to dispute a grade, you must contact the instructor **within one week** of receiving the grade in Canvas. After this one-week window, the grade is considered accepted and no further discussions regarding that assignment are possible.

### Group Work Policy
There is no group work of any kind in this course. All assignments and assessments must be completed individually. Sharing code — by screen share, file transfer, messaging, or any other means — or submitting another student's work constitutes academic dishonesty and will be reported to the Office of Student Conduct.

### Grades of Incomplete
The current USF policy on incomplete grades will be followed. An "I" grade may be awarded only when a small portion of the student's work is incomplete and the student is otherwise earning a passing grade. The time limit may not exceed two academic semesters and/or graduation, whichever comes first. "I" grades not resolved within the time limit will be changed to "IF" or "IU."

### Final Examinations Policy
All final examinations are scheduled in accordance with USF's Final Examination Policy. The Week 16 capstone live demo serves as this course's final assessment. Students must be available for the scheduled demo window during final examination week.

---

## COURSE POLICIES: TECHNOLOGY AND MEDIA [PUBLIC]

### Canvas
This course uses USF's Canvas learning management system. All assignments, quizzes, deadlines, announcements, grades, and submission links are in Canvas. Students are responsible for checking Canvas daily. For Canvas help: (813) 974-1222 or help@usf.edu.

### Recordings
Class sessions may be recorded using lecture capture technology (Microsoft Teams or similar). Student participation in live class discussions may be recorded. Recordings are made available only to students enrolled in this course, to assist those who cannot attend the live session or who want to review content. Students who prefer to participate via audio only may disable their video camera. Please discuss this preference with the instructor.

### Laptop Requirement
A personal laptop is required for every class session. Mac or Linux are preferred; Windows is supported with WSL2 (Windows Subsystem for Linux). Chromebooks and tablets cannot run the required developer environment for this course. Contact the instructor in Week 1 if you need to discuss alternatives.

### Laptop Usage in Class
Laptops are required for all class activities — terminal work, coding, testing, and demos. Close social media and unrelated applications during instruction. During the midterm practical exam, laptops and all electronic devices are prohibited. The exam is open notes (own printed or handwritten materials only).

### Phone Usage
Phones must be silenced and put away during class sessions. Students may use devices to record lectures for personal use but must continue to meet classroom behavioral expectations. Phones are not permitted during the midterm exam.

### Online Exam Proctoring
If online proctoring is required for any assessment, students must have an operational webcam with a microphone. Students are required to use a private testing space, ensure their recordings do not violate third-party privacy rights, and accept all responsibility for meeting technical requirements. For additional information, visit the USF online proctoring student FAQ and Honorlock student resources.

---

## COURSE POLICIES: STUDENT EXPECTATIONS [PUBLIC]

### Health and Wellness
Your health is a priority at the University of South Florida. We encourage members of our community to look out for each other and reach out for help if someone is in need. If you or someone you know is in distress, please make a referral at www.usf.edu/sos so that Student Outreach & Support can provide resources. A 24-hour licensed mental healthcare professional is available through the USF Counseling Center at (813) 974-2831, option 3. In case of emergency, dial 9-1-1.

### Title IX Policy
USF is committed to fostering a safe and respectful learning environment, free from sex discrimination and sexual harassment, in accordance with Title IX and USF Policy 0-004. If a student shares an experience of sexual harassment, sexual assault, stalking, or relationship violence with a USF employee (including faculty), that employee will notify the Title IX Office. This allows the Title IX Office to send the student information about support resources and options. Students are not required to respond. The Title IX Office shares information only on a need-to-know basis. Confidential support: USF Center for Victim Advocacy, (813) 974-5757. Confidential resources do not notify the Title IX Office unless the student requests it. For more information or to make a report: www.usf.edu/title-ix.

### Academic Integrity
All academic work submitted in this course must be the student's own. Violations of the USF Academic Integrity Policy (FGCU 6C4-10.081) are reported to the Office of Student Conduct. Confirmed violations result in a zero on the assignment and may result in a failing grade for the course. The policy applies regardless of whether the student was aware of the rules.

### Course Hero / Chegg Policy
The USF Policy on Academic Integrity specifies that students may not use websites that enable cheating, such as by uploading or downloading material for this purpose. This applies specifically to Chegg.com and CourseHero.com — almost any use of these websites (including uploading proprietary course materials) constitutes a violation of the academic integrity policy.

### Professionalism Policy
Per university policy and classroom etiquette, mobile phones and similar devices must be silenced during all class and lab sessions. Students who do not comply will be asked to leave. Please arrive on time. Students who habitually disturb the class and have been warned may suffer a reduction in their final grade.

### Turnitin
In this course, Turnitin.com may be utilized for originality checking of written submissions. Turnitin compares submitted work against web content and a large database of prior submissions. Students may be expected to submit written assignments electronically for this purpose.

### Netiquette Guidelines
- Act professionally in all course communications. Treat your instructors and peers with the same respect you would bring to a workplace.
- Be respectful and sensitive when sharing your ideas and opinions.
- Proofread and check spelling before sending a message or posting to a discussion board.
- Avoid using all capital letters — it reads as shouting.
- Keep communications focused and on topic.
- Avoid humor or sarcasm in written messages — tone is easily misread without vocal cues.

### Email and Discussion Board Guidelines
- Use a meaningful subject line in every email.
- Keep messages and discussion posts related to course content.
- Personal, grade-related, or confidential matters should be sent directly to the instructor via email — not posted on a public discussion board.
- General debugging or concept questions that benefit the whole class are encouraged on the discussion board.

### End of Semester Student Evaluations
All USF courses use an online evaluation system. You will receive an email notification when the evaluation window opens at the end of the semester. Your participation is encouraged and valued.

### Food and Drink Policy (in-person sessions)
Only bottled water with a cap is permitted in the classroom. No other beverages, food, tobacco products, or similar items are allowed. This policy will be strictly enforced.

---

## GENERATIVE AI POLICY [PRIVATE]

AI tools are permitted in this course within explicitly defined boundaries. The AI policy is a core learning topic in this course — it is not an afterthought.

**Permitted uses:**
- Asking AI to explain what a traceback error means
- Asking AI to explain what a piece of code does in plain English
- Asking AI to suggest test cases for code you already wrote
- Using AI to understand a concept after you have attempted it independently
- Week 16 only: using the Anthropic API as a controlled application feature (this is a required assignment component, not general AI assistance)

**Prohibited uses:**
- Generating any submitted code — all submitted code must be written by the student
- Asking AI to fix bugs (you must attempt to debug independently first)
- Any AI use during the midterm practical exam
- Submitting AI-generated work without explicit disclosure
- Using AI to write the AI literacy reflection in Assignment 8

The Debug-First workflow (taught in Week 8 and assessed in Assignment 8) is the required approach to debugging: read the traceback bottom-up → write your hypothesis → add strategic print() statements → if stuck after 10 minutes, ask AI to explain the error only (not to fix it) → fix the code yourself → write the required reflection.

See the AI Use Policy section of the course syllabus and the AI policy page on the course website for the full policy details.

See also: USF Provost guidance at https://www.usf.edu/provost/faculty-success/teaching-learning/guidance-generative-ai.aspx.

---

## IMPORTANT DATES TO REMEMBER [PRIVATE — OPTIONAL]

All dates and assignments are tentative and may be changed at the discretion of the instructor with reasonable advance notice. For authoritative USF dates, see the Academic Calendar at http://www.usf.edu/registrar/calendars/

| Event | Date |
|-------|------|
| Drop/Add Deadline | [See academic calendar] |
| First Day Attendance Quiz Due | [End of Week 1] |
| Midterm Practical Exam | Week 9 |
| Mid-term Grading Opens | [See academic calendar] |
| Mid-term Grading Closes | [See academic calendar] |
| Withdrawal Deadline | [See academic calendar] |
| Capstone Proposal & Schema Due | Week 13 |
| Capstone Database Due | Week 14 |
| Capstone Streamlit Interface Due | Week 15 |
| Capstone Final Demo | Week 16 |
| Final Examination Week | [See academic calendar] |
| University Holidays | [See academic calendar] |
