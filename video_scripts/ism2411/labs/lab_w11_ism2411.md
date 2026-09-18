# ISM2411 Lab W11: Customer Dictionary & Lookup

## YouTube Metadata

**Title:** Customer Dictionary & Lookup — Full Lab Walkthrough | ISM2411 Lab 11
**Description:**
Step-by-step, test-as-you-go walkthrough of ISM2411 Module 11 Lab. Build customers.py: a single customer dict with key access, adding/updating/deleting fields, .get() vs. bracket-notation lookup and the KeyError it avoids, iterating with .items(), a tier-discount lookup table, a list of customer dicts processed in a loop, a nested product catalog with low-stock alerts, and a region-based sales summary — the pattern behind every real CRM.

Course page: https://markumreed.github.io/ism2411/pages/week11_lab.html

**Chapters:**
0:00 — What this lab covers — the pattern behind every CRM
0:45 — Exercise 1: one customer dict, four fields
1:50 — Exercise 2: add, update, delete — watched step by step
3:20 — Exercise 3: .get() vs. bracket notation and KeyError
5:00 — Exercise 4: iterating with .items()
6:20 — Exercise 5: the tier-discount lookup table
7:40 — Exercise 6: a list of customer dicts, looped
9:00 — Exercise 7: a nested catalog and low-stock alerts
10:30 — Exercise 8: sales summarized by region
12:00 — Reflection questions
12:40 — Submission checklist

**Applies to:** ISM2411 Module 11

**Tags:** python dictionary tutorial, python dict get vs bracket, python keyerror explained, python nested dictionary, ISM2411, USF, python for business beginners

---

## How to Use This Script

**SAY** it, **DO** it, **CHECK** the exact output, **FIX** it if it doesn't match — then move to the next step. Everything builds into one file, `customers.py`.

---

## Script

### INTRO (0:00–0:45)

**SAY:** "Lab 11 — the customer dictionary. This is the pattern that underlies every real CRM and analytics workflow: a record with named fields, looked up by key instead of by position. Everything today builds toward one list of dicts you can loop over — the same shape you'll see in real business data for the rest of your career."

---

### EXERCISE 1 — One Customer (0:45–1:50)

**SAY:** "One customer, four fields, accessed by name instead of by index."

**DO:**
```python
customer = {
    "name": "Alice Chen",
    "email": "alice@example.com",
    "tier": "gold",
    "ytd_spend": 1450.00,
}

print(customer["name"])
print(customer["email"])
print(customer["tier"])
print(customer["ytd_spend"])
print(customer)
```
```bash
python3 customers.py
```

**CHECK:**
```
Alice Chen
alice@example.com
gold
1450.0
{'name': 'Alice Chen', 'email': 'alice@example.com', 'tier': 'gold', 'ytd_spend': 1450.0}
```
Compare to Module 10's list — `customer["name"]` looks up by the meaningful key `"name"`, not by a position like `customer[0]`.

---

### EXERCISE 2 — Update and Add (1:50–3:20)

**SAY:** "Three mutations, printed after each one, same discipline as last week's list exercise."

**DO:**
```python
customer["phone"] = "813-555-0199"
print(customer)

customer["tier"] = "platinum"
print(customer)

del customer["email"]
print(customer)
```
```bash
python3 customers.py
```

**CHECK:**
```
{'name': 'Alice Chen', 'email': 'alice@example.com', 'tier': 'gold', 'ytd_spend': 1450.0, 'phone': '813-555-0199'}
{'name': 'Alice Chen', 'email': 'alice@example.com', 'tier': 'platinum', 'ytd_spend': 1450.0, 'phone': '813-555-0199'}
{'name': 'Alice Chen', 'tier': 'platinum', 'ytd_spend': 1450.0, 'phone': '813-555-0199'}
```
Trace each: assigning to a key that doesn't exist yet — `customer["phone"] = ...` — *adds* a new field. Assigning to a key that already exists — `customer["tier"] = "platinum"` — *overwrites* the old value in place. `del customer["email"]` removes that key-value pair entirely — it's gone from the dict, not just emptied.

---

### EXERCISE 3 — Safe Lookup (3:20–5:00)

**SAY:** "Now look up the field we just deleted, two different ways — one that fails gracefully, one that crashes."

**DO:**
```python
email = customer.get("email", "no email on file")
print(email)

try:
    email2 = customer["email"]
except KeyError as e:
    print(f"Caught a KeyError: {e}")
```
```bash
python3 customers.py
```

**CHECK:**
```
no email on file
Caught a KeyError: 'email'
```

**SAY:** "`.get()` never crashes — if the key isn't found, it returns whatever default you gave it, `\"no email on file\"` here, instead of raising an error. Bracket notation `customer[\"email\"]` is stricter — it demands the key exist, and raises `KeyError` if it doesn't, which is why we needed `try`/`except` to catch it rather than let it crash the script."

---

### EXERCISE 4 — Iterate (5:00–6:20)

**SAY:** "Looping over a dict, two different ways — one gives you keys and values together, one gives you only keys."

**DO:**
```python
for key, value in customer.items():
    print(f"{key}: {value}")

# Without .items():
for key in customer:
    print(key)   # only the key, not the value
```
```bash
python3 customers.py
```

**CHECK:**
```
name: Alice Chen
tier: platinum
ytd_spend: 1450.0
phone: 813-555-0199
name
tier
ytd_spend
phone
```

**SAY:** "`.items()` unpacks each entry into a `(key, value)` pair in one loop variable set — `key, value`. Looping over the dict directly (`for key in customer`) only ever gives you the keys; if you wanted the values too, you'd have to look them up separately with `customer[key]` inside the loop."

---

### EXERCISE 5 — Lookup Table (6:20–7:40)

