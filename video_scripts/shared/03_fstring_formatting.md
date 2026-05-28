# Video 03: F-string Formatting

## YouTube Metadata

**Title:** Python F-String Formatting for Business Reports | ISM2411 / ISM3232
**Description:**
F-strings are Python's cleanest way to embed variables into text and format numbers for professional output. In this video you'll learn the four formatting patterns every business programmer needs: currency, thousands separators, percentages, and padding for aligned columns.

We'll build a formatted order receipt from scratch and finish with a clean sales report table — the kind of output that goes into emails, dashboards, and management summaries.

**Chapters:**
0:00 — What f-strings are and why they replaced .format()
1:30 — Basic f-string syntax
3:00 — Currency formatting :.2f
5:00 — Thousands separator :,
6:30 — Percentage formatting :.1%
8:00 — Column alignment and padding
10:00 — Building a formatted receipt
12:00 — Recap

**Applies to:** ISM2411 Module 3 · ISM3232 Module 5

**Tags:** python f-strings, python string formatting, python fstring, python format numbers, python currency format, python percentage, python business, ISM2411, ISM3232, python tutorial, python beginner, python print formatting

---

## Script

### INTRO (0:00–1:30)

You've got the numbers. The subtotal, the tax, the order total. But `print(192.308)` looks nothing like a professional receipt. Business output needs to look right — two decimal places for dollars, commas in large numbers, percent signs on rates, aligned columns in reports. That's what f-strings are for.

F-strings were introduced in Python 3.6 and they've become the standard way to embed variables into text. They're faster to write, easier to read, and more powerful than the older `.format()` method or `%` formatting. Let's learn them properly.

---

### BASIC SYNTAX (1:30–3:00)

An f-string starts with the letter `f` immediately before the opening quote. Variables and expressions go inside curly braces `{}`.

```python
name  = "Elena Vasquez"
total = 192.308

# Old way — awkward:
print("Customer: " + name + ", Total: $" + str(round(total, 2)))

# f-string — clean:
print(f"Customer: {name}, Total: ${total:.2f}")
```

Output: `Customer: Elena Vasquez, Total: $192.31`

You can put any Python expression inside the braces — variable names, math, function calls, even conditional expressions.

```python
quantity = 8
print(f"You ordered {quantity} item{'s' if quantity != 1 else ''}.")
```

Output: `You ordered 8 items.`

---

### CURRENCY FORMATTING — :.2f (3:00–5:00)

The format spec goes after a colon inside the braces. `:.2f` means: format as a fixed-point number with exactly 2 decimal places.

```python
price    = 24.99
subtotal = 199.92
tax      = 13.994
total    = 213.914

print(f"Price:    ${price:.2f}")      # $24.99
print(f"Subtotal: ${subtotal:.2f}")   # $199.92
print(f"Tax:      ${tax:.2f}")        # $13.99
print(f"Total:    ${total:.2f}")      # $213.91
```

The `.2f` rounds to 2 decimal places for display — it does NOT change the underlying float value. The variable `total` is still `213.914` in memory.

If you want 0 decimal places (for whole-dollar amounts): `:.0f`
If you want 4 decimal places (for unit costs): `:.4f`

---

### THOUSANDS SEPARATOR — :, (5:00–6:30)

For large numbers, use `:,` to add comma separators.

```python
annual_revenue   = 1285400.50
units_sold       = 48250
projected_target = 1500000

print(f"Annual revenue:    ${annual_revenue:,.2f}")
print(f"Units sold:         {units_sold:,}")
print(f"Target:            ${projected_target:,.0f}")
```

Output:
```
Annual revenue:    $1,285,400.50
Units sold:         48,250
Target:            $1,500,000
```

You can combine specifiers: `:,.2f` means comma separator AND 2 decimal places.

---

### PERCENTAGE FORMATTING — :.1% (6:30–8:00)

The `%` specifier multiplies by 100 and adds a percent sign. So `0.085` becomes `8.5%`.

```python
discount_rate = 0.10
tax_rate      = 0.0875
margin        = 0.342

print(f"Discount: {discount_rate:.0%}")   # 10%
print(f"Tax rate: {tax_rate:.2%}")        # 8.75%
print(f"Margin:   {margin:.1%}")          # 34.2%
```

No need to multiply by 100 yourself — the `%` specifier handles it. Store your rates as decimals (0.10, not 10) and format them as percentages only at display time.

---

### COLUMN ALIGNMENT (8:00–10:00)

For reports and tables, you need numbers aligned in columns. Use width specifiers with `>` (right-align), `<` (left-align), or `^` (center).

```python
print(f"{'Item':<20} {'Qty':>5} {'Price':>10} {'Total':>10}")
print(f"{'─' * 20} {'─' * 5} {'─' * 10} {'─' * 10}")

items = [
    ("Laptop Bag",      2, 49.99),
    ("USB-C Hub",       3, 24.99),
    ("Wireless Mouse",  1, 39.99),
]

for name, qty, price in items:
    line_total = qty * price
    print(f"{name:<20} {qty:>5} {price:>10.2f} {line_total:>10.2f}")
```

Output:
```
Item                   Qty      Price      Total
──────────────────── ─────  ──────────  ──────────
Laptop Bag               2      49.99      99.98
USB-C Hub                3      24.99      74.97
Wireless Mouse           1      39.99      39.99
```

`:<20` — left-align in a field 20 characters wide.
`:>10.2f` — right-align in a 10-char field, 2 decimal places.

---

### BUILDING A FORMATTED RECEIPT (10:00–12:00)

Putting it all together — a complete order receipt.

```python
customer     = "Marcus Thompson"
order_id     = "ORD-20240528-004"
subtotal     = 214.94
discount     = subtotal * 0.10
after_disc   = subtotal - discount
tax          = after_disc * 0.0875
total        = after_disc + tax

print(f"{'CAMPUS BOOKSTORE':^40}")
print(f"{'─' * 40}")
print(f"Customer:  {customer}")
print(f"Order ID:  {order_id}")
print(f"{'─' * 40}")
print(f"{'Subtotal':<20} ${subtotal:>15,.2f}")
print(f"{'Discount (10%)':<20} ${discount:>15,.2f}")
print(f"{'After discount':<20} ${after_disc:>15,.2f}")
print(f"{'Tax (8.75%)':<20} ${tax:>15,.2f}")
print(f"{'─' * 40}")
print(f"{'TOTAL':<20} ${total:>15,.2f}")
```

Output:
```
         CAMPUS BOOKSTORE
────────────────────────────────────────
Customer:  Marcus Thompson
Order ID:  ORD-20240528-004
────────────────────────────────────────
Subtotal             $         214.94
Discount (10%)       $          21.49
After discount       $         193.45
Tax (8.75%)          $          16.93
────────────────────────────────────────
TOTAL                $         210.38
```

---

### RECAP (12:00–12:30)

- `f"text {variable}"` — embed a variable in a string
- `{value:.2f}` — 2 decimal places
- `{value:,.2f}` — comma separator + 2 decimal places
- `{value:.1%}` — percentage (multiplies by 100, adds %)
- `{value:<20}` / `{value:>10}` — left/right align in a field width
- Store rates as decimals, format as percentages at print time

Next video: conditionals — using `if`, `elif`, and `else` to encode business rules.
