"""Build ism3232/docs/week13_lecture.html from Bayside's schema.sql and the
saved sqlite3 sessions in runs/week13/.

python reference/ism3232/builders/week13_lecture.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import week13_common as w
from pagekit import (
    DOCS,
    assignment,
    callout_blue,
    card,
    code_block,
    concept_table,
    course_map,
    head_from,
    prev_next,
    prompt_list,
    section_divider,
    two_col,
)
from week13_lab import SUBMIT_NOTE
from week13_reading import COPY, REOPEN
from week13_starters import CHECKLIST

OUT = DOCS / "week13_lecture.html"


def sql(label, text):
    return code_block(label, text, python=False)


def build():
    p = []
    add = p.append

    add('<div class="wrap">')
    add(
        '<div style="font-family:var(--mono);font-size:11px;color:var(--muted);background:var(--bg2);'
        "border:1px solid var(--border);border-radius:6px;padding:8px 14px;margin-bottom:24px;"
        'display:flex;align-items:center;gap:10px;"><span style="opacity:.6;">&#x1F4CB;</span>'
        '<span><strong style="color:var(--text);">In-class page.</strong> Read the '
        '<a href="week13_reading.html" style="color:var(--muted);">Week 13 reading</a> first if you '
        "haven't. Follow along during the live session.</span></div>"
        f'<div class="page-eyebrow" style="color:{w.EYEBROW_COLOR};">{w.UNIT} · Module 13 · Lecture</div>'
    )
    add(f'<h1 class="wk-title">{w.TITLE}</h1>')
    add(
        '<p class="wk-deck">Give the agent data that lasts: turn questions into tables, build '
        "them in the sqlite3 shell, and plan the whole capstone in one proposal.</p>"
    )
    add(
        '<div class="meta">\n<span class="chip accent">Module 13 · Lecture</span>\n'
        f'<span class="chip">{w.UNIT}</span>\n<span class="chip">~75 min</span>\n</div>'
    )
    add(
        '<div class="weekjump">\n<span class="weekjump-label">This module:</span>\n'
        '<a href="week13_reading.html" class="weekjump-link">Reading</a>\n'
        '<a href="week13_lecture.html" class="weekjump-link current">Lecture</a>\n'
        '<a href="week13_lab.html" class="weekjump-link">Lab</a>\n</div>'
    )
    add(course_map("W13 "))
    add(
        callout_blue(
            "&#x1F9E0;",
            "This week &mdash; the capstone starts",
            "Week 12's agent forgot everything when it stopped. Today it gets a database, and "
            "you choose the business your capstone serves. Every sqlite3 output on this page is "
            "a real session of the sqlite3 that Ubuntu installs; a Mac may space columns a "
            "little differently.",
        )
    )

    add(section_divider("Session plan &mdash; 75 minutes"))
    add(
        concept_table(
            ["Minutes", "Segment", "What happens"],
            [
                [
                    "0&ndash;8",
                    "Where Week 12 left off",
                    "Approve a change, restart, and it is gone",
                ],
                [
                    "8&ndash;20",
                    "Tables from questions",
                    "Customer questions become records, tables and keys",
                ],
                [
                    "20&ndash;45",
                    "The sqlite3 shell",
                    (
                        "<code>.read</code>, <code>SELECT</code>, <code>WHERE</code>, "
                        "<code>ORDER BY</code>, <code>COUNT</code>, <code>GROUP BY</code>, live"
                    ),
                ],
                [
                    "45&ndash;55",
                    "Changing rows safely",
                    (
                        "<code>INSERT</code>, <code>UPDATE</code> with and without "
                        "<code>WHERE</code>, reading the schema twice"
                    ),
                ],
                [
                    "55&ndash;70",
                    "Your proposal",
                    "The checklist, the template, the six starters",
                ],
                [
                    "70&ndash;75",
                    "Sign-off and next week",
                    "How sign-off works; queries become tools",
                ],
            ],
        )
    )

    add(section_divider("Section 1 &mdash; Where Week 12 Left Off"))
    add(
        two_col(
            card(
                "Live: the restart problem",
                "<p>Run Week 12's <code>main.py</code>. Ask to change an address, give the order "
                "and the new address, and approve the request at the staff review. Then quit and "
                "run it again.</p>",
            ),
            card(
                "What students see",
                "<p>The request list is empty and the order has its old address back. The queue "
                "was a Python list and the orders a dictionary in <code>main.py</code>; both "
                "vanish when the program stops.</p>",
            ),
        )
    )
    add(
        card(
            "The question to leave on the board",
            "<p>Where should a business keep data so it survives a restart, a crash, or a new "
            "version of the code? Today&rsquo;s answer: in a database file, built from a schema "
            "you can read.</p>",
        )
    )

    add(section_divider("Section 2 &mdash; Tables from Questions"))
    add(
        concept_table(
            ["Customer asks", "Record", "Table", "Found by"],
            [
                [
                    "<em>Has A101 shipped yet?</em>",
                    "an order",
                    "<code>orders</code>",
                    "<code>order_id</code>",
                ],
                [
                    "<em>Is the day pack in stock?</em>",
                    "a product",
                    "<code>products</code>",
                    "<code>name</code>",
                ],
                [
                    "<em>What happened to my address change?</em>",
                    "a change request",
                    "<code>change_requests</code>",
                    "<code>number</code>",
                ],
            ],
        )
    )
    add(sql("schema.sql &mdash; Bayside&rsquo;s three tables", w.schema_text()))
    add(
        card(
            "Say this",
            "<p>Read it top to bottom with the class: a type for every column, one primary key "
            "per table, <code>NOT NULL</code> where a value must exist, and a default status "
            "for new requests. Then ask the room for a business and list its questions on the "
            "board before anyone names a table.</p>",
        )
    )

    add(section_divider("Section 3 &mdash; The sqlite3 Shell"))
    add(sql("sqlite3 &mdash; a first look", w.run_text("first_look")))
    add(
        card(
            "Say this",
            "<p>Dot-commands talk to the shell; everything else is SQL and ends with a "
            "semicolon. The default output separates values with <code>|</code>; two "
            "dot-commands make it readable.</p>",
        )
    )
    add(sql("sqlite3 &mdash; readable output", w.chunk("select", "setup")))
    add(sql("sqlite3 &mdash; choose columns", w.chunk("select", "all")))
    add(sql("sqlite3 &mdash; WHERE keeps matching rows", w.chunk("select", "where")))
    add(sql("sqlite3 &mdash; ORDER BY sorts", w.chunk("select", "order")))
    add(sql("sqlite3 &mdash; COUNT", w.chunk("count", "count")))
    add(sql("sqlite3 &mdash; GROUP BY", w.chunk("count", "group")))
    add(
        card(
            "Say this",
            "<p><code>GROUP BY stock</code> puts the two products with no stock in one row. "
            "Ask: which question from Section 2 would a <code>GROUP BY</code> on "
            "<code>status</code> answer? (How many orders are in each status: you will write "
            "that one yourselves in the lab.)</p>",
        )
    )

    add(section_divider("Section 4 &mdash; Changing Rows Safely"))
    add(sql("sqlite3 &mdash; UPDATE with WHERE", w.chunk("update", "update")))
    add(sql("Terminal &mdash; on a throwaway copy", COPY))
    add(
        sql(
            "sqlite3 &mdash; UPDATE without WHERE (a new session: display on again)",
            w.chunks("update_no_where", "display", "update"),
        )
    )
    add(
        card(
            "Say this",
            "<p>Every new sqlite3 session starts in list mode with headers off, so the copy "
            "needs <code>.mode column</code> and <code>.headers on</code> again. Then quit the "
            "copy and reopen the practice database.</p>",
        )
    )
    add(sql("Terminal &mdash; back to the practice database", REOPEN))
    add(
        sql(
            "sqlite3 &mdash; INSERT, and the primary key refusing a duplicate",
            w.chunks("insert", "display", "insert", "again"),
        )
    )
    add(
        sql(
            "sqlite3 &mdash; reading the schema twice",
            w.chunks("read_twice", "first", "delete", "again"),
        )
    )
    add(
        card(
            "Say this",
            "<p>Week 14&rsquo;s app runs <code>schema.sql</code> every time it starts. "
            "<code>IF NOT EXISTS</code> and <code>INSERT OR IGNORE</code> make that safe. The "
            "deleted sample order came back, and that is fine. But a table numbered by "
            "<code>AUTOINCREMENT</code> would gain duplicates on every start, so "
            "<code>change_requests</code> starts empty.</p>",
        )
    )

    add(section_divider("Section 5 &mdash; Your Proposal"))
    add("<ol>" + "".join(f"<li>{item}</li>" for item in CHECKLIST) + "</ol>")
    add(
        concept_table(
            ["Template section", "Becomes", "Week"],
            [
                ["Tables", "<code>schema.sql</code>", "13"],
                ["Lookup tools and change tool", "<code>tools.py</code>", "14"],
                [
                    "Handoff rule",
                    "<code>HANDOFF_WORDS</code> in <code>agent.py</code>",
                    "14",
                ],
                ["Instructions draft", "<code>settings.py</code>", "14"],
                ["Change tool", "the Staff tab&rsquo;s Approve and Reject", "15"],
                ["Five sample conversations", "<code>evaluation.py</code> cases", "16"],
            ],
        )
    )
    add(
        card(
            "Show the starters",
            '<p>Open the <a href="capstone_starters.html">capstone starters page</a>: six '
            "businesses with the same shape as Bayside, the template, and Bayside&rsquo;s own "
            "proposal. Point out the apartment starter&rsquo;s handoff words (gas, fire, flood, "
            "smoke): a missed handoff there could hurt someone, so false alarms are the cheap "
            "mistake.</p>",
        )
    )

    add(section_divider("Section 6 &mdash; Sign-off and Next Week"))
    add(
        card(
            "Sign-off",
            "<p>In the lab, one or two minutes per student at their laptop, against the "
            "checklist. Canvas then says Approved, or Revise with a comment. A revised "
            "proposal is due before the Week 14 lab, and Week 14 code waits for approval.</p>"
            "<p>Next week the queries from today become Python functions, and the functions "
            "become the agent&rsquo;s tools.</p>",
        )
    )

    add(section_divider("Discussion and misconceptions"))
    add(
        prompt_list(
            [
                (
                    "Discussion 1: two tables",
                    "Which of your business&rsquo;s questions needs information from two tables?",
                    (
                        "Look for: a starting point for JOINs later; this week, pick tables so each "
                        "question needs one."
                    ),
                ),
                (
                    "Discussion 2: keys",
                    "What breaks if <code>order_id</code> is not a primary key?",
                    (
                        "Look for: duplicate orders, and INSERT OR IGNORE adding the sample rows again "
                        "on every start."
                    ),
                ),
                (
                    "Discussion 3: handoff words",
                    "Which handoff word would you rather have fire by mistake than miss?",
                    "Look for: the cost of each kind of mistake, from Week 11 and 12.",
                ),
            ]
        )
    )
    add(
        card(
            "Misconceptions to listen for",
            "<p>&ldquo;A primary key is just the first column.&rdquo; It is the column the "
            "database keeps unique, wherever it sits.</p>"
            "<p>&ldquo;UPDATE changes one row unless you say otherwise.&rdquo; It changes every "
            "row unless <code>WHERE</code> says otherwise.</p>"
            "<p>&ldquo;INSERT OR IGNORE updates the existing row.&rdquo; It leaves the existing "
            "row exactly as it is.</p>"
            "<p>&ldquo;The shell saves only when you quit.&rdquo; Each statement is saved as soon "
            "as it runs.</p>",
        )
    )
    add(
        assignment(
            "Lab 13 &middot; Due end of Week 13 &middot; Proposal and Schema",
            "Your capstone&rsquo;s first commit",
            [
                (
                    "&#x1F4DD;",
                    (
                        "<strong>File:</strong> <code>PROPOSAL.md</code>, every section filled in, "
                        "the checklist ticked."
                    ),
                ),
                (
                    "&#x1F5C3;",
                    (
                        "<strong>File:</strong> <code>schema.sql</code>, your business tables with at "
                        "least five sample rows each and an empty <code>change_requests</code>."
                    ),
                ),
                (
                    "&#x2714;",
                    "<strong>Sign-off:</strong> Approved, or Revise before the Week 14 lab.",
                ),
                ("&#x1F517;", "<strong>Link:</strong> GitHub repository URL."),
                ("&#x2705;", SUBMIT_NOTE),
            ],
        )
    )
    add(
        prev_next(
            f"{w.PREV[0]}_lecture.html",
            w.PREV[1],
            w.PREV[2],
            f"{w.NEXT[0]}_lecture.html",
            w.NEXT[1],
            w.NEXT[2],
        )
    )
    add(
        f'<div class="page-footer">ISM3232 &middot; Week 13 &middot; {w.TITLE}</div></div>'
    )

    head = head_from("week12_lecture.html", f"ISM3232 Week 13 — {w.TITLE_TEXT}")
    page = f'{head}\n<body>{"".join(p)}\n<script src="../site.js"></script>\n</body></html>\n'
    derived = [COPY, REOPEN]
    return page, derived


if __name__ == "__main__":
    page, _ = build()
    OUT.write_text(page)
    print("wrote", OUT)
