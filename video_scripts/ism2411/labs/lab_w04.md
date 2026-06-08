# ISM2411 Lab W04: Revenue, Margin & Discount Calculator

## YouTube Metadata

**Title:** Revenue, Margin & Discount Calculator — Lab Walkthrough | ISM2411 Lab 04
**Description:**
Walkthrough of ISM2411 Module 4 Lab. We apply arithmetic, comparison, and logical operators to real business formulas: revenue, profit margin, discount pricing, and pallet-packing logistics.

**Chapters:**
0:00 — What we're building
0:45 — Revenue and margin calculations
3:00 — Discount application with correct percentage math
5:00 — Comparison and logical operators for approval logic
7:00 — Modulo for pallet logistics
8:30 — Submission checklist

**Applies to:** ISM2411 Module 04

**Tags:** python arithmetic operators, python business calculator, python margin calculation, python modulo operator, ISM2411, USF, python operators tutorial

---

## Script

### INTRO (0:00–0:45)

Lab 4 — Revenue, Margin and Discount Calculator. We're applying operators to business math: revenue, profit margin, discount pricing, and a logistics problem using modulo. Save this as `module04/calculator.py`.

---

### REVENUE AND MARGIN (0:45–3:00)

```python
# --- Exercise 1: Revenue ---
unit_price  = 79.99
quantity    = 150
revenue     = unit_price * quantity
print(f"Revenue: ${revenue:,.2f}")
```

Output: `Revenue: $11,998.50`

```python
# --- Exercise 2: Profit Margin ---
cost_per_unit = 45.00
total_cost    = cost_per_unit * quantity
profit        = revenue - total_cost
margin        = profit / revenue
print(f"Profit:  ${profit:,.2f}")
print(f"Margin:  {margin:.1%}")
```

Output:
```
Profit:  $5,248.50
Margin:  43.7%
```

The `:.1%` format spec multiplies by 100 and adds the percent sign automatically. Always store margins as decimals (0.437), format them as percent only for display.

---

### DISCOUNT APPLICATION (3:00–5:00)

The common mistake in Exercise 6: using `10` instead of `0.10` for a 10% discount.

```python
# --- Exercise 3: Discount ---
original_price   = 79.99
discount_rate    = 0.10          # 10% — must be decimal form
discount_amount  = original_price * discount_rate
discounted_price = original_price - discount_amount

print(f"Original:   ${original_price:.2f}")
print(f"Discount:   ${discount_amount:.2f}")
print(f"Final:      ${discounted_price:.2f}")
```

If you used `10` instead of `0.10`, you get a discount of `$799.90` — larger than the price itself. Python won't crash; it just gives you a wrong answer silently. That's why the lab asks about this: silent errors are harder to catch than crashes.

---

### COMPARISON AND LOGICAL OPERATORS (5:00–7:00)

```python
# --- Exercise 4: Approval Logic ---
order_total   = 850
credit_limit  = 1000
is_approved   = True

can_process = (order_total <= credit_limit) and is_approved
print(f"Order ${order_total} can process: {can_process}")

# Comparison operators
print(order_total > 500)     # True — high-value order
print(order_total == 1000)   # False
print(order_total != 500)    # True
```

Logical operators let you combine conditions. `and` requires both to be True. `or` requires at least one.

---

### MODULO FOR LOGISTICS (7:00–8:30)

```python
# --- Exercise 7: Pallet Packing ---
items_to_ship    = 157
items_per_pallet = 24

full_pallets     = items_to_ship // 24   # integer division
remainder        = items_to_ship % 24    # leftovers

print(f"Full pallets: {full_pallets}")
print(f"Leftover items: {remainder}")
```

Output:
```
Full pallets: 6
Leftover items: 13
```

`//` is floor division — gives you whole pallets only. `%` gives the remainder. Both together answer the logistics question: "how many full pallets, and what's left over?"

---

### SUBMISSION CHECKLIST (8:30–10:00)

- All exercises (1–7) in a single `calculator.py`
- Each exercise marked with `# --- Exercise N ---` comment
- All numeric output uses f-string format specs (`:,.2f`, `:.1%`)
- Discount uses `0.10` not `10`
- Exercise responses written
- Submitted to Canvas
