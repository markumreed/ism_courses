# appointment_main.py
# Author: [Your Name]

from appointment_bot import AppointmentHelper
from appointment_tool import AppointmentBook
from ollama_model import OllamaModel

OPEN_TIMES = {
    "monday": "9:00 am and 2:30 pm",
    "wednesday": "11:00 am",
    "friday": "none",
}

INSTRUCTIONS = """You are Robin, an assistant for Bayside Tax Help.
Answer in one short sentence.
The office is at 40 Harbor Street, on the second floor.
Bring a photo ID and last year's tax return to your appointment.
Only state facts that appear in these instructions.
If you do not know, say you do not know and offer to pass the client to the front desk."""

appointment_book = AppointmentBook(OPEN_TIMES)
model = OllamaModel("granite4.1:3b")
helper = AppointmentHelper("Robin", INSTRUCTIONS, appointment_book, model)

print("Type a message, or type quit to stop.")
user_message = input("You: ")
while user_message != "quit":
    print(f"{helper.name}: {helper.respond(user_message)}")
    user_message = input("You: ")

print(f"Messages in this conversation: {len(helper.history)}")
