# canvas_builder

Builds a Canvas-importable Common Cartridge (`.imscc`) per course from a
YAML manifest — no Canvas API token required. See the design spec
(`docs/superpowers/specs/2026-08-18-canvas-course-build-design.md`) and
implementation plan
(`docs/superpowers/plans/2026-08-18-canvas-course-build.md`) for the full
rationale.

## Build

```bash
cd canvas_builder
pip install -r requirements.txt
python build_cartridge.py --manifest ism2411_manifest.yaml --out ism2411_fa26.imscc
python build_cartridge.py --manifest ism3232_manifest.yaml --out ism3232_fa26.imscc
```

Each run prints the module/weblink/assignment counts it built and exits
non-zero with a `MISMATCH` message if the cartridge doesn't structurally
match the manifest — **do not import a cartridge that printed MISMATCH.**
On a MISMATCH, the CLI deletes the just-written `.imscc` so a broken
cartridge is never left sitting on disk looking like a valid file.

Resource identifiers in the generated cartridge (modules, weblinks,
assignments, the organization, and the manifest itself) are derived
deterministically from the manifest content (course code, module title,
item label) — building the same manifest twice produces byte-identical
output. This matters for re-import: see "Import into Canvas" below.

## Import into Canvas

**Import into a Canvas sandbox/test course first**, not the live ISM2411 or
ISM3232 course, the first time you do this — this cartridge format
(`imswl_xmlv1p3` weblinks + `assignment_xmlv1p0` CC assignments) is a
documented IMS Common Cartridge standard, not Canvas's own proprietary
export format, so it hasn't been round-tripped through a live Canvas import
during development. Confirm Modules, Assignments, and points land correctly
before importing into the real course.

1. In Canvas: **Settings → Import Course Content**
2. Content Type: **Common Cartridge 1.x Package**
3. Choose the `.imscc` file, select **All content**, click **Import**
4. Wait for the import job to finish (Current Jobs list on the same page)
5. Check **Modules** — every module and item from the manifest should appear
6. Check **Assignments** — every assignment should exist with the right name and points

**Re-importing:** because resource identifiers are deterministic (same
manifest in → same identifiers out, see "Build" above), re-importing the
*same* cartridge into a course that already has it should update the
existing content in place rather than duplicating it. Importing a
*different* cartridge build — e.g. one built after this tool's identifier
scheme changes in a future edit — would create duplicates, since Canvas
matches on identifier and different code means different identifiers. If
anything looks wrong after your first import, delete the imported content
before re-importing rather than assuming a re-import will avoid duplicates.

## Post-import checklist (manual — a few minutes per course)

Common Cartridge import doesn't carry Canvas's Assignment Groups, Syllabus
body, Front Page, Navigation settings, publish state, or submission types
(see "Deviations from the spec" in the implementation plan for why)
— finish these by hand:

1. **Publish** — Common Cartridge imports land **unpublished**: the course,
   every Module, and every Assignment are invisible to students until you
   publish them. Course → Settings, publish the course if it isn't already.
   Then Course → **Modules**, publish each module (the toggle also
   publishes its items). Then Course → **Assignments**, confirm each
   assignment shows the published (green check) state, not draft.
