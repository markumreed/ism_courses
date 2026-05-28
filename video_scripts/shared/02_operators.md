# Video 02: Operators — Arithmetic, Comparison & Logical

## YouTube Metadata

**Title:** Python Operators for Business — Arithmetic, Comparison & Logical | ISM2411 / ISM3232
**Description:**
Master Python's three operator families — arithmetic, comparison, and logical — through a single business scenario: processing a customer order from raw numbers to an approved total.

You'll calculate order subtotals, apply discount rules, check approval thresholds, and combine conditions to make real business decisions. These are the building blocks of every conditional, loop, and function you'll write.

**Chapters:**
0:00 — What operators do and why they matter
1:00 — Arithmetic operators: +, -, *, /, //, %, **
5:00 — Comparison operators: ==, !=, <, >, <=, >=
8:30 — Logical operators: and, or, not
11:30 — Putting it all together: order approval logic
13:30 — Common mistakes
14:30 — Recap

**Applies to:** ISM2411 Module 4 · ISM3232 Module 5

**Tags:** python operators, python arithmetic, python comparison operators, python logical operators, python and or not, python business, python tutorial, ISM2411, ISM3232, USF, python for beginners, python expressions, python order of operations

---

## Script

### INTRO (0:00–1:00)

Variables hold data. Operators transform it. In the last video we built a product record — a name, a price, a quantity, a boolean. In this video we take those values and do real work with them: calculate totals, apply discounts, check whether an order qualifies for approval, and combine multiple conditions into a single business decision.

Python has three families of operators you need to know. Arithmetic operators do math. Comparison operators ask yes-or-no questions about values. Logical operators combine those yes-or-no answers. Let's work through all three with one running example.

---

### ARITHMETIC OPERATORS (1:00–5:00)

Open a new file: `order_calculator.py`. We have a customer order — unit price, quantity, and a discount rate.

```python
unit_price    = 24.99
quantity      = 8
discount_rate = 0.10   # 10%
tax_rate      = 0.07   # 7%
```

**Addition and subtraction** — straightforward.

```python
subtotal  = unit_price * quantity        # 199.92
discount  = subtotal * discount_rate     # 19.992
after_discount = subtotal - discount     # 179.928
```

**Multiplication and division** — you just used `*`. Division with `/` always returns a float.

```python
price_per_half_dozen = unit_price * 6 / 2
print(price_per_half_dozen)   # 74.97
```

**Floor division `//`** — divides and drops the decimal, returning an int. Useful for splitting orders into full cases.

```python
units_per_case = 6
full_cases = quantity // units_per_case   # 1 (8 // 6 = 1)
leftover   = quantity % units_per_case    # 2 (8 % 6 = 2)
print(f"{full_cases} full cases, {leftover} loose units")
```

**Modulo `%`** gives you the remainder. In business: packaging, scheduling, splitting batches.

**Exponentiation `**`** — less common but useful for compound growth.

```python
annual_growth = 0.05
projected_value = 10_000 * (1 + annual_growth) ** 3
print(f"3-year projection: ${projected_value:,.2f}")
```

Note: `10_000` — Python lets you use underscores as thousand separators in numbers. Makes large numbers readable.

---

### COMPARISON OPERATORS (5:00–8:30)

Comparison operators compare two values and return `True` or `False`. They are the engine of every `if` statement you'll write.

```python
subtotal = 179.93   # after discount

print(subtotal > 100)     # True  — qualifies for free shipping?
print(subtotal >= 200)    # False — qualifies for manager approval waiver?
print(subtotal == 179.93) # True  — exact match
print(subtotal != 0)      # True  — is there actually an order?
print(subtotal < 50)      # False — too small to process?
```

**The double-equals trap.** `=` assigns a value. `==` compares two values. This is one of the most common beginner errors.

```python
# This ASSIGNS — sets subtotal to 100, doesn't compare:
# subtotal = 100   ← assignment

# This COMPARES — asks "is subtotal equal to 100?":
print(subtotal == 100)   # False
```

---

### LOGICAL OPERATORS (8:30–11:30)

Logical operators combine comparisons. There are three: `and`, `or`, `not`.

**`and`** — both conditions must be True.

```python
# Approve order automatically only if:
# — subtotal is under the approval limit AND
# — customer account is in good standing

approval_limit    = 500
account_in_good_standing = True

auto_approved = subtotal < approval_limit and account_in_good_standing
print(auto_approved)   # True
```

**`or`** — at least one condition must be True.

```python
# Apply discount if customer is a member OR order is over $150

is_member  = False
large_order = subtotal > 150

gets_discount = is_member or large_order
print(gets_discount)   # True (large_order is True)
```

**`not`** — flips True to False and False to True.

```python
is_backordered = False
can_ship_today = not is_backordered
print(can_ship_today)   # True
```

---

### PUTTING IT ALL TOGETHER (11:30–13:30)

Let's combine everything into a real order approval check.

```python
unit_price            = 24.99
quantity              = 8
discount_rate         = 0.10
tax_rate              = 0.07
approval_limit        = 500
account_in_good_standing = True
is_member             = False

subtotal      = unit_price * quantity
discount      = subtotal * discount_rate
after_discount = subtotal - discount
tax           = after_discount * tax_rate
order_total   = after_discount + tax

large_order    = order_total > 150
auto_approved  = order_total < approval_limit and account_in_good_standing
gets_discount  = is_member or large_order

print(f"Order total:    ${order_total:.2f}")
print(f"Gets discount:  {gets_discount}")
print(f"Auto-approved:  {auto_approved}")
```

Output:
```
Order total:    $192.31
Gets discount:  True
Auto-approved:  True
```

One file. Real business logic. All three operator families working together.

---

### COMMON MISTAKES (13:30–14:30)

**Using `=` instead of `==` in a comparison.** Python will either throw a SyntaxError or silently do the wrong thing depending on context. Always double-check.

**Forgetting operator precedence.** Multiplication and division happen before addition and subtraction — same as in math. Use parentheses to be explicit.

```python
# Wrong — calculates (price + tax) * quantity:
total = unit_price + tax_rate * quantity

# Right:
total = (unit_price + unit_price * tax_rate) * quantity
```

**Comparing floats for exact equality.** Floating-point arithmetic has tiny rounding errors. Instead of `total == 192.31`, use `round(total, 2) == 192.31` or compare with a small tolerance.

---

### RECAP (14:30–15:00)

- **Arithmetic:** `+`, `-`, `*`, `/`, `//` (floor div), `%` (modulo), `**` (power)
- **Comparison:** `==`, `!=`, `<`, `>`, `<=`, `>=` — always return `True` or `False`
- **Logical:** `and`, `or`, `not` — combine comparisons into compound conditions
- `=` assigns · `==` compares — never mix them up

Next video: f-strings — how to format these calculated values so they look right in reports, receipts, and dashboards.
