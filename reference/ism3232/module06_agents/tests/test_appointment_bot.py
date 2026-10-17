from appointment_bot import AppointmentHelper
from appointment_tool import AppointmentBook
from mock_model import MockModel


def make_helper():
    """Build a fresh helper with its own tool for each test."""
    book = AppointmentBook({"monday": "9:00 am and 2:30 pm", "friday": "none"})
    return AppointmentHelper("Robin", "Be clear.", book, MockModel())


def test_open_times_question_uses_the_tool():
    helper = make_helper()
    reply = helper.respond("What times are open on Monday?")
    assert reply == "Open times on monday: 9:00 am and 2:30 pm."


def test_question_without_a_known_day_asks_for_one():
    helper = make_helper()
    assert "Which day?" in helper.respond("What times are open on Sunday?")


def test_booking_request_goes_to_a_human():
    helper = make_helper()
    assert "front desk" in helper.respond("Please book me for Monday at 9")


def test_unknown_request_gets_a_safe_reply():
    helper = make_helper()
    assert "not sure" in helper.respond("What is your favorite color?")


def test_history_grows_by_two_each_turn():
    helper = make_helper()
    helper.respond("hello")
    helper.respond("What is open on Friday?")
    assert len(helper.history) == 4


def test_other_messages_go_to_the_model():
    helper = make_helper()
    assert helper.respond("hello") == "Hello! How can I help you today?"
