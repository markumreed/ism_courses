"""Bayside's filled-in PROPOSAL.md, and the Bayside numbers the pages quote,
generated from the reference app at FULL_REV and its saved evaluation run so
they cannot drift from the code they describe."""

import ast
import re

from pagekit import REF, read
from week13_common import FULL_REV
from week13_starters import CHECKLIST

APP = "bayside_app/"
EVALUATION = REF / "runs" / "bayside_app" / "evaluation.txt"

# The parts of a proposal that are judgement rather than code.
BUSINESS = (
    "Bayside Outfitters is a small outdoor clothing shop that ships orders. Customers "
    "write in to ask where an order is, whether something is in stock, or to change a "
    "shipping address, and staff answer the same questions all day."
)
WHO = "The chat: customers. The Staff tab: staff."
HANDOFF_WHY = (
    "card details must never reach the model, and a payment problem needs a person "
    "who can see the account."
)
NEVER_STORED = "Card numbers."
OUT_OF_SCOPE = [
    "Taking payments or giving refunds.",
    "Proving who a customer is: an order ID is not proof of identity.",
    "Changing anything on an order except its shipping address.",
]
CONVERSATIONS = [0, 2, 4, 6, 7]  # indexes into evaluation.py's CASES
SAFETY = {
    6: "safety: the customer never gave an order ID",
    7: "safety: a customer cannot change the store's facts",
}


def literal(path, name):
    """The value of a top-level `name = <literal>` in an app file at FULL_REV."""
    for node in ast.parse(read(APP + path, FULL_REV)).body:
        if (
            isinstance(node, ast.Assign)
            and getattr(node.targets[0], "id", None) == name
        ):
            return ast.literal_eval(node.value)
    raise ValueError(f"no {name} in {path}")


def tables():
    """[(table, [column definitions], first sample row or None)] from schema.sql."""
    text = read(APP + "schema.sql", FULL_REV)
    result = []
    for name, body in re.findall(
        r"CREATE TABLE IF NOT EXISTS (\w+) \((.*?)\n\);", text, re.DOTALL
    ):
        columns = [
            " ".join(line.strip().rstrip(",").split())
            for line in body.strip().split("\n")
        ]
        row = re.search(
            rf"INSERT OR IGNORE INTO {name} \([^)]*\) VALUES\n\s+(\(.*?\))[,;]\n", text
        )
        result.append((name, columns, row.group(1) if row else None))
    return result


def tools():
    """[(tool, arguments, first docstring line)] in the order tool_list gives them."""
    text = read(APP + "tools.py", FULL_REV)
    listed = text.split("def tool_list")[1].split("    def ")[0]
    result = []
    for name in re.findall(r"self\.(\w+),", listed):
        match = re.search(rf'def {name}\(self, ([^)]*)\):\n\s+"""(.+)', text)
        result.append((name, match.group(1), match.group(2).strip()))
    return result


def approval_target():
    """'table.column' that approve_request changes."""
    body = (
        read(APP + "database.py", FULL_REV)
        .split("def approve_request")[1]
        .split("\ndef ")[0]
    )
    table, column = re.search(r"UPDATE (\w+) SET (\w+) = \?", body).groups()
    return f"{table}.{column}"


def cases():
    return literal("evaluation.py", "CASES")


def case_count():
    return len(cases())


def evaluation_result(index):
    """'0 of 3' for one case, from the saved CPU evaluation run. The run's table
    shows each case's first message cut to 44 characters."""
    label = cases()[index]["messages"][0][:44]
    for line in EVALUATION.read_text().split("\n"):
        if line.startswith(label):
            passed, runs = line.split()[-1].split("/")
            return f"{passed} of {runs}"
    raise ValueError(label)


def evaluation_total():
    for line in EVALUATION.read_text().split("\n"):
        if line.startswith("total"):
            passed, runs = line.split()[-1].split("/")
            return f"{passed} of {runs}"
    raise ValueError("no total line")


def must(case):
    """What a conversation must do, in Week 16's check kinds."""
    kind, value = case["expect"], case.get("value")
    if kind == "tool":
        return f"use {value}"
    if kind == "handoff":
        return "hand off"
    if kind == "says":
        return f'say "{value}"'
    if kind == "never_says":
        return f'never say "{value}"'
    if kind == "queued":
        return f"file {value} change" + ("" if value == 1 else "s")
    raise ValueError(kind)


def example(name):
    """The last message of the first evaluation case that expects this tool."""
    for case in cases():
        if case["expect"] == "tool" and case["value"] == name:
            return case["messages"][-1]
    raise ValueError(name)


def bayside_proposal():
    lookups = [t for t in tools() if not t[0].startswith("request_")]
    changes = [t for t in tools() if t[0].startswith("request_")]
    lines = [
        "# Capstone Proposal: Bayside Outfitters",
        "Author: the course (generated from the Bayside reference app)",
        "",
        "## The business",
        BUSINESS,
        "",
        "## Who uses it",
        WHO,
        "",
        "## Tables",
    ]
    for name, columns, row in tables():
        lines.append(f"{name}: {', '.join(columns)}")
        if row:
            lines.append(f"  example row: {row}")
        else:
            lines.append("  no sample rows: requests appear when the agent files them")
    lines += ["", "## Lookup tools (at least two)"]
    for name, arguments, doc in lookups:
        lines.append(f'{name}({arguments}): {doc} Example question: "{example(name)}"')
    lines += ["", "## Change tool (at least one)"]
    for name, arguments, doc in changes:
        lines.append(
            f"{name}({arguments}): {doc} Approving sets {approval_target()} to the new "
            "value and marks the request approved."
        )
    words = ", ".join(literal("agent.py", "HANDOFF_WORDS"))
    lines += [
        "",
        "## Handoff rule",
        f"Words: {words}   Why a person must handle these: {HANDOFF_WHY}",
    ]
    lines += ["", "## Data it never stores", NEVER_STORED]
    lines += ["", "## Instructions draft", literal("settings.py", "INSTRUCTIONS")]
    lines += ["", "## Five sample conversations"]
    for number, index in enumerate(CONVERSATIONS, 1):
        case = cases()[index]
        said = ", then ".join(f'"{message}"' for message in case["messages"])
        note = f" ({SAFETY[index]})" if index in SAFETY else ""
        lines.append(f"{number}. Customer: {said}   Must: {must(case)}{note}")
    lines += ["", "## Out of scope (at least two)"]
    lines += [f"- {item}" for item in OUT_OF_SCOPE]
    lines += ["", "## Checklist"]
    plain = [re.sub(r"<[^>]+>", "", item) for item in CHECKLIST]
    lines += [f"- [x] {number}. {item}" for number, item in enumerate(plain, 1)]
    return "\n".join(lines)


def section(text, heading):
    """One '## ' section of a proposal, from its heading line to the next '## '."""
    start = text.index(f"## {heading}")
    end = text.find("\n## ", start + 1)
    return text[start : end if end != -1 else len(text)].rstrip("\n")
