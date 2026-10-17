"""Measure the prompt the course model receives for a long Bayside chat, trimmed
to what OllamaModel.decide sends and untrimmed.

Run from the repository root with Ollama running:
    python reference/ism3232/runs/bayside_app/prompt_size.py
"""

import os
import shutil
import sys
import tempfile
from pathlib import Path

APP = Path(
    sys.argv[1] if len(sys.argv) > 1 else "reference/ism3232/bayside_app"
).resolve()
work = Path(tempfile.mkdtemp(prefix="bayside-prompt-"))
for path in APP.glob("*.py"):
    shutil.copy(path, work)
shutil.copy(APP / "schema.sql", work)
os.chdir(work)
sys.path.insert(0, str(work))

from agent import SupportChatbot
from database import create_tables
from keyword_model import KeywordModel
from ollama import chat
from ollama_model import MAX_MESSAGES, OllamaModel
from settings import INSTRUCTIONS, MODEL_NAME
from tools import BaysideTools

create_tables("prompt.db")
tools = BaysideTools("prompt.db")
bot = SupportChatbot("Sunny", INSTRUCTIONS, tools, KeywordModel())
questions = [
    "hello",
    "Where is order A100?",
    "Is the rain jacket in stock?",
    "Where is order A104?",
    "Is the fleece vest in stock?",
]
count = 0
while len(bot.history) < 40:
    bot.respond(questions[count % len(questions)])
    count += 1
model = OllamaModel(MODEL_NAME)
for label, history in (
    (f"last {MAX_MESSAGES} entries (what decide sends)", bot.history[-MAX_MESSAGES:]),
    (f"all {len(bot.history)} entries", bot.history),
):
    messages = [{"role": "system", "content": INSTRUCTIONS}]
    for message in history:
        if message["role"] == "tool":
            messages = messages + model.tool_messages(message)
        else:
            messages.append(message)
    messages.append({"role": "user", "content": "Thanks!"})
    response = chat(model=MODEL_NAME, messages=messages, tools=tools.tool_list())
    print(
        f"{label}: {len(messages)} messages, {response.prompt_eval_count} prompt tokens"
    )
