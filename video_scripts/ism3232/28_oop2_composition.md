# Video 28: OOP II — Composition & Inheritance

## YouTube Metadata

**Title:** Python OOP Part 2 — Composition & Inheritance for Business Systems | ISM3232
**Description:**
Real business systems have objects that contain other objects (composition) and objects that are specialized versions of other objects (inheritance). In this video we build a RequestManager that holds BusinessRequest objects (has-a composition), add a UrgentRequest subclass (is-a inheritance), and map the design to SQL tables.

**Chapters:**
0:00 — Composition vs inheritance — choosing correctly
2:00 — Composition: RequestManager has BusinessRequests
6:30 — Filtering and querying the manager
9:30 — Inheritance: UrgentRequest is a BusinessRequest
13:00 — super() — calling parent methods
15:00 — OOP to SQL mapping
17:00 — Recap

**Applies to:** ISM3232 Module 11

**Tags:** python composition, python inheritance, python OOP, python has-a, python is-a, python super, OOP design patterns, ISM3232, python class hierarchy, python business system

---

## Script

### INTRO (0:00–2:00)

In Module 10 we built a single class. In the real world, objects don't exist in isolation — a manager holds a list of requests. An urgent request is a specialized kind of request. A product belongs to a category.

These relationships are **composition** (has-a) and **inheritance** (is-a). Knowing when to use each is one of the most important design decisions in OOP. The rule of thumb: prefer composition. Use inheritance only for genuine is-a relationships. Let's see both in action.

---

### COMPOSITION: RequestManager has BusinessRequests (2:00–6:30)

Composition means one class holds instances of another class as attributes.

```python
# request_manager.py
from business_request import BusinessRequest

class RequestManager:
    """Manages a collection of BusinessRequest objects."""

    def __init__(self, department: str):
        self.department = department
        self.requests   = []       # list of BusinessRequest instances

    def add_request(self, request: BusinessRequest) -> None:
        """Add a BusinessRequest to the collection."""
        if not isinstance(request, BusinessRequest):
            raise TypeError("Only BusinessRequest objects can be added.")
        self.requests.append(request)

    def get_pending(self) -> list:
        """Return all requests with status 'pending'."""
        return [r for r in self.requests if r.status == "pending"]

    def get_approved(self) -> list:
        """Return all approved requests."""
        return [r for r in self.requests if r.approved]

    def get_by_priority(self, priority: str) -> list:
        """Return all requests matching the given priority."""
        return [r for r in self.requests if r.priority == priority]

    def approve_all_high_priority(self, approver: str) -> int:
        """Approve all high-priority pending requests. Returns count approved."""
        count = 0
        for req in self.requests:
            if req.priority == "high" and req.status == "pending":
                req.approve(approver)
                count += 1
        return count

    def summary_report(self) -> str:
        """Return a formatted summary of all requests."""
        total    = len(self.requests)
        approved = len(self.get_approved())
        pending  = len(self.get_pending())
        rejected = total - approved - pending
        return (
            f"Department: {self.department}\n"
            f"Total requests: {total}\n"
            f"  Approved: {approved}\n"
            f"  Pending:  {pending}\n"
            f"  Rejected: {rejected}\n"
        )

    def __len__(self) -> int:
        return len(self.requests)

    def __str__(self) -> str:
        return f"RequestManager(department={self.department!r}, requests={len(self)})"
```

Using the manager:

```python
from business_request import BusinessRequest
from request_manager import RequestManager

mgr = RequestManager("IT Department")

mgr.add_request(BusinessRequest("New Laptop",  "Alice Kim",  "high"))
mgr.add_request(BusinessRequest("USB Hub",     "Bob Patel",  "normal"))
mgr.add_request(BusinessRequest("Monitor",     "Carol White","high"))
mgr.add_request(BusinessRequest("Desk Chair",  "Dave Brown", "normal"))

print(f"Total requests: {len(mgr)}")
approved_count = mgr.approve_all_high_priority("Manager Lee")
print(f"Auto-approved {approved_count} high-priority requests.")
print(mgr.summary_report())
```

Output:
```
Total requests: 4
Auto-approved 2 high-priority requests.
Department: IT Department
Total requests: 4
  Approved: 2
  Pending:  2
  Rejected: 0
```

The manager **has** requests. It doesn't inherit from `BusinessRequest` — it contains them. This is the has-a relationship.

---

### FILTERING AND QUERYING (6:30–9:30)

The manager's methods act like database queries — filter, sort, count.

