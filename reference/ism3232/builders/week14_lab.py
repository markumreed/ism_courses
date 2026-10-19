"""Build ism3232/docs/week14_lab.html: a short Bayside warm-up whose output is a
real run of the page's own blocks, then each student's own database layer,
tools, agent and terminal chat.

python reference/ism3232/builders/week14_lab.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import week14_common as w
from capstone_starters import STYLE as TABLE_STYLE
from pagekit import (
    DOCS,
    NO_SCREENSHOTS,
    callout_box,
    code_block,
    course_map,
    expected,
    function,
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

OUT = DOCS / "week14_lab.html"

START = "cd ~/ism3232/module07_final_project\nsource .venv/bin/activate"
WEEK12_CHECK = (
    "cd ~/ism3232/module06_agents\npytest -q\ncd ~/ism3232/module07_final_project"
)
WARMUP_FOLDER = "cd ~/ism3232/sql_practice\nmkdir -p tests && touch tests/__init__.py"
COPY_MODELS = (
    "cp ../module06_agents/chatbot.py agent.py\n"
    "cp ../module06_agents/fake_model.py ../module06_agents/keyword_model.py "
    "../module06_agents/ollama_model.py ."
)
COPY_FALLBACK = "cp ../module06_agents/fallback_model.py ."
PUSH = (
    "ruff format . && ruff check . && pytest -v\n"
    f"git add . && git commit -m '{w.COMMIT}' && git push"
)


def block(label, code):
    return code_block(label, code, python=False)


def agent_test_top():
    """tests/test_agent.py from its first line through its helpers."""
    text = w.app_file("tests/test_agent.py")
    return text[: text.index("\n\ndef test_keyword_model")].rstrip()


def app_test(file, name):
    return function(w.APP + file, name, w.REV)


def build():
    files = w.warmup_files()
    shell_out = w.warmup_shell()
    pytest_out = w.warmup_pytest()
    p = []
    add = p.append
    add(LAB_STYLE)
    add(TABLE_STYLE)
    add('<div class="wrap">')
    add(
        f'<div class="page-eyebrow" style="color:{w.EYEBROW_COLOR};">{w.UNIT} · Module 14 · Lab</div>'
    )
    add(f'<h1 class="wk-title">{w.TITLE}</h1>')
    add(
        '<p class="wk-deck">Module 7 &mdash; Capstone &mdash; a short warm-up on Bayside, then '
        "your own database functions, tools, agent and tests, ending in a chat with your own "
        "database</p>"
    )
    add(
        '<div class="meta">\n<span class="chip accent">Module 14 · Lab</span>\n'
        f'<span class="chip">{w.UNIT}</span>\n<span class="chip">About 3 hours + finishing at home</span>\n</div>'
    )
    add(
        '<div class="weekjump">\n<span class="weekjump-label">This module:</span>\n'
        '<a href="week14_reading.html" class="weekjump-link">Reading</a>\n'
        '<a href="week14_lecture.html" class="weekjump-link">Lecture</a>\n'
        '<a href="week14_lab.html" class="weekjump-link current">Lab</a>\n'
        '<a href="week14_lab_slides.html" class="weekjump-link">Slides</a>\n</div>'
    )
    add(course_map("W14 "))
    add(
        time_bar(
            [
                "Part 1: Start",
                "Part 2: Bayside warm-up (30 min)",
                "Part 3: database.py",
                "Part 4: database tests",
                "Part 5: tools.py",
                "Part 6: agent and models",
                "Part 7: main.py",
                "Part 8: ritual + push",
            ]
        )
    )
    add(
        callout_box(
            "blue",
            "&#x1F4CB;",
            "Lab goal &mdash; your agent on your own database",
            "Practise the database layer on Bayside for half an hour, then build the same "
            "layer for your business: database functions, tools, the agent from Week 12, at "
            "least 12 tests, and a terminal chat that reads and writes your database.",
        )
    )
    add(
        callout_box(
            "warn",
            "&#x26A0;",
            "If your laptop cannot run the model",
            "Parts 2 to 6 and every test need no Ollama, and they are what is graded. In Part "
            "7, run <code>main.py</code> on your keyword model instead (one line changes).",
        )
    )

    # Part 1
    add(section_divider("Part 1 &mdash; Start"))
    add(
        task(
            1,
            "Open your capstone folder and check last week",
            block("Terminal", START)
            + "<p>Your proposal must be approved, and <code>schema.sql</code> must read twice "
            'with nothing printed the second time (<a href="week13_lab.html">Week 13</a>, Part '
            "6). Check that your Week 12 folder still passes, then come back:</p>"
            + block("Terminal", WEEK12_CHECK)
            + hint(
                "Every Week 12 test should pass. You copy four of its files in Part 6."
            ),
        )
    )

    # Part 2
    add(section_divider("Part 2 &mdash; Bayside Warm-up"))
    add(
        task(
            2,
            "Set up the warm-up in your practice folder",
            "<p>Work in the practice folder from Week 13, outside your capstone repository. "
            "Your capstone venv stays active.</p>"
            + block("Terminal", WARMUP_FOLDER)
            + "<p>Create <code>database.py</code> with this block:</p>"
            + block(w.LABELS["db_top"], w.warmup_database_top())
            + "<p>Add this function below it:</p>"
            + block(w.LABELS["db_find"], w.app_function("find_order"))
            + "<p>Create <code>tools.py</code> with Bayside&rsquo;s whole tools file:</p>"
            + block(w.LABELS["tools"], files["tools.py"])
            + "<p>Create <code>tests/test_database.py</code> with this block, then add the "
            "test below it:</p>"
            + block(w.LABELS["test_top"], w.warmup_test_top())
            + block(w.LABELS["test_find"], w.warmup_find_test()),
        )
    )
    add(
        task(
            3,
            "Try it in a Python shell, then run the test",
            "<p>Start <code>python3</code> in the practice folder and type each line:</p>"
            + block(w.LABELS["shell"], "\n".join(w.WARMUP_SHELL))
            + "<p>You should see:</p>"
            + expected(shell_out)
            + hint(
                "Same tool, same value, two answers: only the first history has the "
                "customer typing A100. And the text with <code>OR '1'='1</code> in it found "
                "nothing, because the placeholder kept it as plain text."
            )
            + "<p>Leave the shell with <code>exit()</code> and run the test:</p>"
            + block("Terminal", "pytest -q")
            + "<p>The last line should say:</p>"
            + expected(pytest_out),
        )
    )

    # Part 3
    add(section_divider("Part 3 &mdash; Your database.py"))
    add(
        task(
            4,
            "Write your database functions",
            "<p>Back in <code>module07_final_project</code>, create <code>database.py</code>. "
            "Copy the first warm-up block as it is: the three helpers and "
            "<code>create_tables</code> work for any tables. Then write one function for each "
            "thing your tools and your staff review need, following Bayside&rsquo;s:</p>"
            + table(
                ["Bayside", "Yours", "Spokewell example"],
                [
                    [
                        (
                            "<code>query_all</code>, <code>query_one</code>, <code>change</code>, "
                            "<code>create_tables</code>"
                        ),
                        "copy as they are",
                        "the same",
                    ],
                    [
                        "<code>find_order(db_file, order_id)</code>",
                        "a lookup by key for each business table",
                        (
                            "<code>find_repair(db_file, ticket_id)</code>, "
                            "<code>find_part(db_file, name)</code>"
                        ),
                    ],
                    [
                        "<code>product_names(db_file)</code>",
                        "only if a tool searches for a name inside a sentence",
                        "<code>part_names(db_file)</code>",
                    ],
                    [
                        "<code>add_change_request(db_file, order_id, new_address)</code>",
                        "files your change",
                        "<code>add_change_request(db_file, ticket_id, new_value)</code>",
                    ],
                    [
                        "<code>find_request</code>, <code>waiting_requests</code>",
                        "the same, with your columns",
                        "the same",
                    ],
                    [
                        "<code>approve_request(db_file, number)</code>",
                        (
                            "changes your record&rsquo;s column, then marks the request approved "
                            "(Week 13&rsquo;s Exercise 4)"
                        ),
                        "<code>UPDATE repairs SET pickup_date = ? WHERE ticket_id = ?</code>",
                    ],
                    [
                        "<code>reject_request(db_file, number)</code>",
                        "the same",
                        "the same",
                    ],
                    [
                        "<code>all_orders(db_file)</code>",
                        "lists your records, for <code>main.py</code>",
                        "<code>all_repairs(db_file)</code>",
                    ],
                ],
            )
            + "<p>Check one lookup in <code>python3</code>: import <code>create_tables</code> "
            "and your lookup from <code>database</code>, run <code>create_tables</code> on a "
            "database named for your business, then look up an ID from your "
            "<code>schema.sql</code>. You should get a dictionary holding that row.</p>"
            + hint(
                "Every query uses <code>?</code> and a tuple of values. A one-item tuple "
                "needs its comma: <code>(ticket_id,)</code>."
            ),
        )
    )

    # Part 4
    add(section_divider("Part 4 &mdash; Database Tests"))
    add(
        task(
            5,
            "Write at least 5 database tests",
            "<p>Create <code>tests/__init__.py</code> (empty) and "
            "<code>tests/test_database.py</code> with a <code>make_db(tmp_path)</code> like "
            "the warm-up&rsquo;s. Write at least five tests, one for each behaviour, using "
            "Bayside&rsquo;s as models:</p>"
            "<ul><li>Creating the tables twice adds no duplicate rows "
            "(<code>test_create_tables_twice_adds_no_duplicate_rows</code>).</li>"
            "<li>A lookup needs the exact ID (<code>test_find_order_needs_the_exact_id</code>).</li>"
            "<li>SQL text in an ID is just text (<code>test_sql_in_an_order_id_is_just_text</code>).</li>"
            "<li>A filed change gets a number and waits "
            "(<code>test_change_requests_get_numbers_and_wait</code>).</li>"
            "<li>Approving changes the record once, and rejecting leaves it alone "
            "(<code>test_approve_changes_the_address_once</code>, "
            "<code>test_reject_changes_nothing_and_cannot_be_approved_later</code>).</li></ul>"
            + block(
                "tests/test_database.py — Bayside's approve test",
                app_test(
                    "tests/test_database.py", "test_approve_changes_the_address_once"
                ),
            )
            + block("Terminal", "pytest -q tests/test_database.py")
            + hint(
                "Run <code>pytest</code> from the project folder: "
                "<code>create_tables</code> opens <code>schema.sql</code> in the folder you run "
                "from, as the autograder does."
            ),
        )
    )

    # Part 5
    add(section_divider("Part 5 &mdash; tools.py"))
    add(
        task(
            6,
            "Write your tools class and its tests",
            "<p>Create <code>tools.py</code> with a class named for your business that takes "
            "<code>db_file</code>, like <code>BaysideTools</code>. Give it "
            "<code>tool_list</code>, your lookup tools and your change tool, each with an "
            "<code>Args:</code> docstring, and the <code>run</code> door. Copy these three "
            "methods as they are:</p>"
            + block(
                "tools.py — copy as they are",
                "\n\n".join(
                    w.app_method("tools.py", n)
                    for n in ("clean", "words", "customer_said")
                ),
            )
            + "<p>Then write <code>tests/test_tools.py</code> with at least five tests. Start "
            "from Bayside&rsquo;s helpers:</p>"
            + block("tests/test_tools.py — first block", w.tools_test_top())
            + "<p>Test a lookup, a change that waits, an unknown tool refused, a missing value "
            "refused, and a value the customer never typed refused.</p>"
            + block(
                "tests/test_tools.py — Bayside's made-up value test",
                app_test("tests/test_tools.py", "test_made_up_order_id_is_refused"),
            ),
        )
    )

    # Part 6
    add(section_divider("Part 6 &mdash; Agent and Models"))
    add(
        task(
            7,
            "Copy the agent and the models from Week 12",
            block("Terminal", COPY_MODELS)
            + "<p>Change the first line of <code>agent.py</code> to <code># agent.py</code> and "
            "set <code>HANDOFF_WORDS</code> to the words in your proposal. If you did Week "
            "12&rsquo;s Exercise 4, copy your fallback model too:</p>"
            + block("Terminal", COPY_FALLBACK)
            + "<p>If you skipped it, create <code>fallback_model.py</code> from this:</p>"
            + block("fallback_model.py", w.app_file("fallback_model.py"))
            + "<p>In <code>ollama_model.py</code>, add <code>MAX_MESSAGES = 20</code> below the "
            "imports and change the loop in <code>decide</code> to send only the last 20 "
            "messages:</p>"
            + block(
                "ollama_model.py — decide", w.app_method("ollama_model.py", "decide")
            )
            + "<p>In <code>keyword_model.py</code>, change the keywords and tool names to "
            "yours, so the program can run without Ollama. This is Bayside&rsquo;s:</p>"
            + block("keyword_model.py", w.app_file("keyword_model.py"))
            + "<p>Create <code>settings.py</code> from your proposal&rsquo;s instructions "
            "draft, in the shape of Bayside&rsquo;s:</p>"
            + block("settings.py", w.app_file("settings.py")),
        )
    )
    add(
        task(
            8,
            "Write at least 2 agent tests",
            "<p>Create <code>tests/test_agent.py</code> from Bayside&rsquo;s helpers, using "
            "your tools class:</p>"
            + block("tests/test_agent.py — first block", agent_test_top())
            + "<p>Adapt at least two of Bayside&rsquo;s agent tests, such as these:</p>"
            + block(
                "tests/test_agent.py",
                app_test(
                    "tests/test_agent.py",
                    "test_model_chosen_lookup_answers_from_the_database",
                ),
            )
            + block(
                "tests/test_agent.py",
                app_test(
                    "tests/test_agent.py",
                    "test_made_up_address_never_reaches_the_database",
                ),
            )
            + block("Terminal", "pytest -q")
            + hint(
                "You now have at least 12 tests across three files. None of them may import "
                "<code>ollama_model.py</code>: the autograder runs them without Ollama."
            ),
        )
    )

    # Part 7
    add(section_divider("Part 7 &mdash; main.py"))
    add(
        task(
            9,
            "Chat with your own database",
            "<p>Create <code>main.py</code> in the shape of Bayside&rsquo;s, with your tools "
            "class, your list-of-records function, and your request&rsquo;s columns in the "
            "staff review:</p>"
            + block("main.py", w.app_file("main.py"))
            + "<p>Start Ollama in a second terminal with <code>ollama serve</code>, then run "
            "<code>python3 main.py</code>. If your laptop cannot run the model, change "
            "<code>OllamaModel(MODEL_NAME)</code> to <code>KeywordModel()</code> and add "
            "<code>from keyword_model import KeywordModel</code>.</p>"
            + hint(
                "Run it twice. File a change, decide it at the staff review, then run it again "
                "and ask about it: the decision is still in your database."
            ),
        )
    )

    # Part 8
    add(section_divider("Part 8 &mdash; Ritual and Push"))
    add(
        task(
            10,
            "Run the full ritual with Ollama switched off",
            "<p>Quit Ollama first. If your tests pass now, they pass when your repository is "
            "graded on a computer that has never had Ollama.</p>"
            + block("Terminal", PUSH)
            + hint(
                "Run it from the project folder. If <code>ruff check</code> stops on a fixable "
                "error, run <code>ruff check --fix .</code>, then the first line again."
            ),
        )
    )
    add(
        submit_box(
            "Lab 14 Submission &middot; Git commit + Canvas URL &middot; Completion credit",
            "Database Tools",
            [
                (
                    "&#x1F4C4;",
                    (
                        "<strong>Files in repo:</strong> <code>database.py</code>, "
                        "<code>tools.py</code>, <code>agent.py</code>, <code>fake_model.py</code>, "
                        "<code>fallback_model.py</code>, <code>keyword_model.py</code>, "
                        "<code>ollama_model.py</code>, <code>settings.py</code>, <code>main.py</code>, "
                        "and at least 12 tests across <code>tests/test_database.py</code>, "
                        "<code>tests/test_tools.py</code> and <code>tests/test_agent.py</code>."
                    ),
                ),
                (
                    "&#x1F517;",
                    (
                        "<strong>Canvas submission:</strong> Paste your GitHub repository URL. "
                        "Commit message must include <code>lab 14</code>."
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
        f'<div class="page-footer">ISM3232 &middot; Week 14 In-Class Lab &middot; {w.TITLE}</div></div>'
    )

    head = head_from("week13_lab.html", "ISM3232 Week 14 In-Class Lab")
    page = f'{head}\n<body>{"".join(p)}\n<script src="../site.js"></script>\n</body></html>\n'
    derived = [
        START,
        WEEK12_CHECK,
        WARMUP_FOLDER,
        COPY_MODELS,
        COPY_FALLBACK,
        PUSH,
        "\n".join(w.WARMUP_SHELL),
        "pytest -q",
        "pytest -q tests/test_database.py",
        "\n\n".join(
            w.app_method("tools.py", n) for n in ("clean", "words", "customer_said")
        ),
        shell_out,
        pytest_out,
    ]
    return page, derived


if __name__ == "__main__":
    page, _ = build()
    OUT.write_text(page)
    print("wrote", OUT)
