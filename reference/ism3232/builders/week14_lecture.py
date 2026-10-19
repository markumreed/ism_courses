"""Build ism3232/docs/week14_lecture.html from the Bayside app at the Week 14
checkpoint, real output generated from it, and the saved runs.

python reference/ism3232/builders/week14_lecture.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import week14_common as w
from pagekit import (
    DOCS,
    NO_SCREENSHOTS,
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

OUT = DOCS / "week14_lecture.html"


def output(label, text):
    return code_block(label, text, python=False)


def build():
    outputs = w.snippet_outputs()
    shell_text = w.reading_shell()
    p = []
    add = p.append

    add('<div class="wrap">')
    add(
        '<div style="font-family:var(--mono);font-size:11px;color:var(--muted);background:var(--bg2);'
        "border:1px solid var(--border);border-radius:6px;padding:8px 14px;margin-bottom:24px;"
        'display:flex;align-items:center;gap:10px;"><span style="opacity:.6;">&#x1F4CB;</span>'
        '<span><strong style="color:var(--text);">In-class page.</strong> Read the '
        '<a href="week14_reading.html" style="color:var(--muted);">Week 14 reading</a> first if you '
        "haven't. Follow along during the live session.</span></div>"
        f'<div class="page-eyebrow" style="color:{w.EYEBROW_COLOR};">{w.UNIT} · Module 14 · Lecture</div>'
    )
    add(f'<h1 class="wk-title">{w.TITLE}</h1>')
    add(
        '<p class="wk-deck">Give the agent its database: query it from Python safely, test '
        "every function, and watch the Week 12 agent work unchanged.</p>"
    )
    add(
        '<div class="meta">\n<span class="chip accent">Module 14 · Lecture</span>\n'
        f'<span class="chip">{w.UNIT}</span>\n<span class="chip">~75 min</span>\n</div>'
    )
    add(
        '<div class="weekjump">\n<span class="weekjump-label">This module:</span>\n'
        '<a href="week14_reading.html" class="weekjump-link">Reading</a>\n'
        '<a href="week14_lecture.html" class="weekjump-link current">Lecture</a>\n'
        '<a href="week14_lab.html" class="weekjump-link">Lab</a>\n</div>'
    )
    add(course_map("W14 "))
    add(
        callout_blue(
            "&#x1F9E0;",
            "This week &mdash; the agent gets its database",
            "Week 13 built the tables. Today Python reads and writes them, the tools sit on "
            "top, and the agent from Week 12 runs against them without a single change. "
            "Every output on this page is a real run of the code it shows; the two chats "
            "are real runs of the course model.",
        )
    )

    add(section_divider("Session plan &mdash; 75 minutes"))
    add(
        concept_table(
            ["Minutes", "Segment", "What happens"],
            [
                ["0&ndash;8", "Where Week 13 left off", "The Week 12&rarr;14 map"],
                [
                    "8&ndash;25",
                    "The connection pattern, live",
                    "<code>query_all</code> in a Python shell; rows as dictionaries",
                ],
                [
                    "25&ndash;35",
                    "Placeholders, live",
                    "The f-string and the <code>?</code>; the model writes the arguments",
                ],
                [
                    "35&ndash;50",
                    "Same door, whole words",
                    "<code>run</code>, <code>customer_said</code>, the A1000 test",
                ],
                [
                    "50&ndash;65",
                    "The agent doesn&rsquo;t notice",
                    "<code>main.py</code> with Ollama, run twice; the data lasts",
                ],
                [
                    "65&ndash;75",
                    "Your project",
                    "What to copy, what to write, 12 tests; next week",
                ],
            ],
        )
    )

    add(section_divider("Section 1 &mdash; Where Week 13 Left Off"))
    add(
        two_col(
            card(
                "The database exists",
                "<p>Every student has a <code>schema.sql</code> that reads twice cleanly. "
                "The sqlite3 shell can query it.</p>",
            ),
            card(
                "The agent cannot reach it",
                "<p>Week 12&rsquo;s tools read a dictionary and a list. Today each one is "
                "replaced, and the agent is not touched.</p>",
            ),
        )
    )
    add(
        concept_table(
            ["Week 12", "Week 14"],
            [
                [
                    "<code>OrderLookup</code>, <code>StockLookup</code>",
                    "<code>database.py</code>",
                ],
                ["<code>ChangeQueue.requests</code>", "<code>change_requests</code>"],
                ["<code>Toolbox</code>", "<code>BaysideTools(db_file)</code>"],
                ["<code>chatbot.py</code>", "<code>agent.py</code>, first line only"],
            ],
        )
    )

    add(section_divider("Section 2 &mdash; The Connection Pattern, Live"))
    add(code_block("database.py", w.app_function("query_all")))
    add(output("Python shell", shell_text))
    add(
        card(
            "Say this",
            "<p>Open, run, close. The <code>?</code> is filled from a tuple, and a one-item "
            "tuple needs its comma: <code>(0,)</code>. <code>dict(row)</code> turns each row "
            "into the dictionaries students have used since Week 6. In <code>change</code>, "
            "nothing is saved until <code>commit</code>.</p>",
        )
    )

    add(section_divider("Section 3 &mdash; Placeholders, Live"))
    add(code_block("placeholders.py", w.SNIPPETS["injection"]))
    add(output("Output", outputs["injection"]))
    add(
        card(
            "Say this",
            "<p>The f-string returned every order; the placeholder found none. In an agent "
            "the model writes the arguments, and a customer can steer the model, so the "
            "database must treat whatever arrives as plain text.</p>",
        )
    )

    add(section_divider("Section 4 &mdash; Same Door, Whole Words"))
    add(code_block("tools.py", w.app_method("tools.py", "run")))
    add(code_block("door.py", w.SNIPPETS["door"]))
    add(output("Output", outputs["door"]))
    add(
        card(
            "Say this",
            "<p>The customer typed A1000 and the model asked for A100. Week 12&rsquo;s "
            "substring check would have let it through; <code>words</code> compares whole "
            "words, so it is refused. Then run the tests: <code>pytest -q "
            "tests/test_tools.py</code>.</p>",
        )
    )

    add(section_divider("Section 5 &mdash; The Agent Doesn&rsquo;t Notice"))
    add(output("First run", w.run_text("main_first_run.txt")))
    add(output("Second run", w.run_text("main_second_run.txt")))
    add(code_block("approve.py", w.SNIPPETS["approve"]))
    add(output("Output", outputs["approve"]))
    add(
        card(
            "Say this",
            "<p>Run <code>main.py</code> twice. The request decided in the first run is "
            "still decided in the second, because it lives in <code>bayside.db</code>. And "
            "approving twice changes the address once: <code>approve_request</code> checks "
            "that the request is still waiting.</p>",
        )
    )

    add(section_divider("Section 6 &mdash; Your Project"))
    add(
        two_col(
            card(
                "Copy",
                "<p>The three helpers and <code>create_tables</code>; <code>clean</code>, "
                "<code>words</code> and <code>customer_said</code>; your Week 12 "
                "<code>chatbot.py</code> as <code>agent.py</code>, <code>fake_model.py</code>, "
                "<code>fallback_model.py</code>, <code>ollama_model.py</code> plus "
                "<code>MAX_MESSAGES</code>.</p>",
            ),
            card(
                "Write",
                "<p>Your database functions, your tools class, an adapted "
                "<code>keyword_model.py</code>, <code>settings.py</code> and "
                "<code>main.py</code>, and at least 12 tests: 5 database, 5 tools, 2 "
                "agent.</p>",
            ),
        )
    )

    add(section_divider("Discussion and misconceptions"))
    add(
        prompt_list(
            [
                (
                    "Discussion 1: steering",
                    "Which of your tools could a customer try to steer with odd text?",
                    "Look for: any tool whose argument comes from what the customer typed.",
                ),
                (
                    "Discussion 2: approval",
                    "What should your approve function check before it changes anything?",
                    "Look for: that the request exists and is still waiting.",
                ),
                (
                    "Discussion 3: keeping tests",
                    "Which Week 12 test would you keep for your own agent?",
                    "Look for: the made-up value refused, and the payment handoff.",
                ),
            ]
        )
    )
    add(
        card(
            "Misconceptions to listen for",
            "<p>&ldquo;The database saves on its own.&rdquo; Nothing is kept until "
            "<code>commit</code>.</p>"
            "<p>&ldquo;An f-string is fine if the value looks safe.&rdquo; The model writes "
            "the value, and a customer can steer the model.</p>"
            "<p>&ldquo;<code>(order_id)</code> is a tuple.&rdquo; Without a comma it is just "
            "<code>order_id</code>.</p>"
            "<p>&ldquo;<code>tmp_path</code> tests touch my real database.&rdquo; Each test "
            "gets a new empty folder.</p>",
        )
    )
    add(
        assignment(
            "Lab 14 &middot; Due end of Week 14 &middot; Database Tools",
            "Your agent on your own database",
            [
                (
                    "&#x1F40D;",
                    (
                        "<strong>Files:</strong> <code>database.py</code>, <code>tools.py</code>, "
                        "<code>agent.py</code>, the four model files, <code>settings.py</code>, "
                        "<code>main.py</code>."
                    ),
                ),
                (
                    "&#x1F9EA;",
                    (
                        "<strong>Tests:</strong> at least 12 across "
                        "<code>tests/test_database.py</code>, <code>tests/test_tools.py</code> and "
                        "<code>tests/test_agent.py</code>, passing with Ollama switched off."
                    ),
                ),
                ("&#x1F517;", "<strong>Link:</strong> GitHub repository URL."),
                ("&#x2705;", NO_SCREENSHOTS),
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
        f'<div class="page-footer">ISM3232 &middot; Week 14 &middot; {w.TITLE}</div></div>'
    )

    head = head_from("week13_lecture.html", f"ISM3232 Week 14 — {w.TITLE_TEXT}")
    page = f'{head}\n<body>{"".join(p)}\n<script src="../site.js"></script>\n</body></html>\n'
    derived = [shell_text, *w.SNIPPETS.values(), *outputs.values()]
    return page, derived


if __name__ == "__main__":
    page, _ = build()
    OUT.write_text(page)
    print("wrote", OUT)