```python
# Get all pending requests:
for req in mgr.get_pending():
    print(req.get_summary())

# Get high priority requests:
high = mgr.get_by_priority("high")
print(f"High priority requests: {len(high)}")

# Get approved requests sorted by title:
approved = sorted(mgr.get_approved(), key=lambda r: r.title)
for req in approved:
    print(f"  {req.title} — {req.requester}")
```

The manager is the interface. External code never touches `mgr.requests` directly — it uses the manager's methods. This is **encapsulation** — the manager controls access to its data.

---

### INHERITANCE: UrgentRequest is-a BusinessRequest (9:30–13:00)

Inheritance means a subclass extends a parent class. The subclass **is** a type of the parent — it has everything the parent has, plus additional behavior.

```python
# urgent_request.py
from business_request import BusinessRequest

class UrgentRequest(BusinessRequest):
    """A BusinessRequest with escalation and deadline tracking."""

    SLA_HOURS = 4   # class variable — shared by all UrgentRequest instances

    def __init__(self, title: str, requester: str, deadline: str, escalation_contact: str):
        super().__init__(title, requester, priority="high")   # always high priority
        self.deadline           = deadline
        self.escalation_contact = escalation_contact
        self.escalated          = False

    def escalate(self) -> None:
        """Escalate this request to the escalation contact."""
        self.escalated = True
        self.comments.append(f"Escalated to {self.escalation_contact}.")
        self.add_comment(f"SLA: {self.SLA_HOURS}h — deadline {self.deadline}")

    def get_summary(self) -> str:
        """Override parent's summary to include deadline."""
        base    = super().get_summary()   # get parent's summary
        urgency = " [ESCALATED]" if self.escalated else ""
        return f"🚨 URGENT{urgency} — {base} — due {self.deadline}"
```

`super().__init__(...)` calls the parent class's `__init__`. Without it, the parent's setup code doesn't run and the inherited attributes won't exist.

`super().get_summary()` calls the parent's method — you get the base behavior and can extend it.

```python
from urgent_request import UrgentRequest

urgent = UrgentRequest("Server Down", "IT Team", "2024-05-28 17:00", "CTO Office")
print(urgent.title)      # Server Down — inherited attribute
print(urgent.priority)   # high — set by __init__ calling super().__init__
print(urgent.status)     # pending — inherited attribute

urgent.escalate()
print(urgent.get_summary())
# 🚨 URGENT [ESCALATED] — [PENDING] Server Down (by IT Team, high priority) — due 2024-05-28 17:00
```

`isinstance()` correctly identifies the inheritance chain:
```python
print(isinstance(urgent, UrgentRequest))    # True
print(isinstance(urgent, BusinessRequest))  # True — because UrgentRequest IS a BusinessRequest
```

---

### OOP TO SQL MAPPING (15:00–17:00)

Every class maps to a database table. Every attribute maps to a column.

```python
"""
BusinessRequest → business_requests table:
  id            INTEGER PRIMARY KEY AUTOINCREMENT
  title         TEXT NOT NULL
  requester     TEXT NOT NULL
  priority      TEXT DEFAULT 'normal'
  status        TEXT DEFAULT 'pending'
  approved      INTEGER DEFAULT 0   (SQLite stores booleans as 0/1)
  created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP

UrgentRequest → urgent_requests table (extends business_requests):
  id            INTEGER PRIMARY KEY AUTOINCREMENT
  request_id    INTEGER REFERENCES business_requests(id)
  deadline      TEXT NOT NULL
  escalation_contact TEXT NOT NULL
  escalated     INTEGER DEFAULT 0
  sla_hours     INTEGER DEFAULT 4

RequestManager → (no separate table — it's a query interface, not data)
"""
```

The manager class doesn't map to a table because it's not data — it's behavior. It becomes your database query layer.

---

### RECAP (17:00–20:00)

- **Composition (has-a):** one class holds instances of another — use for "collections" and "ownership"
- **Inheritance (is-a):** subclass extends parent — use only for genuine type hierarchy
- Prefer composition — most relationships are has-a, not is-a
- `class Child(Parent):` — inherit from parent
- `super().__init__(...)` — call parent's constructor first
- `super().method()` — call parent's version of an overridden method
- Subclass instances pass `isinstance(obj, ParentClass)` — they ARE the parent type
- Every class → one database table; every attribute → one column; manager class → query interface

Module 12: OOP III — design-first, multi-class systems, and applied practice.
