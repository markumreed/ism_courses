"""Build ism3232/docs/week12_slides.html (reveal.js deck) from the reference folder.

python reference/ism3232/builders/week12_slides.py
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import week12_common as w
from pagekit import (
    DOCS,
    method,
    slide_chalk,
    slide_code,
    slide_demo,
    slide_point,
    slide_section,
    slide_title,
    slides_shell,
    with_output,
)
from runs import words

M = "module06_agents/"
G = w.GUIDED


def of(pair):
    return f"{words(pair[0])} out of {words(pair[1])}"


def build():
    c = w.counts()
    out = w.snippet_outputs()
    timings = [
        ("0–10 min", "Where Week 11 left off"),
        ("10–20 min", "Tool calls"),
        ("20–35 min", "The tool loop"),
        ("35–50 min", "One door"),
        ("50–60 min", "Changes wait for a person"),
        ("60–70 min", "Stand-ins and tests"),
        ("70–75 min", "What tools did not fix"),
    ]
    blocks = {name: with_output(w.SNIPPETS[name], out[name]) for name in w.SNIPPETS}
    s = []
    add = s.append
    add(
        slide_title(
            "Week 12",
            w.TITLE,
            timings,
            "Week 12 — Module 6 — Tools and Guardrails\n\nToday's plan:\n"
            + "\n".join(f"  {t} — {what}" for t, what in timings)
            + "\n\nFrame it: last week the rules decided when to use a tool, and they missed things. "
            "Today the model decides, code checks every request, and every change waits for a person. "
            "Every model output on these slides is a real run of the course model; say that students' "
            "wording will differ.",
        )
    )
    add(
        slide_section(
            1,
            "Where Week 11 Left Off",
            "Three problems from last week. Ask the class to recall them before the next slide.",
        )
    )
    add(
        slide_point(
            "Three problems",
            [
                "<em>Has my package A101 shipped?</em> missed the order rule. The model once said it had shipped. It had not.",
                "<em>Do you sell gift cards?</em> tripped the payment rule because of <em>card</em>.",
                "Every reply had the role <code>assistant</code>, whoever wrote it.",
                "Today fixes the first and third. The second stays, on purpose.",
            ],
            "Promise an answer to 'why keep the gift-card problem?' by the end of the hour.",
        )
    )
    add(slide_section(2, "Tool Calls", "The model asks; your code decides."))
    add(
        slide_point(
            "The model asks; your code decides",
            [
                "The chatbot sends a list of <strong>tools</strong> with the conversation.",
                "The model writes a reply, or sends a <strong>tool call</strong>: a name and values.",
                "It never runs anything. Your code decides whether to run the tool.",
                'A decision is a dictionary: <code>{"text": ...}</code> or <code>{"tool": ..., "arguments": {...}}</code>.',
            ],
            "Stress that the model cannot run code. Everything that happens is done by your program.",
        )
    )
    add(
        slide_code(
            "decision.py — read it together",
            blocks["decision"],
            'Point out that "text" in decision is how the chatbot tells the two shapes apart.',
        )
    )
    add(
        slide_code(
            "order_tool.py — a method the model may ask for",
            method(M + "order_tool.py", "look_up_order", G),
            "The docstring's first line says what the tool does. Args says what each value looks like. "
            "The ollama package reads both. Until today a docstring was for people; now a program reads it.",
        )
    )
    add(
        slide_section(
            3,
            "The Tool Loop",
            "One message can take two trips to the model: ask for a tool, then answer.",
        )
    )
    add(
        slide_code(
            "ollama_model.py — the new method, decide",
            method(M + "ollama_model.py", "decide", G),
            "decide sits beside reply. reply stays because the Week 11 mini-project still uses it. "
            "tool_calls[0]: this chatbot runs the first request and lets the model ask again.",
            size=".6em",
        )
    )
    add(
        slide_code(
            "chatbot.py — model_reply, write together",
            method(M + "chatbot.py", "model_reply", G),
            "Write it live. Ask what happens if the model never answers: rounds reaches MAX_TOOL_ROUNDS "
            "and the customer goes to a person.",
            size=".6em",
        )
    )
    add(
        slide_code(
            "Run it with a fake model",
            blocks["loop"],
            "Two decisions played back: a tool request, then a reply. The middle line of the history is the new tool entry.",
            size=".52em",
        )
    )
    add(
        slide_chalk(
            "Draw: the loop",
            "CHALKBOARD: Draw customer → chatbot → model. Arrow back: 'tool call'. Chatbot → Toolbox → tool → result into the history. Arrow to the model again → reply. Mark the counter on the loop. Take 3 minutes.",
        )
    )
    add(
        slide_point(
            "Ollama needs to see its own request",
            [
                "The history keeps one <code>tool</code> entry per tool use.",
                "<code>tool_messages</code> turns it into the two messages Ollama expects.",
                f"Without the request, the model asked for the same lookup twice in {of(c['echo_off_repeats'])} runs.",
            ],
            "Optional depth. Show tool_messages on the reading page if anyone asks how.",
        )
    )
    add(slide_section(4, "One Door", "Every tool request goes through Toolbox.run."))
    add(
        slide_code(
            "toolbox.py — run",
            method(M + "toolbox.py", "run", G),
            "Walk the order: name known? value present? did the customer actually say it? Each refusal is a sentence for the model.",
            size=".5em",
        )
    )
    add(
        slide_code(
            "Try the door",
            blocks["door"],
            "Three refusals: unknown tool, empty value after .strip(), and a made-up order ID.",
            size=".55em",
        )
    )
    add(
        slide_point(
            "The made-up address",
            [
                f"Asked <em>I want to change my shipping address</em> with no details, the model made up order A100 and an address and filed it in {of(c['no_guard_filed'])} runs with the check off.",
                f"With the check on, it was refused in {of(c['with_guard_refused'])} runs, and the model asked the customer.",
                '<code>"" in "any text"</code> is <code>True</code>: the empty check comes first.',
            ],
            "Read one real run aloud from the lecture page. The empty-string bug really happened while this week was being built.",
        )
    )
    add(
        slide_section(
            5,
            "Changes Wait for a Person",
            "A change tool files a request. Only approve changes an order.",
        )
    )
    add(
        slide_code(
            "Try the queue",
            blocks["queue"],
            "The address stays 14 Bay Road until approve. A second approve changes nothing.",
            size=".6em",
        )
    )
    add(
        slide_demo(
            "Terminal &nbsp;→&nbsp; python3 main.py",
            "Type: hello · Has my package A101 shipped? · I want to change my shipping address · then the order ID and an address · quit · yes",
            "LIVE DEMO\nRun main.py with Ollama running. Follow the lab's message list. The model should ask for the order ID and address, file the change, and tell the customer it will be reviewed. At the staff review type yes and show the address changed. If the model is slow, switch to KeywordModel and show that it cannot collect an address: that is the point of a real model.",
        )
    )
    add(
        slide_section(
            6,
            "Stand-ins and Tests",
            "KeywordModel runs the chatbot without Ollama. FakeModel makes tests exact.",
        )
    )
    add(
        slide_point(
            "Two stand-ins",
            [
                "<code>KeywordModel</code>: last week's keyword rules, now inside a model with <code>decide</code>.",
                "<code>FakeModel</code>: plays back the exact decisions a test gives it.",
                "Tests can make the model ask for a missing tool, send an empty address, or ask forever.",
                "Trade-off: with Ollama off, a lookup now needs the model too. Exercise 4 fixes that.",
            ],
            "Show one test from tests/test_chatbot.py, test_made_up_address_is_refused, on the lecture page.",
        )
    )
    add(
        slide_section(
            7, "What Tools Did Not Fix", "Close the loop on the three problems."
        )
    )
    add(
        slide_point(
            "Fixed, not fixed, kept on purpose",
            [
                f"Fixed: A101 answered from a lookup in {of(c['a101'])} runs.",
                f"Not fixed: the false closing time, repeated in {of(c['closing_agrees'])} runs. No tool knows the hours.",
                "Kept: gift cards still go to a person. A protective rule should prefer false alarms.",
            ],
            "Answer the opening promise: matching only the whole word would miss 'Can I pay by card?'. A wait is cheap; a missed payment question is not.",
        )
    )
    add(
        slide_point(
            "Essential, optional, left out",
            [
                "<strong>Essential:</strong> tool calls and docstrings, <code>decide</code>, the loop and its limit, the Toolbox checks, the change queue, <code>FakeModel</code> tests.",
                "<strong>Optional:</strong> <code>tool_messages</code>, the fallback model, turning a guardrail off to watch.",
                "<strong>Left out:</strong> several tool calls at once, streaming, online services, signing customers in, lasting data.",
            ],
            "Point students to the lab: Parts 2 to 5 and the tests are graded and need no Ollama.",
        )
    )
    add(
        slide_point(
            "Next week",
            [
                "Approved changes live in a list. Stop the program and they are gone.",
                "Week 13: choose your own business and design its data in SQLite.",
                "Week 14: database functions become the tools. Today's chatbot is copied over unchanged.",
            ],
            "End on the problem: a business needs data that lasts.",
        )
    )

    before, after = slides_shell("week11_slides.html")
    before = re.sub(
        r"<title>.*?</title>",
        f"<title>ISM3232 Week 12 — {w.TITLE}</title>",
        before,
        count=1,
    )
    page = before + "\n" + "\n".join(s) + after
    path = DOCS / "week12_slides.html"
    path.write_text(page)
    return path, list(blocks.values())


if __name__ == "__main__":
    path, _ = build()
    print("wrote", path)
