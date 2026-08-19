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
              due_at: "2026-09-07T03:59:00Z"
          - title: "Module 4 — Operators"
            items:
              - {label: "Lab", site_path: "pages/week04_lab.html"}
            assignments:
              - {name: "Lab 3", group: "Weekly Labs", points: 10}
              - {name: "DataCamp: Intermediate Python", group: "DataCamp Courses", points: 10}
        """))

    manifest = load_manifest(str(manifest_path))

    assert manifest.course_code == "ISM9999"
    assert manifest.course_title == "Test Course"
    assert manifest.site_base_url == "https://example.github.io/ism9999"  # trailing slash stripped
    assert len(manifest.modules) == 3

    module_1 = manifest.modules[0]
    assert module_1.title == "Module 1 — Intro"
    assert len(module_1.items) == 2
    assert module_1.items[0].label == "Reading"
    assert module_1.items[0].site_path == "pages/week01_reading.html"
    assert module_1.assignments == []

    # Singular `assignment:` key normalizes to a one-item list.
    module_2 = manifest.modules[1]
    assert len(module_2.assignments) == 1
    assert module_2.assignments[0].name == "Lab 1"
    assert module_2.assignments[0].group == "Weekly Labs"
    assert module_2.assignments[0].points == 10
    assert module_2.assignments[0].description_html == ""
    assert module_2.assignments[0].due_at == "2026-09-07T03:59:00Z"

    # Plural `assignments:` key supports more than one per module.
    module_3 = manifest.modules[2]
    assert [a.name for a in module_3.assignments] == ["Lab 3", "DataCamp: Intermediate Python"]
    assert module_3.assignments[1].group == "DataCamp Courses"
    assert module_3.assignments[1].due_at == ""
