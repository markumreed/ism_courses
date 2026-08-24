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

**ISM2411's structure:** `Module 0 — Course Info` comes first and holds
the Syllabus/Grading link, the DataCamp Tracker link (once — not
repeated per DataCamp course), and the Lab Participation & Engagement
assignment. `Module 1` keeps the Pre-Course Setup Walkthrough alongside
its Reading/Lecture. Every other module holds its own Lab assignment
plus, where the syllabus schedules one, that week's DataCamp course as a
second assignment in the same module — there are no separate
"DataCamp N" modules. Weekly Labs, the Midterm, the Capstone, and every
DataCamp assignment carry a `due_at` (11:59 PM Eastern, converted to UTC
— correctly split across the Nov 1 2026 DST boundary); Lab Participation
& Engagement doesn't, since the syllabus assesses it twice (midterm and
end of semester), not on one date.

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
7. **ISM2411 only** — open a couple of assignments (e.g. Lab 2) and check
   whether a due date landed automatically. This uses an `<extensions>`
   block inside the same standard assignment file — the same mechanism
   Canvas's own exporter uses (verified against Canvas's own importer
   source, `lib/cc/importer/standard/assignment_converter.rb`), but it's
   untested against a real import in this project. If dates don't show
   up, nothing else is affected — fall back to setting them by hand
   (step 9 below), same as every other assignment always required.

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

   **ISM2411:**

   | Group | Weight | Assignments |
   |---|---|---|
   | Weekly Labs | 30% | 13 |
   | Weekly Quizzes | 5% | 14 (imported separately as native Canvas Quizzes — see "Import Quizzes" below; Canvas auto-adds a shadow Assignment per quiz, drag those into this group) |
   | DataCamp Courses | 15% | 7 (5 required + 2 bonus — see step 8 below for how the 2 bonus ones work) |
   | Midterm Exam | 20% | 1 |
   | Capstone Project | 25% | 1 |
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
   **ISM3232 only:** before saving, replace the `href="#"` on "First Day
   Attendance Quiz" with that quiz's real URL — copy it from the quiz you
   imported in the "Import Quizzes" section below (it doesn't exist until
   then, which is why it's a placeholder here).
6. **Navigation cleanup** — Course → Settings → **Navigation** tab, drag
   unused items (Files, Collaborations, Discussions if unused, etc.) down
   into the hidden section, save.
7. **Verify weblink URLs resolve** — spot-check a few Module items actually
   open the right page on the live site (confirms `site_base_url` in the
   manifest matches where the site is really deployed).
8. **ISM2411 only — DataCamp bonus assignments** — the syllabus specifies
   the 5 required DataCamp courses earn the full 15% group weight, and the
   2 bonus courses can add up to +5% more, capped so the DataCamp component
   never exceeds 20% of the final grade. Canvas has no single checkbox for
   "capped bonus" — the standard way to get this behavior is to set the 2
   bonus assignments' **points possible to 0** while leaving them counted
   normally in the group (not "omit from final grade"): a 0-point assignment
   doesn't add to the group's points-possible denominator, but any points a
   student earns on it still add to the numerator, which is exactly a
   capped-when-not-completed, uncapped-within-reason-when-completed bonus.
   Verify this behaves as expected in your Canvas instance before relying
   on it — if it doesn't, "do not count this assignment towards the final
   grade" is the safe fallback (bonus students get nothing, but nothing
   breaks for anyone else).
9. **Set due dates** —
   **ISM2411**: Weekly Labs, DataCamp courses, the Midterm, and the
   Capstone carry a `due_at` in the cartridge itself (see step 7 above) —
   verify it actually landed rather than assuming it did, and set it by
   hand for any assignment where it didn't. Lab Participation & Engagement
   has no single due date by design (see "ISM2411's structure" above).
   **ISM3232**: no assignment carries a due date in the cartridge — set
   every one by hand, per the syllabus's weekly schedule.
   **Both courses**: Quizzes never carry a due date regardless of course —
   see "Import Quizzes" below for why — set those by hand too.

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
5. **Set a due date** — not carried by QTI either. Investigated this: Canvas's
   quiz importer *can* read a due date, but only from a separate
   `assessment_meta.xml` companion file inside a differently-typed resource
   (`lib/cc/importer/canvas/quiz_metadata_converter.rb`), not from anything
   inside the standard QTI file this project generates. Retrofitting that
   would mean changing the quiz resource's type in `imsmanifest.xml` —
   real risk to an import that's already known to work, for a feature this
   codebase hasn't verified end-to-end. Not attempted; set quiz due dates
   by hand.
6. **Link it into the matching Module** — the cartridge import (above)
   already created that week's Module with Reading/Lecture/Lab items;
   open that Module → **+ Add Item → Quiz** → select the quiz you just
   imported → **Add Item**, so it appears alongside that week's other
   content instead of living only under the standalone Quizzes tab

Spot-check ISM2411's Module 5 quiz specifically — "Which values are falsy
in Python? (Select all that apply)" is a genuine multi-answer question
(all 4 options are correct); confirm Canvas renders it as checkboxes, not
radio buttons.

### First Day Attendance / Syllabus Quiz

Both syllabi require a short quiz confirming the student read the syllabus
and is actively enrolled — USF policy allows dropping students who don't
complete it by the deadline. Built by `_build_syllabus_quiz.py` (repo
root), hand-authored from each syllabus's actual policies (not extracted
from a reading page, since there's no reading page for this):

```bash
python _build_syllabus_quiz.py
```

Writes `ism2411_syllabus_quiz.zip` ("Module 1 Syllabus Quiz," 6 questions)
and `ism3232_syllabus_quiz.zip` ("First Day Attendance Quiz," 6 questions)
to `quiz_exam_fa26/`. Import each the same way as a weekly quiz (steps
1–5 above), but **do not** link it into a Module — this quiz stands alone
under the Quizzes tab as a course-entry gate, not weekly content. Point
it into the syllabus itself: add a line to the Front Page or Syllabus
page linking to it, since students need to find it without a Module to
guide them there.

## Known gaps (deferred, see spec's Non-goals)

- DataCamp assignments are manually marked complete/incomplete — DataCamp
  itself has no Canvas integration in this build.
- `syllabi/ism2411_simple_syllabus.md` says "14 labs total," but the actual
  Canvas build has **13** lab assignments (Module 1 is pre-course
  setup/orientation, not a graded lab). This is a pre-existing
  inconsistency in the syllabus source itself, already resolved in the
  design spec in favor of 13 — not a bug in this tool — but worth knowing
  so you're not surprised when the count in Canvas doesn't match the
  syllabus text.
