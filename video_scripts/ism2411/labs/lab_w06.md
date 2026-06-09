# ISM2411 Lab W06: Sales Loop — Sum, Average, Max

## YouTube Metadata

**Title:** Sales Loop: Sum, Average, and Max — Lab Walkthrough | ISM2411 Lab 06
**Description:**
Walkthrough of ISM2411 Module 6 Lab. We use for loops and the initialize-loop-update accumulator pattern to compute a sales total, average, and maximum from a list — the foundation of every data processing loop you'll write.

Course page: https://markumreed.github.io/ism2411/pages/week06_lab.html

**Chapters:**
0:00 — What we're building
0:45 — The accumulator pattern: initialize, loop, update
2:30 — Computing sum, count, and average
4:30 — Finding the max without using max()
6:30 — Extension: while loop version
8:30 — Submission checklist

**Applies to:** ISM2411 Module 06

**Tags:** python for loop, python accumulator pattern, python sum average loop, python sales data, ISM2411, USF, python loops tutorial

---

## Script

### INTRO (0:00–0:45)

Lab 6 — Sales Loop: Sum, Average, and Max. We're learning the accumulator pattern — the foundation of every data processing loop. Initialize a variable before the loop, update it inside the loop, read the result after the loop. Let's build it.

---

### THE ACCUMULATOR PATTERN: SUM (0:45–2:30)

```python
# sales_loop.py

sales = [340.00, 215.50, 892.75, 133.00, 567.25, 408.90, 721.00]

# --- Exercise 1: Sum ---
total = 0          # initialize
for sale in sales:
    total += sale  # update

print(f"Total sales: ${total:,.2f}")
```

Output: `Total sales: $3,278.40`

Three steps every time:
1. Initialize the accumulator to 0 before the loop
2. Add each value inside the loop
3. Use the result after the loop

Never define the accumulator inside the loop — it would reset to 0 on every iteration.

---

### AVERAGE (2:30–4:30)

The lab asks you to track both total and count without using `len()` or `sum()`:

```python
# --- Exercise 2: Average ---
total = 0
count = 0

for sale in sales:
    total += sale
    count += 1

average = total / count
print(f"Average sale: ${average:,.2f}")
print(f"Count: {count}")
```

Two accumulators running in parallel inside the same loop. This is the pattern you'll use on real data where you don't know the size in advance.

---

### MAXIMUM WITHOUT max() (4:30–6:30)

```python
# --- Exercise 3: Maximum ---
highest = sales[0]   # initialize to first value (not 0!)

for sale in sales:
    if sale > highest:
        highest = sale

print(f"Highest sale: ${highest:,.2f}")
```

Initialize to the first element, not to 0. If you initialize to 0 and all sales happen to be negative (a return scenario), you'd get the wrong answer. Starting at the first element is always safe.

---

### WHILE LOOP VERSION (6:30–8:30)

Extension exercise — rewrite the sum using a while loop and index variable:

```python
# --- Extension: while loop sum ---
index = 0
total = 0

while index < len(sales):
    total += sales[index]
    index += 1

print(f"Total (while): ${total:,.2f}")
```

Same result, more code. The for loop is cleaner for iterating a known list. The while loop is better when the stop condition isn't just "end of list" — for example, "keep going until the total exceeds $5000."

---

### SUBMISSION CHECKLIST (8:30–10:00)

- `sales_loop.py` with sum, count, average, and max all computed without built-ins
- Accumulator initialized before the loop, updated inside, read after
- Max initialized to `sales[0]`, not `0`
- Extension: while loop version of the sum
- Exercise responses written
- Submitted to Canvas
