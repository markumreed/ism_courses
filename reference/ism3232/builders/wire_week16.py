"""Wire the rebuilt Week 16 into the rest of the ISM3232 site (Phase 4c plan,
Task 10).

Every replacement states how many times it must match. The script checks all
counts first and writes nothing unless every count is right. A replacement whose
old text is gone and whose new text is in place counts as applied, so the script
can be run again after entries are added. Pages that
builders make (Weeks 12 to 16) are not touched here: their strip comes from
pagekit.STRIP and Week 15's next link from week15_common.NEXT.

    python reference/ism3232/builders/wire_week16.py          # check only
    python reference/ism3232/builders/wire_week16.py --write  # apply
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SITE = ROOT / "ism3232"
DOCS = SITE / "docs"
NEW_TITLE = (
    "Evaluation, Safety &amp; Demo — Test Cases, Safety Checks &amp; a Demo Video"
)
SHORT = "Evaluation, Safety &amp; Demo"
BUILT = ("week12_", "week13_", "week14_", "week15_", "week16_")

STRIP_OLD = '<span class="map-item">W16 GenAI+Demo</span>'
STRIP_NEW = '<span class="map-item">W16 Eval+Demo</span>'

BANNER_OLD = (
    'and <a href="week15_reading.html">Streamlit Chat &amp; Staff</a>, with the '
    '<a href="capstone_starters.html">capstone starters</a> and the new '
    '<a href="capstone_rubric.html">capstone rubric</a>. The rest of this page, and Week '
    "16, still describe the earlier version and will be replaced as each week is released."
)
BANNER_NEW = (
    ', <a href="week15_reading.html">Streamlit Chat &amp; Staff</a> and '
    f'<a href="week16_reading.html">{SHORT}</a>, with the '
    '<a href="capstone_starters.html">capstone starters</a> and the new '
    '<a href="capstone_rubric.html">capstone rubric</a>. The rest of this page still '
    "describes the earlier version and will be replaced."
)

REPLACEMENTS = [
    # (files, old, new, expected total count)
    ("strip", STRIP_OLD, STRIP_NEW, 21),
    (
        ["site.js"],
        "Module 16 · GenAI Feature &amp; Final Demo",
        "Module 16 · " + NEW_TITLE,
        2,
    ),
    (
        ["index.html"],
        '<div class="wc-title">GenAI Feature &amp; Final Demo</div>',
        f'<div class="wc-title">{NEW_TITLE}</div>',
        1,
    ),
    (
        ["index.html"],
        (
            "Anthropic API integration. Add a controlled AI feature to your business app. "
            "Final demo day — 5-minute live presentations and course retrospective."
        ),
        (
            "Measure the agent: named test cases, checks tested without a model, three real "
            "runs each, a safety checklist, the final README, and a Public YouTube demo "
            "video."
        ),
        1,
    ),
    (
        ["docs/course_guide.html"],
        '<span class="mod-title">GenAI Feature &amp; Final Demo</span>',
        f'<span class="mod-title">{NEW_TITLE}</span>',
        1,
    ),
    (
        ["docs/course_guide.html"],
        (
            '<span class="mt">GenAI Feature &amp; Final Demo</span><span class="ms">Afternoon '
            "— Anthropic API integration; 3-min presentations at end of day</span>"
        ),
        (
            f'<span class="mt">{SHORT}</span><span class="ms">Afternoon — cases.py, tested '
            "checks, evaluation run and safety checklist; demo videos recorded after "
            "class</span>"
        ),
        1,
    ),
    (
        ["docs/course_guide.html"],
        "Week 9 — GenAI Feature &amp; Demo (W16)",
        f"Week 9 — {SHORT} (W16)",
        1,
    ),
    (
        ["docs/course_guide.html"],
        (
            '<span class="mt">GenAI Feature &amp; Final Demo</span><span class="ms">Mon–Wed: '
            "Anthropic API integration; Thu–Fri: 5-minute presentations (or async video)</span>"
        ),
        (
            f'<span class="mt">{SHORT}</span><span class="ms">Mon–Wed: cases, tested checks '
            "and the evaluation run; Thu–Fri: safety checklist, README and the demo "
            "video</span>"
        ),
        1,
    ),
    (
        ["docs/course_guide.html"],
        (
            '<span class="mt">GenAI Feature &amp; Final Demo</span><span class="ms">Anthropic '
            "API; controlled AI feature; 5-min presentations; course retrospective</span>"
        ),
        (
            f'<span class="mt">{SHORT}</span><span class="ms">Test cases and checks; three '
            "real runs; safety checklist; final README; Public demo video</span>"
        ),
        1,
    ),
    (
        ["docs/course_guide.html"],
        (
            "Weeks 12 to 15 have been rebuilt as well (see below). Week 13 starts the agent "
            "capstone with a proposal, a starter business, and the new capstone rubric; Week "
            "14 turns its database into the agent's tools; Week 15 puts a Chat tab and a "
            "Staff tab in front of them; Week 16 is being rebuilt in the same direction."
        ),
        (
            "Weeks 12 to 16 have been rebuilt as well (see below). Week 13 starts the agent "
            "capstone with a proposal, a starter business, and the new capstone rubric; Week "
            "14 turns its database into the agent's tools; Week 15 puts a Chat tab and a "
            "Staff tab in front of them; Week 16 measures the agent with test cases and a "
            "safety checklist, and the demo is a recorded video."
        ),
        1,
    ),
    (
        ["docs/syllabus.html"],
        '<td style="font-weight:600;">GenAI Feature &amp; Final Demo</td>',
        f'<td style="font-weight:600;">{SHORT}</td>',
        1,
    ),
    (
        ["docs/syllabus.html"],
        "6 controls · ai_feature.py · repo polish · live demo",
        "cases.py · tested checks · safety checklist · demo video",
        1,
    ),
    (
        ["docs/syllabus.html"],
        "Capstone: full repo + demo</td>",
        "Capstone: full repo + demo video</td>",
        1,
    ),
    (
        ["docs/syllabus.html"],
        "Proposal + OOP + Database + Streamlit + GenAI + live demo.",
        "Proposal + database + tools + agent + Streamlit + evaluation + demo video.",
        1,
    ),
    (
        ["docs/syllabus.html"],
        (
            "Final demonstrations via video conferencing if in-person is not possible. "
            "Requirements (live working application, eight topics) remain unchanged."
        ),
        (
            "The final demonstration is a recorded video (face and screen, about 5 minutes, "
            "at most 8), published as Public on YouTube and linked from the capstone README, "
            "so it does not change."
        ),
        1,
    ),
    (
        ["docs/syllabus.html"],
        (
            '<td><strong>Anthropic API Docs</strong></td><td style="font-family:var(--mono);'
            'font-size:12px;color:var(--muted);">docs.anthropic.com</td><td style="font-size:'
            '13px;color:var(--muted);">Required for Week 16. Review the Messages API section.'
            "</td>"
        ),
        (
            '<td><strong>Ollama Docs</strong></td><td style="font-family:var(--mono);'
            'font-size:12px;color:var(--muted);">docs.ollama.com</td><td style="font-size:'
            '13px;color:var(--muted);">The local model used in Weeks 11 to 16: installing '
            "Ollama and pulling a model.</td>"
        ),
        1,
    ),
    (
        ["docs/slos.html"],
        'vertical-align:top;">GenAI Feature &amp; Final Demo</td>',
        f'vertical-align:top;">{SHORT}</td>',
        1,
    ),
    (
        ["docs/slos.html"],
        (
            "Implement all six GenAI controls (disclosure, review gate, no PII, mocked tests, "
            "specific limitations, can explain); deliver the eight required presentation "
            "topics with a live working demo."
        ),
        (
            "Write evaluation cases and test their checks without a model; run each case "
            "three times and report the pass count; run a safety checklist and write "
            "specific limitations; publish a Public demo video linked from the README."
        ),
        1,
    ),
    (
        ["docs/slo_mindmap.html"],
        "{id:'w16',label:'W16',sublabel:'GenAI',",
        "{id:'w16',label:'W16',sublabel:'Eval',",
        1,
    ),
    (
        ["docs/slo_mindmap.html"],
        "tooltip_title:'Week 16 — GenAI Feature & Final Demo',",
        "tooltip_title:'Week 16 — Evaluation, Safety & Demo',",
        1,
    ),
    (
        ["docs/slo_mindmap.html"],
        (
            "tooltip_body:'Implement all six GenAI controls; deliver the eight required "
            "presentation topics with a live working demo.'},"
        ),
        (
            "tooltip_body:'Test cases with tested checks, three real runs each, a safety "
            "checklist, specific limitations, and a Public demo video.'},"
        ),
        1,
    ),
    (
        ["docs/unit_4_overview.html", "docs/unit_4_cheatsheet.html"],
        "Weeks 13 to 15 are new: ",
        "Weeks 13 to 16 are new: ",
        2,
    ),
    (
        ["docs/unit_4_overview.html", "docs/unit_4_cheatsheet.html"],
        BANNER_OLD,
        BANNER_NEW,
        2,
    ),
    # Added by the final-review fix pass: Week 16's old content in the syllabus
    # (AI policy, tech stack) and the course guide's Week 16 topics.
    (
        ["docs/syllabus.html"],
        "<li>Week 16 only: use the Anthropic API as a controlled application feature</li>",
        (
            "<li>Weeks 11 to 16: your app calls a local model (Ollama) as part of the "
            "program; that is course content, not AI help with your code</li>"
        ),
        1,
    ),
    (
        ["docs/syllabus.html"],
        (
            '<strong style="font-family:var(--mono);font-size:13px;">Anthropic API</strong>'
            '</td><td style="font-family:var(--mono);font-size:12px;color:var(--muted);">'
            "pip install anthropic</td><td>Controlled GenAI feature in the capstone. API key "
            "required for Week 16.</td>"
        ),
        (
            '<strong style="font-family:var(--mono);font-size:13px;">Ollama</strong>'
            '</td><td style="font-family:var(--mono);font-size:12px;color:var(--muted);">'
            "pip install ollama</td><td>Runs the course model (granite4.1:3b) on your own "
            "computer in Weeks 11 to 16. No API key.</td>"
        ),
        1,
    ),
    (
        ["docs/course_guide.html"],
        (
            '<td class="mod-topics">Anthropic API integration. Controlled AI feature in your '
            "app. Final demo day: 5-minute live presentations and course retrospective.</td>"
        ),
        (
            '<td class="mod-topics">Bayside&rsquo;s cases.py and the tests for its checks, '
            "three real runs of every case, a safety checklist, specific limitations, the "
            "final README, and a Public demo video.</td>"
        ),
        1,
    ),
    (
        ["../_build_qti.py"],
        '    16: "GenAI Feature & Final Demo",',
        '    16: "Evaluation, Safety & Demo — Test Cases, Safety Checks & a Demo Video",',
        1,
    ),
]


def files_for(spec):
    if spec == "strip":
        pages = [SITE / "index.html", *sorted(DOCS.glob("*.html"))]
        return [p for p in pages if not p.name.startswith(BUILT)]
    return [(SITE / name).resolve() for name in spec]


def files_with(spec, new):
    """The files of spec that should hold new once the replacement is applied: for
    the strip, every page that carries a week strip; otherwise every named file."""
    files = files_for(spec)
    if spec == "strip":
        return [
            p
            for p in files
            if '<span class="map-item">W15 Streamlit</span>' in p.read_text()
        ]
    return files


def main(write):
    plan = []
    ok = True
    for spec, old, new, expected in REPLACEMENTS:
        files = files_for(spec)
        found = {path: path.read_text().count(old) for path in files}
        total = sum(found.values())
        applied = total == 0 and all(
            new in path.read_text() for path in files_with(spec, new)
        )
        if applied:
            print(f"{'applied':>14}  {old[:70]!r}")
            continue
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
    sys.exit(main("--write" in sys.argv[1:]))
