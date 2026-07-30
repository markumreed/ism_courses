"""Local Streamlit GUI for the ISM2411/ISM3232 autograder.

Run with: streamlit run gui.py

Thin presentation layer over autograder_common — every grading decision
(what to fetch, what a check means, how a rubric scores) is delegated to
the same functions the fetch/check/upload CLI (grade_ism2411.py /
grade_ism3232.py) already uses. This file only renders state and wires
button clicks to those functions.
"""
from pathlib import Path

import streamlit as st

from autograder_common import gui_helpers, worksheet
from autograder_common.canvas import CanvasClient, CanvasError
from autograder_common.config import ConfigError, load_course_config
from autograder_common.fetch import FetchError, fetch_submission

ROOT = Path(__file__).resolve().parent
RUNS_DIR = ROOT / "runs"

COURSES = {
    "ISM2411": {
        "config_path": ROOT / "ism2411.config.yaml",
        "assignments_dir": ROOT / "assignments" / "ism2411",
    },
    "ISM3232": {
        "config_path": ROOT / "ism3232.config.yaml",
        "assignments_dir": ROOT / "assignments" / "ism3232",
    },
}

st.set_page_config(page_title="Autograder", layout="wide")
st.title("Autograder")

# ---------------------------------------------------------------------------
# Header controls
# ---------------------------------------------------------------------------
course_name = st.selectbox("Course", list(COURSES.keys()))
course = COURSES[course_name]

try:
    assignments = gui_helpers.discover_assignments(course["assignments_dir"])
except ConfigError as e:
    st.error(f"Could not load assignment configs: {e}")
    st.stop()

if not assignments:
    st.warning(f"No assignment configs found in {course['assignments_dir']}")
    st.stop()

assignment_keys = [a["key"] for a in assignments]
assignment_key = st.selectbox("Assignment", assignment_keys)
assignment_config = next(a for a in assignments if a["key"] == assignment_key)

state_key = f"{course_name}:{assignment_key}"
if st.session_state.get("_current_state_key") != state_key:
    st.session_state["_current_state_key"] = state_key
    st.session_state["edited_rows"] = None
    st.session_state["upload_previewed"] = False
st.session_state.setdefault("check_gen", 0)

worksheet_path = RUNS_DIR / assignment_key / "review.csv"


def get_client():
    course_config = load_course_config(course["config_path"])
    return CanvasClient(
        course_config["canvas_base_url"],
        course_config["canvas_course_id"],
        course_config["canvas_token"],
    )


def get_assignment_id(client):
    override = assignment_config.get("canvas_assignment_id")
    if override:
        return override
    return client.find_assignment_id(assignment_config["canvas_display_name"])


# ---------------------------------------------------------------------------
# Action bar: Fetch / Check
# ---------------------------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    if st.button("Fetch Submissions"):
        try:
            client = get_client()
            assignment_id = get_assignment_id(client)
            submissions = client.list_submissions(assignment_id)
        except (ConfigError, CanvasError) as e:
            st.error(f"Fetch failed: {e}")
        else:
            out_dir = RUNS_DIR / assignment_key
            out_dir.mkdir(parents=True, exist_ok=True)
            count = 0
            log_lines = []
            for sub in submissions:
                user = sub.get("user") or {}
                name = user.get("name", f"user-{sub.get('user_id')}")
                dest = out_dir / gui_helpers.student_key(name)
                try:
                    fetch_submission(sub, assignment_config, client, dest)
                    count += 1
                except FetchError as e:
                    log_lines.append(f"{name}: fetch failed - {e}")
            st.success(f"Fetched {count}/{len(submissions)} submissions to {out_dir}")
            for line in log_lines:
                st.write(f"⚠️ {line}")

