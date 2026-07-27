# Autograder for ISM2411 and ISM3232 — Design

## Problem

Grading weekly labs/assignments and capstone milestones for two courses is
currently manual: export submissions from Canvas by hand, read code, score
against a rubric, upload grades back into Canvas one at a time (or via the
existing `ism3232-grader` skill, which does GitHub fetch + Claude-driven
rubric scoring + CSV output, but doesn't post to Canvas and depends on an LLM
judgment call for every submission).

We want two standalone local Python programs — one per course — that pull
submissions from Canvas directly, run fully deterministic (no-LLM) checks
against each course's actual rubric, and post grades back to Canvas via its
API. Where the rubric genuinely calls for human judgment (code quality,
correctness of open-ended logic, capstone rubric levels), the program
surfaces exactly what a grader needs to make that call quickly, rather than
guessing or delegating it to an LLM.

## Scope

**In scope**, for both courses:
- Weekly labs (ISM2411) / weekly assignments (ISM3232) — the GitHub-URL or
  file-upload coding deliverables.
- Capstone project (both courses, including ISM3232's 4 milestone weeks).
- ISM3232's Developer Workflow grade (15%) — fully mechanical (ruff, pytest,
  git log), scored automatically with no human input.

**Out of scope** (not autogradable, or already handled elsewhere):
- Midterm exams — both courses run these in-class, no-laptop, pen-and-paper
  (see `ism2411/pages/week09_midterm.html`). Nothing to run or fetch. Grade
  entry for the midterm stays exactly as it is today (manual, direct in
  Canvas) — this project does not touch it.
- Quizzes — already auto-graded by Canvas itself.
- DataCamp completion (ISM2411) — tracked by DataCamp, not Canvas submissions.
- Lab Participation & Engagement, Portfolio (both courses) — explicitly
  holistic instructor judgment per the syllabi, not tied to a gradable
  artifact.

## Architecture

```
autograder_common/           # shared library, no course-specific logic
  canvas.py                  #   Canvas API client: list submissions, download,
                              #   fetch current grade, post grade+comment
  fetch.py                   #   resolve a submission (file download or GitHub
                              #   URL clone) into runs/<assignment>/<student>/
  checks.py                  #   mechanical check primitives: file exists,
                              #   run-without-error, ruff, pytest, git log shape
  worksheet.py                #   build/read the review-worksheet CSV
  scoring.py                  #   apply a rubric-weight config to worksheet
                              #   rows to compute a final numeric grade
  cli.py                      #   shared argparse scaffolding (fetch/check/upload)

grade_ism2411.py              # thin CLI: loads ism2411.config.yaml + assignment
                              # configs, wires them into autograder_common.cli
grade_ism3232.py              # same, for ism3232.config.yaml

ism2411.config.yaml           # Canvas base URL, course ID (gitignored: no
ism3232.config.yaml           # secrets in the file itself — token via env var)

assignments/
  ism2411/
    week03_lab.yaml           # per-assignment: files, run command, checks,
    capstone.yaml             # rubric weights
  ism3232/
    week07_assignment.yaml
    developer_workflow.yaml   # applies to every submission, not one assignment
    capstone_milestone_13.yaml
    ...
```

Both programs share 100% of the Canvas/check/scoring engine. "Two distinct
programs" is real at the level a user interacts with (`grade_ism2411.py` vs
`grade_ism3232.py`, separate configs, separate rubrics) — nothing about one
course's grading logic can leak into the other's run.

## Per-assignment config format

One YAML file per assignment, e.g. `assignments/ism2411/week03_lab.yaml`:

```yaml
course: ism2411
key: week03_lab
canvas_assignment_id: null       # filled in during setup, per real course
submission_type: canvas_upload   # canvas_upload | github_url
expected_files: ["pricer.py"]
run:
  command: "python3 {file}"
  timeout_seconds: 10
mechanical_checks:
  - file_present
  - runs_without_error
  - submitted_on_time
rubric:
  # points-based, human-scored fields marked explicitly
  submission: {points: 1, source: mechanical}
  correctness: {points: 4, source: human, prompt: "Compare captured output to the lab's stated expected output"}
  completion: {points: 3, source: human, prompt: "All exercises 1-4 attempted?"}
  code_quality: {points: 2, source: human, prompt: "Meaningful names, no unneeded repetition, readable"}
```

