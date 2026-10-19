"""Build ism3232/docs/week14_lab_slides.html (the lab's reveal.js deck). The
warm-up's outputs are real runs of the lab page's own blocks.

python reference/ism3232/builders/week14_lab_slides.py
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import week14_common as w
from pagekit import DOCS
from week12_lab_slides import (
    SHOWN,
    code_slide,
    divider,
    idea,
    out_slide,
    quiz,
    sec,
    warn,
)
from week14_lab import COPY_MODELS, PUSH, START, WARMUP_FOLDER

OUT = DOCS / "week14_lab_slides.html"


def shell_slide(comment, title, code, expect, notes):
    return code_slide(comment, title, code, expect, notes, readonly=True, lang="shell")


def python_slide(comment, title, code, expect, notes):
    return code_slide(comment, title, code, expect, notes, readonly=True)


def build():
    SHOWN.clear()
    timings = [
        ("0:00–0:05", "Part 1 — Start"),
        ("0:05–0:35", "Part 2 — Bayside warm-up"),
        ("0:35–1:05", "Parts 3–4 — Your database.py and its tests"),
        ("1:05–1:45", "Part 5 — Your tools and their tests"),
        ("1:45–2:30", "Part 6 — Agent and models"),
        ("2:30–3:00", "Parts 7–8 — main.py, ritual and push"),
    ]
    bar = "\n".join(
        f'<span class="t-item"><strong>{t}</strong> {what}</span>'
        for t, what in timings
    )
    s = []
    add = s.append
    add(
        sec(
            "1. TITLE",
            "s-title",
            f'<p class="eyebrow">ISM3232 &nbsp;·&nbsp; Week 14 &nbsp;·&nbsp; Module 14 &nbsp;·&nbsp; {w.UNIT}</p>\n'
            f'<h1>{w.TITLE}</h1>\n<div class="t-bar">\n{bar}\n</div>\n'
            '<p class="hint">&larr; &rarr; navigate &nbsp;·&nbsp; F fullscreen &nbsp;·&nbsp; S notes &nbsp;·&nbsp; D draw</p>',
            "About three hours, with the student's own project finished at home if needed. "
            "Parts 2 to 6 and every test need no Ollama.\nEvery output in this deck is a real "
            "run of the code on the slide before it.",
        )
    )
    add(
        sec(
            "2. GLANCE",
            "s-glance",
            '<h3>Today at a glance</h3>\n<ul class="kv">\n'
            '<div><span class="k">Format</span><span class="v">A 30-minute warm-up on Bayside, then your own database layer</span></div>\n'
            '<div><span class="k">Prerequisites</span><span class="v">Week 13 signed off; Week 12 tests passing</span></div>\n'
            '<div><span class="k">Needs</span><span class="v">The capstone venv; Ollama for Part 7 only</span></div>\n'
            '<div><span class="k">Submission</span><span class="v">GitHub URL in Canvas, at least 12 tests, completion credit</span></div>\n</ul>',
            "<strong>Essential today:</strong> the connection pattern, ? placeholders with "
            "tuples, rows as dicts, tmp_path tests, tools over database functions, the agent "
            "copied unchanged.\n<strong>Left out on purpose:</strong> JOINs, ORMs, two users at "
            "once (Week 15).",
        )
    )

    add(divider("3. PART 1", "Part 1", "Start", "Check last week before anything new."))
    add(
        shell_slide(
            "4. START",
            "Open the capstone folder",
            START,
            "Proposal approved; schema.sql reads twice with nothing printed the second time.",
            "Then run the Week 12 tests once: they must pass, because Part 6 copies four of its files.",
        )
    )

    add(
        divider(
            "5. PART 2",
            "Part 2",
            "Bayside warm-up",
            "In the practice folder, outside the capstone repo.",
        )
    )
    add(
        shell_slide(
            "6. FOLDER",
            "The practice folder",
            WARMUP_FOLDER,
            "Then paste the database.py, tools.py and test blocks from the lab page.",
            "The capstone venv stays active; the practice folder never reaches GitHub.",
        )
    )
    add(
        python_slide(
            "7. HELPERS",
            "database.py — first block",
            w.warmup_database_top(),
            "The connection pattern, three helpers, and create_tables.",
            "Point at the ? and the values tuple in each helper.",
        )
    )
    add(
        shell_slide(
            "8. SHELL",
            "Type each line in python3",
            "\n".join(w.WARMUP_SHELL),
            "The output is on the next slide.",
            "Ask the room to predict the last two lines before revealing them.",
        )
    )
    add(
        out_slide(
            "9. SHELL OUT",
            "What the shell prints",
            w.warmup_shell(),
            "A dict, None for the injection text, then an answer and a refusal.",
            "Same tool, same value: only the first history has the customer typing A100.",
        )
    )
    add(
        out_slide(
            "10. PYTEST OUT",
            "pytest -q",
            w.warmup_pytest(),
            "The tmp_path test passes without touching warmup.db.",
            "Each test gets its own empty folder.",
        )
    )

    add(
        divider(
            "11. PARTS 3-4",
            "Parts 3&ndash;4",
            "Your database.py and its tests",
            "Copy the helpers, write the rest.",
        )
    )
    add(
        idea(
            "12. MAP",
            "Bayside &rarr; yours",
            "The mapping table on the lab page",
            [
                "Copy <code>query_all</code>, <code>query_one</code>, <code>change</code>, <code>create_tables</code>",
                "One lookup by key for each business table",
                "add / find / waiting for change requests; approve and reject",
            ],
            "Approve is Week 13's Exercise 4 with placeholders and a still-waiting check.",
        )
    )
    add(
        warn(
            "13. TESTS",
            "At least 5 database tests",
            [
                "Tables twice, no duplicates; exact IDs; SQL text is just text",
                "A change waits; approve changes once; reject changes nothing",
                "Run pytest from the project folder",
            ],
            "create_tables opens schema.sql in the folder pytest runs from.",
        )
    )

    add(
        divider(
            "14. PART 5",
            "Part 5",
            "Your tools and their tests",
            "Week 12's door, your tools.",
        )
    )
    add(
        shell_slide(
            "15. DOOR HELPERS",
            "Copy these three as they are",
            "\n\n".join(
                w.app_method("tools.py", n) for n in ("clean", "words", "customer_said")
            ),
            "Whole words: A100 is not part of A1000.",
            "Then each tool method calls one database function, with an Args: docstring.",
        )
    )

    add(
        divider(
            "16. PART 6", "Part 6", "Agent and models", "Copy, then adapt two things."
        )
    )
    add(
        shell_slide(
            "17. COPY",
            "Copy from Week 12",
            COPY_MODELS,
            "Then: first line of agent.py, HANDOFF_WORDS, MAX_MESSAGES, keyword_model.py, settings.py.",
            "fallback_model.py comes from Week 12's Exercise 4, or from the lab page.",
        )
    )
    add(
        idea(
            "18. NOTICE",
            "The agent never noticed",
            "Concept",
            [
                "The tools class kept <code>tool_list</code> and <code>run</code>.",
                "So <code>agent.py</code> works on a database without a change.",
            ],
            "This is why Week 12 fixed the tools interface: the agent depends on two method names.",
        )
    )

    add(
        divider(
            "19. PARTS 7-8",
            "Parts 7&ndash;8",
            "main.py, ritual and push",
            "Run it twice.",
        )
    )
    add(
        shell_slide(
            "20. PUSH",
            "Ritual with Ollama switched off",
            PUSH,
            "At least 12 tests across the three files.",
            "If the tests pass with Ollama off here, they pass on the autograder.",
        )
    )
    add(
        quiz(
            "21. QUIZ",
            "Which of these is a tuple with one item?",
            [
                ("a", "(order_id)"),
                ("b", "(order_id,)"),
                ("c", "[order_id]"),
                ("d", "order_id,"),
            ],
            "b",
            "(order_id,) — the comma makes it a tuple; (order_id) is just order_id.",
            "One last check on the most common mistake of the week.",
        )
    )
    add(
        sec(
            "22. WRAP next",
            "s-wrap",
            "<h3>Where this goes next</h3>\n<p>&ldquo;Staff still can&rsquo;t approve anything "
            "without running Python. Next week they get a Staff tab of their own.&rdquo;</p>",
            "Week 15: Streamlit, a chat tab and a Staff tab over the same database functions.",
        )
    )
    add(
        sec(
            "23. END",
            "s-end",
            '<div class="sec-n">ISM3232 · Week 14</div>\n<h1>End of lab</h1>',
            "Every output in this deck is a real run of the lab page's own warm-up blocks.",
        )
    )

    template = (DOCS / "week13_lab_slides.html").read_text()
    start = template.index('<div class="slides">') + len('<div class="slides">')
    end = template.index("</div></div>", template.rindex("</section>"))
    before = re.sub(
        r"<title>.*?</title>",
        f"<title>ISM3232 Lab Week 14 — {w.TITLE}</title>",
        template[:start],
        count=1,
    )
    page = before + "\n\n" + "\n".join(s) + "\n" + template[end:]
    derived = [
        *SHOWN,
        START,
        WARMUP_FOLDER,
        COPY_MODELS,
        PUSH,
        "\n".join(w.WARMUP_SHELL),
        "\n\n".join(
            w.app_method("tools.py", n) for n in ("clean", "words", "customer_said")
        ),
    ]
    return page, derived


if __name__ == "__main__":
    page, _ = build()
    OUT.write_text(page)
    print("wrote", OUT)
