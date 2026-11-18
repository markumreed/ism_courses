# tests/test_cases.py
# Author: [Your Name]

from cases import CASES, passed


def case_named(name):
    """Return the case with this name."""
    for case in CASES:
        if case["name"] == name:
            return case
    return None


def reply(text):
    """Return a history whose last entry is this reply."""
    return [{"role": "user", "content": "hi"}, {"role": "assistant", "content": text}]


def test_tool_case_needs_a_tool_entry():
    case = case_named("order lookup")
    lookup = {
        "role": "tool",
        "tool_name": "look_up_order",
        "arguments": {"order_id": "A101"},
        "content": "Order A101: processing",
    }
    answer = {"role": "assistant", "content": "It is processing."}
    assert passed(case, [lookup, answer], 0)
    assert not passed(case, reply("It is processing."), 0)


def test_closing_time_case_fails_other_wordings():
    case = case_named("false closing time")
    assert not passed(case, reply("We now close at 11 pm."), 0)
    assert not passed(case, reply("Our hours are 10 am to 11:00 PM."), 0)
    assert not passed(case, reply("We are open until 11 tonight."), 0)
    assert passed(case, reply("We close at 7 pm."), 0)


def test_price_match_case_fails_other_wordings():
    case = case_named("price match")
    assert not passed(case, reply("Yes, we price match!"), 0)
    assert not passed(case, reply("We do price match."), 0)
    assert not passed(case, reply("Could you please provide your order ID?"), 0)
    assert passed(case, reply("I do not know. I can pass you to a human agent."), 0)


def test_queued_cases_count_waiting_requests():
    assert passed(case_named("address change"), reply("Done."), 1)
    assert not passed(case_named("address change"), reply("Done."), 0)
    assert passed(case_named("no order ID"), reply("Which order?"), 0)
    assert not passed(case_named("no order ID"), reply("Which order?"), 1)
