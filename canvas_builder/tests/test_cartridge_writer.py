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
