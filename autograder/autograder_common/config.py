"""Load course and per-assignment YAML configs."""
import os
from pathlib import Path

import yaml


class ConfigError(Exception):
    pass


REQUIRED_COURSE_FIELDS = ["canvas_base_url", "canvas_course_id"]
REQUIRED_ASSIGNMENT_FIELDS = ["course", "key", "submission_type", "rubric"]
VALID_SUBMISSION_TYPES = ("canvas_upload", "github_url")


def load_course_config(path):
    """Load a course config YAML and attach the Canvas API token from the
    CANVAS_API_TOKEN environment variable.

    Returns {"canvas_base_url": str, "canvas_course_id": ..., "canvas_token": str}.
    Raises ConfigError if a required field or the env var is missing.
    """
    path = Path(path)
    data = yaml.safe_load(path.read_text())
    if not isinstance(data, dict):
        raise ConfigError(f"{path}: expected a YAML mapping at the top level")
    missing = [f for f in REQUIRED_COURSE_FIELDS if f not in data]
    if missing:
        raise ConfigError(f"{path}: missing required field(s): {', '.join(missing)}")
    token = os.environ.get("CANVAS_API_TOKEN")
    if not token:
        raise ConfigError("CANVAS_API_TOKEN environment variable is not set")
    return {
        "canvas_base_url": data["canvas_base_url"].rstrip("/"),
        "canvas_course_id": data["canvas_course_id"],
        "canvas_token": token,
    }


def load_assignment_config(path):
    """Load and validate a per-assignment YAML config. Returns the parsed
    dict as-is (not transformed) once required fields are confirmed present."""
    path = Path(path)
    data = yaml.safe_load(path.read_text())
    if not isinstance(data, dict):
        raise ConfigError(f"{path}: expected a YAML mapping at the top level")
    missing = [f for f in REQUIRED_ASSIGNMENT_FIELDS if f not in data]
    if missing:
        raise ConfigError(f"{path}: missing required field(s): {', '.join(missing)}")
    if data["submission_type"] not in VALID_SUBMISSION_TYPES:
        raise ConfigError(
            f"{path}: submission_type must be one of {VALID_SUBMISSION_TYPES}, "
            f"got {data['submission_type']!r}"
        )
    return data
