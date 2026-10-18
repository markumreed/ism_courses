"""Build ism3232/docs/capstone_starters.html: the capstone checklist, the six
starter businesses, the PROPOSAL.md template, and Bayside's filled-in proposal.

    python reference/ism3232/builders/capstone_starters.py
"""

import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import week13_common as w
from pagekit import DOCS, callout, esc, head_from, listing
from week13_proposal import bayside_proposal, evaluation_result
from week13_starters import CHECKLIST, STARTERS, TEMPLATE

OUT = DOCS / "capstone_starters.html"

# The reading page's stylesheet gives plain tables no padding or borders, so
# the sample-row tables carry their own (as the Week 10 reading does for code).
STYLE = (
    "<style>.starter-table{border-collapse:collapse;margin:8px 0 6px;font-size:14px;}"
    ".starter-table th,.starter-table td{border:1px solid var(--border);padding:6px 10px;"
    "text-align:left;vertical-align:top;}.starter-table th{background:var(--bg2);"
    "font-weight:600;}</style>"
)


def anchor(name):
    return re.sub(r"[^a-z]+", "-", html.unescape(name).lower()).strip("-")


def cell(value):
    """A sample value as the table shows it: prices with two decimals."""
    return f"{value:.2f}" if isinstance(value, float) else esc(str(value))


def starter_section(starter):
    parts = [
        f'<h2 id="{anchor(starter["name"])}">{starter["name"]}</h2>',
        f"<p>{starter['pitch']}</p>",
        (
            f"<p><strong>The chat serves:</strong> {starter['chat']}. "
            "<strong>The Staff tab serves:</strong> staff.</p>"
        ),
    ]
    for table in starter["tables"]:
        headers = [
            f'<code>{esc(name)}</code><br><span style="font-size:11px;color:var(--muted);">'
            f"{esc(kind)}</span>"
            for name, kind in table["columns"]
        ]
        head = "".join(f"<th>{h}</th>" for h in headers)
        body = "".join(
            "<tr>" + "".join(f"<td>{cell(value)}</td>" for value in row) + "</tr>"
            for row in table["rows"]
        )
        parts.append(f"<h3><code>{table['name']}</code></h3>")
        parts.append(
            f'<div style="overflow-x:auto;"><table class="starter-table"><thead><tr>{head}'
            f"</tr></thead><tbody>{body}</tbody></table></div>"
        )
        if table["note"]:
            parts.append(
                f'<p style="font-size:14px;color:var(--muted);">{table["note"]}</p>'
            )
    lookups = "".join(
        f"<li><code>{tool}({', '.join(arguments)})</code> reads <code>{table_name}</code>. "
        f"Example question: <em>{esc(question)}</em></li>"
        for tool, arguments, table_name, question in starter["lookups"]
    )
    tool, arguments, table_name, column, example = starter["change"]
    if starter["change_value"]:
        value = f"to <code>{starter['change_value']}</code>"
    else:
        value = "to the new value"
    parts.append("<h3>Tools</h3>")
    parts.append(
        f"<ul>{lookups}<li><strong>Change tool:</strong> <code>{tool}({', '.join(arguments)})"
        f"</code> files a request for staff. Approving sets <code>{table_name}.{column}</code> "
        f"{value}. Example request: <em>{esc(example)}</em></li></ul>"
    )
    parts.append(
        f"<p><strong>Handoff words:</strong> {', '.join(starter['handoff'])}. "
        f"<strong>Never stored:</strong> {starter['never_stored']}.</p>"
    )
    return "\n".join(parts)


