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
