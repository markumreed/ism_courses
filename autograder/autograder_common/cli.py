"""Shared CLI scaffolding: fetch / check / upload subcommands, parameterized
by a course's Canvas config and its assignments directory."""
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from . import checks, fetch, scoring, worksheet
from .canvas import CanvasClient
from .config import load_assignment_config, load_course_config


def _student_key(user_name):
    return "".join(ch for ch in user_name.lower() if ch.isalnum())


def _load(course_config_path, assignments_dir, assignment_key):
    course_config = load_course_config(course_config_path)
    assignment_config = load_assignment_config(
        Path(assignments_dir) / f"{assignment_key}.yaml"
    )
    client = CanvasClient(
        course_config["canvas_base_url"],
        course_config["canvas_course_id"],
        course_config["canvas_token"],
    )
    return course_config, assignment_config, client


def _assignment_id(assignment_config, client):
    override = assignment_config.get("canvas_assignment_id")
    if override:
        return override
    return client.find_assignment_id(assignment_config["canvas_display_name"])


def cmd_fetch(args, course_config_path, assignments_dir, runs_dir):
    _, assignment_config, client = _load(course_config_path, assignments_dir, args.assignment)
    assignment_id = _assignment_id(assignment_config, client)
    submissions = client.list_submissions(assignment_id)
    out_dir = Path(runs_dir) / args.assignment
    out_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    for sub in submissions:
        user = sub.get("user") or {}
        name = user.get("name", f"user-{sub.get('user_id')}")
        dest = out_dir / _student_key(name)
        try:
            fetch.fetch_submission(sub, assignment_config, client, dest)
            count += 1
        except fetch.FetchError as e:
            print(f"  {name}: fetch failed - {e}")
    print(f"Fetched {count}/{len(submissions)} submissions to {out_dir}")


def _compute_signals(student_dir, assignment_config):
    """Run every mechanical primitive listed in assignment_config['mechanical_checks']
    once. Returns (signals: {check_id: (passed, output)}, captured_output: str)."""
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


def cmd_check(args, course_config_path, assignments_dir, runs_dir):
    _, assignment_config, client = _load(course_config_path, assignments_dir, args.assignment)
    assignment_id = _assignment_id(assignment_config, client)
    submissions = client.list_submissions(assignment_id)
    out_dir = Path(runs_dir) / args.assignment

    students = []
    for sub in submissions:
        user = sub.get("user") or {}
        name = user.get("name", f"user-{sub.get('user_id')}")
        key = _student_key(name)
        student_dir = out_dir / key
        if not student_dir.exists():
            students.append({
                "student_key": key, "student_name": name,
                "status": "fetch-failed", "captured_output": "",
            })
            continue

        signals, captured = _compute_signals(student_dir, assignment_config)
        record = {"student_key": key, "student_name": name, "status": "ok", "captured_output": captured}
        for field_name, spec in assignment_config["rubric"].items():
            if spec.get("source") == "mechanical":
                passed, _ = signals.get(spec["check"], (False, ""))
                record[field_name] = passed
        students.append(record)

    worksheet_path = out_dir / "review.csv"
    worksheet.build_worksheet(worksheet_path, students, assignment_config)
    print(f"Wrote {worksheet_path}")


def cmd_upload(args, course_config_path, assignments_dir, runs_dir):
    course_config, assignment_config, client = _load(course_config_path, assignments_dir, args.assignment)
    assignment_id = _assignment_id(assignment_config, client)

    worksheet_path = Path(runs_dir) / args.assignment / "review.csv"
    rows = worksheet.read_worksheet(worksheet_path)
    incomplete = worksheet.incomplete_students(rows, assignment_config)
    if incomplete:
        print("Cannot upload - these students have incomplete human-scored fields:")
        for key in incomplete:
            print(f"  {key}")
        sys.exit(1)

    submissions = client.list_submissions(assignment_id)
    key_to_user_id = {
        _student_key((s.get("user") or {}).get("name", f"user-{s['user_id']}")): s["user_id"]
        for s in submissions
    }

    plan = []
    for row in rows:
        if row.get("status") != "ok":
            continue
        user_id = key_to_user_id.get(row["student_key"])
        if user_id is None:
            print(f"  {row['student_name']}: no matching Canvas submission, skipping")
            continue
        score = scoring.compute_score(row, assignment_config)
        current = client.get_current_grade(assignment_id, user_id)
        plan.append((user_id, row["student_name"], current, score, row.get("comment", "")))

    for _, name, current, new, _ in plan:
        current_str = "ungraded" if current is None else current
        print(f"  {name}: {current_str} -> {new}")

    if args.dry_run:
        print(f"Dry run - {len(plan)} grade(s) would be posted, nothing sent.")
        return

    if not args.yes:
        answer = input(f"Post {len(plan)} grade(s) for {args.assignment}? [y/N] ")
        if answer.strip().lower() != "y":
            print("Aborted.")
            return

    log = []
    for user_id, name, current, new, comment in plan:
        client.post_grade(assignment_id, user_id, new, comment or None)
        log.append({"user_id": user_id, "name": name, "previous": current, "posted": new})

    runs_dir_path = Path(runs_dir) / args.assignment
    runs_dir_path.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    log_path = runs_dir_path / f"upload_log_{timestamp}.json"
    log_path.write_text(json.dumps(log, indent=2))
    print(f"Posted {len(log)} grade(s). Log: {log_path}")


def build_cli(course_config_path, assignments_dir, runs_dir="runs"):
    """Build an argparse.ArgumentParser with fetch/check/upload subcommands
    wired to one course's config + assignments directory."""
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    fetch_p = sub.add_parser("fetch")
    fetch_p.add_argument("--assignment", required=True)
    fetch_p.set_defaults(func=lambda a: cmd_fetch(a, course_config_path, assignments_dir, runs_dir))

    check_p = sub.add_parser("check")
    check_p.add_argument("--assignment", required=True)
    check_p.set_defaults(func=lambda a: cmd_check(a, course_config_path, assignments_dir, runs_dir))

    upload_p = sub.add_parser("upload")
    upload_p.add_argument("--assignment", required=True)
    upload_p.add_argument("--dry-run", action="store_true")
    upload_p.add_argument("--yes", action="store_true")
    upload_p.set_defaults(func=lambda a: cmd_upload(a, course_config_path, assignments_dir, runs_dir))

    return parser


def main(course_config_path, assignments_dir, argv=None):
    parser = build_cli(course_config_path, assignments_dir)
    args = parser.parse_args(argv)
    args.func(args)
