"""Ask the Week 12 mini-project helper "hello" five times under three versions of
its instructions. Run from
reference/ism3232/module06_agents with Ollama running on the CPU."""

import ast
import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))

from appointment_bot import AppointmentHelper
from appointment_tool import AppointmentBook
from appointment_toolbox import AppointmentToolbox
from booking_queue import BookingQueue
from ollama_model import OllamaModel

tree = ast.parse(Path("appointment_main.py").read_text())
consts = {}
for node in tree.body:
    if isinstance(node, ast.Assign) and node.targets[0].id in (
        "OPEN_TIMES",
        "INSTRUCTIONS",
    ):
        consts[node.targets[0].id] = ast.literal_eval(node.value)
GREET = "If the client only says hello, greet them and ask how you can help.\n"
TOOL_RULE = "\nUse a tool only when the client asks about open times or wants to book."
WITHOUT_GREET = consts["INSTRUCTIONS"].replace(GREET, "")
for label, instructions in (
    ("without the greeting sentence", WITHOUT_GREET),
    ("without it, plus: " + TOOL_RULE.strip(), WITHOUT_GREET + TOOL_RULE),
    ("as written, with: " + GREET.strip(), consts["INSTRUCTIONS"]),
):
    print(f"== {label}")
    for run in range(1, 6):
        book = AppointmentBook(dict(consts["OPEN_TIMES"]))
        tools = AppointmentToolbox(book, BookingQueue(book))
        helper = AppointmentHelper(
            "Robin", instructions, tools, OllamaModel("granite4.1:3b")
        )
        reply = helper.respond("hello")
        used = [
            (e["tool_name"], e["arguments"])
            for e in helper.history
            if e["role"] == "tool"
        ]
        print(f"run {run}: Robin: {reply}")
        print(f"  tools: {used}")
