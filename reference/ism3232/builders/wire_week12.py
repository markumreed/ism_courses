"""Wire the rebuilt Week 12 into the rest of the ISM3232 site (plan Task 8).

Every replacement states how many times it must match. The script checks all
counts first and writes nothing unless every count is right.

    python reference/ism3232/builders/wire_week12.py          # check only
    python reference/ism3232/builders/wire_week12.py --write  # apply
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SITE = ROOT / "ism3232"
DOCS = SITE / "docs"
NEW_TITLE = "Tools and Guardrails — Model-Chosen Tools, Checks &amp; Approval"

WEEK12_CALLOUT = """<div class="callout teal">
<div class="callout-title">Week 12 was rebuilt in Fall 2026: Tools and Guardrails</div>
<p>Week 12 lets the model choose when to use a tool. Tools are methods on the Week 10 tool objects, described by their docstrings; the model returns either a reply or a tool request, and the chatbot runs a loop of at most three rounds. Every request passes one <code>Toolbox</code>, which refuses unknown tools, empty values, and order IDs or addresses the customer never typed. An address change no longer ends in a handoff: the chatbot files a request in a <code>ChangeQueue</code>, and only a staff approval changes the order. The payment handoff stays a keyword rule, so <em>gift cards</em> still go to a person on purpose.</p>
<p><strong>Essential:</strong> tool calls and docstrings, the new <code>decide</code> method beside <code>reply</code>, the tool loop and its limit, the <code>tool</code> history entry, the Toolbox checks, the change queue, and tests with <code>FakeModel</code>. <strong>Optional enrichment:</strong> why Ollama needs the model's own request (<code>tool_messages</code>), turning a guardrail off to watch (Exercise 3), and a fallback model for when Ollama is down (Exercise 4). <strong>Left out on purpose:</strong> several tool calls at once, streaming, online services, signing customers in, and data that lasts (Week 13).</p>
<p><strong>What the real runs showed:</strong> with the customer-said check off, the model invented an order and an address and filed the change in five out of five runs; with it on, every one was refused and the model asked the customer. The false closing time from Week 11 is still repeated: no tool knows the hours. <strong>Laptops that cannot run the model:</strong> Parts 2 to 5, the tests and Exercises 1, 2 and 4 need nothing but Python and are what is graded.</p>
<p><strong>Misconceptions to listen for:</strong> the model runs the tool; a good docstring makes the model safe; any request for an existing tool is fine. <strong>Teaching material:</strong> timing, discussion questions and speaker notes are on the Week 12 lecture page and in the lab slides. Every model output on the Week 12 pages is a saved real run, and wording on student screens will differ.</p>
</div>"""

REPLACEMENTS = [
    # (files, old, new, expected total count)
    ("strip", '<span class="map-item">W12 OOP III</span>', '<span class="map-item">W12 Tools+Guardrails</span>', 29),
    (
        ["site.js"],
        "Module 12 · OOP III — Design &amp; Practice",
        f"Module 12 · {NEW_TITLE}",
        2,
    ),
    (
        [f"docs/week1{n}_{kind}.html" for n in (1, 3) for kind in ("reading", "lecture", "lab")],
        ">Week 12</span>OOP III — Design &amp; Practice</span>",
        f">Week 12</span>{NEW_TITLE}</span>",
        6,
    ),
    (
        ["index.html"],
        '<div class="wc-title">OOP III — Applied Practice &amp; Design</div>',
        f'<div class="wc-title">{NEW_TITLE}</div>',
        1,
    ),
    (
        ["index.html"],
        "Design patterns in practice. A complete OOP mini-project: model a business domain end-to-end. "
        "Code review session and capstone schema planning.",
        "The model chooses when to use a tool. Every request passes one checked door, made-up details are "
        "refused, and address changes wait for staff approval. Tests use a scripted fake model.",
        1,
    ),
    (
        ["docs/course_guide.html"],
        '<span class="mod-title">OOP III — Applied Practice &amp; Design</span>',
        f'<span class="mod-title">{NEW_TITLE}</span>',
        1,
    ),
    (
        ["docs/course_guide.html"],
        "Design patterns in practice. A complete OOP mini-project: model a business domain end-to-end. "
        "Code review and capstone planning.",
        "The model chooses tools. One checked door for every request, made-up details refused, and an "
        "approval queue for changes. Tests with a fake model.",
        1,
    ),
    (
        ["docs/course_guide.html"],
        '<span class="mt">OOP III — Applied Practice</span><span class="ms">Evening or next morning — '
        "end-to-end mini-project, capstone schema design</span>",
        f'<span class="mt">{NEW_TITLE}</span><span class="ms">Evening or next morning — tool calls, '
        "the Toolbox checks, the approval queue</span>",
        1,
    ),
    (
        ["docs/course_guide.html"],
        '<div class="unit-label" style="color:var(--u3);">Week 6 — OOP Applied (W12)</div>',
        '<div class="unit-label" style="color:var(--u3);">Week 6 — Tools and Guardrails (W12)</div>',
        1,
    ),
    (
        ["docs/course_guide.html"],
        '<span class="mt">OOP III — Applied Practice &amp; Design</span><span class="ms">Full week — '
        "end-to-end OOP mini-project + capstone database schema planning</span>",
        f'<span class="mt">{NEW_TITLE}</span><span class="ms">Full week — tool calls, guardrails, an '
        "approval queue, and tests with a fake model</span>",
        1,
    ),
    (
        ["docs/course_guide.html"],
        '<span class="mt">OOP III — Applied Practice &amp; Design</span><span class="ms">End-to-end OOP '
        "mini-project; code review; capstone planning</span>",
        f'<span class="mt">{NEW_TITLE}</span><span class="ms">Model-chosen tools; the Toolbox checks; '
        "the approval queue; FakeModel tests</span>",
        1,
    ),
    (
        ["docs/course_guide.html"],
        "<p>Weeks 12 to 16 are being rebuilt in the same direction (tools and guardrails, then an agent "
        "capstone). Until each one is released, the rows and dependency chains in this guide that mention "
        "OOP III and the Request Tracker capstone describe the earlier version.</p>",
        "<p>Week 12 has been rebuilt as well (see below). Weeks 13 to 16 are being rebuilt in the same "
        "direction, toward an agent capstone with a chat page and a staff dashboard. Until each one is "
        "released, the rows and dependency chains in this guide that mention the Request Tracker capstone "
        "describe the earlier version.</p>",
        1,
    ),
    (
        ["docs/course_guide.html"],
        "Every model output shown on the Week 11 pages is one real run, and wording on student screens will "
        "differ.</p>\n</div>\n",
        "Every model output shown on the Week 11 pages is one real run, and wording on student screens will "
        "differ.</p>\n</div>\n\n" + WEEK12_CALLOUT + "\n",
        1,
    ),
    (
        ["docs/syllabus.html"],
        '<td style="font-weight:600;">OOP III — Design &amp; Practice</td>\n'
        '      <td style="font-size:12px;color:var(--muted);">design.md first · 2 entities · 1 manager · 6 tests</td>\n'
        '      <td style="font-size:12px;font-family:var(--mono);color:var(--muted);">Assignment 12: design.md + models</td>',
        '<td style="font-weight:600;">Tools and Guardrails</td>\n'
        '      <td style="font-size:12px;color:var(--muted);">model-chosen tools · Toolbox checks · approval queue · FakeModel tests</td>\n'
        '      <td style="font-size:12px;font-family:var(--mono);color:var(--muted);">Assignment 12: toolbox + approval queue</td>',
        1,
    ),
    (
        ["docs/slos.html"],
        'vertical-align:top;">OOP III — Applied Practice</td>',
        'vertical-align:top;">Tools and Guardrails</td>',
        1,
    ),
    (
        ["docs/slos.html"],
        "Write design.md before any class code and commit it first; implement two entity classes and one "
        "manager; pass all six required test types including the instance independence test; identify all "
        "four common OOP mistakes.",
        "Explain a tool call and describe a tool with a docstring; trace the tool loop and its limit; check "
        "every tool request in one place and refuse details the customer never gave; make a change wait for "
        "approval and apply it once; test the loop with a fake model.",
        1,
    ),
    (
        ["docs/slo_mindmap.html"],
        "{id:'w12',label:'W12',sublabel:'Design',",
        "{id:'w12',label:'W12',sublabel:'Tools',",
        1,
    ),
    (
        ["docs/slo_mindmap.html"],
        "tooltip_title:'Week 12 — OOP III: Applied Practice',\n"
        "              tooltip_body:'Write design.md before any code; implement two entity classes and one manager; "
        "pass all six test types.'}",
        "tooltip_title:'Week 12 — Tools and Guardrails',\n"
        "              tooltip_body:'Let the model choose tools; check every request in one Toolbox; make changes "
        "wait for approval; test with a fake model.'}",
        1,
    ),
    (
        ["docs/unit_3_overview.html", "docs/unit_3_cheatsheet.html"],
        'Weeks 10 and 11 are new: <a href="week10_reading.html">OOP for Agents</a> and '
        '<a href="week11_reading.html">Talking to a Local Model</a>. The rest of this page still describes '
        "the earlier Weeks 10 to 12 and will be replaced when Week 12 is released. For Weeks 10 and 11, use "
        "the weekly pages.",
        'Weeks 10 to 12 are new: <a href="week10_reading.html">OOP for Agents</a>, '
        '<a href="week11_reading.html">Talking to a Local Model</a>, and '
        '<a href="week12_reading.html">Tools and Guardrails</a>. The rest of this page still describes the '
        "earlier Weeks 10 to 12 and will be replaced when Unit 4 is rebuilt. For Weeks 10 to 12, use the "
        "weekly pages.",
        2,
    ),
    (
        ["../_build_qti.py"],
        '    12: "OOP III — Applied Practice & Design",',
        '    12: "Tools and Guardrails — Model-Chosen Tools, Checks & Approval",',
        1,
    ),
]


def files_for(spec):
    if spec == "strip":
        return sorted(p for p in DOCS.glob("*.html") if not p.name.startswith("week12_"))
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
