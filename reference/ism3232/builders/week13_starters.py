"""The capstone starters page's data: the eight-item checklist, the
PROPOSAL.md template, and the six starter businesses. Names and notes are
HTML (the page shows them as they are)."""

import re

CHECKLIST = [
    "One business. The chat serves customers or staff; the Staff tab always serves staff.",
    "At least two business tables plus a <code>change_requests</code> table.",
    "At least two lookup tools. They only read, and they check their arguments.",
    (
        "At least one change tool. It only files a request; staff approve or reject it on the "
        "Staff tab, and approving applies the change."
    ),
    (
        "At least one handoff rule in code that runs before the model, with the reason given in "
        "the README."
    ),
    "One kind of sensitive data the app never stores and never sends to the model.",
    (
        "Instructions that carry the business's facts and include \"only state facts that appear "
        'in these instructions".'
    ),
    "Five sample conversations, which become the Week 16 evaluation cases.",
]

TEMPLATE = """# Capstone Proposal: <business name>
Author: <your name>

## The business                    (2-3 sentences: who it serves, what goes wrong today)
## Who uses it                     (the chat: customers or staff; the Staff tab: staff)
## Tables                          -> Week 13 schema.sql
<table>: <column> <TYPE>, ...       (one example row each; include change_requests)
## Lookup tools (at least two)     -> Week 14 tools.py
<name>(<arguments>): what it reads. Example question: "..."
## Change tool (at least one)      -> Week 14 tools.py, Week 15 Staff tab
<name>(<arguments>): what staff approve, and what approving changes
## Handoff rule                    -> Week 14 agent.py (HANDOFF_WORDS)
Words: ...   Why a person must handle these: ...
## Data it never stores            (and never sends to the model)
## Instructions draft              -> Week 14 settings.py
The facts the model may state, ending with:
"Only state facts that appear in these instructions or in tool results."
## Five sample conversations       -> Week 16 evaluation.py CASES
1. Customer: "..."   Must: use <tool> / hand off / say "..." / never say "..." / file <n> change(s)
## Out of scope (at least two)
## Checklist                       (the eight items, ticked before sign-off)"""


def headings(text):
    """The '## ' heading names, without the guidance after two or more spaces."""
    return [
        re.split(r"\s{2,}", line[3:])[0]
        for line in text.split("\n")
        if line.startswith("## ")
    ]


