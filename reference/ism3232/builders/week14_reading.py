"""Build ism3232/docs/week14_reading.html from the Bayside app at the Week 14
checkpoint (d44a23b), real output generated from it, and the saved runs.

    python reference/ism3232/builders/week14_reading.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import week14_common as w
from capstone_starters import STYLE
from pagekit import (
    DOCS,
    callout,
    coming_from,
    function,
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

OUT = DOCS / "week14_reading.html"


def table(headers, rows):
    """A small bordered table (the reading stylesheet leaves plain tables bare)."""
    head = "".join(f"<th>{h}</th>" for h in headers)
    body = "".join(
        "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>" for row in rows
    )
    return (
        f'<div style="overflow-x:auto;"><table class="starter-table"><thead><tr>{head}'
        f"</tr></thead><tbody>{body}</tbody></table></div>"
    )


def test_function(file, name):
    return function(w.APP + file, name, w.REV)


def build():
    outputs = w.snippet_outputs()
    shell_text = w.reading_shell()
    parts = []
    add = parts.append

    add(STYLE)
    add(
        f'<div class="page-eyebrow" style="color:{w.EYEBROW_COLOR};">{w.UNIT} · Module 14 · Reading</div>'
    )
    add(f'<h1 class="wk-title">{w.TITLE}</h1>')
    add(
        '<p class="wk-deck">Turn your database into the agent&rsquo;s tools: query it from '
        "Python safely, test every function, and plug in the agent you already have.</p>"
    )
    add(
        '<div class="meta">\n<span class="chip accent">Module 14</span>\n'
        f'<span class="chip">{w.UNIT}</span>\n'
        '<span class="chip">Reading · sqlite3, placeholders &amp; tools</span>\n</div>'
    )
    add(
        '<div class="weekjump">\n<span class="weekjump-label">This module:</span>\n'
        '<a href="week14_reading.html" class="weekjump-link current">Reading</a>\n'
        '<a href="week14_lecture.html" class="weekjump-link">Lecture</a>\n'
        '<a href="week14_lab.html" class="weekjump-link">Lab</a>\n</div>'
    )
    add(
        objective(
            "By the end of this reading you will be able to query SQLite from Python, pass "
            "values safely with placeholders, get rows back as dictionaries, write and test "
            "database functions, build the agent&rsquo;s tools on top of them, and connect "
            "the agent you wrote in Week 12 without changing it."
        )
    )
    add(
        coming_from(
            "Coming from Week 13",
            "The database exists, but the agent cannot reach it. You have a signed-off "
            "<code>PROPOSAL.md</code> and a <code>schema.sql</code> that reads twice "
            "without changing anything. This week Python opens that database, the agent&rsquo;s "
            "tools read and write it, and a change a customer asks for is still waiting for "
            "staff after the program stops.",
        )
    )
    add(
        '<div style="font-family:var(--mono);font-size:11px;color:var(--muted);background:var(--bg2);'
        "border:1px solid var(--border);border-radius:6px;padding:8px 14px;margin-bottom:24px;"
        'display:flex;align-items:center;gap:10px;"><span style="opacity:.6;">&#x1F4D6;</span>'
        '<span><strong style="color:var(--text);">Pre-class reading.</strong> Read this before the '
        'session. The <a href="week14_lecture.html" style="color:var(--muted);">Lecture page</a> '
        "runs the same code live in class.</span></div>"
    )

    add("<h2>Module at a glance</h2>")
    add(
        term(
            "Time",
            "One week. Reading about 60 minutes, lecture 75 minutes, lab about 3 hours, "
            "then finishing your own project at home.",
        )
    )
    add(
        term(
            "Prerequisites",
            "Week 13 signed off, and your Week 12 <code>module06_agents</code> folder with "
            "its tests passing.",
        )
    )
    add(
        term(
            "Materials",
            "Your capstone venv. Ollama only for the last part of the lab; everything else, "
            "including every test, runs without it.",
        )
    )
    add("<h3>Learning outcomes</h3>")
    add(
        "<ol>"
        "<li>Connect to a SQLite database from Python and run a query.</li>"
        "<li>Pass values safely with <code>?</code> placeholders.</li>"
        "<li>Get rows back as dictionaries.</li>"
        "<li>Write database functions for your own tables.</li>"
        "<li>Test them with <code>tmp_path</code>, so tests never touch your real "
        "database.</li>"
        "<li>Build the agent&rsquo;s tools on those functions.</li>"
        "<li>Explain why the tool check matches whole words.</li>"
        "<li>Connect the agent you wrote in Week 12 without changing it.</li>"
        "</ol>"
    )

    add("<h2>From a list to a table</h2>")
    add(
        "<p>In Week 12 the orders lived in a dictionary in <code>main.py</code> and the "
        "change requests in a Python list. Each piece now has a database-backed "
        "replacement:</p>"
    )
    add(
        table(
            ["Week 12", "Week 14", "What changed"],
            [
                [
                    "<code>OrderLookup</code> and <code>StockLookup</code> dictionaries",
                    "queries in <code>database.py</code>",
                    "the data lasts after the program stops",
                ],
                [
                    "<code>ChangeQueue.requests</code>, a list",
                    "the <code>change_requests</code> table",
                    "requests survive a restart",
                ],
                [
                    "<code>Toolbox</code>",
                    "<code>BaysideTools(db_file)</code>",
                    "the same <code>tool_list</code> and <code>run</code>",
                ],
                [
                    "<code>chatbot.py</code>",
                    "<code>agent.py</code>",
                    "only its first line",
                ],
            ],
        )
    )
    add(
        "<p>The last row is the point of the week: the agent asks the tools for things, "
        "and the tools kept the same two methods, so the agent never notices that the "
        "list became a table.</p>"
    )

    add("<h2>Python talks to SQLite</h2>")
    add(
        "<p>Python comes with a module for SQLite called <code>sqlite3</code>. Every "
        "database function follows the same pattern: open a connection, run SQL, close "
        "the connection. Bayside wraps the pattern in three helpers. Here is the first:</p>"
    )
    add(listing("database.py", w.app_function("query_all")))
    add(
        "<ul><li><code>sqlite3.connect(db_file)</code> opens the database file, or creates "
        "it if it is not there.</li>"
        "<li><code>row_factory = sqlite3.Row</code> lets each row be looked up by column "
        "name.</li>"
        "<li><code>execute(sql, values)</code> runs the SQL. Each <code>?</code> in the SQL "
        "is filled from <code>values</code>, which is a <strong>tuple</strong>: a list that "
        "cannot be changed, written with round brackets. A tuple with one item needs a "
        "comma: <code>(0,)</code>. Without it, <code>(0)</code> is just the number 0.</li>"
        "<li><code>fetchall()</code> returns every row, and <code>close()</code> closes the "
        "connection.</li>"
        "<li><code>[dict(row) for row in rows]</code> turns each row into an ordinary "
        "dictionary, the kind you have used since Week 6.</li></ul>"
    )
    add("<p>This is what the helpers return in a real Python shell:</p>")
    add(listing("Python shell", shell_text))
    add("<p>The other two helpers build on the same pattern:</p>")
    add(listing("database.py", w.app_function("query_one")))
    add(listing("database.py", w.app_function("change")))
    add(
        "<ul><li><code>commit()</code> saves the change. Nothing an <code>INSERT</code> or "
        "<code>UPDATE</code> does is kept until it runs.</li>"
        "<li><code>lastrowid</code> is the number SQLite gave the row just inserted, which "
        "is how a new change request learns its number.</li></ul>"
    )

    add("<h2>The business functions</h2>")
    add(
        "<p>Each business function is one short call to a helper. Lookups need the exact "
        "ID: <code>A1000</code> and <code>a100</code> are not <code>A100</code>.</p>"
    )
    add(listing("database.py", w.app_function("find_order")))
    add(listing("database.py", w.app_function("product_names")))
    add(listing("database.py", w.app_function("find_product")))
    add(
        "<p>Three functions file a change request, find one, and list the ones waiting:</p>"
    )
    add(listing("database.py", w.app_function("add_change_request")))
    add(listing("database.py", w.app_function("find_request")))
    add(listing("database.py", w.app_function("waiting_requests")))
    add(listing("database.py", w.app_function("approve_request")))
    add(
        callout(
            "concept",
            "You have written this SQL before",
            "<p>These are the two <code>UPDATE</code>s you typed by hand in Week 13&rsquo;s "
            "Exercise 4, now with placeholders, and with a check first that the request is "
            "still waiting, so a request is never applied twice.</p>",
        )
    )
    add(listing("database.py", w.app_function("reject_request")))
    add(
        "<p>One more function builds the tables. It reads <code>schema.sql</code> with "
        "<code>with open(...) as f:</code>, the same <code>with</code> you used in Week 6 "
        "to write a file, and runs the whole file with <code>executescript</code>:</p>"
    )
    add(listing("database.py", w.app_function("create_tables")))
    add(
        "<p>The app calls <code>create_tables</code> every time it starts. Week 13&rsquo;s "
        "<code>IF NOT EXISTS</code> and <code>INSERT OR IGNORE</code> are what make that "
        "safe. Three more functions in the file, <code>reset_database</code>, "
        "<code>restock</code> and <code>status_report</code>, are for Week 15&rsquo;s Staff "
        "tab.</p>"
    )

    add("<h2>Placeholders</h2>")
    add(
        "<p>A placeholder sends a value separately from the SQL, so the value can only "
        "ever be data. Building SQL with an f-string puts the value inside the SQL. Here "
        "the same text goes through both:</p>"
    )
    add(listing("placeholders.py", w.SNIPPETS["injection"]))
    add(listing("Output", outputs["injection"]))
    add(
        callout(
            "warn",
            "Why this matters more in an agent",
            "<p>The f-string query returned every order; the placeholder query found none. "
            "In a form app a person types the value. In an agent the model writes it, and a "
            "customer can steer the model. A placeholder keeps whatever arrives as plain "
            "text.</p>",
        )
    )

    add("<h2>Testing with tmp_path</h2>")
    add(
        "<p>Tests must never touch the real database. pytest gives any test that asks for "
        "<code>tmp_path</code> a new, empty folder that only it uses, and "
        '<code>tmp_path / "test.db"</code> is a file path inside that folder:</p>'
    )
    add(listing("tests/test_database.py", w.warmup_test_top()))
    add(
        listing(
            "tests/test_database.py",
            test_function(
                "tests/test_database.py",
                "test_create_tables_twice_adds_no_duplicate_rows",
            ),
        )
    )
    add(
        listing(
            "tests/test_database.py",
            test_function(
                "tests/test_database.py", "test_find_order_needs_the_exact_id"
            ),
        )
    )
    add(
        listing(
            "tests/test_database.py",
            test_function(
                "tests/test_database.py", "test_sql_in_an_order_id_is_just_text"
            ),
        )
    )
    add(
        callout(
            "concept",
            "Run pytest from the project folder",
            "<p><code>create_tables</code> opens <code>schema.sql</code> in the folder you "
            "run from. Run <code>pytest</code> in your project folder, as the autograder "
            "does.</p>",
        )
    )

    add("<h2>tools.py</h2>")
    add(
        "<p>The tools class is handed the database file and keeps Week 12&rsquo;s two "
        "methods. Each tool method calls a database function:</p>"
    )
    add(listing("tools.py", w.app_method("tools.py", "__init__")))
    add(listing("tools.py", w.app_method("tools.py", "look_up_order")))
    add(listing("tools.py", w.app_method("tools.py", "request_address_change")))
    add(
        "<p>A change tool only files a request; nothing about the order changes until "
        "staff approve. The door is Week 12&rsquo;s, with one new tool, "
        "<code>check_request</code>, so a customer can ask what staff decided:</p>"
    )
    add(listing("tools.py", w.app_method("tools.py", "run")))
    add(listing("tools.py", w.app_method("tools.py", "words")))
    add(listing("tools.py", w.app_method("tools.py", "customer_said")))
    add(
        "<p>In Week 12, <code>customer_said</code> checked whether the text appeared "
        "anywhere in a customer message. So when a customer typed <code>A1000</code> and "
        "the model asked for <code>A100</code>, the check passed, because "
        "<code>A100</code> is inside <code>A1000</code>. An automated security review of "
        "this app found it, and the fix came test-first: "
        "<code>test_a_typo_order_id_does_not_count_as_typed</code> failed, then "
        "<code>words</code> made it pass. <code>words</code> uses two string methods you "
        "have not met: <code>.split()</code> breaks text into a list of words, and "
        '<code>" ".join(...)</code> puts a list of words back together with spaces.</p>'
    )
    add(
        listing(
            "tests/test_tools.py",
            test_function(
                "tests/test_tools.py", "test_a_typo_order_id_does_not_count_as_typed"
            ),
        )
    )

    add("<h2>The agent doesn&rsquo;t notice</h2>")
    add(
        table(
            ["File", "Change from Week 12"],
            [
                [
                    "<code>agent.py</code>",
                    "only its first line, <code># agent.py</code>",
                ],
                [
                    "<code>ollama_model.py</code>",
                    (
                        "<code>MAX_MESSAGES = 20</code>: only the last 20 messages are sent, "
                        "so a long chat fits a laptop&rsquo;s model"
                    ),
                ],
                [
                    "<code>settings.py</code>",
                    "new: the database file, model and instructions",
                ],
                [
                    "<code>main.py</code>",
                    "new: the chat and the staff review, on the database",
                ],
            ],
        )
    )
    add(listing("ollama_model.py", w.app_method("ollama_model.py", "decide")))
    add(listing("settings.py", w.app_file("settings.py")))
    add(listing("main.py", w.app_file("main.py")))
    add(
        "<p>Here are two real runs with the course model. In the first, the customer said "
        "hello, asked about order A104 and the fleece vest, asked to change the address on "
        "order A102 to 9 Pine Street, Tampa, asked what happened to request 1, and typed "
        "<code>quit</code>; staff then typed <code>no</code>. What you type does not show "
        "in a recorded run, only the program&rsquo;s side:</p>"
    )
    add(listing("First run", w.run_text("main_first_run.txt")))
    add(
        "<p>In the second run, a new program asked only what happened to request 1. The "
        "answer came from the database, which still held the decision made in the first "
        "run:</p>"
    )
    add(listing("Second run", w.run_text("main_second_run.txt")))

    add("<h2>What this module leaves out, and why</h2>")
    add(
        "<ul><li><strong>JOINs.</strong> Each question your capstone answers comes from one "
        "table.</li>"
        "<li><strong>The <code>with sqlite3.connect(...)</code> shortcut.</strong> It saves "
        "changes but does not close the connection, so this course opens and closes "
        "connections itself.</li>"
        "<li><strong>ORMs and migrations.</strong> Tools that write the SQL for you, and "
        "tools that change a schema over time, are more than a one-file SQLite app "
        "needs.</li>"
        "<li><strong>Two people using the app at once.</strong> That comes with the Staff "
        "tab in Week 15.</li></ul>"
    )

    add('<h2 id="key-terms">Key terms this week</h2>')
    for word, definition in [
        ("Connection", "An open link to a database file, from connect until close."),
        (
            "Placeholder",
            "A ? in SQL whose value is sent separately, so it is always data.",
        ),
        (
            "Tuple",
            "A list that cannot change, in round brackets; one item needs a comma.",
        ),
        (
            "Row factory",
            "Tells sqlite3 how to build each row; sqlite3.Row allows names.",
        ),
        ("Commit", "Saves the changes made since the connection opened."),
        ("lastrowid", "The number SQLite gave the row just inserted."),
        ("tmp_path", "A new empty folder pytest gives one test."),
        ("Tools class", "The class whose methods the model may ask for, behind run."),
        (
            "Whole-word match",
            "A check that A100 is a word the customer typed, not part of one.",
        ),
    ]:
        add(term(word, definition))

    add("<h2>Before you leave this week</h2>")
    add(
        '<ul class="checklist">'
        "<li>Can explain each line of <code>query_all</code></li>"
        "<li>Can explain why <code>(order_id,)</code> needs its comma</li>"
        "<li>Can explain why a placeholder is safe and an f-string is not</li>"
        "<li>Your <code>database.py</code> passes at least 5 <code>tmp_path</code> tests</li>"
        "<li>Your tools refuse a value the customer never typed</li>"
        "<li>Your agent runs against your own database</li>"
        "<li>At least 12 tests pass with Ollama switched off</li>"
        "<li>Lab 14 submitted via GitHub URL</li></ul>"
    )

    add('<h2 id="quiz">Module Quiz</h2>')
    quiz = [
        quiz_mc(
            1,
            "Which line keeps a customer&rsquo;s text from being run as SQL?",
            [
                'conn.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,))',
                "conn.execute(f\"SELECT * FROM orders WHERE order_id = '{order_id}'\")",
                'conn.execute("SELECT * FROM orders WHERE order_id = \'" + order_id + "\'")',
                'conn.execute("SELECT * FROM orders WHERE order_id = %s" % order_id)',
            ],
            0,
            "The ? placeholder sends the value separately, so it can only ever be data.",
        ),
        quiz_tf(
            2,
            "<code>(order_id)</code> is a tuple with one item.",
            False,
            "It is order_id in brackets. A one-item tuple needs a comma: (order_id,).",
        ),
        quiz_trace(
            3,
            "What does this return?",
            'query_one(db_file, "SELECT * FROM orders WHERE order_id = ?", ("A999",))',
            "None",
            "query_one returns None when no row matches.",
        ),
        quiz_mc(
            4,
            "What happens if <code>change</code> leaves out <code>conn.commit()</code>?",
            [
                "The change is lost when the connection closes",
                "SQLite saves it anyway",
                "Python raises an error",
                "Only the first change is saved",
            ],
            0,
            "Nothing is saved until commit.",
        ),
        quiz_tf(
            5,
            "A test that uses tmp_path gets its own new folder, so it never touches "
            "bayside.db.",
            True,
            "Each test gets a folder only it uses.",
        ),
        quiz_mc(
            6,
            "Why does Week 14 match whole words in customer_said?",
            [
                "So A100 does not count when the customer typed A1000",
                "So the check runs faster",
                "Because SQLite needs whole words",
                "So capital letters matter",
            ],
            0,
            "Week 12&rsquo;s check let A100 match inside A1000.",
        ),
        quiz_trace(
            7,
            "What does <code>words</code> return for this text?",
            'tools.words("Where is #A100?")',
            '" where is a100 "',
            "lower case, ?.!,# stripped from each word, and a space at each end.",
        ),
        quiz_mc(
            8,
            "What did agent.py change to work with the database?",
            [
                "Only its first line",
                "Its tool loop",
                "Its history format",
                "Every method that reads orders",
            ],
            0,
            "The tools class kept tool_list and run, so the agent never noticed.",
        ),
        quiz_tf(
            9,
            "Calling approve_request twice on the same request changes the address twice.",
            False,
            "The second call finds the request already approved and changes nothing.",
        ),
        quiz_short(
            10,
            "Why do placeholders matter more in an agent than in a form?",
            "In a form a person types the value. In an agent the model writes it, and a "
            "customer can steer what the model writes. A placeholder keeps whatever arrives "
            "as plain text, never as SQL.",
        ),
    ]
    add("\n".join(quiz))
    add(
        "<p>Staff still can&rsquo;t approve anything without running Python. Next week they "
        "get a page of their own.</p>"
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
        f'<div class="page-footer">ISM3232 &nbsp;·&nbsp; Week 14 &nbsp;·&nbsp; {w.TITLE}</div>'
    )

    head = head_from("week13_reading.html", f"ISM3232 Week 14 — {w.TITLE_TEXT}")
    body = "\n".join(parts)
    page = (
        f'{head}\n<body>\n{body}\n<script src="../site.js"></script>\n</body></html>\n'
    )
    return page, [shell_text, w.SNIPPETS["injection"], outputs["injection"]]


if __name__ == "__main__":
    page, _ = build()
    OUT.write_text(page)
    print("wrote", OUT)
