"""Facts shared by the Week 12 page builders: titles, counts from the saved
runs, and small pieces of real output generated from the reference code."""

import json
import sys

import runs
from pagekit import REF, read

WEEK = "week12"
TITLE = "Tools and Guardrails — Model-Chosen Tools, Checks &amp; Approval"
TITLE_TEXT = "Tools and Guardrails — Model-Chosen Tools, Checks & Approval"
EYEBROW_COLOR = "#fb7185"
UNIT = "Unit 3 · Building AI Agents"
PREV = (
    "week11",
    "Week 11",
    "Talking to a Local Model — Ollama, Instructions &amp; History",
)
NEXT = ("week13", "Week 13", "Capstone Design &amp; SQL")
FOLDER = REF / "module06_agents"
# The commit where module06_agents holds the end of the guided parts, before
# the exercise and mini-project answers were added. (c805807 was the first such
# checkpoint; 5bead57 adds exact order IDs in the change queue.)
GUIDED = "5bead57"


def run_text(name):
    """The saved transcript, exactly as written."""
    return (REF / "runs" / WEEK / name).read_text().rstrip("\n")


def counts():
    """Every count the Week 12 pages quote, computed from the saved runs."""
    a101 = runs.load(WEEK, "a101_after_a100.txt")
    no_guard = runs.load(WEEK, "address_no_guard.txt")
    with_guard = runs.load(WEEK, "address_with_guard.txt")
    three = runs.load(WEEK, "address_three_turns.txt")
    echo = runs.load(WEEK, "no_request_echo.txt")
    closing = runs.load(WEEK, "false_closing_time.txt")
    ex3 = runs.load(WEEK, "exercise3_no_guard.txt")

    def a101_right(run):
        asked = ("look_up_order", {"order_id": "A101"}) in [
            (n, a) for n, a, _ in run["tools"]
        ]
        return asked and "processing" in run["turns"][1][1]

    def three_right(run):
        queued = run["queued"]
        return (
            len(queued) == 1
            and queued[0]["order_id"] == "A102"
            and queued[0]["new_address"] == "9 Pine Street, Tampa"
        )

    return {
        "a101": runs.count(a101, a101_right),
        "no_guard_filed": runs.count(no_guard, lambda r: len(r["queued"]) > 0),
        "with_guard_filed": runs.count(with_guard, lambda r: len(r["queued"]) > 0),
        "with_guard_refused": runs.count(with_guard, runs.refused),
        "three_right": runs.count(three, three_right),
        "three_refused_then_right": runs.count(
            three, lambda r: runs.refused(r) and three_right(r)
        ),
        "echo_off_repeats": runs.count(echo, runs.repeated_lookup),
        "closing_agrees": runs.count(closing, lambda r: "11" in r["turns"][0][1]),
        "ex3_filed": runs.count(ex3, lambda r: len(r["queued"]) > 0),
    }


def first_run(name):
    """The text of run 1 of a count_runs transcript."""
    text = run_text(name)
    return text.split("--- run 2")[0].replace("--- run 1\n", "").rstrip("\n")


def tool_schema():
    """What Ollama builds from OrderLookup.look_up_order, generated now from the
    reference code with the ollama package's own converter."""
    sys.path.insert(0, str(FOLDER))
    from ollama._utils import convert_function_to_tool
    from order_tool import OrderLookup

    tool = convert_function_to_tool(OrderLookup({}).look_up_order)
    return json.dumps(tool.model_dump(exclude_none=True)["function"], indent=2)


def lookup_history():
    """The history after one order question. The chatbot runs for real; a
    FakeModel plays back the decision and the reply the real model gave in
    run 1 of a101_after_a100.txt, so the output is deterministic."""
    sys.path.insert(0, str(FOLDER))
    from change_queue import ChangeQueue
    from chatbot import SupportChatbot
    from fake_model import FakeModel
    from order_tool import OrderLookup
    from stock_tool import StockLookup
    from toolbox import Toolbox

    real = runs.load(WEEK, "a101_after_a100.txt")[0]
    name, arguments, _ = real["tools"][0]
    decisions = [{"tool": name, "arguments": arguments}, {"text": real["turns"][0][1]}]
    orders = {"A100": {"status": "shipped", "address": "14 Bay Road"}}
    order_tool = OrderLookup(orders)
    tools = Toolbox(order_tool, StockLookup({}), ChangeQueue(order_tool))
    bot = SupportChatbot("Sunny", "Be friendly.", tools, FakeModel(decisions))
    bot.respond(real["turns"][0][0])
    return "\n".join(str(entry) for entry in bot.history)


def source(name, rev=GUIDED):
    """A module06_agents file as students have it after the guided parts."""
    return read(f"module06_agents/{name}", rev)


# Standalone snippets the lecture and slides show. The builders run each one
# inside the guided folder and print its real output under it.
SNIPPETS = {
    "decision": """decision = {"tool": "look_up_order", "arguments": {"order_id": "A101"}}
print("text" in decision)
print(decision["tool"], decision["arguments"]["order_id"])""",
    "loop": """from change_queue import ChangeQueue
from chatbot import SupportChatbot
from fake_model import FakeModel
from order_tool import OrderLookup
from stock_tool import StockLookup
from toolbox import Toolbox

orders = {"A101": {"status": "processing", "address": "3 Gull Lane"}}
order_tool = OrderLookup(orders)
tools = Toolbox(order_tool, StockLookup({}), ChangeQueue(order_tool))
model = FakeModel(
    [
        {"tool": "look_up_order", "arguments": {"order_id": "A101"}},
        {"text": "Order A101 is still processing."},
    ]
)
bot = SupportChatbot("Sunny", "Be brief.", tools, model)
print(bot.respond("Has my package A101 shipped?"))
for entry in bot.history:
    print(entry["role"], "|", entry["content"])""",
    "door": """from change_queue import ChangeQueue
from order_tool import OrderLookup
from stock_tool import StockLookup
from toolbox import Toolbox

orders = {"A100": {"status": "shipped", "address": "14 Bay Road"}}
order_tool = OrderLookup(orders)
tools = Toolbox(order_tool, StockLookup({}), ChangeQueue(order_tool))
history = [{"role": "user", "content": "I want to change my shipping address"}]

print(tools.run("delete_order", {"order_id": "A100"}, history))
print(tools.run("look_up_order", {"order_id": " "}, history))
made_up = {"order_id": "A100", "new_address": "123 Main St"}
print(tools.run("request_address_change", made_up, history))""",
    "queue": """from change_queue import ChangeQueue
from order_tool import OrderLookup

orders = {"A100": {"status": "shipped", "address": "14 Bay Road"}}
queue = ChangeQueue(OrderLookup(orders))

print(queue.request_address_change("A100", "9 Pine Street"))
print(orders["A100"]["address"])
print(queue.approve(1))
print(orders["A100"]["address"])
print(queue.approve(1))""",
}


def snippet_outputs():
    """Run every snippet in a copy of the guided folder. Returns {name: output}."""
    from pagekit import folder_at, run_snippet

    folder = folder_at(GUIDED)
    return {name: run_snippet(code, folder) for name, code in SNIPPETS.items()}
