"""Build ism3232/docs/week13_slides.html (reveal.js deck) from Bayside's
schema.sql and the saved sqlite3 sessions in runs/week13/.

python reference/ism3232/builders/week13_slides.py
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import week13_common as w
from pagekit import (
    DOCS,
    slide_chalk,
    slide_code,
    slide_demo,
    slide_point,
    slide_section,
    slide_title,
    slides_shell,
)
from week13_reading import COPY

OUT = DOCS / "week13_slides.html"


def build():
    timings = [
        ("0–8 min", "Where Week 12 left off"),
        ("8–20 min", "Tables from questions"),
        ("20–45 min", "The sqlite3 shell"),
        ("45–55 min", "Changing rows safely"),
        ("55–70 min", "Your proposal"),
        ("70–75 min", "Sign-off and next week"),
    ]
    s = []
    add = s.append
    add(
        slide_title(
            "Week 13",
            w.TITLE,
            timings,
            "Week 13 — Agent Design & SQL\n\nToday's plan:\n"
            + "\n".join(f"  {t} — {what}" for t, what in timings)
            + "\n\nFrame it: the capstone starts today. Week 12's agent forgot everything when it "
            "stopped; today it gets a database, and every student chooses the business their "
            "capstone serves. Every sqlite3 output on these slides is a real session of the sqlite3 "
            "Ubuntu installs.",
        )
    )

    add(
        slide_section(
            1,
            "Where Week 12 Left Off",
            "Run Week 12's main.py live before this section's slides.",
        )
    )
    add(
        slide_demo(
            "Week 12 main.py",
            "Approve an address change, quit, run it again",
            "Ask to change an address, give A102 and 9 Pine Street, approve it at the staff "
            "review, quit, and run again. The request is gone and the address is back. Ask: "
            "where should data live so it survives a restart?",
        )
    )

    add(
        slide_section(
            2,
            "Tables from Questions",
            "Start from what customers ask, never from tables.",
        )
    )
    add(
        slide_point(
            "Questions become tables",
            [
                "<em>Has A101 shipped yet?</em> &rarr; an order &rarr; <code>orders</code>, found by <code>order_id</code>",
                "<em>Is the day pack in stock?</em> &rarr; a product &rarr; <code>products</code>, found by <code>name</code>",
                "<em>What happened to my address change?</em> &rarr; a request &rarr; <code>change_requests</code>, found by <code>number</code>",
            ],
            "Each question points to a kind of record; each kind of record is a table; the value "
            "you look it up by is the primary key.",
        )
    )
    add(
        slide_code(
            "schema.sql",
            w.schema_text(),
            "Read it top to bottom: types, one primary key per table, NOT NULL, the default "
            "status, AUTOINCREMENT for request numbers, INSERT OR IGNORE for sample rows.",
            size=".5em",
            lang="sql",
        )
    )
    add(
        slide_chalk(
            "Questions → tables for a business in the room",
            "Take a business from the class. List five customer questions, then group them into "
            "records, then name the tables and their keys.",
        )
    )

    add(
        slide_section(
            3,
            "The sqlite3 Shell",
            "Run these live in a terminal; the slides are the backup.",
        )
    )
    add(
        slide_demo(
            "sqlite3 bayside.db",
            "In the folder that holds schema.sql",
            "Type each command from the next slides. Pause after .tables and .schema to ask what "
            "each line means.",
        )
    )
    add(
        slide_code(
            "A first look",
            w.run_text("first_look"),
            "Dot-commands talk to the shell; SQL ends with a semicolon. Default output separates "
            "values with a bar.",
            size=".66em",
            lang="plaintext",
        )
    )
    add(
        slide_code(
            "Readable output, then choosing columns",
            w.chunk("select", "setup") + "\n" + w.chunk("select", "all"),
            ".mode column lines values up; .headers on names each column.",
            size=".72em",
            lang="plaintext",
        )
    )
    add(
        slide_code(
            "WHERE keeps matching rows",
            w.chunk("select", "where"),
            "Text values go in single quotes.",
            lang="plaintext",
        )
    )
    add(
        slide_code(
            "ORDER BY sorts",
            w.chunk("select", "order"),
            "DESC means largest first.",
            lang="plaintext",
        )
    )
    add(
        slide_code(
            "COUNT and GROUP BY",
            w.chunk("count", "count") + "\n" + w.chunk("count", "group"),
            "GROUP BY stock puts both out-of-stock products in one row. Ask which question a "
            "GROUP BY on status would answer; students write that one in the lab.",
            size=".8em",
            lang="plaintext",
        )
    )

    add(
        slide_section(
            4,
            "Changing Rows Safely",
            "INSERT, UPDATE with and without WHERE, and reading the schema twice.",
        )
    )
    add(
        slide_code(
            "INSERT, and the primary key refusing a duplicate",
            w.chunk("insert", "insert") + "\n" + w.chunk("insert", "again"),
            "The second INSERT fails: there is already a product with that name.",
            size=".55em",
            lang="plaintext",
        )
    )
    add(
        slide_code(
            "UPDATE with WHERE",
            w.chunk("update", "update"),
            "Only the day pack changes.",
            size=".75em",
            lang="plaintext",
        )
    )
    add(
        slide_code(
            "UPDATE without WHERE, on a copy",
            COPY + "\n\n" + w.chunk("update_no_where", "update"),
            "Every row changes, with no warning and no undo. That is why it is done on a copy.",
            size=".7em",
            lang="plaintext",
        )
    )
    add(
        slide_code(
            "Reading the schema twice",
            w.run_text("read_twice"),
            "Six, five, six: the deleted sample row came back. Week 14 runs schema.sql on every "
            "start, which is why change_requests starts empty.",
            size=".85em",
            lang="plaintext",
        )
    )

    add(
        slide_section(
            5,
            "Your Proposal",
            "The checklist, the template, the starters.",
        )
    )
    add(
        slide_point(
            "The checklist, in short",
            [
                "One business; a chat for customers or staff; a Staff tab for staff",
                "Two business tables plus <code>change_requests</code>",
                "Two lookup tools and one change tool that only files requests",
                "A handoff rule in code; one kind of data never stored",
                "Instructions with &ldquo;only state facts&hellip;&rdquo;; five sample conversations",
            ],
            "The full wording is on the starters page and in the reading. The instructor checks "
            "these eight items at sign-off.",
        )
    )
    add(
        slide_point(
            "Every section becomes code",
            [
                "Tables &rarr; <code>schema.sql</code> (Week 13)",
                "Tools &rarr; <code>tools.py</code>; handoff &rarr; <code>HANDOFF_WORDS</code>; instructions &rarr; <code>settings.py</code> (Week 14)",
                "Change tool &rarr; the Staff tab (Week 15)",
                "Five conversations &rarr; <code>evaluation.py</code> (Week 16)",
            ],
            "Open capstone_starters.html and show the six starters and Bayside's filled-in "
            "proposal.",
        )
    )

    add(
        slide_section(
            6,
            "Sign-off and Next Week",
            "How sign-off works, then the bridge to Week 14.",
        )
    )
    add(
        slide_point(
            "Sign-off",
            [
                "In the lab, at your laptop, one or two minutes against the checklist",
                "Canvas: Approved, or Revise with a comment",
                "Revise means fix it before the Week 14 lab; Week 14 code waits for approval",
            ],
            "Keep it quick: the checklist is the whole test.",
        )
    )
    add(
        slide_point(
            "Next week",
            [
                "The database exists, but the agent cannot reach it.",
                "Week 14: these queries become Python functions, and the functions become the agent's tools.",
            ],
            "End on the bridge: the tool loop from Week 12 stays the same; only the tools change.",
        )
    )

    before, after = slides_shell("week12_slides.html")
    before = re.sub(
        r"<title>.*?</title>",
        f"<title>ISM3232 Week 13 — {w.TITLE}</title>",
        before,
        count=1,
    )
    page = before + "\n" + "\n".join(s) + after
    derived = [
        w.chunk("select", "setup") + "\n" + w.chunk("select", "all"),
        w.chunk("count", "count") + "\n" + w.chunk("count", "group"),
        w.chunk("insert", "insert") + "\n" + w.chunk("insert", "again"),
        COPY + "\n\n" + w.chunk("update_no_where", "update"),
    ]
    return page, derived


if __name__ == "__main__":
    page, _ = build()
    OUT.write_text(page)
    print("wrote", OUT)
