# ISM3232 Lab 10 Code-Along — OOP for Agents

**Build a support chatbot class, give it a separate order-lookup tool, test it, then design a small assistant of your own.**

Type along. Every file below is complete and was run as written. Each output block is a real run, and the final folder passes `ruff format . && ruff check . && pytest -v` with 15 tests.

| | |
|---|---|
| **Folder** | `~/ism3232/module06_agents` (Weeks 10, 11 and 12 all build here) |
| **Time** | About 75 minutes in class, plus about 2 hours for the mini-project |
| **You need** | Python 3.12, your `~/ism3232` repo, pytest and ruff. No AI model, no API key, no internet |
| **You submit** | Your GitHub repo URL in Canvas. The commit message must include `lab 10` |

### Contents

0. [Seven words before you type](#0-seven-words-before-you-type)
1. [Set up the project](#part-1--set-up-the-project)
2. [Write the tool](#part-2--write-the-tool-order_toolpy)
3. [Write the chatbot](#part-3--write-the-chatbot-chatbotpy)
4. [Run it and test it](#part-4--run-it-and-test-it)
5. [Four exercises](#part-5--four-exercises)
6. [Mini-project](#part-6--mini-project-an-assistant-of-your-own)
7. [Ritual and push](#part-7--ritual-push-and-submit)
8. [When something breaks](#when-something-breaks)

### What your folder looks like at the end

```text
module06_agents/
├── .gitignore
├── requirements.txt
├── order_tool.py          ← Part 2: the order tool
├── chatbot.py             ← Part 3: the chatbot (Exercises 2 and 3 add to it)
├── main.py                ← Part 4: runs a conversation
├── stock_tool.py          ← Exercise 3: a second tool
├── exercise1.md           ← Exercise 1
├── two_bots.py            ← Exercise 4
├── my_tool.py             ← Mini-project (your own business)
├── my_assistant.py        ← Mini-project
├── my_main.py             ← Mini-project
├── README.md              ← Mini-project write-up section
└── tests/
    ├── __init__.py
    ├── test_chatbot.py    ← 8 tests, then 10 after the exercises
    └── test_my_assistant.py
```

> **This chatbot is a mock.** It picks replies with `if` statements that look for keywords. There is no AI in this lab. A real model comes in Week 11, and it replaces exactly one method you write today.
>
> **No AI-generated classes.** You must be able to explain every line. If you use AI for any part of a class, paste its output and add a comment explaining each line.

---

## 0. Seven words before you type

*From the reading.* You will use each of these words in the next hour.

| Word | Plain meaning | In this lab |
|---|---|---|
| **class** | A template you write once | `SupportChatbot`, `OrderLookup` |
| **object** | One thing made from the template | `bot`, `order_tool` |
| **attribute** | Data one object remembers | `self.name`, `self.history` |
| **method** | A function that belongs to a class | `respond()`, `find_status()` |
| **`__init__`** | Runs once, by itself, when an object is created | Sets the starting attributes |
| **`self`** | The object the method is working on right now | In `bot.respond(...)`, `self` is `bot` |
| **composition** | Giving one object another object to use | The chatbot *has a* tool |

Two ideas to keep in mind:

- **A class organizes code. It does not make anything intelligent.** Wrapping `if` statements in a class makes them easier to read, extend and test. It does not make the replies any smarter.
- **Two classes, two jobs.** The tool knows orders and nothing about chatting. The chatbot holds the conversation and asks the tool when it needs an order. You can test each one on its own and swap either one out.

---

## Part 1 — Set up the project

Open a terminal and run these one line at a time.

```bash
cd ~/ism3232
mv module06_oop module06_agents
cd module06_agents
python3 -m venv .venv && source .venv/bin/activate
pip install pytest ruff && pip freeze > requirements.txt
echo '.venv/' > .gitignore && echo '__pycache__/' >> .gitignore
touch order_tool.py chatbot.py main.py
mkdir -p tests && touch tests/__init__.py tests/test_chatbot.py
code .
```

What each line does:

- `mv module06_oop module06_agents` renames the empty folder you made in Week 1. **No `module06_oop`?** If `mv` says *No such file or directory*, run `mkdir module06_agents` instead and carry on.
- The `venv` line creates and activates this folder's own Python environment. Your prompt now starts with `(.venv)`.
- `pip freeze > requirements.txt` records the packages so a grader can recreate your setup.
- `.gitignore` keeps the environment and Python's cache files out of Git.
- `touch` creates the empty files you fill in next.

**✅ Checkpoint:** `ls` shows `chatbot.py main.py order_tool.py requirements.txt tests`, and your prompt shows `(.venv)`.

---

## Part 2 — Write the tool (`order_tool.py`)

Start with the tool, because it is the simpler class and the chatbot depends on it. Its whole job is answering questions about orders.

```python
# order_tool.py
# Author: [Your Name]


class OrderLookup:
    """A tool that knows about orders. It knows nothing about chatting."""

    def __init__(self, orders):
        """Store the orders this tool can look up."""
        self.orders = orders

    def find_order_id(self, text):
        """Return the first known order ID mentioned in text, or None."""
        for order_id in self.orders:
            if order_id in text.upper():
                return order_id
        return None

    def find_status(self, order_id):
        """Return the status of one order, or None if there is no such order."""
        if order_id in self.orders:
            return self.orders[order_id]
        return None
```

Read it line by line:

- `class OrderLookup:` starts the template. A class name capitalizes each word and has no underscores.
- `def __init__(self, orders):` You never call this by name. Python runs it when you write `OrderLookup({...})`, and it fills in `self` with the new object.
- `self.orders = orders` The right side is a parameter, which disappears when `__init__` ends. The left side is an attribute, which stays on the object.
- `find_order_id` loops over the order IDs it knows, the same dictionary loop as Week 6. `text.upper()` lets `a100` match `A100`.
- **`None` is the tool's way of saying it has no answer.** Both lookup methods return `None` rather than crashing or guessing. Later, the chatbot checks for `None` and says something sensible.

**✅ Checkpoint:** try the tool in the Python shell before going on.

```pycon
$ python3
>>> from order_tool import OrderLookup
>>> tool = OrderLookup({"A100": "shipped"})
>>> tool.find_order_id("where is a100?")
'A100'
>>> tool.find_status("A100")
'shipped'
>>> tool.find_status("A999")
>>> exit()
```

The last call prints nothing. It returned `None`, and the shell doesn't display `None`.

---

## Part 3 — Write the chatbot (`chatbot.py`)

Build it in five chunks, following the lecture's steps. Type each chunk under the previous one. The full file is at the end of this part.

### 3a. A constant and the setup method: a class that stores data

```python
# chatbot.py
# Author: [Your Name]

HANDOFF_WORDS = ["address", "payment", "card"]


class SupportChatbot:
    """A mock support chatbot. Its replies come from simple rules, not from AI."""

    def __init__(self, name, instructions, order_tool):
        """Set up one chatbot with its own name, instructions, tool, and history."""
        self.name = name
        self.instructions = instructions
        self.order_tool = order_tool
        self.history = []
```

- `HANDOFF_WORDS` lists the request types a person must handle: changing a shipping address, and anything about payment or cards.
- `self.order_tool = order_tool` **is composition, the whole idea of the week.** The chatbot doesn't create its own tool. It is handed one. That is why a test can later give it a tiny tool with made-up data.
- `self.history = []` isn't a parameter, because every conversation starts empty. It **must** be inside `__init__`. See the "list in the wrong place" bug in [When something breaks](#when-something-breaks).
- `self.instructions` is stored but nothing reads it yet. In Week 11 these instructions are sent to a real model.

### 3b. `respond`: the shape every chatbot keeps

```python
    def respond(self, user_message):
        """Record the user's message, choose a reply, record it, and return it."""
        self.history.append({"role": "user", "content": user_message})
        reply = self.choose_reply(user_message)
        self.history.append({"role": "assistant", "content": reply})
        return reply
```

Every chatbot you build this term follows the same four steps: **record, choose, record, return.**

- Each history entry is a dictionary with a `role` (who spoke) and a `content` (what was said). Real AI services expect exactly this shape, which is why we use it now.
- `self.choose_reply(...)` is one method calling another method on the same object.

### 3c. `choose_reply`: the mock, the part a model replaces next week

```python
    def choose_reply(self, user_message):
        """Choose a reply with keyword rules. This is the mock part."""
        text = user_message.lower()
        if self.needs_human(text):
            return "I can't help with that here. I'm passing you to a human agent."
        if "order" in text:
            return self.order_reply(user_message)
        if "hello" in text:
            return f"Hello! I'm {self.name}. I can check an order status for you."
        return "I'm not sure how to help with that. I can check an order status."
```

- **The order of the rules matters.** The handoff check runs first, so a message that mentions both an address and an order goes to a person.
- The last line is the safe reply for anything it doesn't understand. It never makes something up.

### 3d. `needs_human`: the handoff rule

```python
    def needs_human(self, text):
        """Return True if the message is about something a person must handle."""
        for word in HANDOFF_WORDS:
            if word in text:
                return True
        return False
```

### 3e. `order_reply`: where the chatbot uses its tool

```python
    def order_reply(self, user_message):
        """Use the order tool to answer a question about an order."""
        order_id = self.order_tool.find_order_id(user_message)
        if order_id is None:
            return "Which order? Please send an order ID like A100."
        status = self.order_tool.find_status(order_id)
        return f"Order {order_id} is {status}."
```

Read `self.order_tool.find_order_id(...)` left to right: *this chatbot's tool, its `find_order_id` method.* When the tool returns `None`, the chatbot asks for a valid ID. It never invents a status.

<details>
<summary><b>Your complete <code>chatbot.py</code> at the end of Part 3</b></summary>

```python
# chatbot.py
# Author: [Your Name]

HANDOFF_WORDS = ["address", "payment", "card"]


class SupportChatbot:
    """A mock support chatbot. Its replies come from simple rules, not from AI."""

    def __init__(self, name, instructions, order_tool):
        """Set up one chatbot with its own name, instructions, tool, and history."""
        self.name = name
        self.instructions = instructions
        self.order_tool = order_tool
        self.history = []

    def respond(self, user_message):
        """Record the user's message, choose a reply, record it, and return it."""
        self.history.append({"role": "user", "content": user_message})
        reply = self.choose_reply(user_message)
        self.history.append({"role": "assistant", "content": reply})
        return reply

    def choose_reply(self, user_message):
        """Choose a reply with keyword rules. This is the mock part."""
        text = user_message.lower()
        if self.needs_human(text):
            return "I can't help with that here. I'm passing you to a human agent."
        if "order" in text:
            return self.order_reply(user_message)
        if "hello" in text:
            return f"Hello! I'm {self.name}. I can check an order status for you."
        return "I'm not sure how to help with that. I can check an order status."

    def needs_human(self, text):
        """Return True if the message is about something a person must handle."""
        for word in HANDOFF_WORDS:
            if word in text:
                return True
        return False

    def order_reply(self, user_message):
        """Use the order tool to answer a question about an order."""
        order_id = self.order_tool.find_order_id(user_message)
        if order_id is None:
            return "Which order? Please send an order ID like A100."
        status = self.order_tool.find_status(order_id)
        return f"Order {order_id} is {status}."
```

</details>

### Trace one message

*From the reading.* Before you run anything, follow `Where is order A100?` through your code:

1. `bot.respond("Where is order A100?")` runs with `self` set to `bot`.
2. `respond` appends the user's message to `self.history`.
3. `respond` calls `self.choose_reply(...)`.
4. `choose_reply` lowercases the text. There's no handoff word, but it contains `order`, so it calls `self.order_reply(...)`.
5. `order_reply` asks the tool for an ID. The tool returns `A100`.
6. `order_reply` asks the tool for the status. The tool returns `shipped`.
7. The sentence goes back up to `choose_reply`, then to `respond`.
8. `respond` appends the reply to the history and returns it.

```text
history before: []
reply: Order A100 is shipped.
history after:
  {'role': 'user', 'content': 'Where is order A100?'}
  {'role': 'assistant', 'content': 'Order A100 is shipped.'}
```

---

## Part 4 — Run it and test it

### Task 4: `main.py`, a real conversation

```python
# main.py
# Author: [Your Name]

from chatbot import SupportChatbot
from order_tool import OrderLookup

ORDERS = {
    "A100": "shipped",
    "A101": "processing",
    "A102": "delivered",
}

order_tool = OrderLookup(ORDERS)
bot = SupportChatbot(
    "Sunny",
    "You are a friendly support assistant for Bayside Outfitters.",
    order_tool,
)

print("Type a message, or type quit to stop.")
user_message = input("You: ")
while user_message != "quit":
    print(f"{bot.name}: {bot.respond(user_message)}")
    user_message = input("You: ")

print(f"Messages in this conversation: {len(bot.history)}")
```

**Create the tool first, then hand it over.** `order_tool` is created on its own line and then passed into `SupportChatbot(...)`. That one argument is the composition.

Run `python3 main.py` and type these six messages:

```text
Type a message, or type quit to stop.
You: hello
Sunny: Hello! I'm Sunny. I can check an order status for you.
You: Where is order A100?
Sunny: Order A100 is shipped.
You: where is my order
Sunny: Which order? Please send an order ID like A100.
You: Please change my shipping address
Sunny: I can't help with that here. I'm passing you to a human agent.
You: What is the weather?
Sunny: I'm not sure how to help with that. I can check an order status.
You: quit
Messages in this conversation: 10
```

**✅ Checkpoint:** five turns add two messages each, so the history holds **10**. Each reply comes from a different rule: greeting, tool found, tool found nothing, handoff, safe fallback.

### Task 5: eight tests (`tests/test_chatbot.py`)

```python
from chatbot import SupportChatbot
from order_tool import OrderLookup


def make_bot():
    """Build a fresh chatbot with its own tool for each test."""
    orders = {"A100": "shipped", "A101": "processing"}
    return SupportChatbot("Sunny", "Be friendly.", OrderLookup(orders))


def test_tool_finds_known_status():
    tool = OrderLookup({"A100": "shipped"})
    assert tool.find_status("A100") == "shipped"


def test_tool_returns_none_for_unknown_order():
    tool = OrderLookup({"A100": "shipped"})
    assert tool.find_status("A999") is None


def test_respond_records_both_messages():
    bot = make_bot()
    bot.respond("hello")
    assert len(bot.history) == 2
    assert bot.history[0]["role"] == "user"
    assert bot.history[1]["role"] == "assistant"


def test_order_question_uses_the_tool():
    bot = make_bot()
    assert bot.respond("Where is order A100?") == "Order A100 is shipped."


def test_order_question_without_an_id_asks_for_one():
    bot = make_bot()
    assert "order ID" in bot.respond("Where is my order?")


def test_address_change_goes_to_a_human():
    bot = make_bot()
    assert "human" in bot.respond("Please change my shipping address")


def test_unknown_request_gets_a_safe_reply():
    bot = make_bot()
    assert "not sure" in bot.respond("What is the weather today?")


def test_two_chatbots_keep_separate_histories():
    first = make_bot()
    second = make_bot()
    first.respond("hello")
    assert len(first.history) == 2
    assert len(second.history) == 0
```

What these tests show:

- **`make_bot()` gives every test a fresh chatbot.** Because the chatbot is *handed* its tool, a test can give it a tiny tool with only two orders. This is the payoff of composition.
- The first two tests check the tool with **no chatbot at all**, which is possible because it is its own class.
- The last test proves each object has its own history.

Run `pytest -v`:

```text
tests/test_chatbot.py::test_tool_finds_known_status PASSED               [ 12%]
tests/test_chatbot.py::test_tool_returns_none_for_unknown_order PASSED   [ 25%]
tests/test_chatbot.py::test_respond_records_both_messages PASSED         [ 37%]
tests/test_chatbot.py::test_order_question_uses_the_tool PASSED          [ 50%]
tests/test_chatbot.py::test_order_question_without_an_id_asks_for_one PASSED [ 62%]
tests/test_chatbot.py::test_address_change_goes_to_a_human PASSED        [ 75%]
tests/test_chatbot.py::test_unknown_request_gets_a_safe_reply PASSED     [ 87%]
tests/test_chatbot.py::test_two_chatbots_keep_separate_histories PASSED  [100%]

============================== 8 passed in 0.01s ===============================
```

**✅ Checkpoint: 8 passed.** This is a good place to commit: `git add . && git commit -m 'lab 10: chatbot and order tool'`.

---

## Part 5 — Four exercises

Each exercise states its expected result. Try it before you read the solution.

### Exercise 1: Label the parts (`exercise1.md`)

Create `exercise1.md` and answer the six questions about the code you just wrote. Here are the answers to check yours against:

```markdown
# Exercise 1

1. The two classes are: OrderLookup and SupportChatbot
2. One object of each class in main.py: order_tool and bot
3. Every attribute of SupportChatbot: name, instructions, order_tool, history
4. Every method of OrderLookup: __init__, find_order_id, find_status
5. The line in chatbot.py that is the composition: self.order_tool = order_tool
6. In bot.respond("hello"), self is: bot
```

**Why:** a class is the template you wrote with the keyword `class`. An object is what you get back when you call it. Attributes are the names assigned with `self.` in `__init__`. `__init__` counts as a method even though you never call it by name.

**Common mistake:** answering `SupportChatbot` to question 2 or question 6. That's the class. `bot` is the object.

### Exercise 2: `count_user_messages`

**Goal:** a method that returns how many messages in the history have the role `user`, plus one test.

Add this method to the bottom of `SupportChatbot` in `chatbot.py`:

```python
    def count_user_messages(self):
        """Return how many messages the user has sent so far."""
        count = 0
        for message in self.history:
            if message["role"] == "user":
                count += 1
        return count
```

Add this to the bottom of `tests/test_chatbot.py`:

```python
def test_count_user_messages():
    bot = make_bot()
    bot.respond("hello")
    bot.respond("Where is order A100?")
    assert bot.count_user_messages() == 2
```

**✅ Checkpoint:** `pytest -v` shows **9 passed**.

**Why it works:** the method reads `self.history`, so it counts whichever chatbot it is called on. It is the Week 6 counting loop over a list of dictionaries.

**Common mistakes:**
- Leaving out `self`, which fails with `takes 0 positional arguments but 1 was given`.
- Writing `history` without `self.`, which gives a `NameError`.
- Returning `len(self.history)`, which counts the chatbot's replies too.

### Exercise 3: A second tool (`stock_tool.py`)

**Goal:** customers ask about stock, too. Add that ability **without** putting stock data inside the chatbot. The chatbot gains an ability by gaining a part.

**Step 1: the new tool.** It has the same shape as `OrderLookup`: find the thing the message is about, then look it up.

```python
# stock_tool.py
# Author: [Your Name]


class StockLookup:
    """A tool that knows how many of each product are in stock."""

    def __init__(self, stock):
        """Store the stock counts this tool can look up."""
        self.stock = stock

    def find_product(self, text):
        """Return the first known product mentioned in text, or None."""
        for product in self.stock:
            if product in text.lower():
                return product
        return None

    def count_for(self, product):
        """Return how many of one product are in stock, or None if unknown."""
        if product in self.stock:
            return self.stock[product]
        return None
```

**Step 2: `chatbot.py`.** Make three changes.

Replace `__init__` so it accepts and stores a fourth value:

```python
    def __init__(self, name, instructions, order_tool, stock_tool):
        """Set up one chatbot with its own name, instructions, tools, and history."""
        self.name = name
        self.instructions = instructions
        self.order_tool = order_tool
        self.stock_tool = stock_tool
        self.history = []
```

In `choose_reply`, add the stock rule right after the order rule:

```python
        if "order" in text:
            return self.order_reply(user_message)
        if "stock" in text:
            return self.stock_reply(user_message)
```

Add a method that uses the new tool. Put it right after `order_reply`:

```python
    def stock_reply(self, user_message):
        """Use the stock tool to answer a question about a product."""
        product = self.stock_tool.find_product(user_message)
        if product is None:
            return "Which product? Please name the item you want me to check."
        count = self.stock_tool.count_for(product)
        return f"We have {count} of the {product} in stock."
```

**Step 3: every place that creates a chatbot must now pass a stock tool.** There are two such places.

In `main.py`, add the import, a `STOCK` dictionary and the tool:

```python
from chatbot import SupportChatbot
from order_tool import OrderLookup
from stock_tool import StockLookup

ORDERS = {
    "A100": "shipped",
    "A101": "processing",
    "A102": "delivered",
}

STOCK = {
    "rain jacket": 12,
    "day pack": 0,
    "trail hat": 5,
}

order_tool = OrderLookup(ORDERS)
stock_tool = StockLookup(STOCK)
bot = SupportChatbot(
    "Sunny",
    "You are a friendly support assistant for Bayside Outfitters.",
    order_tool,
    stock_tool,
)
```

The `while` loop below it stays the same.

In `tests/test_chatbot.py`, add the import, rebuild `make_bot`, and add one test:

```python
from chatbot import SupportChatbot
from order_tool import OrderLookup
from stock_tool import StockLookup


def make_bot():
    """Build a fresh chatbot with its own tools for each test."""
    order_tool = OrderLookup({"A100": "shipped", "A101": "processing"})
    stock_tool = StockLookup({"rain jacket": 12, "day pack": 0})
    return SupportChatbot("Sunny", "Be friendly.", order_tool, stock_tool)
```

```python
def test_stock_question_uses_the_stock_tool():
    bot = make_bot()
    assert "12" in bot.respond("Is the rain jacket in stock?")
```

**✅ Checkpoint:** `pytest -v` shows **10 passed**, and `python3 main.py` gives:

```text
Type a message, or type quit to stop.
You: Is the rain jacket in stock?
Sunny: We have 12 of the rain jacket in stock.
You: Do you have it in stock?
Sunny: Which product? Please name the item you want me to check.
You: quit
Messages in this conversation: 4
```

**Common mistakes:**
- Changing `__init__` but missing a place that creates the chatbot. That fails with `TypeError: SupportChatbot.__init__() missing 1 required positional argument: 'stock_tool'`.
- Forgetting `from stock_tool import StockLookup`.
- Putting the stock dictionary inside `SupportChatbot`, which mixes two unrelated jobs in one class.

### Exercise 4: Two chatbots from one class (`two_bots.py`)

```python
# two_bots.py
# Author: [Your Name]

from chatbot import SupportChatbot
from order_tool import OrderLookup
from stock_tool import StockLookup

order_tool = OrderLookup({"A100": "shipped", "A101": "processing"})
stock_tool = StockLookup({"rain jacket": 12, "day pack": 0})

sunny = SupportChatbot("Sunny", "You are cheerful and brief.", order_tool, stock_tool)
river = SupportChatbot("River", "You are formal and detailed.", order_tool, stock_tool)

sunny.respond("hello")
sunny.respond("Where is order A100?")
river.respond("hello")

print(sunny.name, len(sunny.history))
print(river.name, len(river.history))
print(sunny.history[1]["content"])
print(river.history[1]["content"])
print(sunny.instructions)
print(river.instructions)
```

Run `python3 two_bots.py`:

```text
Sunny 4
River 2
Hello! I'm Sunny. I can check an order status for you.
Hello! I'm River. I can check an order status for you.
You are cheerful and brief.
You are formal and detailed.
```

**Why it works:** each `SupportChatbot(...)` call runs `__init__` again, so each chatbot gets its own name, instructions and empty history. Sunny's two turns don't appear in River's history. Both share the same two tool objects, which is fine because the tools only answer questions.

**Notice:** the two sets of instructions don't change the replies, because in this mock nothing reads them. They start to matter in Week 11, when they are sent to a model.

---

## Part 6 — Mini-project: an assistant of your own

Build a small business assistant with the same two-class shape, in **four new files** so it doesn't disturb Sunny: `my_tool.py`, `my_assistant.py`, `my_main.py` and `tests/test_my_assistant.py`. Choose one: an FAQ assistant, an appointment helper, an order-status assistant for a different business, or your own idea with your instructor's approval.

### Design it before you type: five decisions

1. **The business and the assistant's name.** Use a different business from the reference below.
2. **The tool's data:** one dictionary, such as days to open times, questions to answers, or tickets to statuses.
3. **The tool's two methods:** `find_...(text)` returns the key named in the message or `None`, and a lookup returns the value or `None`. These are `OrderLookup`'s two methods with new names.
4. **The trigger words** that send a message to the tool, such as `"open"` or `"available"`.
5. **The handoff words:** requests that *change* something, which a person must approve. Be ready to say why.

### Checklist (graded)

- [ ] A tool class in its own file, with `__init__` and at least one other method
- [ ] An assistant class in its own file that is handed the tool and stores it
- [ ] The assistant keeps a history with a role and content for every message
- [ ] `my_main.py` accepts typed messages until the user types `quit`
- [ ] At least one kind of request is answered by using the tool
- [ ] A lookup that finds nothing gets a helpful reply, not a crash or a made-up answer
- [ ] A request it can't handle gets a safe reply that says so
- [ ] At least one kind of request is passed to a person, and you can say why
- [ ] At least four tests, all passing
- [ ] A `README.md` section of four to six sentences (template below)

### Worked example: Robin, an appointment helper for Bayside Tax Help

This is the lab page's reference solution. **Compare against it, don't copy it.** Your assistant should serve a different business and have its own rules. The reference uses `appointment_*` file names, and yours use the `my_*` names above.

**The tool, `appointment_tool.py`:**

```python
# appointment_tool.py
# Author: [Your Name]


class AppointmentBook:
    """A tool that knows which appointment times are open on each day."""

    def __init__(self, open_times):
        """Store the open times this tool can look up."""
        self.open_times = open_times

    def find_day(self, text):
        """Return the first known day mentioned in text, or None."""
        for day in self.open_times:
            if day in text.lower():
                return day
        return None

    def times_for(self, day):
        """Return the open times for one day, or None if the day is unknown."""
        if day in self.open_times:
            return self.open_times[day]
        return None
```

**The assistant, `appointment_bot.py`.** It is the same shape as `SupportChatbot`: record, choose, record, return.

```python
# appointment_bot.py
# Author: [Your Name]

HANDOFF_WORDS = ["book", "cancel", "reschedule"]


class AppointmentHelper:
    """A mock appointment helper. Its replies come from simple rules, not from AI."""

    def __init__(self, name, instructions, appointment_book):
        """Set up one helper with its own name, instructions, tool, and history."""
        self.name = name
        self.instructions = instructions
        self.appointment_book = appointment_book
        self.history = []

    def respond(self, user_message):
        """Record the user's message, choose a reply, record it, and return it."""
        self.history.append({"role": "user", "content": user_message})
        reply = self.choose_reply(user_message)
        self.history.append({"role": "assistant", "content": reply})
        return reply

    def choose_reply(self, user_message):
        """Choose a reply with keyword rules. This is the mock part."""
        text = user_message.lower()
        if self.needs_human(text):
            return "I can't change the schedule. I'm passing you to the front desk."
        if "open" in text or "available" in text:
            return self.times_reply(user_message)
        if "hello" in text:
            return f"Hello! I'm {self.name}. Ask me which times are open on a day."
        return "I'm not sure how to help with that. I can list open times."

    def needs_human(self, text):
        """Return True if the message asks to change the schedule."""
        for word in HANDOFF_WORDS:
            if word in text:
                return True
        return False

    def times_reply(self, user_message):
        """Use the appointment book to answer a question about open times."""
        day = self.appointment_book.find_day(user_message)
        if day is None:
            return "Which day? I can check Monday, Wednesday, or Friday."
        times = self.appointment_book.times_for(day)
        return f"Open times on {day}: {times}."
```

**The runner, `appointment_main.py`:**

```python
# appointment_main.py
# Author: [Your Name]

from appointment_bot import AppointmentHelper
from appointment_tool import AppointmentBook

OPEN_TIMES = {
    "monday": "9:00 am and 2:30 pm",
    "wednesday": "11:00 am",
    "friday": "none",
}

appointment_book = AppointmentBook(OPEN_TIMES)
helper = AppointmentHelper(
    "Robin",
    "You help clients of Bayside Tax Help find an open appointment time.",
    appointment_book,
)

print("Type a message, or type quit to stop.")
user_message = input("You: ")
while user_message != "quit":
    print(f"{helper.name}: {helper.respond(user_message)}")
    user_message = input("You: ")

print(f"Messages in this conversation: {len(helper.history)}")
```

**The tests, `tests/test_appointment_bot.py`.** There is one test per checklist behavior: tool used, lookup finds nothing, handoff, safe reply and history.

```python
from appointment_bot import AppointmentHelper
from appointment_tool import AppointmentBook


def make_helper():
    """Build a fresh helper with its own tool for each test."""
    book = AppointmentBook({"monday": "9:00 am and 2:30 pm", "friday": "none"})
    return AppointmentHelper("Robin", "Be clear.", book)


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
```

**A sample run.** Each line exercises one checklist item:

```text
Type a message, or type quit to stop.
You: hello
Robin: Hello! I'm Robin. Ask me which times are open on a day.
You: What times are open on Monday?
Robin: Open times on monday: 9:00 am and 2:30 pm.
You: What is available?
Robin: Which day? I can check Monday, Wednesday, or Friday.
You: Please book me for Monday at 9
Robin: I can't change the schedule. I'm passing you to the front desk.
You: Do you validate parking?
Robin: I'm not sure how to help with that. I can list open times.
You: quit
Messages in this conversation: 10
```

**Why it's built this way:** the tool knows the schedule, and the helper knows the conversation. Booking, cancelling and rescheduling change someone's calendar, so those go to the front desk. The helper only reads.

### The README section

Add four to six sentences to `README.md` covering each of these points:

```markdown
## Lab 10 Mini-Project: <assistant name>

<What it does: the business, and the one kind of question it answers with its tool.>
<What is mock about it: replies come from keyword rules, and the data is a dictionary typed into the file.>
<Which requests go to a person, and why: they change something real.>
<One thing that could go wrong with real customer data, such as private details in the history or a keyword rule misfiring.>
```

### Rubric (10 points)

| Pts | Requirement |
|---|---|
| 2 | The tool is a separate class in its own file and has no conversation code in it |
| 2 | The assistant class stores its tool and its history as attributes set in `__init__` |
| 2 | The program runs from `my_main.py`, answers one kind of request with the tool, and records every turn |
| 2 | Unknown requests, failed lookups and the human handoff each get a sensible reply |
| 1 | At least four tests pass, and the full ritual passes |
| 1 | The README section is specific about what is mock and what could go wrong |

---

## Part 7 — Ritual, push and submit

```bash
ruff format . && ruff check . && pytest -v
git add . && git commit -m 'lab 10: OOP for agents chatbot and tool' && git push
```

- With the reference mini-project in the folder, the last line of the test output reads **`15 passed`**: 10 chatbot tests plus 5 mini-project tests. With your own mini-project, it is 10 plus however many tests you wrote, at least four.
- **If `ruff check` stops on a fixable error,** the `&&` chain ends there and `pytest` never runs. Run `ruff check --fix .`, then run the full first line again.

**Submit:** paste your GitHub repository URL in Canvas.

- [ ] The repo is **Public**, and `git status` says *nothing to commit, working tree clean*
- [ ] The commit message includes `lab 10`
- [ ] The repo contains `exercise1.md`, `two_bots.py`, your four `my_*` files, and the `README.md` section
- [ ] No screenshots. The repo is the whole submission: it is graded by cloning it and running your code and `pytest`

---

## When something breaks

*From the reading's "three mistakes almost everyone makes", plus the exercises.*

| You see | Cause | Fix |
|---|---|---|
| `TypeError: ...greet() takes 0 positional arguments but 1 was given` | A method is missing `self` in its parameter list. Python passes the object in, and there's nowhere to put it | `def greet(self):` |
| `AttributeError: 'SupportChatbot' object has no attribute 'name'` | `name = name` without `self.` sets a local variable that disappears | `self.name = name` |
| `TypeError: ...missing 1 required positional argument: 'self'` | You called a method on the **class** (`SupportChatbot.respond(...)`) | Call it on an **object**: `bot.respond(...)` |
| `TypeError: SupportChatbot.__init__() missing 1 required positional argument: 'stock_tool'` | Exercise 3 changed `__init__`, but one place still passes three values | Update `main.py`, `make_bot()` and `two_bots.py` |
| `ModuleNotFoundError: No module named 'stock_tool'` | The file name doesn't match the import (for example `stock_tools.py`), or the file was never saved | Run `ls` and make the file name match the `import` line exactly |
| `can't open file '.../main.py': [Errno 2] No such file or directory` | The terminal is in a different folder | `cd ~/ism3232/module06_agents`, then run it again |
| One chatbot's history shows another's messages | `history = []` was written in the class body, so every object shares one list | Create it in `__init__` as `self.history = []` |

**A list in the wrong place.** This is the bug behind the last row. Predict the output before you run it:

```python
class SupportChatbot:
    history = []  # BUG: written in the class body, so every chatbot shares one list

    def __init__(self, name):
        self.name = name

    def respond(self, user_message):
        self.history.append(user_message)
        return "ok"


sunny = SupportChatbot("Sunny")
river = SupportChatbot("River")
sunny.respond("hello")
print(len(sunny.history))
print(len(river.history))
```

```text
1
1
```

River holds a message only Sunny received. In a real chatbot, that shows one customer another customer's conversation.

### What a business chatbot can get wrong

*From the lecture's last segment.* Try the first one in your own `main.py`.

```text
You: Can I pay with a different card?
Sunny: I can't help with that here. I'm passing you to a human agent.
You: Do you sell cardigans?
Sunny: I can't help with that here. I'm passing you to a human agent.
```

1. **Unreliable output.** The cardigan question goes to a human because `cardigans` contains `card`. Keyword rules are brittle. A model is wrong in less predictable ways, and you find out by testing with real messages.
2. **Failed tools.** The order may not exist, or the order system may be down. Sunny asks for a valid ID and never invents a status.
3. **Sensitive data.** `self.history` keeps everything a user types, including anything typed by accident. Sunny never asks for payment details.
4. **Actions that need a person.** Looking something up changes nothing. Changing an address changes where a parcel goes. A person approves changes, and Week 12 builds that approval step.

### Where this goes next

| Built today | Becomes |
|---|---|
| `choose_reply` (the mock) | Week 11: a local model through Ollama replaces it |
| `self.instructions` (stored, unused) | Week 11: sent to the model as its system message |
| `self.order_tool`, `self.stock_tool` | Week 12: the model decides when to call a tool |
| The `None` checks | Error handling for model and tool failures |
| `HANDOFF_WORDS` | Week 12: human approval for actions |
| `make_bot()` and your tests | Testing with a fake model |
