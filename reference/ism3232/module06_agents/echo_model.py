# echo_model.py
# Author: [Your Name]


class EchoModel:
    """A model that repeats the last message. It needs no AI and no internet."""

    def reply(self, instructions, history):
        """Return the last message with a few words in front of it."""
        last_message = history[-1]["content"]
        return f"You said: {last_message}"
