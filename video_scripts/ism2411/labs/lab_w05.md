# ISM2411 Lab W05: Tiered Discount Calculator

## YouTube Metadata

**Title:** Tiered Discount Calculator — Lab Walkthrough | ISM2411 Lab 05
**Description:**
Walkthrough of ISM2411 Module 5 Lab. We build a tiered discount calculator using if/elif/else to apply different discount rates based on order size — the same logic used in real pricing systems.

Course page: https://markumreed.github.io/ism2411/pages/week05_lab.html

**Chapters:**
0:00 — What we're building
0:45 — Writing the tiered if/elif/else logic
3:30 — Tracing a value through the tiers
5:30 — Combining conditions with and
7:30 — Submission checklist

**Applies to:** ISM2411 Module 05

**Tags:** python if elif else, python conditionals, python discount calculator, python business logic, ISM2411, USF, python tiered pricing

---

## Script

### INTRO (0:00–0:45)

Lab 5 — Tiered Discount Calculator. We're using if/elif/else to apply discount tiers: small orders get no discount, medium orders get 10%, large orders get 20%. This is the core pattern behind real pricing engines, tax brackets, and shipping rules. Save as `module05/discount.py`.

---

### THE TIERED LOGIC (0:45–3:30)

```python
# discount.py

order_total = float(input("Enter order total: $"))

if order_total >= 1000:
    discount_rate = 0.20
    tier = "Premium (20%)"
elif order_total >= 500:
    discount_rate = 0.10
    tier = "Standard (10%)"
elif order_total >= 100:
    discount_rate = 0.05
    tier = "Basic (5%)"
else:
    discount_rate = 0.00
    tier = "No discount"

discount_amount  = order_total * discount_rate
final_price      = order_total - discount_amount

print(f"\nOrder total:    ${order_total:,.2f}")
print(f"Tier:           {tier}")
print(f"Discount:       ${discount_amount:,.2f}")
print(f"Final price:    ${final_price:,.2f}")
```

Run it with different values:
- `$350` → Basic (5%) → saves $17.50
- `$750` → Standard (10%) → saves $75.00
- `$1200` → Premium (20%) → saves $240.00
- `$50` → No discount

---

### TRACING A VALUE THROUGH THE TIERS (3:30–5:30)

Exercise 1 asks you to trace `order_total = 350` through the logic manually.

- `350 >= 1000`? No → skip
- `350 >= 500`? No → skip
- `350 >= 100`? Yes → `discount_rate = 0.05`, tier = "Basic (5%)"
- The `else` never runs

This is the key insight about elif: Python stops at the first True condition and skips everything below it. The order of conditions matters — always put the highest threshold first.

---

### COMBINING CONDITIONS WITH AND (5:30–7:30)

Exercise 2 asks about the difference between a compound condition and two separate ifs:

```python
# Compound — both must be true simultaneously
if total > 100 and total < 500:
    ...

# Two separate ifs — each evaluated independently
if total > 100:
    ...
if total < 500:
    ...
```

With two separate ifs, both conditions are checked every time — they don't form a range. For range checks, always use `and` in a single condition.

The cleaner Python way to write a range:
```python
if 100 < total < 500:   # chained comparison — very readable
    ...
```

---

### SUBMISSION CHECKLIST (7:30–10:00)

- `discount.py` with at least three tiers using if/elif/else
- `input()` used for order total with `float()` conversion
- Formatted output showing tier, discount amount, and final price
- Exercise 1: manual trace of `order_total = 350` written out
- Exercise 2: compound vs separate if explained
- Career example written (2–3 sentences)
- Submitted to Canvas
