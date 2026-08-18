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

## Post-import checklist (manual — a few minutes per course)

Common Cartridge import doesn't carry Canvas's Assignment Groups, Syllabus
body, Front Page, or Navigation settings (see "Deviations from the spec" in
the implementation plan for why) — finish these by hand:

1. **Assignment Groups** — Settings → Assignments → **+ Group**, create one
   group per distinct `group:` value in the manifest (e.g. "Weekly Labs",
   "Midterm Exam", "Capstone Project" for ISM2411), then drag each imported
   assignment into its matching group. Set each group's weight from the
   syllabus grading table, then enable **weighted grading** in the
   Assignments page settings.
2. **Syllabus** — Course → Syllabus → **Edit**, switch to the HTML source
   view (`</>` icon), paste the contents of `ism2411_syllabus.html` (or
   `ism3232_syllabus.html`), save.
3. **Front Page** — Course → Pages → **+ Page**, name it "Home", switch to
   HTML source view, paste the contents of `ism2411_front_page.html` (or
   `ism3232_front_page.html`), save, then Pages → **⋮ → Use as Front Page**.
   Finally, Course → Settings → **Choose Home Page → Front Page**.
4. **Navigation cleanup** — Course → Settings → **Navigation** tab, drag
   unused items (Files, Collaborations, Discussions if unused, etc.) down
   into the hidden section, save.
5. **Verify weblink URLs resolve** — spot-check a few Module items actually
   open the right page on the live site (confirms `site_base_url` in the
   manifest matches where the site is really deployed).
6. **ISM2411 only — DataCamp bonus assignments** — on the two "DataCamp
   Bonus" assignments, open Edit → check **"Do not count this assignment
   towards the final grade"**, so they add up to +5% without diluting the
   required DataCamp component's denominator.

## Known gaps (deferred, see spec's Non-goals)

- No native Canvas Quizzes (ISM2411's 14 weekly quizzes, or either course's
  First-Day-Attendance/Syllabus quiz). ISM2411 already has a QTI export
  script (`_build_qti.py`, repo root) a future pass can wire in.
- DataCamp assignments are manually marked complete/incomplete — DataCamp
  itself has no Canvas integration in this build.
