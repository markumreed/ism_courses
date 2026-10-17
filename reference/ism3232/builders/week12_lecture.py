"""Build ism3232/docs/week12_lecture.html from the reference folder and saved runs.

python reference/ism3232/builders/week12_lecture.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import week12_common as w
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
    method,
    prev_next,
    prompt_list,
    section_divider,
    two_col,
)
from runs import words
from week12_reading import MAIN_INPUTS, typed

M = "module06_agents/"
G = w.GUIDED


OUT = DOCS / "week12_lecture.html"


def of(pair):
    return f"{words(pair[0])} out of {words(pair[1])}"


def build():
    c = w.counts()
    out = w.snippet_outputs()
    main_typed = typed(w.run_text("main_conversation.txt"), MAIN_INPUTS)
    no_guard = w.first_run("address_no_guard.txt")
    with_guard = w.first_run("address_with_guard.txt")
    off = typed(w.run_text("ollama_off.txt"), ["hello", "Where is order A100?", "quit"])
    p = []
    add = p.append

    add('<div class="wrap">')
    add(
        '<div style="font-family:var(--mono);font-size:11px;color:var(--muted);background:var(--bg2);'
        "border:1px solid var(--border);border-radius:6px;padding:8px 14px;margin-bottom:24px;"
        'display:flex;align-items:center;gap:10px;"><span style="opacity:.6;">&#x1F4CB;</span>'
        '<span><strong style="color:var(--text);">In-class page.</strong> Read the '
        '<a href="week12_reading.html" style="color:var(--muted);">Week 12 reading</a> first if you '
        "haven't. Follow along during the live session.</span></div>"
        f'<div class="page-eyebrow" style="color:{w.EYEBROW_COLOR};">{w.UNIT} · Module 12 · Lecture</div>'
    )
    add(f'<h1 class="wk-title">{w.TITLE}</h1>')
    add(
        '<p class="wk-deck">Let the model choose when to use a tool, check every request it makes, '
        "and make every change wait for a person.</p>"
    )
    add(
        '<div class="meta">\n<span class="chip accent">Module 12 · Lecture</span>\n'
        f'<span class="chip">{w.UNIT}</span>\n<span class="chip">~75 min</span>\n</div>'
    )
    add(
        '<div class="weekjump">\n<span class="weekjump-label">This module:</span>\n'
        '<a href="week12_reading.html" class="weekjump-link">Reading</a>\n'
        '<a href="week12_lecture.html" class="weekjump-link current">Lecture</a>\n'
        '<a href="week12_lab.html" class="weekjump-link">Lab</a>\n</div>'
    )
    add(course_map("W12 "))
    add(
        callout_blue(
            "&#x1F9E0;",
            "This week &mdash; the model gets to ask for tools",
            "Last week the rules decided when to use a tool, and they missed things. This week the "
            "model decides, your code checks every request, and anything that changes an order waits "
            "for a person. Every model output on this page is a real run of the course model; yours "
            "will be worded differently.",
        )
    )

    add(section_divider("Session plan &mdash; 75 minutes"))
    add(
        concept_table(
            ["Minutes", "Segment", "What happens"],
            [
                [
                    "0&ndash;10",
                    "Where Week 11 left off",
                    "A101, gift cards, and a history that hides who said what",
                ],
                [
                    "10&ndash;20",
                    "Tool calls",
                    "The model asks; your code decides. Docstrings become tool descriptions",
                ],
                [
                    "20&ndash;35",
                    "The tool loop",
                    "<code>decide</code>, <code>model_reply</code>, and a <code>tool</code> entry in the history",
                ],
                [
                    "35&ndash;50",
                    "One door",
                    "<code>Toolbox.run</code> and the made-up address",
                ],
                [
                    "50&ndash;60",
                    "Changes wait",
                    "<code>ChangeQueue</code>, staff review, one real conversation",
                ],
                [
                    "60&ndash;70",
                    "Stand-ins and tests",
                    "<code>KeywordModel</code>, <code>FakeModel</code>, tests that need no Ollama",
                ],
                [
                    "70&ndash;75",
                    "Wrap-up",
                    "What tools did not fix, and next week's problem",
                ],
            ],
        )
    )

    add(section_divider("Section 1 &mdash; Where Week 11 Left Off"))
    add(
        two_col(
            card(
                "The rules missed things",
                "<p><em>Has my package A101 shipped?</em> has no word <em>order</em>, so the order rule "
                "never ran and the model answered from memory. It once said A101 had shipped. It had not.</p>",
            ),
            card(
                "The rules caught too much",
                "<p><em>Do you sell gift cards?</em> contains <em>card</em>, so it went to a person "
                "without the model ever seeing it.</p>",
            ),
        )
    )
    add(
        card(
            "And nobody could tell who said what",
            "<p>Every reply in the history had the role <code>assistant</code>, whether a rule, a tool "
            "or the model wrote it. Today fixes the first and third problems, and keeps the second on "
            "purpose. By the end of the hour you will be able to say why.</p>",
        )
    )

    add(section_divider("Section 2 &mdash; Tool Calls"))
    add(
        card(
            "The model asks; your code decides",
            "<p>Along with the conversation, the chatbot now sends a list of <strong>tools</strong>. The "
            "model either writes a reply or sends back a <strong>tool call</strong>: a tool's name and the "
            "values to use. It never runs anything. Your code decides whether to run the tool.</p>",
        )
    )
    add(code_block("A decision is a dictionary", w.SNIPPETS["decision"]))
    add(code_block("Output", out["decision"], python=False))
    add(
        code_block(
            "order_tool.py &mdash; a method the model may ask for",
            method(M + "order_tool.py", "look_up_order", G),
        )
    )
    add(
        card(
            "What to notice",
            "<p>The first line of the docstring says what the tool does. The <code>Args:</code> section "
            "says what each value should look like. The <code>ollama</code> package reads both and "
            "builds the description the model sees.</p><p>Until today a docstring was for people. Now a "
            "program reads it too.</p>",
        )
    )

    add(section_divider("Section 3 &mdash; The Tool Loop"))
    add(
        code_block(
            "ollama_model.py &mdash; the new method, decide",
            method(M + "ollama_model.py", "decide", G),
        )
    )
    add(
        card(
            "Why a new method?",
            "<p><code>reply</code> returns text, and the Week 11 mini-project still calls it. A model "
            "that can ask for tools returns a decision, so it gets a second method and "
            "<code>reply</code> stays as it was.</p>",
        )
    )
    add(
        code_block(
            "chatbot.py &mdash; model_reply, write together",
            method(M + "chatbot.py", "model_reply", G),
        )
    )
    add(
        code_block(
            "Run it with a fake model that asks for the lookup", w.SNIPPETS["loop"]
        )
    )
    add(code_block("Output", out["loop"], python=False))
    add(
        card(
            "What to notice",
            "<p>Two trips to the model for one customer message: one to ask for the tool, one to answer. "
            "The middle line is the new <code>tool</code> entry. The model's reply and the tool's "
            "result are no longer mixed up.</p><p><code>rounds</code> stops a model that never "
            "answers. After three trips the customer goes to a person.</p>",
        )
    )
    add(
        code_block(
            "ollama_model.py &mdash; tool_messages",
            method(M + "ollama_model.py", "tool_messages", G),
        )
    )
    add(
        card(
            "Ollama needs to see its own request",
            f"<p>Store only the result and the model cannot tell it already asked. It asked for the same "
            f"lookup twice in {of(c['echo_off_repeats'])} runs of <em>Where is order A100?</em> "
            f"<code>tool_messages</code> turns one history entry into the two messages Ollama expects.</p>",
        )
    )

    add(section_divider("Section 4 &mdash; One Door"))
    add(
        code_block(
            "toolbox.py &mdash; run, the one door", method(M + "toolbox.py", "run", G)
        )
    )
    add(
        code_block(
            "toolbox.py &mdash; clean and customer_said",
            method(M + "toolbox.py", "clean", G)
            + "\n\n"
            + method(M + "toolbox.py", "customer_said", G),
        )
    )
    add(code_block("Try the door", w.SNIPPETS["door"]))
    add(code_block("Output", out["door"], python=False))
    add(
        code_block(
            f"With the check turned off &mdash; filed in {of(c['no_guard_filed'])} runs",
            no_guard,
            python=False,
        )
    )
    add(
        code_block(
            f"With the check on &mdash; refused in {of(c['with_guard_refused'])} runs",
            with_guard,
            python=False,
        )
    )
    add(
        card(
            "What to notice",
            "<p>Asked to change an address with no details, the model made up an order and an address. "
            "The check refused both, and the refusal told the model what to do next: ask the customer.</p>"
            "<p><code>.strip()</code> is new: it removes spaces from both ends. The empty check comes first "
            'because <code>"" in "any text"</code> is <code>True</code>; an empty address once got '
            "through an earlier version of this check.</p>",
        )
    )

    add(section_divider("Section 5 &mdash; Changes Wait for a Person"))
    add(
        code_block(
            "change_queue.py &mdash; the change tool only files a request",
            method(M + "change_queue.py", "request_address_change", G),
        )
    )
    add(
        code_block(
            "change_queue.py &mdash; approve is the only code that changes an order",
            method(M + "change_queue.py", "approve", G),
        )
    )
    add(code_block("Try the queue", w.SNIPPETS["queue"]))
    add(code_block("Output", out["queue"], python=False))
    add(
        code_block(
            "One real conversation with the real model", main_typed, python=False
        )
    )
    add(
        card(
            "What to notice",
            "<p>The model asked for the missing details, filed the change, and told the customer it "
            "would be reviewed. The address only changed when staff typed <code>yes</code>. "
            "<code>request_address_change</code> checks the order ID exactly: a lookup may find "
            "A100 inside A1000, a change may not. "
            "<em>Do you sell gift cards?</em> still went to a person.</p><p>Last week an address request "
            "ended the conversation. Now the chatbot collects the details and a person still decides.</p>",
        )
    )

    add(section_divider("Section 6 &mdash; Stand-ins and Tests"))
    add(
        two_col(
            card(
                "KeywordModel",
                "<p>Last week's keyword rules, moved out of the chatbot into a model with "
                "<code>decide</code>. It runs the chatbot without Ollama, and it still misses "
                "<em>Has my package A101 shipped?</em></p>",
            ),
            card(
                "FakeModel",
                "<p>Plays back the exact decisions a test gives it. A test can make the model ask for a "
                "tool that does not exist, send an empty address, or ask forever.</p>",
            ),
        )
    )
    add(code_block("The same chatbot with Ollama switched off", off, python=False))
    add(
        card(
            "A trade-off to name",
            "<p>Last week the order rule kept working when Ollama was down. Now that the model decides, "
            "a lookup needs the model too. Exercise 4 in the lab builds a model that falls back to the "
            "keyword rules when the real one has no answer.</p>",
        )
    )

    add(section_divider("Section 7 &mdash; What Tools Did Not Fix"))
    add(
        two_col(
            card(
                "Fixed",
                f"<p>A101 was answered from a lookup in {of(c['a101'])} runs.</p>",
            ),
            card(
                "Not fixed",
                f"<p>Told the store now closes at 11 pm, the model repeated it in {of(c['closing_agrees'])} "
                "runs. No tool knows the hours, so no tool is called.</p>",
            ),
        )
    )
    add(
        card(
            "Kept on purpose: gift cards",
            "<p>The payment rule still looks for <code>card</code> anywhere. Matching only the whole word "
            "would miss <em>Can I pay by card?</em> A gift-card question sent to a person costs a short "
            "wait; a missed payment question could put card details in front of the model. When a rule "
            "protects something, prefer false alarms.</p>",
        )
    )

    add(section_divider("What Is Essential, What Is Optional, What Is Left Out"))
    add(
        two_col(
            card(
                "Essential",
                "<p>Tool calls and docstrings, <code>decide</code>, the tool loop and its limit, the "
                "<code>tool</code> entry, the Toolbox checks, the change queue, <code>FakeModel</code> "
                "tests.</p>",
            ),
            card(
                "Optional enrichment",
                "<p>Why Ollama needs the model's own request (<code>tool_messages</code>), the "
                "fallback model (Exercise 4), turning a guardrail off to watch what happens (Exercise 3).</p>",
            ),
        )
    )
    add(
        card(
            "Left out on purpose",
            "<p>Several tool calls in one decision, streaming, online AI services, signing customers "
            "in, and data that lasts after the program stops (next week).</p>",
        )
    )

    add(section_divider("Discussion"))
    add(
        prompt_list(
            [
                (
                    "Discussion 1: who decides?",
                    (
                        "The model asked for <code>request_address_change</code> with an address nobody typed. "
                        "Whose job was it to stop that: the model's, the instructions', or the code's?"
                    ),
                    (
                        "Look for: the model cannot check itself; instructions help but do not guarantee; "
                        "the Toolbox check and the staff approval are code and people."
                    ),
                ),
                (
                    "Discussion 2: which tools need a person?",
                    (
                        "Bayside wants three more tools: show a product's price, cancel an order, and issue a "
                        "refund. Which ones may run straight away, and which must wait in the queue?"
                    ),
                    (
                        "Look for: looking something up changes nothing; anything that moves money or "
                        "changes an order waits for a person."
                    ),
                ),
                (
                    "Discussion 3: false alarms",
                    "Is it acceptable that <em>Do you sell gift cards?</em> goes to a person?",
                    (
                        "Look for: the cost of each kind of mistake; a protective rule should prefer the "
                        "cheap mistake."
                    ),
                ),
            ]
        )
    )
    add(
        card(
            "Misconceptions to listen for",
            "<p>“The model runs the tool.” It only asks; <code>run</code> does the work.</p>"
            "<p>“A good docstring makes the model safe.” It makes requests better. The checks make "
            "them safe.</p>"
            "<p>“If the tool exists, any request for it is fine.” A request can carry made-up values; "
            "that is what <code>customer_said</code> is for.</p>",
        )
    )
    add(
        card(
            "Where this goes next",
            "<p>Approved changes live in a Python list. Stop the program and they are gone. Next week "
            "you choose a business of your own, design its data, and keep it in a SQLite database. In "
            "Week 14 the database functions become the tools, and the chatbot you wrote today is copied "
            "over unchanged.</p>",
        )
    )
    add(
        assignment(
            "Assignment 12 &middot; Due end of Week 12 &middot; Tools and Guardrails",
            "A chatbot that asks for tools",
            [
                (
                    "&#x1F40D;",
                    (
                        "<strong>Files:</strong> <code>toolbox.py</code>, <code>change_queue.py</code>, "
                        "<code>keyword_model.py</code>, <code>fake_model.py</code>, and the updated chatbot, "
                        "tools and <code>ollama_model.py</code>."
                    ),
                ),
                (
                    "&#x1F9EA;",
                    "<strong>Tests:</strong> <code>tests/test_tools.py</code> and the new <code>tests/test_chatbot.py</code>, all passing with Ollama switched off.",
                ),
                (
                    "&#x1F4DD;",
                    "<strong>File:</strong> <code>week12_answers.md</code> with your answers to Exercises 1 and 3.",
                ),
                (
                    "&#x1F6E0;",
                    "<strong>Mini-project:</strong> your assistant, now choosing its own tool, with a request that waits for approval.",
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
        '<div class="page-footer">ISM3232 &middot; Week 12 &middot; Module 6 &mdash; Tools and '
        "Guardrails: Model-Chosen Tools, Checks, and Approval</div></div>"
    )

    head = head_from("week11_lecture.html", f"ISM3232 Week 12 — {w.TITLE_TEXT}")
    page = f'{head}\n<body>{"".join(p)}\n<script src="../site.js"></script>\n</body></html>\n'
    derived = [
        main_typed,
        no_guard,
        with_guard,
        off,
        *w.SNIPPETS.values(),
        *out.values(),
    ]
    derived.append(
        method(M + "toolbox.py", "clean", G)
        + "\n\n"
        + method(M + "toolbox.py", "customer_said", G)
    )
    return page, derived


if __name__ == "__main__":
    page, _ = build()
    OUT.write_text(page)
    print("wrote", OUT)