STARTERS = [
    {
        "name": "Spokewell Bike Repair",
        "pitch": "A neighborhood bike shop. Customers ask whether a repair is done, whether "
        "a part is in stock, and whether they can pick their bike up on a different day.",
        "chat": "customers",
        "tables": [
            {
                "name": "repairs",
                "columns": [
                    ("ticket_id", "TEXT PRIMARY KEY"),
                    ("customer", "TEXT"),
                    ("bike", "TEXT"),
                    ("status", "TEXT"),
                    ("pickup_date", "TEXT"),
                ],
                "rows": [
                    ("R200", "Jordan Lee", "road bike", "in repair", "2026-11-20"),
                    ("R201", "Priya Nair", "kids bike", "ready", "2026-11-18"),
                ],
                "note": "Statuses: waiting for parts, in repair, ready.",
            },
            {
                "name": "parts",
                "columns": [
                    ("name", "TEXT PRIMARY KEY"),
                    ("price", "REAL"),
                    ("stock", "INTEGER"),
                ],
                "rows": [("inner tube", 8.00, 25), ("brake pads", 15.00, 0)],
                "note": "",
            },
        ],
        "lookups": [
            ("look_up_repair", ["ticket_id"], "repairs", "Is my repair R200 ready?"),
            ("check_part", ["name"], "parts", "Do you have brake pads in stock?"),
        ],
        "change": (
            "request_pickup_change",
            ["ticket_id", "new_date"],
            "repairs",
            "pickup_date",
            "Can I pick up R200 on 2026-11-22 instead?",
        ),
        "change_value": None,
        "handoff": ["payment", "card"],
        "never_stored": "card numbers",
    },
    {
        "name": "Wagtail Grooming",
        "pitch": "A dog grooming salon. Owners ask when an appointment is, what a service "
        "costs and how long it takes, and whether they can move to another time.",
        "chat": "customers",
        "tables": [
            {
                "name": "appointments",
                "columns": [
                    ("appt_id", "TEXT PRIMARY KEY"),
                    ("pet_name", "TEXT"),
                    ("owner", "TEXT"),
                    ("service", "TEXT"),
                    ("time", "TEXT"),
                    ("status", "TEXT"),
                ],
                "rows": [
                    (
                        "G300",
                        "Biscuit",
                        "Ana Lopez",
                        "bath and brush",
                        "Friday 10:00 am",
                        "booked",
                    ),
                    (
                        "G301",
                        "Pepper",
                        "Tom Reyes",
                        "nail trim",
                        "Saturday 2:00 pm",
                        "booked",
                    ),
                ],
                "note": "Statuses: booked, done, cancelled.",
            },
            {
                "name": "services",
                "columns": [
                    ("name", "TEXT PRIMARY KEY"),
                    ("price", "REAL"),
                    ("minutes", "INTEGER"),
                ],
                "rows": [("bath and brush", 45.00, 60), ("nail trim", 15.00, 15)],
                "note": "",
            },
        ],
        "lookups": [
            (
                "look_up_appointment",
                ["appt_id"],
                "appointments",
                "When is appointment G300?",
            ),
            ("check_service", ["name"], "services", "How much is a nail trim?"),
        ],
        "change": (
            "request_reschedule",
            ["appt_id", "new_time"],
            "appointments",
            "time",
            "Can you move G301 to Sunday 11:00 am?",
        ),
        "change_value": None,
        "handoff": ["vet", "sick", "injured"],
        "never_stored": "pet medical history",
    },
    {
        "name": "Crestview Campus Bookstore",
        "pitch": "A campus bookstore that holds textbook orders for pickup. Students ask "
        "whether an order is ready, which books a course needs, and to cancel an order.",
        "chat": "customers",
        "tables": [
            {
                "name": "orders",
                "columns": [
                    ("order_id", "TEXT PRIMARY KEY"),
                    ("student", "TEXT"),
                    ("title", "TEXT"),
                    ("status", "TEXT"),
                    ("pickup_desk", "TEXT"),
                ],
                "rows": [
                    (
                        "B400",
                        "Mia Park",
                        "Intro to Accounting",
                        "ready for pickup",
                        "North desk",
                    ),
                    (
                        "B401",
                        "Leo Grant",
                        "Business Statistics",
                        "ordered",
                        "South desk",
                    ),
                ],
                "note": "Statuses: ordered, ready for pickup, picked up, cancelled.",
            },
            {
                "name": "textbooks",
                "columns": [
                    ("title", "TEXT PRIMARY KEY"),
                    ("course", "TEXT"),
                    ("price", "REAL"),
                    ("stock", "INTEGER"),
                ],
                "rows": [
                    ("Intro to Accounting", "ACG2021", 120.00, 4),
                    ("Business Statistics", "QMB3200", 95.00, 0),
                ],
                "note": "",
            },
        ],
        "lookups": [
            ("look_up_order", ["order_id"], "orders", "Is my order B400 ready?"),
            (
                "find_textbooks",
                ["course"],
                "textbooks",
                "Which textbooks do I need for ACG2021?",
            ),
        ],
        "change": (
            "request_cancellation",
            ["order_id"],
            "orders",
            "status",
            "Please cancel my order B401.",
        ),
        "change_value": "cancelled",
        "handoff": ["financial aid", "payment"],
        "never_stored": "student ID numbers",
    },
    {
        "name": "Northline Fitness Studio",
        "pitch": "A small fitness studio with a weekly class schedule. Members ask what is "
        "on a given day, whether their booking stands, and to move to a different class.",
        "chat": "customers",
        "tables": [
            {
                "name": "classes",
                "columns": [
                    ("class_id", "TEXT PRIMARY KEY"),
                    ("name", "TEXT"),
                    ("day", "TEXT"),
                    ("time", "TEXT"),
                    ("spots_left", "INTEGER"),
                ],
                "rows": [
                    ("C10", "Spin", "Monday", "6:00 pm", 4),
                    ("C11", "Yoga", "Wednesday", "7:00 am", 0),
                ],
                "note": "",
            },
            {
                "name": "bookings",
                "columns": [
                    ("booking_id", "TEXT PRIMARY KEY"),
                    ("member", "TEXT"),
                    ("class_id", "TEXT"),
                    ("status", "TEXT"),
                ],
                "rows": [
                    ("K500", "Sam Ortiz", "C10", "booked"),
                    ("K501", "Ava Kim", "C11", "booked"),
                ],
                "note": "Statuses: booked, cancelled.",
            },
        ],
        "lookups": [
            ("classes_on", ["day"], "classes", "Which classes are on Monday?"),
            (
                "look_up_booking",
                ["booking_id"],
                "bookings",
                "Am I booked? My booking is K501.",
            ),
        ],
        "change": (
            "request_booking_move",
            ["booking_id", "new_class_id"],
            "bookings",
            "class_id",
            "Can you move booking K501 to class C10?",
        ),
        "change_value": None,
        "handoff": ["injury", "pain", "medical"],
        "never_stored": "health information",
    },
    {
        "name": "Marlow &amp; Co. IT Help Desk",
        "pitch": "The IT help desk inside a small company. Employees use the chat to check a "
        "ticket, find out who has a device, and ask for a ticket's priority to change; "
        "help-desk staff approve on the Staff tab.",
        "chat": "staff",
        "tables": [
            {
                "name": "tickets",
                "columns": [
                    ("ticket_id", "TEXT PRIMARY KEY"),
                    ("employee", "TEXT"),
                    ("issue", "TEXT"),
                    ("status", "TEXT"),
                    ("priority", "TEXT"),
                ],
                "rows": [
                    ("T600", "Rosa Diaz", "laptop will not start", "open", "normal"),
                    ("T601", "Ken Wu", "printer jam", "in progress", "low"),
                ],
                "note": "Statuses: open, in progress, closed. Priorities: low, normal, high.",
            },
            {
                "name": "devices",
                "columns": [
                    ("asset_tag", "TEXT PRIMARY KEY"),
                    ("model", "TEXT"),
                    ("assigned_to", "TEXT"),
                ],
                "rows": [
                    ("L-1042", "ThinkPad T14", "Rosa Diaz"),
                    ("P-0007", "LaserJet 4000", "Front office"),
                ],
                "note": "",
            },
        ],
        "lookups": [
            (
                "look_up_ticket",
                ["ticket_id"],
                "tickets",
                "What is happening with ticket T600?",
            ),
            ("who_has_device", ["asset_tag"], "devices", "Who has laptop L-1042?"),
        ],
        "change": (
            "request_priority_change",
            ["ticket_id", "new_priority"],
            "tickets",
            "priority",
            "Please raise ticket T601 to high priority.",
        ),
        "change_value": None,
        "handoff": ["password"],
        "never_stored": "passwords",
    },
    {
        "name": "Elm Court Apartments Maintenance",
        "pitch": "The maintenance office of an apartment complex. Tenants ask when a repair "
        "is scheduled, what is open for their unit, and when maintenance may come in.",
        "chat": "customers",
        "tables": [
            {
                "name": "work_orders",
                "columns": [
                    ("work_order_id", "TEXT PRIMARY KEY"),
                    ("unit", "TEXT"),
                    ("issue", "TEXT"),
                    ("status", "TEXT"),
                    ("entry_time", "TEXT"),
                ],
                "rows": [
                    ("W700", "2B", "leaking faucet", "scheduled", "Tuesday 9:00 am"),
                    ("W701", "4A", "broken blinds", "reported", "not set"),
                ],
                "note": "Statuses: reported, scheduled, fixed. The table is called work_orders "
                "so that &ldquo;request&rdquo; only ever means a change waiting for staff.",
            },
            {
                "name": "units",
                "columns": [
                    ("unit", "TEXT PRIMARY KEY"),
                    ("tenant", "TEXT"),
                    ("building", "TEXT"),
                ],
                "rows": [("2B", "Lena Ford", "North"), ("4A", "Omar Haddad", "South")],
                "note": "",
            },
        ],
        "lookups": [
            (
                "look_up_work_order",
                ["work_order_id"],
                "work_orders",
                "When is someone coming for W700?",
            ),
            (
                "open_work_orders",
                ["unit"],
                "work_orders",
                "What repairs are open for unit 2B?",
            ),
        ],
        "change": (
            "request_entry_time",
            ["work_order_id", "new_time"],
            "work_orders",
            "entry_time",
            "Can maintenance come for W701 on Thursday 10:00 am?",
        ),
        "change_value": None,
        "handoff": ["gas", "fire", "flood", "smoke"],
        "never_stored": "door and lock codes",
    },
]
