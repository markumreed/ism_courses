"""Pure helper functions for the Streamlit GUI (gui.py). No Streamlit
import here — every function is independently unit-testable and mirrors
the same logic autograder_common.cli's private functions use, so the CLI
and GUI produce identical records/files for the same inputs."""
from pathlib import Path

from . import checks
from .config import load_assignment_config
from .scoring import ScoringError, compute_score


def student_key(user_name):
    """Same normalization cli._student_key uses: lowercase, alphanumeric only."""
    return "".join(ch for ch in user_name.lower() if ch.isalnum())


def discover_assignments(assignments_dir):
    """Load every *.yaml file in assignments_dir as an assignment config.
    Each returned dict has an added "_path" key (the source Path)."""
    assignments_dir = Path(assignments_dir)
    result = []
    for path in sorted(assignments_dir.glob("*.yaml")):
        config = load_assignment_config(path)
        config["_path"] = path
        result.append(config)
    return result


def compute_signals(student_dir, assignment_config):
    """Run every mechanical primitive listed in assignment_config['mechanical_checks']
    once. Returns (signals: {check_id: (passed, output)}, captured_output: str).
    Identical logic/shape to autograder_common.cli._compute_signals."""
    signals = {}
    captured_parts = []
    checks_to_run = set(assignment_config.get("mechanical_checks", []))
    expected_files = assignment_config.get("expected_files", [])

    if "file_present" in checks_to_run and expected_files:
        presence = checks.file_present(student_dir, expected_files)
        signals["file_present"] = (all(presence.values()), "")

    if "runs_without_error" in checks_to_run and expected_files:
        run_cfg = assignment_config.get("run", {})
        target = Path(student_dir) / expected_files[0]
        ok, out, err = checks.runs_without_error(
            target, run_cfg["command"], run_cfg.get("timeout_seconds", 10)
        )
        signals["runs_without_error"] = (ok, out)
        captured_parts.append(out + (("\n" + err) if err else ""))

    if "ruff_clean" in checks_to_run:
        ok, out = checks.ruff_check(student_dir)
        signals["ruff_clean"] = (ok, out)
        captured_parts.append("--- ruff ---\n" + out)

    if "pytest_passes" in checks_to_run:
        ok, out = checks.pytest_check(student_dir)
        signals["pytest_passes"] = (ok, out)
        captured_parts.append("--- pytest ---\n" + out)

    if checks_to_run & {"git_log_commit_count", "git_log_message_quality", "git_log_spread"}:
        log = checks.git_log_checks(student_dir)
        signals["git_log_commit_count"] = (log["commit_count"] >= 3, f"{log['commit_count']} commits")
        signals["git_log_message_quality"] = (
            log["generic_message_count"] == 0,
            f"{log['generic_message_count']} generic commit message(s)",
        )
        signals["git_log_spread"] = (
            log["spans_multiple_hours"],
            "spans multiple hours" if log["spans_multiple_hours"] else "all commits within one hour",
        )

    return signals, "\n".join(captured_parts)


def compute_student_record(student_dir, student_key_val, student_name, assignment_config):
    """Build one student's check-result record: student_key, student_name,
    status, captured_output, plus one key per mechanical rubric field holding
    True/False. Human-scored fields are never set here (left for the GUI's
    input widgets). Identical record shape to what cli.cmd_check builds."""
    signals, captured = compute_signals(student_dir, assignment_config)
    record = {
        "student_key": student_key_val,
        "student_name": student_name,
        "status": "ok",
        "captured_output": captured,
    }
    for field_name, spec in assignment_config.get("rubric", {}).items():
        if spec.get("source") == "mechanical":
            passed, _ = signals.get(spec["check"], (False, ""))
            record[field_name] = passed
    return record


def live_score(row, assignment_config):
    """Compute the current score for a (possibly incomplete) worksheet row.
    Returns None instead of raising when a human field is still blank or
    out of range, so the GUI can render "-" without crashing the page."""
    try:
        return compute_score(row, assignment_config)
    except ScoringError:
        return None


def build_upload_plan(rows, assignment_config, current_grades):
    """rows: worksheet rows (as read by worksheet.read_worksheet).
    current_grades: {student_key: float|None}, already fetched by the caller
    via CanvasClient.get_current_grade (kept out of this function so it has
    no Canvas dependency and stays trivially testable).

    Returns a list of {student_key, student_name, current_grade, new_grade,
    comment} for every status == "ok" row, in row order."""
    plan = []
    for row in rows:
        if row.get("status") != "ok":
            continue
        plan.append({
            "student_key": row["student_key"],
            "student_name": row["student_name"],
            "current_grade": current_grades.get(row["student_key"]),
            "new_grade": compute_score(row, assignment_config),
            "comment": row.get("comment", ""),
        })
    return plan
