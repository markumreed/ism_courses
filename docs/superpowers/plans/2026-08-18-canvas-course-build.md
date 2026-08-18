# Canvas Course Build (ISM2411 & ISM3232) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build one Canvas-importable Common Cartridge (`.imscc`) file per course (ISM2411, ISM3232) that creates Modules (mirroring each course's existing week/unit schedule), gradable Assignments matching each syllabus's grading table, and outbound links to the existing course websites — with no Canvas API access required.

**Architecture:** A small standalone Python tool, `canvas_builder/`, reads a per-course YAML manifest (modules → items → optional assignment) and emits a standards-compliant IMS Common Cartridge 1.3 package: `<organization>` items become Canvas Modules, IMS "Web Link" resources (`imswl_xmlv1p3`) become External URL module items pointing at the course website, and IMS "CC Assignment" resources (`assignment_xmlv1p0`) become gradable Canvas Assignments with a title, description, and point value. Both weblinks and CC assignments are documented, cross-vendor IMS Common Cartridge extensions (not Canvas-proprietary XML), which is deliberately chosen over Canvas's undocumented proprietary export format to minimize the risk of a broken import.

**Tech Stack:** Python 3, PyYAML (already a project dependency — see `autograder/requirements.txt`), stdlib `zipfile` and `xml.etree.ElementTree`/`xml.sax.saxutils`, pytest (matching the `autograder/` package's existing structure and conventions).

**Spec:** `docs/superpowers/specs/2026-08-18-canvas-course-build-design.md`

## Deviations from the spec (read before implementing)

The spec's manifest example sketched `syllabus_source: .../*.md` (auto-convert markdown) and a cartridge-embedded Syllabus/Front Page/Assignment-Groups built from Canvas's proprietary `course_settings/` cartridge extension. During planning these were refined for lower risk and more consistency with the rest of the design:

1. **Syllabus & Front Page ship as separate hand-authored HTML files, not inside the cartridge.** Canvas's proprietary `course_settings/` schema (used to auto-import Syllabus/Front-Page content) is undocumented and not part of the standard IMS Common Cartridge spec — getting it wrong risks a broken cartridge import for everything, not just the syllabus. Both courses already have a **complete, polished Syllabus page on their website** (`ism2411/pages/syllabus.html`, `ism3232/docs/syllabus.html` — full grading tables, schedule, and policies). So the Canvas Syllabus tool gets a short **summary + grading table + link to the full page**, consistent with this project's "Canvas organizes, the website is the source of truth" strategy — not a duplicate copy. Same idea for the Front Page. Both ship as standalone `.html` files the instructor pastes into Canvas's Syllabus/Front-Page rich text editor (30 seconds each, zero import risk).
2. **No automated Assignment Groups.** Canvas's per-course "Assignment Groups with weights" is also part of the undocumented proprietary extension. Each `AssignmentSpec` still carries a `group` field, but it's used only to generate a **post-import checklist** in `canvas_builder/README.md` telling the instructor which group each assignment belongs in — a few minutes of drag-and-drop in Canvas, versus a much higher risk of a rejected cartridge.
3. **Assignment point values are the plan author's disclosed assumption**, not sourced from an explicit Canvas points scale in either syllabus (neither syllabus specifies raw points, only percentage weights). Labs use 10 pts (matching ISM2411's explicit "each lab scored out of 10 points" rubric); other assignments use a proportioned placeholder documented in Task 5/6 below. All are trivially editable in Canvas after import.

None of this changes the spec's goals or scope — it changes *how* the same deliverables get built, in favor of the lower-risk path.

## Global Constraints

