"""Build and read the review worksheet CSV: mechanical results auto-filled,
human-scored rubric fields left blank for the instructor to complete."""
import csv
from pathlib import Path

MECHANICAL_COLUMN_PREFIX = "mech_"
HUMAN_COLUMN_PREFIX = "human_"


def human_fields(assignment_config):
    """Rubric field names whose source is 'human' (need instructor input),
    in the order they appear in the config."""
    return [
        name for name, spec in assignment_config["rubric"].items()
        if spec.get("source") == "human"
    ]


def mechanical_fields(assignment_config):
    """Rubric field names whose source is 'mechanical'."""
    return [
        name for name, spec in assignment_config["rubric"].items()
        if spec.get("source") == "mechanical"
    ]


def build_worksheet(path, students, assignment_config):
    """Write the review worksheet CSV.

    students: list of dicts, each with at least student_key, student_name,
    status, and (for mechanical fields) that field's already-computed value
    keyed directly on the dict, e.g. {"submission": True, ...}.
    Human-scored fields are always written blank.
    """
    human = human_fields(assignment_config)
    mechanical = mechanical_fields(assignment_config)
    fieldnames = (
        ["student_key", "student_name", "status"]
        + [f"{MECHANICAL_COLUMN_PREFIX}{f}" for f in mechanical]
        + [f"{HUMAN_COLUMN_PREFIX}{f}" for f in human]
        + ["captured_output", "comment"]
    )
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for student in students:
            row = {
                "student_key": student["student_key"],
                "student_name": student["student_name"],
                "status": student["status"],
                "captured_output": student.get("captured_output", ""),
                "comment": "",
            }
            for f in mechanical:
                row[f"{MECHANICAL_COLUMN_PREFIX}{f}"] = student.get(f, "")
            for f in human:
                row[f"{HUMAN_COLUMN_PREFIX}{f}"] = ""
            writer.writerow(row)


def read_worksheet(path):
    """Read a worksheet CSV back into a list of dicts (all values strings,
    as written by csv.DictReader)."""
    path = Path(path)
    with path.open(newline="") as fh:
        return list(csv.DictReader(fh))


def incomplete_students(rows, assignment_config):
    """Return the student_keys (for rows with status == 'ok') whose
    human-scored fields are still blank."""
    human = human_fields(assignment_config)
    incomplete = []
    for row in rows:
        if row.get("status") != "ok":
            continue
        for f in human:
            if not row.get(f"{HUMAN_COLUMN_PREFIX}{f}", "").strip():
                incomplete.append(row["student_key"])
                break
    return incomplete
