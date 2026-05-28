# Video 29: OOP III — Design-First & Multi-Class Systems

## YouTube Metadata

**Title:** Python OOP Part 3 — Design-First Multi-Class Systems | ISM3232
**Description:**
The hardest part of OOP is deciding what classes to create before writing any code. In this video we practice design-first OOP — drawing the class diagram, identifying responsibilities, spotting common mistakes, and building a complete multi-class business simulation with tests.

**Chapters:**
0:00 — Design before you type, always
2:00 — The design process: 4 questions
5:00 — Case study: a library checkout system
9:00 — Avoiding the 4 OOP mistakes
13:00 — Building the system
17:00 — Recap

**Applies to:** ISM3232 Module 12

**Tags:** OOP design, python class design, python multi-class, UML class diagram, python design patterns, ISM3232, python object oriented design, software design python, python architecture

---

## Script

### INTRO (0:00–2:00)

The two biggest mistakes beginners make in OOP: they start coding before they've decided what classes they need, and they put too much logic into one class. Both lead to the same outcome — code that works for the first use case and falls apart for the second.

Design-first means: before you open VS Code, you draw the diagram. You answer four questions. Only then do you write `class`. This video teaches that discipline.

---

### THE DESIGN PROCESS (2:00–5:00)

Four questions to answer before writing any class:

**1. What are the entities?** List the nouns in your problem domain. These become candidate classes.

**2. What data does each entity hold?** These become attributes.

**3. What can each entity do?** These become methods. A method should do exactly one thing. If you can't describe a method's purpose in 10 words without "and", it should be two methods.

**4. What are the relationships?** Is-a → inheritance. Has-a → composition. Identify which before writing the class.

---

### CASE STUDY: LIBRARY CHECKOUT SYSTEM (5:00–9:00)

**Step 1 — Entities:**
Reading the problem: "A library tracks books. Members can check out books. Each checkout has a due date. Overdue books incur fines."

Nouns: Library, Book, Member, Checkout. Four classes.

**Step 2 — Data:**
```
Book: isbn, title, author, genre, is_available
Member: member_id, name, email, checkouts (list of Checkout)
Checkout: book, member, checkout_date, due_date, returned_date, fine_amount
Library: books (list of Book), members (list of Member)
```

**Step 3 — Behavior:**
```
Book: check_out(), return_book(), get_info()
Member: checkout_book(book), return_book(book), get_active_checkouts(), get_total_fines()
Checkout: calculate_fine(daily_rate), is_overdue(), mark_returned()
Library: add_book(), register_member(), find_book(isbn), find_member(id), get_overdue_report()
```

**Step 4 — Relationships:**
- Library HAS Books (composition — list of Book instances)
- Library HAS Members (composition — list of Member instances)
- Member HAS Checkouts (composition — list of Checkout instances)
- Checkout HAS a Book reference and a Member reference (composition)
- No inheritance needed — none of these is a specialized version of another

Diagram:
```
Library ──has──► [Book, Book, Book...]
Library ──has──► [Member, Member...]
Member  ──has──► [Checkout, Checkout...]
Checkout──ref──► Book
Checkout──ref──► Member
```

---

### THE 4 OOP MISTAKES (9:00–13:00)

**Mistake 1: God class.** One class that does everything.

```python
# Wrong — Library does too much, knows everything:
class Library:
    def checkout_book(self, member_id, isbn): ...
    def calculate_fine(self, checkout_id): ...
    def send_overdue_email(self, member_id): ...
    def generate_annual_report(self): ...
    def update_catalog(self, isbn, field, value): ...
```

Fix: distribute responsibilities. `Checkout.calculate_fine()`. `Member.get_overdue_checkouts()`. The Library orchestrates, not implements.

**Mistake 2: Anemic model.** Classes that only hold data, with all behavior in separate utility functions.

```python
# Wrong — Book is just a struct, all logic is elsewhere:
class Book:
    def __init__(self, isbn, title, available):
        self.isbn = isbn
        self.title = title
        self.available = available

def check_out_book(book):   # logic lives outside the class
    book.available = False
```

Fix: behavior belongs where the data is. `book.check_out()` modifies `book.available`. Keep data and behavior together.