**SAY:** "A second dict, used purely as a lookup table — mapping tier names to discount rates."

**DO:**
```python
tier_discounts = {"bronze": 0, "silver": .05, "gold": .10, "platinum": .15}

discount = tier_discounts.get(customer["tier"], 0)
purchase = 200
final_price = purchase * (1 - discount)

print(f"Tier: {customer['tier']}")
print(f"Discount: {discount*100:.0f}%")
print(f"Final price: ${final_price:.2f}")
```
```bash
python3 customers.py
```

**CHECK:**
```
Tier: platinum
Discount: 15%
Final price: $170.00
```
Confirm: `customer["tier"]` is `"platinum"` after Exercise 2's update, and `200 × (1 - 0.15) = 170.00`.

**SAY:** "Notice the `.get(customer['tier'], 0)` default — if a customer somehow had a tier that's not in `tier_discounts` at all, this returns `0` instead of crashing the whole report."

---

### EXERCISE 6 — List of Dicts (7:40–9:00)

**SAY:** "Now the shape from Module 10 and Module 11 combined — a list, where every item is itself a dict."

**DO:**
```python
customers = [
    {"name": "Alice Chen", "tier": "gold"},
    {"name": "Ben Torres", "tier": "silver"},
    {"name": "Casey Nguyen", "tier": "bronze"},
]

purchase = 300
for c in customers:
    discount = tier_discounts.get(c["tier"], 0)
    final = purchase * (1 - discount)
    print(f"{c['name']} ({c['tier']}): {discount*100:.0f}% off, final ${final:.2f}")
```
```bash
python3 customers.py
```

**CHECK:**
```
Alice Chen (gold): 10% off, final $270.00
Ben Torres (silver): 5% off, final $285.00
Casey Nguyen (bronze): 0% off, final $300.00
```
Confirm each: gold `300 × 0.90 = 270.00`, silver `300 × 0.95 = 285.00`, bronze `300 × 1.00 = 300.00`.

---

### EXERCISE 7 — Nested Catalog (9:00–10:30)

**SAY:** "A dict whose *values* are themselves dicts — the nested pattern for anything with multiple sub-fields per entry, like a product catalog."

**DO:**
```python
catalog = {
    "Widget A": {"price": 9.99, "stock": 150},
    "Gadget C": {"price": 49.99, "stock": 8},
}

for product, details in catalog.items():
    if details["stock"] < 20:
        print(f"LOW STOCK: {product} — only {details['stock']} left")
```
```bash
python3 customers.py
```

**CHECK:**
```
LOW STOCK: Gadget C — only 8 left
```
Only `Gadget C` triggers the alert — `Widget A`'s stock of 150 doesn't clear the `< 20` threshold, so it never prints.

**SAY:** "Trace the access pattern: `catalog.items()` gives us `(product, details)` where `details` is itself a dict — `{'price': ..., 'stock': ...}` — so `details['stock']` reaches one level deeper than Exercise 4's flat dict."

---

### EXERCISE 8 — Sales by Region (10:30–12:00)

**SAY:** "The accumulator pattern from Module 6, but accumulating into a dict instead of a single number — a running total *per region*."

**DO:**
```python
transactions = [
    {"region": "South", "amount": 300},
    {"region": "North", "amount": 150},
    {"region": "South", "amount": 200},
]

region_totals = {}
for t in transactions:
    region = t["region"]
    region_totals[region] = region_totals.get(region, 0) + t["amount"]

for region in sorted(region_totals):
    print(f"{region}: {region_totals[region]}")
```
```bash
python3 customers.py
```

**CHECK:**
```
North: 150
South: 500
```

**SAY:** "Trace the accumulation: for the first `'South'` transaction, `region_totals.get('South', 0)` returns `0` since `'South'` isn't in the dict yet, so `region_totals['South']` becomes `0 + 300 = 300`. For `'North'`, same thing — becomes `150`. For the second `'South'` transaction, `.get('South', 0)` now returns the `300` already stored, so it becomes `300 + 200 = 500`. That `.get(key, 0)` default is what makes this pattern work without a separate 'does this key already exist' check — exactly the same role `.get()` played back in Exercise 3."

---

### REFLECTION QUESTIONS (12:00–12:40)

**SAY:** "Add these as a comment block at the very top of the file."

**DO:** Answer, 2–3 sentences each:
1. In Exercise 3 you saw the difference between `.get()` and bracket notation. When in real work would you use each one, and what's your rule of thumb for choosing?
2. Exercise 8 asked you to build a summary dictionary with a loop. What does this pattern remind you of from Excel, and why might the Python version be more useful for large datasets?

**CHECK:** Question 2's honest answer usually names a pivot table or `SUMIF` — the Python version scales to millions of rows without the spreadsheet slowing to a crawl or hitting row limits, and the logic is explicit and reviewable rather than hidden inside a formula.

---

### SUBMISSION CHECKLIST (12:40–end)

- [ ] `customers.py` — filename matches exactly, lowercase
- [ ] Exercise 1: one customer dict with 4+ fields, printed individually and as a whole
- [ ] Exercise 2: add/update/delete shown step by step
- [ ] Exercise 3: `.get()` returning a default, bracket notation's `KeyError` caught
- [ ] Exercise 4: `.items()` iteration, plus a comment on the difference without it
- [ ] Exercise 5: tier discount lookup applied to a $200 purchase
- [ ] Exercise 6: list of 3+ customer dicts processed in a loop
- [ ] Exercise 7: nested catalog with only the correct low-stock alert firing
- [ ] Exercise 8: sales summarized by region, sorted by region name
- [ ] Reflection comment block at the top of the file, both questions answered
- [ ] Pushed to GitHub in a `week11/` folder
- [ ] Repo URL submitted to Canvas
