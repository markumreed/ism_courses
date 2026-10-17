"""Build ism3232/docs/week12_lab.html from the reference folder and saved runs.

Listing labels follow a convention the rebuild check (rebuild_week12_lab.py)
applies mechanically:
  "file.py"                                  write the whole file
  "file.py — add this method to the class"   append a method to the class
  "file.py — replace NAME"                   replace one method or function
  "file.py — add at the bottom"              append a top-level function
  "file.py — add this import below ..."      insert one import line
Any other label is not applied (outputs, shell sessions, things to try).

    python reference/ism3232/builders/week12_lab.py
"""

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import runs
import week12_common as w
from pagekit import (
    DOCS,
    NO_SCREENSHOTS,
    callout_box,
    check_list,
    code_block,
    concept_table,
    course_map,
    esc,
    expected,
    folder_at,
    function,
    head_from,
    hint,
    method,
    prev_next,
    reveal,
    section_divider,
    shell,
    submit_box,
    task,
    time_bar,
)
from runs import words
from week12_reading import MAIN_INPUTS, typed

M = "module06_agents/"
G = w.GUIDED
DASH = " &mdash; "


OUT = DOCS / "week12_lab.html"


def block(label, code):
    return code_block(label, code, python=False)


def pytest_summary(folder, *args):
    """The last line of a real pytest run, without the timing."""
    result = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", *args],
        cwd=folder,
        capture_output=True,
        text=True,
        check=False,
    )
    last = result.stdout.strip().split("\n")[-1]
    return last.split(" in ")[0]


def exercise1_history():
    """Replay run 1 of address_three_turns.txt with a FakeModel: the chatbot code
    runs for real, the decisions are the ones the real model made."""
    sys.path.insert(0, str(w.FOLDER))
    from change_queue import ChangeQueue
    from chatbot import SupportChatbot
    from fake_model import FakeModel
    from order_tool import OrderLookup
    from stock_tool import StockLookup
    from toolbox import Toolbox

    real = runs.load(w.WEEK, "address_three_turns.txt")[0]
    tool_calls = list(real["tools"])
    orders = {
        "A100": {"status": "shipped", "address": "14 Bay Road"},
        "A102": {"status": "delivered", "address": "88 Pier Street"},
    }
    order_tool = OrderLookup(orders)
    tools = Toolbox(order_tool, StockLookup({}), ChangeQueue(order_tool))
    decisions = []
    for (_, reply), (name, arguments, _) in zip(real["turns"], tool_calls, strict=True):
        decisions.append({"tool": name, "arguments": arguments})
        decisions.append({"text": reply})
    bot = SupportChatbot("Sunny", "Be friendly.", tools, FakeModel(decisions))
    for you, _ in real["turns"]:
        bot.respond(you)
    lines = []
    for entry in bot.history:
        if entry["role"] == "tool":
            lines.append(
                f"tool      | {entry['tool_name']} {entry['arguments']} -> {entry['content']}"
            )
        else:
            lines.append(f"{entry['role']:<9} | {entry['content']}")
    return "\n".join(lines), bot.history


