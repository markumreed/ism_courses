import database
from tools import BaysideTools


def make_tools(tmp_path):
    """Build tools over a fresh database with the sample rows."""
    db_file = tmp_path / "test.db"
    database.create_tables(db_file)
    return BaysideTools(db_file)


def customer(text):
    """Build a history that holds one customer message."""
    return [{"role": "user", "content": text}]


def test_look_up_order(tmp_path):
    tools = make_tools(tmp_path)
    assert tools.look_up_order("A101") == "Order A101 is processing."


def test_look_up_order_finds_the_id_in_a_sentence(tmp_path):
    tools = make_tools(tmp_path)
    assert tools.look_up_order("Where is order a100?") == "Order A100 is shipped."


def test_look_up_order_needs_an_exact_id(tmp_path):
    tools = make_tools(tmp_path)
    assert "No order" in tools.look_up_order("A1015")


def test_check_stock_gives_the_count_and_price(tmp_path):
    tools = make_tools(tmp_path)
    reply = tools.check_stock("Is the Rain Jacket in stock?")
    assert reply == "We have 12 of the rain jacket in stock, at $89.00."
    assert tools.check_stock("tent") == "That product was not found."


def test_address_change_waits_and_needs_an_exact_id(tmp_path):
    tools = make_tools(tmp_path)
    assert "No order" in tools.request_address_change("A1000", "9 Pine Street")
    reply = tools.request_address_change("a102", "9 Pine Street")
    assert reply == "Request 1 was sent to staff. The address has not changed yet."
    assert database.find_order(tools.db_file, "A102")["address"] == "88 Pier Street"


def test_check_request_reports_the_decision_without_the_address(tmp_path):
    tools = make_tools(tmp_path)
    tools.request_address_change("A102", "9 Pine Street")
    assert tools.check_request("1") == "Request 1 for order A102 is waiting for staff."
    database.approve_request(tools.db_file, 1)
    reply = tools.check_request("1")
    assert reply == "Request 1 for order A102 was approved."
    assert "Pine" not in reply


def test_check_request_with_a_bad_number(tmp_path):
    tools = make_tools(tmp_path)
    assert tools.check_request("seven") == "Request numbers look like 3."
    assert tools.check_request("7") == "There is no request 7."


def test_unknown_tool_is_refused(tmp_path):
    tools = make_tools(tmp_path)
    reply = tools.run("delete_order", {"order_id": "A100"}, customer("Delete A100"))
    assert reply == "There is no tool named delete_order."


def test_missing_value_is_refused(tmp_path):
    tools = make_tools(tmp_path)
    assert "missing" in tools.run("check_request", {}, customer("What happened?"))


def test_made_up_order_id_is_refused(tmp_path):
    tools = make_tools(tmp_path)
    reply = tools.run("look_up_order", {"order_id": "A101"}, customer("Where is A100?"))
    assert "has not given that order ID" in reply


def test_made_up_address_is_refused_and_nothing_waits(tmp_path):
    tools = make_tools(tmp_path)
    arguments = {"order_id": "A102", "new_address": "123 Main St"}
    reply = tools.run("request_address_change", arguments, customer("Change A102"))
    assert "has not given that address" in reply
    assert database.waiting_requests(tools.db_file) == []


def test_made_up_request_number_is_refused(tmp_path):
    tools = make_tools(tmp_path)
    reply = tools.run(
        "check_request", {"number": 4}, customer("What about my request?")
    )
    assert "has not given that request number" in reply
