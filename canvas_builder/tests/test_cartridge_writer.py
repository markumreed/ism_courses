import xml.etree.ElementTree as ET

from canvas_builder_common.cartridge_writer import build_cartridge_files
from canvas_builder_common.manifest_schema import (
    AssignmentSpec,
    CourseManifest,
    ModuleItem,
    ModuleSpec,
)

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


def test_default_description_links_to_first_module_item():
    files = build_cartridge_files(_course_with_assignment())
    root = ET.fromstring(files["imsmanifest.xml"])
    resources = root.findall("cc:resources/cc:resource", NS)
    href = next(r.get("href") for r in resources if r.get("type") == "assignment_xmlv1p0")
    content = files[href]

    # Not just a bare title restatement...
    assert content.count(b"Lab 1") >= 1
    # ...it links out to the module's first item on the course website.
    assert b"&lt;a href=" in content
    assert b"https://example.github.io/ism9999/pages/week02_lab.html" in content


def test_explicit_description_html_is_used_verbatim():
    course = CourseManifest(
        course_code="ISM9999",
        course_title="Test Course",
        site_base_url="https://example.github.io/ism9999",
        modules=[
            ModuleSpec(
                title="Module 2",
                items=[ModuleItem(label="Lab", site_path="pages/week02_lab.html")],
                assignment=AssignmentSpec(
                    name="Lab 1",
                    group="Weekly Labs",
                    points=10,
                    description_html="<p>Custom instructions.</p>",
                ),
            ),
        ],
    )
    files = build_cartridge_files(course)
    root = ET.fromstring(files["imsmanifest.xml"])
    resources = root.findall("cc:resources/cc:resource", NS)
    href = next(r.get("href") for r in resources if r.get("type") == "assignment_xmlv1p0")
    content = files[href]
    assert b"&lt;p&gt;Custom instructions.&lt;/p&gt;" in content
    assert b"&lt;a href=" not in content


def test_bare_title_fallback_when_module_has_no_items():
    course = CourseManifest(
        course_code="ISM9999",
        course_title="Test Course",
        site_base_url="https://example.github.io/ism9999",
        modules=[
            ModuleSpec(
                title="Module 2",
                items=[],
                assignment=AssignmentSpec(name="Lab 1", group="Weekly Labs", points=10),
            ),
        ],
    )
    files = build_cartridge_files(course)
    root = ET.fromstring(files["imsmanifest.xml"])
    resources = root.findall("cc:resources/cc:resource", NS)
    href = next(r.get("href") for r in resources if r.get("type") == "assignment_xmlv1p0")
    content = files[href]
    assert b"&lt;p&gt;Lab 1&lt;/p&gt;" in content
    assert b"&lt;a href=" not in content


def test_ids_are_deterministic_across_builds():
    course = _course_with_assignment()
    files_a = build_cartridge_files(course)
    files_b = build_cartridge_files(_course_with_assignment())
    assert files_a["imsmanifest.xml"] == files_b["imsmanifest.xml"]
    assert sorted(files_a.keys()) == sorted(files_b.keys())
