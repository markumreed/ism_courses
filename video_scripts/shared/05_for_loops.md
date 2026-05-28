# Video 05: For Loops & Iteration Patterns

## YouTube Metadata

**Title:** Python For Loops & Iteration — Business Data Patterns | ISM2411 / ISM3232
**Description:**
A loop lets you apply the same logic to every item in a collection without copy-pasting code. In this video we process a list of sales transactions to calculate total revenue, average order value, the largest order, and a filtered count — four patterns every business programmer reaches for constantly.

By the end you'll understand the accumulator pattern cold, know when to use enumerate() and range(), and be able to process any list of business records with clean, readable code.

**Chapters:**
0:00 — Why loops exist
1:00 — For loop syntax
2:30 — The accumulator pattern: running total
5:00 — Average, max, min
8:00 — Filtering with if inside a loop
10:00 — enumerate() and range()
13:00 — Common mistakes
15:30 — Recap

**Applies to:** ISM2411 Module 6 · ISM3232 Module 6

**Tags:** python for loop, python loops, python iteration, python accumulator, python enumerate, python range, python business, python data processing, ISM2411, ISM3232, python tutorial, python beginner, python list loop

---

## Script

### INTRO (0:00–1:00)

Imagine you have 50 customer orders. You need the total revenue, the average order size, the largest single order, and a count of orders that qualify for free shipping. Without loops, you'd write the same code 50 times. With a loop, you write it once and Python applies it to every item automatically.

For loops are how you process collections of data — lists of orders, rows in a spreadsheet, records from a database. They are the workhorse of data processing, and the patterns we're about to learn — accumulator, filter, search — come up in virtually every real business script. Let's start.

---

### FOR LOOP SYNTAX (1:00–2:30)

The basic structure:

```python
for item in collection:
    # code that runs for each item
```

A concrete example:

```python
products = ["Laptop Bag", "USB-C Hub", "Wireless Mouse", "Monitor Stand"]

for product in products:
    print(product)
```

Output:
```
Laptop Bag
USB-C Hub
Wireless Mouse
Monitor Stand
```

Python takes each element out of the list one at a time, assigns it to the variable `product`, runs the indented block, then moves to the next element. When the list is exhausted, the loop ends.

The variable name — `product` here — is your choice. It can be anything. But name it what the items actually are: `order`, `customer`, `row`, `transaction`.

---

### THE ACCUMULATOR PATTERN (2:30–5:00)

The accumulator pattern is the most important loop pattern in business programming. You start a counter or total at zero, then update it with each item.

```python
daily_sales = [142.50, 89.99, 312.00, 47.25, 203.80, 156.40, 78.95]

total_revenue = 0   # start at zero — the accumulator

for sale in daily_sales:
    total_revenue = total_revenue + sale   # or: total_revenue += sale

print(f"Total revenue: ${total_revenue:,.2f}")
```

Output: `Total revenue: $1,030.89`

The `+=` shorthand — `total_revenue += sale` — means "add `sale` to `total_revenue` and store the result back in `total_revenue`". It's equivalent to the full form but cleaner.

**Counting** uses the same pattern, adding 1 instead of the value:

```python
order_count = 0

for sale in daily_sales:
    order_count += 1

print(f"Number of orders: {order_count}")
```

Python also has `len()` for this specific case — `len(daily_sales)` — but the counting accumulator generalizes to conditional counting, which we'll use shortly.

---

### AVERAGE, MAX, MIN (5:00–8:00)

**Average** — total divided by count.

```python
total   = 0
count   = 0

for sale in daily_sales:
    total += sale
    count += 1

average = total / count
print(f"Average order: ${average:.2f}")
```

Output: `Average order: $147.27`

**Maximum** — track the highest value seen so far.

```python
max_sale = 0   # start at 0, or use daily_sales[0] to start at first element

for sale in daily_sales:
    if sale > max_sale:
        max_sale = sale

print(f"Largest order: ${max_sale:.2f}")
```

