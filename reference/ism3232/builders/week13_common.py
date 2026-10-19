"""Facts shared by the Week 13 page builders: titles and links, the exercise
answers, the sqlite3 sessions the pages show, and the saved transcripts of
those sessions, cut into the parts each page quotes."""

import sys
import tempfile
from pathlib import Path

from pagekit import REF, read

WEEK = "week13"
TITLE = "Agent Design &amp; SQL — Proposal, Schema &amp; sqlite3"
TITLE_TEXT = "Agent Design & SQL — Proposal, Schema & sqlite3"
EYEBROW_COLOR = "#fbbf24"
UNIT = "Unit 4 · Capstone Build"
PREV = (
    "week12",
    "Week 12",
    "Tools and Guardrails — Model-Chosen Tools, Checks &amp; Approval",
)
NEXT = ("week14", "Week 14", "Python + SQL Integration")
# Bayside reference app checkpoints (reference/ism3232/README.md).
SCHEMA_REV = "04bc8c9"  # Week 13: schema.sql only
FULL_REV = "172d6ad"  # the whole app after the final review fixes
RUNS = REF / "runs" / WEEK
COMMIT = "lab 13: proposal and schema"
REPO = "ism3232-module07"
GITIGNORE_LINE = (
    "echo '.venv/' > .gitignore && echo '__pycache__/' >> .gitignore"
    " && echo '*.db' >> .gitignore"
)

SETUP = [".read schema.sql", ".mode column", ".headers on"]
# Every new sqlite3 session starts in list mode with headers off, so pages
# that reopen a database show these two lines again.
DISPLAY = [".mode column", ".headers on"]

# Exercise answers. Only the lab page (inside its answer keys) and the lab
# slides may show these lines.
EX1 = "SELECT order_id, customer FROM orders WHERE status = 'processing' ORDER BY customer;"
EX2 = "SELECT name, price FROM products WHERE stock = 0;"
EX3 = "SELECT status, COUNT(*) FROM orders GROUP BY status;"
EX4_ADDRESS = (
    "UPDATE orders SET address = '9 Pine Street, Tampa' WHERE order_id = 'A101';"
)
EX4_STATUS = "UPDATE change_requests SET status = 'approved' WHERE number = 1;"
ANSWERS = [EX1, EX2, EX3, EX4_ADDRESS, EX4_STATUS]

# Lines the pages give students to type.
A106 = (
    "INSERT INTO orders (order_id, customer, item, status, address) "
    "VALUES ('A106', 'Kai Moreno', 'trail hat', 'processing', '5 Shell Road');"
)
A101_REQUEST = (
    "INSERT INTO change_requests (order_id, new_address) "
    "VALUES ('A101', '9 Pine Street, Tampa');"
)
TOWEL = "INSERT INTO products (name, price, stock) VALUES ('beach towel', 22.00, 15);"
SAMPLE_REQUEST = (
    "INSERT OR IGNORE INTO change_requests (order_id, new_address) "
    "VALUES ('A100', '1 Main Street');"
)

