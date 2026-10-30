"""Build ism3232/docs/week15_lecture.html from the Bayside app at the Week 15
checkpoint, the saved browser session, and results generated with Streamlit's
test tool.

python reference/ism3232/builders/week15_lecture.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import week15_common as w
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
from week15_reading import SHOT_STYLE

OUT = DOCS / "week15_lecture.html"


def output(label, text):
    return code_block(label, text, python=False)


def build():
    results = w.warmup_results()
    steps = w.session_steps()
    typed = w.typed_shell()
    row = w.staff_row()
    p = []
    add = p.append

    add(SHOT_STYLE)
    add('<div class="wrap">')
    add(
        '<div style="font-family:var(--mono);font-size:11px;color:var(--muted);background:var(--bg2);'
        "border:1px solid var(--border);border-radius:6px;padding:8px 14px;margin-bottom:24px;"
        'display:flex;align-items:center;gap:10px;"><span style="opacity:.6;">&#x1F4CB;</span>'
        '<span><strong style="color:var(--text);">In-class page.</strong> Read the '
        '<a href="week15_reading.html" style="color:var(--muted);">Week 15 reading</a> first if you '
        "haven't. Follow along during the live session.</span></div>"
        f'<div class="page-eyebrow" style="color:{w.EYEBROW_COLOR};">{w.UNIT} · Module 15 · Lecture</div>'
    )
    add(f'<h1 class="wk-title">{w.TITLE}</h1>')
    add(
        '<p class="wk-deck">Give the agent a web page: a Chat tab for customers, a Staff tab '
        "for the people who approve, and the one rule that explains them both.</p>"
    )
    add(
        '<div class="meta">\n<span class="chip accent">Module 15 · Lecture</span>\n'
        f'<span class="chip">{w.UNIT}</span>\n<span class="chip">~75 min</span>\n</div>'
    )
    add(
        '<div class="weekjump">\n<span class="weekjump-label">This module:</span>\n'
        '<a href="week15_reading.html" class="weekjump-link">Reading</a>\n'
        '<a href="week15_lecture.html" class="weekjump-link current">Lecture</a>\n'
        '<a href="week15_lab.html" class="weekjump-link">Lab</a>\n</div>'
    )
    add(course_map("W15 "))
    add(
        callout_blue(
            "&#x1F9E0;",
            "This week &mdash; the agent gets a web page",
            "Week 14 put the agent on a database, but staff still decide in a terminal. "
            "Today Bayside&rsquo;s <code>app.py</code> gives customers a chat and staff a "
            "page of their own. Every result on this page is a real run of the code it "
            "shows, and the chat and the screenshot come from one real session on the "
            "course model.",
        )
    )

    add(section_divider("Session plan &mdash; 75 minutes"))
    add(
        concept_table(
            ["Minutes", "Segment", "What happens"],
            [
                [
                    "0&ndash;8",
                    "Where Week 14 left off",
                    "<code>main.py</code>&rsquo;s staff review in a terminal: who would use that?",
                ],
                [
                    "8&ndash;25",
                    "Reruns, live",
                    "The counter stuck at 1; <code>session_state</code>; the Week 11 callback",
                ],
                [
                    "25&ndash;45",
                    "The chat, live",
                    "Bayside&rsquo;s Chat tab on the course model; switching models keeps the chat",
                ],
                [
                    "45&ndash;60",
                    "The Staff tab, live",
                    "Approve the request filed in the chat; the notice; the report; restock",
                ],
                [
                    "60&ndash;68",
                    "Customer text is data",
                    "Markdown and a <code>$</code> in an address; why <code>st.text</code> matters",
                ],
                [
                    "68&ndash;75",
                    "Your project",
                    "The Bayside&rarr;yours map, three new database tests, next week",
                ],
            ],
        )
    )

    add(section_divider("Section 1 &mdash; Where Week 14 Left Off"))
    add(
        two_col(
            card(
                "The agent files requests",
                "<p>Every student&rsquo;s agent can file a change into "
                "<code>change_requests</code>, and the tools refuse values the customer "
                "never typed.</p>",
            ),
            card(
                "Staff decide in a terminal",
                "<p><code>main.py</code> asks yes or no about each request after the chat "
                "ends. Ask the room: who at a real shop would work like that?</p>",
            ),
        )
    )

    add(section_divider("Section 2 &mdash; Reruns, Live"))
    add(code_block("counter.py", w.WARMUP["counter.py"]))
    add(output("After 3 clicks the page shows", results["counter"]))
    add(
        card(
            "Say this",
            "<p>Streamlit runs the whole script again on every click, so "
            "<code>count = 0</code> runs again before the <code>if</code> adds one. Ask "
            "what they expect before you click.</p>",
        )
    )
    add(code_block("counter_state.py", w.WARMUP["counter_state.py"]))
    add(output("After 3 clicks the page shows", results["counter_state"]))
    add(output("After a browser refresh", results["fresh"]))
    add(
        card(
            "The Week 11 callback",
            "<p>The model remembers nothing, so the chatbot sends it the history every "
            "time. Streamlit remembers nothing either; <code>st.session_state</code> is "
            "the one thing it keeps between runs.</p>",
        )
    )

    add(section_divider("Section 3 &mdash; The Chat, Live"))
    add(code_block("app.py — the chatbot, created once", w.app_part("bot")))
    add(code_block("app.py — the Chat tab", w.app_part("chat")))
    add(output("The chat in the session", steps["chat"]))
    add(
        w.figure(
            "chat.png",
            "The same session&rsquo;s Chat tab, as a fallback if the demo fails.",
        )
    )
    add(
        card(
            "Do this",
            "<p>Mid-chat, switch the sidebar to keyword rules only and ask about an order. "
            "The conversation stays, because the chatbot is the same object; only "
            "<code>bot.model</code> changed.</p>",
        )
    )

    add(section_divider("Section 4 &mdash; The Staff Tab, Live"))
    add(code_block("app.py — the waiting requests", w.app_part("waiting")))
    add(output("The waiting request in the session", steps["staff waiting"]))
    add(output("After Approve", steps["staff approved"]))
    add(
        w.figure(
            "staff_approved.png",
            "After Approve in the same session: the notice, and A102 at its new address.",
        )
    )
    add(
        card(
            "Say this",
            "<p>The notice goes in <code>st.session_state</code> because Approve&rsquo;s run "
            "ends in <code>st.rerun()</code>. Then show the report (Week 13&rsquo;s "
            "<code>GROUP BY</code>) and restock one product with the form.</p>",
        )
    )

    add(section_divider("Section 5 &mdash; Customer Text Is Data"))
    add(output("Python shell", typed))
    add(output("The Staff tab draws", row))
    add(code_block("app.py — the model switch and show()", w.app_part("top")))
    add(
        card(
            "Say this",
            "<p>The row shows the link and the dollar signs exactly as typed, because it "
            "uses <code>st.text</code>. With <code>st.markdown</code> the customer would "
            "have planted a working link on the staff page. Then name the open limit: "
            "there is no sign-in, so anyone who opens the app can approve.</p>",
        )
    )

    add(section_divider("Section 6 &mdash; Your Project"))
    add(
        concept_table(
            ["Bayside", "Yours"],
            [
                [
                    "<code>status_report(db_file)</code>",
                    "a <code>GROUP BY</code> report over your main table",
                ],
                [
                    "<code>restock(db_file, name, stock)</code>",
                    "the one change your edit form makes",
                ],
                [
                    "<code>product_names(db_file)</code>",
                    "the dropdown&rsquo;s choices",
                ],
            ],
        )
    )
    add(
        card(
            "Three new tests",
            "<p>The report counts correctly; the edit changes the chosen row; the edit "
            "leaves the other rows alone. That makes 15 or more. <code>app.py</code> gets "
            "no tests: the autograder runs without Streamlit.</p>",
        )
    )
    add(
        prompt_list(
            [
                (
                    "Discussion 1: what staff may change",
                    (
                        "Which of your records should staff change on the Staff tab, and which "
                        "should change only through a request?"
                    ),
                    "Look for: a reason tied to who is affected and who is accountable.",
                ),
                (
                    "Discussion 2: session state",
                    "What would go wrong if the chatbot were created outside session_state?",
                    "Look for: a new chatbot, with an empty history, on every click.",
                ),
                (
                    "Discussion 3: the open limit",
                    (
                        "Who should be able to open your Staff tab, and how would a real "
                        "business make sure?"
                    ),
                    "Look for: a sign-in, and staff accounts kept apart from customers.",
                ),
            ]
        )
    )
    add(
        card(
            "Misconceptions to listen for",
            "<p>&ldquo;Streamlit keeps my variables between clicks.&rdquo; Only "
            "<code>st.session_state</code> does.</p>"
            "<p>&ldquo;The chat history is in the database.&rdquo; It is in "
            "<code>st.session_state</code>; a refresh clears it.</p>"
            "<p>&ldquo;I should test <code>app.py</code>.&rdquo; The autograder cannot; keep "
            "<code>app.py</code> thin.</p>"
            "<p>&ldquo;Reject deletes the request.&rdquo; It marks the request rejected.</p>",
        )
    )
    add(
        assignment(
            "Lab 15 &middot; Due end of Week 15 &middot; Streamlit Chat &amp; Staff",
            "Your agent in a web app",
            [
                (
                    "&#x1F40D;",
                    (
                        "<strong>Files:</strong> <code>app.py</code> with a Chat tab and a Staff "
                        "tab, and the new functions in <code>database.py</code>."
                    ),
                ),
                (
                    "&#x1F9EA;",
                    (
                        "<strong>Tests:</strong> at least 15 across "
                        "<code>tests/test_database.py</code>, <code>tests/test_tools.py</code> and "
                        "<code>tests/test_agent.py</code>, passing with Ollama switched off. No "
                        "test imports <code>app.py</code> or <code>ollama_model.py</code>."
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
        f'<div class="page-footer">ISM3232 &middot; Week 15 &middot; {w.TITLE}</div></div>'
    )

    head = head_from("week14_lecture.html", f"ISM3232 Week 15 — {w.TITLE_TEXT}")
    page = f'{head}\n<body>{"".join(p)}\n<script src="../site.js"></script>\n</body></html>\n'
    derived = [*results.values(), *w.WARMUP.values(), typed, row]
    return page, derived


if __name__ == "__main__":
    page, _ = build()
    OUT.write_text(page)
    print("wrote", OUT)
