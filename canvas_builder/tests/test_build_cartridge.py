import subprocess
import sys
import textwrap
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

VALID_MANIFEST = """\
course_code: ISM9999
course_title: Test Course
site_base_url: https://example.github.io/ism9999/
modules:
  - title: "Module 1"
    items:
      - {label: "Reading", site_path: "pages/week01_reading.html"}
      - {label: "Lecture", site_path: "pages/week01_lecture.html"}
  - title: "Module 2"
    items:
      - {label: "Lab", site_path: "pages/week02_lab.html"}
    assignment:
      name: "Lab 1"
      group: "Weekly Labs"
      points: 10
"""


def _run_cli(manifest_path, out_path):
    return subprocess.run(
        [
            sys.executable,
            "canvas_builder/build_cartridge.py",
            "--manifest", str(manifest_path),
            "--out", str(out_path),
        ],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )


def test_cli_builds_cartridge_with_matching_counts(tmp_path):
    manifest_path = tmp_path / "manifest.yaml"
    manifest_path.write_text(textwrap.dedent(VALID_MANIFEST))
    out_path = tmp_path / "out.imscc"

    result = _run_cli(manifest_path, out_path)

    assert result.returncode == 0, result.stderr
    assert "MISMATCH" not in result.stdout
    assert "Weblinks:    3 (expected 3)" in result.stdout
    assert "Assignments: 1 (expected 1)" in result.stdout

    with zipfile.ZipFile(out_path) as zf:
        names = zf.namelist()
        assert "imsmanifest.xml" in names
        assert sum(1 for n in names if n.startswith("weblinks/")) == 3
        assert sum(1 for n in names if n.startswith("assignment_")) == 1
