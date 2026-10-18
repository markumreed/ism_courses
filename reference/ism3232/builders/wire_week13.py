"""Wire the rebuilt Week 13 and the two capstone pages into the rest of the
ISM3232 site (Phase 3 plan, Task 11).

Every replacement states how many times it must match. The script checks all
counts first and writes nothing unless every count is right. Week 12's pages
are not touched here: their next link comes from week12_common.NEXT.

    python reference/ism3232/builders/wire_week13.py          # check only
    python reference/ism3232/builders/wire_week13.py --write  # apply
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SITE = ROOT / "ism3232"
NEW_TITLE = "Agent Design &amp; SQL — Proposal, Schema &amp; sqlite3"

BANNER = (
    '<div style="border:1px solid rgba(251,191,36,.35);border-left:3px solid #fbbf24;'
    "border-radius:0 8px 8px 0;padding:12px 16px;margin:16px 0 24px;font-size:14px;"
    'line-height:1.65;"><strong>Unit 4 is being rebuilt around the agent capstone.</strong> '
    'Week 13 is new: <a href="week13_reading.html">Agent Design &amp; SQL</a>, with the '
    '<a href="capstone_starters.html">capstone starters</a> and the new '
    '<a href="capstone_rubric.html">capstone rubric</a>. The rest of this page, and Weeks 14 '
    "to 16, still describe the earlier version and will be replaced as each week is "
    "released.</div>"
)
DESKTOP_OLD = (
    '        <a href="${pg}unit_4_cheatsheet.html">Cheat Sheet</a>\n'
    '        <a href="${pg}week13_reading.html">Module 13 · Capstone Design &amp; SQL</a>'
)
DESKTOP_NEW = (
    '        <a href="${pg}unit_4_cheatsheet.html">Cheat Sheet</a>\n'
    '        <a href="${pg}capstone_starters.html">Capstone Starters</a>\n'
    '        <a href="${pg}capstone_rubric.html">Capstone Rubric</a>\n'
    '        <a href="${pg}week13_reading.html">Module 13 · ' + NEW_TITLE + "</a>"
)
MOBILE_OLD = (
    '\n      <a href="${pg}unit_4_cheatsheet.html">Cheat Sheet</a>\n'
    '      <a href="${pg}week13_reading.html">Module 13 · Capstone Design &amp; SQL</a>'
)
MOBILE_NEW = (
    '\n      <a href="${pg}unit_4_cheatsheet.html">Cheat Sheet</a>\n'
    '      <a href="${pg}capstone_starters.html">Capstone Starters</a>\n'
    '      <a href="${pg}capstone_rubric.html">Capstone Rubric</a>\n'
    '      <a href="${pg}week13_reading.html">Module 13 · ' + NEW_TITLE + "</a>"
)

REPLACEMENTS = [
    # (files relative to ism3232/, old, new, expected total count)
    (["site.js"], DESKTOP_OLD, DESKTOP_NEW, 1),
    (["site.js"], MOBILE_OLD, MOBILE_NEW, 1),
    (
        ["index.html"],
        (
            '      <a class="unit-link" href="docs/unit_4_overview.html">Overview</a>\n'
            '      <a class="unit-link" href="docs/capstone_rubric.html">Rubric</a>'
        ),
        (
            '      <a class="unit-link" href="docs/unit_4_overview.html">Overview</a>\n'
            '      <a class="unit-link" href="docs/capstone_starters.html">Starters</a>\n'
            '      <a class="unit-link" href="docs/capstone_rubric.html">Rubric</a>'
        ),
        1,
    ),
    (
        ["index.html"],
        '<div class="wc-title">Capstone Design &amp; SQL Foundations</div>',
        f'<div class="wc-title">{NEW_TITLE}</div>',
        1,
    ),
    (
        ["index.html"],
        (
            "Entity-Relationship diagrams. CREATE TABLE, INSERT, SELECT. SQLite from Python's "
            "sqlite3 module. Design and build your capstone database schema."
        ),
        (
            "Choose a business and write a proposal whose sections become code. Design its "
            "tables, build them in the sqlite3 shell, and get your proposal signed off."
        ),
        1,
    ),
    (
        [f"docs/week14_{kind}.html" for kind in ("reading", "lecture", "lab")],
        ">Week 13</span>Capstone Design &amp; SQL</span>",
        f">Week 13</span>{NEW_TITLE}</span>",
        3,
    ),
    (
        ["docs/course_guide.html"],
        '<span class="mod-title">Capstone Design &amp; SQL Foundations</span>',
        f'<span class="mod-title">{NEW_TITLE}</span>',
        1,
    ),
    (
        ["docs/course_guide.html"],
        (
            "Entity-Relationship diagrams. CREATE TABLE, INSERT, SELECT. SQLite from Python's "
            "sqlite3 module. Design the capstone database schema."
        ),
        (
            "Choose a starter business and write a proposal whose sections become code. Design "
            "its tables and build them in the sqlite3 shell: CREATE TABLE, INSERT, SELECT, "
            "UPDATE, GROUP BY. Instructor sign-off."
        ),
        1,
    ),
    (
        ["docs/course_guide.html"],
        (
            '<span class="mt">Capstone Design &amp; SQL Foundations</span><span class="ms">'
            "Morning — ER diagrams, CREATE TABLE, INSERT, SELECT, sqlite3</span>"
        ),
        (
            f'<span class="mt">{NEW_TITLE}</span><span class="ms">Morning — the proposal, '
            "tables from questions, the sqlite3 shell</span>"
        ),
        1,
    ),
    (
        ["docs/course_guide.html"],
        (
            '<span class="mt">Capstone Design &amp; SQL Foundations</span><span class="ms">'
            "Sessions 1–2 — ER diagrams, CREATE TABLE, INSERT, SELECT, sqlite3</span>"
        ),
        (
            f'<span class="mt">{NEW_TITLE}</span><span class="ms">Sessions 1–2 — the proposal, '
            "tables from questions, the sqlite3 shell, sign-off</span>"
        ),
        1,
    ),
    (
        ["docs/course_guide.html"],
        (
            '<span class="mt">Capstone Design &amp; SQL Foundations</span><span class="ms">'
            "ER diagrams; CREATE TABLE, INSERT, SELECT; sqlite3 module</span>"
        ),
        (
            f'<span class="mt">{NEW_TITLE}</span><span class="ms">Proposal and sign-off; '
            "CREATE TABLE, INSERT, SELECT, UPDATE, GROUP BY in the sqlite3 shell</span>"
        ),
        1,
    ),
    (
        ["docs/course_guide.html"],
        (
            "<p>Week 12 has been rebuilt as well (see below). Weeks 13 to 16 are being rebuilt "
            "in the same direction, toward an agent capstone with a chat page and a staff "
            "dashboard. Until each one is released, the rows and dependency chains in this "
            "guide that mention the Request Tracker capstone describe the earlier version.</p>"
        ),
        (
            "<p>Weeks 12 and 13 have been rebuilt as well (see below). Week 13 starts the agent "
            "capstone with a proposal, a starter business, and the new capstone rubric; Weeks "
            "14 to 16 are being rebuilt in the same direction, toward a chat page and a staff "
            "dashboard. Until each one is released, the rows and dependency chains in this "
            "guide that mention the Request Tracker capstone describe the earlier version.</p>"
        ),
        1,
    ),
    (
        ["docs/syllabus.html"],
        (
            '      <td style="font-weight:600;">Capstone Design &amp; SQL</td>\n'
            '      <td style="font-size:12px;color:var(--muted);">PROPOSAL.md · CREATE · INSERT · '
            "SELECT · UPDATE</td>\n"
            '      <td style="font-size:12px;font-family:var(--mono);color:var(--muted);">Capstone: '
            "proposal + schema.sql</td>"
        ),
        (
            '      <td style="font-weight:600;">Agent Design &amp; SQL</td>\n'
            '      <td style="font-size:12px;color:var(--muted);">starter business · PROPOSAL.md · '
            "sqlite3 shell · CREATE · INSERT · SELECT · UPDATE · GROUP BY</td>\n"
            '      <td style="font-size:12px;font-family:var(--mono);color:var(--muted);">Lab 13: '
            "PROPOSAL.md + schema.sql, signed off</td>"
        ),
        1,
    ),
    (
        ["docs/slos.html"],
        'vertical-align:top;">Capstone Design &amp; SQL Foundations</td>',
        'vertical-align:top;">Agent Design &amp; SQL</td>',
        1,
    ),
    (
        ["docs/slos.html"],
        (
            "Complete a ten-field PROPOSAL.md with specific business rules (threshold + "
            "consequence); write all five required SQL operations in the sqlite3 shell; design a "
            "schema with correct column types; commit schema.sql."
        ),
        (
            "Choose a business against the eight-item checklist; write a PROPOSAL.md whose "
            "sections map to code; design tables with types and keys; write CREATE TABLE, "
            "INSERT, SELECT, UPDATE … WHERE and GROUP BY in the sqlite3 shell; commit a "
            "schema.sql that runs twice without duplicates."
        ),
        1,
    ),
    (
        ["docs/slo_mindmap.html"],
        "tooltip_title:'Week 13 — Capstone Design & SQL Foundations',",
        "tooltip_title:'Week 13 — Agent Design & SQL',",
        1,
    ),
    (
        ["docs/slo_mindmap.html"],
        (
            "tooltip_body:'Complete PROPOSAL.md; write all five SQL operations in the sqlite3 "
            "shell; design a schema with correct column types.'}"
        ),
        (
            "tooltip_body:'Choose a business; write a proposal whose sections map to code; "
            "design tables and build them in the sqlite3 shell.'}"
        ),
        1,
    ),
    (
        ["docs/unit_4_overview.html"],
        '<span class="chip">Modules 13–16</span>\n</div>\n',
        '<span class="chip">Modules 13–16</span>\n</div>\n' + BANNER + "\n",
        1,
    ),
    (
        ["docs/unit_4_cheatsheet.html"],
        '<span class="chip">Quick reference</span>\n</div>\n',
        '<span class="chip">Quick reference</span>\n</div>\n' + BANNER + "\n",
        1,
    ),
    (
        ["../_build_qti.py"],
        '    13: "Capstone Design & SQL Foundations",',
        '    13: "Agent Design & SQL — Proposal, Schema & sqlite3",',
        1,
    ),
]


def files_for(names):
    return [(SITE / name).resolve() for name in names]


def main(write):
    plan = []
    ok = True
    for names, old, new, expected in REPLACEMENTS:
        files = files_for(names)
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
