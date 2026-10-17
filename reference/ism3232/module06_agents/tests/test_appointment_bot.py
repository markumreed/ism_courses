from appointment_bot import AppointmentHelper
from appointment_tool import AppointmentBook
from appointment_toolbox import AppointmentToolbox
from booking_queue import BookingQueue
from fake_model import FakeModel
from keyword_model import KeywordModel


def make_helper(model):
    """Build a fresh helper with its own tools and the model it is given."""
    book = AppointmentBook({"monday": "9:00 am and 2:30 pm", "friday": "none"})
    tools = AppointmentToolbox(book, BookingQueue(book))
    return AppointmentHelper("Robin", "Be clear.", tools, model)


def booking(day, time, client):
    """Build the decision a model returns when it wants to request a booking."""
    arguments = {"day": day, "time": time, "client": client}
    return {"tool": "request_booking", "arguments": arguments}


def test_model_can_ask_for_open_times():
    model = FakeModel(
        [
            {"tool": "check_open_times", "arguments": {"day": "Monday"}},
            {"text": "Monday has 9:00 am and 2:30 pm."},
        ]
    )
    helper = make_helper(model)
    helper.respond("When can I come in on Monday?")
    assert helper.history[1]["content"] == "Open times on monday: 9:00 am and 2:30 pm."


def test_booking_waits_for_the_front_desk():
    model = FakeModel([booking("monday", "9:00 am", "Dana Cruz"), {"text": "Sent."}])
    helper = make_helper(model)
    helper.respond("Please book Monday at 9:00 am for Dana Cruz")
    assert len(helper.tools.booking_queue.waiting()) == 1
    assert helper.tools.appointment_book.bookings == []


def test_made_up_name_is_refused():
    model = FakeModel([booking("monday", "9:00 am", "Jane Doe"), {"text": "Name?"}])
    helper = make_helper(model)
    helper.respond("Please book Monday at 9:00 am")
    assert "has not given that name" in helper.history[1]["content"]
    assert helper.tools.booking_queue.waiting() == []


def test_approval_records_the_booking_once():
    book = AppointmentBook({"monday": "9:00 am and 2:30 pm"})
    queue = BookingQueue(book)
    queue.request_booking("monday", "9:00 am", "Dana Cruz")
    queue.approve(1)
    queue.approve(1)
    assert len(book.bookings) == 1


def test_cancellation_goes_to_the_front_desk():
    helper = make_helper(FakeModel([]))
    assert "front desk" in helper.respond("Please cancel my appointment")


def test_keyword_model_still_greets():
    helper = make_helper(KeywordModel())
    assert helper.respond("hello") == "Hello! How can I help you today?"
