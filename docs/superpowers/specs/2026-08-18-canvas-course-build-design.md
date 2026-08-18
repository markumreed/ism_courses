# Canvas Course Build — ISM2411 & ISM3232

**Status:** Draft, pending user review
**Date:** 2026-08-18

## Goal

Build a clean, easy-to-follow Canvas course shell for ISM2411 (Python for
Business) and ISM3232 (Business Application Development) — Modules,
Assignments, Syllabus — that organizes the semester and points students to
the existing course websites (`ism2411/`, `ism3232/`), which remain the
source of truth for actual reading/lecture/lab content.

Both course shells already exist in Canvas (empty/unbuilt), and the
instructor has Teacher access. Canvas's Common Cartridge Course Import tool
is available; personal API access tokens are **disabled by the institution's
admin**, so no Canvas REST API automation is possible.

## Non-goals (this pass)

- **No API integration.** Blocked at the institution level — not revisited
  here. (Note: this also means the existing `autograder/grade_*.py` scripts
  can't run against a live token either, but that's a separate, pre-existing
  problem outside this task's scope.)
- **No native Canvas Quizzes.** ISM2411's 14 weekly quizzes and the
  First-Day-Attendance/Syllabus quiz both syllabi require are deferred to a
  follow-up pass (ISM2411 already has a QTI export script, `_build_qti.py`,
  that a future pass can wire into a cartridge or a manual Quiz import).
- **No content duplication.** Reading/lecture/lab bodies are not copied into
  Canvas Pages — Canvas links out to the existing GitHub Pages sites.
- **No live write to Canvas by Claude.** Output is a file the instructor
  reviews and imports themselves.

## Approach: generate one Common Cartridge (.imscc) per course

A new `canvas_builder/` directory (sibling to `autograder/`) holds:

```
canvas_builder/
├── build_cartridge.py        # reads a manifest, emits a valid .imscc
├── ism2411_manifest.yaml     # course structure, one row per module/week
├── ism3232_manifest.yaml
└── README.md                 # how to build + how to import into Canvas
```

`build_cartridge.py` is standalone (no Canvas credentials needed at all) and
produces a standard IMS Common Cartridge 1.3 package: `imsmanifest.xml`
describing an `<organization>` of Modules → Items, plus one small Canvas
Page per module-item (short blurb + outbound link to the matching page on
the course website), one Assignment resource per gradable deliverable, and
the Syllabus body as cartridge-level `course_settings/syllabus.html`, using
Canvas's cartridge extension schema (the same shape Canvas's own "Export
Course Content" produces, which its importer is guaranteed to accept).

The instructor imports each `.imscc` via **Canvas → Settings → Import
Course Content → Content Type: Canvas Course Export Package**, reviews the
Canvas-native "select content" screen, and confirms. Fully reversible —
Canvas retains import history and content can be deleted individually
afterward if something looks wrong.

### Why a cartridge over the alternatives

- **vs. API:** not available — institution disables personal tokens.
- **vs. browser automation:** ~150+ discrete UI actions across two courses
  (add module → add item → set name → set URL, repeated per week/course) is
  slow and fragile to page-layout drift. One cartridge + one import click
  per course is far more reliable at this scale.

## Manifest schema (`*_manifest.yaml`)

```yaml
course_code: ISM2411
site_base_url: https://YOUR-USERNAME.github.io/ism2411   # placeholder, confirm before build
assignment_groups:
  - name: Weekly Labs
    weight: 30
  - name: Weekly Quizzes
    weight: 5
  - name: DataCamp Courses
    weight: 15
  - name: Midterm Exam
    weight: 20
  - name: Capstone Project
    weight: 25
  - name: Lab Participation & Engagement
    weight: 5
modules:
  - number: 1
    title: "Module 1 — What is a Computer?"
    items:
      - {type: page, label: "Reading", site_path: pages/week01_reading.html}
      - {type: page, label: "Lecture", site_path: pages/week01_lecture.html}
      # Module 1 has no lab — pre-course setup only, per syllabus
    assignment: null   # no gradable deliverable this module
  - number: 2
    title: "Module 2 — The Command Line"
    items:
      - {type: page, label: "Reading", site_path: pages/week02_reading.html}
      - {type: page, label: "Lecture", site_path: pages/week02_lecture.html}
      - {type: page, label: "Lab",     site_path: pages/week02_lab.html}
    assignment: {name: "Lab 1", group: "Weekly Labs", points: 10}
  # ... one entry per module, 1-16
front_page:
  title: Home
  site_home_reference: ../ism2411/index.html   # source to summarize from, not pasted verbatim
syllabus_source: ../syllabi/ism2411_simple_syllabus.md
```

`ism3232_manifest.yaml` follows the same shape; its `modules` list uses
`week` instead of `number` alongside a `unit` field (Unit 1–4), since the
site organizes by week-within-unit rather than flat module numbers.

## Course structure to encode

### ISM2411 — 16 modules, Assignment Groups per syllabus grade table

| # | Deliverable | Assignment? |
|---|---|---|
| 1 | Pre-course setup | none (informational module only) |
| 2–8 | Lab 1–7 | Weekly Labs, 10 pts each |
| 9 | Midterm Exam | Midterm Exam group |
| 10–15 | Lab 8–13 | Weekly Labs, 10 pts each |
| 16 | Capstone Project | Capstone Project group |

Plus 10 standalone DataCamp-course assignment stubs, pulled directly from
`ism2411/pages/datacamp.html` (completion-graded, all-or-nothing per
course, linked to the DataCamp page for instructions), and one Lab
Participation & Engagement assignment for the holistic score. Weekly-Quiz
assignments are **not** created this pass (see Non-goals).

**DataCamp Courses group (10%, required)** — one assignment each, due at
the end of the listed week, 0 pts / complete-incomplete:

| # | Due | Course |
|---|---|---|
| 1 | W2 | Introduction to Python |
| 2 | W4 | Intermediate Python |
| 3 | W6 | Python Toolbox |
| 4 | W7 | Writing Functions in Python |
| 5 | W10 | Data Types for Data Science |
| 6 | W11 | Working with Dictionaries |
| 7 | W13 | Introduction to pandas |
| 8 | W14 | Data Manipulation with pandas |

**DataCamp Bonus (extra credit, up to +5%, not in the 100% total)** — two
more assignments, marked `omit_from_final_grade` off but zero-weighted /
bonus points so they only add, never subtract:

| # | Suggested by | Course |
|---|---|---|
| 9 | W15 | Joining Data with pandas |
| 10 | W15 | Introduction to Data Visualization with Matplotlib |

> **Flag for review:** the syllabus grading table says "14 labs total,"
> but the week-by-week schedule table only shows 13 lab deliverables
> (Modules 2–8, 10–15). Built from the schedule table as the more specific
> source — confirm this is correct before import.

### ISM3232 — 16 modules grouped into 4 units, Assignment Groups per syllabus

| Week(s) | Unit | Deliverable | Assignment group |
|---|---|---|---|
| 1–4 | Unit 1 — Developer Foundations | Assignment 1–4 | Weekly Assignments & Quizzes |
| 5–8 | Unit 2 — Python Foundations | Assignment 5–8 | Weekly Assignments & Quizzes |
| 9 | — | Midterm Practical Exam | Midterm Practical Exam |
| 10–12 | Unit 3 — OOP | Assignment 10–12 | Weekly Assignments & Quizzes |
| 13–16 | Unit 4 — Capstone Build | Capstone milestones (schema, DB, Streamlit, demo) | Capstone Project |

Plus one Developer Workflow assignment (holistic, 15%), one Portfolio
assignment (holistic, 5%), and one Lab Participation & Engagement
assignment (5%) — all assessed manually per the syllabus, so these exist as
Canvas Assignments to hold the grade, not as submission-graded items.

### Both courses

- **Front Page** — short welcome, links to Syllabus, Course Map
  (`course_map.html`), Pre-Course Setup, and "this week."
- **Syllabus tool** — built from the `[PUBLIC]`-marked sections of the
  matching `syllabi/*_simple_syllabus.md` file (grading table, schedule,
  policies). `[PRIVATE]` sections (course purpose, AI policy detail) are
  left off the Canvas syllabus page and instead linked to their website page
  (`ai_policy.html`) where one exists.
- **Navigation cleanup** — not settable via Common Cartridge import; each
  course gets a short manual post-import checklist (Settings → Navigation,
  drag unused items to the hidden section: Files, Collaborations,
  Discussions if unused, etc.) rather than automating this narrow step.

## Validation plan

1. `build_cartridge.py` is unit-tested against a small fixture manifest
   (2–3 modules) to confirm the emitted `imsmanifest.xml` is well-formed XML
   and matches the Common Cartridge 1.3 resource/organization schema Canvas
   expects.
2. Full build for both real manifests, then **structural self-check**:
   unzip and confirm module/item/assignment counts match the manifest
   row-for-row (no silently dropped items).
3. Hand off both `.imscc` files to the instructor to import into a real
   Canvas course — Claude does not perform the import.

## Decisions (resolved 2026-08-18)

1. ~~**Site URLs**~~ — resolved: `https://markumreed.github.io/ism2411/` and
   `https://markumreed.github.io/ism3232/`, inferred from the GitHub remote
   (`markumreed/ism_courses`) and each README's own "Option 1" deploy
   instructions. **Not independently confirmed as actually deployed** —
   verify before import; if either site lives at a different URL, only the
   `site_base_url` line in that course's manifest needs to change.
2. ~~**ISM2411 lab count discrepancy**~~ — resolved: build off the 13-lab
   schedule table (Modules 2–8, 10–15); the "14 labs" line in the grading
   table is a pre-existing wording inconsistency in the syllabus source
   itself, not something the Canvas build needs to resolve.
3. ~~**DataCamp assignment list**~~ — resolved: pulled directly from
   `ism2411/pages/datacamp.html` (see the DataCamp Courses group table
   above). `pages/datacamp.html` has no per-course links (DataCamp access
   is via an emailed invite, not direct URLs), so each stub assignment
   links back to the DataCamp Tracker page rather than a course-specific
   URL.
4. ~~**Module 1 check-in**~~ — resolved: stays purely informational this
   pass, no placeholder assignment — consistent with deferring the
   quiz/attendance-check system to the follow-up pass.
