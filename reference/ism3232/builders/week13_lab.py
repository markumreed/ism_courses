"""Build ism3232/docs/week13_lab.html from Bayside's schema.sql and the saved
sqlite3 sessions in runs/week13/. The four exercise answers appear only inside
the click-to-reveal answer keys.

python reference/ism3232/builders/week13_lab.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import week13_common as w
from pagekit import (
    DOCS,
    NO_SCREENSHOTS,
    callout_box,
    code_block,
    course_map,
    expected,
    head_from,
    hint,
    prev_next,
    reveal,
    section_divider,
    submit_box,
    task,
    time_bar,
)
from week13_starters import CHECKLIST

OUT = DOCS / "week13_lab.html"

INSTALL_UBUNTU = "sudo apt update\nsudo apt install sqlite3\nsqlite3 --version"
INSTALL_MAC = "sqlite3 --version"
PRACTICE_FOLDER = (
    "mkdir -p ~/ism3232/sql_practice\ncd ~/ism3232/sql_practice\ncode schema.sql"
)
OPEN = "sqlite3 lab13.db"
SETUP = (
    "mkdir -p ~/ism3232/module07_final_project\n"
    "cd ~/ism3232/module07_final_project\n"
    "python3 -m venv .venv && source .venv/bin/activate\n"
    "pip install pytest ruff streamlit ollama && pip freeze > requirements.txt\n"
    f"{w.GITIGNORE_LINE}\n"
    "git init"
)
GITHUB = (
    "# Create a new repository on github.com first:\n"
    f"# Name: {w.REPO}  |  Public  |  No README\n"
    f"git remote add origin https://github.com/YOURUSERNAME/{w.REPO}.git\n"
    "git branch -M main"
)
FILES = "touch PROPOSAL.md schema.sql && code ."
CHECK = (
    "sqlite3 my_business.db\n"
    ".read schema.sql\n"
    ".tables\n"
    "SELECT COUNT(*) FROM <table>;\n"
    ".read schema.sql\n"
    "SELECT COUNT(*) FROM <table>;\n"
    ".quit"
)
PUSH = f"git add . && git commit -m '{w.COMMIT}' && git push -u origin main"


# .task is a flex row, so without min-width:0 its content column grows to fit
# the longest SQL line and pushes the card past the page edge. With it, the
# code block's own overflow-x:auto scrolls instead. Expected boxes here hold
# sqlite3 tables, which must scroll rather than wrap on a phone.
STYLE = (
    "<style>.task-content{min-width:0;flex:1;}"
    ".expected{white-space:pre !important;overflow-x:auto;}</style>"
)


def block(label, code):
    return code_block(label, code, python=False)


def build():
    p = []
    add = p.append
    add(STYLE)
    add('<div class="wrap">')
    add(
        f'<div class="page-eyebrow" style="color:{w.EYEBROW_COLOR};">{w.UNIT} · Module 13 · Lab</div>'
    )
    add(f'<h1 class="wk-title">{w.TITLE}</h1>')
    add(
        '<p class="wk-deck">Module 7 &mdash; Capstone &mdash; practise SQL on Bayside, choose your '
        "business, write its proposal and schema, and get signed off</p>"
    )
    add(
        '<div class="meta">\n<span class="chip accent">Module 13 · Lab</span>\n'
        f'<span class="chip">{w.UNIT}</span>\n<span class="chip">About 3 hours</span>\n</div>'
    )
    add(
        '<div class="weekjump">\n<span class="weekjump-label">This module:</span>\n'
        '<a href="week13_reading.html" class="weekjump-link">Reading</a>\n'
        '<a href="week13_lecture.html" class="weekjump-link">Lecture</a>\n'
        '<a href="week13_lab.html" class="weekjump-link current">Lab</a>\n'
        '<a href="week13_lab_slides.html" class="weekjump-link">Slides</a>\n</div>'
    )
    add(course_map("W13 "))
    add(
        time_bar(
            [
                "Part 1: Install sqlite3 (10 min)",
                "Part 2: Practise (20)",
                "Part 3: Four exercises (30)",
                "Part 4: Set up (15)",
                "Part 5: Proposal (45)",
                "Part 6: Schema (30)",
                "Part 7: Sign-off (10)",
                "Part 8: Push (5)",
            ]
        )
    )
    add(
        callout_box(
            "blue",
            "&#x1F4CB;",
            "Lab goal &mdash; your capstone&rsquo;s first commit",
            "Practise SQL on Bayside&rsquo;s database, then start your own capstone: choose a "
            "business, write <code>PROPOSAL.md</code> and <code>schema.sql</code>, check the "
            "schema in sqlite3, and get your proposal signed off.",
        )
    )
    add(
        callout_box(
            "blue",
            "&#x1F4CD;",
            "Where you start",
            "Week 12 finished and pushed. No Ollama and no Python today: everything runs in the "
            'terminal and the <code>sqlite3</code> shell. Read the <a href="week13_reading.html">Week '
            "13 reading</a> first; this lab uses the same commands.",
        )
    )
    add(
        callout_box(
            "warn",
            "&#x26A0;",
            "Your proposal is your own",
            "The course AI policy still applies (syllabus, section 7). AI may explain a SQL error "
            "message, but the proposal and the schema you submit must be your own work.",
        )
    )

    # Part 1
    add(section_divider("Part 1 &mdash; Install sqlite3"))
    add(
        task(
            1,
            "Install the sqlite3 shell",
            "<p>On Windows, work in your Ubuntu (WSL) terminal:</p>"
            + block("Terminal &mdash; Ubuntu (WSL)", INSTALL_UBUNTU)
            + "<p>On a Mac, sqlite3 is already installed:</p>"
            + block("Terminal &mdash; macOS", INSTALL_MAC)
            + "<p>The last command prints a version line like this:</p>"
            + expected(w.run_text("version"))
            + hint(
                "Your version number and date may differ. On a Mac the columns of a table can be "
                "spaced a little differently. The rows are what matter."
            ),
        )
    )

    # Part 2
    add(section_divider("Part 2 &mdash; Practise on Bayside"))
    add(
        task(
            2,
            "Make a practice folder with Bayside&rsquo;s schema",
            "<p>Practise outside your capstone folder, so the practice database never reaches "
            "GitHub:</p>"
            + block("Terminal", PRACTICE_FOLDER)
            + "<p>Paste this into <code>schema.sql</code> and save it:</p>"
            + block("schema.sql", w.schema_text()),
        )
    )
    add(
        task(
            3,
            "Open the database and look around",
            "<p>Open a new database file for the lab. If you followed along with the "
            "reading in this folder, its <code>bayside.db</code> has your changes in it; a "
            "new file means none of them change today&rsquo;s results.</p>"
            + block("Terminal", OPEN)
            + "<p>At the <code>sqlite&gt;</code> prompt, type each line:</p>"
            + block("sqlite3", w.typed("lab", "practice"))
            + "<p>You should see:</p>"
            + expected(w.chunk("lab", "practice"))
            + hint(
                "<code>.quit</code> leaves sqlite3. Run <code>sqlite3 lab13.db</code> again "
                "later and everything is still there, but you would have to turn "
                "<code>.mode column</code> and <code>.headers on</code> on again: every new "
                "session starts with them off. Keep this window open for Part 3."
            ),
        )
    )

    # Part 3
    add(section_divider("Part 3 &mdash; Four SQL Exercises"))
    add(
        callout_box(
            "blue",
            "&#x1F9E9;",
            "Same window, in order",
            "Do the exercises in the sqlite3 window from Part 3, one after another. Exercise 3 "
            "adds an order and Exercise 4 files a request, so the later results depend on the "
            "earlier steps.",
        )
    )
    add(
        task(
            4,
            "Exercise 1 &mdash; Orders still processing",
            "<p>List the order ID and customer of every order whose status is "
            "<code>processing</code>, sorted by customer name.</p>"
            + expected(w.output_of("lab", "ex1"))
            + reveal(
                "Answer key &mdash; Exercise 1",
                block("sqlite3", w.chunk("lab", "ex1"))
                + "<p><strong>Common mistake:</strong> forgetting the quotes around "
                "<code>'processing'</code>. Without them SQLite looks for a column with that "
                "name.</p>",
            ),
        )
    )
    add(
        task(
            5,
            "Exercise 2 &mdash; Out of stock",
            "<p>List the name and price of every product with no stock.</p>"
            + expected(w.output_of("lab", "ex2"))
            + reveal(
                "Answer key &mdash; Exercise 2",
                block("sqlite3", w.chunk("lab", "ex2"))
                + "<p><strong>Common mistake:</strong> writing <code>stock = '0'</code>. SQLite "
                "lets it work, but it compares a number with text. Write <code>0</code>.</p>",
            ),
        )
    )
    add(
        task(
            6,
            "Exercise 3 &mdash; Orders by status",
            "<p>First add one more order. An <code>INSERT</code> prints nothing:</p>"
            + block("sqlite3", w.A106)
            + "<p>Now count the orders in each status.</p>"
            + expected(w.output_of("lab", "ex3"))
            + reveal(
                "Answer key &mdash; Exercise 3",
                block("sqlite3", w.chunk("lab", "ex3"))
                + "<p>Processing is 3 because of the order you just added.</p>",
            ),
        )
    )
    add(
        task(
            7,
            "Exercise 4 &mdash; Approve a change by hand",
            "<p>The agent filed this request for staff. Type it:</p>"
            + block("sqlite3", w.A101_REQUEST)
            + "<p>Now approve it yourself with two <code>UPDATE</code> statements: change order "
            "A101&rsquo;s address to <code>9 Pine Street, Tampa</code>, and mark request 1 as "
            "<code>approved</code>. Then check your work:</p>"
            + block("sqlite3", w.typed("lab", "ex4_check"))
            + expected(w.chunk("lab", "ex4_check"))
            + hint(
                "Typed the <code>INSERT</code> twice? Then there is a request 2 as well: "
                "<code>AUTOINCREMENT</code> gives every insert a new number. That is fine; "
                "approve request 1."
            )
            + reveal(
                "Answer key &mdash; Exercise 4",
                block("sqlite3", w.chunk("lab", "ex4"))
                + "<p>In Week 14 these two statements become <code>approve_request</code>, the "
                "only code that changes an order&rsquo;s address. Each <code>UPDATE</code> has a "
                "<code>WHERE</code>, so exactly one row changes.</p>",
            ),
        )
    )

    # Part 4
    add(section_divider("Part 4 &mdash; Set Up Your Capstone Folder"))
    add(
        task(
            8,
            "Create module07_final_project",
            "<p>You made this folder in Week 1. <code>mkdir -p</code> is safe if it is already "
            "there. Quit sqlite3 first.</p>"
            + block("Terminal", SETUP)
            + callout_box(
                "blue",
                "&#x1F517;",
                "One-time GitHub setup",
                "Each module folder is its own repository, as in Week 4.",
            )
            + block("Terminal", GITHUB)
            + hint(
                "<code>*.db</code> is in <code>.gitignore</code> because the database is "
                "rebuilt from <code>schema.sql</code>, and real data never goes to GitHub."
            ),
        )
    )

    # Part 5
    add(section_divider("Part 5 &mdash; Choose a Business and Write PROPOSAL.md"))
    add(
        task(
            9,
            "Choose your business and write the proposal",
            '<p>Open the <a href="capstone_starters.html">capstone starters page</a>. Pick one of '
            "the six businesses, or your own idea that meets the checklist. Then create the two "
            "files and open the folder:</p>"
            + block("Terminal", FILES)
            + '<p>Copy the <a href="capstone_starters.html#template">template</a> into '
            "<code>PROPOSAL.md</code> and fill in every section. "
            '<a href="capstone_starters.html#bayside">Bayside&rsquo;s proposal</a> shows a '
            "finished one. Before sign-off, tick each item:</p>"
            + "<ol>"
            + "".join(f"<li>{item}</li>" for item in CHECKLIST)
            + "</ol>",
        )
    )

    # Part 6
    add(section_divider("Part 6 &mdash; Write schema.sql"))
    add(
        task(
            10,
            "Write and check your schema",
            "<p>In <code>schema.sql</code>, create your business tables with "
            "<code>CREATE TABLE IF NOT EXISTS</code> and add at least five sample rows to each "
            "with <code>INSERT OR IGNORE</code>. Add an empty <code>change_requests</code> table "
            'with the columns on the <a href="capstone_starters.html">starters page</a>. Then '
            "read it twice and compare the counts. Use your business&rsquo;s name for the "
            "database file and your own table names:</p>"
            + block("Terminal and sqlite3", CHECK)
            + "<p>This is what Bayside&rsquo;s check looks like. The counts after the second "
            "<code>.read</code> must match the first:</p>"
            + block(
                "sqlite3 &mdash; Bayside, first read",
                w.chunks("read_twice", "setup", "first"),
            )
            + block(
                "sqlite3 &mdash; Bayside, read again", w.chunk("read_twice", "again")
            )
            + hint(
                "If a count grows, a table is missing its <code>PRIMARY KEY</code>, or "
                "<code>change_requests</code> has sample rows. Fix the file, delete the "
                "<code>.db</code> file, and check again."
            ),
        )
    )

    # Part 7
    add(section_divider("Part 7 &mdash; Sign-off"))
    add(
        task(
            11,
            "Get your proposal signed off",
            "<p>Show your instructor <code>PROPOSAL.md</code> and the two <code>.read</code> "
            "runs. They check the eight items, which takes one or two minutes. In Canvas, Lab 13 "
            "is then marked <strong>Approved</strong>, or <strong>Revise</strong> with a comment. "
            "Revise means fix it before the Week 14 lab; Week 14 code waits for approval.</p>",
        )
    )

    # Part 8
    add(section_divider("Part 8 &mdash; Commit and Push"))
    add(
        task(
            12,
            "Your capstone&rsquo;s first commit",
            block("Terminal", PUSH)
            + callout_box(
                "warn",
                "&#x26A0;",
                "Why there is no ruff or pytest this week",
                "Your folder has no Python yet. <code>pytest</code> finds no tests, exits with "
                "code 5 (&ldquo;no tests ran&rdquo;), and the <code>&amp;&amp;</code> chain would "
                "stop before git. Week 14 adds the tests, and the full ritual comes back. After "
                "this first push, <code>git push</code> is enough.",
            ),
        )
    )
    add(
        submit_box(
            "Lab 13 Submission &middot; Git commit + Canvas URL &middot; Approved or Revise",
            "Agent Design and SQL",
            [
                (
                    "&#x1F4C4;",
                    (
                        "<strong>Files in repo:</strong> <code>PROPOSAL.md</code>, "
                        "<code>schema.sql</code>, <code>requirements.txt</code> and "
                        "<code>.gitignore</code> in <code>module07_final_project</code>."
                    ),
                ),
                (
                    "&#x1F517;",
                    (
                        "<strong>Canvas submission:</strong> Paste your GitHub repository URL. Commit "
                        "message must include <code>lab 13</code>."
                    ),
                ),
                (
                    "&#x2714;",
                    "<strong>Sign-off:</strong> Approved, or Revise before the Week 14 lab.",
                ),
                ("&#x2705;", NO_SCREENSHOTS),
            ],
        )
    )
    add(
        prev_next(
            f"{w.PREV[0]}_lab.html",
            w.PREV[1],
            w.PREV[2],
            f"{w.NEXT[0]}_lab.html",
            w.NEXT[1],
            w.NEXT[2],
        )
    )
    add(
        f'<div class="page-footer">ISM3232 &middot; Week 13 In-Class Lab &middot; {w.TITLE}</div></div>'
    )

    head = head_from("week12_lab.html", "ISM3232 Week 13 In-Class Lab")
    page = f'{head}\n<body>{"".join(p)}\n<script src="../site.js"></script>\n</body></html>\n'
    derived = [
        INSTALL_UBUNTU,
        INSTALL_MAC,
        PRACTICE_FOLDER,
        OPEN,
        SETUP,
        GITHUB,
        FILES,
        CHECK,
        PUSH,
        w.typed("lab", "practice"),
        w.typed("lab", "ex4_check"),
        w.A106,
        w.A101_REQUEST,
    ]
    return page, derived


if __name__ == "__main__":
    page, _ = build()
    OUT.write_text(page)
    print("wrote", OUT)