**Mistake 3: Inheritance when composition is correct.**

```python
# Wrong — CheckoutManager is NOT a kind of Checkout:
class CheckoutManager(Checkout):   # bad inheritance
    ...

# Right — CheckoutManager HAS Checkouts:
class CheckoutManager:
    def __init__(self):
        self.checkouts = []
```

**Mistake 4: Insufficient tests.** Testing only the happy path.

```python
# Wrong — only tests creation:
def test_book():
    b = Book("978-0-13", "Clean Code", "Martin")
    assert b.title == "Clean Code"

# Right — test all 6 types including state changes:
def test_checkout_changes_availability():
    b = Book("978-0-13", "Clean Code", "Martin")
    assert b.is_available == True
    b.check_out()
    assert b.is_available == False
```

---

### BUILDING THE SYSTEM (13:00–17:00)

```python
# book.py
from datetime import date

class Book:
    def __init__(self, isbn: str, title: str, author: str, genre: str = "General"):
        self.isbn         = isbn
        self.title        = title
        self.author       = author
        self.genre        = genre
        self.is_available = True

    def check_out(self) -> None:
        if not self.is_available:
            raise ValueError(f"'{self.title}' is already checked out.")
        self.is_available = False

    def return_book(self) -> None:
        self.is_available = True

    def get_info(self) -> str:
        status = "Available" if self.is_available else "Checked Out"
        return f"{self.title} by {self.author} ({self.genre}) — {status}"

    def __str__(self) -> str:
        return f"Book(isbn={self.isbn!r}, title={self.title!r}, available={self.is_available})"
```

```python
# checkout.py
from datetime import date, timedelta

class Checkout:
    DAILY_FINE_RATE = 0.25   # $0.25 per day overdue

    def __init__(self, book, member, loan_days: int = 14):
        self.book           = book
        self.member         = member
        self.checkout_date  = date.today()
        self.due_date       = date.today() + timedelta(days=loan_days)
        self.returned_date  = None
        self.fine_amount    = 0.0

    def is_overdue(self) -> bool:
        if self.returned_date:
            return self.returned_date > self.due_date
        return date.today() > self.due_date

    def calculate_fine(self) -> float:
        if not self.is_overdue():
            return 0.0
        end = self.returned_date or date.today()
        days_overdue = (end - self.due_date).days
        return round(days_overdue * self.DAILY_FINE_RATE, 2)

    def mark_returned(self) -> None:
        if self.returned_date:
            raise ValueError("Already returned.")
        self.returned_date = date.today()
        self.fine_amount   = self.calculate_fine()
        self.book.return_book()

    def __str__(self) -> str:
        return (f"Checkout(book={self.book.title!r}, "
                f"due={self.due_date}, overdue={self.is_overdue()})")
```

```python
# member.py
from checkout import Checkout

class Member:
    def __init__(self, member_id: int, name: str, email: str):
        self.member_id = member_id
        self.name      = name
        self.email     = email
        self.checkouts = []

    def checkout_book(self, book, loan_days: int = 14) -> Checkout:
        if not book.is_available:
            raise ValueError(f"'{book.title}' is not available.")
        book.check_out()
        co = Checkout(book, self, loan_days)
        self.checkouts.append(co)
        return co

    def get_active_checkouts(self) -> list:
        return [co for co in self.checkouts if co.returned_date is None]

    def get_total_fines(self) -> float:
        return sum(co.calculate_fine() for co in self.checkouts)

    def __str__(self) -> str:
        return f"Member(id={self.member_id}, name={self.name!r}, active={len(self.get_active_checkouts())})"
```

---

### RECAP (17:00–20:00)

- **Design first:** entities → data → behavior → relationships
- Four questions before any class: what, what data, what behavior, what relationships
- Prefer composition over inheritance; use inheritance only for genuine is-a
- Mistake 1: God class — distribute responsibility
- Mistake 2: Anemic model — keep behavior with data
- Mistake 3: wrong relationship type — is-a vs has-a
- Mistake 4: insufficient tests — test state changes, not just creation
- One responsibility per method; if you need "and," split it

Module 13: capstone design and SQL foundations — from OOP objects to database tables.
