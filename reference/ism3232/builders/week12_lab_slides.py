"""Build ism3232/docs/week12_lab_slides.html, the interactive lab deck.

Runnable blocks execute in the browser with Pyodide, so each is a complete
standalone script that uses only Python taught by Week 12. Their output slides
come from running the same code with CPython here. File listings are read-only.

    python reference/ism3232/builders/week12_lab_slides.py
"""

import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import week12_common as w
from pagekit import DOCS, esc, folder_at, method, run_snippet, shell
from runs import words
from week12_reading import MAIN_INPUTS, typed

M = "module06_agents/"
G = w.GUIDED

RUNNABLE = {
    "decision": w.SNIPPETS["decision"],
    "said": """def customer_said(history, text):
    for message in history:
        if message["role"] == "user" and text.lower() in message["content"].lower():
            return True
    return False


history = [{"role": "user", "content": "I want to change my shipping address"}]
print(customer_said(history, "A100"))
print(customer_said(history, "shipping ADDRESS"))
print(customer_said(history, ""))""",
    "queue": """orders = {"A100": {"status": "shipped", "address": "14 Bay Road"}}
requests = []

request = {"number": 1, "order_id": "A100", "new_address": "9 Pine Street"}
request["status"] = "waiting"
requests.append(request)
print(orders["A100"]["address"], request["status"])

if request["status"] == "waiting":
    request["status"] = "approved"
    orders[request["order_id"]]["address"] = request["new_address"]
print(orders["A100"]["address"], request["status"])""",
    "loop": """decisions = [
    {"tool": "look_up_order", "arguments": {"order_id": "A101"}},
    {"text": "Order A101 is still processing."},
]
history = [{"role": "user", "content": "Has my package A101 shipped?"}]

reply = None
rounds = 0
while reply is None and rounds < 3:
    decision = decisions[rounds]
    if "text" in decision:
        reply = decision["text"]
    else:
        print("tool request:", decision["tool"], decision["arguments"])
        history.append({"role": "tool", "content": "Order A101 is processing."})
    rounds += 1

print("reply:", reply)
print("history entries:", len(history))""",
}


OUT = DOCS / "week12_lab_slides.html"


def of(pair):
    return f"{words(pair[0])} out of {words(pair[1])}"


def sec(comment, cls, inner, notes):
    return f'<!-- {comment} -->\n<section class="{cls}">\n{inner}\n<aside class="notes">\n{notes}\n</aside>\n</section>\n'


def run_block(code, readonly=False, lang="python"):
    flag = " data-readonly" if readonly else ""
    return f'<div class="run" data-lang="{lang}"{flag}>{esc(code.rstrip())}</div>'


SHOWN = []


def wrap_for_slide(text, width=74):
    """Wrap long lines for a slide. A continuation line is indented under the
    text after 'Sunny: ' or 'You: ' (or by four spaces), so the speaker stays clear."""
    import textwrap

    lines = []
    for line in text.rstrip().split("\n"):
        if len(line) <= width:
            lines.append(line)
            continue
        head = len(line) - len(line.lstrip())
        for prefix in ("Sunny: ", "Robin: ", "You: "):
            if line.lstrip().startswith(prefix):
                head += len(prefix)
                break
        else:
            head += 4
        lines.extend(
            textwrap.wrap(
                line, width=width, subsequent_indent=" " * head, break_on_hyphens=False
            )
        )
    return "\n".join(lines)


def out_slide(comment, title, text, expect, notes):
    shown = wrap_for_slide(text)
    SHOWN.append(shown)
    return sec(
        comment,
        "s-out",
        f'<h3>{title}</h3>\n<pre>{esc(shown)}</pre>\n<p class="expect">{expect}</p>',
        notes,
    )


def code_slide(comment, title, code, expect, notes, readonly=False, lang="python"):
    inner = f'<h3>{title}</h3>\n{run_block(code, readonly, lang)}\n<p class="expect">{expect}</p>'
    return sec(comment, "s-code", inner, notes)


