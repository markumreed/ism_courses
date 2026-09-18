# ISM2411 Lab W04: Revenue, Margin & Discount Calculator

## YouTube Metadata

**Title:** Revenue, Margin & Discount Calculator — Full Lab Walkthrough | ISM2411 Lab 04
**Description:**
Step-by-step, test-as-you-go walkthrough of ISM2411 Module 4 Lab. Build calculator.py: revenue and margin formulas, a two-product comparison using comparison operators, a logical "premium product" check, the division/floor-division/modulo trio predicted before running, a full interactive pricing calculator, and a warehouse packaging problem solved with // and %.

Course page: https://markumreed.github.io/ism2411/pages/week04_lab.html

**Chapters:**
0:00 — What this lab covers
0:40 — Exercise 1: revenue with thousands separator
1:30 — Exercise 2: margin as a percentage
2:20 — Exercise 3: comparing two products' margins
3:30 — Exercise 4: the logical "is_premium" check
4:50 — Exercise 5: predict, then verify — /, //, %
6:20 — Exercise 6: the full interactive pricing calculator
8:30 — Exercise 7: the warehouse packaging problem
10:00 — Reflection questions
10:50 — Submission checklist

**Applies to:** ISM2411 Module 04

**Tags:** python arithmetic operators, python floor division modulo, python comparison logical operators, python break even calculator, ISM2411, USF, python for business beginners

---

## How to Use This Script

**SAY** it, **DO** it, **CHECK** the exact output, **FIX** it if it doesn't match — then move to the next step. Everything builds into one file, `calculator.py`, with a `# --- Exercise N ---` comment marking each section.

---

## Script

### INTRO (0:00–0:40)

**SAY:** "Lab 4 — revenue, margin, and a discount calculator. Today's operators — arithmetic, comparison, logical — are the building blocks of every business rule you'll ever encode: is this over budget, does this qualify for a discount, which of two options is better. All of it starts here."

---

### EXERCISE 1 — Revenue (0:40–1:30)

**SAY:** "The simplest possible business formula — price times quantity — formatted for a human to read."

**DO:**
```python
# --- Exercise 1 ---
price = 50
quantity = 12
revenue = price * quantity
print(f"Revenue: ${revenue:,.2f}")
```
```bash
python3 calculator.py
```

**CHECK:**
```
Revenue: $600.00
```
`:,.2f` does two things at once: adds thousands separators (not visible yet at $600, but it will matter soon) and forces exactly two decimal places.

---

### EXERCISE 2 — Margin (1:30–2:20)

**SAY:** "Margin — the same formula from last week's product card, now formatted with the `%` format spec instead of computing a percentage by hand."

**DO:**
```python
# --- Exercise 2 ---
cost = 32
price = 50
margin = (price - cost) / price
print(f"Margin: {margin:.1%}")
```
```bash
python3 calculator.py
```

**CHECK:**
```
Margin: 36.0%
```

**SAY:** "Notice `margin` itself is `0.36`, a plain decimal fraction — the `.1%` format spec is what multiplies it by 100 and appends the `%` sign for display. The underlying variable never actually becomes `36.0`; only the printed *text* does."

---

### EXERCISE 3 — Two Products (2:20–3:30)

**SAY:** "Now a comparison — which of two products has the better margin? Store the answer as a boolean, not just print it as a sentence."

**DO:**
```python
# --- Exercise 3 ---
price_a, cost_a = 50, 32
price_b, cost_b = 80, 60

margin_a = (price_a - cost_a) / price_a
margin_b = (price_b - cost_b) / price_b

product_a_wins = margin_a > margin_b

print(f"Product A margin: {margin_a:.1%}")
print(f"Product B margin: {margin_b:.1%}")
print(f"Product A wins: {product_a_wins}")
```
```bash
python3 calculator.py
```

**CHECK:**
```
Product A margin: 36.0%
Product B margin: 25.0%
Product A wins: True
```
Confirm by hand: Product B's margin is `(80-60)/80 = 0.25`, lower than A's `0.36` — so `margin_a > margin_b` correctly evaluates to `True`.

---

### EXERCISE 4 — Logical Combo (3:30–4:50)

**SAY:** "Now combine two conditions with `and` — a product only counts as 'premium' if *both* the price is high enough *and* the margin is good enough."

**DO:**
```python
# --- Exercise 4 ---
price = 150
margin = 0.35
is_premium = price > 100 and margin > 0.3
print(f"is_premium = {is_premium}")
```
```bash
python3 calculator.py
```

**CHECK:**
```
is_premium = True
```

**SAY:** "Now change the values so only one condition holds — say the margin drops to 0.2 while the price stays at 150."

**DO:**
```python
price = 150
margin = 0.2
is_premium = price > 100 and margin > 0.3
print(f"is_premium = {is_premium}")
```

**CHECK:**
```
is_premium = False
```
Even though `price > 100` is still `True`, `and` requires **both** sides to be `True` — one failing condition is enough to make the whole expression `False`.

---

### EXERCISE 5 — Common-Mistake Check (4:50–6:20)

**SAY:** "Before running anything, predict out loud what each of these three produces — then check yourself."

