# ISM2411 Lab 10 Code-Along — Inventory List Manager

**Build one script, `inventory.py`, that manages a product inventory with lists, indexing, slicing, list methods and a tuple.**

Type along, one exercise at a time. Run the file after each one and compare with the **You should see** block. Every output below is a real run of the code shown.

| | |
|---|---|
| **File** | `ism2411/week10/inventory.py`, one file holding all 8 exercises |
| **Time** | About one lab session |
| **Builds on** | `for` loops and `if` (Modules 5–6), f-strings (Module 3), the GitHub workflow (Module 8) |
| **New this week** | Lists, indexing, slicing, list methods, tuples. Two small extras the lab needs: `try`/`except` (Exercise 5) and `round()` (Exercise 7) |
| **You submit** | Your GitHub repo URL in Canvas |

### Contents

0. [Five-minute refresher](#0-five-minute-refresher)
1. [Set up the file](#1-set-up-the-file)
2. [Exercises 1–3: build, index and slice](#exercise-1--build-the-list)
3. [Exercise 4: modify the list](#exercise-4--modify)
4. [Exercise 5: tuples](#exercise-5--tuple-comparison)
5. [Exercises 6–8: sales numbers](#exercise-6--average-of-a-list-of-sales)
6. [The finished file and full run](#the-finished-file)
7. [Submit](#submit)
8. [When something breaks](#when-something-breaks)

---

## 0. Five-minute refresher

*From the reading and lecture.* Everything the lab uses:

```python
inventory = ["pen", "notebook", "stapler", "tape"]

inventory[0]        # 'pen'      indexes start at 0
inventory[-1]       # 'tape'     negative indexes count from the end
inventory[1:3]      # ['notebook', 'stapler']   start included, stop excluded
"pen" in inventory  # True       membership test

inventory.append("marker")   # add to the end
inventory.remove("tape")     # delete the first matching value
inventory.sort()             # sort in place, and returns None
len(inventory)               # how many items

coords = (40.7128, -74.0060)  # a tuple: like a list, but can't be changed
```

**List or tuple?** Use a **list** when the collection changes over time, like an inventory, a cart or a daily sales log. Use a **tuple** for a fixed record that should never change, like a GPS coordinate or a database row. The tuple tells the reader *this data stays put*, and Python enforces that.

> **The trap everyone falls into:** `sorted_items = items.sort()` makes `sorted_items` equal `None`. `.sort()` changes the original list and returns nothing. If you want a sorted *copy*, use `sorted(items)`.

---

## 1. Set up the file

Open VS Code's terminal (**View → Terminal**) and go to your course repo from Module 8:

```bash
cd ~/ism2411
git pull
mkdir week10
code week10/inventory.py
```

`git pull` brings down anything you changed on github.com, so your next push isn't rejected.

Paste this header at the top of the file. The lab requires your two reflection answers in a comment block at the top, so leave the placeholders now and fill them in at the end.

```python
# inventory.py
# Author: [Your Name]
# Module 10 Lab: Inventory List Manager
#
# Reflection 1: What surprised me most about how lists work in Python:
#   [2-3 sentences]
#
# Reflection 2: A business situation where a Python list would have saved me time:
#   [2-3 sentences]
```

To run the file, use this from inside `~/ism2411`. On a Mac, type `python3` if `python` isn't found.

```bash
python week10/inventory.py
```

Each exercise below starts with a `print("--- Exercise N ---")` line, so the output is easy to read and easy to grade.

---

## Exercise 1 — Build the list

**Goal:** create the inventory, print it, then print how many items it holds.

```python
# --- Exercise 1: Build the list ---
print("--- Exercise 1 ---")
inventory = ["pen", "notebook", "stapler", "tape", "marker"]
print(inventory)
print(len(inventory))
```

**You should see:**

```text
--- Exercise 1 ---
['pen', 'notebook', 'stapler', 'tape', 'marker']
5
```

**Why:** square brackets with commas make a list, and `len()` counts its items. Think of `inventory` as one spreadsheet column: one variable holding five rows.

---

## Exercise 2 — Index practice

**Goal:** print the first, last and middle items. **Don't hard-code the middle position.** Compute it from `len(inventory)`.

```python
# --- Exercise 2: Index practice ---
print("--- Exercise 2 ---")
print(inventory[0])  # first item
print(inventory[-1])  # last item
middle = len(inventory) // 2
print(inventory[middle])  # middle item
```

**You should see:**

```text
--- Exercise 2 ---
pen
marker
stapler
```

**Why:**

- Five items have indexes `0, 1, 2, 3, 4`, so the first is `[0]`.
- `[-1]` is always the last item, however long the list is. That matters when you don't know the length in advance.
- `//` is floor division, which divides and drops the remainder: `5 // 2` is `2`, and `inventory[2]` is `"stapler"`. Because it is computed from `len()`, the line still works if the list grows.

---

## Exercise 3 — Slicing

**Goal:** print the first three items, the last two, and every other item.

```python
# --- Exercise 3: Slicing ---
print("--- Exercise 3 ---")
print(inventory[:3])  # first three
print(inventory[-2:])  # last two
print(inventory[::2])  # every other item
```

**You should see:**

```text
--- Exercise 3 ---
['pen', 'notebook', 'stapler']
['tape', 'marker']
['pen', 'stapler', 'marker']
```

**Why:**

- `[start:stop]` includes `start` and **excludes** `stop`. Leaving out `start` means *from the beginning*, and leaving out `stop` means *to the end*.
- `[-2:]` starts two from the end and runs to the end.
- `[::2]` adds a **step**: take index 0, skip one, take index 2, skip one, take index 4.
- A slice always returns a **new** list. The original `inventory` hasn't changed.

---

## Exercise 4 — Modify

**Goal:** append `"envelope"`, remove `"tape"`, sort, and print after each step so you can watch the list change.

```python
# --- Exercise 4: Modify ---
print("--- Exercise 4 ---")
inventory.append("envelope")
print(inventory)
inventory.remove("tape")
print(inventory)
inventory.sort()
print(inventory)
```

**You should see:**

```text
--- Exercise 4 ---
['pen', 'notebook', 'stapler', 'tape', 'marker', 'envelope']
['pen', 'notebook', 'stapler', 'marker', 'envelope']
['envelope', 'marker', 'notebook', 'pen', 'stapler']
```

**Why:**

- **These methods change the list in place.** There's no `inventory = ...` on any line, yet the list is different each time you print it.
- `.append()` adds to the end. `.remove("tape")` deletes the first item equal to `"tape"`, matching by **value**, not by position. `.sort()` puts strings in alphabetical order.
- Don't write `inventory = inventory.sort()`. That replaces your list with `None`.

> **Order matters in one file.** Exercises 2 and 3 run *before* this one, so they see the original five items. If you move Exercise 4 higher up, their output changes.

---

## Exercise 5 — Tuple comparison

**Goal:** make a tuple of NYC's coordinates, try to change it, **catch** the error, explain why tuples suit coordinates, and print the tuple unchanged.

**New syntax: `try` / `except`.** Python runs the `try` block. If a line in it raises the named error, Python jumps to the `except` block instead of crashing, then carries on below. `as error` keeps the error message so you can print it.

```python
# --- Exercise 5: Tuple comparison ---
print("--- Exercise 5 ---")
coords = (40.7128, -74.0060)
try:
    coords[0] = 99
except TypeError as error:
    print("TypeError caught:", error)
    print("Tuples protect coordinates: a location should never change by accident.")
print(coords)
```

**You should see:**

```text
--- Exercise 5 ---
TypeError caught: 'tuple' object does not support item assignment
Tuples protect coordinates: a location should never change by accident.
(40.7128, -74.006)
```

**Why:**

- `coords[0] = 99` would work on a list. On a tuple, Python refuses with a `TypeError`. **The immutability is the feature.** A coordinate pair that changes by accident is a bug, and the tuple makes that bug impossible.
- The last line prints `-74.006`, not `-74.0060`. Python drops trailing zeros on floats, and the value is the same.
- You can write your own explanation sentence. It just has to say why tuples fit coordinates.

> **Try it without `try`.** Comment out the `try:` and `except` lines, unindent `coords[0] = 99`, and run the file. You'll see the crash that `except` was catching: `TypeError: 'tuple' object does not support item assignment`. Put it back before you move on.

---

## Exercise 6 — Average of a list of sales

**Goal:** for `sales = [100, 250, 75, 480, 200]`, print the total, count, average, best day and worst day using `sum()`, `len()`, `max()` and `min()`.

```python
# --- Exercise 6: Average of a list of sales ---
print("--- Exercise 6 ---")
sales = [100, 250, 75, 480, 200]
total = sum(sales)
count = len(sales)
average = total / count
print(f"Total: {total}")
print(f"Count: {count}")
print(f"Average: {average}")
print(f"Best: {max(sales)}")
print(f"Worst: {min(sales)}")
```

**You should see:**

```text
--- Exercise 6 ---
Total: 1105
Count: 5
Average: 221.0
Best: 480
Worst: 75
```

**Why:** the average is the total divided by the count. `/` always gives a float, so the result prints as `221.0`, not `221`.

> **Exam practice: the loop version.** The lab says to use `max()` and `min()`, so use them here. On the exam's loop question, those built-ins **aren't accepted**, so practice the pattern by hand too. Start with the first item, then let each item challenge the current best and worst. This prints `480 75`:
>
> ```python
> best = sales[0]
> worst = sales[0]
> for amount in sales:
>     if amount > best:
>         best = amount
>     if amount < worst:
>         worst = amount
> print(best, worst)
> ```

---

## Exercise 7 — Accumulator pattern

**Goal:** build a new list, `discounted`, with every price cut by 10%, using a loop and `.append()`. Print both lists.

This is the most common list pattern in business scripts: **start with an empty list, loop, and append one result per item**. It's how you build a spreadsheet column one row at a time.

```python
# --- Exercise 7: Accumulator pattern ---
print("--- Exercise 7 ---")
prices = [9.99, 14.99, 4.99, 24.99, 1.99]
discounted = []
for price in prices:
    discounted.append(round(price * 0.9, 2))
print(prices)
print(discounted)
```

**You should see:**

```text
--- Exercise 7 ---
[9.99, 14.99, 4.99, 24.99, 1.99]
[8.99, 13.49, 4.49, 22.49, 1.79]
```

**Why:**

- `discounted = []` goes **before** the loop. If you put it inside, the list is emptied on every pass and ends with one item.
- `price * 0.9` keeps 90% of the price. For `9.99`, that's `8.991`.
- **New: `round(value, 2)`** rounds to 2 decimal places, so `8.991` becomes `8.99`. The list stores the rounded number. An f-string's `:.2f` only changes how a number *prints*, and it can't round the numbers stored inside a list.
- The original `prices` list is unchanged. You built a new list rather than changing the one you were looping over.

---

## Exercise 8 — Filter above threshold

**Goal:** keep only the days with sales **over 300** in a new list, `high_sales`. Print the list, its length, and the average of those days.

This is the same accumulator pattern with an `if` in front of the `append`.

```python
# --- Exercise 8: Filter above threshold ---
print("--- Exercise 8 ---")
sales = [340, 127, 589, 204, 467, 88, 731, 315, 62, 490]
high_sales = []
for amount in sales:
    if amount > 300:
        high_sales.append(amount)
print(high_sales)
print(f"Count: {len(high_sales)}")
print(f"Avg: {sum(high_sales) / len(high_sales):.2f}")
```

**You should see:**

```text
--- Exercise 8 ---
[340, 589, 467, 731, 315, 490]
Count: 6
Avg: 488.67
```

**Why:**

- Only values that pass `amount > 300` get appended, so `high_sales` keeps their original order.
- `:.2f` in the f-string displays `488.666...` as `488.67`. Here we only print the number, so formatting is enough and `round()` isn't needed.
- **Never remove items from `sales` while looping over it.** Python skips items when you do. Build a new list, as here. The lecture's "Common Errors" shows the broken version.
- Reusing the name `sales` is fine. Exercise 6 is finished with the old list.

---

## The finished file

<details>
<summary><b>Complete <code>week10/inventory.py</code></b> (check yours against it)</summary>

```python
# inventory.py
# Author: [Your Name]
# Module 10 Lab: Inventory List Manager
#
# Reflection 1: What surprised me most about how lists work in Python:
#   [2-3 sentences]
#
# Reflection 2: A business situation where a Python list would have saved me time:
#   [2-3 sentences]

# --- Exercise 1: Build the list ---
print("--- Exercise 1 ---")
inventory = ["pen", "notebook", "stapler", "tape", "marker"]
print(inventory)
print(len(inventory))

# --- Exercise 2: Index practice ---
print("--- Exercise 2 ---")
print(inventory[0])  # first item
print(inventory[-1])  # last item
middle = len(inventory) // 2
print(inventory[middle])  # middle item

# --- Exercise 3: Slicing ---
print("--- Exercise 3 ---")
print(inventory[:3])  # first three
print(inventory[-2:])  # last two
print(inventory[::2])  # every other item

# --- Exercise 4: Modify ---
print("--- Exercise 4 ---")
inventory.append("envelope")
print(inventory)
inventory.remove("tape")
print(inventory)
inventory.sort()
print(inventory)

# --- Exercise 5: Tuple comparison ---
print("--- Exercise 5 ---")
coords = (40.7128, -74.0060)
try:
    coords[0] = 99
except TypeError as error:
    print("TypeError caught:", error)
    print("Tuples protect coordinates: a location should never change by accident.")
print(coords)

# --- Exercise 6: Average of a list of sales ---
print("--- Exercise 6 ---")
sales = [100, 250, 75, 480, 200]
total = sum(sales)
count = len(sales)
average = total / count
print(f"Total: {total}")
print(f"Count: {count}")
print(f"Average: {average}")
print(f"Best: {max(sales)}")
print(f"Worst: {min(sales)}")

# --- Exercise 7: Accumulator pattern ---
print("--- Exercise 7 ---")
prices = [9.99, 14.99, 4.99, 24.99, 1.99]
discounted = []
for price in prices:
    discounted.append(round(price * 0.9, 2))
print(prices)
print(discounted)

# --- Exercise 8: Filter above threshold ---
print("--- Exercise 8 ---")
sales = [340, 127, 589, 204, 467, 88, 731, 315, 62, 490]
high_sales = []
for amount in sales:
    if amount > 300:
        high_sales.append(amount)
print(high_sales)
print(f"Count: {len(high_sales)}")
print(f"Avg: {sum(high_sales) / len(high_sales):.2f}")
```

</details>

**Full run** of `python week10/inventory.py`:

```text
--- Exercise 1 ---
['pen', 'notebook', 'stapler', 'tape', 'marker']
5
--- Exercise 2 ---
pen
marker
stapler
--- Exercise 3 ---
['pen', 'notebook', 'stapler']
['tape', 'marker']
['pen', 'stapler', 'marker']
--- Exercise 4 ---
['pen', 'notebook', 'stapler', 'tape', 'marker', 'envelope']
['pen', 'notebook', 'stapler', 'marker', 'envelope']
['envelope', 'marker', 'notebook', 'pen', 'stapler']
--- Exercise 5 ---
TypeError caught: 'tuple' object does not support item assignment
Tuples protect coordinates: a location should never change by accident.
(40.7128, -74.006)
--- Exercise 6 ---
Total: 1105
Count: 5
Average: 221.0
Best: 480
Worst: 75
--- Exercise 7 ---
[9.99, 14.99, 4.99, 24.99, 1.99]
[8.99, 13.49, 4.49, 22.49, 1.79]
--- Exercise 8 ---
[340, 589, 467, 731, 315, 490]
Count: 6
Avg: 488.67
```

### Now write your reflection

Replace the two `[2-3 sentences]` placeholders at the top with your own answers:

1. What is the most surprising thing about how lists work in Python compared to what you expected coming in? Possible starting points: zero-based indexing, the stop index being excluded, or `.sort()` returning `None`.
2. Describe one real business situation, from a job, an internship or a class, where a Python list would have saved you time compared to doing it manually in Excel.

---

## Submit

From inside `~/ism2411`:

```bash
git status
git add week10/
git commit -m "add module 10 inventory list manager: exercises 1-8 and reflection"
git push
```

Then open your repo on github.com, click into `week10/`, and confirm `inventory.py` is there with your reflection at the top.

**Canvas:** paste your GitHub repository URL. That is the only thing you submit. Don't upload the file.

- [ ] `week10/inventory.py` is in your `ism2411` repo on github.com
- [ ] It runs from top to bottom with no errors and includes Exercises 1–8
- [ ] The reflection comment block at the top is filled in, not placeholders
- [ ] The commit message describes the change
- [ ] The repo URL is pasted in Canvas

---

## When something breaks

| You see | Cause | Fix |
|---|---|---|
| `IndexError: list index out of range` | You asked for an index that doesn't exist. Five items stop at index 4, so `inventory[5]` fails | Use `[-1]` for the last item, or check `len()` |
| `ValueError: list.remove(x): x not in list` | `.remove()` couldn't find that exact value. Check the spelling and capitals, or whether it was already removed | Print the list just before the `.remove()` |
| A list prints as `None` | You wrote `inventory = inventory.sort()` | Write `inventory.sort()` on its own line |
| `TypeError: 'tuple' object does not support item assignment`, and the program stops | The assignment isn't inside `try:`, or the `except` names a different error | Indent `coords[0] = 99` under `try:` and use `except TypeError` |
| `discounted` ends up with only one number | `discounted = []` is inside the loop | Move it above the `for` line |
| `ZeroDivisionError: division by zero` in Exercise 8 | `high_sales` is empty, so `len()` is 0. Check your `if` condition | It should be `amount > 300` |
| `can't open file ... No such file or directory` | The terminal isn't in `~/ism2411`, or the folder is named differently | `cd ~/ism2411`, then `ls week10` |
| `git push` is rejected | You edited something on github.com | `git pull`, then `git push` |

### Lecture discussion questions to try

*From the lecture.* If you finish early, try these with your new script:

- **Rolling window.** Keep only the last 10 daily sales. After each `.append()`, how could a slice like `[-10:]` drop the oldest?
- **Why tuples?** A colleague says "just use a list and don't change it." What does immutability protect against that good intentions don't?
- **`.sort()` or `sorted()`?** Describe a business case where you need the original order preserved.