def idea(comment, title, label, paragraphs, notes):
    body = "".join(f"<p>{p}</p>" for p in paragraphs)
    return sec(
        comment,
        "s-idea",
        f'<h3>{title}</h3>\n<div class="concept">\n<div class="concept-lbl">{label}</div>\n{body}\n</div>',
        notes,
    )


def warn(comment, title, paragraphs, notes):
    body = "".join(f"<p>{p}</p>" for p in paragraphs)
    return sec(
        comment,
        "s-warn",
        f'<h3>{title}</h3>\n<div class="warn-card">\n<div class="warn-lbl">Watch for</div>\n{body}\n</div>',
        notes,
    )


def quiz(comment, question, options, answer, why, notes):
    buttons = "\n".join(
        f'<button data-opt="{letter}">{text}</button>' for letter, text in options
    )
    inner = (
        f'<h3>Knowledge check</h3>\n<div class="quiz" data-answer="{answer}">\n<p class="q">{question}</p>\n'
        f'{buttons}\n<p class="why" hidden>{why}</p>\n</div>'
    )
    return sec(comment, "s-quiz", inner, notes)


def divider(comment, chip, title, notes):
    return sec(
        comment, "s-sec", f'<span class="chip">{chip}</span>\n<h1>{title}</h1>', notes
    )


def pytest_pane(folder):
    """Real `pytest -v` output: one line per test, then the summary without timing."""
    result = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-v", "-p", "no:cacheprovider"],
        cwd=folder,
        capture_output=True,
        text=True,
        check=False,
    )
    lines = [
        re.sub(r"\s+\[\s*\d+%\]$", "", line)
        for line in result.stdout.split("\n")
        if " PASSED" in line or " FAILED" in line
    ]
    summary = result.stdout.strip().split("\n")[-1].strip("= ").split(" in ")[0]
    return "\n".join(lines) + "\n" + summary


