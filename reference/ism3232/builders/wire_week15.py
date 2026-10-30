"""Wire the rebuilt Week 15 into the rest of the ISM3232 site (Phase 4b plan,
Task 8).

Every replacement states how many times it must match. The script checks all
counts first and writes nothing unless every count is right. Pages that
builders make are not touched here: Week 14's next link comes from
week14_common.NEXT, and the week strip keeps its W15 Streamlit label.

    python reference/ism3232/builders/wire_week15.py          # check only
    python reference/ism3232/builders/wire_week15.py --write  # apply
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SITE = ROOT / "ism3232"
NEW_TITLE = "Streamlit Chat &amp; Staff — Reruns, Session State &amp; Approvals"
SHORT = "Streamlit Chat &amp; Staff"

REPLACEMENTS = [
    (["site.js"], "Module 15 · Streamlit Interface", "Module 15 · " + NEW_TITLE, 2),
    (
        ["index.html"],
        '<div class="wc-title">Streamlit Business Interface</div>',
        f'<div class="wc-title">{NEW_TITLE}</div>',
        1,
    ),
    (
        ["index.html"],
        (
            "Streamlit widgets, layout, and session state. Connect your app to SQLite. Build an "
            "interactive business dashboard that runs in a browser."
        ),
        (
            "A web page for the agent: a Chat tab for customers and a Staff tab that approves the "
            "change requests it files. Streamlit reruns, st.session_state, tabs and forms."
        ),
        1,
    ),
    (
        [f"docs/week16_{kind}.html" for kind in ("reading", "lecture", "lab")],
        ">Week 15</span>Streamlit Interface</span>",
        f">Week 15</span>{NEW_TITLE}</span>",
        3,
    ),
    (
        ["docs/course_guide.html"],
        '<span class="mod-title">Streamlit Business Interface</span>',
        f'<span class="mod-title">{NEW_TITLE}</span>',
        1,
    ),
    (
        ["docs/course_guide.html"],
        (
            "Streamlit widgets, layout, session state. Connect to SQLite. Build an interactive "
            "business dashboard in a browser."
        ),
        (
            "Bayside's app.py: Streamlit's rerun model, st.session_state, a Chat tab over the agent, "
            "and a Staff tab that approves or rejects change requests, shows a GROUP BY report, and "
            "edits the database."
        ),
        1,
    ),
    (
        ["docs/course_guide.html"],
        (
            '<span class="mt">Streamlit Business Interface</span><span class="ms">Morning — '
            "widgets, layout, session state, connect to SQLite</span>"
        ),
        (
            f'<span class="mt">{NEW_TITLE}</span><span class="ms">Morning — reruns, '
            "session_state, Chat tab, Staff approvals</span>"
        ),
        1,
    ),
    (
        ["docs/course_guide.html"],
        (
            '<span class="mt">Streamlit Business Interface</span><span class="ms">Full week — '
            "widgets, layout, session state, connect SQLite to Streamlit</span>"
        ),
        (
            f'<span class="mt">{NEW_TITLE}</span><span class="ms">Full week — reruns and '
            "session_state, a Chat tab over the agent, a Staff tab with approvals and a "
            "report</span>"
        ),
        1,
    ),
    (
        ["docs/course_guide.html"],
        (
            '<span class="mt">Streamlit Business Interface</span><span class="ms">Widgets, layout, '
            "session state; connect SQLite to Streamlit</span>"
        ),
        (
            f'<span class="mt">{NEW_TITLE}</span><span class="ms">Reruns and session_state; Chat '
            "and Staff tabs; approvals, report, edit form</span>"
        ),
        1,
    ),
    (
        ["docs/course_guide.html"],
        (
            "<p>Weeks 12 to 14 have been rebuilt as well (see below). Week 13 starts the agent "
            "capstone with a proposal, a starter business, and the new capstone rubric; Week 14 "
            "turns its database into the agent's tools; Weeks 15 and 16 are being rebuilt in the "
            "same direction, toward a chat page and a staff dashboard."
        ),
        (
            "<p>Weeks 12 to 15 have been rebuilt as well (see below). Week 13 starts the agent "
            "capstone with a proposal, a starter business, and the new capstone rubric; Week 14 "
            "turns its database into the agent's tools; Week 15 puts a Chat tab and a Staff tab in "
            "front of them; Week 16 is being rebuilt in the same direction."
        ),
        1,
    ),
    (
        ["docs/syllabus.html"],
        (
            '<td style="font-weight:600;">Streamlit Interface</td>\n'
            '      <td style="font-size:12px;color:var(--muted);">Rerun model · 5 tabs · '
            "Submit/View/Filter/Update/Report</td>\n"
            '      <td style="font-size:12px;font-family:var(--mono);color:var(--muted);">Capstone: '
            "app.py</td>"
        ),
        (
            f'<td style="font-weight:600;">{SHORT}</td>\n'
            '      <td style="font-size:12px;color:var(--muted);">Rerun model · session_state · '
            "chat_message · tabs · approve/reject</td>\n"
            '      <td style="font-size:12px;font-family:var(--mono);color:var(--muted);">Lab 15: '
            "app.py + 15 tests</td>"
        ),
        1,
    ),
    (
        ["docs/slos.html"],
        'vertical-align:top;">Streamlit Interface</td>',
        f'vertical-align:top;">{SHORT}</td>',
        1,
    ),
    (
        ["docs/slos.html"],
        (
            "Explain Streamlit&#x27;s rerun execution model; implement all five required tabs "
            "(Submit, View All, Filter, Update Status, Report) wired to the live database; call "
            "create_table() before any widget."
        ),
        (
            "Explain Streamlit&#x27;s rerun model and keep objects in st.session_state; build a Chat "
            "tab over the agent and a Staff tab that approves or rejects change requests, shows "
            "records and a GROUP BY report, and edits the database; show customer text safely."
        ),
        1,
    ),
    (
        ["docs/slo_mindmap.html"],
        "tooltip_title:'Week 15 — Streamlit Interface',",
        "tooltip_title:'Week 15 — Streamlit Chat & Staff',",
        1,
    ),
    (
        ["docs/slo_mindmap.html"],
        (
            "tooltip_body:'Explain Streamlit\\'s rerun model; implement all five required tabs "
            "wired to the live database.'}"
        ),
        (
            "tooltip_body:'Explain the rerun model; keep the agent in session_state; build Chat and "
            "Staff tabs that approve change requests.'}"
        ),
        1,
    ),
    (
        ["docs/unit_4_overview.html", "docs/unit_4_cheatsheet.html"],
        (
            'Weeks 13 and 14 are new: <a href="week13_reading.html">Agent Design &amp; SQL</a> and '
            '<a href="week14_reading.html">Database Tools</a>, with the'
        ),
        (
            'Weeks 13 to 15 are new: <a href="week13_reading.html">Agent Design &amp; SQL</a>, '
            '<a href="week14_reading.html">Database Tools</a> and '
            f'<a href="week15_reading.html">{SHORT}</a>, with the'
        ),
        2,
    ),
    (
        ["docs/unit_4_overview.html", "docs/unit_4_cheatsheet.html"],
        "The rest of this page, and Weeks 15 and 16, still describe",
        "The rest of this page, and Week 16, still describe",
        2,
    ),
    (
        ["../_build_qti.py"],
        '    15: "Streamlit Business Interface",',
        '    15: "Streamlit Chat & Staff — Reruns, Session State & Approvals",',
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
