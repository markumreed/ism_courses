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
    due_at: str = ""  # ISO 8601 UTC timestamp, e.g. "2026-09-07T03:59:00Z"; "" = no due date


@dataclass
class ModuleSpec:
    title: str
    items: list[ModuleItem] = field(default_factory=list)
    assignments: list[AssignmentSpec] = field(default_factory=list)


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
        # Accept either a single `assignment:` mapping (most modules have at
        # most one) or a plural `assignments:` list (a module with a Lab and
        # a DataCamp course due the same week, for example) — normalize to
        # a list either way.
        raw_assignments = m.get("assignments")
        if raw_assignments is None:
            single = m.get("assignment")
            raw_assignments = [single] if single else []

        assignments = [
            AssignmentSpec(
                name=a["name"],
                group=a["group"],
                points=float(a["points"]),
                description_html=a.get("description_html", ""),
                due_at=a.get("due_at", ""),
            )
            for a in raw_assignments
        ]
        modules.append(ModuleSpec(title=m["title"], items=items, assignments=assignments))

    return CourseManifest(
        course_code=data["course_code"],
        course_title=data["course_title"],
        site_base_url=data["site_base_url"].rstrip("/"),
        modules=modules,
    )
