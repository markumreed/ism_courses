import database
from agent import SupportChatbot
from fake_model import FakeModel
from fallback_model import FallbackModel
from keyword_model import KeywordModel
from tools import BaysideTools


class SilentModel:
    """A model that never has an answer. It stands in for Ollama being switched off."""

    def decide(self, instructions, history, tools):
        return None


def make_bot(tmp_path, model):
    """Build a chatbot over a fresh database with the sample rows."""
    db_file = tmp_path / "test.db"
    database.create_tables(db_file)
    return SupportChatbot("Sunny", "Be friendly.", BaysideTools(db_file), model)


def ask_for_tool(name, arguments):
    """Build the decision a model returns when it wants a tool."""
    return {"tool": name, "arguments": arguments}


def test_keyword_model_looks_up_an_order_in_the_database(tmp_path):
    bot = make_bot(tmp_path, KeywordModel())
    assert bot.respond("Where is order A104?") == "Order A104 is shipped."


def test_model_chosen_lookup_answers_from_the_database(tmp_path):
    model = FakeModel(
        [
            ask_for_tool("look_up_order", {"order_id": "A101"}),
            {"text": "Your package A101 is still processing."},
        ]
    )
    bot = make_bot(tmp_path, model)
    bot.respond("Has my package A101 shipped?")
    assert bot.history[1]["content"] == "Order A101 is processing."


def test_address_change_waits_in_the_database(tmp_path):
    model = FakeModel(
        [
            ask_for_tool(
                "request_address_change",
                {"order_id": "A102", "new_address": "9 Pine Street, Tampa"},
            ),
            {"text": "Sent to staff."},
        ]
    )
    bot = make_bot(tmp_path, model)
    bot.respond("Change the address on order A102 to 9 Pine Street, Tampa")
    db_file = bot.tools.db_file
    assert len(database.waiting_requests(db_file)) == 1
    assert database.find_order(db_file, "A102")["address"] == "88 Pier Street"


def test_made_up_address_never_reaches_the_database(tmp_path):
    model = FakeModel(
        [
            ask_for_tool(
                "request_address_change",
                {"order_id": "A102", "new_address": "123 Main St"},
            ),
            {"text": "What is the new address?"},
        ]
    )
    bot = make_bot(tmp_path, model)
    bot.respond("Please change the address on order A102")
    assert database.waiting_requests(bot.tools.db_file) == []


def test_customer_can_ask_what_staff_decided(tmp_path):
    model = FakeModel(
        [
            ask_for_tool("check_request", {"number": "1"}),
            {"text": "It was approved."},
        ]
    )
    bot = make_bot(tmp_path, model)
    database.add_change_request(bot.tools.db_file, "A102", "9 Pine Street")
    database.approve_request(bot.tools.db_file, 1)
    bot.respond("What happened to request 1?")
    assert bot.history[1]["content"] == "Request 1 for order A102 was approved."


def test_payment_question_never_reaches_the_model(tmp_path):
    bot = make_bot(tmp_path, FakeModel([]))
    assert "human" in bot.respond("Can I pay with a different card?")


def test_loop_stops_after_three_tool_rounds(tmp_path):
    request = ask_for_tool("look_up_order", {"order_id": "A100"})
    bot = make_bot(tmp_path, FakeModel([request, request, request]))
    assert "human" in bot.respond("Where is order A100?")


def test_safe_reply_when_the_model_has_no_answer(tmp_path):
    bot = make_bot(tmp_path, SilentModel())
    assert "try again" in bot.respond("hello")


def test_lookups_keep_working_when_the_model_is_down(tmp_path):
    bot = make_bot(tmp_path, FallbackModel(SilentModel(), KeywordModel()))
    assert bot.respond("Is the day pack in stock?") == (
        "We have 0 of the day pack in stock, at $45.00."
    )


def test_blank_address_is_refused(tmp_path):
    model = FakeModel(
        [
            ask_for_tool(
                "request_address_change", {"order_id": "A102", "new_address": " "}
            ),
            {"text": "What is the new address?"},
        ]
    )
    bot = make_bot(tmp_path, model)
    bot.respond("Please change the address on order A102")
    assert (
        bot.history[1]["content"] == "The order ID and the new address are both needed."
    )
    assert database.waiting_requests(bot.tools.db_file) == []
