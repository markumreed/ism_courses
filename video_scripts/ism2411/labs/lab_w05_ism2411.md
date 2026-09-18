# ISM2411 Lab W05: Tiered Discount Calculator

## YouTube Metadata

**Title:** Tiered Discount Calculator — Full Lab Walkthrough | ISM2411 Lab 05
**Description:**
Step-by-step, test-as-you-go walkthrough of ISM2411 Module 5 Lab. Build discount.py: if/elif/else discount tiers, a manager-approval flag, combined conditions with and, refactoring a nested if into a flat one, anomaly flagging with three bands, and VIP boolean logic with not.

Course page: https://markumreed.github.io/ism2411/pages/week05_lab.html

**Chapters:**
0:00 — What this lab covers
0:40 — Exercise 1: the discount tier ladder
2:30 — Exercise 2: the manager-approval flag
3:30 — Exercise 3: combining conditions with and
5:00 — Exercise 4: flattening a nested if
6:40 — Exercise 5: anomaly flagging with three bands
8:10 — Exercise 6: VIP boolean logic with not
9:40 — Reflection questions
10:30 — Submission checklist

**Applies to:** ISM2411 Module 05

**Tags:** python if elif else tutorial, python conditional logic business, python and or not, python nested if refactor, ISM2411, USF, python for business beginners, marginal tax bracket python

---

## How to Use This Script

**SAY** it, **DO** it, **CHECK** the exact output, **FIX** it if it doesn't match — then move to the next step. Everything builds into one file, `discount.py`.

---

## Script

### INTRO (0:00–0:40)

**SAY:** "Lab 5 — the tiered discount calculator. This is the lab where `if`/`elif`/`else` stops being an abstract syntax lesson and becomes actual business decision logic — the same shape as tax brackets, shipping tiers, and loyalty programs you interact with every day."

---

### EXERCISE 1 — Discount Tiers (0:40–2:30)

**SAY:** "Four tiers, checked from highest threshold to lowest — order matters here, and we'll see why in a second."

**DO:** Starting from the given scaffold:
```python
total = float(input("Enter cart total: $"))
# Add your if/elif/else here
discount = 0  # replace with correct logic
final = total * (1 - discount)
print(f"Discount: {discount*100:.0f}%")
```
Fill in the logic:
```python
total = float(input("Enter cart total: $"))

if total >= 500:
    discount = 0.15
elif total >= 200:
    discount = 0.10
elif total >= 100:
    discount = 0.05
else:
    discount = 0

final = total * (1 - discount)
print(f"Discount: {discount*100:.0f}%")
print(f"Final price: ${final:,.2f}")
```
```bash
python3 discount.py
```
Enter `250`.

**CHECK:**
```
Enter cart total: $250
Discount: 10%
Final price: $225.00
```

**SAY:** "Trace it: `250` fails the `>= 500` check, but passes `>= 200` — so `elif` stops right there at 10%, never even checking the `>= 100` branch. That's exactly why the order is highest-threshold-first: if you checked `>= 100` first, a $250 cart would incorrectly stop at the 5% tier instead of reaching the 10% one."

---

### EXERCISE 2 — Approval Flag (2:30–3:30)

**SAY:** "A second, independent decision — nothing to do with the discount tier, just a threshold on the final price."

**DO:**
```python
if final > 1000:
    status = "manager_approval_required"
else:
    status = "auto_approved"

print(f"Status: {status}")
```
```bash
python3 discount.py
```
Enter `637.50` as the cart total directly this time, or trace it through from a total that produces `final = 637.50`.

**CHECK:**
```
Status: auto_approved
```
`637.50` doesn't exceed `1000`, so it auto-approves.

---

### EXERCISE 3 — Combine Conditions (3:30–5:00)

**SAY:** "Now a regional bonus, layered on top of the tier discount — and this is where `and` combines two separate facts into one condition."

**DO:**
```python
region = "South"

extra_discount = 0
if region == "South" and total >= 100:
    extra_discount = 0.02
    print("Region bonus applied: additional 2% off")

final_discount = discount + extra_discount
final = total * (1 - final_discount)

print(f"Final discount: {final_discount*100:.0f}%")
print(f"Final price: ${final:,.2f}")
```
```bash
python3 discount.py
```
Enter `250` as the total, with `region = "South"`.

**CHECK:**
```
Region bonus applied: additional 2% off
Final discount: 12%
Final price: $220.00
```

**SAY:** "Trace it: tier discount from Exercise 1 was 10% for a $250 cart. The region bonus adds 2%, since both `region == \"South\"` and `total >= 100` are true — `12%` combined. `250 × (1 - 0.12) = 250 × 0.88 = 220.00`."