- No Canvas API calls anywhere in this tool — it must run with zero network access and zero credentials (spec: institution disables personal API tokens).
- Cartridges must validate structurally before hand-off: the CLI itself must compare the manifest's expected weblink/assignment counts against what actually landed in the built `.imscc` and fail loudly (exit code 1) on any mismatch (spec's Validation Plan step 2).
- Follow the existing `autograder/` package's conventions: a `<tool>_common/` package for logic, flat CLI scripts, a `tests/` dir, run via `cd canvas_builder && pytest tests/` (see `autograder/tests/test_config.py` for the import style to match: `from canvas_builder_common.x import y`, not a relative or repo-root-qualified import).
- No content duplication: module items link to the existing course websites; nothing here re-hosts reading/lecture/lab text.
- Quizzes and native Canvas Quiz creation are out of scope for this plan (spec's Non-goals).

---

### Task 1: Manifest schema + YAML loader

**Files:**
- Create: `canvas_builder/canvas_builder_common/__init__.py` (empty)
- Create: `canvas_builder/canvas_builder_common/manifest_schema.py`
- Test: `canvas_builder/tests/__init__.py` (empty)
- Test: `canvas_builder/tests/test_manifest_schema.py`

**Interfaces:**
- Produces: `ModuleItem(label: str, site_path: str)`, `AssignmentSpec(name: str, group: str, points: float, description_html: str = "")`, `ModuleSpec(title: str, items: list[ModuleItem], assignment: AssignmentSpec | None = None)`, `CourseManifest(course_code: str, course_title: str, site_base_url: str, modules: list[ModuleSpec])`, `load_manifest(path: str) -> CourseManifest`.

- [ ] **Step 1: Write the failing test**

Create `canvas_builder/tests/__init__.py` (empty file) and `canvas_builder/tests/test_manifest_schema.py`:

```python
import textwrap

from canvas_builder_common.manifest_schema import load_manifest


def test_load_manifest_parses_modules_and_items(tmp_path):
    manifest_path = tmp_path / "test_manifest.yaml"
    manifest_path.write_text(textwrap.dedent("""\
        course_code: ISM9999
        course_title: Test Course
        site_base_url: https://example.github.io/ism9999/
        modules:
          - title: "Module 1 — Intro"
            items:
              - {label: "Reading", site_path: "pages/week01_reading.html"}
              - {label: "Lecture", site_path: "pages/week01_lecture.html"}
          - title: "Module 2 — Loops"
            items:
              - {label: "Lab", site_path: "pages/week02_lab.html"}
            assignment:
              name: "Lab 1"
              group: "Weekly Labs"
              points: 10
        """))

    manifest = load_manifest(str(manifest_path))

    assert manifest.course_code == "ISM9999"
    assert manifest.course_title == "Test Course"
    assert manifest.site_base_url == "https://example.github.io/ism9999"  # trailing slash stripped
    assert len(manifest.modules) == 2

    module_1 = manifest.modules[0]
    assert module_1.title == "Module 1 — Intro"
    assert len(module_1.items) == 2
    assert module_1.items[0].label == "Reading"
    assert module_1.items[0].site_path == "pages/week01_reading.html"
    assert module_1.assignment is None

    module_2 = manifest.modules[1]
    assert module_2.assignment.name == "Lab 1"
    assert module_2.assignment.group == "Weekly Labs"
    assert module_2.assignment.points == 10
    assert module_2.assignment.description_html == ""
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd canvas_builder && python -m pytest tests/test_manifest_schema.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'canvas_builder_common'`

- [ ] **Step 3: Write minimal implementation**

Create `canvas_builder/canvas_builder_common/__init__.py` (empty), then `canvas_builder/canvas_builder_common/manifest_schema.py`:

```python
"""Data model and YAML loader for canvas_builder course manifests."""
from __future__ import annotations

from dataclasses import dataclass, field

import yaml


@dataclass
class ModuleItem:
    label: str
    site_path: str  # relative path on the course website, e.g. "pages/week02_lab.html"


@dataclass
class AssignmentSpec:
    name: str
    group: str
    points: float
    description_html: str = ""


@dataclass
class ModuleSpec:
    title: str
    items: list[ModuleItem] = field(default_factory=list)
    assignment: AssignmentSpec | None = None


@dataclass
class CourseManifest:
    course_code: str
    course_title: str
    site_base_url: str
    modules: list[ModuleSpec] = field(default_factory=list)


def load_manifest(path: str) -> CourseManifest:
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    modules = []
    for m in data["modules"]:
        items = [
            ModuleItem(label=i["label"], site_path=i["site_path"])
            for i in m.get("items", [])
        ]
        assignment = None
        a = m.get("assignment")
        if a:
            assignment = AssignmentSpec(
                name=a["name"],
                group=a["group"],
                points=float(a["points"]),
                description_html=a.get("description_html", ""),
            )
        modules.append(ModuleSpec(title=m["title"], items=items, assignment=assignment))

    return CourseManifest(
        course_code=data["course_code"],
        course_title=data["course_title"],
        site_base_url=data["site_base_url"].rstrip("/"),
        modules=modules,
    )
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd canvas_builder && python -m pytest tests/test_manifest_schema.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add canvas_builder/canvas_builder_common/__init__.py \
        canvas_builder/canvas_builder_common/manifest_schema.py \
        canvas_builder/tests/__init__.py \
        canvas_builder/tests/test_manifest_schema.py
git commit -m "canvas_builder: add course manifest schema and YAML loader"
```

---

### Task 2: Cartridge writer — modules and weblink items

**Files:**
- Create: `canvas_builder/canvas_builder_common/cartridge_writer.py`
- Test: `canvas_builder/tests/test_cartridge_writer.py`

**Interfaces:**
- Consumes: `CourseManifest`, `ModuleSpec`, `ModuleItem`, `AssignmentSpec` from Task 1 (`canvas_builder_common.manifest_schema`).
- Produces: `new_id(prefix: str) -> str`, `weblink_xml(title: str, url: str) -> str`, `build_cartridge_files(course: CourseManifest) -> dict[str, bytes]` (path-in-zip → file content, including `"imsmanifest.xml"`).

- [ ] **Step 1: Write the failing test**

Create `canvas_builder/tests/test_cartridge_writer.py`:

```python
import xml.etree.ElementTree as ET

from canvas_builder_common.cartridge_writer import build_cartridge_files
from canvas_builder_common.manifest_schema import CourseManifest, ModuleItem, ModuleSpec

NS = {"cc": "http://www.imsglobal.org/xsd/imsccv1p3/imscp_v1p1"}


def _two_module_course():
    return CourseManifest(
        course_code="ISM9999",
        course_title="Test Course",
        site_base_url="https://example.github.io/ism9999",
        modules=[
            ModuleSpec(
                title="Module 1",
                items=[
                    ModuleItem(label="Reading", site_path="pages/week01_reading.html"),
                    ModuleItem(label="Lecture", site_path="pages/week01_lecture.html"),
                ],
            ),
            ModuleSpec(
                title="Module 2",
                items=[ModuleItem(label="Lab", site_path="pages/week02_lab.html")],
            ),
        ],
    )


def _module_items(root):
    return root.findall("cc:organizations/cc:organization/cc:item/cc:item", NS)


def test_manifest_has_one_top_level_item_per_module():
    files = build_cartridge_files(_two_module_course())
    root = ET.fromstring(files["imsmanifest.xml"])
    modules = _module_items(root)
    assert len(modules) == 2
    assert modules[0].find("cc:title", NS).text == "Module 1"
    assert modules[1].find("cc:title", NS).text == "Module 2"


def test_module_items_become_weblink_children_in_order():
    files = build_cartridge_files(_two_module_course())
    root = ET.fromstring(files["imsmanifest.xml"])
    module_1_children = _module_items(root)[0].findall("cc:item", NS)
    assert [c.find("cc:title", NS).text for c in module_1_children] == ["Reading", "Lecture"]


def test_resources_list_one_weblink_per_item_with_matching_files():
    files = build_cartridge_files(_two_module_course())
    root = ET.fromstring(files["imsmanifest.xml"])
    resources = root.findall("cc:resources/cc:resource", NS)
    assert len(resources) == 3  # Reading, Lecture, Lab
    for r in resources:
        assert r.get("type") == "imswl_xmlv1p3"
        href = r.get("href")
        assert href in files, f"resource href {href} missing from generated files"


def test_weblink_file_contains_absolute_url_built_from_site_base_url():
    files = build_cartridge_files(_two_module_course())
    reading_content = next(
        content
        for path, content in files.items()
        if path.startswith("weblinks/") and b"<title>Reading</title>" in content
    )
    assert b"https://example.github.io/ism9999/pages/week01_reading.html" in reading_content
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd canvas_builder && python -m pytest tests/test_cartridge_writer.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'canvas_builder_common.cartridge_writer'`

- [ ] **Step 3: Write minimal implementation**

Create `canvas_builder/canvas_builder_common/cartridge_writer.py`:

```python
"""Builds an IMS Common Cartridge 1.3 package from a CourseManifest.

Uses only standard, documented IMS Common Cartridge elements (Organizations
for Modules, Web Link resources for outbound links, CC Assignment resources
for gradable work) rather than Canvas's undocumented proprietary cartridge
extensions — see the "Deviations from the spec" note in the implementation
plan for why.
"""
from __future__ import annotations

import uuid
from xml.sax.saxutils import escape

from canvas_builder_common.manifest_schema import CourseManifest

CC_NS = "http://www.imsglobal.org/xsd/imsccv1p3/imscp_v1p1"
WEBLINK_NS = "http://www.imsglobal.org/xsd/imsccv1p3/imswl_v1p3"


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


def weblink_xml(title: str, url: str) -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<webLink xmlns="{WEBLINK_NS}">\n'
        f"  <title>{escape(title)}</title>\n"
        f'  <url href="{escape(url)}" target="_blank"/>\n'
        "</webLink>\n"
    )


def build_cartridge_files(course: CourseManifest) -> dict[str, bytes]:
    """Returns {path-within-zip: content-bytes} for every cartridge file,
    including imsmanifest.xml."""
    resource_entries = []  # (identifier, type, path, content_bytes)
    module_items_xml = []

    for module in course.modules:
        child_items_xml = []
        for item in module.items:
            ident = new_id("link")
            url = f"{course.site_base_url}/{item.site_path}"
            path = f"weblinks/{ident}.xml"
            content = weblink_xml(item.label, url).encode("utf-8")
            resource_entries.append((ident, "imswl_xmlv1p3", path, content))
            child_items_xml.append(
                f'      <item identifier="item_{ident}" identifierref="{ident}">\n'
                f"        <title>{escape(item.label)}</title>\n"
                "      </item>\n"
            )

        module_id = new_id("module")
        module_items_xml.append(
            f'    <item identifier="{module_id}">\n'
            f"      <title>{escape(module.title)}</title>\n"
            + "".join(child_items_xml)
            + "    </item>\n"
        )

    resources_xml = "".join(
        f'    <resource identifier="{ident}" type="{rtype}" href="{path}">\n'
        f'      <file href="{path}"/>\n'
        "    </resource>\n"
        for ident, rtype, path, _content in resource_entries
    )

    manifest_xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<manifest identifier="{new_id("man")}" xmlns="{CC_NS}">\n'
        "  <metadata>\n"
        "    <schema>IMS Common Cartridge</schema>\n"
        "    <schemaversion>1.3.0</schemaversion>\n"
        "  </metadata>\n"
        "  <organizations>\n"
        f'    <organization identifier="{new_id("org")}" structure="rooted-hierarchy">\n'
        '      <item identifier="LearningModules">\n'
        + "".join(module_items_xml)
        + "      </item>\n"
        "    </organization>\n"
        "  </organizations>\n"
        "  <resources>\n" + resources_xml + "  </resources>\n"
        "</manifest>\n"
    )

    files = {path: content for _ident, _rtype, path, content in resource_entries}
    files["imsmanifest.xml"] = manifest_xml.encode("utf-8")
    return files
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd canvas_builder && python -m pytest tests/test_cartridge_writer.py -v`
Expected: PASS (4 tests)

- [ ] **Step 5: Commit**

```bash
git add canvas_builder/canvas_builder_common/cartridge_writer.py \
        canvas_builder/tests/test_cartridge_writer.py
git commit -m "canvas_builder: generate CC manifest with modules and weblink items"
```

---

### Task 3: Cartridge writer — gradable Assignments

**Files:**
- Modify: `canvas_builder/canvas_builder_common/cartridge_writer.py`
- Modify: `canvas_builder/tests/test_cartridge_writer.py`

**Interfaces:**
- Consumes: `AssignmentSpec` (Task 1), the `build_cartridge_files` structure from Task 2.
- Produces: `assignment_xml(assignment: AssignmentSpec, identifier: str) -> str`; `build_cartridge_files` now also emits an `assignment_xmlv1p0` resource + `<item>` for any `module.assignment` that is not `None`.

- [ ] **Step 1: Write the failing test**

Append to `canvas_builder/tests/test_cartridge_writer.py`:

```python
from canvas_builder_common.manifest_schema import AssignmentSpec


def _course_with_assignment():
    return CourseManifest(
        course_code="ISM9999",
        course_title="Test Course",
        site_base_url="https://example.github.io/ism9999",
        modules=[
            ModuleSpec(
                title="Module 2",
                items=[ModuleItem(label="Lab", site_path="pages/week02_lab.html")],
                assignment=AssignmentSpec(name="Lab 1", group="Weekly Labs", points=10),
            ),
        ],
    )


def test_module_with_assignment_gets_weblink_and_assignment_items():
    files = build_cartridge_files(_course_with_assignment())
    root = ET.fromstring(files["imsmanifest.xml"])
    children = _module_items(root)[0].findall("cc:item", NS)
    assert [c.find("cc:title", NS).text for c in children] == ["Lab", "Lab 1"]


def test_assignment_resource_has_correct_type_and_points():
    files = build_cartridge_files(_course_with_assignment())
    root = ET.fromstring(files["imsmanifest.xml"])
    resources = root.findall("cc:resources/cc:resource", NS)
    assignment_resources = [r for r in resources if r.get("type") == "assignment_xmlv1p0"]
    assert len(assignment_resources) == 1

    href = assignment_resources[0].get("href")
    content = files[href]
    assert b"<title>Lab 1</title>" in content
    assert b'points_possible="10"' in content


def test_module_without_assignment_has_no_assignment_resource():
    files = build_cartridge_files(_two_module_course())
    root = ET.fromstring(files["imsmanifest.xml"])
    resources = root.findall("cc:resources/cc:resource", NS)
    assert not any(r.get("type") == "assignment_xmlv1p0" for r in resources)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd canvas_builder && python -m pytest tests/test_cartridge_writer.py -v`
Expected: FAIL — `test_module_with_assignment_gets_weblink_and_assignment_items` and
`test_assignment_resource_has_correct_type_and_points` fail (no assignment item/resource emitted yet).

- [ ] **Step 3: Write minimal implementation**

In `canvas_builder/canvas_builder_common/cartridge_writer.py`, add the `assignment_xml` function and extend `build_cartridge_files`:

```python
ASSIGNMENT_NS = "http://www.imsglobal.org/xsd/imscc_extensions/assignment"


def assignment_xml(assignment, identifier: str) -> str:
    description = assignment.description_html or f"<p>{escape(assignment.name)}</p>"
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<assignment xmlns="{ASSIGNMENT_NS}" identifier="{identifier}">\n'
        f"  <title>{escape(assignment.name)}</title>\n"
        f'  <text texttype="text/html">{escape(description)}</text>\n'
        f'  <gradable points_possible="{assignment.points:g}">true</gradable>\n'
        "</assignment>\n"
    )
```

Inside the `for module in course.modules:` loop in `build_cartridge_files`, after the `for item in module.items:` block, add:

```python
        if module.assignment is not None:
            ident = new_id("assignment")
            path = f"{ident}/{ident}.xml"
            content = assignment_xml(module.assignment, ident).encode("utf-8")
            resource_entries.append((ident, "assignment_xmlv1p0", path, content))
            child_items_xml.append(
                f'      <item identifier="item_{ident}" identifierref="{ident}">\n'
                f"        <title>{escape(module.assignment.name)}</title>\n"
                "      </item>\n"
            )
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd canvas_builder && python -m pytest tests/test_cartridge_writer.py -v`
Expected: PASS (7 tests)

- [ ] **Step 5: Commit**

```bash
git add canvas_builder/canvas_builder_common/cartridge_writer.py \
        canvas_builder/tests/test_cartridge_writer.py
git commit -m "canvas_builder: emit gradable CC assignment resources per module"
```

---

### Task 4: Zip packaging + CLI with structural self-check

**Files:**
- Modify: `canvas_builder/canvas_builder_common/cartridge_writer.py`
- Create: `canvas_builder/build_cartridge.py`
- Create: `canvas_builder/requirements.txt`
- Test: `canvas_builder/tests/test_build_cartridge.py`

**Interfaces:**
- Consumes: `build_cartridge_files` (Task 2/3), `load_manifest` (Task 1).
- Produces: `write_cartridge(course: CourseManifest, out_path: str) -> None`; CLI `build_cartridge.py --manifest <path> --out <path>`, exit code 0 on a structurally-matching build, exit code 1 on mismatch.

- [ ] **Step 1: Write the failing test**

Create `canvas_builder/tests/test_build_cartridge.py`:

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd canvas_builder && python -m pytest tests/test_build_cartridge.py -v`
Expected: FAIL — `canvas_builder/build_cartridge.py` does not exist yet.

- [ ] **Step 3: Write minimal implementation**

Add `write_cartridge` to the bottom of `canvas_builder/canvas_builder_common/cartridge_writer.py`:

```python
def write_cartridge(course: CourseManifest, out_path: str) -> None:
    import zipfile

    files = build_cartridge_files(course)
    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for path, content in files.items():
            zf.writestr(path, content)
```

Create `canvas_builder/build_cartridge.py`:

```python
#!/usr/bin/env python3
"""CLI: build a Canvas-importable Common Cartridge from a course manifest.

Usage:
    python build_cartridge.py --manifest ism2411_manifest.yaml --out ism2411_fa26.imscc
"""
from __future__ import annotations

import argparse
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from canvas_builder_common.cartridge_writer import write_cartridge
from canvas_builder_common.manifest_schema import load_manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, help="Path to the course manifest YAML")
    parser.add_argument("--out", required=True, help="Output .imscc path")
    args = parser.parse_args(argv)

    course = load_manifest(args.manifest)
    write_cartridge(course, args.out)

    expected_weblinks = sum(len(m.items) for m in course.modules)
    expected_assignments = sum(1 for m in course.modules if m.assignment)

    with zipfile.ZipFile(args.out) as zf:
        names = zf.namelist()
        actual_weblinks = sum(1 for n in names if n.startswith("weblinks/"))
        actual_assignments = sum(1 for n in names if n.startswith("assignment_"))

    print(f"Built {args.out}")
    print(f"  Modules:     {len(course.modules)}")
    print(f"  Weblinks:    {actual_weblinks} (expected {expected_weblinks})")
    print(f"  Assignments: {actual_assignments} (expected {expected_assignments})")

    if actual_weblinks != expected_weblinks or actual_assignments != expected_assignments:
        print("MISMATCH — cartridge contents do not match manifest. Do not import.", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
```

Create `canvas_builder/requirements.txt`:

```
PyYAML>=6.0
pytest>=8.0
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd canvas_builder && python -m pytest tests/ -v`
Expected: PASS (all tests across all three test files)

- [ ] **Step 5: Commit**

```bash
git add canvas_builder/canvas_builder_common/cartridge_writer.py \
        canvas_builder/build_cartridge.py \
        canvas_builder/requirements.txt \
        canvas_builder/tests/test_build_cartridge.py
git commit -m "canvas_builder: add CLI with structural self-check before hand-off"
```

---

### Task 5: ISM2411 real manifest, syllabus, and front page

**Files:**
- Create: `canvas_builder/ism2411_manifest.yaml`
- Create: `canvas_builder/ism2411_syllabus.html`
- Create: `canvas_builder/ism2411_front_page.html`

**Interfaces:**
- Consumes: `build_cartridge.py` (Task 4) to build and structurally validate the real cartridge.
- Produces: `canvas_builder/ism2411_fa26.imscc` (built, not committed — see `.gitignore` note in Step 3).

Content sourced from `syllabi/ism2411_simple_syllabus.md` (grading table, schedule table) and `ism2411/pages/datacamp.html` (DataCamp course list), per the design spec.

- [ ] **Step 1: Create the manifest**

Create `canvas_builder/ism2411_manifest.yaml`:

```yaml
course_code: ISM2411
course_title: "ISM2411: Python for Business"
site_base_url: https://markumreed.github.io/ism2411/

modules:
  - title: "Module 1 — What is a Computer?"
    items:
      - {label: "Reading", site_path: "pages/week01_reading.html"}
      - {label: "Lecture", site_path: "pages/week01_lecture.html"}
      - {label: "Pre-Course Setup Walkthrough", site_path: "pages/week01_lab.html"}
    # No assignment: Module 1 is orientation/setup, not a graded lab (per syllabus).

  - title: "Module 2 — The Command Line"
    items:
      - {label: "Reading", site_path: "pages/week02_reading.html"}
      - {label: "Lecture", site_path: "pages/week02_lecture.html"}
      - {label: "Lab", site_path: "pages/week02_lab.html"}
    assignment: {name: "Lab 1", group: "Weekly Labs", points: 10}

  - title: "Module 3 — Variables & First Output"
    items:
      - {label: "Reading", site_path: "pages/week03_reading.html"}
      - {label: "Lecture", site_path: "pages/week03_lecture.html"}
      - {label: "Lab", site_path: "pages/week03_lab.html"}
    assignment: {name: "Lab 2", group: "Weekly Labs", points: 10}

  - title: "Module 4 — Operators & Expressions"
    items:
      - {label: "Reading", site_path: "pages/week04_reading.html"}
      - {label: "Lecture", site_path: "pages/week04_lecture.html"}
      - {label: "Lab", site_path: "pages/week04_lab.html"}
    assignment: {name: "Lab 3", group: "Weekly Labs", points: 10}

  - title: "Module 5 — Conditionals"
    items:
      - {label: "Reading", site_path: "pages/week05_reading.html"}
      - {label: "Lecture", site_path: "pages/week05_lecture.html"}
      - {label: "Lab", site_path: "pages/week05_lab.html"}
    assignment: {name: "Lab 4", group: "Weekly Labs", points: 10}

  - title: "Module 6 — Loops"
    items:
      - {label: "Reading", site_path: "pages/week06_reading.html"}
      - {label: "Lecture", site_path: "pages/week06_lecture.html"}
      - {label: "Lab", site_path: "pages/week06_lab.html"}
    assignment: {name: "Lab 5", group: "Weekly Labs", points: 10}

  - title: "Module 7 — Functions, Debugging & AI Literacy"
    items:
      - {label: "Reading", site_path: "pages/week07_reading.html"}
      - {label: "Lecture", site_path: "pages/week07_lecture.html"}
      - {label: "Lab", site_path: "pages/week07_lab.html"}
    assignment: {name: "Lab 6", group: "Weekly Labs", points: 10}

  - title: "Module 8 — Git & GitHub"
    items:
      - {label: "Reading", site_path: "pages/week08_reading.html"}
      - {label: "Lecture", site_path: "pages/week08_lecture.html"}
      - {label: "Lab", site_path: "pages/week08_lab.html"}
    assignment: {name: "Lab 7", group: "Weekly Labs", points: 10}

  - title: "Module 9 — Midterm Exam"
    items:
      - {label: "Midterm Overview", site_path: "pages/week09_midterm.html"}
    assignment: {name: "Midterm Exam", group: "Midterm Exam", points: 100}

  - title: "Module 10 — Lists & Tuples"
    items:
      - {label: "Reading", site_path: "pages/week10_reading.html"}
      - {label: "Lecture", site_path: "pages/week10_lecture.html"}
      - {label: "Lab", site_path: "pages/week10_lab.html"}
    assignment: {name: "Lab 8", group: "Weekly Labs", points: 10}

  - title: "Module 11 — Dictionaries"
    items:
      - {label: "Reading", site_path: "pages/week11_reading.html"}
      - {label: "Lecture", site_path: "pages/week11_lecture.html"}
      - {label: "Lab", site_path: "pages/week11_lab.html"}
    assignment: {name: "Lab 9", group: "Weekly Labs", points: 10}

  - title: "Module 12 — Working with Files"
    items:
      - {label: "Reading", site_path: "pages/week12_reading.html"}
      - {label: "Lecture", site_path: "pages/week12_lecture.html"}
      - {label: "Lab", site_path: "pages/week12_lab.html"}
    assignment: {name: "Lab 10", group: "Weekly Labs", points: 10}

  - title: "Module 13 — Intro to pandas"
    items:
      - {label: "Reading", site_path: "pages/week13_reading.html"}
      - {label: "Lecture", site_path: "pages/week13_lecture.html"}
      - {label: "Lab", site_path: "pages/week13_lab.html"}
    assignment: {name: "Lab 11", group: "Weekly Labs", points: 10}

  - title: "Module 14 — Data Cleaning & Descriptive Stats"
    items:
      - {label: "Reading", site_path: "pages/week14_reading.html"}
      - {label: "Lecture", site_path: "pages/week14_lecture.html"}
      - {label: "Lab", site_path: "pages/week14_lab.html"}
    assignment: {name: "Lab 12", group: "Weekly Labs", points: 10}

  - title: "Module 15 — Grouping & Visualization"
    items:
      - {label: "Reading", site_path: "pages/week15_reading.html"}
      - {label: "Lecture", site_path: "pages/week15_lecture.html"}
      - {label: "Lab", site_path: "pages/week15_lab.html"}
    assignment: {name: "Lab 13", group: "Weekly Labs", points: 10}

  - title: "Module 16 — Capstone Project"
    items:
      - {label: "Capstone Overview", site_path: "pages/week16_capstone.html"}
      - {label: "Capstone Rubric", site_path: "pages/capstone_rubric.html"}
    assignment: {name: "Capstone Project", group: "Capstone Project", points: 100}

  # DataCamp for Classrooms — parallel track, 8 required + 2 bonus (see
  # ism2411/pages/datacamp.html). All-or-nothing completion grade; the
  # DataCamp platform itself tracks completion, so each item here is a
  # placeholder the instructor marks complete/incomplete by the due week.
  - title: "DataCamp 1 — Introduction to Python (due Week 2)"
    items: [{label: "DataCamp Tracker", site_path: "pages/datacamp.html"}]
    assignment: {name: "DataCamp: Introduction to Python", group: "DataCamp Courses", points: 0}
  - title: "DataCamp 2 — Intermediate Python (due Week 4)"
    items: [{label: "DataCamp Tracker", site_path: "pages/datacamp.html"}]
    assignment: {name: "DataCamp: Intermediate Python", group: "DataCamp Courses", points: 0}
  - title: "DataCamp 3 — Python Toolbox (due Week 6)"
    items: [{label: "DataCamp Tracker", site_path: "pages/datacamp.html"}]
    assignment: {name: "DataCamp: Python Toolbox", group: "DataCamp Courses", points: 0}
  - title: "DataCamp 4 — Writing Functions in Python (due Week 7)"
    items: [{label: "DataCamp Tracker", site_path: "pages/datacamp.html"}]
    assignment: {name: "DataCamp: Writing Functions in Python", group: "DataCamp Courses", points: 0}
  - title: "DataCamp 5 — Data Types for Data Science (due Week 10)"
    items: [{label: "DataCamp Tracker", site_path: "pages/datacamp.html"}]
    assignment: {name: "DataCamp: Data Types for Data Science", group: "DataCamp Courses", points: 0}
  - title: "DataCamp 6 — Working with Dictionaries (due Week 11)"
    items: [{label: "DataCamp Tracker", site_path: "pages/datacamp.html"}]
    assignment: {name: "DataCamp: Working with Dictionaries", group: "DataCamp Courses", points: 0}
  - title: "DataCamp 7 — Introduction to pandas (due Week 13)"
    items: [{label: "DataCamp Tracker", site_path: "pages/datacamp.html"}]
    assignment: {name: "DataCamp: Introduction to pandas", group: "DataCamp Courses", points: 0}
  - title: "DataCamp 8 — Data Manipulation with pandas (due Week 14)"
    items: [{label: "DataCamp Tracker", site_path: "pages/datacamp.html"}]
    assignment: {name: "DataCamp: Data Manipulation with pandas", group: "DataCamp Courses", points: 0}
  - title: "DataCamp Bonus — Joining Data with pandas (suggested Week 15)"
    items: [{label: "DataCamp Tracker", site_path: "pages/datacamp.html"}]
    assignment: {name: "DataCamp Bonus: Joining Data with pandas", group: "DataCamp Courses", points: 0}
  - title: "DataCamp Bonus — Intro to Data Visualization with Matplotlib (suggested Week 15)"
    items: [{label: "DataCamp Tracker", site_path: "pages/datacamp.html"}]
    assignment: {name: "DataCamp Bonus: Intro to Data Visualization with Matplotlib", group: "DataCamp Courses", points: 0}

  - title: "Participation"
    items: [{label: "Syllabus — Grading", site_path: "pages/syllabus.html"}]
    assignment: {name: "Lab Participation & Engagement", group: "Lab Participation & Engagement", points: 100}
```

> Points note: Weekly labs use 10 pts (matches the syllabus's explicit "each lab scored out of 10 points" rubric). Midterm, Capstone, and Participation use a 100-pt placeholder scaled for easy Canvas gradebook percentage math — adjust freely; the syllabus only specifies grade-category *weights* (20% / 25% / 5%), not raw point totals, so any consistent scale is correct. DataCamp assignments use 0 pts / complete-incomplete, matching the "all-or-nothing" grading described on the DataCamp Tracker page — set each to worth 10 pts (or your preferred DataCamp component scale) once you decide how it feeds the 15% category in Canvas's gradebook.

- [ ] **Step 2: Write the Syllabus and Front Page HTML**

Create `canvas_builder/ism2411_syllabus.html` (paste into Canvas Syllabus tool's HTML source view):

```html
<p><strong>ISM2411: Python for Business</strong> — USF Muma College of Business.</p>
<p>This Canvas course organizes weekly work and grades. All readings, lectures, lab instructions,
self-check quizzes, and cheat sheets live on the
<a href="https://markumreed.github.io/ism2411/" target="_blank">course website</a> — start there each week.</p>

<h3>Grading</h3>
<table border="1" cellpadding="6" cellspacing="0">
<tr><th>Component</th><th>Weight</th></tr>
<tr><td>Weekly Labs</td><td>30%</td></tr>
<tr><td>Weekly Quizzes</td><td>5%</td></tr>
<tr><td>DataCamp Courses (8 required)</td><td>15%</td></tr>
<tr><td>Midterm Exam</td><td>20%</td></tr>
<tr><td>Capstone Project</td><td>25%</td></tr>
<tr><td>Lab Participation &amp; Engagement</td><td>5%</td></tr>
</table>
<p><em>DataCamp Bonus: up to +5% extra credit for 2 optional courses.</em></p>

<h3>Full Syllabus</h3>
<p>Complete grading rubric, weekly schedule, late-work policy, generative AI policy, and all course
policies: <a href="https://markumreed.github.io/ism2411/pages/syllabus.html" target="_blank">read the full syllabus</a>.</p>
```

Create `canvas_builder/ism2411_front_page.html` (paste into Canvas Pages → set as Front Page):

```html
<h2>Welcome to ISM2411 — Python for Business</h2>
<p>This Canvas course tracks Modules, Assignments, and grades. All course content — readings, lectures,
lab instructions, self-check quizzes, and cheat sheets — lives on the course website.</p>

<ul>
  <li><a href="https://markumreed.github.io/ism2411/" target="_blank">Course Website (start here)</a></li>
  <li><a href="https://markumreed.github.io/ism2411/pages/syllabus.html" target="_blank">Full Syllabus</a></li>
  <li><a href="https://markumreed.github.io/ism2411/pages/course_map.html" target="_blank">Course Map</a></li>
  <li><a href="https://markumreed.github.io/ism2411/pages/precourse.html" target="_blank">Pre-Course Setup (complete before Module 1)</a></li>
  <li><a href="https://markumreed.github.io/ism2411/pages/datacamp.html" target="_blank">DataCamp Tracker</a></li>
</ul>

<p>Each week: read + watch the lecture on the website, attend the in-person lab, then submit that
week's Lab assignment here in Canvas by Sunday 11:59 PM.</p>
```

- [ ] **Step 3: Build and structurally validate**

Add `canvas_builder/*.imscc` to `.gitignore` (built artifacts, not source):

```bash
echo "canvas_builder/*.imscc" >> .gitignore
```

Run: `cd canvas_builder && python build_cartridge.py --manifest ism2411_manifest.yaml --out ism2411_fa26.imscc`
Expected output: `Modules: 27`, `Weblinks: 56 (expected 56)`, `Assignments: 26 (expected 26)`, exit code 0, no `MISMATCH` line.

(27 modules = 16 weekly Modules 1–16 + 10 DataCamp modules + 1 Participation module. 56 weblinks = 14 modules with 3 items each [Modules 1–8 and 10–15, since Module 1 also has 3 items] = 42, + 1 for Module 9, + 2 for Module 16, + 10 for the DataCamp modules, + 1 for Participation = 42+1+2+10+1 = 56. **If the CLI's printed count doesn't match the number in this plan, trust the CLI** — it counts the manifest and the built zip directly; this plan's arithmetic is a sanity check, not the source of truth.)

- [ ] **Step 4: Commit**

```bash
git add canvas_builder/ism2411_manifest.yaml \
        canvas_builder/ism2411_syllabus.html \
        canvas_builder/ism2411_front_page.html \
        .gitignore
git commit -m "canvas_builder: add real ISM2411 manifest, syllabus, and front page"
```

---

### Task 6: ISM3232 real manifest, syllabus, and front page

**Files:**
- Create: `canvas_builder/ism3232_manifest.yaml`
- Create: `canvas_builder/ism3232_syllabus.html`
- Create: `canvas_builder/ism3232_front_page.html`

**Interfaces:**
- Consumes: `build_cartridge.py` (Task 4).
- Produces: `canvas_builder/ism3232_fa26.imscc` (built, gitignored).

Content sourced from `syllabi/ism3232_simple_syllabus.md` (grading table, schedule table); site paths use the `docs/` prefix (matching `ism3232/docs/*.html`, not `ism3232/pages/`).

- [ ] **Step 1: Create the manifest**

Create `canvas_builder/ism3232_manifest.yaml`:

```yaml
course_code: ISM3232
course_title: "ISM3232: Business Application Development"
site_base_url: https://markumreed.github.io/ism3232/

modules:
  - title: "Unit 1 · Week 1 — Developer Mindset & Setup"
    items:
      - {label: "Reading", site_path: "docs/week01_reading.html"}
      - {label: "Lecture", site_path: "docs/week01_lecture.html"}
      - {label: "Lab", site_path: "docs/week01_lab.html"}
      - {label: "Slides", site_path: "docs/week01_slides.html"}
    assignment: {name: "Assignment 1: Setup Screenshots", group: "Weekly Assignments & Quizzes", points: 10}

  - title: "Unit 1 · Week 2 — zsh Navigation & File Ops"
    items:
      - {label: "Reading", site_path: "docs/week02_reading.html"}
      - {label: "Lecture", site_path: "docs/week02_lecture.html"}
      - {label: "Lab", site_path: "docs/week02_lab.html"}
      - {label: "Slides", site_path: "docs/week02_slides.html"}
    assignment: {name: "Assignment 2: Terminal Screenshots", group: "Weekly Assignments & Quizzes", points: 10}

  - title: "Unit 1 · Week 3 — Virtual Environments & .zshrc"
    items:
      - {label: "Reading", site_path: "docs/week03_reading.html"}
      - {label: "Lecture", site_path: "docs/week03_lecture.html"}
      - {label: "Lab", site_path: "docs/week03_lab.html"}
      - {label: "Slides", site_path: "docs/week03_slides.html"}
    assignment: {name: "Assignment 3: venv + .zshrc", group: "Weekly Assignments & Quizzes", points: 10}

  - title: "Unit 1 · Week 4 — Search, Ritual & Git"
    items:
      - {label: "Reading", site_path: "docs/week04_reading.html"}
      - {label: "Lecture", site_path: "docs/week04_lecture.html"}
      - {label: "Lab", site_path: "docs/week04_lab.html"}
      - {label: "Slides", site_path: "docs/week04_slides.html"}
    assignment: {name: "Assignment 4: Ritual + GitHub URL", group: "Weekly Assignments & Quizzes", points: 10}

  - title: "Unit 2 · Week 5 — Variables, Data Types & Operators"
    items:
      - {label: "Reading", site_path: "docs/week05_reading.html"}
      - {label: "Lecture", site_path: "docs/week05_lecture.html"}
      - {label: "Lab", site_path: "docs/week05_lab.html"}
      - {label: "Slides", site_path: "docs/week05_slides.html"}
    assignment: {name: "Assignment 5: business_data.py", group: "Weekly Assignments & Quizzes", points: 10}

  - title: "Unit 2 · Week 6 — Conditionals, Loops & Dictionaries"
    items:
      - {label: "Reading", site_path: "docs/week06_reading.html"}
      - {label: "Lecture", site_path: "docs/week06_lecture.html"}
      - {label: "Lab", site_path: "docs/week06_lab.html"}
      - {label: "Slides", site_path: "docs/week06_slides.html"}
    assignment: {name: "Assignment 6: record_processor.py", group: "Weekly Assignments & Quizzes", points: 10}

  - title: "Unit 2 · Week 7 — Functions, Modules & pytest"
    items:
      - {label: "Reading", site_path: "docs/week07_reading.html"}
      - {label: "Lecture", site_path: "docs/week07_lecture.html"}
      - {label: "Lab", site_path: "docs/week07_lab.html"}
      - {label: "Slides", site_path: "docs/week07_slides.html"}
    assignment: {name: "Assignment 7: business_rules.py", group: "Weekly Assignments & Quizzes", points: 10}

  - title: "Unit 2 · Week 8 — Debugging & AI Literacy"
    items:
      - {label: "Reading", site_path: "docs/week08_reading.html"}
      - {label: "Lecture", site_path: "docs/week08_lecture.html"}
      - {label: "Lab", site_path: "docs/week08_lab.html"}
      - {label: "Slides", site_path: "docs/week08_slides.html"}
    assignment: {name: "Assignment 8: Fixed Code + Reflection", group: "Weekly Assignments & Quizzes", points: 10}

  - title: "Unit 2 · Week 9 — Midterm Practical Exam"
    items:
      - {label: "Reading", site_path: "docs/week09_reading.html"}
      - {label: "Lecture", site_path: "docs/week09_lecture.html"}
      - {label: "Slides", site_path: "docs/week09_slides.html"}
    assignment: {name: "Midterm Practical Exam", group: "Midterm Practical Exam", points: 100}

  - title: "Unit 3 · Week 10 — OOP I: Classes & Objects"
    items:
      - {label: "Reading", site_path: "docs/week10_reading.html"}
      - {label: "Lecture", site_path: "docs/week10_lecture.html"}
      - {label: "Lab", site_path: "docs/week10_lab.html"}
      - {label: "Slides", site_path: "docs/week10_slides.html"}
    assignment: {name: "Assignment 10: models.py", group: "Weekly Assignments & Quizzes", points: 10}

  - title: "Unit 3 · Week 11 — OOP II: Composition"
    items:
      - {label: "Reading", site_path: "docs/week11_reading.html"}
      - {label: "Lecture", site_path: "docs/week11_lecture.html"}
      - {label: "Lab", site_path: "docs/week11_lab.html"}
      - {label: "Slides", site_path: "docs/week11_slides.html"}
    assignment: {name: "Assignment 11: Entity + Manager", group: "Weekly Assignments & Quizzes", points: 10}

  - title: "Unit 3 · Week 12 — OOP III: Design & Practice"
    items:
      - {label: "Reading", site_path: "docs/week12_reading.html"}
      - {label: "Lecture", site_path: "docs/week12_lecture.html"}
      - {label: "Lab", site_path: "docs/week12_lab.html"}
      - {label: "Slides", site_path: "docs/week12_slides.html"}
    assignment: {name: "Assignment 12: design.md + Models", group: "Weekly Assignments & Quizzes", points: 10}

  - title: "Unit 4 · Week 13 — Capstone Design & SQL"
    items:
      - {label: "Reading", site_path: "docs/week13_reading.html"}
      - {label: "Lecture", site_path: "docs/week13_lecture.html"}
      - {label: "Lab", site_path: "docs/week13_lab.html"}
      - {label: "Slides", site_path: "docs/week13_slides.html"}
    assignment: {name: "Capstone: Proposal + schema.sql", group: "Capstone Project", points: 25}

  - title: "Unit 4 · Week 14 — Python + SQL Integration"
    items:
      - {label: "Reading", site_path: "docs/week14_reading.html"}
      - {label: "Lecture", site_path: "docs/week14_lecture.html"}
      - {label: "Lab", site_path: "docs/week14_lab.html"}
      - {label: "Slides", site_path: "docs/week14_slides.html"}
    assignment: {name: "Capstone: database.py", group: "Capstone Project", points: 25}

  - title: "Unit 4 · Week 15 — Streamlit Interface"
    items:
      - {label: "Reading", site_path: "docs/week15_reading.html"}
      - {label: "Lecture", site_path: "docs/week15_lecture.html"}
      - {label: "Lab", site_path: "docs/week15_lab.html"}
      - {label: "Slides", site_path: "docs/week15_slides.html"}
    assignment: {name: "Capstone: app.py", group: "Capstone Project", points: 25}

  - title: "Unit 4 · Week 16 — GenAI Feature & Final Demo"
    items:
      - {label: "Reading", site_path: "docs/week16_reading.html"}
      - {label: "Lecture", site_path: "docs/week16_lecture.html"}
      - {label: "Lab", site_path: "docs/week16_lab.html"}
      - {label: "Slides", site_path: "docs/week16_slides.html"}
    assignment: {name: "Capstone: Full Repo + Live Demo", group: "Capstone Project", points: 25}

  - title: "Developer Workflow & Portfolio"
    items:
      - {label: "Syllabus — Developer Workflow Grade", site_path: "docs/syllabus.html"}
    assignment: {name: "Developer Workflow", group: "Developer Workflow", points: 100}

  - title: "Portfolio"
    items:
      - {label: "Syllabus — Portfolio Requirement", site_path: "docs/syllabus.html"}
    assignment: {name: "Portfolio", group: "Portfolio", points: 100}

  - title: "Participation"
    items:
      - {label: "Syllabus — Grading", site_path: "docs/syllabus.html"}
    assignment: {name: "Lab Participation & Engagement", group: "Lab Participation & Engagement", points: 100}
```

> Points note: same disclosed-assumption approach as ISM2411 — the syllabus specifies category *weights* only. Weekly assignments use 10 pts; the midterm, Developer Workflow, Portfolio, and Participation use 100-pt scales; the four capstone milestones use 25 pts each (summing to 100 for the Capstone Project group, matching its 30% weight being the largest single category). Adjust freely in Canvas.

- [ ] **Step 2: Write the Syllabus and Front Page HTML**

Create `canvas_builder/ism3232_syllabus.html`:

```html
<p><strong>ISM3232: Business Application Development</strong> — USF Muma College of Business.</p>
<p>This Canvas course organizes weekly work and grades. All readings, lectures, lab instructions,
slides, and cheat sheets live on the
<a href="https://markumreed.github.io/ism3232/" target="_blank">course website</a> — start there each week.</p>

<h3>Grading</h3>
<table border="1" cellpadding="6" cellspacing="0">
<tr><th>Component</th><th>Weight</th></tr>
<tr><td>Developer Workflow</td><td>15%</td></tr>
<tr><td>Weekly Assignments &amp; Quizzes</td><td>25%</td></tr>
<tr><td>Midterm Practical Exam</td><td>20%</td></tr>
<tr><td>Capstone Project</td><td>30%</td></tr>
<tr><td>Portfolio</td><td>5%</td></tr>
<tr><td>Lab Participation &amp; Engagement</td><td>5%</td></tr>
</table>
<p><em>Automation Bonus: up to +5% extra credit, details on the course website.</em></p>

<h3>Full Syllabus</h3>
<p>Complete grading rubric, weekly schedule, developer workflow ritual, generative AI policy, and all
course policies:
<a href="https://markumreed.github.io/ism3232/docs/syllabus.html" target="_blank">read the full syllabus</a>.</p>
```

Create `canvas_builder/ism3232_front_page.html`:

```html
<h2>Welcome to ISM3232 — Business Application Development</h2>
<p>This Canvas course tracks Modules, Assignments, and grades. All course content — readings, lectures,
lab instructions, slides, and cheat sheets — lives on the course website.</p>

<ul>
  <li><a href="https://markumreed.github.io/ism3232/" target="_blank">Course Website (start here)</a></li>
  <li><a href="https://markumreed.github.io/ism3232/docs/syllabus.html" target="_blank">Full Syllabus</a></li>
  <li><a href="https://markumreed.github.io/ism3232/docs/course_map.html" target="_blank">Course Map</a></li>
  <li><a href="https://markumreed.github.io/ism3232/docs/precourse.html" target="_blank">Pre-Course Setup (complete before Week 1)</a></li>
</ul>

<p>Every assignment is submitted as a GitHub URL, not a file upload. Each week: read + watch the lecture
on the website, attend the in-person lab (starting Week 2), then submit that week's assignment here in
Canvas.</p>
```

- [ ] **Step 3: Build and structurally validate**

Run: `cd canvas_builder && python build_cartridge.py --manifest ism3232_manifest.yaml --out ism3232_fa26.imscc`
Expected: exit code 0, no `MISMATCH` line — the printed `Weblinks: N (expected N)` and
`Assignments: N (expected N)` lines are the source of truth for whether it succeeded; hand-verify by eye
that `N` looks right (19 modules → 19 assignments, one per module; weblink count = sum of each module's
item list length).

- [ ] **Step 4: Commit**

```bash
git add canvas_builder/ism3232_manifest.yaml \
        canvas_builder/ism3232_syllabus.html \
        canvas_builder/ism3232_front_page.html
git commit -m "canvas_builder: add real ISM3232 manifest, syllabus, and front page"
```

---

### Task 7: README with import instructions and post-import checklist

**Files:**
- Create: `canvas_builder/README.md`

**Interfaces:**
- Consumes: nothing new — documents Tasks 1–6.
- Produces: nothing consumed by other tasks — this is the hand-off artifact for the instructor.

- [ ] **Step 1: Write the README**

Create `canvas_builder/README.md`:

```markdown
# canvas_builder

Builds a Canvas-importable Common Cartridge (`.imscc`) per course from a
YAML manifest — no Canvas API token required. See the design spec
(`docs/superpowers/specs/2026-08-18-canvas-course-build-design.md`) and
implementation plan
(`docs/superpowers/plans/2026-08-18-canvas-course-build.md`) for the full
rationale.

## Build

```bash
cd canvas_builder
pip install -r requirements.txt
python build_cartridge.py --manifest ism2411_manifest.yaml --out ism2411_fa26.imscc
python build_cartridge.py --manifest ism3232_manifest.yaml --out ism3232_fa26.imscc
```

Each run prints the module/weblink/assignment counts it built and exits
non-zero with a `MISMATCH` message if the cartridge doesn't structurally
match the manifest — **do not import a cartridge that printed MISMATCH.**

## Import into Canvas

**Import into a Canvas sandbox/test course first**, not the live ISM2411 or
ISM3232 course, the first time you do this — this cartridge format
(`imswl_xmlv1p3` weblinks + `assignment_xmlv1p0` CC assignments) is a
documented IMS Common Cartridge standard, not Canvas's own proprietary
export format, so it hasn't been round-tripped through a live Canvas import
during development. Confirm Modules, Assignments, and points land correctly
before importing into the real course.

1. In Canvas: **Settings → Import Course Content**
2. Content Type: **Common Cartridge 1.x Package**
3. Choose the `.imscc` file, select **All content**, click **Import**
4. Wait for the import job to finish (Current Jobs list on the same page)
5. Check **Modules** — every module and item from the manifest should appear
6. Check **Assignments** — every assignment should exist with the right name and points

## Post-import checklist (manual — a few minutes per course)

Common Cartridge import doesn't carry Canvas's Assignment Groups, Syllabus
body, Front Page, or Navigation settings (see "Deviations from the spec" in
the implementation plan for why) — finish these by hand:

1. **Assignment Groups** — Settings → Assignments → **+ Group**, create one
   group per distinct `group:` value in the manifest (e.g. "Weekly Labs",
   "Midterm Exam", "Capstone Project" for ISM2411), then drag each imported
   assignment into its matching group. Set each group's weight from the
   syllabus grading table, then enable **weighted grading** in the
   Assignments page settings.
2. **Syllabus** — Course → Syllabus → **Edit**, switch to the HTML source
   view (`</>` icon), paste the contents of `ism2411_syllabus.html` (or
   `ism3232_syllabus.html`), save.
3. **Front Page** — Course → Pages → **+ Page**, name it "Home", switch to
   HTML source view, paste the contents of `ism2411_front_page.html` (or
   `ism3232_front_page.html`), save, then Pages → **⋮ → Use as Front Page**.
   Finally, Course → Settings → **Choose Home Page → Front Page**.
4. **Navigation cleanup** — Course → Settings → **Navigation** tab, drag
   unused items (Files, Collaborations, Discussions if unused, etc.) down
   into the hidden section, save.
5. **Verify weblink URLs resolve** — spot-check a few Module items actually
   open the right page on the live site (confirms `site_base_url` in the
   manifest matches where the site is really deployed).
6. **ISM2411 only — DataCamp bonus assignments** — on the two "DataCamp
   Bonus" assignments, open Edit → check **"Do not count this assignment
   towards the final grade"**, so they add up to +5% without diluting the
   required DataCamp component's denominator.

## Known gaps (deferred, see spec's Non-goals)

- No native Canvas Quizzes (ISM2411's 14 weekly quizzes, or either course's
  First-Day-Attendance/Syllabus quiz). ISM2411 already has a QTI export
  script (`_build_qti.py`, repo root) a future pass can wire in.
- DataCamp assignments are manually marked complete/incomplete — DataCamp
  itself has no Canvas integration in this build.
```

- [ ] **Step 2: Commit**

```bash
git add canvas_builder/README.md
git commit -m "canvas_builder: add README with import steps and post-import checklist"
```

---

## Final check before hand-off

After Task 7, confirm both cartridges still build clean from a fresh checkout state (catches anything accidentally left uncommitted):

```bash
cd canvas_builder
rm -f ism2411_fa26.imscc ism3232_fa26.imscc
python build_cartridge.py --manifest ism2411_manifest.yaml --out ism2411_fa26.imscc
python build_cartridge.py --manifest ism3232_manifest.yaml --out ism3232_fa26.imscc
python -m pytest tests/ -v
```

All tests pass, both builds exit 0 with no `MISMATCH`. Hand `ism2411_fa26.imscc` and
`ism3232_fa26.imscc`, plus the four syllabus/front-page HTML files, to the instructor per
`canvas_builder/README.md`.
