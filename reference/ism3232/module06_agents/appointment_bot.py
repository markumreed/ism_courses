# appointment_bot.py
# Author: [Your Name]

HANDOFF_WORDS = ["cancel", "reschedule"]
MAX_TOOL_ROUNDS = 3


class AppointmentHelper:
    """An appointment helper. The model decides. The toolbox checks every request."""

    def __init__(self, name, instructions, tools, model):
        """Set up one helper with its own name, instructions, tools, model, and history."""
        self.name = name
        self.instructions = instructions
        self.tools = tools
        self.model = model
        self.history = []

    def respond(self, user_message):
        """Record the user's message, choose a reply, record it, and return it."""
        self.history.append({"role": "user", "content": user_message})
        reply = self.choose_reply(user_message)
        self.history.append({"role": "assistant", "content": reply})
        return reply

    def choose_reply(self, user_message):
        """Pass cancellations and changes to the front desk. Send the rest to the model."""
        if self.needs_human(user_message.lower()):
            return "I can't change a booking. I'm passing you to the front desk."
        return self.model_reply()

    def needs_human(self, text):
        """Return True if the message asks to cancel or move a booking."""
        for word in HANDOFF_WORDS:
            if word in text:
                return True
        return False

    def model_reply(self):
        """Ask the model. Run each tool it asks for, then ask again, up to a limit."""
        rounds = 0
        while rounds < MAX_TOOL_ROUNDS:
            tool_list = self.tools.tool_list()
            decision = self.model.decide(self.instructions, self.history, tool_list)
            if decision is None:
                return "Sorry, I can't answer that right now. Please try again in a moment."
            if "text" in decision:
                return decision["text"]
            name = decision["tool"]
            arguments = decision["arguments"]
            result = self.tools.run(name, arguments, self.history)
            self.history.append(
                {
                    "role": "tool",
                    "tool_name": name,
                    "arguments": arguments,
                    "content": result,
                }
            )
            rounds += 1
        return "Sorry, I couldn't finish that. I'm passing you to the front desk."