with col2:
    if st.button("Run Checks"):
        try:
            client = get_client()
            assignment_id = get_assignment_id(client)
            submissions = client.list_submissions(assignment_id)
        except (ConfigError, CanvasError) as e:
            st.error(f"Check failed: {e}")
        else:
            out_dir = RUNS_DIR / assignment_key
            students = []
            for sub in submissions:
                user = sub.get("user") or {}
                name = user.get("name", f"user-{sub.get('user_id')}")
                key = gui_helpers.student_key(name)
                student_dir = out_dir / key
                if not student_dir.exists():
                    students.append({
                        "student_key": key, "student_name": name,
                        "status": "fetch-failed", "captured_output": "",
                    })
                    continue
                students.append(
                    gui_helpers.compute_student_record(student_dir, key, name, assignment_config)
                )
            worksheet.build_worksheet(worksheet_path, students, assignment_config)
            st.session_state["edited_rows"] = None
            st.session_state["upload_previewed"] = False
            st.session_state["check_gen"] += 1
            st.success(f"Wrote {worksheet_path}")

# ---------------------------------------------------------------------------
# Grading table
# ---------------------------------------------------------------------------
if not worksheet_path.exists():
    st.info("Run Check to build the review worksheet before grading.")
    st.stop()

if st.session_state["edited_rows"] is None:
    st.session_state["edited_rows"] = worksheet.read_worksheet(worksheet_path)

rows = st.session_state["edited_rows"]
human_fields = worksheet.human_fields(assignment_config)
mechanical_fields = worksheet.mechanical_fields(assignment_config)
scoring_type = assignment_config.get("scoring_type", "points")

st.header("Grading")

for row in rows:
    with st.expander(f"{row['student_name']} — status: {row['status']}"):
        if row["status"] != "ok":
            st.write("No submission to grade (fetch failed or not yet fetched).")
            continue

        st.text(row.get("captured_output", "") or "(no captured output)")

        for field in mechanical_fields:
            col_name = f"{worksheet.MECHANICAL_COLUMN_PREFIX}{field}"
            st.write(f"**{field}** (mechanical): {row.get(col_name)}")

        for field in human_fields:
            col_name = f"{worksheet.HUMAN_COLUMN_PREFIX}{field}"
            spec = assignment_config["rubric"][field]
            prompt = spec.get("prompt", field)
            widget_key = f"{state_key}:{st.session_state['check_gen']}:{row['student_key']}:{field}"
            if scoring_type == "capstone_levels":
                options = ["", "excellent", "good", "developing", "incomplete"]
                current = row.get(col_name, "")
                index = options.index(current) if current in options else 0
                value = st.selectbox(prompt, options, index=index, key=widget_key)
                row[col_name] = str(value)
            else:
                points = spec.get("points", 0)
                current = row.get(col_name, "")
                current_val = float(current) if current.strip() else None
                value = st.number_input(
                    prompt, min_value=0.0, max_value=float(points),
                    value=current_val if current_val is not None else 0.0,
                    key=f"{widget_key}:value",
                )
                graded = st.checkbox(
                    "Graded", value=current_val is not None, key=f"{widget_key}:graded"
                )
                row[col_name] = str(value) if graded else ""

        row["comment"] = st.text_area(
            "Comment", value=row.get("comment", ""),
            key=f"{state_key}:{st.session_state['check_gen']}:{row['student_key']}:comment"
        )

        score = gui_helpers.live_score(row, assignment_config)
        st.write(f"**Live score:** {score if score is not None else '—'}")

if st.button("Save Worksheet"):
    students_for_write = []
    for row in rows:
        record = {
            "student_key": row["student_key"],
            "student_name": row["student_name"],
            "status": row["status"],
            "captured_output": row.get("captured_output", ""),
        }
        for field in mechanical_fields:
            col_name = f"{worksheet.MECHANICAL_COLUMN_PREFIX}{field}"
            record[field] = row.get(col_name, "").strip().lower() in ("true", "1", "yes")
        students_for_write.append(record)
    worksheet.build_worksheet(worksheet_path, students_for_write, assignment_config)
    # build_worksheet always writes human columns blank — overwrite them
    # with the in-memory edits, then re-read/re-save to merge.
    saved_rows = worksheet.read_worksheet(worksheet_path)
    for saved_row, edited_row in zip(saved_rows, rows):
        for field in human_fields:
            col_name = f"{worksheet.HUMAN_COLUMN_PREFIX}{field}"
            saved_row[col_name] = edited_row.get(col_name, "")
        saved_row["comment"] = edited_row.get("comment", "")
    import csv
    with worksheet_path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(saved_rows[0].keys()) if saved_rows else [])
        writer.writeheader()
        writer.writerows(saved_rows)
    st.session_state["upload_previewed"] = False
    st.success(f"Saved {worksheet_path}")

