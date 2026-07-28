#!/usr/bin/env python3
"""ISM3232 autograder CLI. See README.md for setup and usage.

Usage:
    python grade_ism3232.py fetch  --assignment week07_assignment
    python grade_ism3232.py check  --assignment week07_assignment
    python grade_ism3232.py upload --assignment week07_assignment --dry-run
    python grade_ism3232.py upload --assignment week07_assignment
"""
from pathlib import Path

from autograder_common.cli import main

ROOT = Path(__file__).resolve().parent

if __name__ == "__main__":
    main(
        course_config_path=ROOT / "ism3232.config.yaml",
        assignments_dir=ROOT / "assignments" / "ism3232",
    )
