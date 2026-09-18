# ISM2411 Lab W06: Sales Loop — Sum, Average, Max

## YouTube Metadata

**Title:** Sales Loop — Sum, Average, Max — Full Lab Walkthrough | ISM2411 Lab 06
**Description:**
Step-by-step, test-as-you-go walkthrough of ISM2411 Module 6 Lab. Build sales_loop.py: the accumulator pattern for sum, average, and max without built-in helpers, a filtered count, break/continue for outlier detection, a while-loop rewrite compared side by side with the for-loop version, and tiered discounts applied across an entire list.

Course page: https://markumreed.github.io/ism2411/pages/week06_lab.html

**Chapters:**
0:00 — What this lab covers — the accumulator pattern
0:45 — Exercise 1: sum without sum()
1:50 — Exercise 2: average — total and count together
3:00 — Exercise 3: max without max()
4:10 — Exercise 4: filtered count and total
5:30 — Exercise 5: break and continue for outlier detection
7:20 — Exercise 6: the while-loop rewrite, compared
8:50 — Exercise 7: tiered discount across the whole list
10:20 — Reflection questions
11:10 — Submission checklist

**Applies to:** ISM2411 Module 06

**Tags:** python for loop accumulator pattern, python while loop tutorial, python break continue, python nested loops, ISM2411, USF, python for business beginners

---

## How to Use This Script

**SAY** it, **DO** it, **CHECK** the exact output, **FIX** it if it doesn't match — then move to the next step. Everything builds into one file, `sales_loop.py`, reusing the same `sales` list across every exercise.

---

## Script

### INTRO (0:00–0:45)

**SAY:** "Lab 6 — the sales loop. Today's core idea is the accumulator pattern: initialize a variable before the loop, update it on every pass through the loop, and read the final result after the loop ends. That three-step shape shows up in almost every data-processing script you'll ever write — sum, average, max, filtered counts, all of it."

---

### EXERCISE 1 — Sum a List (0:45–1:50)

**SAY:** "The accumulator pattern, in its purest form — no `sum()`, just the three steps by hand."

**DO:**
```python
sales = [120, 80, 250, 175, 90, 410, 60, 215]
total = 0       # initialize
for sale in sales:
    total += sale   # update
print(f"Total: ${total}")
```
```bash
python3 sales_loop.py
```

**CHECK:**
```
Total: $1400
```
Confirm by hand: `120+80+250+175+90+410+60+215 = 1,400`.

**SAY:** "Three steps, always in this order: `total = 0` initializes *before* the loop starts. `total += sale` updates on *every single pass* through the loop. Reading `total` only happens *after* the loop is completely finished — read it inside the loop and you'd only see a partial sum."

---

### EXERCISE 2 — Average (1:50–3:00)

**SAY:** "Two accumulators running side by side — a running total and a running count — combined into one calculation after the loop ends."

**DO:**
```python
total = 0
count = 0
for sale in sales:
    total += sale
    count += 1

average = total / count
print(f"Total: ${total}")
print(f"Count: {count}")
print(f"Average: ${average:.2f}")
```
```bash
python3 sales_loop.py
```

**CHECK:**
```
Total: $1400
Count: 8
Average: $175.00
```
Confirm: `1400 / 8 = 175.00` exactly.

---

### EXERCISE 3 — Max (3:00–4:10)

**SAY:** "A different kind of accumulator — instead of adding, we're comparing and conditionally replacing."

**DO:**
```python
current_max = 0   # or sales[0], to be safe with negative numbers
for sale in sales:
    if sale > current_max:
        current_max = sale

print(f"Largest sale: ${current_max}")
```
```bash
python3 sales_loop.py
```

**CHECK:**
```
Largest sale: $410
```

**SAY:** "Trace it: `current_max` starts at 0. Every sale that's bigger than the current `current_max` replaces it. `410` is the largest single value in the list, so it's the last one to win that comparison. Note initializing to `0` only works safely if you're certain every value in the list is non-negative — if the list could contain negative numbers, initialize to `sales[0]` instead."

---

### EXERCISE 4 — Filtered Count (4:10–5:30)

**SAY:** "Now combine the accumulator pattern with a condition — count and total, but only for values that pass a filter."

**DO:**
```python
count_over_100 = 0
total_over_100 = 0
for sale in sales:
    if sale > 100:
        count_over_100 += 1
        total_over_100 += sale

print(f"Sales over $100: {count_over_100}")
print(f"Total of those sales: ${total_over_100}")
```
```bash
python3 sales_loop.py
```

