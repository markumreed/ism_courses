# Video 27: OOP I — Classes, __init__ & Instance Methods

## YouTube Metadata

**Title:** Python OOP Part 1 — Classes, __init__ & Instance Methods | ISM3232
**Description:**
Object-Oriented Programming organizes code around objects — bundles of data and behavior that model real business entities. In this video we build a complete BusinessRequest class with __init__, instance attributes, business logic methods, and a full pytest test suite — the ISM3232 Module 10 standard.

**Chapters:**
0:00 — The mental model: blueprint and instance
2:00 — Defining a class
4:00 — __init__ — the constructor
7:00 — Instance methods
10:30 — Instance independence
13:00 — The __str__ method
14:30 — Complete test suite
17:30 — Recap

**Applies to:** ISM3232 Module 10

**Tags:** python OOP, python classes, python __init__, python instance methods, python object oriented, ISM3232, python class tutorial, python objects, python business class, OOP beginners

---

## Script

### INTRO (0:00–2:00)

Everything we've written so far has been procedural — functions that take inputs and return outputs, organized in files. Object-Oriented Programming is a different way of organizing code: instead of functions that work on data, you create **objects** that are data and behavior bundled together.

Think of a class as a blueprint — a template that defines what every object of that type will look like. An instance is one actual object built from that blueprint. A car blueprint defines that every car has a make, model, and speed, and can accelerate, brake, and honk. A specific 2024 Toyota Camry is one instance of that blueprint.

In ISM3232, we build business classes — `BusinessRequest`, `Customer`, `Product`, `Order`. Each models a real entity in a business system.

---

### DEFINING A CLASS (2:00–4:00)

```python
class BusinessRequest:
    pass   # empty class — valid Python
```

Create an instance:
```python
req = BusinessRequest()
print(type(req))   # <class '__main__.BusinessRequest'>
```

The class is the blueprint. `req` is one instance of it. `BusinessRequest()` calls the class to create an instance — similar to calling a function.

Convention: class names use **PascalCase** — each word capitalized, no underscores. `BusinessRequest`, not `business_request` or `businessrequest`.

---

### __init__ — THE CONSTRUCTOR (4:00–7:00)

`__init__` is a special method (called a **dunder** — double underscore — method) that runs automatically when you create an instance. It's where you set up the object's initial state.

```python
class BusinessRequest:
    def __init__(self, title: str, requester: str, priority: str = "normal"):
        self.title     = title
        self.requester = requester
        self.priority  = priority
        self.status    = "pending"      # always starts pending
        self.approved  = False          # always starts unapproved
        self.comments  = []             # always starts empty
```

`self` is the instance — the specific object being created. `self.title = title` stores the `title` argument as an attribute of this instance.

Create instances:

```python
req1 = BusinessRequest("New Laptop", "Alice Kim", "high")
req2 = BusinessRequest("Office Chair", "Bob Patel")   # uses default priority

print(req1.title)     # New Laptop
print(req1.status)    # pending
print(req2.priority)  # normal
```

Each instance has its own independent copy of every attribute.

---

### INSTANCE METHODS (7:00–10:30)

Instance methods define what an object can **do**. They always take `self` as the first parameter.

```python
class BusinessRequest:
    def __init__(self, title: str, requester: str, priority: str = "normal"):
        self.title     = title
        self.requester = requester
        self.priority  = priority
        self.status    = "pending"
        self.approved  = False
        self.comments  = []

    def approve(self, approver: str) -> None:
        """Approve the request."""
        self.approved  = True
        self.status    = "approved"
        self.comments.append(f"Approved by {approver}.")

    def reject(self, reason: str) -> None:
        """Reject the request with a reason."""
        self.approved  = False
        self.status    = "rejected"
        self.comments.append(f"Rejected: {reason}")

    def add_comment(self, comment: str) -> None:
        """Add a comment to the request."""
        self.comments.append(comment)

    def get_summary(self) -> str:
        """Return a one-line summary of the request."""
        return f"[{self.status.upper()}] {self.title} (by {self.requester}, {self.priority} priority)"

    def is_high_priority(self) -> bool:
        """Return True if this is a high priority request."""
        return self.priority == "high"
```

Using the methods:

