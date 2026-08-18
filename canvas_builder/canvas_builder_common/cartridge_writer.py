"""Builds an IMS Common Cartridge 1.3 package from a CourseManifest.

Uses only standard, documented IMS Common Cartridge elements (Organizations
for Modules, Web Link resources for outbound links, CC Assignment resources
for gradable work) rather than Canvas's undocumented proprietary cartridge
extensions — see the "Deviations from the spec" note in the implementation
plan for why.
"""
from __future__ import annotations

import hashlib
from dataclasses import replace
from xml.sax.saxutils import escape

from canvas_builder_common.manifest_schema import CourseManifest

CC_NS = "http://www.imsglobal.org/xsd/imsccv1p3/imscp_v1p1"
WEBLINK_NS = "http://www.imsglobal.org/xsd/imsccv1p3/imswl_v1p3"
ASSIGNMENT_NS = "http://www.imsglobal.org/xsd/imscc_extensions/assignment"


def stable_id(prefix: str, *parts: str) -> str:
    """Deterministic identifier: same prefix + parts always yields the same id.

    Canvas's import mechanism keys re-import update-vs-duplicate behavior on
    the cartridge's resource identifiers, so identifiers must be stable
    across repeated builds of the same manifest content (see final-review
    finding #4) — unlike a random uuid4-based id, hashing the parts that
    make each element unique within the manifest reproduces the same id
    every time for the same input.
    """
    digest = hashlib.sha1("|".join(parts).encode("utf-8")).hexdigest()[:16]
    return f"{prefix}_{digest}"


def weblink_xml(title: str, url: str) -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<webLink xmlns="{WEBLINK_NS}">\n'
        f"  <title>{escape(title)}</title>\n"
        f'  <url href="{escape(url)}" target="_blank"/>\n'
        "</webLink>\n"
    )


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


def _default_description_for(course: CourseManifest, module) -> str:
    """Richer default assignment description linking to the module's first
    item on the course website, instead of a bare title restatement.

    Falls back to the bare-title description for the rare module that has
    an assignment but zero items.
    """
    if not module.items:
        return f"<p>{escape(module.assignment.name)}</p>"
    first_item = module.items[0]
    url = f"{course.site_base_url}/{first_item.site_path}"
    return (
        f"<p>{escape(module.assignment.name)}. See the assignment instructions on the "
        f'course website: <a href="{escape(url)}">{escape(module.title)}</a>.</p>'
    )


def build_cartridge_files(course: CourseManifest) -> dict[str, bytes]:
    """Returns {path-within-zip: content-bytes} for every cartridge file,
    including imsmanifest.xml."""
    resource_entries = []  # (identifier, type, path, content_bytes)
    module_items_xml = []

    for module in course.modules:
        child_items_xml = []
        for item in module.items:
            ident = stable_id("link", course.course_code, module.title, item.label)
            url = f"{course.site_base_url}/{item.site_path}"
            path = f"weblinks/{ident}.xml"
            content = weblink_xml(item.label, url).encode("utf-8")
            resource_entries.append((ident, "imswl_xmlv1p3", path, content))
            child_items_xml.append(
                f'      <item identifier="item_{ident}" identifierref="{ident}">\n'
                f"        <title>{escape(item.label)}</title>\n"
                "      </item>\n"
            )

        if module.assignment is not None:
            ident = stable_id("assignment", course.course_code, module.title)
            path = f"{ident}/{ident}.xml"
            description = module.assignment.description_html or _default_description_for(
                course, module
            )
            assignment_with_description = replace(
                module.assignment, description_html=description
            )
            content = assignment_xml(assignment_with_description, ident).encode("utf-8")
            resource_entries.append((ident, "assignment_xmlv1p0", path, content))
            child_items_xml.append(
                f'      <item identifier="item_{ident}" identifierref="{ident}">\n'
                f"        <title>{escape(module.assignment.name)}</title>\n"
                "      </item>\n"
            )

        module_id = stable_id("module", course.course_code, module.title)
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
        f'<manifest identifier="{stable_id("man", course.course_code)}" xmlns="{CC_NS}">\n'
        "  <metadata>\n"
        "    <schema>IMS Common Cartridge</schema>\n"
        "    <schemaversion>1.3.0</schemaversion>\n"
        "  </metadata>\n"
        "  <organizations>\n"
        f'    <organization identifier="{stable_id("org", course.course_code)}" structure="rooted-hierarchy">\n'
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


def write_cartridge(course: CourseManifest, out_path: str) -> None:
    import zipfile

    files = build_cartridge_files(course)
    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for path, content in files.items():
            zf.writestr(path, content)
