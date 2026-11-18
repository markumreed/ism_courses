# evaluation.py
# Author: [Your Name]

from agent import SupportChatbot
from cases import CASES, passed
from database import reset_database, waiting_requests
from ollama_model import OllamaModel
from settings import INSTRUCTIONS, MODEL_NAME
from tools import BaysideTools

EVAL_DB = "evaluation.db"
RUNS = 3


def model_is_running():
    """Return True if the course model answers a one-word question."""
    model = OllamaModel(MODEL_NAME)
    hello = [{"role": "user", "content": "hello"}]
    return model.reply("Answer in one word.", hello) is not None


def run_case(case):
    """Run one case RUNS times, each with a fresh database. Return how many passed."""
    passes = 0
    run = 0
    while run < RUNS:
        reset_database(EVAL_DB)
        tools = BaysideTools(EVAL_DB)
        bot = SupportChatbot("Sunny", INSTRUCTIONS, tools, OllamaModel(MODEL_NAME))
        for message in case["messages"]:
            bot.respond(message)
        if passed(case, bot.history, len(waiting_requests(EVAL_DB))):
            passes += 1
        run += 1
    return passes


if model_is_running():
    print(f"{'case':<20}passes")
    total = 0
    for case in CASES:
        passes = run_case(case)
        total += passes
        print(f"{case['name']:<20}{passes}/{RUNS}")
    print(f"{'total':<20}{total}/{RUNS * len(CASES)}")
else:
    print("The course model did not answer. Is Ollama running?")
    print(
        f"Start it with: ollama serve    Download the model with: ollama pull {MODEL_NAME}"
    )
