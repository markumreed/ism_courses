# ISM2411 Lab W10: Inventory List Manager

## YouTube Metadata

**Title:** Inventory List Manager — Full Lab Walkthrough | ISM2411 Lab 10
**Description:**
Step-by-step, test-as-you-go walkthrough of ISM2411 Module 10 Lab. Build inventory.py: list creation and indexing (positive and negative), slicing including step slices, append/remove/sort mutation, a tuple immutability experiment with try/except, sales statistics with sum/len/max/min, the accumulator pattern building a discounted list, and filtering a list above a threshold — one complete data-structures lab from list basics to a full filter-and-summarize pass.

Course page: https://markumreed.github.io/ism2411/pages/week10_lab.html

**Chapters:**
0:00 — What this lab covers
0:40 — Exercise 1: build the list, print it, len()
1:30 — Exercise 2: positive, negative, and computed-middle indices
2:50 — Exercise 3: three kinds of slicing
4:20 — Exercise 4: append, remove, sort — watched step by step
5:50 — Exercise 5: tuples, TypeError, and try/except
7:30 — Exercise 6: sum, len, average, max, min on a sales list
8:50 — Exercise 7: the accumulator pattern building a new list
10:10 — Exercise 8: filtering above a threshold
11:40 — Reflection questions
12:20 — Submission checklist

**Applies to:** ISM2411 Module 10

**Tags:** python lists tutorial, python slicing negative index, python tuples immutable, python try except typeerror, ISM2411, USF, python for business beginners

---

## How to Use This Script

**SAY** it, **DO** it, **CHECK** the exact output, **FIX** it if it doesn't match — then move to the next step. Everything builds into one file, `inventory.py`.

---

## Script

### INTRO (0:00–0:40)

**SAY:** "Lab 10 — the inventory list manager. First lab of Unit 3, data structures. Lists are the single most-used data structure in this entire course — indexing, slicing, and the methods you'll build today show up in nearly every script from here forward."

---

### EXERCISE 1 — Build the List (0:40–1:30)

**SAY:** "Five items, one list, and its length."

**DO:**
```python
inventory = ["pen", "notebook", "stapler", "tape", "marker"]
print(inventory)
print(len(inventory))
```
```bash
python3 inventory.py
```

**CHECK:**
```
['pen', 'notebook', 'stapler', 'tape', 'marker']
5
```

---

### EXERCISE 2 — Index Practice (1:30–2:50)

**SAY:** "First, last, and middle — but the middle position gets *computed*, not hardcoded, so this still works if the list grows or shrinks."

**DO:**
```python
print(inventory[0])
print(inventory[-1])
print(inventory[len(inventory) // 2])
```
```bash
python3 inventory.py
```

**CHECK:**
```
pen
marker
stapler
```

**SAY:** "`inventory[0]` — the first item, always index zero. `inventory[-1]` — negative indexing counts from the end, so `-1` is always the last item regardless of the list's length. `len(inventory) // 2` — with 5 items, that's `5 // 2 = 2`, and `inventory[2]` is `'stapler'`, the exact middle of a 5-item list."

---

### EXERCISE 3 — Slicing (2:50–4:20)

**SAY:** "Three different slice patterns — a range from the start, a range from the end, and a step."

**DO:**
```python
print(inventory[:3])
print(inventory[-2:])
print(inventory[::2])
```
```bash
python3 inventory.py
```

**CHECK:**
```
['pen', 'notebook', 'stapler']
['tape', 'marker']
['pen', 'stapler', 'marker']
```

**SAY:** "`[:3]` — everything from the start up to, but not including, index 3. `[-2:]` — everything from the second-to-last item to the end. `[::2]` — every second item, starting from index 0: positions 0, 2, 4 — `'pen'`, `'stapler'`, `'marker'`."

---

### EXERCISE 4 — Modify (4:20–5:50)

**SAY:** "Three mutations in sequence, printing after each one so you can watch the list actually change."

**DO:**
```python
inventory.append("envelope")
print(inventory)

inventory.remove("tape")
print(inventory)

inventory.sort()
print(inventory)
```
```bash
python3 inventory.py
```

**CHECK:**
```
['pen', 'notebook', 'stapler', 'tape', 'marker', 'envelope']
['pen', 'notebook', 'stapler', 'marker', 'envelope']
['envelope', 'marker', 'notebook', 'pen', 'stapler']
```

**SAY:** "`.append()` adds to the end. `.remove()` deletes the *first* item matching that exact value — `'tape'` disappears from the middle, everything after it shifts left. `.sort()` reorders in place, alphabetically for strings — note it's `'envelope'` first now, not `'pen'`, because sorting doesn't care about insertion order, only alphabetical order."

---

### EXERCISE 5 — Tuple Comparison (5:50–7:30)

