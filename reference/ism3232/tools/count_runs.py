"""Run one conversation several times against the course model and print each run.

Run it from a Week 12 lab folder (it imports that folder's classes and reads
MODEL_NAME, INSTRUCTIONS, ORDERS and STOCK from its main.py without running it):

  python ../tools/count_runs.py 5 "Has my package A101 shipped?"
  python ../tools/count_runs.py 5 --no-guard "I want to change my shipping address"
  python ../tools/count_runs.py 5 --no-request-echo "Where is order A100?"
  python ../tools/count_runs.py 1 --keyword "Where is order A100?"

Each quoted message is one customer turn; together they make one conversation.
--no-guard turns off the customer-said check, --no-request-echo stops OllamaModel
from recording the model's own tool request, --keyword uses KeywordModel.
"""

import ast
import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))

from change_queue import ChangeQueue
from chatbot import SupportChatbot
from keyword_model import KeywordModel
from order_tool import OrderLookup
from stock_tool import StockLookup
from toolbox import Toolbox


def read_settings(path="main.py"):
    """Return the constant values assigned at the top level of main.py."""
    settings = {}
    for node in ast.parse(Path(path).read_text()).body:
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
            if name in ("MODEL_NAME", "INSTRUCTIONS", "ORDERS", "STOCK"):
                settings[name] = ast.literal_eval(node.value)
    return settings


def make_bot(settings, use_keyword):
    """Build a fresh chatbot with fresh copies of the orders and stock."""
    orders = {key: dict(value) for key, value in settings["ORDERS"].items()}
    order_tool = OrderLookup(orders)
    tools = Toolbox(
        order_tool, StockLookup(dict(settings["STOCK"])), ChangeQueue(order_tool)
    )
    if use_keyword:
        model = KeywordModel()
    else:
        from ollama_model import OllamaModel

        model = OllamaModel(settings["MODEL_NAME"])
    return SupportChatbot("Sunny", settings["INSTRUCTIONS"], tools, model)


def main(argv):
    runs = int(argv[0])
    flags = [arg for arg in argv[1:] if arg.startswith("--")]
    messages = [arg for arg in argv[1:] if not arg.startswith("--")]
    if "--no-guard" in flags:
        Toolbox.customer_said = lambda self, history, text: True
    if "--no-request-echo" in flags:
        from ollama_model import OllamaModel

        OllamaModel.tool_messages = lambda self, m: [
            {"role": "tool", "tool_name": m["tool_name"], "content": m["content"]}
        ]
    settings = read_settings()
    for run in range(1, runs + 1):
        bot = make_bot(settings, "--keyword" in flags)
        print(f"--- run {run}")
        for message in messages:
            print(f"You: {message}")
            print(f"Sunny: {bot.respond(message)}")
        for entry in bot.history:
            if entry["role"] == "tool":
                print(
                    f"  tool {entry['tool_name']} {entry['arguments']} -> {entry['content']}"
                )
        for request in bot.tools.change_queue.requests:
            print(f"  queued {request}")


if __name__ == "__main__":
    main(sys.argv[1:])