```python
req = BusinessRequest("New Laptop", "Alice Kim", "high")
print(req.get_summary())     # [PENDING] New Laptop (by Alice Kim, high priority)

req.add_comment("Needed for project deadline May 31.")
req.approve("Manager Lee")
print(req.get_summary())     # [APPROVED] New Laptop (by Alice Kim, high priority)
print(req.comments)          # ['Needed for project deadline May 31.', 'Approved by Manager Lee.']
print(req.approved)          # True
```

---

### INSTANCE INDEPENDENCE (10:30–13:00)

This is the most important demo in OOP. Two instances of the same class are completely independent.

```python
req1 = BusinessRequest("New Laptop", "Alice Kim", "high")
req2 = BusinessRequest("Office Chair", "Bob Patel", "normal")

req1.approve("Manager Lee")

print(req1.status)   # approved — req1 was approved
print(req2.status)   # pending  — req2 is unaffected

req2.reject("Budget frozen this quarter.")
print(req2.status)   # rejected
print(req1.status)   # approved — still approved, unaffected by req2's rejection
```

Each instance has its own memory space for its attributes. Modifying one instance never affects another.

---

### __str__ METHOD (13:00–14:30)

`__str__` controls what `print(object)` shows. Without it, you get something like `<__main__.BusinessRequest object at 0x102a3f6b0>`.

```python
def __str__(self) -> str:
    return (
        f"BusinessRequest(\n"
        f"  title={self.title!r},\n"
        f"  requester={self.requester!r},\n"
        f"  priority={self.priority!r},\n"
        f"  status={self.status!r},\n"
        f"  approved={self.approved}\n"
        f")"
    )
```

Now:
```python
req = BusinessRequest("New Laptop", "Alice Kim", "high")
print(req)
```

Output:
```
BusinessRequest(
  title='New Laptop',
  requester='Alice Kim',
  priority='high',
  status='pending',
  approved=False
)
```

Always implement `__str__` for your business classes — it makes debugging dramatically easier.

---

### COMPLETE TEST SUITE (14:30–17:30)

```python
# tests/test_business_request.py
import pytest
from business_request import BusinessRequest

# 1. Happy path
def test_create_request_basic():
    req = BusinessRequest("New Laptop", "Alice Kim", "high")
    assert req.title     == "New Laptop"
    assert req.requester == "Alice Kim"
    assert req.priority  == "high"
    assert req.status    == "pending"
    assert req.approved  == False

# 2. Default parameter
def test_default_priority():
    req = BusinessRequest("Chair", "Bob Patel")
    assert req.priority == "normal"

# 3. Instance independence
def test_instance_independence():
    req1 = BusinessRequest("Laptop", "Alice", "high")
    req2 = BusinessRequest("Chair",  "Bob",   "normal")
    req1.approve("Manager Lee")
    assert req1.status == "approved"
    assert req2.status == "pending"   # unaffected

# 4. Approve method
def test_approve():
    req = BusinessRequest("Laptop", "Alice", "high")
    req.approve("Manager Lee")
    assert req.approved == True
    assert req.status   == "approved"
    assert any("Approved by Manager Lee" in c for c in req.comments)

# 5. Reject method
def test_reject():
    req = BusinessRequest("Laptop", "Alice", "high")
    req.reject("Over budget.")
    assert req.approved == False
    assert req.status   == "rejected"

# 6. Return types
def test_return_types():
    req = BusinessRequest("Laptop", "Alice", "high")
    assert isinstance(req.get_summary(),      str)
    assert isinstance(req.is_high_priority(), bool)
    assert isinstance(req.comments,           list)
```

Run:
```bash
pytest -v
```

All 6 tests pass — you have a correct, tested business class.

---

### RECAP (17:30–20:00)

- `class Name:` — define a class (blueprint)
- `__init__(self, ...)` — constructor, runs on instantiation, sets up attributes
- `self.attribute = value` — store data on the instance
- Instance methods take `self` as first parameter, operate on `self.*` attributes
- `instance.method()` — call a method on a specific object
- Two instances are independent — modifying one never affects another
- `__str__` — controls `print(object)` output; always implement it
- Write tests for every method: happy path, default, independence, behavior, edge, types

Module 11: composition and inheritance — building systems of objects that work together.
