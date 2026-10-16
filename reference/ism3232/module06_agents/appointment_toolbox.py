# appointment_toolbox.py
# Author: [Your Name]


class AppointmentToolbox:
    """Every tool request from the model comes through here and is checked."""

    def __init__(self, appointment_book, booking_queue):
        """Hold the tools the model is allowed to ask for."""
        self.appointment_book = appointment_book
        self.booking_queue = booking_queue

    def tool_list(self):
        """Return the tools the model may ask for. They are not called here."""
        return [
            self.appointment_book.check_open_times,
            self.booking_queue.request_booking,
        ]

    def run(self, name, arguments, history):
        """Check one tool request. Run the tool only if every check passes."""
        if name == "check_open_times":
            day = self.clean(arguments, "day")
            if day == "":
                return "The day is missing. Ask the client which day."
            return self.appointment_book.check_open_times(day)
        if name == "request_booking":
            day = self.clean(arguments, "day")
            time = self.clean(arguments, "time")
            client = self.clean(arguments, "client")
            if day == "" or time == "" or client == "":
                return "The day, the time, and the client's name are all needed."
            if not self.client_said(history, time):
                return "The client has not given that time. Ask them for it."
            if not self.client_said(history, client):
                return "The client has not given that name. Ask them for it."
            return self.booking_queue.request_booking(day, time, client)
        return f"There is no tool named {name}."

    def clean(self, arguments, key):
        """Return one argument as text without extra spaces, or "" if it is missing."""
        return str(arguments.get(key, "")).strip()

    def client_said(self, history, text):
        """Return True if text appears in a message the client typed."""
        for message in history:
            if message["role"] == "user" and text.lower() in message["content"].lower():
                return True
        return False
