# appointment_bot.py
# Author: [Your Name]

HANDOFF_WORDS = ["book", "cancel", "reschedule"]


class AppointmentHelper:
    """An appointment helper. Rules handle the schedule. A model handles the rest."""

    def __init__(self, name, instructions, appointment_book, model):
        """Set up one helper with its own name, instructions, tool, model, and history."""
        self.name = name
        self.instructions = instructions
        self.appointment_book = appointment_book
        self.model = model
        self.history = []

    def respond(self, user_message):
        """Record the user's message, choose a reply, record it, and return it."""
        self.history.append({"role": "user", "content": user_message})
        reply = self.choose_reply(user_message)
        self.history.append({"role": "assistant", "content": reply})
        return reply

    def choose_reply(self, user_message):
        """Use a rule when one applies. Otherwise ask the model."""
        text = user_message.lower()
        if self.needs_human(text):
            return "I can't change the schedule. I'm passing you to the front desk."
        if "open" in text or "available" in text:
            return self.times_reply(user_message)
        return self.model_reply()

    def model_reply(self):
        """Ask the model for a reply. Give a safe answer if the model has none."""
        reply = self.model.reply(self.instructions, self.history)
        if reply is None:
            return "Sorry, I can't answer that right now. Please try again in a moment."
        return reply

    def needs_human(self, text):
        """Return True if the message asks to change the schedule."""
        for word in HANDOFF_WORDS:
            if word in text:
                return True
        return False

    def times_reply(self, user_message):
        """Use the appointment book to answer a question about open times."""
        day = self.appointment_book.find_day(user_message)
        if day is None:
            return "Which day? I can check Monday, Wednesday, or Friday."
        times = self.appointment_book.times_for(day)
        return f"Open times on {day}: {times}."
