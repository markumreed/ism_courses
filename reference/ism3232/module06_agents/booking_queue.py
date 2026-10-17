# booking_queue.py
# Author: [Your Name]


class BookingQueue:
    """Bookings waiting for the front desk to approve. Nothing is booked until then."""

    def __init__(self, appointment_book):
        """Start with no requests. Approved bookings go into the appointment book."""
        self.appointment_book = appointment_book
        self.requests = []

    def request_booking(self, day, time, client):
        """Ask the front desk to book an appointment. The front desk must approve it.

        Args:
            day: The day of the week, like Monday.
            time: The time, like 9:00 am.
            client: The client's full name.
        """
        found = self.appointment_book.find_day(day)
        if found is None:
            return "That day was not found. I can check Monday, Wednesday, or Friday."
        number = len(self.requests) + 1
        request = {
            "number": number,
            "day": found,
            "time": time,
            "client": client,
            "status": "waiting",
        }
        self.requests.append(request)
        return f"Request {number} was sent to the front desk. Nothing is booked yet."

    def waiting(self):
        """Return the requests that are still waiting for a decision."""
        result = []
        for request in self.requests:
            if request["status"] == "waiting":
                result.append(request)
        return result

    def find(self, number):
        """Return the request with this number, or None."""
        for request in self.requests:
            if request["number"] == number:
                return request
        return None

    def approve(self, number):
        """Approve one waiting request and record the booking."""
        request = self.find(number)
        if request is None:
            return f"There is no request {number}."
        if request["status"] != "waiting":
            return f"Request {number} is already {request['status']}."
        request["status"] = "approved"
        self.appointment_book.add_booking(
            request["day"], request["time"], request["client"]
        )
        return f"Request {number} approved."

    def reject(self, number):
        """Reject one waiting request. Nothing is booked."""
        request = self.find(number)
        if request is None:
            return f"There is no request {number}."
        if request["status"] != "waiting":
            return f"Request {number} is already {request['status']}."
        request["status"] = "rejected"
        return f"Request {number} rejected."