# ---------------------------------------------------------------------------
# Upload panel
# ---------------------------------------------------------------------------
st.header("Upload")

if st.button("Preview Upload"):
    saved_rows = worksheet.read_worksheet(worksheet_path)
    incomplete = worksheet.incomplete_students(saved_rows, assignment_config)
    if incomplete:
        st.error(f"Cannot preview - incomplete human-scored fields for: {', '.join(incomplete)}")
        st.session_state["upload_previewed"] = False
    else:
        try:
            client = get_client()
            assignment_id = get_assignment_id(client)
            submissions = client.list_submissions(assignment_id)
        except (ConfigError, CanvasError) as e:
            st.error(f"Preview failed: {e}")
        else:
            key_to_user_id = {
                gui_helpers.student_key((s.get("user") or {}).get("name", f"user-{s['user_id']}")): s["user_id"]
                for s in submissions
            }
            current_grades = {}
            try:
                for row in saved_rows:
                    if row.get("status") != "ok":
                        continue
                    user_id = key_to_user_id.get(row["student_key"])
                    if user_id is not None:
                        current_grades[row["student_key"]] = client.get_current_grade(assignment_id, user_id)
            except CanvasError as e:
                st.error(f"Preview failed: {e}")
            else:
                plan = gui_helpers.build_upload_plan(saved_rows, assignment_config, current_grades)
                st.session_state["upload_plan"] = plan
                st.session_state["upload_previewed"] = True
                for item in plan:
                    current_str = "ungraded" if item["current_grade"] is None else item["current_grade"]
                    st.write(f"{item['student_name']}: {current_str} → {item['new_grade']}")

confirm_text = st.text_input(f"Type '{assignment_key}' to confirm posting grades")
post_disabled = not (st.session_state.get("upload_previewed") and confirm_text == assignment_key)

if st.button("Post Grades to Canvas", disabled=post_disabled):
    saved_rows = worksheet.read_worksheet(worksheet_path)
    incomplete = worksheet.incomplete_students(saved_rows, assignment_config)
    if incomplete:
        st.error(f"Cannot post - incomplete human-scored fields for: {', '.join(incomplete)}")
    else:
        try:
            client = get_client()
            assignment_id = get_assignment_id(client)
            submissions = client.list_submissions(assignment_id)
        except (ConfigError, CanvasError) as e:
            st.error(f"Upload failed: {e}")
        else:
            key_to_user_id = {
                gui_helpers.student_key((s.get("user") or {}).get("name", f"user-{s['user_id']}")): s["user_id"]
                for s in submissions
            }
            import json
            from datetime import datetime, timezone

            log = []
            error_message = None
            for row in saved_rows:
                if row.get("status") != "ok":
                    continue
                user_id = key_to_user_id.get(row["student_key"])
                if user_id is None:
                    continue
                score = gui_helpers.live_score(row, assignment_config)
                try:
                    current = client.get_current_grade(assignment_id, user_id)
                    client.post_grade(assignment_id, user_id, score, row.get("comment") or None)
                except CanvasError as e:
                    error_message = str(e)
                    break
                log.append({"user_id": user_id, "name": row["student_name"], "previous": current, "posted": score})

            runs_dir_path = RUNS_DIR / assignment_key
            runs_dir_path.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            log_path = runs_dir_path / f"upload_log_{timestamp}.json"
            log_path.write_text(json.dumps(log, indent=2))

            if error_message:
                st.error(
                    f"Upload stopped after posting {len(log)} grade(s) due to a Canvas "
                    f"error: {error_message}. Log: {log_path}"
                )
            else:
                st.success(f"Posted {len(log)} grade(s). Log: {log_path}")
            st.session_state["upload_previewed"] = False
