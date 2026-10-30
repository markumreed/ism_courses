"""Build ism3232/docs/week15_slides.html (reveal.js deck) from the Bayside app at
the Week 15 checkpoint and the saved browser session. The counter slides show
what each app looks like after clicks; verify_week15 drives them again.

python reference/ism3232/builders/week15_slides.py
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import week15_common as w
from pagekit import (
    DOCS,
    esc,
    slide_code,
    slide_demo,
    slide_point,
    slide_section,
    slide_title,
    slides_shell,
)

OUT = DOCS / "week15_slides.html"


def shot(name, title, note):
    """A slide holding one screenshot from the saved session, the fallback for a demo."""
    return (
        f'<section class="s-code"><h3 style="color:var(--S);text-align:left;font-size:.52em;'
        f'margin-bottom:.25em;">{title}</h3><img src="../assets/img/week15/{name}" '
        f'alt="{esc(w.ALT[name])}" style="max-height:78vh;width:auto;border-radius:8px;">'
        f'<aside class="notes">{esc(note)}</aside></section>'
    )


def build():
    results = w.warmup_results()
    steps = w.session_steps()
    timings = [
        ("0–8 min", "Where Week 14 left off"),
        ("8–25 min", "Reruns"),
        ("25–45 min", "The chat"),
        ("45–60 min", "The Staff tab"),
        ("60–68 min", "Customer text is data"),
        ("68–75 min", "Your project"),
    ]
    s = []
    add = s.append
    add(
        slide_title(
            "Week 15",
            w.TITLE,
            timings,
            "Week 15 — Streamlit Chat & Staff\n\nToday's plan:\n"
            + "\n".join(f"  {t} — {what}" for t, what in timings)
            + "\n\nFrame it: the agent and the database work; today they get a web page. "
            "One idea explains the whole app: Streamlit runs the script again on every click.",
        )
    )

    add(slide_section(1, "Where Week 14 Left Off", "Staff decide in a terminal."))
    add(
        slide_point(
            "Who would use this?",
            [
                "The agent files change requests into <code>change_requests</code>",
                "<code>main.py</code> asks yes or no about each one after the chat ends",
                "Today: a Chat tab for customers and a Staff tab for staff",
            ],
            "Ask the room who at a real shop would approve requests in a terminal.",
        )
    )

    add(slide_section(2, "Reruns", "The counter that will not count."))
    add(
        slide_code(
            "counter.py",
            w.with_clicks(w.WARMUP["counter.py"], w.CLICKS, results["counter"]),
            "Ask what they expect after three clicks before you show it. Every click reruns "
            "the script, so count = 0 runs again.",
            size=".62em",
        )
    )
    add(
        slide_code(
            "counter_state.py",
            w.with_clicks(
                w.WARMUP["counter_state.py"], w.CLICKS, results["counter_state"]
            ),
            "st.session_state is the one thing Streamlit keeps between runs. A browser "
            f"refresh starts a new session: {results['fresh']}.",
            size=".62em",
        )
    )
    add(
        slide_point(
            "You have seen this before",
            [
                "Week 11: the model remembers nothing, so we send the history every time",
                "Streamlit remembers nothing either",
                "So the chatbot lives in <code>st.session_state</code>",
            ],
            "Connect the two ideas; this is the week's one rule.",
        )
    )

    add(slide_section(3, "The Chat", "One chatbot, kept between clicks."))
    add(
        slide_code(
            "The chatbot, created once",
            w.app_part("bot"),
            "Created on the first run only. The last line runs every time, so switching "
            "models keeps the conversation.",
        )
    )
    add(
        slide_code(
            "The Chat tab",
            w.app_part("chat"),
            "Draw the history, skipping tool entries; chat_input returns text only on the "
            "run after Enter; respond inside a spinner; rerun to draw the reply.",
            size=".62em",
        )
    )
    add(
        slide_demo(
            "streamlit run app.py",
            "Bayside on the course model: ask about A101, then change A102's address",
            "Run it live. If the demo fails, the next slide is the same session as a "
            "screenshot. Switch the sidebar to keyword rules mid-chat: the chat stays.",
        )
    )
    add(shot("chat.png", "The Chat tab", "A real session of the checkpoint app."))
    add(
        slide_code(
            "The chat in the session",
            steps["chat"],
            "The text of the screenshot, from the same session.",
            size=".6em",
            lang="plaintext",
        )
    )

    add(slide_section(4, "The Staff Tab", "A person decides."))
    add(
        slide_code(
            "The waiting requests",
            w.app_part("waiting"),
            "st.columns makes three columns; key= names each button; the notice goes in "
            "session_state because Approve's run ends in st.rerun().",
            size=".6em",
        )
    )
    add(
        slide_demo(
            "The Staff tab",
            "Approve the request the chat filed",
            "Approve it live; then show the report and restock one product.",
        )
    )
    add(
        shot(
            "staff_waiting.png",
            "Waiting for approval",
            "The request the agent filed, waiting for a person.",
        )
    )
    add(
        shot(
            "staff_approved.png",
            "After Approve",
            "The notice shows once; A102 has its new address.",
        )
    )
    add(
        slide_code(
            "Then the customer asks",
            steps["chat after approval"],
            "The agent does not remember the approval; check_request reads the database.",
            size=".6em",
            lang="plaintext",
        )
    )

    add(slide_section(5, "Customer Text Is Data", "Type something nasty."))
    add(
        slide_code(
            "A typed address",
            w.typed_shell(),
            "File a request whose address holds a Markdown link and two dollar signs.",
            size=".56em",
            lang="plaintext",
        )
    )
    add(
        slide_code(
            "The Staff tab draws",
            w.staff_row(),
            "st.text shows it exactly as typed. Then name the open limit: no sign-in, so "
            "anyone can approve.",
            size=".6em",
            lang="plaintext",
        )
    )

    add(slide_section(6, "Your Project", "Bayside to yours."))
    add(
        slide_point(
            "Bayside to yours",
            [
                "<code>status_report</code> &rarr; a <code>GROUP BY</code> report over your main table",
                "<code>restock</code> &rarr; the one change your edit form makes",
                (
                    "Three new tests: the report counts, the edit changes its row, the edit "
                    "leaves the others alone"
                ),
                "15 or more tests; none for <code>app.py</code>",
            ],
            "Point to the lab's mapping tables.",
        )
    )
    add(
        slide_point(
            "Next week",
            [
                "The app runs.",
                "Week 16: how often is it right?",
            ],
            "End on the question the next week answers.",
        )
    )

    before, after = slides_shell("week14_slides.html")
    before = re.sub(
        r"<title>.*?</title>",
        f"<title>ISM3232 Week 15 — {w.TITLE}</title>",
        before,
        count=1,
    )
    page = before + "\n" + "\n".join(s) + after
    derived = [
        w.with_clicks(w.WARMUP["counter.py"], w.CLICKS, results["counter"]),
        w.with_clicks(w.WARMUP["counter_state.py"], w.CLICKS, results["counter_state"]),
        w.typed_shell(),
        w.staff_row(),
    ]
    return page, derived


if __name__ == "__main__":
    page, _ = build()
    OUT.write_text(page)
    print("wrote", OUT)
