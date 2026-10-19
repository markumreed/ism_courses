"""Wire the rebuilt Week 14 into the rest of the ISM3232 site (Phase 4a plan,
Task 8).

Every replacement states how many times it must match. The script checks all
counts first and writes nothing unless every count is right. Pages that
builders make (Weeks 12 to 14) are not touched here: their strip comes from
pagekit.STRIP and Week 13's next link from week13_common.NEXT.

    python reference/ism3232/builders/wire_week14.py          # check only
    python reference/ism3232/builders/wire_week14.py --write  # apply
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SITE = ROOT / "ism3232"
DOCS = SITE / "docs"
NEW_TITLE = "Database Tools — sqlite3, Placeholders &amp; Tested Tools"
BUILT = ("week12_", "week13_", "week14_")

STRIP_OLD = '<span class="map-item">W14 Python+SQL</span>'
STRIP_NEW = '<span class="map-item">W14 DB Tools</span>'

REPLACEMENTS = [
    # (files, old, new, expected total count)
    ("strip", STRIP_OLD, STRIP_NEW, 25),
    (
        ["site.js"],
        "Module 14 · Python + SQL Integration",
        "Module 14 · " + NEW_TITLE,
        2,
    ),
    (
        ["index.html"],
        '<div class="wc-title">Python + SQL Integration</div>',
        f'<div class="wc-title">{NEW_TITLE}</div>',
        1,
    ),
    (
        ["index.html"],
        (
            "sqlite3 module. Parameterized queries to prevent injection. SELECT with JOINs. CRUD "
            "operations wrapped in clean Python functions."
        ),
        (
            "Your database becomes the agent's tools: sqlite3 from Python with ? placeholders, "
            "functions tested with tmp_path, and the Week 12 agent copied over unchanged."
        ),
        1,
    ),
    (
        [f"docs/week15_{kind}.html" for kind in ("reading", "lecture", "lab")],
        ">Week 14</span>Python + SQL Integration</span>",
        f">Week 14</span>{NEW_TITLE}</span>",
        3,
    ),
    (
        ["docs/course_guide.html"],
        '<span class="mod-title">Python + SQL Integration</span>',
        f'<span class="mod-title">{NEW_TITLE}</span>',
        1,
    ),
    (
        ["docs/course_guide.html"],
        (
            "sqlite3 module. Parameterized queries. SELECT with JOINs. CRUD operations wrapped in "
            "Python functions."
        ),
        (
            "Bayside's database.py and tools.py: sqlite3 from Python, ? placeholders, rows as "
            "dicts, tmp_path tests, and tools over database functions; the Week 12 agent copied "
            "over unchanged."
        ),
        1,
    ),
    (
        ["docs/course_guide.html"],
        (
            '<span class="mt">Python + SQL Integration</span><span class="ms">Afternoon — '
            "parameterized queries, JOINs, CRUD Python functions</span>"
        ),
        (
            f'<span class="mt">{NEW_TITLE}</span><span class="ms">Afternoon — sqlite3 from '
            "Python, ? placeholders, database tools</span>"
        ),
        1,
    ),
    (
        ["docs/course_guide.html"],
        (
            '<span class="mt">Python + SQL Integration</span><span class="ms">Session 3 — '
            "parameterized queries, JOINs, CRUD functions</span>"
        ),
        (
            f'<span class="mt">{NEW_TITLE}</span><span class="ms">Session 3 — database.py, '
            "placeholders, tools over the database, tmp_path tests</span>"
        ),
        1,
    ),
    (
        ["docs/course_guide.html"],
        (
            '<span class="mt">Python + SQL Integration</span><span class="ms">Parameterized '
            "queries; JOINs; CRUD wrapped in Python functions</span>"
        ),
        (
            f'<span class="mt">{NEW_TITLE}</span><span class="ms">sqlite3 and ? placeholders; '
            "database.py and tools.py; tmp_path tests</span>"
        ),
        1,
    ),
    (
        ["docs/course_guide.html"],
        (
            "<p>Weeks 12 and 13 have been rebuilt as well (see below). Week 13 starts the agent "
            "capstone with a proposal, a starter business, and the new capstone rubric; Weeks 14 "
            "to 16 are being rebuilt in the same direction, toward a chat page and a staff "
            "dashboard."
        ),
        (
            "<p>Weeks 12 to 14 have been rebuilt as well (see below). Week 13 starts the agent "
            "capstone with a proposal, a starter business, and the new capstone rubric; Week 14 "
            "turns its database into the agent's tools; Weeks 15 and 16 are being rebuilt in the "
            "same direction, toward a chat page and a staff dashboard."
        ),
        1,
    ),
    (
        ["docs/syllabus.html"],
        (
            '      <td style="font-weight:600;">Python + SQL Integration</td>\n'
            '      <td style="font-size:12px;color:var(--muted);">sqlite3 · ? placeholders · '
            "row_factory · tmp_path</td>\n"
            '      <td style="font-size:12px;font-family:var(--mono);color:var(--muted);">Capstone: '
            "database.py</td>"
        ),
        (
            '      <td style="font-weight:600;">Database Tools</td>\n'
            '      <td style="font-size:12px;color:var(--muted);">sqlite3 · ? placeholders · rows as '
            "dicts · tmp_path · tools over the database</td>\n"
            '      <td style="font-size:12px;font-family:var(--mono);color:var(--muted);">Lab 14: '
            "database.py + tools.py + 12 tests</td>"
        ),
        1,
    ),
    (
        ["docs/slos.html"],
        'vertical-align:top;">Python + SQL Integration</td>',
        'vertical-align:top;">Database Tools</td>',
        1,
    ),
    (
        ["docs/slos.html"],
        (
            "Implement all five database functions using the context manager pattern and ? "
            "placeholders exclusively; apply row_factory for dict-based results; write all "
            "database tests using tmp_path for isolation."
        ),
        (
            "Query SQLite from Python with ? placeholders and rows as dicts; write database "
            "functions tested with tmp_path; build the agent's tools on those functions with the "
            "Week 12 checks; connect the unchanged agent and run it against your own database."
        ),
        1,
    ),
    (
        ["docs/slo_mindmap.html"],
        "tooltip_title:'Week 14 — Python + SQL Integration',",
        "tooltip_title:'Week 14 — Database Tools',",
        1,
    ),
    (
        ["docs/slo_mindmap.html"],
        (
            "tooltip_body:'Implement all five database functions using ? placeholders; apply "
            "row_factory; write tmp_path tests.'}"
        ),
        (
            "tooltip_body:'Query SQLite with ? placeholders; test database functions with "
            "tmp_path; turn them into tools for the agent.'}"
        ),
        1,
    ),
    (
        ["docs/unit_4_overview.html", "docs/unit_4_cheatsheet.html"],
        'Week 13 is new: <a href="week13_reading.html">Agent Design &amp; SQL</a>, with the',
        (
            'Weeks 13 and 14 are new: <a href="week13_reading.html">Agent Design &amp; SQL</a> '
            'and <a href="week14_reading.html">Database Tools</a>, with the'
        ),
        2,
    ),
    (
        ["docs/unit_4_overview.html", "docs/unit_4_cheatsheet.html"],
        "The rest of this page, and Weeks 14 to 16, still describe",
        "The rest of this page, and Weeks 15 and 16, still describe",
        2,
    ),
    (
        ["../_build_qti.py"],
        '    14: "Python + SQL Integration",',
        '    14: "Database Tools — sqlite3, Placeholders & Tested Tools",',
        1,
    ),
]


def files_for(spec):
    if spec == "strip":
        pages = [SITE / "index.html", *sorted(DOCS.glob("*.html"))]
        return [p for p in pages if not p.name.startswith(BUILT)]
    return [(SITE / name).resolve() for name in spec]


def main(write):
    plan = []
    ok = True
    for spec, old, new, expected in REPLACEMENTS:
        files = files_for(spec)
        found = {path: path.read_text().count(old) for path in files}
        total = sum(found.values())
        status = "ok" if total == expected else "COUNT MISMATCH"
        ok = ok and total == expected
        print(f"{status:>14}  {total:>2}/{expected:<2}  {old[:70]!r}")
        plan.append((old, new, [p for p, n in found.items() if n]))
    if not ok:
        print("Nothing written.")
        return 1
    if write:
        changed = set()
        for old, new, paths in plan:
            for path in paths:
                path.write_text(path.read_text().replace(old, new))
                changed.add(path)
        print(f"Wrote {len(changed)} files.")
    return 0


if __name__ == "__main__":
    sys.exit(main("--write" in sys.argv))