def build():
    c = w.counts()
    guided = folder_at(G)
    empty = Path(tempfile.mkdtemp(prefix="ism3232-run-"))
    outputs = {name: run_snippet(code, empty) for name, code in RUNNABLE.items()}
    main_typed = typed(w.run_text("main_conversation.txt"), MAIN_INPUTS)
    off = typed(w.run_text("ollama_off.txt"), ["hello", "Where is order A100?", "quit"])
    no_guard = w.first_run("address_no_guard.txt")
    with_guard = w.first_run("address_with_guard.txt")
    shell_orders = shell(
        [
            "from order_tool import OrderLookup",
            'tool = OrderLookup({"A100": {"status": "shipped", "address": "14 Bay Road"}})',
            'tool.look_up_order("a100")',
            'tool.look_up_order("A999")',
        ],
        guided,
    )
    pane = pytest_pane(guided)
    hello_text = w.run_text("mini_project_hello.txt")
    hello_counts = [
        part.count("check_open_times") for part in hello_text.split("== ")[1:]
    ]

    timings = [
        ("0:00–0:05", "Welcome: the model gets to ask for tools", 5),
        ("0:05–0:08", "Part 1 — Where you start", 3),
        ("0:08–0:20", "Part 2 — The tools describe themselves", 12),
        ("0:20–0:30", "Part 3 — Changes wait for a person", 10),
        ("0:30–0:45", "Part 4 — One door for every tool", 15),
        ("0:45–0:58", "Part 5 — The tool loop and the tests", 13),
        ("0:58–1:08", "Part 6 — The real model and staff review", 10),
        ("1:08–1:15", "Parts 7–9 — Exercises, mini-project brief, ritual", 7),
    ]
    s = []
    add = s.append
    bar = "\n".join(
        f'<span class="t-item"><strong>{t}</strong> {what}</span>'
        for t, what, _ in timings
    )
    add(
        sec(
            "1. TITLE",
            "s-title",
            f'<p class="eyebrow">ISM3232 &nbsp;·&nbsp; Week 12 &nbsp;·&nbsp; Module 12 &nbsp;·&nbsp; {w.UNIT}</p>\n'
            f'<h1>{w.TITLE}</h1>\n<div class="t-bar">\n{bar}\n</div>\n'
            '<p class="hint">&larr; &rarr; navigate &nbsp;·&nbsp; F fullscreen &nbsp;·&nbsp; S notes &nbsp;·&nbsp; D draw</p>',
            "Full class period, 75 minutes. Live code-along. Students arrive with the Week 11 chatbot, its model, "
            "the mini-project and passing tests in <code>module06_agents</code>.\n"
            "Today the model chooses when to use a tool, every request passes one checked door, and an address "
            "change waits for staff approval.\n"
            "<strong>Policy:</strong> a student whose laptop cannot run the model is not penalized. Parts 2 to 5 "
            "and every test need nothing but Python. They pair up for Part 6 and note it in their README.\n"
            "Every model output in this deck is a real run. Wording on student screens will differ. Say so early.",
        )
    )
    add(
        sec(
            "2. GLANCE",
            "s-glance",
            '<h3>Today at a glance</h3>\n<ul class="kv">\n'
            '<div><span class="k">Format</span><span class="v">Live code-along, then exercises and a mini-project upgrade finished on your own</span></div>\n'
            '<div><span class="k">Prerequisites</span><span class="v">Week 11: <code>MockModel</code>, <code>OllamaModel</code>, a chatbot handed a model, passing tests</span></div>\n'
            '<div><span class="k">Needs</span><span class="v">Nothing new to install. Part 6 uses Ollama and <code>granite4.1:3b</code> from last week</span></div>\n'
            '<div><span class="k">Submission</span><span class="v">GitHub URL in Canvas (no screenshots), completion credit</span></div>\n</ul>',
            "<strong>Essential today:</strong> tool calls and docstrings, <code>decide</code>, the tool loop and its limit, "
            "the <code>tool</code> history entry, the Toolbox checks, the change queue, <code>FakeModel</code> tests.\n"
            "<strong>Optional enrichment:</strong> <code>tool_messages</code>, Exercise 3 (turning a guardrail off), "
            "Exercise 4 (the fallback model).\n"
            "<strong>Left out on purpose:</strong> several tool calls at once, streaming, online services, signing "
            "customers in, lasting data.",
        )
    )
    add(
        sec(
            "3. OBJECTIVES",
            "s-obj",
            "<h3>Learning objectives</h3>\n<p>By the end of this class period, students should be able to:</p>\n<ul>\n"
            "<li>Explain what a tool call is, and describe a tool with a docstring.</li>\n"
            "<li>Trace the tool loop and read the <code>tool</code> entries in a history.</li>\n"
            "<li>Check every tool request in one place, and refuse details the customer never gave.</li>\n"
            "<li>Make a change wait for a person, and apply it only once.</li>\n"
            "<li>Test the loop with a fake model that needs nothing installed.</li>\n"
            "<li>Say what tools fixed and what they did not.</li>\n</ul>",
            "The module's eight outcomes, grouped. The only new Python is <code>.strip()</code> and passing a method "
            "without calling it. Everything else is composition and dictionaries, used a new way.",
        )
    )
    rows = "\n".join(
        f"<tr><td>{t}</td><td>{what}</td><td>{mins}</td></tr>"
        for t, what, mins in timings
    )
    add(
        sec(
            "4. TIMING",
            "s-timing",
            f'<h3>Timing plan — 75 minutes</h3>\n<table class="grid">\n<thead><tr><th>Time</th><th>Segment</th><th>Min</th></tr></thead>\n<tbody>\n{rows}\n</tbody>\n</table>',
            "Parts 4 and 5 get the most time. If the room is slow, show Part 6 from the front: every graded part works without the model.",
        )
    )
    add(
        divider(
            "5. INTRO divider",
            "Intro · 0:00–0:05",
            "Last week the rules decided. This week the model asks.",
            "Teaching goal: connect to Week 11's three problems.\n"
            'Say to the class: "Last week the order rule missed <em>Has my package A101 shipped?</em>, the payment rule '
            "caught <em>gift cards</em>, and the history hid which answers came from a tool. Today the model decides when "
            'to look something up, your code checks every request, and the history says who said what."\n'
            "Discussion opener: should a chatbot be allowed to change a customer's address on its own? Keep the answers; "
            "Part 3 returns to them.",
        )
    )
    add(
        divider(
            "6. PART 1 divider",
            "Part 1 · 0:05–0:08",
            "Where You Start",
            "Everyone confirms the Week 11 tests pass before changing anything.",
        )
    )
    add(
        code_slide(
            "7. PART 1 check (readonly shell)",
            "Check that last week's work passes",
            "cd ~/ism3232/module06_agents\nsource .venv/bin/activate\npytest -q",
            "The last line should say <code>21 passed</code>: fifteen chatbot tests and six mini-project tests.",
            "Warn the room now: after Part 2 the old chatbot tests fail until Part 5 replaces them. That is expected. "
            "Each part has its own check in the Python shell.",
            readonly=True,
            lang="shell",
        )
    )
    add(
        divider(
            "8. PART 2 divider",
            "Part 2 · 0:08–0:20",
            "The Tools Describe Themselves",
            "Teaching goal: a tool is an ordinary method; its docstring is now read by a program.",
        )
    )
    add(
        idea(
            "9. PART 2 idea",
            "The model asks; your code decides",
            "Concept",
            [
                "The chatbot sends a list of <strong>tools</strong> along with the conversation.",
                "The model writes a reply, or sends a <strong>tool call</strong>: a name and the values to use.",
                "It never runs anything. Your code decides whether to run the tool.",
                'A decision is a dictionary: <code>{"text": ...}</code> or <code>{"tool": ..., "arguments": {...}}</code>.',
            ],
            "Stress the second bullet. Students often believe the model executes their code.",
        )
    )
    add(
        code_slide(
            "10. PART 2 decision (RUNNABLE)",
            "Tell the two shapes apart",
            RUNNABLE["decision"],
            'No model here. <code>"text" in decision</code> asks whether the dictionary has that key. Press <strong>Run</strong>.',
            "The chatbot uses exactly this test to decide whether it got a reply or a tool request.",
        )
    )
    add(
        out_slide(
            "11. PART 2 decision output",
            "Expected output",
            outputs["decision"],
            "<code>False</code>: this decision is a tool request, not a reply.",
            "Ask: what would the dictionary look like if the model just wanted to say hello?",
        )
    )
    add(
        code_slide(
            "12. PART 2 look_up_order (readonly)",
            "order_tool.py — the method the model may ask for",
            method(M + "order_tool.py", "look_up_order", G),
            "The docstring's first line says what the tool does; <code>Args:</code> says what each value looks like.",
            "Orders are now dictionaries with a status and an address. Point at <code>find_order_id</code>: last week's "
            "method, so <code>a100</code> still works.",
            readonly=True,
        )
    )
    add(
        out_slide(
            "13. PART 2 shell check",
            "Check it in the Python shell",
            shell_orders,
            "Real output. The shell does not print <code>None</code>.",
            "Have students run this exact check before moving on.",
        )
    )
    add(
        quiz(
            "14. PART 2 quiz",
            "Where does the model learn what <code>look_up_order</code> is for?",
            [
                ("A", "From its name, its parameters and its docstring"),
                ("B", "From reading the method's body"),
                ("C", "From the order data"),
            ],
            "A",
            "The ollama package builds the tool description from the name, the parameters and the docstring. The body is never sent.",
            "If a student answers B: the model never sees your code, only the description.",
        )
    )
    add(
        divider(
            "15. PART 3 divider",
            "Part 3 · 0:20–0:30",
            "Changes Wait for a Person",
            "Teaching goal: a change tool files a request; only an approval changes data, and only once.",
        )
    )
    add(
        code_slide(
            "16. PART 3 queue (RUNNABLE)",
            "A request waits; an approval changes the order",
            RUNNABLE["queue"],
            "Plain dictionaries and a list, no classes. <code>ChangeQueue</code> wraps exactly this. Press <strong>Run</strong>.",
            "Return to the opening question: the chatbot never changes the address. It files a request, and a person decides.",
        )
    )
    add(
        out_slide(
            "17. PART 3 queue output",
            "Expected output",
            outputs["queue"],
            "The address changes only after the status moves from waiting to approved.",
            "Ask: what stops this from running twice? The status check.",
        )
    )
    add(
        code_slide(
            "18. PART 3 approve (readonly)",
            "change_queue.py — approve is the only code that changes an order",
            method(M + "change_queue.py", "approve", G),
            "A request that is already approved or rejected is refused, so a change can never happen twice.",
            "Students type the whole <code>change_queue.py</code> from the lab page, then run the shell check there.",
            readonly=True,
        )
    )
    add(
        warn(
            "19. PART 3 pitfalls",
            "Common student mistakes",
            [
                "Making the change inside <code>request_address_change</code>. The tool only files a request.",
                "Forgetting the status check in <code>approve</code>, so a second approval applies the change again.",
                "Running the whole test suite now. The old chatbot tests fail until Part 5.",
            ],
            "The first mistake defeats the purpose of the week. Ask a student to say why in one sentence.",
        )
    )
    add(
        divider(
            "20. PART 4 divider",
            "Part 4 · 0:30–0:45",
            "One Door for Every Tool",
            "Teaching goal: every request passes Toolbox.run, which refuses unknown tools, empty values and made-up details.",
        )
    )
    add(
        code_slide(
            "21. PART 4 run (readonly)",
            "toolbox.py — run",
            method(M + "toolbox.py", "run", G),
            "Each refusal is a sentence for the model, which reads it as the tool's result.",
            "Walk one branch out loud: name known, value present, customer said it. Then the tool runs.",
            readonly=True,
        )
    )
    add(
        code_slide(
            "22. PART 4 customer_said (RUNNABLE)",
            "Did the customer say it?",
            RUNNABLE["said"],
            "The same check as the Toolbox, as a plain function. Predict the three lines, then press <strong>Run</strong>.",
            "Collect predictions first. Most students expect the last line to be False.",
        )
    )
    add(
        out_slide(
            "23. PART 4 customer_said output",
            "Expected output",
            outputs["said"],
            '<code>"" in "any text"</code> is <code>True</code>. That is why <code>run</code> checks for an empty value first.',
            "This bug really happened while the week was built: the model sent an empty address and the first draft let it through.",
        )
    )
    add(
        out_slide(
            "24. PART 4 made-up address",
            f"With the check off: made-up details filed in {of(c['no_guard_filed'])} runs",
            no_guard,
            f"With the check on, the same request was refused in {of(c['with_guard_refused'])} runs:<br><code>{esc(with_guard.split(chr(10))[1])}</code>",
            "Read the made-up request aloud: order A100, 123 Main St, Anytown. Nobody typed either. Exercise 3 lets students see it for themselves.",
        )
    )
    add(
        warn(
            "25. PART 4 pitfalls",
            "Common student mistakes",
            [
                "Parentheses in <code>tool_list</code>: <code>look_up_order()</code> calls the method instead of passing it.",
                "<code>I001 Import block is un-sorted</code> on a test file: the module it imports does not exist yet, or is misspelled.",
                "Putting the empty check after <code>customer_said</code>.",
            ],
            "The I001 one surprises everyone: ruff sorts imports of files it can find in the folder separately from ones it cannot.",
        )
    )
    add(
        divider(
            "26. PART 5 divider",
            "Part 5 · 0:45–0:58",
            "The Tool Loop",
            "Teaching goal: ask, check, run, record, ask again, at most three times. Then test it with FakeModel.",
        )
    )
    add(
        code_slide(
            "27. PART 5 loop (RUNNABLE)",
            "The loop, with the model's decisions written out",
            RUNNABLE["loop"],
            "The <code>while</code> stops when there is a reply or after three rounds. Press <strong>Run</strong>.",
            "This is <code>model_reply</code> with the model replaced by a list. The chatbot version calls <code>decide</code> and <code>run</code>.",
        )
    )
    add(
        out_slide(
            "28. PART 5 loop output",
            "Expected output",
            outputs["loop"],
            "Two trips for one message: a tool request, then the reply. The history gained the tool entry.",
            "Ask what happens if every decision is a tool request: the loop stops after three rounds.",
        )
    )
    add(
        code_slide(
            "29. PART 5 model_reply (readonly)",
            "chatbot.py — model_reply",
            method(M + "chatbot.py", "model_reply", G),
            "After <code>MAX_TOOL_ROUNDS</code> the customer goes to a person.",
            "The chatbot now takes four values: name, instructions, tools, model. The order and stock rules are gone; the payment rule stays.",
            readonly=True,
        )
    )
    add(
        out_slide(
            "30. PART 5 pytest pane",
            "pytest -v — the whole suite",
            pane,
            "Real output with no Ollama installed in the test path.",
            f"{words(pane.count('test_chatbot.py::')).capitalize()} chatbot tests, "
            f"{words(pane.count('test_tools.py::'))} tool tests, and the "
            f"{words(pane.count('test_appointment_bot.py::'))} mini-project tests, which still use MockModel and reply.",
        )
    )
    add(
        quiz(
            "31. PART 5 quiz",
            "Why do the tests use <code>FakeModel</code> and not the real model?",
            [
                (
                    "A",
                    "A test can make it ask for a missing tool, send an empty value, or ask forever, every time",
                ),
                ("B", "FakeModel is more accurate than the real model"),
                ("C", "The real model cannot ask for tools"),
            ],
            "A",
            "A real model does those things only sometimes. A test needs the exact same decisions on every run, with nothing installed.",
            "Link to Week 11: MockModel made the replies predictable; FakeModel makes the decisions predictable.",
        )
    )
    add(
        divider(
            "32. PART 6 divider",
            "Part 6 · 0:58–1:08",
            "The Real Model and Staff Review",
            "Teaching goal: see the whole loop with the real model, including an approval.",
        )
    )
    add(
        out_slide(
            "33. PART 6 conversation",
            "One real conversation, ending in approval",
            main_typed,
            "The model's wording will differ. The staff review and the final addresses should match.",
            "Point out the model asking for the missing details, and the address changing only after yes.",
        )
    )
    add(
        out_slide(
            "34. PART 6 Ollama off",
            "The same program with Ollama switched off",
            off,
            "Both answers are the apology. Last week the order rule still worked here.",
            "Name the trade-off: when the model decides, a lookup needs the model too. Exercise 4 adds a fallback.",
        )
    )
    add(
        warn(
            "35. PART 6 pitfalls",
            "Watch for",
            [
                "Every reply is the apology: Ollama is not running, or the model is not downloaded.",
                "The model rewords an address the customer typed (<em>9 Pine Street</em> for <em>9 Pine St</em>): the door refuses it and the model asks again. That is the check working.",
                "A shortened address (<em>9 Pine St</em> for <em>9 Pine Street</em>) is inside what the customer typed, so it passes. Staff see it in the review: the check and the approval are two layers.",
                "Expecting the same wording as the slide. Only the tool results and the staff review are fixed.",
            ],
            "If the room's laptops are slow, show this part from the front.",
        )
    )
    add(
        divider(
            "36. PART 7 divider",
            "Parts 7–9 · 1:08–1:15",
            "Exercises, Mini-Project, Ritual",
            "Teaching goal: every student leaves knowing what the four exercises ask and how the mini-project is upgraded.",
        )
    )
    add(
        idea(
            "37. PART 7 exercises",
            "Four exercises",
            "On the lab page",
            [
                "<strong>1.</strong> Read a history with three tool entries and two refusals.",
                "<strong>2.</strong> Add a tool, <code>check_return</code>: the method, <code>tool_list</code>, and a branch in <code>run</code>.",
                "<strong>3.</strong> Turn the customer-said check off and watch a made-up request reach staff. Then turn it back on.",
                "<strong>4.</strong> Keep lookups working when Ollama is down with a model made of two models.",
            ],
            "Exercises 1, 2 and 4 need no Ollama. Exercise 3 needs the real model: pair up if needed.",
        )
    )
    add(
        idea(
            "38. PART 8 mini-project",
            "Mini-project — let your assistant choose its tool",
            "What to build",
            [
                "The model chooses your assistant's tool through <code>decide</code>, in a loop with a limit.",
                "A toolbox <code>run</code> refuses unknown tools, empty values, and details the user never typed.",
                "One change waits for approval and can only be applied once. One rule still hands something to a person.",
                f"Instructions matter: the reference helper answered <em>hello</em> with open times in {hello_counts[0]} of 5 runs until one sentence said what to do with a greeting ({hello_counts[2]} of 5).",
            ],
            "The lab page has the checklist, a real sample run, a 10-point rubric and a reference solution behind a click.",
        )
    )
    add(
        code_slide(
            "39. PART 9 ritual (readonly shell)",
            "The full pre-submission ritual — with Ollama switched off",
            "ruff format . && ruff check . && pytest -v\ngit add . && git commit -m 'lab 12: tools, guardrails, and approval' && git push",
            "If the tests pass now, they pass when the repository is graded. The commit message must include <strong>&ldquo;lab 12&rdquo;</strong>.",
            "<code>&amp;&amp;</code> stops at the first failure. If <code>ruff check</code> stops on a fixable error, run <code>ruff check --fix .</code> and run the first line again.",
            readonly=True,
            lang="shell",
        )
    )
    add(
        sec(
            "40. WRAP checklist",
            "s-wrap",
            "<h3>Wrap-up — submission checklist</h3>\n<ul>\n"
            "<li>Git commit made, with a message including <strong>&ldquo;lab 12&rdquo;</strong></li>\n"
            "<li><code>toolbox.py</code>, <code>change_queue.py</code>, <code>keyword_model.py</code> and <code>fake_model.py</code> exist</li>\n"
            "<li>All tests pass with Ollama switched off</li>\n"
            "<li><code>week12_answers.md</code> is in the repo</li>\n"
            "<li>The mini-project chooses its tool, has a waiting change, and its README section is written</li>\n"
            "<li>Full ritual run, and the GitHub repository URL pasted into Canvas</li>\n</ul>",
            "Completion credit. The idea to reinforce as they leave: <em>the model asks, code checks, people approve.</em>",
        )
    )
    add(
        sec(
            "41. WRAP next",
            "s-wrap",
            "<h3>Where this goes next</h3>\n<p>&ldquo;Today the approved change lived in a list. Stop the program and it is gone. "
            "Next week you choose a business of your own and keep its data in a database.&rdquo;</p>",
            "Connections. <strong>Week 13:</strong> the proposal and SQLite. <strong>Week 14:</strong> database functions become "
            "the tools, and today's chatbot is copied over unchanged. <strong>Week 15:</strong> the staff review becomes a tab in "
            "a web app. <strong>Week 16:</strong> the false closing time comes back as an evaluation case.",
        )
    )
    add(
        sec(
            "42. END",
            "s-end",
            '<div class="sec-n">ISM3232 · Week 12</div>\n<h1>End of lab</h1>',
            "Every runnable block in this deck is a complete standalone script, and its expected-output slide was produced "
            "by running it with CPython 3.12. Read-only listings are the lab's own files. Outputs of the course model are "
            "single real runs of granite4.1:3b captured with Ollama 0.34.4 on the CPU; wording varies from run to run. The "
            "<code>pytest -v</code> pane is the real output of the suite with no Ollama installed in the test path.",
        )
    )

    template = (DOCS / "week11_lab_slides.html").read_text()
    start = template.index('<div class="slides">') + len('<div class="slides">')
    end = template.index("</div></div>", template.rindex("</section>"))
    before = re.sub(
        r"<title>.*?</title>",
        f"<title>ISM3232 Lab Week 12 — {w.TITLE}</title>",
        template[:start],
        count=1,
    )
    page = before + "\n\n" + "\n".join(s) + "\n" + template[end:]
    derived = [*RUNNABLE.values(), *outputs.values(), *SHOWN]
    derived += [
        "cd ~/ism3232/module06_agents\nsource .venv/bin/activate\npytest -q",
        "ruff format . && ruff check . && pytest -v\ngit add . && git commit -m 'lab 12: tools, guardrails, and approval' && git push",
    ]
    return page, derived


if __name__ == "__main__":
    page, _ = build()
    OUT.write_text(page)
    print("wrote", OUT)
