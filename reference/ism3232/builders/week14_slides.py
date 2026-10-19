"""Build ism3232/docs/week14_slides.html (reveal.js deck) from the Bayside app at
the Week 14 checkpoint. Code slides with output are standalone snippets that
verify_week14 re-runs.

python reference/ism3232/builders/week14_slides.py
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import week14_common as w
from pagekit import (
    DOCS,
    slide_code,
    slide_demo,
    slide_point,
    slide_section,
    slide_title,
    slides_shell,
    with_output,
)

OUT = DOCS / "week14_slides.html"


def build():
    outputs = w.snippet_outputs()
    timings = [
        ("0–8 min", "Where Week 13 left off"),
        ("8–25 min", "The connection pattern"),
        ("25–35 min", "Placeholders"),
        ("35–50 min", "Same door, whole words"),
        ("50–65 min", "The agent doesn't notice"),
        ("65–75 min", "Your project"),
    ]
    s = []
    add = s.append
    add(
        slide_title(
            "Week 14",
            w.TITLE,
            timings,
            "Week 14 — Database Tools\n\nToday's plan:\n"
            + "\n".join(f"  {t} — {what}" for t, what in timings)
            + "\n\nFrame it: Week 13 built the tables; today Python reads and writes them, the "
            "tools sit on top, and the Week 12 agent runs against them unchanged. Every output "
            "on these slides is a real run of the code it shows.",
        )
    )

    add(
        slide_section(
            1,
            "Where Week 13 Left Off",
            "The database exists; the agent cannot reach it.",
        )
    )
    add(
        slide_point(
            "From a list to a table",
            [
                "<code>OrderLookup</code>, <code>StockLookup</code> &rarr; <code>database.py</code>",
                "<code>ChangeQueue.requests</code> &rarr; the <code>change_requests</code> table",
                "<code>Toolbox</code> &rarr; <code>BaysideTools(db_file)</code>, same two methods",
                "<code>chatbot.py</code> &rarr; <code>agent.py</code>, first line only",
            ],
            "The last row is the point of the week: the agent never notices.",
        )
    )

    add(slide_section(2, "The Connection Pattern", "Open, run, close."))
    add(
        slide_code(
            "query_all",
            w.app_function("query_all"),
            "Line by line: connect, row_factory, execute with a tuple of values, fetchall, "
            "close, then dict(row) for each row.",
        )
    )
    add(
        slide_code(
            "Rows come back as dictionaries",
            with_output(w.SNIPPETS["rows"], outputs["rows"]),
            'The ? is filled from a one-item tuple, so it needs its comma: ("shipped",).',
            size=".6em",
        )
    )
    add(
        slide_demo(
            "python3 in the Bayside folder",
            "query_all, find_order",
            "Type the reading's shell session live.",
        )
    )

    add(slide_section(3, "Placeholders", "The model writes the arguments."))
    add(
        slide_code(
            "An f-string versus ?",
            with_output(w.SNIPPETS["injection"], outputs["injection"]),
            "The f-string returned every order; the placeholder found none. A customer can "
            "steer the model, so whatever arrives must stay plain text.",
            size=".6em",
        )
    )

    add(slide_section(4, "Same Door, Whole Words", "Week 12's door, one fix."))
    add(
        slide_code(
            "The run door",
            w.app_method("tools.py", "run"),
            "Unknown tool, missing value, and a value the customer never typed are all refused "
            "before any tool runs.",
            size=".5em",
            lang="python",
        )
    )
    add(
        slide_code(
            "A100 is not A1000",
            with_output(w.SNIPPETS["door"], outputs["door"]),
            "Week 12's substring check let A100 match inside A1000. words compares whole words, "
            "so the request is refused. Then run pytest -q tests/test_tools.py.",
            size=".62em",
        )
    )

    add(slide_section(5, "The Agent Doesn't Notice", "Run main.py twice."))
    add(
        slide_demo(
            "python3 main.py",
            "Twice, with Ollama",
            "Run it, reject the request, run it again and ask about request 1.",
        )
    )
    add(
        slide_code(
            "First run",
            w.run_text("main_first_run.txt"),
            "A real run of the course model: the change is filed, then rejected at the staff review.",
            size=".5em",
            lang="plaintext",
        )
    )
    add(
        slide_code(
            "Second run",
            w.run_text("main_second_run.txt"),
            "A new program, the same database: the decision is still there.",
            size=".62em",
            lang="plaintext",
        )
    )
    add(
        slide_code(
            "Approving twice changes it once",
            with_output(w.SNIPPETS["approve"], outputs["approve"]),
            "approve_request checks that the request is still waiting before it changes anything.",
            size=".6em",
        )
    )

    add(slide_section(6, "Your Project", "Copy, then write."))
    add(
        slide_point(
            "Copy, then write",
            [
                "Copy: the helpers and <code>create_tables</code>; <code>clean</code>, <code>words</code>, <code>customer_said</code>; your Week 12 agent and models",
                "Write: your database functions, your tools class, <code>keyword_model.py</code>, <code>settings.py</code>, <code>main.py</code>",
                "At least 12 tests: 5 database, 5 tools, 2 agent",
            ],
            "Point to the lab's mapping table: each Bayside function and its counterpart.",
        )
    )
    add(
        slide_point(
            "Next week",
            [
                "Staff still can't approve anything without running Python.",
                "Week 15: a Staff tab of their own, in a web app.",
            ],
            "End on the problem the next week solves.",
        )
    )

    before, after = slides_shell("week13_slides.html")
    before = re.sub(
        r"<title>.*?</title>",
        f"<title>ISM3232 Week 14 — {w.TITLE}</title>",
        before,
        count=1,
    )
    page = before + "\n" + "\n".join(s) + after
    derived = [with_output(code, outputs[name]) for name, code in w.SNIPPETS.items()]
    return page, derived


if __name__ == "__main__":
    page, _ = build()
    OUT.write_text(page)
    print("wrote", OUT)