Output: `Largest order: $312.00`

**Putting all three together:**

```python
daily_sales = [142.50, 89.99, 312.00, 47.25, 203.80, 156.40, 78.95]

total    = 0
count    = 0
max_sale = 0
min_sale = daily_sales[0]   # start with first element for minimum

for sale in daily_sales:
    total    += sale
    count    += 1
    if sale > max_sale:
        max_sale = sale
    if sale < min_sale:
        min_sale = sale

average = total / count

print(f"Orders processed: {count}")
print(f"Total revenue:    ${total:,.2f}")
print(f"Average order:    ${average:.2f}")
print(f"Largest order:    ${max_sale:.2f}")
print(f"Smallest order:   ${min_sale:.2f}")
```

Output:
```
Orders processed: 7
Total revenue:    $1,030.89
Average order:    $147.27
Largest order:    $312.00
Smallest order:   $47.25
```

---

### FILTERING INSIDE A LOOP (8:00–10:00)

Add an `if` statement inside the loop to process only items that match a condition. This is the filter pattern.

```python
SHIPPING_THRESHOLD = 100.00

free_shipping_count    = 0
free_shipping_revenue  = 0

for sale in daily_sales:
    if sale >= SHIPPING_THRESHOLD:
        free_shipping_count   += 1
        free_shipping_revenue += sale

print(f"Orders with free shipping: {free_shipping_count}")
print(f"Revenue from those orders: ${free_shipping_revenue:,.2f}")
```

Output:
```
Orders with free shipping: 4
Revenue from those orders: $814.70
```

The `if` inside the loop acts as a gate — only orders at or above the threshold update those accumulators.

---

### enumerate() AND range() (10:00–13:00)

**`enumerate()`** gives you both the index and the value as you iterate. Useful when you need to know the position of each item.

```python
for index, sale in enumerate(daily_sales):
    day = index + 1   # days start at 1, not 0
    print(f"Day {day}: ${sale:.2f}")
```

Output:
```
Day 1: $142.50
Day 2: $89.99
Day 3: $312.00
...
```

**`range()`** generates a sequence of numbers. Use it when you want to repeat something N times, or when you need the index to access list elements.

```python
# Repeat 5 times:
for i in range(5):
    print(f"Processing batch {i + 1}")

# Loop over indices:
for i in range(len(daily_sales)):
    print(f"Day {i + 1}: ${daily_sales[i]:.2f}")
```

In most cases, iterating directly over the list (`for sale in daily_sales`) is cleaner. Use `range()` when you specifically need the numeric index for something other than display.

---

### COMMON MISTAKES (13:00–15:30)

**Forgetting to initialize the accumulator before the loop.**

```python
# Wrong — total is not defined before the loop:
for sale in daily_sales:
    total += sale   # NameError: name 'total' is not defined

# Right:
total = 0
for sale in daily_sales:
    total += sale
```

**Indentation error — code that should be in the loop is outside it.**

```python
# Wrong — total prints after every single iteration:
for sale in daily_sales:
    total += sale
    print(f"Total so far: ${total:.2f}")   # prints 7 times

# Right — print once, after the loop:
for sale in daily_sales:
    total += sale

print(f"Final total: ${total:.2f}")   # prints once
```

The indentation level is everything. Code inside the loop (indented) runs every iteration. Code after the loop (not indented) runs once.

**Dividing by zero.** If the list might be empty, guard against it.

```python
if count > 0:
    average = total / count
else:
    average = 0
    print("No orders to average.")
```

---

### RECAP (15:30–18:00)

- `for item in collection:` — iterates over every element
- **Accumulator pattern:** initialize before the loop, update inside it
- `total += value` — shorthand for `total = total + value`
- Add an `if` inside a loop to filter — only process matching items
- `enumerate()` gives you index + value
- `range(n)` generates 0, 1, 2, … n-1
- Print results AFTER the loop, not inside it

Next video: dictionaries — storing a complete record for a customer, product, or transaction in a single variable.
