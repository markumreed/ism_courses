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
