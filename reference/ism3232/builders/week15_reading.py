"""Build ism3232/docs/week15_reading.html from the Bayside app at the Week 15
checkpoint (8b1b491), the saved browser session, and warm-up results generated
with Streamlit's test tool.

    python reference/ism3232/builders/week15_reading.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import week15_common as w
from pagekit import (
    DOCS,
    callout,
    coming_from,
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

OUT = DOCS / "week15_reading.html"
SHOT_STYLE = (
    "<style>.shot{margin:18px 0}.shot img{max-width:100%;height:auto;"
    "border:1px solid var(--border);border-radius:8px}.shot figcaption{font-size:13px;"
    "color:var(--muted);margin-top:6px}</style>"
)
RUN_APP = "streamlit run app.py"
RUN_COUNTER = "streamlit run counter.py"
SHOW_TEXT = "Total: $5 and $6"


def part(label, name):
    return listing(f"app.py — {label}", w.app_part(name))


def build():
    results = w.warmup_results()
    steps = w.session_steps()
    two_clicks = w.counter_after_clicks(w.WARMUP["counter_state.py"], 2)
    parts = []
    add = parts.append

    add(SHOT_STYLE)
    add(
        f'<div class="page-eyebrow" style="color:{w.EYEBROW_COLOR};">{w.UNIT} · Module 15 · Reading</div>'
    )
    add(f'<h1 class="wk-title">{w.TITLE}</h1>')
    add(
        '<p class="wk-deck">Put a web page in front of your agent: a Chat tab for '
        "customers and a Staff tab where people approve what the agent asked for.</p>"
    )
    add(
        '<div class="meta">\n<span class="chip accent">Module 15</span>\n'
        f'<span class="chip">{w.UNIT}</span>\n'
        '<span class="chip">Reading · Streamlit, session state &amp; approvals</span>\n</div>'
    )
    add(
        '<div class="weekjump">\n<span class="weekjump-label">This module:</span>\n'
        '<a href="week15_reading.html" class="weekjump-link current">Reading</a>\n'
        '<a href="week15_lecture.html" class="weekjump-link">Lecture</a>\n'
        '<a href="week15_lab.html" class="weekjump-link">Lab</a>\n</div>'
    )
    add(
        objective(
            "By the end of this reading you will be able to run a Streamlit app, explain "
            "why it runs your whole script again on every click, keep the agent alive "
            "between clicks with <code>st.session_state</code>, and build the two tabs of "
            "your capstone: a chat for customers and a staff page that approves or rejects "
            "what the agent filed."
        )
    )
    add(
        coming_from(
            "Coming from Week 14",
            "Staff still can&rsquo;t approve anything without running Python. Your agent "
            "files change requests into the database, and <code>main.py</code> asks about "
            "each one in a terminal after the chat ends. Nobody at a real business works "
            "like that. This week the same agent and the same database get a web page.",
        )
    )
    add(
        '<div style="font-family:var(--mono);font-size:11px;color:var(--muted);background:var(--bg2);'
        "border:1px solid var(--border);border-radius:6px;padding:8px 14px;margin-bottom:24px;"
        'display:flex;align-items:center;gap:10px;"><span style="opacity:.6;">&#x1F4D6;</span>'
        '<span><strong style="color:var(--text);">Pre-class reading.</strong> Read this before the '
        'session. The <a href="week15_lecture.html" style="color:var(--muted);">Lecture page</a> '
        "runs the same app live in class.</span></div>"
    )

    add("<h2>Module at a glance</h2>")
    add(
        term(
            "Time",
            "One week. Reading about 60 minutes, lecture 75 minutes, lab about 3 hours, "
            "then finishing your own app at home.",
        )
    )
    add(
        term(
            "Prerequisites",
            "Week 14 done: your capstone project passes its tests (12 or more).",
        )
    )
    add(
        term(
            "Materials",
            "Your capstone venv, which has had Streamlit since Week 13. Ollama is optional: "
            "the app has a keyword-only mode, and every test runs without it.",
        )
    )
    add("<h3>Learning outcomes</h3>")
    add(
        "<ol>"
        "<li>Run and stop a Streamlit app.</li>"
        "<li>Explain the rerun model.</li>"
        "<li>Keep objects between reruns with <code>st.session_state</code>.</li>"
        "<li>Build a chat with <code>st.chat_message</code> and <code>st.chat_input</code>.</li>"
        "<li>Lay out a page with a sidebar, tabs and columns.</li>"
        "<li>Show records and a <code>GROUP BY</code> report with <code>st.dataframe</code>.</li>"
        "<li>Use buttons and a form that change the database, then rerun.</li>"
        "<li>Show customer text safely.</li>"
        "</ol>"
    )

    add("<h2>What you build this week</h2>")
    add(
        "<p>This is Bayside&rsquo;s app, running on the course model. A customer asked two "
        "things in the Chat tab. The second one, an address change, did not change "
        "anything yet: the agent filed a request, and it waits on the Staff tab for a "
        "person. By the end of the lab your own business has the same two tabs.</p>"
    )
    add(
        w.figure(
            "chat.png",
            "The Chat tab, captured from a real session of Bayside&rsquo;s app.",
        )
    )

    add("<h2>Streamlit runs everything again</h2>")
    add(
        "<p>A Streamlit app is an ordinary Python script. You start it with "
        "<code>streamlit run</code>, and it draws the page in your browser. Here is the "
        "whole trick, and the one idea of this week: <strong>every time someone clicks a "
        "button or types a message, Streamlit runs your whole script again, from the top."
        "</strong> Watch what that does to a counter.</p>"
    )
    add(listing("counter.py", w.WARMUP["counter.py"]))
    add(listing("Terminal", RUN_COUNTER))
    add(listing("After 3 clicks the page shows", results["counter"]))
    add(
        "<p>The count is stuck at 1. Each click reruns the script, so <code>count = 0</code> "
        "runs again before the <code>if</code> adds one. Nothing you set in a normal "
        "variable survives a click.</p>"
    )
    add(
        "<p>Streamlit keeps exactly one thing between runs: <code>st.session_state</code>. "
        "It works like an object whose attributes stay put while the same browser tab is "
        "open.</p>"
    )
    add(listing("counter_state.py", w.WARMUP["counter_state.py"]))
    add(listing("After 3 clicks the page shows", results["counter_state"]))
    add(listing("After a browser refresh", results["fresh"]))
    add(
        "<ul>"
        '<li><code>"count" not in st.session_state</code> uses <code>in</code>, as with a '
        "dictionary: it is True only on the very first run.</li>"
        "<li><code>st.session_state.count = 0</code> sets an attribute, the way "
        "<code>self.history = []</code> did in Week 10.</li>"
        "<li>A browser refresh starts a new session, so the count goes back to 0.</li>"
        "</ul>"
    )
    add(
        callout(
            "concept",
            "You have seen this before",
            "<p>In Week 11 you learned that the model remembers nothing, so the chatbot "
            "sends it the whole history every time. Streamlit remembers nothing either. "
            "Anything that must last between clicks, such as the chatbot and its history, "
            "goes in <code>st.session_state</code>.</p>",
        )
    )

    add("<h2>The chat</h2>")
    add(
        "<p>Bayside&rsquo;s <code>app.py</code> is about 100 lines, and you will copy most "
        "of it. It starts with imports from the files you already have, then two small "
        "helpers.</p>"
    )
    add(part("imports", "imports"))
    add(part("the model switch and show()", "top"))
    add(
        "<p><code>make_model</code> turns the sidebar choice into a model: the course model "
        "with the keyword rules behind it, or the keyword rules alone. <code>show</code> "
        "writes text into the page. Streamlit reads a pair of <code>$</code> signs as "
        'math, so a price like $60.00 would come out garbled; <code>"\\\\$"</code> is a '
        "backslash and a dollar sign (a backslash in a string is written twice), and a "
        "backslash before <code>$</code> tells Streamlit to show a plain dollar sign.</p>"
    )
    add(part("the sidebar", "sidebar"))
    add(
        "<p><code>create_tables</code> runs on every rerun. That is safe, because your "
        "<code>schema.sql</code> uses <code>IF NOT EXISTS</code> and <code>INSERT OR IGNORE"
        "</code>. <code>st.sidebar.radio</code> draws the model choice in the sidebar and "
        "returns the one that is selected.</p>"
    )
    add(part("the chatbot, created once", "bot"))
    add(
        "<p>This is the counter&rsquo;s pattern with a chatbot instead of a number. The "
        "chatbot is created only on the first run and kept in <code>st.session_state.bot"
        "</code>, so its history survives every click. The last line runs every time: it "
        "gives the same chatbot whichever model the sidebar now asks for, which is why "
        "switching models keeps the conversation.</p>"
    )
    add(part("the tabs", "tabs"))
    add(
        "<p><code>st.tabs</code> returns one tab for each name, and "
        "<code>chat_tab, staff_tab = ...</code> unpacks them into two names in one line, "
        "first to first and second to second.</p>"
    )
    add(part("the Chat tab", "chat"))
    add(
        "<ul>"
        "<li><code>with chat_tab:</code> means &ldquo;put what this block draws inside the "
        "Chat tab&rdquo;. You know <code>with</code> from <code>with open(...)</code>; here "
        "it is used for page layout.</li>"
        "<li>The loop draws the history, skipping the tool entries a customer should not "
        "see. <code>st.chat_message</code> draws one speech bubble.</li>"
        "<li><code>st.chat_input</code> is the box at the bottom. It returns what the "
        "customer typed on the run right after they press Enter, and <code>None</code> on "
        "every other run.</li>"
        "<li><code>bot.respond</code> is the same method as in Week 12, inside "
        "<code>st.spinner</code> so the page says it is working. <code>st.rerun()</code> "
        "then starts a fresh run, which draws the history again with the new reply in "
        "it.</li>"
        "</ul>"
    )
    add(
        "<p>This is the text of the chat in the screenshot above, from the same session:</p>"
    )
    add(listing("The chat in the session", steps["chat"]))

    add("<h2>The Staff tab</h2>")
    add(
        "<p>The Staff tab is where a person decides. It starts with a notice and the "
        "requests that are waiting.</p>"
    )
    add(part("the notice", "notice"))
    add(part("the waiting requests", "waiting"))
    add(
        "<ul>"
        "<li>Clicking Approve reruns the script, and <code>st.rerun()</code> reruns it "
        "again, so a message written with <code>st.success</code> on the click&rsquo;s run "
        "would vanish at once. Instead the result goes into "
        "<code>st.session_state.notice</code>; the next run shows it, then "
        "<code>del st.session_state.notice</code> removes it so it shows only once.</li>"
        "<li><code>st.columns([4, 1, 1])</code> makes three columns side by side, the "
        "first four times as wide, and <code>text_col, approve_col, reject_col = ...</code> "
        "unpacks them.</li>"
        '<li><code>key=f"approve{number}"</code> is a keyword argument: it names each '
        "button, because two buttons both labelled Approve need different keys.</li>"
        "<li>The row is written with <code>st.text</code>, not <code>show</code>. More on "
        "why below.</li>"
        "</ul>"
    )
    add(
        w.figure(
            "staff_waiting.png",
            "The Staff tab in the same session, with the agent&rsquo;s request waiting.",
        )
    )
    add(part("the orders and the report", "tables"))
    add(listing("database.py", w.app_function("status_report")))
    add(
        "<p><code>st.dataframe</code> draws a list of dictionaries as a table. "
        "<code>status_report</code> is Week 13&rsquo;s <code>GROUP BY</code>, now inside a "
        "function: one row per status, with how many orders have it.</p>"
    )
    add(part("the restock form", "restock"))
    add(listing("database.py", w.app_function("restock")))
    add(listing("database.py", w.app_function("product_names")))
    add(
        "<p>Changing a dropdown would normally rerun the script at once. Inside "
        "<code>st.form</code>, nothing reruns until the form&rsquo;s own button is pressed, "
        "so staff can pick a product and type a number, then send both together. "
        "<code>min_value=0</code> and <code>step=1</code> are keyword arguments that stop "
        "the number going below zero.</p>"
    )

    add("<h2>One round trip</h2>")
    add(
        "<p>Here is the whole journey of one request, all from the same real session on "
        "the course model. First the customer asks, and the agent files a request:</p>"
    )
    add(listing("Chat tab", steps["chat"]))
    add(
        "<p>A member of staff opens the Staff tab and clicks Approve. The notice appears, "
        "nothing is waiting any more, and the order has its new address:</p>"
    )
    add(listing("Staff tab: the notice", steps["staff approved"]))
    add(listing("The orders table, read from bayside.db", steps["orders"]))
    add(
        w.figure(
            "staff_approved.png",
            "After Approve: the notice, and A102 at its new address.",
        )
    )
    add(
        "<p>Back in the Chat tab, the customer asks what happened. The agent does not "
        "remember the approval; it looks the request up with <code>check_request</code>, "
        "so the answer comes from the database:</p>"
    )
    add(listing("Chat tab", steps["chat after approval"]))
    add(
        "<p>Finally, a browser refresh. A refresh starts a new session, so "
        "<code>st.session_state</code> is empty and the chat is gone. The address change "
        "is still in <code>bayside.db</code>.</p>"
    )
    add(listing("After a browser refresh", steps["after a refresh"]))

    add("<h2>Customer text is data</h2>")
    add(
        "<p>The address on a request is whatever the customer typed. If the Staff tab drew "
        "it with <code>st.markdown</code>, a customer could type <code>[click me]"
        "(https://example.com)</code> and plant a link on the staff page, or type "
        "<code>$5 and $6</code> and garble it. <code>st.text</code> shows text exactly as "
        "typed, so the request row can never format the page. The chat uses "
        "<code>show</code>, which escapes <code>$</code> but still allows ordinary "
        "formatting, because there both sides are talking to each other.</p>"
    )
    add(
        callout(
            "warn",
            "The open limit",
            "<p>Anyone who opens this app can click Approve: there is no sign-in, so the "
            "Staff tab is open to customers too. A real business would put staff behind a "
            "login. This course leaves that out (see below), but you should be able to say "
            "it is the app&rsquo;s biggest gap.</p>",
        )
    )

    add("<h2>Running it</h2>")
    add(listing("Terminal", RUN_APP))
    add(
        "<ul>"
        "<li>The very first time you run Streamlit, it stops at &ldquo;Welcome to "
        "Streamlit!&rdquo; and asks for an email address. Press Enter to skip it.</li>"
        "<li>Open <code>http://localhost:8501</code>. In WSL, open that address in your "
        "Windows browser.</li>"
        "<li>Ctrl+C in the terminal stops the server.</li>"
        "<li>A browser refresh clears the chat. The database keeps every request and "
        "decision.</li>"
        "<li>With Ollama off, the default sidebar choice falls back to the keyword rules, "
        "or you can pick keyword rules only. They can look up orders and stock, but they "
        "cannot file a change request. To try the Staff tab without Ollama, file a request "
        "from <code>python3</code> with <code>add_change_request</code>, as in Week 14.</li>"
        "</ul>"
    )

    add("<h2>Why app.py has no tests</h2>")
    add(
        "<p>The autograder runs your tests without Streamlit or Ollama installed. So "
        "<code>app.py</code> stays thin: it draws things and calls functions, and every "
        "decision lives in <code>database.py</code>, <code>tools.py</code> and "
        "<code>agent.py</code>, which your tests already cover. The new database functions "
        "the Staff tab needs get tests of their own. Bayside&rsquo;s two are the models for "
        "yours:</p>"
    )
    add(
        listing(
            "tests/test_database.py", w.app_test("test_status_report_counts_orders")
        )
    )
    add(listing("tests/test_database.py", w.app_test("test_restock")))

    add("<h2>What this module leaves out, and why</h2>")
    add(
        "<ul>"
        "<li><strong>Staff sign-in.</strong> Accounts and passwords are a course of their "
        "own; the pages name the gap instead.</li>"
        "<li><strong>Streaming replies.</strong> The reply arrives whole after the spinner; "
        "streaming adds a new kind of function for little gain here.</li>"
        "<li><strong>Deploying online.</strong> The model runs on your laptop, so the app "
        "does too.</li>"
        "<li><strong>Caching.</strong> The Staff tab must always show fresh data, and the "
        "database is small.</li>"
        "<li><strong>FastAPI.</strong> The capstone has no second program that needs to "
        "talk to it.</li>"
        "</ul>"
    )

    add("<h2>Key terms</h2>")
    for word, definition in [
        (
            "Rerun",
            "Streamlit running the whole script again after a click or a message.",
        ),
        ("Session state", "st.session_state: the one place values survive reruns."),
        ("Widget", "Something a person uses on the page: a button, a box, a dropdown."),
        ("Chat message", "One speech bubble, drawn with st.chat_message."),
        ("Tab", "One of the page&rsquo;s sections, made with st.tabs."),
        ("Column", "A side-by-side slice of the page, made with st.columns."),
        ("Form", "A group of widgets that reruns only when its button is pressed."),
        ("Dataframe", "The table st.dataframe draws from a list of dictionaries."),
        ("Widget key", "The key= name that tells two look-alike widgets apart."),
    ]:
        add(term(word, definition))

    add("<h2>Before you leave this week</h2>")
    add(
        '<ul class="checklist">'
        "<li>Can explain why the plain counter stays at 1</li>"
        "<li>Can explain why the chatbot lives in <code>st.session_state</code></li>"
        "<li>Your app has a Chat tab and a Staff tab on your own database</li>"
        "<li>Approve and Reject work, and the notice shows once</li>"
        "<li>Customer text on the Staff tab uses <code>st.text</code></li>"
        "<li>At least 15 tests pass with Ollama switched off</li>"
        "<li>Lab 15 submitted via GitHub URL</li></ul>"
    )

    add('<h2 id="quiz">Module Quiz</h2>')
    quiz = [
        quiz_mc(
            1,
            "A counter shows Count: 1 after three clicks. Why?",
            [
                (
                    "Streamlit runs the whole script again on every click, so count = 0 runs "
                    "again"
                ),
                "The button works only once",
                "st.write keeps the first value it showed",
                "The browser ignores repeated clicks",
            ],
            0,
            "Every click reruns the script from the top. Only st.session_state keeps a "
            "value between runs.",
        ),
        quiz_tf(
            2,
            "Refreshing the browser clears the chat but keeps an approved change.",
            True,
            "The chat lives in st.session_state, which starts empty in a new session. The "
            "decision is in the database.",
        ),
        quiz_trace(
            3,
            "What does the page show after two clicks?",
            w.WARMUP["counter_state.py"],
            two_clicks,
            "st.session_state.count survives each rerun, so each click adds one to the "
            "kept value.",
        ),
        quiz_mc(
            4,
            "Why does app.py create the chatbot inside "
            '<code>if "bot" not in st.session_state:</code>?',
            [
                "So the same chatbot, with its history, is used on every rerun",
                "So the chatbot answers faster",
                "Because a SupportChatbot can only be created once",
                "So the database is created only once",
            ],
            0,
            "Without it, every rerun would build a new chatbot with an empty history.",
        ),
        quiz_mc(
            5,
            "Why does the Staff tab show each request with <code>st.text</code>?",
            [
                "So text a customer typed cannot format the page or add a link",
                "st.text is faster than st.markdown",
                "st.markdown cannot show numbers",
                "st.text saves the request",
            ],
            0,
            "Customer text is data. st.text shows it exactly as typed.",
        ),
        quiz_tf(
            6,
            "Clicking Reject deletes the change request.",
            False,
            "It marks the request rejected. The order does not change, and the request "
            "cannot be approved later.",
        ),
        quiz_mc(
            7,
            "Why does app.py have no tests?",
            [
                (
                    "The autograder runs without Streamlit, so the logic lives in tested files "
                    "and app.py stays thin"
                ),
                "Streamlit apps cannot be tested at all",
                "app.py never changes",
                "pytest cannot import a file named app.py",
            ],
            0,
            "Every decision is in database.py, tools.py and agent.py, which the tests "
            "cover.",
        ),
        quiz_mc(
            8,
            "What does <code>st.form</code> change about the restock inputs?",
            [
                "Nothing reruns until the form&rsquo;s submit button is pressed",
                "The inputs are saved to the database by themselves",
                "The form clears the table first",
                "The form keeps its values after a refresh",
            ],
            0,
            "Changing the dropdown or the number waits; Save sends both at once.",
        ),
        quiz_trace(
            9,
            "What does Bayside&rsquo;s <code>show()</code> pass to st.markdown for this "
            "text?",
            f'show("{SHOW_TEXT}")',
            SHOW_TEXT.replace("$", "\\$"),
            "Each $ gets a backslash, so Streamlit shows a dollar sign instead of reading "
            "$5 and $6 as math.",
        ),
        quiz_short(
            10,
            "Anyone who opens the Bayside app can approve a request. What would a real "
            "business add, and why does Week 15 leave it out?",
            "A staff sign-in, so only staff can open the Staff tab and approve. It is left "
            "out to keep the course on the agent and its data, and the pages name it as "
            "the app&rsquo;s open limit.",
        ),
    ]
    add("\n".join(quiz))
    add("<p>The app runs. Next week: how often is it right?</p>")
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
        f'<div class="page-footer">ISM3232 &nbsp;·&nbsp; Week 15 &nbsp;·&nbsp; {w.TITLE}</div>'
    )

    head = head_from("week14_reading.html", f"ISM3232 Week 15 — {w.TITLE_TEXT}")
    body = "\n".join(parts)
    page = (
        f'{head}\n<body>\n{body}\n<script src="../site.js"></script>\n</body></html>\n'
    )
    return page, [*results.values(), *w.WARMUP.values(), RUN_APP, RUN_COUNTER]


if __name__ == "__main__":
    page, _ = build()
    OUT.write_text(page)
    print("wrote", OUT)