**CHECK:**
```
Sales over $100: 5
Total of those sales: $1170
```

**SAY:** "Trace which five sales clear $100: 120, 250, 175, 410, 215 — five values, and `120+250+175+410+215 = 1,170`."

---

### EXERCISE 5 — break / continue (5:30–7:20)

**SAY:** "Two loop-control keywords in one exercise: `continue` skips the rest of the current pass and moves to the next item; `break` exits the loop entirely, immediately."

**DO:**
```python
for sale in sales:
    if sale > 400:
        print(f"Alert: outlier found — ${sale}. Stopping.")
        break
    if sale <= 100:
        continue
    print(f"${sale}")
```
```bash
python3 sales_loop.py
```

**CHECK:**
```
$120
$250
$175
Alert: outlier found — $410. Stopping.
```

**SAY:** "Trace every value: 120 — neither condition fires, so it prints. 80 — `<= 100` fires `continue`, skipping the print entirely, straight to the next item. 250 and 175 — both print normally. 90 — skipped again by `continue`. 410 — this is the first value over 400, so `break` fires immediately: the alert prints, and the loop stops completely, before even looking at `60` or `215`."

---

### EXERCISE 6 — While Loop (7:20–8:50)

**SAY:** "Same sum as Exercise 1, rewritten with a `while` loop and a manually managed index — watch how much more bookkeeping this requires."

**DO:**
```python
total = 0
i = 0            # index
while i < len(sales):
    total += sales[i]
    i += 1

print(f"Total (while loop): ${total}")
```
```bash
python3 sales_loop.py
```

**CHECK:**
```
Total (while loop): $1400
```
Same answer as Exercise 1 — confirming both approaches are logically equivalent.

**SAY:** "Compare the code length: the `for` loop needed one line to declare the loop and Python handled the indexing internally. The `while` loop needs a manually initialized index (`i = 0`), a comparison against `len(sales)`, and a manual increment (`i += 1`) that you must remember to include — forget that last line and this becomes an infinite loop. Add a comment: for iterating over every item in a known list, `for` is almost always the production choice — `while` earns its keep when the stopping condition isn't simply 'reached the end of a list,' like waiting for user input to equal `'quit'`."

---

### EXERCISE 7 — Discount Applied to All Items (8:50–10:20)

**SAY:** "Reusing last week's tiered discount logic, now applied inside a loop instead of to one single value."

**DO:**
```python
for sale in sales:
    if sale >= 200:
        discount = 0.10
    elif sale >= 100:
        discount = 0.05
    else:
        discount = 0

    discounted_price = sale * (1 - discount)
    print(f"${sale} → {discount*100:.0f}% discount → ${discounted_price:.2f}")
```
```bash
python3 sales_loop.py
```

**CHECK:** First two rows:
```
$120 → 5% discount → $114.00
$80 → 0% discount → $80.00
```
Trace: `120` is between 100 and 200, so it gets the 5% tier: `120 × 0.95 = 114.00`. `80` is under 100, so it gets no discount at all.

---

### REFLECTION QUESTIONS (10:20–11:10)

**DO:** Answer honestly:
1. Explain the accumulator pattern in your own words, as if explaining to a classmate who missed the lecture. What are the three steps, and why does each step matter?
2. When you ran Exercise 6 (the while-loop version of sum), what did you notice about the code length compared to the for-loop version? What are the trade-offs of each approach?
3. Describe a real dataset from your major or a summer job where you would use a loop to compute a summary statistic. What would the list contain, what would you accumulate, and what would you print at the end?

**CHECK:** Question 1's answer should name all three steps explicitly — initialize before the loop, update inside the loop, read the result after the loop — and explain that skipping any one of them (initializing inside the loop, reading the result too early) breaks the pattern.

---

### SUBMISSION CHECKLIST (11:10–end)

- [ ] `sales_loop.py` — filename matches exactly, lowercase
- [ ] Exercise 1: sum computed via accumulator, matching $1,400
- [ ] Exercise 2: total, count, and average all printed correctly
- [ ] Exercise 3: max found without using `max()`
- [ ] Exercise 4: filtered count and total for sales over $100
- [ ] Exercise 5: `break`/`continue` producing the exact expected sequence
- [ ] Exercise 6: while-loop rewrite, with a comment comparing it to the for-loop version
- [ ] Exercise 7: discount applied across every item in the list
- [ ] Three reflection questions answered honestly
- [ ] Submitted to Canvas