**DO:** Predict, then run:
```python
# --- Exercise 5 ---
print(17 / 5)
print(17 // 5)
print(17 % 5)
```
```bash
python3 calculator.py
```

**CHECK:**
```
3.4
3
2
```

**SAY:** "`/` is true division — always returns a float, `3.4`. `//` is floor division — drops everything after the decimal, keeping just the whole number, `3`. `%` is modulo — the *remainder* after floor division, `2`, because `3 × 5 = 15` and `17 − 15 = 2`. In business terms: `//` answers 'how many complete groups fit,' and `%` answers 'what's left over that doesn't fill a complete group' — you'll use exactly that pairing in Exercise 7."

---

### EXERCISE 6 — Full Pricing Calculator (6:20–8:30)

**SAY:** "Now the real tool — five inputs from the user, four calculations, a five-line formatted report."

**DO:**
```python
# --- Exercise 6 ---
name          = input("Product name: ")
retail_price  = float(input("Retail price: "))
unit_cost     = float(input("Unit cost: "))
quantity_sold = int(input("Quantity sold: "))
discount_pct  = float(input("Discount percent (e.g., 10 for 10%): "))

revenue             = retail_price * quantity_sold
discounted_revenue  = revenue * (1 - discount_pct / 100)
gross_margin        = (retail_price - unit_cost) / retail_price
net_profit          = discounted_revenue - (unit_cost * quantity_sold)

print(f"Product:            {name}")
print(f"Revenue:             ${revenue:,.2f}")
print(f"Discounted Revenue:  ${discounted_revenue:,.2f}")
print(f"Gross Margin:        {gross_margin:.1%}")
print(f"Net Profit:          ${net_profit:,.2f}")
```
```bash
python3 calculator.py
```
Enter: `Widget`, `25`, `15`, `200`, `10`.

**CHECK:**
```
Product name: Widget
Retail price: 25
Unit cost: 15
Quantity sold: 200
Discount percent (e.g., 10 for 10%): 10
Product:            Widget
Revenue:             $5,000.00
Discounted Revenue:  $4,500.00
Gross Margin:        40.0%
Net Profit:          $1,500.00
```

**SAY:** "Trace it: revenue is `25 × 200 = 5,000`. Discounted revenue applies the 10% discount: `5,000 × 0.90 = 4,500`. Gross margin is `(25-15)/25 = 40.0%`. Net profit subtracts total cost from discounted revenue: `4,500 − (15 × 200) = 4,500 − 3,000 = 1,500`."

**FIX:** If your discounted revenue is way too small (or negative), you likely forgot to divide `discount_pct` by 100 — using `10` directly instead of `0.10` would compute `5000 × (1 - 10) = 5000 × -9 = -45,000`, a silently wrong but *not crashing* answer. That's the trap Reflection Question 1 asks about.

---

### EXERCISE 7 — Packaging Problem (8:30–10:00)

**SAY:** "A logistics problem — how many full boxes, and how many loose items are left — using exactly the `//` and `%` pairing from Exercise 5."

**DO:**
```python
# --- Exercise 7 ---
BOX_SIZE = 24
items_ordered = int(input("Number of items ordered: "))

full_boxes   = items_ordered // BOX_SIZE
loose_items  = items_ordered % BOX_SIZE
exact_fit    = loose_items == 0

print(f"Full boxes: {full_boxes}")
print(f"Loose items: {loose_items}")
print(f"Exact fit: {exact_fit}")
```
```bash
python3 calculator.py
```
Enter `100`.

**CHECK:**
```
Number of items ordered: 100
Full boxes: 4
Loose items: 4
Exact fit: False
```
Confirm: `100 // 24 = 4` (since `4 × 24 = 96`), `100 % 24 = 4` (the leftover), and since the remainder isn't zero, `exact_fit` is `False`.

---

### REFLECTION QUESTIONS (10:00–10:50)

**DO:** Answer honestly:
1. In Exercise 6, what would happen if you forgot to divide the discount percentage by 100 — used `10` instead of `0.10`? Describe the error this causes — does Python crash, or does it produce a wrong answer silently?
2. The modulo operator (`%`) might seem obscure, but Exercise 7 shows it solving a real logistics problem. Describe another business scenario where you'd need to know both "how many full groups" and "how many are left over."
3. Looking back at Modules 01–04, you've gone from "what is a computer" to writing a working pricing calculator that handles user input and produces formatted financial output. What concept from these four modules do you feel least confident about, and what would help you strengthen it?

**CHECK:** Question 1's answer should be specific: Python does **not** crash — it silently computes a wildly wrong (often negative) discounted revenue. That silence is precisely why this kind of bug is dangerous in real business code.

---

### SUBMISSION CHECKLIST (10:50–end)

- [ ] `calculator.py` — filename matches exactly, lowercase
- [ ] All exercises 1–7 present as one runnable script
- [ ] Each exercise marked with a `# --- Exercise N ---` comment
- [ ] All numeric output uses appropriate f-string format specs (`:,.2f`, `:.1%`, etc.)
- [ ] Three reflection questions answered honestly
- [ ] Submitted to Canvas
