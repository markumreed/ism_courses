"""Build ism3232/docs/week15_lab_slides.html (the lab's reveal.js deck). The
warm-up's results are real test-tool runs of the lab page's own files, and the
screenshots come from the saved browser session. Every Streamlit block is
static: Pyodide, which runs the deck's Python, has no Streamlit.

python reference/ism3232/builders/week15_lab_slides.py
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import week15_common as w
from pagekit import DOCS, esc
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
from week15_lab import FILE_REQUEST, PRACTICE, PUSH, RUN, RUN_APP, START

OUT = DOCS / "week15_lab_slides.html"


def static_slide(comment, title, code, expect, notes):
    return code_slide(comment, title, code, expect, notes, readonly=True, lang="shell")


def shot_slide(comment, title, name, notes):
    return sec(
        comment,
        "s-code",
        f'<h3>{title}</h3>\n<img src="../assets/img/week15/{name}" '
        f'alt="{esc(w.ALT[name])}" style="max-height:72vh;width:auto;border-radius:8px;">',
        notes,
    )


def build():
    SHOWN.clear()
    results = w.warmup_results()
    timings = [
        ("0:00–0:05", "Part 1 — Start"),
        ("0:05–0:35", "Part 2 — Rerun warm-up"),
        ("0:35–1:00", "Parts 3–4 — Database additions and three tests"),
        ("1:00–1:40", "Part 5 — app.py: sidebar and Chat tab"),
        ("1:40–2:20", "Part 6 — The Staff tab"),
        ("2:20–3:00", "Parts 7–8 — Round trip, ritual and push"),
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
            f'<p class="eyebrow">ISM3232 &nbsp;·&nbsp; Week 15 &nbsp;·&nbsp; Module 15 &nbsp;·&nbsp; {w.UNIT}</p>\n'
            f'<h1>{w.TITLE}</h1>\n<div class="t-bar">\n{bar}\n</div>\n'
            '<p class="hint">&larr; &rarr; navigate &nbsp;·&nbsp; F fullscreen &nbsp;·&nbsp; S notes &nbsp;·&nbsp; D draw</p>',
            "About three hours, with the student's own app finished at home if needed. "
            "Parts 1 to 6 and every test need no Ollama.\nEvery warm-up result in this "
            "deck is a real run of the lab page's own files.",
        )
    )
    add(
        sec(
            "2. GLANCE",
            "s-glance",
            '<h3>Today at a glance</h3>\n<ul class="kv">\n'
            '<div><span class="k">Format</span><span class="v">A 30-minute rerun warm-up, then your own app.py</span></div>\n'
            '<div><span class="k">Prerequisites</span><span class="v">Week 14 tests passing (12 or more)</span></div>\n'
            '<div><span class="k">Needs</span><span class="v">The capstone venv; Ollama optional (keyword-only mode runs the app)</span></div>\n'
            '<div><span class="k">Submission</span><span class="v">GitHub URL in Canvas, at least 15 tests, completion credit</span></div>\n</ul>',
            "<strong>Essential today:</strong> the rerun model, st.session_state, the "
            "Chat tab, the Staff tab with Approve and Reject, three new database tests.\n"
            "<strong>Left out on purpose:</strong> sign-in, streaming, deploying, caching.",
        )
    )

    add(divider("3. PART 1", "Part 1", "Start", "Check last week before anything new."))
    add(
        static_slide(
            "4. START",
            "Open your capstone folder",
            START,
            "pytest passes your Week 14 tests; streamlit version prints a number.",
            "Streamlit was installed in Week 13 with the other packages.",
        )
    )

    add(
        divider(
            "5. PART 2",
            "Part 2",
            "Rerun warm-up",
            "Three tiny apps in the practice folder.",
        )
    )
    add(
        static_slide(
            "6. COUNTER",
            "counter.py",
            w.WARMUP["counter.py"],
            f"{PRACTICE} first, then {RUN['counter.py']}. Click Add one three times.",
            "Ask the room what it will show before anyone clicks. The first streamlit run "
            "asks for an email: press Enter.",
        )
    )
    add(
        out_slide(
            "7. COUNTER OUT",
            "After three clicks",
            results["counter"],
            "Every click reruns the whole script, so count = 0 runs again.",
            "This is the week's one idea. Stop the server with Ctrl+C.",
        )
    )
    add(
        static_slide(
            "8. COUNTER STATE",
            "counter_state.py",
            w.WARMUP["counter_state.py"],
            f"{RUN['counter_state.py']}, three clicks, then a browser refresh.",
            "in, setting an attribute: the same as a dictionary and an object.",
        )
    )
    add(
        out_slide(
            "9. COUNTER STATE OUT",
            "Three clicks, then a refresh",
            f"{results['counter_state']}\n{results['fresh']}",
            "session_state survives clicks; a refresh starts a new session.",
            "Same as the chat later: a refresh clears it.",
        )
    )
    add(
        static_slide(
            "10. ECHO",
            "echo.py",
            w.WARMUP["echo.py"],
            f"{RUN['echo.py']}, then type two messages.",
            "The Chat tab's pattern without the agent.",
        )
    )
    add(
        out_slide(
            "11. ECHO OUT",
            "Four chat bubbles",
            results["echo"],
            "History in session_state, drawn by the loop, redrawn by st.rerun().",
            "Point at each line of echo.py as you read the bubbles.",
        )
    )
    add(
        idea(
            "12. IDEA",
            "Streamlit remembers nothing; session_state does",
            "Concept",
            [
                "Week 11: the model remembers nothing, so the history is sent every time.",
                (
                    "Streamlit remembers nothing either, so the chatbot lives in "
                    "<code>st.session_state</code>."
                ),
            ],
            "Everything in Parts 5 and 6 follows from this.",
        )
    )

    add(
        divider(
            "13. PARTS 3-4",
            "Parts 3&ndash;4",
            "Database additions and three tests",
            "A report, an edit, and their tests.",
        )
    )
    add(
        static_slide(
            "14. REPORT",
            "Bayside&rsquo;s report and edit",
            w.app_function("status_report") + "\n\n\n" + w.app_function("restock"),
            "Yours: a GROUP BY over your main table, and the one change your form makes.",
            "Use the mapping table on the lab page.",
        )
    )
    add(
        warn(
            "15. TESTS",
            "Three new tests, 15 or more in total",
            [
                "The report counts correctly",
                "The edit changes the chosen row",
                "The edit leaves the other rows alone",
            ],
            "No tests for app.py: the autograder runs without Streamlit.",
        )
    )

    add(
        divider(
            "16. PART 5",
            "Part 5",
            "Sidebar and Chat tab",
            "Bayside's blocks, your names.",
        )
    )
    add(
        static_slide(
            "17. BOT",
            "The chatbot, created once",
            w.app_part("bot"),
            "Created on the first run only; the model is set on every run.",
            "So switching models in the sidebar keeps the conversation.",
        )
    )
    add(
        static_slide(
            "18. CHAT",
            "The Chat tab",
            w.app_part("chat"),
            f"Then {RUN_APP}, keyword rules only, and look up one of your records.",
            "Tool entries are skipped; chat_input returns text only on the run after Enter.",
        )
    )
    add(
        shot_slide(
            "19. CHAT SHOT",
            "Bayside&rsquo;s Chat tab",
            "chat.png",
            "A real session of Bayside on the course model.",
        )
    )

    add(divider("20. PART 6", "Part 6", "The Staff tab", "A person decides."))
    add(
        static_slide(
            "21. WAITING",
            "The waiting requests",
            w.app_part("waiting"),
            "st.text for customer text; key= for each button; the notice in session_state.",
            "Then add the records table, your report, and your edit form.",
        )
    )
    add(
        shot_slide(
            "22. STAFF SHOT",
            "Waiting for approval",
            "staff_waiting.png",
            "The request the agent filed in the chat.",
        )
    )
    add(
        shot_slide(
            "23. APPROVED SHOT",
            "After Approve",
            "staff_approved.png",
            "The notice shows once; the record changed.",
        )
    )

    add(
        divider(
            "24. PARTS 7-8",
            "Parts 7&ndash;8",
            "Round trip, ritual and push",
            "File, approve, ask, refresh.",
        )
    )
    add(
        static_slide(
            "25. KEYWORD PATH",
            "Keyword rules only: file one yourself",
            FILE_REQUEST,
            "In python3 from your project folder, with the app running; then refresh the "
            "browser and approve.",
            "With Ollama, ask for the change in the chat instead. Everyone refreshes once.",
        )
    )
    add(
        static_slide(
            "26. PUSH",
            "Ritual with Ollama switched off",
            PUSH,
            "At least 15 tests across the three files.",
            "Stop the app first.",
        )
    )
    add(
        quiz(
            "27. QUIZ",
            "Which line keeps the chatbot between reruns?",
            [
                (
                    "a",
                    'bot = SupportChatbot("Sunny", INSTRUCTIONS, tools, KeywordModel())',
                ),
                ("b", 'if "bot" not in st.session_state:'),
                ("c", "bot.model = make_model(choice)"),
                ("d", "st.rerun()"),
            ],
            "b",
            "It creates the chatbot only on the first run; every later run reuses the one "
            "kept in st.session_state.",
            "One last check on the week's one idea.",
        )
    )
    add(
        sec(
            "28. WRAP next",
            "s-wrap",
            "<h3>Where this goes next</h3>\n<p>&ldquo;The app runs. Next week: how often is "
            "it right?&rdquo;</p>",
            "Week 16: evaluation, safety and the demo.",
        )
    )
    add(
        sec(
            "29. END",
            "s-end",
            '<div class="sec-n">ISM3232 · Week 15</div>\n<h1>End of lab</h1>',
            "Every warm-up result in this deck is a real run of the lab page's own files.",
        )
    )

    template = (DOCS / "week14_lab_slides.html").read_text()
    start = template.index('<div class="slides">') + len('<div class="slides">')
    end = template.index("</div></div>", template.rindex("</section>"))
    before = re.sub(
        r"<title>.*?</title>",
        f"<title>ISM3232 Lab Week 15 — {w.TITLE}</title>",
        template[:start],
        count=1,
    )
    page = before + "\n\n" + "\n".join(s) + "\n" + template[end:]
    derived = [
        *SHOWN,
        START,
        FILE_REQUEST,
        PUSH,
        *w.WARMUP.values(),
        w.app_function("status_report") + "\n\n\n" + w.app_function("restock"),
    ]
    return page, derived


if __name__ == "__main__":
    page, _ = build()
    OUT.write_text(page)
    print("wrote", OUT)
