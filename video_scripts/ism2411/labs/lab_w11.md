# ISM2411 Lab 11 Code-Along — Customer Dictionary & Lookup

**Build one script, `customers.py`, that stores customer records as dictionaries, looks values up safely, applies a tier discount from a lookup table, and turns a list of transactions into a summary.**

Type along, one exercise at a time. Run the file after each one and compare with the **You should see** block. Every output below is a real run of the code shown.

| | |
|---|---|
| **File** | `ism2411/week11/customers.py`, one file holding all 8 exercises |
| **Time** | About one lab session |
| **Builds on** | Lists and the accumulator pattern (Module 10), `for` loops and `if` (Modules 5–6), f-strings (Module 3), `try`/`except` (Lab 10, Exercise 5), the GitHub workflow (Module 8) |
| **New this week** | Dictionaries: key access, add/update/delete, `.get()`, `.items()`, lookup tables, nested dictionaries, a list of dictionaries |
| **You submit** | Your GitHub repo URL in Canvas |

### Contents

0. [Five-minute refresher](#0-five-minute-refresher)
1. [Set up the file](#1-set-up-the-file)
2. [Exercises 1–4: one customer record](#exercise-1--one-customer)
3. [Exercise 5: a lookup table](#exercise-5--lookup-table)
4. [Exercises 6–8: many records](#exercise-6--list-of-dicts)
5. [The finished file and full run](#the-finished-file)
6. [Submit](#submit)
7. [When something breaks](#when-something-breaks)

---

## 0. Five-minute refresher

*From the reading and lecture.* Everything the lab uses:

```python
customer = {"name": "Alice", "tier": "gold", "ytd_spend": 12400}

customer["name"]                  # 'Alice'     look up a value by its key
customer["phone"] = "555-0100"    # add: assign to a key that isn't there yet
customer["tier"] = "platinum"     # update: assign to a key that is there
del customer["phone"]             # delete a key and its value

customer.get("email", "N/A")      # 'N/A'       safe lookup, no KeyError
for key, value in customer.items():   # both the key and the value
    print(key, value)
for key in customer:              # a plain loop gives the keys only
    print(key)
```

**List or dictionary?** A list says *here are five products, in order*, and you reach an item by its position. A dictionary says *here is one customer and everything I know about them*, and you reach a value by its label. `customer["email"]` still works if someone adds a field. `row[6]` silently breaks the moment someone reorders the columns.

> **The rule this whole lab turns on:** bracket notation, `customer["email"]`, crashes with a `KeyError` if the key isn't there. `.get("email", default)` hands back the default instead. Exercise 3 shows both side by side.

---

## 1. Set up the file

Open VS Code's terminal (**View → Terminal**) and go to your course repo:

```bash
cd ~/ism2411
git pull
mkdir week11
code week11/customers.py
```

`git pull` brings down anything you changed on github.com, so your next push isn't rejected.

Paste this header at the top of the file. The lab requires your two reflection answers in a comment block at the top, so leave the placeholders now and fill them in at the end.

```python
# customers.py
# Author: [Your Name]
# Module 11 Lab: Customer Dictionary & Lookup
#
# Reflection 1: When I would use .get() and when I would use bracket notation:
#   [2-3 sentences]
#
# Reflection 2: What the Exercise 8 summary reminds me of in Excel, and why
# Python is more useful for large datasets:
#   [2-3 sentences]
```

To run the file, use this from inside `~/ism2411`. In Ubuntu on Windows and on a Mac, the command is `python3`.

```bash
python3 week11/customers.py
```

Each exercise starts with a `print("--- Exercise N ---")` line, so the output is easy to read and easy to grade.

> **One file, top to bottom.** Exercises 1–5 all work on the same `customer`. Exercise 2 changes it, and Exercises 3–5 see those changes. Keep the exercises in order.

---

## Exercise 1 — One customer

**Goal:** create one customer with at least four fields (`name`, `email`, `tier`, `ytd_spend`), print each field on its own line using key access, then print the whole dictionary.

```python
# --- Exercise 1: One customer ---
print("--- Exercise 1 ---")
customer = {
    "name": "Alice",
    "email": "alice@example.com",
    "tier": "gold",
    "ytd_spend": 12400,
}
print(customer["name"])
print(customer["email"])
print(customer["tier"])
print(customer["ytd_spend"])
print(customer)
```

**You should see:**

```text
--- Exercise 1 ---
Alice
alice@example.com
gold
12400
{'name': 'Alice', 'email': 'alice@example.com', 'tier': 'gold', 'ytd_spend': 12400}
```

**Why:**

- Curly braces make a dictionary. Each entry is a **key**, a colon, and a **value**, and commas separate the entries. Writing one entry per line is optional, but it reads like a record card.
- `customer["name"]` asks for the value stored under the key `"name"`. The key goes in quotes because it is a string.
- Printing the whole dictionary shows every key and value. Python prints strings in single quotes, whichever quotes you typed.

---

## Exercise 2 — Update and add

**Goal:** add a `phone` field, change the tier to `"platinum"`, delete `email` with `del`, and print the dictionary after each step.

```python
# --- Exercise 2: Update and add ---
print("--- Exercise 2 ---")
customer["phone"] = "813-555-0142"
print(customer)
customer["tier"] = "platinum"
print(customer)
del customer["email"]
print(customer)
```

**You should see:**

```text
--- Exercise 2 ---
{'name': 'Alice', 'email': 'alice@example.com', 'tier': 'gold', 'ytd_spend': 12400, 'phone': '813-555-0142'}
{'name': 'Alice', 'email': 'alice@example.com', 'tier': 'platinum', 'ytd_spend': 12400, 'phone': '813-555-0142'}
{'name': 'Alice', 'tier': 'platinum', 'ytd_spend': 12400, 'phone': '813-555-0142'}
```

**Why:**

- **Adding and updating are the same line.** If the key doesn't exist, assignment creates it, and that's why `phone` appears at the end. If the key exists, assignment overwrites the value, and that's why `tier` changes in place. There is no special "add" method.
- Keys are unique. A dictionary can't hold two `"tier"` entries, so the old value is gone.
- `del customer["email"]` removes the key and its value. The lecture also shows `customer.pop("email", None)`, which deletes and hands back the old value.

---

## Exercise 3 — Safe lookup

**Goal:** look up the `email` you just deleted with `.get()` and the default `"no email on file"`. Then look it up with bracket notation, and catch the `KeyError` with `try`/`except`.

```python
# --- Exercise 3: Safe lookup ---
print("--- Exercise 3 ---")
print(customer.get("email", "no email on file"))
try:
    print(customer["email"])
except KeyError as error:
    print("KeyError caught:", error)
```

**You should see:**

```text
--- Exercise 3 ---
no email on file
KeyError caught: 'email'
```

**Why:**

- `.get("email", "no email on file")` checks for the key. It isn't there, so you get the default and the program carries on.
- `customer["email"]` insists the key exists. It doesn't, so Python raises a `KeyError`. The `try`/`except` is the same pattern as Lab 10's tuple exercise: Python runs the `try` block, and when that error happens it jumps to `except` instead of crashing. `as error` keeps the message, which is just the missing key, `'email'`.

> **Try it without `try`.** Comment out the `try:` and `except` lines, unindent `print(customer["email"])`, and run the file. The program stops on that line with `KeyError: 'email'`, and nothing after it runs. Put it back before you move on.

**Rule of thumb (you'll need it for Reflection 1):** use `.get()` for fields that may legitimately be missing, like an optional phone number or a column some CSV rows leave blank. Use brackets when the key *must* be there. If it isn't, a crash tells you something is wrong with the data.

---

## Exercise 4 — Iterate

**Goal:** print every field as `key: value` with a `for` loop and `.items()`. Then loop without `.items()` and explain the difference in a comment.

```python
# --- Exercise 4: Iterate ---
print("--- Exercise 4 ---")
for key, value in customer.items():
    print(f"{key}: {value}")
for key in customer:
    print(key)
# Without .items(), the loop gives only the keys. To get a value you have
# to look it up yourself with customer[key].
```

**You should see:**

```text
--- Exercise 4 ---
name: Alice
tier: platinum
ytd_spend: 12400
phone: 813-555-0142
name
tier
ytd_spend
phone
```

**Why:**

- `.items()` hands the loop one `(key, value)` pair at a time, and `for key, value in ...` unpacks each pair into two variables. This is the pattern you'll use most. Memorize it.
- A plain `for key in customer:` loop gives **keys only**. You can still reach the value with `customer[key]`, but `.items()` saves the lookup.
- The order is the order the keys were added. `email` is gone, and `phone` comes last because Exercise 2 added it last. Python keeps that order, but don't build logic on it. If order matters, sort explicitly, as in Exercise 8.

---

## Exercise 5 — Lookup table

**Goal:** build `tier_discounts`, look up the discount for the customer's current tier with `.get()` and a default of `0`, and work out the price of a $200 purchase. Print the tier, the discount rate and the final price.

A **lookup table** is a dictionary that maps one value to another. It replaces an `if`/`elif` chain: adding a tier is one new entry, not another branch. It is Python's version of a VLOOKUP.

```python
# --- Exercise 5: Lookup table ---
print("--- Exercise 5 ---")
tier_discounts = {"bronze": 0, "silver": 0.05, "gold": 0.10, "platinum": 0.15}
purchase = 200
discount_rate = tier_discounts.get(customer["tier"], 0)
final_price = purchase * (1 - discount_rate)
print(f"Tier: {customer['tier']}")
print(f"Discount: {discount_rate * 100:.0f}%")
print(f"Final price: ${final_price:.2f}")
```

**You should see:**

```text
--- Exercise 5 ---
Tier: platinum
Discount: 15%
Final price: $170.00
```

**Why:**

- The tier is `"platinum"` because Exercise 2 changed it. The lookup finds `0.15`.
- `1 - discount_rate` is the share the customer pays: 85% of $200 is $170.
- `.get(..., 0)` means a tier that isn't in the table gets no discount instead of a crash. The lab page writes the rates as `.05`, `.10` and `.15`. That's the same number as `0.05`, and the leading zero is easier to read.
- `{discount_rate * 100:.0f}` turns `0.15` into `15`, and `:.2f` prints money with two decimals.

> **Quotes inside an f-string.** Write `f"Tier: {customer['tier']}"`, with single quotes around the key inside the double-quoted string. Python 3.12 and newer also accept double quotes there, but Python 3.11 and older stop with `SyntaxError: f-string: unmatched '['`. Single quotes work everywhere.

---

## Exercise 6 — List of dicts

**Goal:** build a list of at least three customers with different tiers. Loop through it and print each customer's name, tier and discount on a $300 purchase, using `tier_discounts`.

A **list of dictionaries** is a table in Python: each dictionary is a row, and each key is a column name. It's exactly what you'll get when you read a CSV file in Module 12.

```python
# --- Exercise 6: List of dicts ---
print("--- Exercise 6 ---")
customers = [
    {"name": "Bob", "tier": "silver", "ytd_spend": 3200},
    {"name": "Carol", "tier": "gold", "ytd_spend": 8750},
    {"name": "David", "tier": "bronze", "ytd_spend": 450},
]
for record in customers:
    rate = tier_discounts.get(record["tier"], 0)
    discount = 300 * rate
    print(f"{record['name']} ({record['tier']}): ${discount:.2f} off a $300 purchase")
```

**You should see:**

```text
--- Exercise 6 ---
Bob (silver): $15.00 off a $300 purchase
Carol (gold): $30.00 off a $300 purchase
David (bronze): $0.00 off a $300 purchase
```

**Why:**

- Each pass of the loop puts one whole dictionary in `record`, so `record["tier"]` is *that* customer's tier.
- The same `tier_discounts` table from Exercise 5 serves every customer. That's the payoff of a lookup table: one line handles every tier.
- The page asks for the **discount amount**, so this prints what comes off the price, not the final price.

---

## Exercise 7 — Nested catalog

**Goal:** build the page's product catalog, a dictionary whose values are dictionaries. Loop through it and print a `LOW STOCK` alert for any product with stock below 20.

```python
# --- Exercise 7: Nested catalog ---
print("--- Exercise 7 ---")
catalog = {
    "Widget A": {"price": 9.99, "stock": 150},
    "Gadget C": {"price": 49.99, "stock": 8},
}
for name, details in catalog.items():
    if details["stock"] < 20:
        print(f"LOW STOCK: {name} — only {details['stock']} left")
```

**You should see:**

```text
--- Exercise 7 ---
LOW STOCK: Gadget C — only 8 left
```

**Why:**

- The outer keys are product names, and each value is that product's record. `.items()` gives you both: `name` is `"Gadget C"` and `details` is `{"price": 49.99, "stock": 8}`.
- `details["stock"]` reaches into the inner dictionary. Outside a loop you'd chain the brackets: `catalog["Gadget C"]["stock"]` is `8`.
- Only Gadget C prints, as the page expects. Widget A has 150.

---

## Exercise 8 — Sales by region

**Goal:** turn a list of transactions into a summary dictionary of total sales per region, using a loop and `.get(region, 0)`. Print the summary sorted by region name.

This is the accumulator pattern from Lab 10, with a dictionary as the accumulator: **start empty, loop, and add each amount to its region's running total.**

```python
# --- Exercise 8: Sales by region ---
print("--- Exercise 8 ---")
transactions = [
    {"region": "South", "amount": 300},
    {"region": "North", "amount": 150},
    {"region": "South", "amount": 200},
]
sales_by_region = {}
for sale in transactions:
    region = sale["region"]
    sales_by_region[region] = sales_by_region.get(region, 0) + sale["amount"]
print(sales_by_region)
for region in sorted(sales_by_region):
    print(f"{region}: {sales_by_region[region]}")
```

**You should see:**

```text
--- Exercise 8 ---
{'South': 500, 'North': 150}
North: 150
South: 500
```

**Why:**

- **Trace it.** First sale: `South` isn't in the summary yet, so `.get` gives `0`, and `0 + 300` stores `300`. Second sale: `North` gets `0 + 150`. Third sale: `South` is there now, so `.get` gives `300`, and `300 + 200` stores `500`.
- Without `.get`, the first `sales_by_region["South"] += ...` crashes with `KeyError: 'South'`, because there is nothing to add to yet. `.get(region, 0)` is what makes the first sale for each region work.
- `print(sales_by_region)` shows the regions in the order they first appeared: South, then North. That's the page's sample (*South: 500, North: 150*). The task asks for the summary **sorted by region name**, so `sorted(sales_by_region)` gives the keys alphabetically and North prints first.
- Add a fourth transaction, like `{"region": "West", "amount": 75}`, and the loop handles it with no new code. That's the answer to Reflection 2: this is a SUMIF or a PivotTable, and it runs the same on three rows or three million.

> **Know this one by hand.** It is the same loop-and-accumulate shape as Lab 10's Exercises 7 and 8, with a dictionary where the list was. No built-in does the work: one loop updates one running total per key.

---

## The finished file

<details>
<summary><b>Complete <code>week11/customers.py</code></b> (check yours against it)</summary>

```python
# customers.py
# Author: [Your Name]
# Module 11 Lab: Customer Dictionary & Lookup
#
# Reflection 1: When I would use .get() and when I would use bracket notation:
#   [2-3 sentences]
#
# Reflection 2: What the Exercise 8 summary reminds me of in Excel, and why
# Python is more useful for large datasets:
#   [2-3 sentences]

# --- Exercise 1: One customer ---
print("--- Exercise 1 ---")
customer = {
    "name": "Alice",
    "email": "alice@example.com",
    "tier": "gold",
    "ytd_spend": 12400,
}
print(customer["name"])
print(customer["email"])
print(customer["tier"])
print(customer["ytd_spend"])
print(customer)

# --- Exercise 2: Update and add ---
print("--- Exercise 2 ---")
customer["phone"] = "813-555-0142"
print(customer)
customer["tier"] = "platinum"
print(customer)
del customer["email"]
print(customer)

# --- Exercise 3: Safe lookup ---
print("--- Exercise 3 ---")
print(customer.get("email", "no email on file"))
try:
    print(customer["email"])
except KeyError as error:
    print("KeyError caught:", error)

# --- Exercise 4: Iterate ---
print("--- Exercise 4 ---")
for key, value in customer.items():
    print(f"{key}: {value}")
for key in customer:
    print(key)
# Without .items(), the loop gives only the keys. To get a value you have
# to look it up yourself with customer[key].

# --- Exercise 5: Lookup table ---
print("--- Exercise 5 ---")
tier_discounts = {"bronze": 0, "silver": 0.05, "gold": 0.10, "platinum": 0.15}
purchase = 200
discount_rate = tier_discounts.get(customer["tier"], 0)
final_price = purchase * (1 - discount_rate)
print(f"Tier: {customer['tier']}")
print(f"Discount: {discount_rate * 100:.0f}%")
print(f"Final price: ${final_price:.2f}")

# --- Exercise 6: List of dicts ---
print("--- Exercise 6 ---")
customers = [
    {"name": "Bob", "tier": "silver", "ytd_spend": 3200},
    {"name": "Carol", "tier": "gold", "ytd_spend": 8750},
    {"name": "David", "tier": "bronze", "ytd_spend": 450},
]
for record in customers:
    rate = tier_discounts.get(record["tier"], 0)
    discount = 300 * rate
    print(f"{record['name']} ({record['tier']}): ${discount:.2f} off a $300 purchase")

# --- Exercise 7: Nested catalog ---
print("--- Exercise 7 ---")
catalog = {
    "Widget A": {"price": 9.99, "stock": 150},
    "Gadget C": {"price": 49.99, "stock": 8},
}
for name, details in catalog.items():
    if details["stock"] < 20:
        print(f"LOW STOCK: {name} — only {details['stock']} left")

# --- Exercise 8: Sales by region ---
print("--- Exercise 8 ---")
transactions = [
    {"region": "South", "amount": 300},
    {"region": "North", "amount": 150},
    {"region": "South", "amount": 200},
]
sales_by_region = {}
for sale in transactions:
    region = sale["region"]
    sales_by_region[region] = sales_by_region.get(region, 0) + sale["amount"]
print(sales_by_region)
for region in sorted(sales_by_region):
    print(f"{region}: {sales_by_region[region]}")
```

</details>

**Full run** of `python3 week11/customers.py`:

```text
--- Exercise 1 ---
Alice
alice@example.com
gold
12400
{'name': 'Alice', 'email': 'alice@example.com', 'tier': 'gold', 'ytd_spend': 12400}
--- Exercise 2 ---
{'name': 'Alice', 'email': 'alice@example.com', 'tier': 'gold', 'ytd_spend': 12400, 'phone': '813-555-0142'}
{'name': 'Alice', 'email': 'alice@example.com', 'tier': 'platinum', 'ytd_spend': 12400, 'phone': '813-555-0142'}
{'name': 'Alice', 'tier': 'platinum', 'ytd_spend': 12400, 'phone': '813-555-0142'}
--- Exercise 3 ---
no email on file
KeyError caught: 'email'
--- Exercise 4 ---
name: Alice
tier: platinum
ytd_spend: 12400
phone: 813-555-0142
name
tier
ytd_spend
phone
--- Exercise 5 ---
Tier: platinum
Discount: 15%
Final price: $170.00
--- Exercise 6 ---
Bob (silver): $15.00 off a $300 purchase
Carol (gold): $30.00 off a $300 purchase
David (bronze): $0.00 off a $300 purchase
--- Exercise 7 ---
LOW STOCK: Gadget C — only 8 left
--- Exercise 8 ---
{'South': 500, 'North': 150}
North: 150
South: 500
```

### Now write your reflection

Replace the two `[2-3 sentences]` placeholders at the top with your own answers:

1. In Exercise 3 you saw the difference between `.get()` and bracket notation. When in real work would you use each one, and what's your rule of thumb for choosing?
2. Exercise 8 asked you to build a summary dictionary with a loop. What does this pattern remind you of from Excel, and why might the Python version be more useful for large datasets?

---

## Submit

From inside `~/ism2411`:

```bash
git status
git add week11/
git commit -m "add module 11 customer dictionary lab: exercises 1-8 and reflection"
git push
```

Then open your repo on github.com, click into `week11/`, and confirm `customers.py` is there with your reflection at the top.

**Canvas:** paste your GitHub repository URL. That is the only thing you submit. Don't upload the file.

- [ ] `week11/customers.py` is in your `ism2411` repo on github.com
- [ ] It runs from top to bottom with no errors and includes Exercises 1–8
- [ ] The reflection comment block at the top is filled in, not placeholders
- [ ] The commit message describes the change
- [ ] The repo URL is pasted in Canvas

---

## When something breaks

| You see | Cause | Fix |
|---|---|---|
| `KeyError: 'email'` and the program stops | Bracket notation asked for a key that isn't there, outside a `try` | Use `.get("email", "no email on file")`, or put the lookup under `try:` with `except KeyError` |
| `KeyError: 'South'` in Exercise 8 | `sales_by_region[region] += ...` adds to a key that doesn't exist yet | `sales_by_region[region] = sales_by_region.get(region, 0) + sale["amount"]` |
| `NameError: name 'name' is not defined` | The key has no quotes: `customer[name]` | `customer["name"]` |
| `TypeError: string indices must be integers, not 'str'` | A plain `for` loop over a dictionary gives keys, which are strings, and then the code indexes the string | Loop with `for name, details in catalog.items():` |
| `TypeError: 'builtin_function_or_method' object is not subscriptable` | `.get` with square brackets: `customer.get["email"]` | `.get` is a method, so it takes parentheses: `customer.get("email")` |
| `SyntaxError: f-string: unmatched '['` | Double quotes around a key inside a double-quoted f-string, on Python 3.11 or older | Single quotes inside: `f"{customer['tier']}"` |
| Exercise 5 prints `Discount: 0%` | The tier doesn't match a key exactly (`"Platinum"` vs `"platinum"`), so `.get` returns the default | Match the spelling and capitals in `tier_discounts` |
| `can't open file ... No such file or directory` | The terminal isn't in `~/ism2411`, or the folder is named differently | `cd ~/ism2411`, then `ls week11` |
| `git push` is rejected | You edited something on github.com | `git pull`, then `git push` |

> **`.get` can hide a typo.** The Exercise 5 row above has no error message at all, and that's what makes it dangerous. The default you chose is applied silently. When a `.get()` result looks wrong, print the key you looked up.

### Lecture discussion questions to try

*From the lecture.* If you finish early, try these with your new script:

- **Column numbers vs keys.** A script reads the email as `row[7]`. Why is that fragile, and how would a dictionary fix it?
- **Tuples or dictionaries?** A colleague stores the catalog as `[("Widget A", 9.99, 150), ...]`. What do you gain and lose compared with Exercise 7's dictionaries?
- **Lookup table or `if`/`elif`?** Name a business rule, such as shipping zones or tax codes, where Exercise 5's pattern would save real code.
- **Does order matter?** When would you sort a dictionary's output, as Exercise 8 does, and when doesn't it matter?
