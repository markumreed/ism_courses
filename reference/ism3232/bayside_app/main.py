# main.py
# Author: [Your Name]

from agent import SupportChatbot
from database import (
    all_orders,
    approve_request,
    create_tables,
    reject_request,
    waiting_requests,
)
from ollama_model import OllamaModel
from settings import DB_FILE, INSTRUCTIONS, MODEL_NAME
from tools import BaysideTools

create_tables(DB_FILE)
bot = SupportChatbot(
    "Sunny", INSTRUCTIONS, BaysideTools(DB_FILE), OllamaModel(MODEL_NAME)
)

print("Type a message, or type quit to stop.")
user_message = input("You: ")
while user_message != "quit":
    print(f"{bot.name}: {bot.respond(user_message)}")
    user_message = input("You: ")

print(f"Messages in this conversation: {len(bot.history)}")

print("Staff review")
for request in waiting_requests(DB_FILE):
    number = request["number"]
    print(f"Request {number}: {request['order_id']} to {request['new_address']}")
    answer = input("Approve? yes or no: ")
    if answer == "yes":
        print(approve_request(DB_FILE, number))
    elif answer == "no":
        print(reject_request(DB_FILE, number))
    else:
        print(f"Request {number} is still waiting.")

for order in all_orders(DB_FILE):
    print(order["order_id"], order["address"])