def build():
    proposal = bayside_proposal()
    parts = []
    add = parts.append

    add(STYLE)
    add(
        f'<div class="page-eyebrow" style="color:{w.EYEBROW_COLOR};">{w.UNIT} · Starters</div>'
    )
    add('<h1 class="wk-title">Capstone Starters</h1>')
    add(
        '<p class="wk-deck">Pick one of six businesses, or propose your own. Every starter has '
        "the same shape as Bayside, so each week's pages carry straight over to your "
        "project.</p>"
    )
    add(
        '<div class="meta">\n<span class="chip accent">Unit 4</span>\n'
        '<span class="chip">Capstone</span>\n<span class="chip">Weeks 13–16</span>\n</div>'
    )
    add(
        '<p>You choose your business in the <a href="week13_lab.html">Week 13 lab</a>. The '
        '<a href="capstone_rubric.html">capstone rubric</a> says how the finished project is '
        "graded.</p>"
    )

    add('<h2 id="checklist">The checklist</h2>')
    add(
        "<p>Every capstone meets these, from this page or not. The instructor checks them at "
        "sign-off, and the rubric grades against them.</p>"
    )
    add("<ol>" + "".join(f"<li>{item}</li>" for item in CHECKLIST) + "</ol>")

    add("<h2>How a starter works</h2>")
    add(
        "<p>Each starter gives the columns of its two business tables and two example rows. "
        "You write the <code>CREATE TABLE</code> statements and at least five rows per "
        "business table yourself: that is Week 13's practice.</p>"
    )
    add(
        "<p>Every starter also has a <code>change_requests</code> table with these columns: "
        "<code>number INTEGER PRIMARY KEY AUTOINCREMENT</code>, your record's ID column "
        "<code>TEXT NOT NULL</code> (for example <code>ticket_id</code>), "
        "<code>new_value TEXT NOT NULL</code>, and "
        "<code>status TEXT NOT NULL DEFAULT 'waiting'</code>. It starts empty. Its numbers "
        "come from <code>AUTOINCREMENT</code>, so <code>INSERT OR IGNORE</code> never sees a "
        "repeated key, and every run of <code>schema.sql</code> would add sample requests "
        "again.</p>"
    )
    add(
        "<p>The tool names are suggestions. Rename them if you like, but keep the shape: "
        "lookup tools only read, and the change tool only files a request that staff "
        "approve or reject.</p>"
    )

    add("<h2>The six starters</h2>")
    add(
        "<ul>"
        + "".join(
            f'<li><a href="#{anchor(s["name"])}">{s["name"]}</a></li>' for s in STARTERS
        )
        + "</ul>"
    )
    for starter in STARTERS:
        add(starter_section(starter))

    add("<h2>Or propose your own</h2>")
    add(
        "<p>Any business that meets the checklist works, approved at sign-off. Good fits have "
        "records people ask about, and one change that a person should approve before it "
        "happens. Poor fits are businesses whose answers need a licensed professional, such "
        "as medical, legal or financial advice. Those topics belong in your handoff rule, "
        "not in your tools.</p>"
    )

    add('<h2 id="template">The PROPOSAL.md template</h2>')
    add(
        "<p>Copy it into <code>module07_final_project/PROPOSAL.md</code> and fill in every "
        "section. Each arrow shows which file the section turns into.</p>"
    )
    add(listing("PROPOSAL.md template", TEMPLATE))

    add('<h2 id="bayside">A filled-in example: Bayside</h2>')
    add(
        "<p>This is Bayside's proposal, generated from the reference app the Week 13 to 16 "
        "pages build, so it always matches that code.</p>"
    )
    add(listing("PROPOSAL.md — Bayside Outfitters", proposal))
    add(
        callout(
            "concept",
            "A proposal states what should happen",
            "<p>Conversation 5 is a safety case: a customer claims the store's hours have "
            "changed. In the real runs of the finished app, the agent passed it "
            f"{evaluation_result(7)} times and repeated the false closing time. That is "
            "still the right thing to write in a proposal. A proposal states what should "
            "happen; Week 16 measures what does.</p>",
        )
    )

    add('<div class="page-footer">ISM3232 · Capstone Starters · Unit 4</div>')

    head = head_from("week12_reading.html", "ISM3232 Capstone Starters")
    body = "\n".join(parts)
    page = (
        f'{head}\n<body>\n{body}\n<script src="../site.js"></script>\n</body></html>\n'
    )
    return page, [TEMPLATE, proposal]


if __name__ == "__main__":
    page, _ = build()
    OUT.write_text(page)
    print("wrote", OUT)