---

### EXERCISE 4 — Refactor a Nested If (5:00–6:40)

**SAY:** "Now a code-quality exercise — the same logic, written two different ways, and one of them is clearly easier to read."

**DO:** Start with the nested version:
```python
# Nested version — the one to rewrite
if region == "South":
    if total > 100:
        if customer_type == "wholesale":
            extra_discount = 0.03
```
Rewrite it flat, using `and`:
```python
# Flat version
if region == "South" and total > 100 and customer_type == "wholesale":
    extra_discount = 0.03
    # Flat is easier to read and test: all three conditions are visible on one line,
    # and you can test each condition independently without needing to nest
    # test cases three levels deep to reach the code that actually runs.
```

**CHECK:** Run both versions with `region = "South"`, `total = 150`, `customer_type = "wholesale"` — confirm both produce `extra_discount = 0.03`. They're logically identical; only the *readability* differs. That's the lesson: three levels of indentation hide the fact that all three conditions must be true simultaneously, while the flat `and` chain makes that requirement visible at a glance.

---

### EXERCISE 5 — Anomaly Flagging (6:40–8:10)

**SAY:** "Three bands this time, not two — and notice the order again matters, same as Exercise 1."

**DO:**
```python
amount = -50   # test with -50, then 500, then 15000

if amount <= 0:
    print("SUSPICIOUS")
elif amount < 10000:
    print("NORMAL")
else:
    print("LARGE — REVIEW REQUIRED")
```
```bash
python3 discount.py
```
Run it three times, changing `amount` each time to `-50`, then `500`, then `15000`.

**CHECK:**
```
-50   → SUSPICIOUS
500   → NORMAL
15000 → LARGE — REVIEW REQUIRED
```

**SAY:** "For `amount = 15000`: it fails `<= 0`, fails `< 10000`, so it falls all the way to `else` — the only branch left. That's the pattern with three-way branching: each `elif` only runs if every condition above it already failed."

---

### EXERCISE 6 — Boolean Logic (8:10–9:40)

**SAY:** "One condition built from `or`, then narrowed with `not` — a two-part business rule."

**DO:**
```python
total_spent_this_year = 2500
orders_this_year = 6
has_outstanding_balance = False

qualifies_by_spend  = total_spent_this_year > 2000
qualifies_by_orders = orders_this_year > 10
vip_upgrade = (qualifies_by_spend or qualifies_by_orders) and not has_outstanding_balance

print(f"VIP upgrade: {vip_upgrade}")
```
```bash
python3 discount.py
```

**CHECK:**
```
VIP upgrade: True
```

**SAY:** "Trace it: spend of $2,500 clears $2,000, so `qualifies_by_spend` is `True` — that alone is enough for the `or` to be `True`, regardless of the order count. Then `not has_outstanding_balance` — since there's no outstanding balance, `not False` is `True`, and `True and True` gives the final `True`. Now flip `has_outstanding_balance` to `True` and re-run — even with the same spend and order numbers, the customer no longer qualifies."

---

### REFLECTION QUESTIONS (9:40–10:30)

**DO:** Answer honestly:
1. Without looking at your code, can you explain in plain English what happens to `order_total = 350` as it passes through your discount tier logic? Trace it step by step.
2. What is the difference between `if total > 100 and total < 500:` and two separate `if` statements checking each condition? Would both produce the same result? Why or why not?
3. Where in your day-to-day life do you encounter systems that use tiered conditional logic? (Think: tax brackets, shipping fees, insurance premiums, credit card rewards.) How does knowing Python conditionals change how you think about those systems?

**CHECK:** Question 2's honest answer: two separate `if` statements (not `elif`) would both evaluate independently and *both* run their bodies if both conditions are true, whereas `and` inside a single `if` requires both conditions simultaneously to run the body even once — they're related but not automatically interchangeable, and the right choice depends on whether you want one combined decision or two independent ones.

---

### SUBMISSION CHECKLIST (10:30–end)

- [ ] `discount.py` — filename matches exactly, lowercase
- [ ] Exercise 1: correct tier logic, tested with `total = 250` giving 10% / $225.00
- [ ] Exercise 2: approval flag correct for `final = 637.50`
- [ ] Exercise 3: South-region bonus tested, giving 12% / $220.00
- [ ] Exercise 4: nested if flattened, with a comment explaining why it's easier to read
- [ ] Exercise 5: all three anomaly bands tested with `-50`, `500`, `15000`
- [ ] Exercise 6: VIP logic using both `or` and `not`
- [ ] Three reflection questions answered honestly
- [ ] Submitted to Canvas
