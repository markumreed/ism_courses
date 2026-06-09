# Video 15: Lists & Tuples

## YouTube Metadata

**Title:** Python Lists & Tuples for Business Data | ISM2411
**Description:**
Lists are Python's most versatile data structure — ordered, mutable collections you'll use constantly for sequences of sales figures, product names, customer IDs, and transaction records. Tuples are their immutable counterparts, ideal for fixed records like coordinates, date ranges, or table rows. Learn both with practical business examples.

Course page: https://markumreed.github.io/ism2411/pages/week10_lecture.html

**Chapters:**
0:00 — Lists vs tuples — which and when
1:30 — Creating and indexing lists
4:00 — List methods: append, remove, sort
7:00 — Slicing
9:30 — Looping over lists (the accumulator pattern)
12:00 — Tuples — immutable sequences
14:00 — Recap

**Applies to:** ISM2411 Module 10

**Tags:** python lists, python tuples, python list methods, python append, python sort, python slicing, python data structures, ISM2411, python tutorial, python business data

---

## Script

### INTRO (0:00–1:30)

You've worked with single values — one price, one customer name, one order total. But real business data is collections — a week's worth of daily sales, a catalog of product names, a list of customer IDs in a loyalty tier. Python's list is the right tool for all of these. And its close cousin, the tuple, handles fixed-size records that shouldn't change.

---

### CREATING AND INDEXING (1:30–4:00)

A list is created with square brackets. Elements are separated by commas.

```python
daily_sales = [142.50, 89.99, 312.00, 47.25, 203.80, 156.40, 78.95]
products    = ["Laptop Bag", "USB-C Hub", "Wireless Mouse", "Monitor Stand"]
is_in_stock = [True, True, False, True]
```

Lists can hold any type — and even mix types — but in practice, keep one type per list.

Access elements by index. Python lists are **zero-indexed** — the first element is index 0.

```python
print(daily_sales[0])    # 142.50 — first element
print(daily_sales[6])    # 78.95  — seventh (last) element
print(daily_sales[-1])   # 78.95  — last element (negative index counts from end)
print(daily_sales[-2])   # 156.40 — second to last
```

The length of a list:
```python
print(len(daily_sales))   # 7
```

---

### LIST METHODS (4:00–7:00)

Lists are **mutable** — you can add, remove, and change elements.

**append()** — add an element to the end:
```python
daily_sales.append(220.00)
print(daily_sales)   # [..., 78.95, 220.00]
print(len(daily_sales))   # 8
```

**insert()** — add at a specific position:
```python
daily_sales.insert(0, 99.99)   # insert at beginning
```

**remove()** — remove the first occurrence of a value:
```python
products.remove("Wireless Mouse")
print(products)   # ["Laptop Bag", "USB-C Hub", "Monitor Stand"]
```

**pop()** — remove and return element at index (default: last):
```python
last_sale = daily_sales.pop()    # removes last, returns it
print(last_sale)
```

**sort()** — sort in place:
```python
daily_sales.sort()                    # ascending
daily_sales.sort(reverse=True)        # descending
print(daily_sales)
```

**sorted()** — returns a new sorted list, original unchanged:
```python
original = [312.00, 89.99, 47.25, 203.80]
ranked   = sorted(original, reverse=True)
print(original)   # unchanged
print(ranked)     # sorted copy
```

---

### SLICING (7:00–9:30)

A slice extracts a portion of a list using `[start:stop]` — includes `start`, excludes `stop`.

```python
week_sales = [142.50, 89.99, 312.00, 47.25, 203.80, 156.40, 78.95]

first_three   = week_sales[0:3]    # [142.50, 89.99, 312.00]
middle        = week_sales[2:5]    # [312.00, 47.25, 203.80]
last_two      = week_sales[-2:]    # [156.40, 78.95]
all_but_first = week_sales[1:]     # skip first
all_but_last  = week_sales[:-1]    # skip last

print(f"Best day was Monday: ${first_three[0]:.2f}")
```

Slices return a new list — the original is not changed.

---

### LOOPING WITH THE ACCUMULATOR PATTERN (9:30–12:00)

Process every element with a `for` loop:

```python
week_sales = [142.50, 89.99, 312.00, 47.25, 203.80, 156.40, 78.95]

total   = 0
count   = 0
max_day = 0

for sale in week_sales:
    total += sale
    count += 1
    if sale > max_day:
        max_day = sale

avg = total / count

print(f"Days:    {count}")
print(f"Total:   ${total:,.2f}")
print(f"Average: ${avg:.2f}")
print(f"Best:    ${max_day:.2f}")
```

Use `enumerate()` to get index + value when you need the day number:

```python
days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

for i, sale in enumerate(week_sales):
    flag = " ← best!" if sale == max_day else ""
    print(f"{days[i]}: ${sale:.2f}{flag}")
```

---

### TUPLES (12:00–14:00)

A tuple is like a list but **immutable** — once created, it cannot be changed.

```python
# Created with parentheses (or just commas):
product_record  = ("Laptop Bag", 49.99, 12, True)
date_range      = ("2024-01-01", "2024-12-31")
rgb_color       = (75, 0, 130)

# Access same as lists:
print(product_record[0])    # Laptop Bag
print(product_record[1])    # 49.99

# This raises a TypeError — tuples are immutable:
# product_record[1] = 54.99
```

**When to use a tuple vs a list:**
- **List** — ordered collection of similar items that may change: sales figures, product names, customer IDs
- **Tuple** — fixed record with named positions: a (name, price, qty) product entry, a (lat, lon) coordinate, a database row

Tuples as function return values — Python can return multiple values by packing them into a tuple:

```python
def sales_summary(sales):
    total = sum(sales)
    avg   = total / len(sales)
    peak  = max(sales)
    return total, avg, peak   # returns a tuple

total, avg, peak = sales_summary(week_sales)   # unpacking
print(f"Total: ${total:.2f}, Avg: ${avg:.2f}, Peak: ${peak:.2f}")
```

This is called **tuple unpacking** — Python assigns each value to the corresponding variable name.

---

### RECAP (14:00–15:00)

- `[a, b, c]` — create a list; `(a, b, c)` — create a tuple
- Zero-indexed: `lst[0]` is first, `lst[-1]` is last
- `append()`, `remove()`, `sort()` — mutate the list
- `sorted()` — returns a new sorted list
- Slicing `lst[start:stop]` — extract a portion
- Loop with `for item in lst:`, use `enumerate()` for index
- Tuples are immutable — use for fixed records, function returns
- Tuple unpacking: `a, b, c = my_tuple`

Next module: working with files and CSVs — loading real business data from disk.
