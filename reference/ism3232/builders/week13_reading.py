"""Build ism3232/docs/week13_reading.html from Bayside's schema.sql (04bc8c9),
the saved sqlite3 sessions in runs/week13/, and Bayside's model proposal.

    python reference/ism3232/builders/week13_reading.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import week13_common as w
from pagekit import (
    DOCS,
    callout,
    coming_from,
    head_from,
    listing,
    objective,
    prev_next,
    quiz_mc,
    quiz_short,
    quiz_tf,
    quiz_trace,
    term,
)
from week13_proposal import bayside_proposal, section
from week13_starters import CHECKLIST

OUT = DOCS / "week13_reading.html"
OPEN = "cd ~/ism3232/sql_practice\nsqlite3 bayside.db"
COPY = "cp bayside.db practice_copy.db\nsqlite3 practice_copy.db"
REOPEN = "sqlite3 bayside.db"


def build():
    proposal = bayside_proposal()
    tables_section = section(proposal, "Tables")
    conversations_section = section(proposal, "Five sample conversations")

    parts = []
    add = parts.append

    add(
        f'<div class="page-eyebrow" style="color:{w.EYEBROW_COLOR};">{w.UNIT} · Module 13 · Reading</div>'
    )
    add(f'<h1 class="wk-title">{w.TITLE}</h1>')
    add(
        '<p class="wk-deck">Choose a business, design the tables its customers&rsquo; questions '
        "need, and build them in the sqlite3 shell.</p>"
    )
    add(
        '<div class="meta">\n<span class="chip accent">Module 13</span>\n'
        f'<span class="chip">{w.UNIT}</span>\n'
        '<span class="chip">Reading · Proposal, tables &amp; SQL</span>\n</div>'
    )
    add(
        '<div class="weekjump">\n<span class="weekjump-label">This module:</span>\n'
        '<a href="week13_reading.html" class="weekjump-link current">Reading</a>\n'
        '<a href="week13_lecture.html" class="weekjump-link">Lecture</a>\n'
        '<a href="week13_lab.html" class="weekjump-link">Lab</a>\n</div>'
    )
    add(
        objective(
            "By the end of this reading you will be able to choose a business for your "
            "capstone, turn its customers&rsquo; questions into tables, build those tables and "
            "query them in the sqlite3 shell, change rows safely, and write a proposal whose "
            "every section becomes code in the weeks that follow."
        )
    )
    add(
        coming_from(
            "Coming from Week 12",
            "Last week a change waited for a person to approve it. But the approval queue was "
            "a Python list, <code>ChangeQueue.requests</code>, and the orders were a dictionary "
            "typed into <code>main.py</code>. Stop the program and every request, and every "
            "approved address, is gone. A real business needs data that lasts after the "
            "program stops. This week your capstone starts: you choose a business, and you "
            "give it a database.",
        )
    )
    add(
        '<div style="font-family:var(--mono);font-size:11px;color:var(--muted);background:var(--bg2);'
        "border:1px solid var(--border);border-radius:6px;padding:8px 14px;margin-bottom:24px;"
        'display:flex;align-items:center;gap:10px;"><span style="opacity:.6;">&#x1F4D6;</span>'
        '<span><strong style="color:var(--text);">Pre-class reading.</strong> Read this before the '
        'session. The <a href="week13_lecture.html" style="color:var(--muted);">Lecture page</a> '
        "runs the same sqlite3 commands live in class.</span></div>"
    )

    add("<h2>Module at a glance</h2>")
    add(
        term(
            "Time",
            "One week. Reading about 60 minutes, lecture 75 minutes, lab about 3 hours, "
            "including your proposal and your schema.",
        )
    )
    add(
        term(
            "Prerequisites",
            "Week 12: the tool loop, the Toolbox checks and the approval queue. No Python "
            "this week, but every table you design here becomes Python next week.",
        )
    )
    add(
        term(
            "Materials",
            "A terminal, your editor, and the <code>sqlite3</code> tool (the lab installs it). "
            "No Ollama this week.",
        )
    )
    add(
        term(
            "Where things live",
            "Practice in <code>~/ism3232/sql_practice/</code>. Your capstone lives in "
            "<code>~/ism3232/module07_final_project/</code> from now until Week 16.",
        )
    )
    add("<h3>Learning outcomes</h3>")
    add(
        "<ol>"
        "<li>Choose a business for your capstone against the eight-item checklist.</li>"
        "<li>Design tables from the questions customers will ask.</li>"
        "<li>Write <code>CREATE TABLE</code> with column types and a primary key.</li>"
        "<li>Add sample rows with <code>INSERT</code>.</li>"
        "<li>Query with <code>SELECT</code>, <code>WHERE</code> and <code>ORDER BY</code>.</li>"
        "<li>Change rows safely with <code>UPDATE &hellip; WHERE</code>.</li>"
        "<li>Count with <code>COUNT(*)</code> and <code>GROUP BY</code>.</li>"
        "<li>Write a proposal whose sections map to the code you write in Weeks 14 to 16.</li>"
        "</ol>"
    )

    add("<h2>From questions to tables</h2>")
    add(
        "<p>Start with what people will ask, not with tables. Bayside&rsquo;s customers ask "
        "three kinds of question, and each one points to a kind of record:</p>"
    )
    add(
        "<ul><li><em>Has A101 shipped yet?</em> needs an order: its ID, the customer, the "
        "item, its status and its address. Orders go in a table called <code>orders</code>, "
        "one row per order, found by <code>order_id</code>.</li>"
        "<li><em>Is the day pack in stock?</em> needs a product: its name, price and stock. "
        "Products go in <code>products</code>, found by <code>name</code>.</li>"
        "<li><em>What happened to my address change?</em> needs a change request: which "
        "order, the new address, and whether staff approved it. Requests go in "
        "<code>change_requests</code>, found by a <code>number</code>.</li></ul>"
    )
    add(
        "<p>A <strong>table</strong> is a grid. Each <strong>row</strong> is one record, and "
        "each <strong>column</strong> is one fact every record has. The file that creates the "
        "tables is called the <strong>schema</strong>. Here is Bayside&rsquo;s, the exact file "
        "the reference app uses:</p>"
    )
    add(listing("schema.sql", w.schema_text()))
    add(
        "<ul><li><code>TEXT</code> holds words, <code>REAL</code> holds numbers with decimals "
        "(money), and <code>INTEGER</code> holds whole numbers (counts).</li>"
        "<li><code>PRIMARY KEY</code> marks the column that tells rows apart. Two orders can "
        "never share an <code>order_id</code>.</li>"
        "<li><code>NOT NULL</code> means the column must have a value.</li>"
        "<li><code>DEFAULT 'waiting'</code> fills in the status when a new request leaves it "
        "out.</li>"
        "<li><code>AUTOINCREMENT</code> gives each new request the next number: 1, 2, 3.</li>"
        "<li><code>INSERT OR IGNORE INTO &hellip; VALUES</code> adds the sample rows. Why "
        "&ldquo;or ignore&rdquo; matters comes below.</li></ul>"
    )

    add("<h2>SQL in the sqlite3 shell</h2>")
    add(
        "<p>SQL is the language databases understand. You type it into the "
        "<code>sqlite3</code> shell, which keeps a whole database in one file. Go to the "
        "folder that holds <code>schema.sql</code> and open a database file. If the file does "
        "not exist yet, sqlite3 creates it.</p>"
    )
    add(listing("Terminal", OPEN))
    add(
        "<p>Lines that start with a dot are <strong>dot-commands</strong>: instructions to "
        "the shell itself, not SQL. <code>.read</code> runs a file of SQL, "
        "<code>.tables</code> lists the tables, and <code>.schema</code> shows how one was "
        "created. Everything else is SQL and ends with a semicolon. This is one real "
        "session:</p>"
    )
    add(listing("sqlite3", w.run_text("first_look")))
    add(
        "<p>The first two lines are the shell&rsquo;s greeting; the version on your screen "
        "may differ. <code>SELECT * FROM products;</code> means &ldquo;show every column of "
        "every row&rdquo;. <code>.quit</code> leaves the shell; the database file keeps "
        "everything.</p>"
    )
    add("<h3>Choosing rows</h3>")
    add(
        "<p>Two more dot-commands make results easier to read: <code>.mode column</code> lines "
        "the values up, and <code>.headers on</code> names each column.</p>"
    )
    add(listing("sqlite3", w.chunk("select", "setup")))
    add("<p>Name the columns you want after <code>SELECT</code>:</p>")
    add(listing("sqlite3", w.chunk("select", "all")))
    add(
        "<p><code>WHERE</code> keeps only the rows that match. Text goes in single quotes:</p>"
    )
    add(listing("sqlite3", w.chunk("select", "where")))
    add(
        "<p><code>ORDER BY</code> sorts the result. <code>DESC</code> means largest "
        "first:</p>"
    )
    add(listing("sqlite3", w.chunk("select", "order")))
    add("<h3>Counting</h3>")
    add("<p><code>COUNT(*)</code> counts the rows that match:</p>")
    add(listing("sqlite3", w.chunk("count", "count")))
    add(
        "<p><code>GROUP BY</code> puts rows with the same value together and counts each "
        "group. The two products with no stock land in one row:</p>"
    )
    add(listing("sqlite3", w.chunk("count", "group")))
    add("<h3>Changing rows</h3>")
    add(
        "<p><code>UPDATE &hellip; SET &hellip; WHERE</code> changes the rows that match. "
        "Here the day pack is restocked:</p>"
    )
    add(listing("sqlite3", w.chunk("update", "update")))
    add(
        callout(
            "warn",
            "An UPDATE without WHERE changes every row",
            "<p>Leave out the <code>WHERE</code> and every product is changed, with no "
            "warning and no undo. Try it once, but only on a throwaway copy. Leave sqlite3 "
            "with <code>.quit</code>, copy the database, and open the copy:</p>",
        )
    )
    add(listing("Terminal", COPY))
    add(
        "<p>Every new sqlite3 session starts with <code>.mode column</code> and "
        "<code>.headers on</code> turned off, so turn them on again in the copy first:</p>"
    )
    add(listing("sqlite3", w.chunks("update_no_where", "display", "update")))
    add(
        "<p>Every product now has a stock of 0. Leave the copy with <code>.quit</code> and "
        "open your practice database again. The copy can simply be deleted.</p>"
    )
    add(listing("Terminal", REOPEN))
    add("<h3>Adding a row</h3>")
    add(
        "<p><code>INSERT</code> adds a row. List the columns, then the values. This is a new "
        "session, so turn the display on again first:</p>"
    )
    add(listing("sqlite3", w.chunks("insert", "display", "insert")))
    add(
        "<p>Run the same <code>INSERT</code> again and the primary key refuses it, because "
        "there is already a product with that name:</p>"
    )
    add(listing("sqlite3", w.chunk("insert", "again")))

    add("<h2>Why IF NOT EXISTS and INSERT OR IGNORE</h2>")
    add(
        "<p>Next week the app runs <code>schema.sql</code> every time it starts. That is safe "
        "only because of two choices. <code>CREATE TABLE IF NOT EXISTS</code> skips a table "
        "that is already there. <code>INSERT OR IGNORE</code> skips a row whose primary key "
        "is already in the table. One side effect: a sample row you delete comes back the "
        "next time the file runs. Count the orders, delete one, then read the schema "
        "again:</p>"
    )
    add(listing("sqlite3", w.chunks("read_twice", "first", "delete", "again")))
    add(
        "<p>Six orders, then five after the <code>DELETE</code>, then six again: the second "
        "<code>.read</code> put A105 back. That is fine for sample rows, and it is why your "
        "real changes should go through the app, never through deleting sample rows by "
        "hand.</p>"
    )
    add(
        "<p>And it is why <code>change_requests</code> has no sample rows. Its numbers come "
        "from <code>AUTOINCREMENT</code>, so every insert gets a new number and "
        "<code>INSERT OR IGNORE</code> never sees a repeat. Here is the same sample request "
        "inserted twice, which is what reading a schema that contained it twice would "
        "do:</p>"
    )
    add(listing("sqlite3", w.chunk("requests_twice", "insert")))
    add(
        "<p>Two identical requests, numbered 1 and 2. Every restart would add another. So "
        "<code>change_requests</code> starts empty, and requests appear only when the agent "
        "files them.</p>"
    )

    add("<h2>Writing your proposal</h2>")
    add(
        "<p>Your capstone is an agent for one business, with a chat for customers (or staff) "
        "and a Staff tab where people approve changes. You can pick one of six starter "
        "businesses or propose your own. Either way it must meet this checklist:</p>"
    )
    add("<ol>" + "".join(f"<li>{item}</li>" for item in CHECKLIST) + "</ol>")
    add(
        '<p>The <a href="capstone_starters.html">capstone starters page</a> has the six '
        'businesses, the <a href="capstone_starters.html#template">PROPOSAL.md template</a>, '
        "and Bayside&rsquo;s proposal filled in. Every section of the template turns into "
        "code: the tables into <code>schema.sql</code> this week, the tools into "
        "<code>tools.py</code> next week, the handoff rule into <code>HANDOFF_WORDS</code>, "
        "the instructions into <code>settings.py</code>, and the five conversations into the "
        "Week 16 evaluation. Here are two sections of Bayside&rsquo;s:</p>"
    )
    add(listing("From Bayside's PROPOSAL.md", tables_section))
    add(listing("From Bayside's PROPOSAL.md", conversations_section))
    add(
        "<p>Each conversation ends with what <em>must</em> happen, written in a form a program "
        "can check: use a tool, hand off, say something, never say something, or file some "
        "number of changes. In Week 16 these become test cases without any rewriting. "
        "Conversations 4 and 5 are safety cases, things the agent must <em>not</em> do. Yours "
        "needs at least one.</p>"
    )

    add("<h2>How sign-off works</h2>")
    add(
        "<p>In the lab, your instructor checks your <code>PROPOSAL.md</code> against the "
        "checklist at your laptop. It takes one or two minutes. Then Lab 13 is marked "
        "<strong>Approved</strong> in Canvas, or <strong>Revise</strong> with a comment "
        "saying what to fix. A revised proposal is due before the Week 14 lab, and Week 14 "
        "code waits until your proposal is approved. The rubric&rsquo;s Proposal part checks "
        "this.</p>"
    )

    add("<h2>What this module leaves out, and why</h2>")
    add(
        "<ul><li><strong>JOINs and foreign keys.</strong> They connect rows across tables. "
        "Each question in your capstone can be answered from one table, so you do not need "
        "them yet.</li>"
        "<li><strong>Indexes.</strong> They speed up searches in large tables. A few hundred "
        "rows need none.</li>"
        "<li><strong>Other databases.</strong> SQLite is one file with no server to set up, "
        "which is all a capstone needs. The SQL you learn works almost unchanged in larger "
        "databases.</li>"
        "<li><strong>Connecting from Python.</strong> That is next week, when these queries "
        "become functions.</li></ul>"
    )

    add('<h2 id="key-terms">Key terms this week</h2>')
    for word, definition in [
        ("Table", "A grid of records: one row per record, one column per fact."),
        ("Row", "One record in a table, such as one order."),
        (
            "Column",
            "One fact every row has, with a type such as TEXT, REAL or INTEGER.",
        ),
        (
            "Primary key",
            "The column whose value tells rows apart. No two rows share it.",
        ),
        ("Schema", "The SQL that creates the tables. Yours is schema.sql."),
        ("Query", "A SQL statement that asks for rows, such as SELECT."),
        ("WHERE", "The part of a query that keeps only the rows that match."),
        ("ORDER BY", "The part of a query that sorts the result."),
        (
            "GROUP BY",
            "Puts rows with the same value together so each group can be counted.",
        ),
        (
            "INSERT OR IGNORE",
            "Adds a row unless its primary key is already in the table.",
        ),
        ("AUTOINCREMENT", "Gives each new row the next number automatically."),
        (
            "Dot-command",
            "An instruction to the sqlite3 shell itself, such as .read or .tables.",
        ),
        (
            "Proposal",
            "PROPOSAL.md: what your agent does, section by section, before any code.",
        ),
        ("Sign-off", "Your instructor's check of the proposal against the checklist."),
    ]:
        add(term(word, definition))

    add("<h2>Before you leave this week</h2>")
    add(
        '<ul class="checklist">'
        "<li><code>sqlite3 --version</code> works on your laptop</li>"
        "<li>Can <code>.read</code> a schema and query it with <code>WHERE</code> and "
        "<code>ORDER BY</code></li>"
        "<li>Can explain why an <code>UPDATE</code> needs a <code>WHERE</code></li>"
        "<li>Can explain why <code>change_requests</code> starts empty</li>"
        "<li>Business chosen, from the starters or your own</li>"
        "<li><code>PROPOSAL.md</code> drafted, every section filled in</li>"
        "<li><code>schema.sql</code> reads twice without changing the row counts</li>"
        "<li>Proposal signed off, or revised before the Week 14 lab</li></ul>"
    )

    add('<h2 id="quiz">Module Quiz</h2>')
    quiz = [
        quiz_mc(
            1,
            "Which column type should hold a product&rsquo;s price?",
            ["TEXT", "INTEGER", "REAL", "BLOB"],
            2,
            "Money has cents. Bayside stores 89.00 as REAL.",
        ),
        quiz_tf(
            2,
            "<code>INSERT OR IGNORE</code> skips a row whose primary key is already in the "
            "table.",
            True,
            "That is why reading schema.sql twice does not duplicate the sample orders.",
        ),
        quiz_trace(
            3,
            "Bayside&rsquo;s orders table starts with six rows. What does the last line "
            "print?",
            ".read schema.sql\nDELETE FROM orders WHERE order_id = 'A105';\n"
            ".read schema.sql\nSELECT COUNT(*) FROM orders;",
            "6",
            "the second .read puts A105 back, because INSERT OR IGNORE only skips rows that "
            "are already there.",
        ),
        quiz_mc(
            4,
            "What does <code>UPDATE products SET stock = 0;</code> do?",
            [
                "Sets stock to 0 for one product",
                "Sets stock to 0 for every product",
                "Fails because it has no WHERE",
                "Asks which product to change",
            ],
            1,
            "Without WHERE an UPDATE changes every row. Try it only on a copy.",
        ),
        quiz_mc(
            5,
            "Which query lists the orders that have shipped?",
            [
                "SELECT order_id FROM orders WHERE status = 'shipped';",
                "SELECT order_id FROM orders ORDER BY 'shipped';",
                "SELECT shipped FROM orders;",
                "UPDATE orders WHERE status = 'shipped';",
            ],
            0,
            "WHERE keeps only the rows that match.",
        ),
        quiz_trace(
            6,
            "How many rows does this print under its headers?",
            "SELECT stock, COUNT(*) FROM products GROUP BY stock;",
            "5",
            "one row for each different stock value. The two products with stock 0 share a "
            "row.",
        ),
        quiz_mc(
            7,
            "Why does Bayside&rsquo;s change_requests table start with no rows?",
            [
                (
                    "AUTOINCREMENT gives every insert a new number, so sample requests would be "
                    "added again on every start"
                ),
                "SQLite tables cannot hold sample rows",
                "Staff delete the requests every morning",
                "The agent cannot read old requests",
            ],
            0,
            "Week 14 runs schema.sql every time the app starts.",
        ),
        quiz_tf(
            8,
            "A lookup tool may change a row if the customer asks politely.",
            False,
            "Lookup tools only read. A change goes through a change tool that files a request "
            "for staff.",
        ),
        quiz_mc(
            9,
            "Which proposal section becomes HANDOFF_WORDS in Week 14?",
            ["Handoff rule", "Tables", "Out of scope", "Instructions draft"],
            0,
            "The words go into agent.py and are checked before the model sees the message.",
        ),
        quiz_short(
            10,
            "Write one sample conversation for your proposal in evaluation terms, and name "
            "its check kind.",
            "For example: Customer: &ldquo;Is the day pack in stock?&rdquo; Must: use "
            "check_stock (a tool check). The five kinds are use a tool, hand off, says, never "
            "says, and files N changes; at least one conversation must be a safety case.",
        ),
    ]
    add("\n".join(quiz))
    add(
        "<p>The database exists, but the agent cannot reach it. Next week these queries "
        "become Python functions, and the functions become the agent&rsquo;s tools.</p>"
    )
    add(
        prev_next(
            f"{w.PREV[0]}_reading.html",
            w.PREV[1],
            w.PREV[2],
            f"{w.NEXT[0]}_reading.html",
            w.NEXT[1],
            w.NEXT[2],
        )
    )
    add(
        f'<div class="page-footer">ISM3232 &nbsp;·&nbsp; Week 13 &nbsp;·&nbsp; {w.TITLE}</div>'
    )

    head = head_from("week12_reading.html", f"ISM3232 Week 13 — {w.TITLE_TEXT}")
    body = "\n".join(parts)
    page = (
        f'{head}\n<body>\n{body}\n<script src="../site.js"></script>\n</body></html>\n'
    )
    return page, [OPEN, COPY, REOPEN, tables_section, conversations_section]


if __name__ == "__main__":
    page, _ = build()
    OUT.write_text(page)
    print("wrote", OUT)
