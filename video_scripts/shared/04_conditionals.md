# Video 04: Conditionals — if / elif / else

## YouTube Metadata

**Title:** Python Conditionals for Business Logic — if, elif, else | ISM2411 / ISM3232
**Description:**
Business rules are conditionals in disguise. "Apply a 10% discount on orders over $100. Apply 15% over $250. Flag anything over $500 for manager review." In Python, you write that logic with if, elif, and else.

In this video we translate real business decision trees into Python code. You'll learn the exact syntax, understand indentation as structure, avoid the most common conditional bugs, and write a multi-tier discount engine by the end.

**Chapters:**
0:00 — Business rules as code
1:00 — if statement syntax and indentation
3:30 — Adding elif for multiple tiers
6:30 — else as the default case
8:30 — Nested conditionals
10:30 — Combining conditions with and / or
12:30 — Common mistakes
14:00 — Recap

**Applies to:** ISM2411 Module 5 · ISM3232 Module 6

**Tags:** python if else, python conditionals, python elif, python if statement, python business logic, python decision making, python indentation, python tutorial, ISM2411, ISM3232, python for beginners, python control flow

---

## Script

### INTRO (0:00–1:00)

Every business runs on rules. A customer who spends over $100 gets 10% off. Over $250, they get 15%. Over $500, the order needs manager approval. A product that drops below 5 units on hand gets flagged for reorder.

These are all conditionals — decisions the program makes by asking "is this condition true?" In Python, you write conditionals with `if`, `elif`, and `else`. They are the most important control flow structure in the language, and you'll use them in every non-trivial script you ever write. Let's learn them right.

---

### IF STATEMENT SYNTAX (1:00–3:30)

The basic structure:

```python
if condition:
    # code that runs when condition is True
```

Two things to notice immediately. The condition is followed by a colon. And the code that runs when the condition is true is **indented** — 4 spaces, or one tab. Indentation is not decoration in Python. It is the structure. Python uses it to know which code belongs to which block.

```python
order_total = 150.00

if order_total > 100:
    discount_rate = 0.10
    discount = order_total * discount_rate
    print(f"Discount applied: {discount_rate:.0%}")
    print(f"You save: ${discount:.2f}")
```

Output:
```
Discount applied: 10%
You save: $15.00
```

If you change `order_total` to 80, nothing prints — the condition is False, so the indented block is skipped entirely.

---

### ADDING ELIF (3:30–6:30)

`elif` means "else if" — it gives you additional branches to check when the first condition is False.

```python
order_total = 300.00

if order_total > 250:
    discount_rate = 0.15
elif order_total > 100:
    discount_rate = 0.10
else:
    discount_rate = 0.0

discount = order_total * discount_rate
final_total = order_total - discount

print(f"Order total:    ${order_total:.2f}")
print(f"Discount rate:  {discount_rate:.0%}")
print(f"Discount:      -${discount:.2f}")
print(f"Final total:    ${final_total:.2f}")
```

Python checks conditions from top to bottom. The **first** condition that is `True` wins — the rest are skipped. So the order of your `elif` branches matters. Here, we check the larger threshold first. If we checked `> 100` first, every $300 order would only get 10% off, because `300 > 100` is also True.

With `order_total = 300`:
```
Order total:    $300.00
Discount rate:  15%
Discount:      -$45.00
Final total:    $255.00
```

---

### ELSE AS DEFAULT (6:30–8:30)

`else` catches everything that didn't match any previous condition. It has no condition of its own — it's the fallback.

```python
order_total = 600.00
APPROVAL_LIMIT = 500

if order_total >= APPROVAL_LIMIT:
    status = "PENDING APPROVAL"
    print(f"Order flagged: ${order_total:.2f} exceeds limit of ${APPROVAL_LIMIT:,.0f}")
    print("Sending alert to manager.")
elif order_total > 250:
    status = "AUTO-APPROVED"
    discount_rate = 0.15
elif order_total > 100:
    status = "AUTO-APPROVED"
    discount_rate = 0.10
else:
    status = "AUTO-APPROVED"
    discount_rate = 0.0

print(f"Status: {status}")
```

Note: `APPROVAL_LIMIT` is in all caps — a Python convention for constants, values that don't change. Use it to make your business rules easy to find and update.

---

### NESTED CONDITIONALS (8:30–10:30)

Sometimes a decision depends on a previous decision. Nest one `if` inside another.

```python
is_member       = True
order_total     = 120.00
account_overdue = False

if is_member:
    if account_overdue:
        print("Account overdue — no discount applied.")
        discount_rate = 0.0
    else:
        discount_rate = 0.12   # member gets extra 2%
        print(f"Member discount: {discount_rate:.0%}")
else:
    if order_total > 100:
        discount_rate = 0.10
    else:
        discount_rate = 0.0
```

Keep nesting shallow — more than 2 levels deep is usually a sign to refactor into functions. We'll cover that in a later video.

---

### COMBINING CONDITIONS (10:30–12:30)

Use `and` / `or` to combine conditions on a single line instead of nesting.

```python
is_member   = True
order_total = 120.00
is_holiday  = False

# Member AND order over $100:
if is_member and order_total > 100:
    discount_rate = 0.12

# Member OR holiday sale:
if is_member or is_holiday:
    free_shipping = True

# Not overdue:
account_overdue = False
if not account_overdue:
    print("Account in good standing.")
```

`and` requires both sides True. `or` requires at least one True. `not` flips True/False.

---

### COMMON MISTAKES (12:30–14:00)

**Missing colon after the condition.** SyntaxError every time.

```python
# Wrong:
if order_total > 100
    print("Discount applies")

# Right:
if order_total > 100:
    print("Discount applies")
```

**Wrong indentation.** Python is strict. All lines in the same block must be indented by the same amount.

```python
# Wrong — inconsistent indentation:
if order_total > 100:
    discount = 0.10
        print("Applied")   # IndentationError

# Right:
if order_total > 100:
    discount = 0.10
    print("Applied")
```

**Using `=` instead of `==`.**

```python
# Wrong — assigns 100 to order_total instead of comparing:
if order_total = 100:   # SyntaxError

# Right:
if order_total == 100:
```

**Unreachable elif.** Putting a broader condition before a narrower one.

```python
# Wrong — the second branch never runs:
if order_total > 100:
    rate = 0.10
elif order_total > 250:   # never reached if first is True
    rate = 0.15

# Right — check narrow first, then broaden:
if order_total > 250:
    rate = 0.15
elif order_total > 100:
    rate = 0.10
```

---

### RECAP (14:00–15:00)

- `if condition:` — runs the indented block when True
- `elif condition:` — checked only if everything above was False
- `else:` — runs when nothing else matched
- Conditions are checked top to bottom — first match wins
- Use `and`, `or`, `not` to combine conditions
- Indentation is structure — 4 spaces, always consistent
- Put narrower conditions before broader ones

Next video: for loops — running the same logic over every item in a list of orders.
