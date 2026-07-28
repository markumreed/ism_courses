# ISM2411 / ISM3232 Autograder

Two local CLI programs that fetch student submissions from Canvas, run
deterministic checks against each course's rubric, and post grades back to
Canvas. No LLM/AI is used anywhere in the grading path — criteria the rubric
can't check mechanically are left blank in a review worksheet for you to
fill in by hand.

Design doc: `docs/superpowers/specs/2026-07-27-autograder-design.md`.

## Setup

1. **Install dependencies:**
   ```bash
   cd autograder
   pip install -r requirements.txt
   ```

2. **Get a Canvas API token:** in Canvas, go to Account -> Settings ->
   scroll to "Approved Integrations" -> "+ New Access Token". Copy the token
   immediately (Canvas only shows it once).

3. **Export the token as an environment variable** (never put it in a config
   file or commit it):
   ```bash
   export CANVAS_API_TOKEN="paste-your-token-here"
   ```

4. **Find your course ID:** open the course in Canvas; the URL looks like
   `https://YOUR_INSTITUTION.instructure.com/courses/12345` — `12345` is the
   course ID.

5. **Fill in `ism2411.config.yaml` and `ism3232.config.yaml`** with your real
   `canvas_base_url` and `canvas_course_id`.

## Usage

Per assignment, per course:

```bash
python grade_ism2411.py fetch   --assignment week03_lab
python grade_ism2411.py check   --assignment week03_lab
# Opens runs/week03_lab/review.csv in a spreadsheet app - fill in the blank
# human_* columns (each has a "prompt" in the assignment's YAML config
# telling you what to judge), save.
python grade_ism2411.py upload  --assignment week03_lab --dry-run
# Review the current -> new grade for every student, confirm nothing looks wrong.
python grade_ism2411.py upload  --assignment week03_lab
# Type 'y' to confirm. Posts grades + comments to Canvas, writes a local
# audit log to runs/week03_lab/upload_log_<timestamp>.json.
```

Same for `grade_ism3232.py`, using assignment keys from
`assignments/ism3232/`.

## Adding a new assignment

Copy an existing YAML file in `assignments/ism2411/` or
`assignments/ism3232/` as a template — the field names are the same across
every assignment (`submission_type`, `expected_files`, `run`,
`mechanical_checks`, `scoring_type`, `rubric`). See
`docs/superpowers/specs/2026-07-27-autograder-design.md` for the full config
schema and what each `mechanical_checks` value does.

Currently configured (pilot set):
- ISM2411: `week03_lab`, `capstone`
- ISM3232: `week07_assignment`, `developer_workflow`, `capstone`

The remaining labs/weekly assignments for both courses follow the same
template and can be added the same way.

## Running the test suite

```bash
cd autograder
pytest -v
```

No test hits the real Canvas API — everything is mocked. Before trusting
`upload` against a real assignment, run `fetch` and `check` (with
`upload --dry-run`) against one real, low-stakes assignment first.