**SAY:** "A completely different data structure — a tuple — used specifically because it *can't* be changed after creation. That immutability is the whole point for something like GPS coordinates."

**DO:**
```python
coords = (40.7128, -74.0060)   # NYC

try:
    coords[0] = 99
except TypeError as e:
    print(f"Caught an error: {e}")
    print("Tuples are immutable — useful for coordinates because a location's")
    print("latitude/longitude shouldn't be accidentally reassigned partway through a program.")

print(coords)
```
```bash
python3 inventory.py
```

**CHECK:**
```
Caught an error: 'tuple' object does not support item assignment
Tuples are immutable — useful for coordinates because a location's
latitude/longitude shouldn't be accidentally reassigned partway through a program.
(40.7128, -74.006)
```

**SAY:** "Without the `try`/`except`, that `TypeError` would have crashed the whole script right there. Catching it lets the program acknowledge the error, explain it, and keep running — and the final `print(coords)` confirms the original tuple is completely untouched, exactly as it was created."

---

### EXERCISE 6 — Average of a List of Sales (7:30–8:50)

**SAY:** "Now built-in functions doing the accumulator work from Module 6 in a single call each — `sum()`, `len()`, `max()`, `min()`."

**DO:**
```python
sales = [100, 250, 75, 480, 200]

total = sum(sales)
count = len(sales)
average = total / count

print(f"Total: {total}")
print(f"Average: {average}")
print(f"Best: {max(sales)}")
print(f"Worst: {min(sales)}")
```
```bash
python3 inventory.py
```

**CHECK:**
```
Total: 1105
Average: 221.0
Best: 480
Worst: 75
```
Confirm by hand: `100+250+75+480+200 = 1105`, and `1105 / 5 = 221.0`.

---

### EXERCISE 7 — Accumulator Pattern (8:50–10:10)

**SAY:** "Same accumulator shape as Module 6, but instead of accumulating a single number, we're building up an entire new list, one `.append()` at a time."

**DO:**
```python
prices = [9.99, 14.99, 4.99, 24.99, 1.99]
discounted = []

for price in prices:
    discounted.append(round(price * 0.9, 2))

print(prices)
print(discounted)
```
```bash
python3 inventory.py
```

**CHECK:**
```
[9.99, 14.99, 4.99, 24.99, 1.99]
[8.99, 13.49, 4.49, 22.49, 1.79]
```
Spot-check one: `9.99 × 0.9 = 8.991`, and `round(8.991, 2)` gives `8.99`.

**SAY:** "`discounted = []` is the initialize step — an *empty* list this time, not zero. `.append()` inside the loop is the update step. And the original `prices` list is completely untouched — we built a brand-new list rather than modifying the old one in place."

---

### EXERCISE 8 — Filter Above Threshold (10:10–11:40)

**SAY:** "Same filtering idea from Module 6's `if` inside a loop, but now the output is a whole new list, not just a count."

**DO:**
```python
sales = [340, 127, 589, 204, 467, 88, 731, 315, 62, 490]
high_sales = []

for amount in sales:
    if amount > 300:
        high_sales.append(amount)

print(high_sales)
print(len(high_sales))
print(sum(high_sales) / len(high_sales))
```
```bash
python3 inventory.py
```

**CHECK:**
```
[340, 589, 467, 731, 315, 490]
6
488.6666666666667
```
Confirm: six values clear 300 — `340, 589, 467, 731, 315, 490` — and their sum, `2,932`, divided by `6`, gives roughly `488.67`.

---

### REFLECTION QUESTIONS (11:40–12:20)

**SAY:** "Add these as a comment block at the very top of the file."

**DO:** Answer, 2–3 sentences each:
1. What is the most surprising thing about how lists work in Python compared to what you expected coming in?
2. Describe one real business situation — from a job you've had, an internship, or a class — where a Python list would have saved you time compared to doing it manually in Excel.

**CHECK:** Question 1's answer is a real test of whether today's material actually surprised you — common honest answers involve negative indexing, mutation-in-place vs. creating a new list, or the fact that slicing never raises an error even for out-of-range positions.

---

### SUBMISSION CHECKLIST (12:20–end)

- [ ] `inventory.py` — filename matches exactly, lowercase
- [ ] Exercise 1–3: list creation, indexing, and slicing all correct
- [ ] Exercise 4: append/remove/sort shown step by step
- [ ] Exercise 5: `TypeError` caught with `try`/`except`, explanation printed
- [ ] Exercise 6: sum, average, max, min all correct
- [ ] Exercise 7: `discounted` list built with the accumulator pattern
- [ ] Exercise 8: `high_sales` filtered correctly, with count and average
- [ ] Reflection comment block at the top of the file, both questions answered
- [ ] Pushed to GitHub in a `week10/` folder
- [ ] Repo URL submitted to Canvas
