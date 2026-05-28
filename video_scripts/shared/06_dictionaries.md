# Video 06: Dictionaries as Structured Data

## YouTube Metadata

**Title:** Python Dictionaries for Business Records — The Complete Guide | ISM2411 / ISM3232
**Description:**
A dictionary stores related fields together under a single variable — exactly how a customer record, a product entry, or a transaction works in real business data. In this video you'll learn to create dicts, read and update fields, loop over a list of records, and build a simple customer lookup system.

Dictionaries are the data structure closest to a spreadsheet row, a database record, and a JSON object — so mastering them unlocks working with real-world data sources.

**Chapters:**
0:00 — Why dictionaries exist
1:30 — Creating a dictionary
3:00 — Reading and updating fields
5:30 — Looping over a dictionary
7:30 — List of dictionaries — the record pattern
11:00 — Filtering and searching records
13:00 — Common mistakes
14:30 — Recap

**Applies to:** ISM2411 Module 11 · ISM3232 Module 6

**Tags:** python dictionary, python dict, python key value, python business data, python records, python list of dicts, python data structures, ISM2411, ISM3232, python tutorial, python beginner, python json

---

## Script

### INTRO (0:00–1:30)

A list is great for a sequence of values: Monday's sales, a list of product names, a series of order totals. But when you need to store a complete record — a customer's name, their email, their tier, their year-to-date spend — a list isn't the right tool. You'd have no idea which index holds which field.

A dictionary solves this. It stores data as named fields — keys — with associated values. Think of it as one row in a spreadsheet, where the column headers are your keys. It's the most important data structure for working with real business data, and it maps directly to JSON, database rows, and API responses.

---

### CREATING A DICTIONARY (1:30–3:00)

A dictionary is defined with curly braces. Each entry is a key-value pair, separated by a colon. Pairs are separated by commas.

```python
customer = {
    "name":         "Priya Sharma",
    "email":        "priya.sharma@example.com",
    "tier":         "Gold",
    "ytd_spend":    1840.50,
    "is_active":    True
}
```

Keys are almost always strings. Values can be any type — string, number, boolean, list, even another dictionary.

Print the whole thing:

```python
print(customer)
```

Output:
```
{'name': 'Priya Sharma', 'email': 'priya.sharma@example.com', 'tier': 'Gold', 'ytd_spend': 1840.5, 'is_active': True}
```

---

### READING AND UPDATING FIELDS (3:00–5:30)

Access a value by its key in square brackets:

```python
print(customer["name"])        # Priya Sharma
print(customer["ytd_spend"])   # 1840.5
print(customer["tier"])        # Gold
```

Update a value the same way — assign to the key:

```python
customer["ytd_spend"] += 250.00    # new purchase
customer["tier"] = "Platinum"      # tier upgrade

print(f"{customer['name']} is now {customer['tier']} with ${customer['ytd_spend']:,.2f} YTD")
```

Output: `Priya Sharma is now Platinum with $2,090.50 YTD`

Add a new field by assigning to a key that doesn't exist yet:

```python
customer["last_order_date"] = "2024-05-28"
customer["rep"] = "Dana Kim"
```

Use `.get()` when you're not sure a key exists — it returns `None` (or a default) instead of crashing:

```python
print(customer.get("loyalty_points"))           # None
print(customer.get("loyalty_points", 0))        # 0
```

---

### LOOPING OVER A DICTIONARY (5:30–7:30)

Loop over keys, values, or both:

```python
# Keys only:
for key in customer:
    print(key)

# Values only:
for value in customer.values():
    print(value)

# Both — most useful:
for key, value in customer.items():
    print(f"{key}: {value}")
```

Output of `.items()` loop:
```
name: Priya Sharma
email: priya.sharma@example.com
tier: Gold
ytd_spend: 1840.5
is_active: True
```

---

### LIST OF DICTIONARIES — THE RECORD PATTERN (7:30–11:00)

In practice, you almost never work with a single record. You work with many records — a list where each element is a dictionary.

```python
customers = [
    {"name": "Priya Sharma",   "tier": "Gold",     "ytd_spend": 1840.50, "is_active": True},
    {"name": "Marcus Thompson","tier": "Silver",    "ytd_spend":  620.00, "is_active": True},
    {"name": "Elena Vasquez",  "tier": "Bronze",    "ytd_spend":  185.75, "is_active": False},
    {"name": "Jordan Lee",     "tier": "Platinum",  "ytd_spend": 4200.00, "is_active": True},
    {"name": "Sam Okonkwo",    "tier": "Silver",    "ytd_spend":  890.25, "is_active": True},
]
```

Loop over the list, access fields from each dict:

```python
total_spend = 0
active_count = 0

for customer in customers:
    if customer["is_active"]:
        total_spend  += customer["ytd_spend"]
        active_count += 1
        print(f"{customer['name']:<20} {customer['tier']:<10} ${customer['ytd_spend']:>8,.2f}")

print(f"\nActive customers: {active_count}")
print(f"Total YTD spend:  ${total_spend:,.2f}")
print(f"Average spend:    ${total_spend / active_count:,.2f}")
```

Output:
```
Priya Sharma         Gold       $1,840.50
Marcus Thompson      Silver       $620.00
Jordan Lee           Platinum   $4,200.00
Sam Okonkwo          Silver       $890.25

Active customers: 4
Total YTD spend:  $7,550.75
Average spend:    $1,887.69
```

---

### FILTERING AND SEARCHING (11:00–13:00)

Find all Gold-tier active customers:

```python
gold_customers = []

for customer in customers:
    if customer["tier"] == "Gold" and customer["is_active"]:
        gold_customers.append(customer["name"])

print(f"Gold tier: {gold_customers}")
```

Find the customer with the highest spend:

```python
top_customer = customers[0]

for customer in customers:
    if customer["ytd_spend"] > top_customer["ytd_spend"]:
        top_customer = customer

print(f"Top spender: {top_customer['name']} — ${top_customer['ytd_spend']:,.2f}")
```

Output: `Top spender: Jordan Lee — $4,200.00`

Look up a customer by name:

```python
def find_customer(name, records):
    for record in records:
        if record["name"] == name:
            return record
    return None

result = find_customer("Marcus Thompson", customers)
if result:
    print(f"Found: {result}")
else:
    print("Customer not found.")
```

---

### COMMON MISTAKES (13:00–14:30)

**KeyError — accessing a key that doesn't exist.**

```python
# Wrong — crashes if "points" key doesn't exist:
print(customer["points"])   # KeyError

# Right — use .get() with a default:
print(customer.get("points", 0))
```

**Confusing list index with dict key.**

```python
customer = {"name": "Priya", "tier": "Gold"}

# Wrong — dicts don't have numeric indices (usually):
print(customer[0])   # KeyError

# Right — use the key:
print(customer["name"])
```

**Modifying a dictionary while iterating over it.** Don't add or remove keys inside a `for key in dict:` loop — iterate over a copy or collect changes and apply after.

---

### RECAP (14:30–15:00)

- `{"key": value}` — create a dictionary
- `d["key"]` — read a value
- `d["key"] = new_value` — update or add a field
- `d.get("key", default)` — safe read, no crash if key missing
- `d.items()` — iterate over key-value pairs
- List of dicts — one dict per record, list holds all records
- Loop + if inside the loop = filter records

Next video: functions — wrapping reusable logic in a named block so you can call it from anywhere.
