"""Convert a completed worksheet row into a final numeric grade, per an
assignment's rubric config."""
from .worksheet import HUMAN_COLUMN_PREFIX, MECHANICAL_COLUMN_PREFIX

LEVEL_VALUES = {"excellent": 4, "good": 3, "developing": 2, "incomplete": 1}


class ScoringError(Exception):
    pass


def compute_points_score(row, assignment_config):
    """Points-based rubric (labs, weekly assignments, developer workflow,
    ISM3232 capstone): sum each rubric field's points.

    Mechanical fields: row['mech_<field>'] is 'True' (earned, full points)
    or anything else (not earned, 0 points).
    Human fields: row['human_<field>'] is a number from 0..points, entered
    directly by the instructor (supports partial credit).
    """
    total = 0.0
    for name, spec in assignment_config["rubric"].items():
        points = spec["points"]
        if spec["source"] == "mechanical":
            raw = row.get(f"{MECHANICAL_COLUMN_PREFIX}{name}", "")
            earned = raw.strip().lower() in ("true", "1", "yes")
            total += points if earned else 0
        else:
            raw = row.get(f"{HUMAN_COLUMN_PREFIX}{name}", "").strip()
            if not raw:
                raise ScoringError(
                    f"human field {name!r} is blank for {row.get('student_key')}"
                )
            value = float(raw)
            if value < 0 or value > points:
                raise ScoringError(
                    f"human field {name!r} for {row.get('student_key')} is {value}, "
                    f"outside 0..{points}"
                )
            total += value
    return total


def compute_capstone_score(row, assignment_config):
    """Level-based rubric (ISM2411 capstone): each dimension in
    assignment_config['rubric'] is source: human, and the instructor enters
    one of excellent/good/developing/incomplete into human_<dimension>.
    Final score = average(level value 1-4 across dimensions) * 25.
    """
    dimensions = list(assignment_config["rubric"].keys())
    values = []
    for name in dimensions:
        raw = row.get(f"{HUMAN_COLUMN_PREFIX}{name}", "").strip().lower()
        if raw not in LEVEL_VALUES:
            raise ScoringError(
                f"dimension {name!r} for {row.get('student_key')} must be one of "
                f"{sorted(LEVEL_VALUES)}, got {raw!r}"
            )
        values.append(LEVEL_VALUES[raw])
    return (sum(values) / len(values)) * 25


def compute_score(row, assignment_config):
    """Dispatch to compute_points_score or compute_capstone_score based on
    assignment_config.get('scoring_type', 'points')."""
    scoring_type = assignment_config.get("scoring_type", "points")
    if scoring_type == "points":
        return compute_points_score(row, assignment_config)
    if scoring_type == "capstone_levels":
        return compute_capstone_score(row, assignment_config)
    raise ScoringError(f"unknown scoring_type: {scoring_type!r}")