For ISM3232's Developer Workflow (`assignments/ism3232/developer_workflow.yaml`),
every field is `source: mechanical` — ruff exit code, pytest exit code, and two
git-log heuristics (commit message quality: flag generic messages like "fix"/
"final"/"asdf"; commit spread: more than one commit, not all within the same
hour) — 3 points each, summing to 15.

Capstone configs (`capstone.yaml` per course, `capstone_milestone_1[3-6].yaml`
for ISM3232) use a `levels` block instead of `points` per dimension, mapping
Excellent/Good/Developing/Incomplete to 4/3/2/1, matching
`capstone_rubric.html`'s actual structure; mechanical checks feed a couple of
the dimension prompts (e.g. "runs top-to-bottom without errors" under Code
Clarity) but the level pick itself is always `source: human`.

## Workflow

```bash
python grade_ism2411.py fetch   --assignment week03_lab
python grade_ism2411.py check   --assignment week03_lab
# -> runs/week03_lab/review.csv: one row per student, mechanical columns
#    auto-filled + captured stdout, human columns blank
# ... instructor fills in the human columns, saves the CSV ...
python grade_ism2411.py upload  --assignment week03_lab --dry-run
# -> prints "Jane Doe: current 8/10 -> new 9/10" per student, posts nothing
python grade_ism2411.py upload  --assignment week03_lab
# -> interactive y/n confirmation showing student count + assignment name,
#    then posts score + comment via Canvas API, writes
#    runs/week03_lab/upload_log_<timestamp>.json as a local audit trail
```

`fetch` for `submission_type: canvas_upload` downloads the file directly via
the Canvas API; for `github_url` it resolves the submitted URL (adapting the
existing `ism3232-grader` skill's clone/resolve logic) into
`runs/<assignment>/<student>/`.

## Canvas API integration

- `ism2411.config.yaml` / `ism3232.config.yaml` hold `canvas_base_url` and
  `canvas_course_id` only. The API token is read from `CANVAS_API_TOKEN` in
  the environment — never written to a config file or committed.
- Setup prerequisite (not yet confirmed available): a Canvas personal access
  token (Account → Settings → New Access Token) and the numeric course ID for
  each course (visible in the course's Canvas URL). Assignment IDs are
  resolved by name via the API at `fetch` time — not hardcoded — falling back
  to a `canvas_assignment_id` override in the assignment YAML if name lookup
  is ambiguous.
- Grade upload always shows current-grade-before / new-grade-after per
  student and requires interactive confirmation, since posting to the live
  gradebook is hard to reverse. `--dry-run` never calls the write endpoint.

## Error handling

- A submission that fails to fetch (private repo, broken link, no submission)
  is recorded as `status: fetch-failed` in the worksheet with the reason, and
  is skipped (not zeroed) on `upload` — the instructor handles it manually,
  same failure modes the existing `ism3232-grader` skill already surfaces
  (`no-github-url`, `clone-failed`, `no-code-file-found`).
- A submission whose code times out or crashes still gets a worksheet row —
  `runs_without_error: false` plus captured stderr — so mechanical points for
  that check are 0 but the row is still gradable for the human-scored fields.
- `upload` refuses to run if the worksheet has any row with an incomplete
  human-scored field (blank where the rubric expects a value), listing which
  students are incomplete, to avoid silently posting a partial score.

## Testing

- `autograder_common` (checks, scoring, worksheet round-trip) gets unit tests
  against fixture repos/worksheets — no real Canvas calls.
- Canvas API client gets unit tests against a mocked HTTP layer.
- End-to-end validation happens by the instructor running `fetch`/`check` with
  `--dry-run` against one real, low-stakes assignment before trusting `upload`
  on anything that counts.

## Initial delivery scope

Build the full `autograder_common` engine and both CLI programs now. Author
YAML configs for a pilot set only:
- One ISM2411 lab (`week03_lab` — has clear per-exercise expected output,
  file-upload submission).
- One ISM3232 weekly assignment (`week07_assignment` — has clear file
  deliverables, GitHub-URL submission).
- `developer_workflow.yaml` (ISM3232).
- Both courses' capstone configs.

Remaining lab/assignment configs are templated out afterward, once the
pattern is proven end-to-end against real Canvas data — this is a mechanical
follow-up, not a design question.