2. **Set submission type** — imported assignments have **no submission
   type set** (the cartridge's `assignment_xml` only carries title, HTML
   description, and points; it doesn't emit `submission_formats`), so as
   imported, students cannot submit anything. For each assignment: Edit →
   **Submission Type**.
   - **ISM3232**: the front page tells students "every assignment is
     submitted as a GitHub URL" → use **Online → Website URL** for the
     weekly assignments and Capstone milestones.
   - **ISM2411**: the front page says to "submit that week's Lab
     assignment here in Canvas" → use **Online → File Upload** (and/or
     Text Entry, instructor's choice) for the weekly labs.
   - Don't blanket-apply one submission type to every assignment in a
     course — Capstone/Midterm/DataCamp/Participation assignments may need
     something different (e.g. DataCamp and Participation are likely
     **No Submission** / instructor-graded-only, not a student upload).
     Set each assignment's type to match how it's actually meant to be
     turned in.
3. **Assignment Groups** — Settings → Assignments → **+ Group**, create one
   group per distinct `group:` value in the manifest, drag each imported
   assignment into its matching group, set each group's weight from the
   table below, then enable **weighted grading** in the Assignments page
   settings.

   **ISM2411** (DataCamp is 10%, not 15% — see "Known gaps" below for why):

   | Group | Weight | Assignments |
   |---|---|---|
   | Weekly Labs | 30% | 13 |
   | Midterm Exam | 20% | 1 |
   | Capstone Project | 25% | 1 |
   | DataCamp Courses | 10% | 10 (8 required + 2 bonus — mark the 2 bonus ones "do not count towards final grade", step 8 below) |
   | Lab Participation & Engagement | 5% | 1 |

   **ISM3232**:

   | Group | Weight | Assignments |
   |---|---|---|
   | Developer Workflow | 15% | 1 |
   | Weekly Assignments & Quizzes | 25% | 11 |
   | Midterm Practical Exam | 20% | 1 |
   | Capstone Project | 30% | 4 |
   | Portfolio | 5% | 1 |
   | Lab Participation & Engagement | 5% | 1 |

   **ISM3232 only** — the syllabus (`syllabi/ism3232_simple_syllabus.md:142`)
   specifies "lowest grade dropped" for Weekly Assignments & Quizzes. That's
   a Canvas assignment-group rule the cartridge can't set: on that group,
   Edit group → **"Drop the lowest N scores"** → set to 1.
4. **Syllabus** — Course → Syllabus → **Edit**, switch to the HTML source
   view (`</>` icon), paste the contents of `ism2411_syllabus.html` (or
   `ism3232_syllabus.html`), save.
5. **Front Page** — Course → Pages → **+ Page**, name it "Home", switch to
   HTML source view, paste the contents of `ism2411_front_page.html` (or
   `ism3232_front_page.html`), save, then Pages → **⋮ → Use as Front Page**.
   Finally, Course → Settings → **Choose Home Page → Front Page**.
6. **Navigation cleanup** — Course → Settings → **Navigation** tab, drag
   unused items (Files, Collaborations, Discussions if unused, etc.) down
   into the hidden section, save.
7. **Verify weblink URLs resolve** — spot-check a few Module items actually
   open the right page on the live site (confirms `site_base_url` in the
   manifest matches where the site is really deployed).
8. **ISM2411 only — DataCamp bonus assignments** — on the two "DataCamp
   Bonus" assignments, open Edit → check **"Do not count this assignment
   towards the final grade"**, so they add up to +5% without diluting the
   required DataCamp component's denominator.
9. **Set due dates** — imported assignments have **no due dates**: this
   cartridge's assignment resources don't carry due-date data. Set each
   one Canvas-side to match the course's schedule (ISM2411: Sunday
   11:59 PM each week; ISM3232: per the syllabus's weekly schedule).

## Import Quizzes (QTI)

Weekly self-check quizzes for both courses are built separately from the
cartridge, by `_build_qti.py` (repo root) — one Canvas-native QTI 1.2 `.zip`
per week, plus a combined midterm-coverage `.zip` per course. Unlike the
Common Cartridge above, Canvas has no bulk-import path for a set of QTI
files — each `.zip` is imported as its own quiz.

```bash
python _build_qti.py
```

Writes to `quiz_exam_fa26/` (gitignored): 14 ISM2411 weekly quizzes + 1
midterm, 15 ISM3232 weekly quizzes + 1 midterm. The script fails loudly
(raises, doesn't write partial output) if it can't confidently determine a
question's correct answer from the page HTML — don't silently patch around
that if it ever fires again; fix the source reading page's answer text
instead (see the git history on `ism2411`/`ism3232` for the pattern used
to resolve this the first time).

Per quiz, per course:

1. Canvas → **Quizzes → + Quiz**, name it (e.g. "Module 2 Quiz")
2. **Settings → Import Course Content → Content Type: QTI .zip file**,
   choose that week's `.zip`, **Import**
3. Open the quiz, confirm the question count and points match what the
   build printed for that file
4. **Publish** the quiz — QTI imports land unpublished, same as the
   cartridge's modules/assignments
5. **Set a due date** — not carried by QTI either
6. **Link it into the matching Module** — the cartridge import (above)
   already created that week's Module with Reading/Lecture/Lab items;
   open that Module → **+ Add Item → Quiz** → select the quiz you just
   imported → **Add Item**, so it appears alongside that week's other
   content instead of living only under the standalone Quizzes tab

Spot-check ISM2411's Module 5 quiz specifically — "Which values are falsy
in Python? (Select all that apply)" is a genuine multi-answer question
(all 4 options are correct); confirm Canvas renders it as checkboxes, not
radio buttons.

## Known gaps (deferred, see spec's Non-goals)

- Neither course's First-Day-Attendance/Syllabus quiz is built — only the
  weekly content quizzes above. A future pass can add these.
- `ism2411_syllabus.html`'s grading table doesn't yet reflect Weekly
  Quizzes as a line item now that quizzes exist — its visible rows still
  sum to 90%, not 100% (see the DataCamp 10%-vs-15% note in the git history
  of this file). Reconciling the syllabus page's grading table with the
  now-built quizzes is a small follow-up, not done as part of this pass.
- DataCamp assignments are manually marked complete/incomplete — DataCamp
  itself has no Canvas integration in this build.
- `syllabi/ism2411_simple_syllabus.md` says "14 labs total," but the actual
  Canvas build has **13** lab assignments (Module 1 is pre-course
  setup/orientation, not a graded lab). This is a pre-existing
  inconsistency in the syllabus source itself, already resolved in the
  design spec in favor of 13 — not a bug in this tool — but worth knowing
  so you're not surprised when the count in Canvas doesn't match the
  syllabus text.
