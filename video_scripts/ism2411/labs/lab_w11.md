# ISM2411 Lab W11: Customer Dictionary & Lookup

## YouTube Metadata

**Title:** Customer Dictionary & Lookup — Lab Walkthrough | ISM2411 Lab 11
**Description:**
Walkthrough of ISM2411 Module 11 Lab. We build customer records as dictionaries, use tier-based lookups, handle missing keys safely with .get(), and loop over a list of customer dicts to generate a summary report.

**Chapters:**
0:00 — What we're building
0:45 — A customer record as a dictionary
2:30 — Safe key access: .get() vs bracket notation
4:30 — A list of customer dictionaries
6:00 — Building a summary dictionary with a loop
8:30 — Submission checklist

**Applies to:** ISM2411 Module 11

**Tags:** python dictionaries, python dict get, python customer records, python list of dicts, ISM2411, USF, python dictionary tutorial

---

## Script

### INTRO (0:00–0:45)

Lab 11 — Customer Dictionary and Lookup. Dictionaries are Python's key-value store. Every database row, every JSON response, every CRM record maps directly onto this structure. By the end we'll have a working customer lookup system and summary report.

---

### A CUSTOMER RECORD (0:45–2:30)

Create `module11/customers.py`:

```python
# customers.py

customer = {
    "id":       1001,
    "name":     "Acme Corp",
    "email":    "billing@acme.com",
    "tier":     "Gold",
    "balance":  4750.00,
    "active":   True
}

# Access by key
print(customer["name"])       # Acme Corp
print(customer["balance"])    # 4750.0

# Modify
customer["balance"] += 250.00
print(customer["balance"])    # 5000.0

# Add a new key
customer["region"] = "Southeast"

# Delete a key
del customer["email"]
```

Dictionaries are mutable — you can add, modify, and delete keys after creation.

---

### .GET() VS BRACKET NOTATION (2:30–4:30)

Now try to access the key we just deleted:

```python
# Bracket notation — crashes if key doesn't exist
print(customer["email"])   # KeyError: 'email'

# .get() — returns None (or a default) if key doesn't exist
print(customer.get("email"))                    # None
print(customer.get("email", "no email on file")) # no email on file
```

Rule of thumb: use `.get()` whenever the key might not be present. Use bracket notation when you know the key must be there — the crash is a useful signal if something's wrong.

---

### LIST OF CUSTOMER DICTIONARIES (4:30–6:00)

```python
customers = [
    {"name": "Acme Corp",      "tier": "Gold",   "balance": 5000.00},
    {"name": "Beta LLC",       "tier": "Silver", "balance": 1200.00},
    {"name": "Gamma Inc",      "tier": "Gold",   "balance": 8750.00},
    {"name": "Delta Partners", "tier": "Bronze", "balance": 450.00},
    {"name": "Echo Co",        "tier": "Silver", "balance": 2100.00},
]

# Loop and print formatted output
for c in customers:
    status = "⚠ Review" if c["balance"] > 5000 else "OK"
    print(f"{c['name']:<18} {c['tier']:<8} ${c['balance']:>8,.2f}  {status}")
```

This is the list-of-dicts pattern — the same structure pandas uses internally.

---

### SUMMARY DICTIONARY WITH A LOOP (6:00–8:30)

Exercise 8 asks you to build a summary dict counting customers per tier:

```python
# Initialize with known tiers
tier_counts = {"Gold": 0, "Silver": 0, "Bronze": 0}
tier_totals = {"Gold": 0.0, "Silver": 0.0, "Bronze": 0.0}

for c in customers:
    tier = c["tier"]
    tier_counts[tier] += 1
    tier_totals[tier] += c["balance"]

print("\nTier Summary:")
for tier in tier_counts:
    avg = tier_totals[tier] / tier_counts[tier] if tier_counts[tier] > 0 else 0
    print(f"  {tier:<8} {tier_counts[tier]} customers  avg balance ${avg:,.2f}")
```

This is the GroupBy pattern in pure Python — you'll recreate it with pandas in Module 13.

---

### SUBMISSION CHECKLIST (8:30–10:00)

- Single customer dict with add/modify/delete demonstrated
- `.get()` with default used for missing key
- List of customer dicts with loop and formatted output
- Summary dict built with a loop (no Counter or groupby)
- Exercise responses written
- GitHub commit with descriptive message, URL pasted to Canvas
