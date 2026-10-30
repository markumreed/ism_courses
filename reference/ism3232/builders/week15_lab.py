"""Build ism3232/docs/week15_lab.html: a short rerun warm-up whose results are
real test-tool runs of the page's own files, then each student's own database
additions, tests, and app.py with a Chat tab and a Staff tab.

python reference/ism3232/builders/week15_lab.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import week15_common as w
from capstone_starters import STYLE as TABLE_STYLE
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
    section_divider,
    submit_box,
    task,
    time_bar,
)
from week13_lab import STYLE as LAB_STYLE
from week14_reading import table

OUT = DOCS / "week15_lab.html"

START = (
    "cd ~/ism3232/module07_final_project\nsource .venv/bin/activate\n"
    "pytest -q\nstreamlit version"
)
PRACTICE = "cd ~/ism3232/sql_practice"
RUN = {name: f"streamlit run {name}" for name in w.WARMUP}
RUN_APP = "streamlit run app.py"
PYTEST = "pytest -q"
SECOND_TERMINAL = (
    "cd ~/ism3232/module07_final_project\nsource .venv/bin/activate\npython3"
)
FILE_REQUEST = (
    "from database import add_change_request\n"
    'add_change_request("<yours>.db", "<an ID>", "<new value>")'
)
PUSH = (
    "ruff format . && ruff check . && pytest -v\n"
    f"git add . && git commit -m '{w.COMMIT}' && git push"
)


def block(label, code):
    return code_block(label, code, python=False)


def part(label, name):
    return block(f"app.py — {label}", w.app_part(name))


def build():
    results = w.warmup_results()
    p = []
    add = p.append
    add(LAB_STYLE)
    add(TABLE_STYLE)
    add('<div class="wrap">')
    add(
        f'<div class="page-eyebrow" style="color:{w.EYEBROW_COLOR};">{w.UNIT} · Module 15 · Lab</div>'
    )
    add(f'<h1 class="wk-title">{w.TITLE}</h1>')
    add(
        '<p class="wk-deck">Module 7 &mdash; Capstone &mdash; a short warm-up on reruns, then '
        "a web app for your own business: a Chat tab for customers and a Staff tab that "
        "approves what your agent files</p>"
    )
    add(
        '<div class="meta">\n<span class="chip accent">Module 15 · Lab</span>\n'
        f'<span class="chip">{w.UNIT}</span>\n<span class="chip">About 3 hours + finishing at home</span>\n</div>'
    )
    add(
        '<div class="weekjump">\n<span class="weekjump-label">This module:</span>\n'
        '<a href="week15_reading.html" class="weekjump-link">Reading</a>\n'
        '<a href="week15_lecture.html" class="weekjump-link">Lecture</a>\n'
        '<a href="week15_lab.html" class="weekjump-link current">Lab</a>\n'
        '<a href="week15_lab_slides.html" class="weekjump-link">Slides</a>\n</div>'
    )
    add(course_map("W15 "))
    add(
        time_bar(
            [
                "Part 1: Start",
                "Part 2: Rerun warm-up (30 min)",
                "Parts 3–4: database + tests",
                "Part 5: sidebar + Chat",
                "Part 6: Staff tab",
                "Part 7: round trip",
                "Part 8: ritual + push",
            ]
        )
    )
    add(
        callout_box(
            "blue",
            "&#x1F4CB;",
            "Lab goal &mdash; your agent in a web app",
            "See for yourself why Streamlit needs <code>st.session_state</code>, then build "
            "Bayside&rsquo;s two tabs for your business: a chat over your agent, and a staff "
            "page that approves or rejects change requests, shows your records and a report, "
            "and edits one thing. At least 15 tests pass at the end.",
        )
    )
    add(
        callout_box(
            "warn",
            "&#x26A0;",
            "If your laptop cannot run the model",
            "Parts 1 to 6 and every test need no Ollama. The sidebar&rsquo;s keyword-only "
            "mode runs the whole app, and Part 7 shows how to try the Staff tab without "
            "the model.",
        )
    )

    # Part 1
    add(section_divider("Part 1 &mdash; Start"))
    add(
        task(
            1,
            "Open your capstone folder and check last week",
            block("Terminal", START)
            + hint(
                "<code>pytest -q</code> should pass your Week 14 tests (12 or more). "
                "<code>streamlit version</code> prints a version number; you installed "
                "Streamlit in Week 13."
            ),
        )
    )

    # Part 2
    add(section_divider("Part 2 &mdash; Rerun Warm-up"))
    add(
        task(
            2,
            "A counter that will not count",
            "<p>Work in the practice folder, outside your capstone repository. Your venv "
            "stays active.</p>"
            + block("Terminal", PRACTICE)
            + "<p>Create <code>counter.py</code>:</p>"
            + block(w.LABELS["counter"], w.WARMUP["counter.py"])
            + block("Terminal", RUN["counter.py"])
            + "<p>Open <code>http://localhost:8501</code> and click <strong>Add one</strong> "
            "three times. The page shows:</p>"
            + expected(results["counter"])
            + "<p>Stop the server with Ctrl+C. Every click ran the whole script again, so "
            "<code>count = 0</code> ran again each time.</p>"
            + hint(
                "The very first <code>streamlit run</code> stops at &ldquo;Welcome to "
                "Streamlit!&rdquo; and asks for an email address: press Enter to skip it. In "
                "WSL, open <code>http://localhost:8501</code> in your Windows browser."
            ),
        )
    )
    add(
        task(
            3,
            "Keep the count in session state",
            "<p>Create <code>counter_state.py</code>:</p>"
            + block(w.LABELS["counter_state"], w.WARMUP["counter_state.py"])
            + block("Terminal", RUN["counter_state.py"])
            + "<p>Click <strong>Add one</strong> three times:</p>"
            + expected(results["counter_state"])
            + "<p>Now refresh the browser. A refresh starts a new session:</p>"
            + expected(results["fresh"])
            + "<p>Stop the server with Ctrl+C.</p>",
        )
    )
    add(
        task(
            4,
            "A chat that echoes",
            "<p>Create <code>echo.py</code>:</p>"
            + block(w.LABELS["echo"], w.WARMUP["echo.py"])
            + block("Terminal", RUN["echo.py"])
            + f"<p>Type <code>{w.ECHO_MESSAGES[0]}</code>, press Enter, then type "
            f"<code>{w.ECHO_MESSAGES[1]}</code>. You should see four chat bubbles:</p>"
            + expected(results["echo"])
            + hint(
                "This is the Chat tab&rsquo;s pattern without the agent: the history lives in "
                "<code>st.session_state</code>, the loop draws it, and "
                "<code>st.rerun()</code> draws the new messages."
            ),
        )
    )

    # Part 3
    add(section_divider("Part 3 &mdash; Database Additions"))
    add(
        task(
            5,
            "Add what the Staff tab needs to database.py",
            "<p>Back in your capstone folder (<code>cd ~/ism3232/module07_final_project"
            "</code>). The Staff tab needs a report and one edit. Write yours from this "
            "table:</p>"
            + table(
                ["Bayside", "Yours", "Spokewell example"],
                [
                    [
                        "<code>status_report(db_file)</code>",
                        "a <code>GROUP BY</code> report over your main table",
                        "<code>repairs_by_status(db_file)</code>",
                    ],
                    [
                        "<code>restock(db_file, name, stock)</code>",
                        "the one change your edit form makes",
                        "<code>set_part_stock(db_file, name, stock)</code>",
                    ],
                    [
                        "<code>product_names(db_file)</code>",
                        (
                            "the dropdown&rsquo;s choices, if you do not already have such a "
                            "function"
                        ),
                        "<code>part_names(db_file)</code> (already written in Week 14)",
                    ],
                ],
            )
            + "<p>Bayside&rsquo;s two, as the shape:</p>"
            + block("database.py", w.app_function("status_report"))
            + block("database.py", w.app_function("restock")),
        )
    )

    # Part 4
    add(section_divider("Part 4 &mdash; Three Tests"))
    add(
        task(
            6,
            "Test the report and the edit",
            "<p>Add three tests to <code>tests/test_database.py</code>, each with "
            "<code>make_db(tmp_path)</code>:</p>"
            "<ol><li>the report counts correctly, modelled on "
            "<code>test_status_report_counts_orders</code>;</li>"
            "<li>the edit changes the chosen row, modelled on <code>test_restock</code>;</li>"
            "<li>the edit leaves the other rows alone: copy your edit test, and assert that "
            "another row is still what <code>schema.sql</code> says.</li></ol>"
            + block(
                "tests/test_database.py", w.app_test("test_status_report_counts_orders")
            )
            + block("tests/test_database.py", w.app_test("test_restock"))
            + block("Terminal", PYTEST)
            + hint(
                "You should now have 15 or more tests. <code>app.py</code> gets none: the "
                "autograder runs without Streamlit, so every decision stays in the files "
                "your tests cover."
            ),
        )
    )

    # Part 5
    add(section_divider("Part 5 &mdash; app.py: Sidebar and Chat Tab"))
    add(
        task(
            7,
            "Start app.py from Bayside&rsquo;s",
            "<p>Create <code>app.py</code> from these blocks, in order, changing what this "
            "table says:</p>"
            + table(
                ["Bayside", "Yours", "Spokewell example"],
                [
                    [
                        '<code>st.title("Bayside Outfitters")</code>',
                        "your business name",
                        "Spokewell Bike Repair",
                    ],
                    [
                        "<code>BaysideTools(DB_FILE)</code>",
                        "your tools class",
                        "<code>SpokewellTools(DB_FILE)</code>",
                    ],
                    [
                        '<code>"Sunny"</code>',
                        "your assistant&rsquo;s name",
                        '<code>"Spoke"</code>',
                    ],
                    [
                        "the caption&rsquo;s &ldquo;address change&rdquo;",
                        "your change",
                        "&ldquo;pickup change&rdquo;",
                    ],
                    [
                        (
                            "the chat box&rsquo;s hint and the spinner&rsquo;s "
                            "&ldquo;Sunny is thinking&rdquo;"
                        ),
                        "what your customers ask about, and your assistant&rsquo;s name",
                        "&ldquo;Ask Spoke about a repair, a part, or a pickup change&rdquo;",
                    ],
                    [
                        "<code>all_orders</code>",
                        "your list function",
                        "<code>all_repairs</code>",
                    ],
                    [
                        "<code>request['order_id']</code>, <code>request['new_address']</code>",
                        "your request columns",
                        "<code>request['ticket_id']</code>, <code>request['new_value']</code>",
                    ],
                    [
                        (
                            "<code>status_report</code> / <code>restock</code> / "
                            "<code>product_names</code>"
                        ),
                        "Part 3",
                        (
                            "<code>repairs_by_status</code> / <code>set_part_stock</code> / "
                            "<code>part_names</code>"
                        ),
                    ],
                ],
            )
            + part("imports", "imports")
            + part("the model switch and show()", "top")
            + part("the sidebar", "sidebar")
            + part("the chatbot, created once", "bot")
            + part("the tabs", "tabs")
            + part("the Chat tab", "chat"),
        )
    )
    add(
        task(
            8,
            "Run it and try a lookup",
            block("Terminal", RUN_APP)
            + "<p>Pick <strong>Keyword rules only</strong> in the sidebar and ask about one "
            "of your records by its ID. The keyword rules answer lookups without the model. "
            "Ctrl+C stops the server when you are done.</p>"
            + hint(
                "Nothing shows on the Staff tab yet: that is Part 6. If the page shows an "
                "error, read its last line, as with any traceback."
            ),
        )
    )

    # Part 6
    add(section_divider("Part 6 &mdash; The Staff Tab"))
    add(
        task(
            9,
            "Approvals, records, report and edit form",
            "<p>Add these blocks at the end of <code>app.py</code>, adapted with the table "
            "in Part 5:</p>"
            + part("the notice", "notice")
            + part("the waiting requests", "waiting")
            + part("the orders and the report", "tables")
            + part("the restock form", "restock")
            + hint(
                "Keep <code>st.text</code> for the waiting rows: the request holds text a "
                "customer typed, and <code>st.text</code> shows it exactly as typed. Your "
                "edit form changes your Part 3 function, with your own labels."
            )
            + "<p>Fit the form to the value you edit:</p>"
            "<ul>"
            "<li>A whole number, like Bayside&rsquo;s stock: keep "
            "<code>st.number_input</code> and <code>int()</code>.</li>"
            '<li>Text, such as a tenant&rsquo;s name: use <code>st.text_input("New '
            'tenant")</code> instead of <code>st.number_input</code>, and pass the value '
            "without <code>int()</code>.</li>"
            "<li>A price: keep <code>st.number_input</code> with "
            "<code>min_value=0.0, step=0.01</code>, and pass the value without "
            "<code>int()</code>, which would cut off the cents.</li>"
            "<li>One of a fixed set, such as a priority: use <code>st.selectbox</code> with "
            "a list of the choices.</li>"
            "</ul>"
            "<p>If your change request has no new value (a cancellation), leave "
            "&ldquo;to &hellip;&rdquo; out of the waiting row.</p>"
            "<p>Now run it and open the Staff tab:</p>"
            + block("Terminal", RUN_APP)
            + "<p>If no request is waiting you see <em>Nothing is waiting.</em>, then your "
            "records, your report and your form. Save one edit: the notice appears once and "
            "the records table shows the change. Leave the app running for Part 7.</p>",
        )
    )

    # Part 7
    add(section_divider("Part 7 &mdash; One Round Trip"))
    add(
        task(
            10,
            "File, approve, ask",
            "<p><strong>With Ollama</strong> (<code>ollama serve</code> in a second "
            "terminal): ask for a change in the Chat tab, approve it on the Staff tab, then "
            "go back to the Chat tab and ask what happened to it.</p>"
            "<p><strong>Keyword rules only:</strong> the keyword rules cannot file a change, "
            "so file one yourself, as in Week 14. With the app still running, open a second "
            "terminal and start <code>python3</code> in your project folder:</p>"
            + block("Terminal", SECOND_TERMINAL)
            + "<p>Then type each line (leave out the new value if your request has none):</p>"
            + block("Python shell — type each line", FILE_REQUEST)
            + "<p>The page only shows the new request after it reruns, so refresh the "
            "browser: the request is already in your database. Approve it on the Staff tab "
            "and watch your records table change.</p>"
            "<p><strong>Everyone:</strong> refresh the browser once at the end. The chat "
            "clears, because it lived in <code>st.session_state</code>; the decision stays, "
            "because it is in your database.</p>",
        )
    )

    # Part 8
    add(section_divider("Part 8 &mdash; Ritual and Push"))
    add(
        task(
            11,
            "Run the full ritual with Ollama switched off",
            "<p>Stop the app (Ctrl+C) and quit Ollama first.</p>"
            + block("Terminal", PUSH)
            + hint(
                "Run it from the project folder. If <code>ruff check</code> stops on a fixable "
                "error, run <code>ruff check --fix .</code>, then the first line again."
            ),
        )
    )
    add(
        submit_box(
            "Lab 15 Submission &middot; Git commit + Canvas URL &middot; Completion credit",
            "Streamlit Chat &amp; Staff",
            [
                (
                    "&#x1F4C4;",
                    (
                        "<strong>Files in repo:</strong> <code>app.py</code> with a Chat tab "
                        "and a Staff tab, the new functions in <code>database.py</code>, and "
                        "at least 15 tests across <code>tests/test_database.py</code>, "
                        "<code>tests/test_tools.py</code> and <code>tests/test_agent.py</code>. "
                        "No test imports <code>app.py</code> or <code>ollama_model.py</code>."
                    ),
                ),
                (
                    "&#x1F517;",
                    (
                        "<strong>Canvas submission:</strong> Paste your GitHub repository URL. "
                        "Commit message must include <code>lab 15</code>."
                    ),
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
        f'<div class="page-footer">ISM3232 &middot; Week 15 In-Class Lab &middot; {w.TITLE}</div></div>'
    )

    head = head_from("week14_lab.html", "ISM3232 Week 15 In-Class Lab")
    page = f'{head}\n<body>{"".join(p)}\n<script src="../site.js"></script>\n</body></html>\n'
    derived = [
        START,
        PRACTICE,
        *RUN.values(),
        RUN_APP,
        PYTEST,
        SECOND_TERMINAL,
        FILE_REQUEST,
        PUSH,
        *w.WARMUP.values(),
        *results.values(),
    ]
    return page, derived


if __name__ == "__main__":
    page, _ = build()
    OUT.write_text(page)
    print("wrote", OUT)