def build():
    c = w.counts()
    guided = folder_at(G)
    main_typed = typed(w.run_text("main_conversation.txt"), MAIN_INPUTS)
    off = typed(w.run_text("ollama_off.txt"), ["hello", "Where is order A100?", "quit"])
    ex3 = typed(
        w.run_text("exercise3_main.txt"),
        ["I want to change my shipping address", "quit", "no"],
    )
    ex4 = typed(
        w.run_text("exercise4_fallback.txt"), ["hello", "Where is order A100?", "quit"]
    )
    mini = typed(
        w.run_text("mini_project.txt"),
        [
            "hello",
            "What times are open on Monday?",
            "Please book Monday at 9:00 am",
            "My name is Dana Cruz",
            "Please cancel my appointment",
            "quit",
            "yes",
        ],
    )
    hello_text = w.run_text("mini_project_hello.txt")
    hello_counts = [
        part.count("check_open_times") for part in hello_text.split("== ")[1:]
    ]
    history_text, history = exercise1_history()
    tool_entries = sum(1 for e in history if e["role"] == "tool")
    next_call = 1 + (len(history) - tool_entries) + 2 * tool_entries + 1
    users = [e["content"] for e in history if e["role"] == "user"]
    refusals = [
        e for e in history if e["role"] == "tool" and "has not given" in e["content"]
    ]

    shell_orders = shell(
        [
            "from order_tool import OrderLookup",
            'tool = OrderLookup({"A100": {"status": "shipped", "address": "14 Bay Road"}})',
            'tool.look_up_order("a100")',
            'tool.look_up_order("A999")',
        ],
        guided,
    )
    shell_stock = shell(
        [
            "from stock_tool import StockLookup",
            'tool = StockLookup({"rain jacket": 12, "day pack": 0})',
            'tool.check_stock("Rain Jacket")',
            'tool.check_stock("tent")',
        ],
        guided,
    )
    shell_queue = shell(
        [
            "from change_queue import ChangeQueue",
            "from order_tool import OrderLookup",
            'orders = {"A100": {"status": "shipped", "address": "14 Bay Road"}}',
            "queue = ChangeQueue(OrderLookup(orders))",
            'queue.request_address_change("A100", "9 Pine Street")',
            'orders["A100"]["address"]',
            "queue.approve(1)",
            'orders["A100"]["address"]',
            "queue.approve(1)",
        ],
        guided,
    )
    tools_tests = pytest_summary(guided, "tests/test_tools.py")
    all_tests = pytest_summary(guided)
    n_chat = w.source("tests/test_chatbot.py").count("\ndef test_")
    n_tools = w.source("tests/test_tools.py").count("\ndef test_")
    n_appt = w.source("tests/test_appointment_bot.py").count("\ndef test_")
    guided_total = n_chat + n_tools + n_appt
    final_total = pytest_summary(w.FOLDER)
    if final_total != f"{guided_total + 3} passed":
        raise ValueError(
            f"expected {guided_total + 3} tests at the end, found {final_total}"
        )

    p = []
    add = p.append
    add('<div class="wrap">')
    add(
        f'<div class="page-eyebrow" style="color:{w.EYEBROW_COLOR};">{w.UNIT} · Module 12 · Lab</div>'
    )
    add(f'<h1 class="wk-title">{w.TITLE}</h1>')
    add(
        '<p class="wk-deck">Module 6 &mdash; Tools and Guardrails &mdash; let the model choose when to '
        "use a tool, check every request in one place, and make address changes wait for staff "
        "approval</p>"
    )
    add(
        '<div class="meta">\n<span class="chip accent">Module 12 · Lab</span>\n'
        f'<span class="chip">{w.UNIT}</span>\n<span class="chip">Full class period + exercises</span>\n</div>'
    )
    add(
        '<div class="weekjump">\n<span class="weekjump-label">This module:</span>\n'
        '<a href="week12_reading.html" class="weekjump-link">Reading</a>\n'
        '<a href="week12_lecture.html" class="weekjump-link">Lecture</a>\n'
        '<a href="week12_lab.html" class="weekjump-link current">Lab</a>\n'
        '<a href="week12_lab_slides.html" class="weekjump-link">Slides</a>\n</div>'
    )
    add(course_map("W12 "))
    add(
        time_bar(
            [
                "Part 1: Where you start",
                "Part 2: Tools describe themselves",
                "Part 3: Changes wait",
                "Part 4: One door",
                "Part 5: The loop",
                "Part 6: The real model",
                "Part 7: Four exercises",
                "Part 8: Mini-project",
                "Part 9: Ritual + push",
            ]
        )
    )
    add(
        callout_box(
            "blue",
            "&#x1F4CB;",
            "Lab goal &mdash; full class period, then finish on your own",
            "Give the model a list of tools it may ask for, check every request it makes in one place, "
            "and make an address change wait until a person approves it. Then test all of it with a "
            "fake model that needs nothing installed.",
        )
    )
    add(
        callout_box(
            "blue",
            "&#x1F4CD;",
            "Where you start",
            "Your <code>module06_agents</code> folder from Week 11, with <code>MockModel</code>, "
            "<code>OllamaModel</code>, a chatbot that is handed a model, your mini-project, and all tests "
            'passing. If anything is missing, finish the <a href="week11_lab.html">Week 11 lab</a> first.',
        )
    )
    add(
        callout_box(
            "warn",
            "&#x26A0;",
            "If your laptop cannot run the model",
            "Parts 2 to 5, Exercises 1, 2 and 4, and every test need nothing but Python, and they are "
            "what is graded. For Part 6, Exercise 3 and the real-model part of the mini-project, work "
            "beside a classmate whose laptop runs the model, and write one line in your "
            "<code>README.md</code> saying who you worked with.",
        )
    )
    add(
        callout_box(
            "warn",
            "&#x26A0;",
            "No AI-generated classes",
            "You must be able to explain every line of your classes. If you use AI to generate any part "
            "of a class definition, you must paste the AI output and add a comment explaining what each "
            "line does and why.",
        )
    )

    # Part 1
    add(section_divider("Part 1 &mdash; Where You Start"))
    add(
        task(
            1,
            "Check that last week's work passes",
            block(
                "Terminal",
                "cd ~/ism3232/module06_agents\nsource .venv/bin/activate\npytest -q",
            )
            + "<p>The last line should say:</p>"
            + expected("21 passed")
            + "<p>That is fifteen chatbot tests and six mini-project tests. Your count can be higher if "
            "you wrote extra tests.</p>"
            + hint(
                "<strong>Run the whole test suite again only at the end of Part 5.</strong> Part 2 "
                "changes the shape of the order data, so your old chatbot tests fail until Part 5 "
                "replaces them. That is expected. Each part below has its own check."
            ),
        )
    )

    # Part 2
    add(section_divider("Part 2 &mdash; The Tools Describe Themselves"))
    add(
        task(
            2,
            "Give every order an address, and add a tool method to OrderLookup",
            "<p>Each order becomes a dictionary with a status and an address, the shape of a database "
            "row in Week 14. <code>look_up_order</code> is the method the model may ask for. Its "
            "docstring is now read by a program, so write it exactly.</p>"
            + block("order_tool.py", w.source("order_tool.py"))
            + "<p>Check it in the Python shell:</p>"
            + block("Python shell", shell_orders)
            + "<p><code>look_up_order</code> uses last week's <code>find_order_id</code>, so "
            "<code>a100</code> works as well as <code>A100</code>. <code>change_address</code> is "
            "only ever called by an approval, in Part 3.</p>",
        )
    )
    add(
        task(
            3,
            "Add a tool method to StockLookup",
            block(
                "stock_tool.py" + DASH + "add this method to the class",
                method(M + "stock_tool.py", "check_stock", G),
            )
            + block("Python shell", shell_stock),
        )
    )

    # Part 3
    add(section_divider("Part 3 &mdash; Changes Wait for a Person"))
    add(
        task(
            4,
            "Write ChangeQueue in change_queue.py",
            "<p>A change tool never makes the change. It files a request with the status "
            '<code>"waiting"</code>. Only <code>approve</code> changes an order, and only once. It '
            "checks the order ID exactly, so a typo such as <code>A1000</code> is refused instead of "
            "being filed against <code>A100</code>.</p>"
            + block("change_queue.py", w.source("change_queue.py"))
            + block("Python shell", shell_queue)
            + "<p>The address stayed <code>14 Bay Road</code> until the approval, and the second "
            "approval changed nothing.</p>",
        )
    )

    # Part 4
    add(section_divider("Part 4 &mdash; One Door for Every Tool"))
    add(
        task(
            5,
            "Write Toolbox in toolbox.py",
            "<p>Every tool request from the model comes through <code>run</code>. It refuses a tool it "
            "does not know, an empty value, and an order ID or address the customer never typed. "
            "<code>.strip()</code> is new: it removes spaces from both ends of a string.</p>"
            + block("toolbox.py", w.source("toolbox.py"))
            + hint(
                "<strong>No parentheses in <code>tool_list</code>.</strong> "
                "<code>self.order_tool.look_up_order</code> passes the method along without calling it. "
                "Ollama reads its name, parameters and docstring."
            ),
        )
    )
    add(
        task(
            6,
            "Test the tools and the door",
            block("tests/test_tools.py", w.source("tests/test_tools.py"))
            + "<p>Run: <code>pytest -v tests/test_tools.py</code></p>"
            + expected(tools_tests)
            + hint(
                "<strong><code>ruff check</code> says <code>I001 Import block is un-sorted</code> for a "
                "test file?</strong> ruff sorts imports of files it can find in your folder separately "
                "from ones it cannot. If <code>toolbox.py</code> or <code>change_queue.py</code> does not "
                "exist yet, or is misspelled, ruff treats it as a package from the internet. Check the "
                "file names first."
            ),
        )
    )

    # Part 5
    add(section_divider("Part 5 &mdash; The Tool Loop"))
    add(
        task(
            7,
            "Write the two stand-in models",
            "<p><code>KeywordModel</code> carries last week's keyword rules, moved out of the chatbot, so "
            "the chatbot runs without Ollama. <code>FakeModel</code> is for tests: it plays back exactly "
            "the decisions you give it.</p>"
            + block("keyword_model.py", w.source("keyword_model.py"))
            + block("fake_model.py", w.source("fake_model.py")),
        )
    )
    add(
        task(
            8,
            "Replace chatbot.py",
            "<p>The chatbot is now handed a toolbox and a model. The order and stock rules are gone; the "
            "model decides. The payment rule stays, and <code>address</code> is no longer a handoff "
            "word, because an address change now waits for approval.</p>"
            + block("chatbot.py", w.source("chatbot.py"))
            + "<p>Read <code>model_reply</code> slowly: ask, check, run, record, ask again, at most three "
            "times.</p>",
        )
    )
    add(
        task(
            9,
            "Replace the chatbot tests, and update two_bots.py",
            block("tests/test_chatbot.py", w.source("tests/test_chatbot.py"))
            + block("two_bots.py", w.source("two_bots.py"))
            + "<p>Run: <code>pytest -v</code>. Now the whole suite runs.</p>"
            + expected(all_tests)
            + f"<p>{words(n_chat).capitalize()} chatbot tests, {words(n_tools)} tool tests, and your "
            f"{words(n_appt)} mini-project tests, which still use <code>MockModel</code> and "
            "<code>reply</code>.</p>"
            + hint(
                "<strong><code>missing 1 required positional argument: 'model'</code>?</strong> "
                "<code>chatbot.py</code> is still the Week 11 version, which takes five values. Replace "
                "it with the listing in step 8 and save it. <strong><code>takes 5 positional arguments "
                "but 6 were given</code>?</strong> A line somewhere still creates a chatbot with the old "
                "five values. The chatbot now takes four: name, instructions, tools, model."
            ),
        )
    )

    # Part 6
    add(section_divider("Part 6 &mdash; The Real Model and Staff Review"))
    add(
        task(
            10,
            "Give OllamaModel a decide method, and replace main.py",
            "<p><code>reply</code> stays exactly as it was, because your mini-project still uses it. "
            "<code>decide</code> sends the tools along, and <code>tool_messages</code> turns each "
            "<code>tool</code> entry into the two messages Ollama expects.</p>"
            + block("ollama_model.py", w.source("ollama_model.py"))
            + block("main.py", w.source("main.py")),
        )
    )
    add(
        task(
            11,
            "Have a conversation, then approve the change",
            "<p>Run: <code>python3 main.py</code> and type: <code>hello</code>, <code>Has my package A101 "
            "shipped?</code>, <code>Is the day pack in stock?</code>, <code>I want to change my shipping "
            "address</code>, <code>It's order A102</code>, <code>9 Pine Street, Tampa</code>, <code>Do you "
            "sell gift cards?</code>, then <code>quit</code>, and <code>yes</code> at the staff review.</p>"
            + expected(main_typed)
            + "<p>This is one real run. The model's wording will differ. The staff review and the final "
            "addresses should match exactly.</p>",
        )
    )
    add(
        task(
            12,
            "Switch Ollama off and try again",
            "<p>On a Mac, quit the Ollama app. On Windows, press Ctrl+C in the terminal running "
            "<code>ollama serve</code>. Then run <code>python3 main.py</code>, type <code>hello</code>, "
            "<code>Where is order A100?</code> and <code>quit</code>.</p>"
            + expected(off)
            + "<p>Last week the order question still worked with Ollama off, because a rule answered it. "
            "Now the model decides, so a lookup needs the model too. Exercise 4 fixes that. Turn Ollama "
            "back on before the exercises.</p>",
        )
    )

    # Part 7
    add(section_divider("Part 7 &mdash; Four Exercises"))
    add(
        callout_box(
            "blue",
            "&#x270F;",
            "How the exercises work",
            "Each exercise states the result you should get. Try it first, then open the answer key. "
            "Written answers go in a new file, <code>week12_answers.md</code>.",
        )
    )
    ex1_answers = (
        f"1. The customer typed: {', '.join(users)}\n"
        f"2. Refused: {len(refusals)}. The first used order A100 and the second used the address "
        "123 Main St, Anytown, AN 12345; the customer had typed neither.\n"
        f"3. {next_call} messages: the system message, the {len(history) - tool_entries} user and "
        f"assistant entries, two for each of the {tool_entries} tool entries, and the new message.\n"
        "4. Because the payment rule looks for card anywhere in the message. A wait is a cheap mistake;\n"
        "   a missed payment question could put card details in front of the model."
    )
    add(
        task(
            13,
            "Exercise 1 — Read a history",
            "<p>This is a chatbot's history after a three-message conversation. The model's decisions are "
            "the ones the real model made.</p>"
            + block("The history", history_text)
            + block(
                "week12_answers.md",
                "# Week 12 answers\n\n## Exercise 1\n1. The messages the customer typed:\n"
                "2. How many tool requests were refused, and why:\n"
                '3. If the customer now types "thanks", how many messages does Ollama receive on the next call?\n'
                '4. Why does "Do you sell gift cards?" still go to a person, and why is that acceptable?',
            )
            + "<p><strong>Expected result:</strong> three messages, a number with a reason, a number, and "
            "two sentences.</p>"
            + reveal(
                "Answer key &mdash; Exercise 1",
                block("Answers", ex1_answers)
                + "<p><strong>Why it matters:</strong> the model's first two requests used details nobody "
                "typed. The Toolbox refused them, and each refusal told the model to ask. The change was "
                "filed only with the customer's real details.</p><p><strong>Common mistake:</strong> "
                "counting each tool entry as one message for question 3. "
                "<code>tool_messages</code> sends two for each.</p>",
            ),
        )
    )
    add(
        task(
            14,
            "Exercise 2 — Add a tool",
            "<p>Customers ask whether they can return an order. Add a tool <code>check_return(order_id)</code> "
            "to <code>OrderLookup</code>: a delivered order can be returned within 30 days, anything else "
            "cannot be returned yet. A tool lives in three places: the method with its <code>Args:</code> "
            "docstring, <code>tool_list</code>, and a branch in <code>run</code> that checks the order ID. "
            "Add one test for the tool and one chatbot test that uses <code>FakeModel</code>.</p>"
            f"<p><strong>Expected result:</strong> <code>pytest -v</code> shows {guided_total + 2} "
            "tests passing.</p>"
            + reveal(
                "Answer key &mdash; Exercise 2",
                block(
                    "order_tool.py" + DASH + "add this method to the class",
                    method(M + "order_tool.py", "check_return"),
                )
                + block(
                    "toolbox.py" + DASH + "replace tool_list",
                    method(M + "toolbox.py", "tool_list"),
                )
                + block(
                    "toolbox.py" + DASH + "replace run", method(M + "toolbox.py", "run")
                )
                + block(
                    "tests/test_tools.py" + DASH + "add at the bottom",
                    function(
                        M + "tests/test_tools.py",
                        "test_only_delivered_orders_can_be_returned",
                    ),
                )
                + block(
                    "tests/test_chatbot.py" + DASH + "add at the bottom",
                    function(
                        M + "tests/test_chatbot.py", "test_model_can_ask_about_a_return"
                    ),
                )
                + "<p><strong>Why it works:</strong> the model can only ask for tools in "
                "<code>tool_list</code>, and <code>run</code> refuses any name without a branch. A new "
                "tool needs both, plus the same order-ID checks as the other order tool.</p>"
                "<p><strong>Common mistakes:</strong> adding the method but not the branch, which gives "
                "<em>There is no tool named check_return.</em> Calling the method in <code>tool_list</code> "
                "(<code>check_return()</code>), which fails with a missing argument. Leaving out the "
                "<code>Args:</code> section, so the model guesses what to send.</p>",
            ),
        )
    )
    add(
        task(
            15,
            "Exercise 3 — Turn a guardrail off and watch",
            "<p>In <code>toolbox.py</code>, add <code>return True</code> as the first line of "
            "<code>customer_said</code>'s body, under its docstring. That turns the check off. Run "
            "<code>python3 main.py</code>, type <code>I want to change my shipping address</code>, then "
            "<code>quit</code>, and answer <code>no</code> at the staff review. Copy what you see into "
            "<code>week12_answers.md</code>, then <strong>remove the line</strong>.</p>"
            "<p><strong>Expected result:</strong> a request for an order and an address you never gave. "
            "One real run:</p>"
            + expected(ex3)
            + f"<p>With the check off, the model filed made-up details in {c['ex3_filed'][0]} of "
            f"{c['ex3_filed'][1]} runs while this lab was being written.</p>"
            + reveal(
                "Answer key &mdash; Exercise 3",
                "<p><strong>What happened:</strong> asked to change an address with no details, the model "
                "filled in an order and an address that look like examples, and nothing stopped them. "
                "Staff saw a request that no customer made.</p><p><strong>A good answer says:</strong> a "
                "busy staff member could approve it and send someone's parcel to a made-up address. The "
                "check costs one extra question to the customer. The approval queue is a second line of "
                "defence, not a reason to drop the first.</p><p><strong>Common mistake:</strong> leaving "
                "<code>return True</code> in the file. Run <code>pytest -v</code>: "
                "<code>test_made_up_address_is_refused</code> fails until you remove it.</p>",
            ),
        )
    )
    add(
        task(
            16,
            "Exercise 4 — Keep lookups working when Ollama is down",
            "<p>Write <code>FallbackModel</code> in <code>fallback_model.py</code>. It is handed two "
            "models. Its <code>decide</code> asks the first; if that returns <code>None</code>, it asks "
            "the second. Add a test that hands the chatbot <code>FallbackModel(SilentModel(), "
            "KeywordModel())</code>, then try it in <code>main.py</code> with Ollama switched off.</p>"
            f"<p><strong>Expected result:</strong> {guided_total + 3} tests passing, and with "
            "Ollama off:</p>"
            + expected(ex4)
            + reveal(
                "Answer key &mdash; Exercise 4",
                block("fallback_model.py", w.source("fallback_model.py", rev=None))
                + block(
                    "tests/test_chatbot.py"
                    + DASH
                    + "add this import below the fake_model import",
                    "from fallback_model import FallbackModel",
                )
                + block(
                    "tests/test_chatbot.py" + DASH + "add at the bottom",
                    function(
                        M + "tests/test_chatbot.py",
                        "test_lookups_keep_working_when_the_model_is_down",
                    ),
                )
                + block(
                    "main.py" + DASH + "try this: two imports and one changed line",
                    "from fallback_model import FallbackModel\nfrom keyword_model import KeywordModel\n\n"
                    "model = FallbackModel(OllamaModel(MODEL_NAME), KeywordModel())",
                )
                + "<p><strong>Why it works:</strong> <code>FallbackModel</code> has a <code>decide</code> "
                "method, so the chatbot cannot tell it apart from any other model. It is composition "
                "again: a model made of two models.</p><p><strong>Common mistake:</strong> returning the "
                "second model's decision every time. Only ask it when the first returned "
                "<code>None</code>.</p>",
            ),
        )
    )

    # Part 8
    add(
        section_divider(
            "Part 8 &mdash; Mini-Project: Let Your Assistant Choose Its Tool"
        )
    )
    add(
        task(
            17,
            "Upgrade the assistant you built in Weeks 10 and 11",
            "<p>Your assistant gets the same three upgrades as Sunny: the model chooses when to use the "
            "tool, every request passes one checked door, and one kind of change waits for a person.</p>"
            + check_list(
                [
                    "The model is asked with <code>decide</code>, in a loop with a limit",
                    "At least one tool method the model may ask for, with an <code>Args:</code> docstring",
                    "A toolbox <code>run</code> that refuses unknown tools, empty values, and details the user never typed",
                    "One change that waits in a queue; <code>approve</code> is the only code that makes it, and a second approval changes nothing",
                    "At least one rule still passes something to a person before the model sees it",
                    "Tests use <code>FakeModel</code>: a made-up detail is refused, a request waits, and the handoff happens",
                    "Your main file runs with the real model and ends with a review step",
                    "<code>README.md</code> gains four to six sentences: one request the model handled well, one the door refused, and one thing you had to add to the instructions",
                ]
            )
            + "<p>Sample interaction from the reference solution, one real run:</p>"
            + expected(mini)
            + callout_box(
                "warn",
                "&#x26A0;",
                "Instructions can tell a model when not to use a tool",
                f"<p>Without one sentence about greetings, the reference helper answered <em>hello</em> "
                f"with Monday's open times in {hello_counts[0]} of 5 runs: the model asked for the "
                f"open-times tool on a greeting. Adding <em>Use a tool only when the client asks about "
                f"open times or wants to book</em> made it worse, {hello_counts[1]} of 5. What worked was "
                f"saying what to do instead: <em>If the client only says hello, greet them and ask how "
                f"you can help</em>, {hello_counts[2]} of 5. The lookup only reads, so the mistake was "
                f"harmless; a change tool would have gone to the queue.</p>",
            )
            + "<p><strong>Rubric &mdash; 10 points</strong></p>"
            + concept_table(
                ["Points", "Requirement"],
                [
                    [
                        "3",
                        "The model chooses the tool through <code>decide</code> in a limited loop, and the toolbox checks every request",
                    ],
                    ["2", "One change waits for approval and can only be applied once"],
                    [
                        "2",
                        "Tests use <code>FakeModel</code>, cover a refused detail and a waiting request, and pass without Ollama",
                    ],
                    [
                        "2",
                        "The README section is specific about one good request, one refusal, and one instruction you added",
                    ],
                    ["1", "The full ritual passes"],
                ],
            )
            + reveal(
                "Reference solution &mdash; appointment helper with a tool and a booking queue",
                block("appointment_tool.py", w.source("appointment_tool.py", rev=None))
                + block("booking_queue.py", w.source("booking_queue.py", rev=None))
                + block(
                    "appointment_toolbox.py",
                    w.source("appointment_toolbox.py", rev=None),
                )
                + block("appointment_bot.py", w.source("appointment_bot.py", rev=None))
                + block(
                    "appointment_main.py", w.source("appointment_main.py", rev=None)
                )
                + block(
                    "tests/test_appointment_bot.py",
                    w.source("tests/test_appointment_bot.py", rev=None),
                )
                + "<p><strong>Why it is built this way:</strong> booking moved from a handoff to a request "
                "that waits for the front desk; cancelling and rescheduling still go to a person by rule. "
                "The name and time must come from the client, so the model cannot book a made-up person. "
                "It reuses <code>FakeModel</code>, <code>KeywordModel</code> and <code>OllamaModel</code> "
                "unchanged.</p><p>Use it to compare, not to copy. Your assistant serves a different "
                "business and has its own tool and its own change.</p>",
            ),
        )
    )

    # Part 9
    add(section_divider("Part 9 &mdash; Ritual and Push"))
    add(
        task(
            18,
            "Run the full ritual with Ollama switched off",
            "<p>Quit Ollama first. If your tests pass now, they pass when your repository is graded on a "
            "computer that has never had Ollama.</p>"
            + block(
                "Terminal",
                "ruff format . && ruff check . && pytest -v\n"
                "git add . && git commit -m 'lab 12: tools, guardrails, and approval' && git push",
            )
            + hint(
                "If <code>ruff check</code> stops on a fixable error, the <code>&amp;&amp;</code> chain ends "
                "there and <code>pytest</code> never runs. Run <code>ruff check --fix .</code>, then run the "
                "full first line again."
            ),
        )
    )
    add(
        submit_box(
            "Lab 12 Submission &middot; Git commit + Canvas URL &middot; Completion credit",
            "Tools and Guardrails",
            [
                (
                    "&#x1F4C4;",
                    (
                        "<strong>Files in repo:</strong> <code>toolbox.py</code>, <code>change_queue.py</code>, "
                        "<code>keyword_model.py</code>, <code>fake_model.py</code>, <code>fallback_model.py</code>, "
                        "<code>tests/test_tools.py</code>, <code>week12_answers.md</code>, and your upgraded "
                        "mini-project with its README section."
                    ),
                ),
                (
                    "&#x1F517;",
                    (
                        "<strong>Canvas submission:</strong> Paste your GitHub repository URL. Commit message "
                        "must include <code>lab 12</code>."
                    ),
                ),
                ("&#x2705;", NO_SCREENSHOTS),
            ],
        )
    )
    add(
        prev_next(
            f"{w.PREV[0]}_lab.html",
            w.PREV[1],
            w.PREV[2],
            f"{w.NEXT[0]}_lab.html",
            w.NEXT[1],
            w.NEXT[2],
        )
    )
    add(
        '<div class="page-footer">ISM3232 &middot; Week 12 In-Class Lab &middot; Module 6 &mdash; '
        "Tools and Guardrails: Model-Chosen Tools, Checks, and Approval</div></div>"
    )

    head = head_from("week11_lab.html", "ISM3232 Week 12 In-Class Lab")
    page = f'{head}\n<body>{"".join(p)}\n<script src="../site.js"></script>\n</body></html>\n'
    derived = [
        main_typed,
        off,
        ex3,
        ex4,
        mini,
        history_text,
        ex1_answers,
        shell_orders,
        shell_stock,
        shell_queue,
        "cd ~/ism3232/module06_agents\nsource .venv/bin/activate\npytest -q",
        "from fallback_model import FallbackModel",
        (
            "from fallback_model import FallbackModel\nfrom keyword_model import KeywordModel\n\n"
            "model = FallbackModel(OllamaModel(MODEL_NAME), KeywordModel())"
        ),
        (
            "ruff format . && ruff check . && pytest -v\n"
            "git add . && git commit -m 'lab 12: tools, guardrails, and approval' && git push"
        ),
    ]
    derived.append(esc(""))
    derived.append(
        "# Week 12 answers\n\n## Exercise 1\n1. The messages the customer typed:\n"
        "2. How many tool requests were refused, and why:\n"
        '3. If the customer now types "thanks", how many messages does Ollama receive on the next call?\n'
        '4. Why does "Do you sell gift cards?" still go to a person, and why is that acceptable?'
    )
    return page, derived


if __name__ == "__main__":
    page, _ = build()
    OUT.write_text(page)
    print("wrote", OUT)