# Every session is typed into `sqlite3 bayside.db` in a new folder that holds
# schema.sql from SCHEMA_REV (and plain_insert.sql, made from it). Each part is (name, typed lines).
SESSIONS = {
    "first_look": [
        ("read", [".read schema.sql", ".tables"]),
        ("schema", [".schema products"]),
        ("rows", ["SELECT * FROM products;"]),
    ],
    "select": [
        ("setup", SETUP),
        ("all", ["SELECT order_id, customer, status FROM orders;"]),
        ("where", ["SELECT order_id, item FROM orders WHERE status = 'shipped';"]),
        ("order", ["SELECT name, price FROM products ORDER BY price DESC;"]),
    ],
    "count": [
        ("setup", SETUP),
        ("count", ["SELECT COUNT(*) FROM products WHERE stock = 0;"]),
        ("group", ["SELECT stock, COUNT(*) FROM products GROUP BY stock;"]),
    ],
    "insert": [
        ("read", [".read schema.sql"]),
        ("display", DISPLAY),
        ("insert", [TOWEL, "SELECT * FROM products WHERE name = 'beach towel';"]),
        ("again", [TOWEL]),
    ],
    "update": [
        ("setup", SETUP),
        (
            "update",
            [
                "UPDATE products SET stock = 20 WHERE name = 'day pack';",
                "SELECT name, stock FROM products;",
            ],
        ),
    ],
    "update_no_where": [
        ("read", [".read schema.sql"]),
        ("display", DISPLAY),
        (
            "update",
            ["UPDATE products SET stock = 0;", "SELECT name, stock FROM products;"],
        ),
    ],
    "read_twice": [
        ("setup", SETUP),
        ("first", ["SELECT COUNT(*) FROM orders;"]),
        (
            "delete",
            [
                "DELETE FROM orders WHERE order_id = 'A105';",
                "SELECT COUNT(*) FROM orders;",
            ],
        ),
        ("again", [".read schema.sql", "SELECT COUNT(*) FROM orders;"]),
    ],
    "requests_twice": [
        ("setup", SETUP),
        (
            "insert",
            [
                SAMPLE_REQUEST,
                SAMPLE_REQUEST,
                "SELECT number, order_id, new_address, status FROM change_requests;",
            ],
        ),
    ],
    # Bayside's schema with every OR IGNORE removed (plain_insert.sql): the counts
    # still match on the second .read, but it prints an error, and Week 14's app
    # would crash on every start after the first.
    "plain_twice": [
        ("first", [".read plain_insert.sql", "SELECT COUNT(*) FROM orders;"]),
        ("again", [".read plain_insert.sql", "SELECT COUNT(*) FROM orders;"]),
    ],
    # One practice database, typed in the order the lab gives it.
    "lab": [
        (
            "practice",
            [
                ".read schema.sql",
                ".tables",
                ".mode column",
                ".headers on",
                "SELECT * FROM orders;",
            ],
        ),
        ("ex1", [EX1]),
        ("ex2", [EX2]),
        ("ex3_given", [A106]),
        ("ex3", [EX3]),
        ("ex4_given", [A101_REQUEST]),
        ("ex4", [EX4_ADDRESS, EX4_STATUS]),
        (
            "ex4_check",
            [
                "SELECT order_id, address FROM orders WHERE order_id = 'A101';",
                "SELECT number, order_id, status FROM change_requests;",
            ],
        ),
    ],
}


def session_lines(name):
    """Every line typed in one session, in order."""
    lines = []
    for _, typed_lines in SESSIONS[name]:
        lines += typed_lines
    return lines


def schema_text():
    """Bayside's schema.sql as the Week 13 pages show it."""
    return read("bayside_app/schema.sql", SCHEMA_REV)


def plain_insert_text():
    """Bayside's schema.sql with every INSERT OR IGNORE turned into a plain INSERT."""
    return schema_text().replace("INSERT OR IGNORE", "INSERT")


def fresh_folder():
    """A new temporary folder holding schema.sql and plain_insert.sql."""
    folder = Path(tempfile.mkdtemp(prefix="ism3232-sql-"))
    (folder / "schema.sql").write_text(schema_text())
    (folder / "plain_insert.sql").write_text(plain_insert_text())
    return folder


def run_session(cli, name):
    """Type one session into sqlite3 now and return what it shows."""
    sys.path.insert(0, str(REF / "tools"))
    from sqlite_cli import transcript

    return transcript(cli, fresh_folder(), session_lines(name))


def run_text(name):
    """A saved transcript from runs/week13/, exactly as captured."""
    return (RUNS / f"{name}.txt").read_text().rstrip("\n")


def split(text, parts):
    """Cut a transcript into parts. Each part starts where its first line was
    typed and ends where the next part's first line was typed."""
    starts, pos = [], 0
    for part, typed_lines in parts:
        pos = text.index("sqlite> " + typed_lines[0], pos)
        starts.append((part, pos))
        pos += 1
    pieces = {}
    for i, (part, start) in enumerate(starts):
        end = starts[i + 1][1] if i + 1 < len(starts) else len(text)
        pieces[part] = text[start:end].rstrip("\n")
    return pieces


def chunk(name, part):
    """One part of a saved session: the typed lines after 'sqlite> ' and their output."""
    return split(run_text(name), SESSIONS[name])[part]


def output_of(name, part):
    """One part of a saved session without the typed lines: only what was printed."""
    lines = chunk(name, part).split("\n")
    return "\n".join(line for line in lines if not line.startswith("sqlite> "))


def typed(name, part):
    """The lines a student types for one part, as a shell block shows them."""
    return "\n".join(dict(SESSIONS[name])[part])


def chunks(name, *parts):
    """Several adjacent parts of one saved session, as one block."""
    return "\n".join(chunk(name, part) for part in parts)
