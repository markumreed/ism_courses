#!/usr/bin/env python3
"""ISM2411 autograder CLI. See README.md for setup and usage.

Usage:
    python grade_ism2411.py fetch  --assignment week03_lab
    python grade_ism2411.py check  --assignment week03_lab
    python grade_ism2411.py upload --assignment week03_lab --dry-run
    python grade_ism2411.py upload --assignment week03_lab
"""
from pathlib import Path

from autograder_common.cli import main

ROOT = Path(__file__).resolve().parent

if __name__ == "__main__":
    main(
        course_config_path=ROOT / "ism2411.config.yaml",
        assignments_dir=ROOT / "assignments" / "ism2411",
    )
