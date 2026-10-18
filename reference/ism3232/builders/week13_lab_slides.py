"""Build ism3232/docs/week13_lab_slides.html (the lab's reveal.js deck) from
Bayside's schema.sql and the saved sqlite3 sessions in runs/week13/. Shell
blocks are read-only, and each is followed by its captured output.

python reference/ism3232/builders/week13_lab_slides.py
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import week13_common as w
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
from week13_lab import CHECK, GITHUB, INSTALL_UBUNTU, OPEN, PRACTICE_FOLDER, PUSH, SETUP
from week13_starters import CHECKLIST

OUT = DOCS / "week13_lab_slides.html"


def shell_slide(comment, title, code, expect, notes):
    return code_slide(comment, title, code, expect, notes, readonly=True, lang="shell")


def build():
    SHOWN.clear()
    timings = [
        ("0:00–0:10", "Part 1 — Install sqlite3"),
        ("0:10–0:30", "Part 2 — Practise on Bayside"),
        ("0:30–1:00", "Part 3 — Four SQL exercises"),
        ("1:00–1:15", "Part 4 — Set up your capstone folder"),
        ("1:15–2:00", "Part 5 — Choose a business, write PROPOSAL.md"),
        ("2:00–2:30", "Part 6 — Write and check schema.sql"),
        ("2:30–3:00", "Parts 7–8 — Sign-off, commit and push"),
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
            f'<p class="eyebrow">ISM3232 &nbsp;·&nbsp; Week 13 &nbsp;·&nbsp; Module 13 &nbsp;·&nbsp; {w.UNIT}</p>\n'
            f'<h1>{w.TITLE}</h1>\n<div class="t-bar">\n{bar}\n</div>\n'
            '<p class="hint">&larr; &rarr; navigate &nbsp;·&nbsp; F fullscreen &nbsp;·&nbsp; S notes &nbsp;·&nbsp; D draw</p>',
            "About three hours, with the proposal and schema finished on their own if needed. No "
            "Ollama and no Python today: the terminal and the sqlite3 shell only.\n"
            "Every sqlite3 output in this deck is a real session of the sqlite3 Ubuntu installs. "
            "A Mac may space columns a little differently; the rows are the same.",
        )
    )
    add(
        sec(
            "2. GLANCE",
            "s-glance",
            '<h3>Today at a glance</h3>\n<ul class="kv">\n'
            '<div><span class="k">Format</span><span class="v">Practise SQL together, then start your own capstone</span></div>\n'
            '<div><span class="k">Prerequisites</span><span class="v">Week 12 pushed; the Week 13 reading</span></div>\n'
            '<div><span class="k">Needs</span><span class="v">The sqlite3 shell (Part 1 installs it)</span></div>\n'
            '<div><span class="k">Submission</span><span class="v">GitHub URL in Canvas; sign-off marks Approved or Revise</span></div>\n</ul>',
            "<strong>Essential today:</strong> .read, SELECT with WHERE and ORDER BY, GROUP BY, "
            "UPDATE with WHERE, a proposal that meets the checklist, a schema that reads twice "
            "without duplicates.\n<strong>Left out on purpose:</strong> JOINs, foreign keys, "
            "indexes, Python (Week 14).",
        )
    )

    add(
        divider(
            "3. PART 1",
            "Part 1",
            "Install sqlite3",
            "Most students need only the apt line.",
        )
    )
    add(
        shell_slide(
            "4. INSTALL",
            "Install sqlite3 (Ubuntu / WSL)",
            INSTALL_UBUNTU,
            "On a Mac, only the last line: sqlite3 is already installed.",
            "Walk the room for apt password prompts. WSL users type their Ubuntu password, not "
            "their Windows one.",
        )
    )
    add(
        out_slide(
            "5. VERSION",
            "What the last line prints",
            w.run_text("version"),
            "Your version and date may differ.",
            "Any 3.x version works for this course.",
        )
    )

    add(
        divider(
            "6. PART 2", "Part 2", "Practise on Bayside", "Outside the capstone folder."
        )
    )
    add(
        shell_slide(
            "7. FOLDER",
            "A practice folder with Bayside&rsquo;s schema",
            PRACTICE_FOLDER,
            "Paste schema.sql from the lab page, save it, then open the database.",
            "The practice database stays out of the capstone repository on purpose.",
        )
    )
    add(
        shell_slide(
            "8. OPEN",
            "Open the database, then type each line",
            OPEN + "\n\n" + w.typed("lab", "practice"),
            "The first line runs in the terminal; the rest at the sqlite&gt; prompt.",
            "Point out the dot-commands versus SQL: the semicolon ends SQL.",
        )
    )
    add(
        out_slide(
            "9. PRACTICE OUT",
            "What you should see",
            w.chunk("lab", "practice"),
            "Six orders, A100 to A105.",
            "If .tables prints nothing, schema.sql was not saved in this folder.",
        )
    )
    add(
        warn(
            "10. QUIT",
            "Leaving and coming back",
            [
                "<code>.quit</code> leaves sqlite3. The database file keeps everything.",
                "Keep this window open for Part 3: the exercises build on each other.",
            ],
            "A common worry is losing work by quitting; there is nothing to save.",
        )
    )

    add(divider("11. PART 3", "Part 3", "Four SQL exercises", "Same window, in order."))
    exercises = [
        (
            "ex1",
            "Exercise 1 — Orders still processing",
            "Order ID and customer of every processing order, sorted by customer.",
        ),
        (
            "ex2",
            "Exercise 2 — Out of stock",
            "Name and price of every product with no stock.",
        ),
        (
            "ex3",
            "Exercise 3 — Orders by status",
            "First add order A106 (given on the lab page), then count orders in each status.",
        ),
    ]
    number = 12
    for part, title, prompt in exercises:
        add(
            idea(
                f"{number}. {part.upper()} PROMPT",
                title,
                "Try it",
                [prompt],
                "Give students five minutes before showing the answer.",
            )
        )
        if part == "ex3":
            add(
                shell_slide(
                    f"{number + 1}. EX3 GIVEN",
                    "Exercise 3 — first add this order",
                    w.A106,
                    "An INSERT prints nothing.",
                    "This makes the counts unequal, so a wrong query cannot match by luck.",
                )
            )
            number += 1
        add(
            shell_slide(
                f"{number + 1}. {part.upper()} ANSWER",
                f"{title}: answer",
                w.typed("lab", part),
                "Then the output on the next slide.",
                "Ask a student to read the query aloud before you reveal the output.",
            )
        )
        add(
            out_slide(
                f"{number + 2}. {part.upper()} OUT",
                f"{title}: output",
                w.chunk("lab", part),
                "Compare with the expected box on the lab page.",
                "Common mistakes: missing quotes around text values; comparing stock with '0'.",
            )
        )
        number += 3
    add(
        idea(
            f"{number}. EX4 PROMPT",
            "Exercise 4 — Approve a change by hand",
            "Try it",
            [
                "Type the request the agent filed (on the lab page).",
                (
                    "Write two UPDATEs: change A101&rsquo;s address to 9 Pine Street, Tampa, and mark "
                    "request 1 approved."
                ),
                "Check with the two SELECTs on the lab page.",
            ],
            "This is the SQL approve_request runs in Week 14. Let them struggle a little.",
        )
    )
    add(
        shell_slide(
            f"{number + 1}. EX4 GIVEN",
            "Exercise 4 — the request the agent filed",
            w.A101_REQUEST,
            "Typed twice? Then there is a request 2 as well; approve request 1.",
            "AUTOINCREMENT gives every insert a new number.",
        )
    )
    add(
        shell_slide(
            f"{number + 2}. EX4 ANSWER",
            "Exercise 4: answer",
            w.typed("lab", "ex4"),
            "Each UPDATE has a WHERE, so exactly one row changes.",
            "In Week 14 these two statements become approve_request.",
        )
    )
    add(
        out_slide(
            f"{number + 3}. EX4 OUT",
            "Exercise 4: check",
            w.chunk("lab", "ex4_check"),
            "A101 has the new address; request 1 is approved.",
            "If the address did not change, the WHERE did not match: check the quotes and the ID.",
        )
    )
    number += 4

    add(
        divider(
            f"{number}. PART 4",
            "Part 4",
            "Set up your capstone folder",
            "One repository per module.",
        )
    )
    add(
        shell_slide(
            f"{number + 1}. SETUP",
            "module07_final_project",
            SETUP,
            "Quit sqlite3 first. mkdir -p is safe if the folder exists.",
            "The folder was made in Week 1. Check that .gitignore holds three lines.",
        )
    )
    add(
        shell_slide(
            f"{number + 2}. GITHUB",
            "One-time GitHub setup",
            GITHUB,
            "Public, so it can be graded by cloning.",
            "Same pattern as Week 4's first push.",
        )
    )
    add(
        idea(
            f"{number + 3}. GITIGNORE",
            "Why *.db is ignored",
            "Concept",
            [
                "The database is rebuilt from <code>schema.sql</code> every time.",
                "Real data never goes to GitHub.",
            ],
            "Connect to Week 14: the app runs schema.sql on every start.",
        )
    )
    number += 4

    add(
        divider(
            f"{number}. PART 5",
            "Part 5",
            "Choose a business, write PROPOSAL.md",
            "The longest part.",
        )
    )
    add(
        idea(
            f"{number + 1}. CHECKLIST",
            "The checklist",
            "Sign-off checks these eight items",
            [f"{i}. {item}" for i, item in enumerate(CHECKLIST, 1)],
            "Starters or their own idea; the checklist is the same.",
        )
    )
    add(
        idea(
            f"{number + 2}. ARROWS",
            "Every section becomes code",
            "The template&rsquo;s arrows",
            [
                "Tables &rarr; schema.sql today",
                "Tools, handoff words, instructions &rarr; Week 14",
                "Change tool &rarr; the Staff tab, Week 15",
                "Five conversations &rarr; evaluation cases, Week 16",
            ],
            "At sign-off, ask: what will you put in tools.py for this section?",
        )
    )
    number += 3

    add(
        divider(
            f"{number}. PART 6",
            "Part 6",
            "Write and check schema.sql",
            "Read it twice.",
        )
    )
    add(
        shell_slide(
            f"{number + 1}. CHECK",
            "Check your schema",
            CHECK,
            "Use your business&rsquo;s name and your own table names.",
            "The counts after the second .read must match the first.",
        )
    )
    add(
        out_slide(
            f"{number + 2}. BAYSIDE CHECK",
            "What Bayside&rsquo;s check looks like",
            w.chunk("read_twice", "first")
            + "\n"
            + w.chunk("read_twice", "delete")
            + "\n"
            + w.chunk("read_twice", "again"),
            "Six, five after a DELETE, six again.",
            "A deleted sample row comes back; that is INSERT OR IGNORE doing its job.",
        )
    )
    add(
        warn(
            f"{number + 3}. NO SAMPLE REQUESTS",
            "change_requests starts empty",
            [
                (
                    "AUTOINCREMENT gives every insert a new number, so INSERT OR IGNORE never sees a "
                    "repeat."
                ),
                "Sample requests would be added again on every start.",
            ],
            "Show requests_twice from the reading if a student asks why.",
        )
    )
    number += 4

    add(
        divider(
            f"{number}. PARTS 7-8",
            "Parts 7&ndash;8",
            "Sign-off, commit and push",
            "Two minutes each.",
        )
    )
    add(
        idea(
            f"{number + 1}. SIGNOFF",
            "Sign-off",
            "At your laptop",
            [
                "Show PROPOSAL.md and the two .read runs.",
                "Canvas: Approved, or Revise with a comment.",
                "Revise: fix it before the Week 14 lab.",
            ],
            "Keep each sign-off to one or two minutes: the checklist is the whole test.",
        )
    )
    add(
        shell_slide(
            f"{number + 2}. PUSH",
            "Your capstone&rsquo;s first commit",
            PUSH,
            "After this first push, git push is enough.",
            "No ruff or pytest this week: pytest finds no tests and exits with code 5, which "
            "stops the chain before git.",
        )
    )
    add(
        quiz(
            f"{number + 3}. QUIZ",
            "What does an UPDATE without WHERE change?",
            [
                ("a", "Nothing"),
                ("b", "The first row"),
                ("c", "Every row"),
                ("d", "Only rows with NULL"),
            ],
            "c",
            "Every row in the table, with no warning and no undo.",
            "One last check before they leave.",
        )
    )
    add(
        sec(
            f"{number + 4}. WRAP next",
            "s-wrap",
            "<h3>Where this goes next</h3>\n<p>&ldquo;The database exists, but the agent cannot "
            "reach it. Next week these queries become Python functions, and the functions become "
            "the agent&rsquo;s tools.&rdquo;</p>",
            "Week 14: database.py and tools.py. Week 15: the Staff tab. Week 16: the five "
            "conversations become evaluation cases.",
        )
    )
    add(
        sec(
            f"{number + 5}. END",
            "s-end",
            '<div class="sec-n">ISM3232 · Week 13</div>\n<h1>End of lab</h1>',
            "Every sqlite3 output in this deck is a real session of sqlite3 3.45.1, the version "
            "Ubuntu 24.04 installs, run on a fresh copy of Bayside's schema.sql.",
        )
    )

    template = (DOCS / "week12_lab_slides.html").read_text()
    start = template.index('<div class="slides">') + len('<div class="slides">')
    end = template.index("</div></div>", template.rindex("</section>"))
    before = re.sub(
        r"<title>.*?</title>",
        f"<title>ISM3232 Lab Week 13 — {w.TITLE}</title>",
        template[:start],
        count=1,
    )
    page = before + "\n\n" + "\n".join(s) + "\n" + template[end:]
    derived = [
        *SHOWN,
        INSTALL_UBUNTU,
        PRACTICE_FOLDER,
        OPEN + "\n\n" + w.typed("lab", "practice"),
        SETUP,
        GITHUB,
        CHECK,
        PUSH,
        w.A106,
        w.A101_REQUEST,
        *[w.typed("lab", part) for part in ("ex1", "ex2", "ex3", "ex4")],
    ]
    return page, derived


if __name__ == "__main__":
    page, _ = build()
    OUT.write_text(page)
    print("wrote", OUT)
