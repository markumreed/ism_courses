# ISM2411 Lab 12 Code-Along — Read a Sales CSV, Write a Cleaned Report

**Build one script, `csv_practice.py`, that reads a sales CSV, totals every order, writes the high-value orders to a new CSV, adds up revenue by product, and keeps a log that grows by one line each time it runs.**

Type along, one exercise at a time. Run the file after each one and compare with the **You should see** block. Every output below is a real run of the code shown, on the sample `sales.csv` in Step 1.

| | |
|---|---|
| **Files** | `ism2411/week12/csv_practice.py`, one file holding all 8 exercises. It reads `week12/data/sales.csv` and writes `week12/data/cleaned.csv` and `week12/data/run_log.txt` |
| **Time** | About one lab session |
| **Builds on** | Dictionaries and `.get()` (Module 11), lists and the accumulator pattern (Module 10), `for` loops and `if` (Modules 5–6), f-strings (Module 3), the GitHub workflow (Module 8) |
| **New this week** | `open()` and its modes, `with`, `csv.reader`, `next()`, `csv.writer` with `newline=""`, `csv.DictReader`, relative paths, append mode |
| **You submit** | Your GitHub repo URL in Canvas |

### Contents

0. [Five-minute refresher](#0-five-minute-refresher)
1. [Set up the folder and the data](#1-set-up-the-folder-and-the-data)
2. [Exercises 1–4: read the file](#exercise-1--get-the-file)
3. [Exercise 5: write a cleaned file](#exercise-5--filter-and-write)
4. [Exercises 6–8: read by name, summarize, log](#exercise-6--csvdictreader)
5. [The finished file and full run](#the-finished-file)
6. [Submit](#submit)
7. [When something breaks](#when-something-breaks)

---

## 0. Five-minute refresher

*From the reading and lecture.* Read this one, don't type it. It's everything the lab uses:

```python
import csv

with open("data/sales.csv", "r") as f:   # "r" read, "w" write, "a" append
    reader = csv.reader(f)               # each row comes back as a list of strings
    header = next(reader)                # take one row off the top: the header
    for row in reader:                   # so the loop starts at the first data row
        print(row)
# Here the file is already closed, even if something inside the block failed.

with open("data/out.csv", "w", newline="") as f:   # "w" empties the file first
    writer = csv.writer(f)
    writer.writerow(["Product", "Total"])          # one row per call

with open("data/sales.csv", "r") as f:
    for row in csv.DictReader(f):        # each row is a dictionary keyed by the header
        print(row["price"])
```

**Every value is a string.** `'9.99'` looks like a number, but the `csv` module never converts anything. `row[1] * row[2]` stops with `TypeError: can't multiply sequence by non-int of type 'str'`. Convert first: `float(row[1]) * int(row[2])`. (A string times a whole number does run, and repeats the string: `"ab" * 3` is `'ababab'`. That's why `"9.99" * 50` gives fifty copies of `9.99` instead of an error.)

> **`"w"` empties the file the moment it opens,** before you write anything. Use it for a file you rebuild on every run (`cleaned.csv`). Use `"a"` for a file that should keep its history (`run_log.txt`). Exercise 8 shows the difference.

---

## 1. Set up the folder and the data

Open VS Code's terminal (**View → Terminal**) and go to your course repo:

```bash
cd ~/ism2411
git pull
mkdir -p week12/data
```

`mkdir -p` makes `week12` and the `data` folder inside it in one step. `git pull` brings down anything you changed on github.com, so your next push isn't rejected.

**Get `sales.csv`.** Download it from Canvas and drag it into `week12/data/` in VS Code's Explorer. To follow this code-along number for number, or if you don't have the Canvas file yet, make your own instead: run `code week12/data/sales.csv`, paste these 13 lines, and save.

```text
product,price,quantity
Widget A,9.99,50
Widget B,24.50,3
Gadget C,149.00,2
Cable D,4.25,12
Widget A,9.99,8
Gadget C,149.00,3
Adapter E,12.75,10
Cable D,4.25,40
Widget B,24.50,6
Adapter E,12.75,4
Widget A,9.99,15
Stand F,39.99,2
```

> **Using the Canvas file?** Your products and totals will differ from the outputs below, but every exercise prints the same kind of thing. The Canvas file needs the same three columns, in this order: `product,price,quantity`.

Now move into the week folder and create the script:

```bash
cd week12
code csv_practice.py
```

**Run everything from inside `~/ism2411/week12` this week.** The script opens `"data/sales.csv"`, a *relative* path, and Python looks for it starting from the folder your terminal is in, not the folder the script is in. From `~/ism2411`, that path means `~/ism2411/data/sales.csv`, which doesn't exist. Lab 11 ran from `~/ism2411`; this lab doesn't.

Paste this header at the top of the file. The lab requires your two reflection answers in a comment block at the top, so leave the placeholders now and fill them in at the end.

```python
# csv_practice.py
# Author: [Your Name]
# Module 12 Lab: Read a Sales CSV, Write a Cleaned Report
#
# Reflection 1: How this pipeline compares to doing the same task in Excel,
# what Python can do that Excel can't do easily, and the reverse:
#   [2-3 sentences]
#
# Reflection 2: A real business process that would benefit from an
# append-mode log file, and why append mode is the right tool:
#   [2-3 sentences]
```

Under it, the imports and the three file paths:

```python
import csv
from datetime import datetime

SALES_FILE = "data/sales.csv"
CLEANED_FILE = "data/cleaned.csv"
LOG_FILE = "data/run_log.txt"
```

- `import csv` brings in Python's built-in CSV module. `from datetime import datetime` is for Exercise 8.
- The paths are **constants**, named in capitals by convention. Every exercise uses `SALES_FILE`, so if the file moves, you change one line.

To run the file:

```bash
python3 csv_practice.py
```

In Ubuntu on Windows and on a Mac, the command is `python3`. Each exercise starts with a `print("--- Exercise N ---")` line, so the output is easy to read and easy to grade.

> **Each exercise opens the file again.** A reader hands out each row once. When a loop has gone through every row, the reader is used up, and a second loop over it prints nothing, with no error. Opening the file again starts from the top.

---

## Exercise 1 — Get the file

**Goal:** confirm that `sales.csv` is at the path the script uses, has the header `product,price,quantity`, and has at least 10 data rows.

Check it from the terminal first:

```bash
head -3 data/sales.csv
wc -l data/sales.csv
```

```text
product,price,quantity
Widget A,9.99,50
Widget B,24.50,3
13 data/sales.csv
```

`head -3` shows the first three lines: the header and two data rows. `wc -l` counts lines. 13 is the header plus 12 orders.

Then open it from Python:

```python
# --- Exercise 1: Get the file ---
print("--- Exercise 1 ---")
with open(SALES_FILE, "r") as f:
    print(f"Opened {SALES_FILE}")
```

**You should see:**

```text
--- Exercise 1 ---
Opened data/sales.csv
```

**Why:**

- `open(SALES_FILE, "r")` opens the file for reading. Always write the mode, even though `"r"` is the default, so the next person can see what the code does to the file.
- `with ... as f:` gives the open file the name `f` and closes it when the indented block ends. There's no `f.close()` to forget.
- No output except the message means it worked. A wrong path stops the program here with `FileNotFoundError`, before anything else runs. See [When something breaks](#when-something-breaks).

---

## Exercise 2 — Read and print raw rows

**Goal:** use `csv.reader` in a `with` block to print every row, header included, and notice that every value is a string.

```python
# --- Exercise 2: Read and print raw rows ---
print("--- Exercise 2 ---")
with open(SALES_FILE, "r") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
```

**You should see:**

```text
--- Exercise 2 ---
['product', 'price', 'quantity']
['Widget A', '9.99', '50']
['Widget B', '24.50', '3']
['Gadget C', '149.00', '2']
['Cable D', '4.25', '12']
['Widget A', '9.99', '8']
['Gadget C', '149.00', '3']
['Adapter E', '12.75', '10']
['Cable D', '4.25', '40']
['Widget B', '24.50', '6']
['Adapter E', '12.75', '4']
['Widget A', '9.99', '15']
['Stand F', '39.99', '2']
```

**Why:**

- `csv.reader(f)` reads the file one row at a time and splits each line at the commas. Each row is a **list**.
- Every value has quotes around it, so every value is a string: `'9.99'`, `'50'`. Python can't do arithmetic on these until you convert them.
- The header row prints too. `csv.reader` doesn't know the first line is special. Exercise 3 deals with that.
- Why not `line.split(",")`? A value like `"1,299.00"` or `"123 Main St, Suite 4"` has a comma inside quotes. `csv.reader` keeps it in one piece, and `split` cuts it in two.

---

## Exercise 3 — Skip the header

**Goal:** take the header off with `next(reader)`, keep it in a variable, print it once, then print only the data rows.

```python
# --- Exercise 3: Skip the header ---
print("--- Exercise 3 ---")
with open(SALES_FILE, "r") as f:
    reader = csv.reader(f)
    header = next(reader)
    print(f"Header: {header}")
    for row in reader:
        print(row)
```

**You should see:**

```text
--- Exercise 3 ---
Header: ['product', 'price', 'quantity']
['Widget A', '9.99', '50']
['Widget B', '24.50', '3']
['Gadget C', '149.00', '2']
['Cable D', '4.25', '12']
['Widget A', '9.99', '8']
['Gadget C', '149.00', '3']
['Adapter E', '12.75', '10']
['Cable D', '4.25', '40']
['Widget B', '24.50', '6']
['Adapter E', '12.75', '4']
['Widget A', '9.99', '15']
['Stand F', '39.99', '2']
```

**Why:** `next(reader)` takes exactly one row from the reader and returns it. Here that's the header, saved in `header`. The `for` loop then picks up where the reader is, at the first data row. The header is printed once with its label, and it no longer appears in the list of rows.

---

## Exercise 4 — Compute totals

**Goal:** for each row, convert the price and quantity, compute price × quantity, and print a line like `Widget A: 50 units × $9.99 = $499.50`. After the loop, print the total revenue.

```python
# --- Exercise 4: Compute totals ---
print("--- Exercise 4 ---")
total_revenue = 0
with open(SALES_FILE, "r") as f:
    reader = csv.reader(f)
    next(reader)  # skip the header row
    for row in reader:
        product, price_str, qty_str = row
        price = float(price_str)
        quantity = int(qty_str)
        total = price * quantity
        total_revenue += total
        print(f"{product}: {quantity} units × ${price:.2f} = ${total:.2f}")
print(f"Total revenue: ${total_revenue:,.2f}")
```

**You should see:**

```text
--- Exercise 4 ---
Widget A: 50 units × $9.99 = $499.50
Widget B: 3 units × $24.50 = $73.50
Gadget C: 2 units × $149.00 = $298.00
Cable D: 12 units × $4.25 = $51.00
Widget A: 8 units × $9.99 = $79.92
Gadget C: 3 units × $149.00 = $447.00
Adapter E: 10 units × $12.75 = $127.50
Cable D: 40 units × $4.25 = $170.00
Widget B: 6 units × $24.50 = $147.00
Adapter E: 4 units × $12.75 = $51.00
Widget A: 15 units × $9.99 = $149.85
Stand F: 2 units × $39.99 = $79.98
Total revenue: $2,174.25
```

**Why:**

- `product, price_str, qty_str = row` **unpacks** the three-item list into three names in one line. It needs exactly three values. A row with fewer stops with `ValueError: not enough values to unpack`, and a row with more stops with `ValueError: too many values to unpack (expected 3)`.
- `float(price_str)` and `int(qty_str)` turn the strings into numbers. Price has cents, so it's a `float`. Quantity is a whole number, so it's an `int`.
- `total_revenue` is the accumulator from Module 10: start at 0 before the loop, add inside it, print after it.
- `:.2f` shows two decimal places. `:,.2f` adds the thousands comma, for `$2,174.25`.
- The `×` sign is copied from the lab. On a keyboard without it, a lowercase `x` is fine.

> **Two `Widget A` lines?** The file has three Widget A orders. Each row is one order, not one product. Exercise 7 adds them up per product.

---

## Exercise 5 — Filter and write

**Goal:** write `data/cleaned.csv` with only the orders whose total is over $100, under the header `Product,Price,Qty,Total`. Open it with `newline=""`, and print how many rows were written out of how many were read.

```python
# --- Exercise 5: Filter and write ---
print("--- Exercise 5 ---")
high_value = []
rows_read = 0
with open(SALES_FILE, "r") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        rows_read += 1
        product, price_str, qty_str = row
        price = float(price_str)
        quantity = int(qty_str)
        total = price * quantity
        if total > 100:
            high_value.append([product, f"{price:.2f}", quantity, f"{total:.2f}"])

with open(CLEANED_FILE, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Product", "Price", "Qty", "Total"])
    for row in high_value:
        writer.writerow(row)
print(f"Wrote {len(high_value)} of {rows_read} rows to {CLEANED_FILE}")
```

**You should see:**

```text
--- Exercise 5 ---
Wrote 7 of 12 rows to data/cleaned.csv
```

Open `data/cleaned.csv` in VS Code, or print it from the terminal with `cat data/cleaned.csv`:

```text
Product,Price,Qty,Total
Widget A,9.99,50,499.50
Gadget C,149.00,2,298.00
Gadget C,149.00,3,447.00
Adapter E,12.75,10,127.50
Cable D,4.25,40,170.00
Widget B,24.50,6,147.00
Widget A,9.99,15,149.85
```

**Why:**

- The first `with` block is **extract and transform**: read every row, compute the total, and keep only the ones over $100 in the list `high_value`. The second is **load**: write them out. That's a complete ETL pipeline.
- `rows_read` counts every data row, kept or not, so the summary line can say *7 of 12*.
- Each kept row is a list in the order of the new header. `f"{price:.2f}"` and `f"{total:.2f}"` store the money as `149.00`, not `149.0` or `499.50000000000006`.
- `"w"` creates the file, or empties it if it's there. Run the script again and you get the same seven rows, not fourteen.
- `newline=""` lets the `csv` module control line endings. Without it, Python running on Windows adds an extra line ending to every row, which Excel shows as an empty row between rows. Always use it when you write a CSV.
- `writer.writerow(...)` writes one row. `writer.writerows(high_value)` would write the whole list in one call. Both give the same file.

---

## Exercise 6 — csv.DictReader

**Goal:** read the same file with `csv.DictReader`, reach the values by column name, and check that the totals match Exercise 4. Add a two-line comment comparing the two readers.

```python
# --- Exercise 6: csv.DictReader ---
print("--- Exercise 6 ---")
# csv.reader gives each row as a list, so the code must know that price is row[1].
# csv.DictReader names each value by its header, so row["price"] still works if the columns move.
dict_total = 0
with open(SALES_FILE, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        price = float(row["price"])
        quantity = int(row["quantity"])
        total = price * quantity
        dict_total += total
        print(f"{row['product']}: {quantity} units × ${price:.2f} = ${total:.2f}")
print(f"Total revenue: ${dict_total:,.2f}")
```

**You should see:**

```text
--- Exercise 6 ---
Widget A: 50 units × $9.99 = $499.50
Widget B: 3 units × $24.50 = $73.50
Gadget C: 2 units × $149.00 = $298.00
Cable D: 12 units × $4.25 = $51.00
Widget A: 8 units × $9.99 = $79.92
Gadget C: 3 units × $149.00 = $447.00
Adapter E: 10 units × $12.75 = $127.50
Cable D: 40 units × $4.25 = $170.00
Widget B: 6 units × $24.50 = $147.00
Adapter E: 4 units × $12.75 = $51.00
Widget A: 15 units × $9.99 = $149.85
Stand F: 2 units × $39.99 = $79.98
Total revenue: $2,174.25
```

**Why:**

- `csv.DictReader` uses the header row as the keys, so each row is a **dictionary**: `{'product': 'Widget A', 'price': '9.99', 'quantity': '50'}`. It takes the header itself, so there's no `next(reader)`.
- `row["price"]` says what it is. `row[1]` only works as long as price stays the second column.
- The values are still strings. `DictReader` names them but doesn't convert them.
- The total, `$2,174.25`, matches Exercise 4. The two readers see the same data.
- Inside the f-string, the key has **single** quotes: `{row['product']}`. The f-string itself uses double quotes.

**Write your own two-line comment.** Ours says why `DictReader` survives a column change. Yours should say when you'd pick each one. For example, `csv.reader` for a file with no header, and `DictReader` when there is one.

---

## Exercise 7 — Sales summary by product

**Goal:** build a dictionary `{product_name: total_revenue}`, adding up products that appear on more than one row, and print it sorted by product name.

```python
# --- Exercise 7: Sales summary by product ---
print("--- Exercise 7 ---")
summary = {}
with open(SALES_FILE, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        product = row["product"]
        total = float(row["price"]) * int(row["quantity"])
        summary[product] = summary.get(product, 0) + total
for product in sorted(summary):
    print(f"{product}: ${summary[product]:,.2f}")
```

**You should see:**

```text
--- Exercise 7 ---
Adapter E: $178.50
Cable D: $221.00
Gadget C: $745.00
Stand F: $79.98
Widget A: $729.27
Widget B: $220.50
```

**Why:**

- This is Lab 11's summary pattern on real data. `summary.get(product, 0)` returns the running total so far, or 0 the first time a product shows up. Adding this row's total and storing it back keeps the sum growing.
- `summary[product] += total` on its own stops with `KeyError: 'Widget A'` on the first row, because the key isn't there yet.
- Widget A appears on three rows: $499.50 + $79.92 + $149.85 = $729.27. Gadget C: $298.00 + $447.00 = $745.00. Twelve orders become six products.
- `sorted(summary)` gives the keys in alphabetical order. The dictionary itself keeps the order the products first appeared.

---

## Exercise 8 — Append mode log

**Goal:** each time the script runs, add one line to `data/run_log.txt` with the date and time and the total revenue. Run the script three times. The log should have three lines, not one.

```python
# --- Exercise 8: Append mode log ---
print("--- Exercise 8 ---")
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
with open(LOG_FILE, "a") as f:
    f.write(f"{timestamp} total revenue ${total_revenue:,.2f}\n")

entries = 0
with open(LOG_FILE, "r") as f:
    for line in f:
        entries += 1
        print(line.strip())
print(f"Log entries so far: {entries}")
```

**You should see, on the first run:**

```text
--- Exercise 8 ---
2026-11-02 09:13:34 total revenue $2,174.25
Log entries so far: 1
```

**Run it two more times.** On the third run, Exercise 8 shows:

```text
--- Exercise 8 ---
2026-11-02 09:13:34 total revenue $2,174.25
2026-11-02 09:13:35 total revenue $2,174.25
2026-11-02 09:13:36 total revenue $2,174.25
Log entries so far: 3
```

Your dates and times will be different. The count is what matters: one more line per run.

**Why:**

- `"a"` opens the file for **appending**. It creates the file if it isn't there, and otherwise writes after the last line, keeping what's already in it. With `"w"`, every run would wipe the log and the count would always be 1.
- `f.write(...)` writes exactly the text you give it, with no newline at the end. The `\n` at the end of the f-string makes each run start a new line.
- `datetime.now()` is the current date and time. `.strftime("%Y-%m-%d %H:%M:%S")` formats it as year-month-day hour:minute:second. You could also write `{datetime.now()}`, which adds fractions of a second.
- The second block reads the log back and counts its lines with an accumulator. `line.strip()` removes the newline at the end of each line, so `print` doesn't double-space them.
- `total_revenue` comes from Exercise 4. That's why the exercises stay in order, in one file.

---

## The finished file

<details>
<summary><b>The whole <code>csv_practice.py</code></b></summary>

```python
# csv_practice.py
# Author: [Your Name]
# Module 12 Lab: Read a Sales CSV, Write a Cleaned Report
#
# Reflection 1: How this pipeline compares to doing the same task in Excel,
# what Python can do that Excel can't do easily, and the reverse:
#   [2-3 sentences]
#
# Reflection 2: A real business process that would benefit from an
# append-mode log file, and why append mode is the right tool:
#   [2-3 sentences]

import csv
from datetime import datetime

SALES_FILE = "data/sales.csv"
CLEANED_FILE = "data/cleaned.csv"
LOG_FILE = "data/run_log.txt"

# --- Exercise 1: Get the file ---
print("--- Exercise 1 ---")
with open(SALES_FILE, "r") as f:
    print(f"Opened {SALES_FILE}")

# --- Exercise 2: Read and print raw rows ---
print("--- Exercise 2 ---")
with open(SALES_FILE, "r") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)

# --- Exercise 3: Skip the header ---
print("--- Exercise 3 ---")
with open(SALES_FILE, "r") as f:
    reader = csv.reader(f)
    header = next(reader)
    print(f"Header: {header}")
    for row in reader:
        print(row)

# --- Exercise 4: Compute totals ---
print("--- Exercise 4 ---")
total_revenue = 0
with open(SALES_FILE, "r") as f:
    reader = csv.reader(f)
    next(reader)  # skip the header row
    for row in reader:
        product, price_str, qty_str = row
        price = float(price_str)
        quantity = int(qty_str)
        total = price * quantity
        total_revenue += total
        print(f"{product}: {quantity} units × ${price:.2f} = ${total:.2f}")
print(f"Total revenue: ${total_revenue:,.2f}")

# --- Exercise 5: Filter and write ---
print("--- Exercise 5 ---")
high_value = []
rows_read = 0
with open(SALES_FILE, "r") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        rows_read += 1
        product, price_str, qty_str = row
        price = float(price_str)
        quantity = int(qty_str)
        total = price * quantity
        if total > 100:
            high_value.append([product, f"{price:.2f}", quantity, f"{total:.2f}"])

with open(CLEANED_FILE, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Product", "Price", "Qty", "Total"])
    for row in high_value:
        writer.writerow(row)
print(f"Wrote {len(high_value)} of {rows_read} rows to {CLEANED_FILE}")

# --- Exercise 6: csv.DictReader ---
print("--- Exercise 6 ---")
# csv.reader gives each row as a list, so the code must know that price is row[1].
# csv.DictReader names each value by its header, so row["price"] still works if the columns move.
dict_total = 0
with open(SALES_FILE, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        price = float(row["price"])
        quantity = int(row["quantity"])
        total = price * quantity
        dict_total += total
        print(f"{row['product']}: {quantity} units × ${price:.2f} = ${total:.2f}")
print(f"Total revenue: ${dict_total:,.2f}")

# --- Exercise 7: Sales summary by product ---
print("--- Exercise 7 ---")
summary = {}
with open(SALES_FILE, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        product = row["product"]
        total = float(row["price"]) * int(row["quantity"])
        summary[product] = summary.get(product, 0) + total
for product in sorted(summary):
    print(f"{product}: ${summary[product]:,.2f}")

# --- Exercise 8: Append mode log ---
print("--- Exercise 8 ---")
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
with open(LOG_FILE, "a") as f:
    f.write(f"{timestamp} total revenue ${total_revenue:,.2f}\n")

entries = 0
with open(LOG_FILE, "r") as f:
    for line in f:
        entries += 1
        print(line.strip())
print(f"Log entries so far: {entries}")
```

</details>

**Full run** of `python3 csv_practice.py`, starting with no `cleaned.csv` and no `run_log.txt`:

```text
--- Exercise 1 ---
Opened data/sales.csv
--- Exercise 2 ---
['product', 'price', 'quantity']
['Widget A', '9.99', '50']
['Widget B', '24.50', '3']
['Gadget C', '149.00', '2']
['Cable D', '4.25', '12']
['Widget A', '9.99', '8']
['Gadget C', '149.00', '3']
['Adapter E', '12.75', '10']
['Cable D', '4.25', '40']
['Widget B', '24.50', '6']
['Adapter E', '12.75', '4']
['Widget A', '9.99', '15']
['Stand F', '39.99', '2']
--- Exercise 3 ---
Header: ['product', 'price', 'quantity']
['Widget A', '9.99', '50']
['Widget B', '24.50', '3']
['Gadget C', '149.00', '2']
['Cable D', '4.25', '12']
['Widget A', '9.99', '8']
['Gadget C', '149.00', '3']
['Adapter E', '12.75', '10']
['Cable D', '4.25', '40']
['Widget B', '24.50', '6']
['Adapter E', '12.75', '4']
['Widget A', '9.99', '15']
['Stand F', '39.99', '2']
--- Exercise 4 ---
Widget A: 50 units × $9.99 = $499.50
Widget B: 3 units × $24.50 = $73.50
Gadget C: 2 units × $149.00 = $298.00
Cable D: 12 units × $4.25 = $51.00
Widget A: 8 units × $9.99 = $79.92
Gadget C: 3 units × $149.00 = $447.00
Adapter E: 10 units × $12.75 = $127.50
Cable D: 40 units × $4.25 = $170.00
Widget B: 6 units × $24.50 = $147.00
Adapter E: 4 units × $12.75 = $51.00
Widget A: 15 units × $9.99 = $149.85
Stand F: 2 units × $39.99 = $79.98
Total revenue: $2,174.25
--- Exercise 5 ---
Wrote 7 of 12 rows to data/cleaned.csv
--- Exercise 6 ---
Widget A: 50 units × $9.99 = $499.50
Widget B: 3 units × $24.50 = $73.50
Gadget C: 2 units × $149.00 = $298.00
Cable D: 12 units × $4.25 = $51.00
Widget A: 8 units × $9.99 = $79.92
Gadget C: 3 units × $149.00 = $447.00
Adapter E: 10 units × $12.75 = $127.50
Cable D: 40 units × $4.25 = $170.00
Widget B: 6 units × $24.50 = $147.00
Adapter E: 4 units × $12.75 = $51.00
Widget A: 15 units × $9.99 = $149.85
Stand F: 2 units × $39.99 = $79.98
Total revenue: $2,174.25
--- Exercise 7 ---
Adapter E: $178.50
Cable D: $221.00
Gadget C: $745.00
Stand F: $79.98
Widget A: $729.27
Widget B: $220.50
--- Exercise 8 ---
2026-11-02 09:13:34 total revenue $2,174.25
Log entries so far: 1
```

After three runs, `data/run_log.txt` holds:

```text
2026-11-02 09:13:34 total revenue $2,174.25
2026-11-02 09:13:35 total revenue $2,174.25
2026-11-02 09:13:36 total revenue $2,174.25
```

### Now write your reflection

Replace the two placeholders at the top of the file with 2–3 sentences each:

1. **This pipeline vs Excel.** You read a CSV, transformed it and wrote a new one. How does that compare with doing it in Excel? What can Python do that Excel can't do easily, and the other way round? Think about next week's file, a file with 500,000 rows, and someone who has to check your steps.
2. **An append-mode log.** Name a real business process that would benefit from a log like Exercise 8's, and say why append mode is the right tool. For example: a nightly import that records how many orders it loaded, so someone can see the night it loaded zero.

---

## Submit

From inside `~/ism2411/week12`, go back up one folder first, so `git add` picks up the whole week:

```bash
cd ~/ism2411
git status
git add week12/
git commit -m "add module 12 csv lab: exercises 1-8, cleaned report and run log"
git push
```

Then open your repo on github.com and click into `week12/`. You should see `csv_practice.py` and a `data/` folder holding `sales.csv`, `cleaned.csv` and `run_log.txt`.

**Canvas:** paste your GitHub repository URL. That is the only thing you submit. Don't upload the files.

- [ ] `week12/csv_practice.py` is in your `ism2411` repo on github.com, with Exercises 1–8
- [ ] It runs from top to bottom with no errors, from inside `week12`, and writes `data/cleaned.csv` and a new line in `data/run_log.txt`
- [ ] `data/cleaned.csv` and `data/run_log.txt` are pushed too, and the log has at least three lines
- [ ] The reflection comment block at the top is filled in, not placeholders
- [ ] The commit message describes the change
- [ ] The repo URL is pasted in Canvas

---

## When something breaks

| You see | Cause | Fix |
|---|---|---|
| `FileNotFoundError: [Errno 2] No such file or directory: 'data/sales.csv'` | The terminal is in the wrong folder, often `~/ism2411`, or the file is somewhere else | `cd ~/ism2411/week12`, then `ls data`. To see where Python is looking, `import os` and `print(os.getcwd())` |
| `TypeError: can't multiply sequence by non-int of type 'str'` | Two strings multiplied: `row[1] * row[2]` | Convert first: `float(row[1]) * int(row[2])` |
| `ValueError: could not convert string to float: 'price'` | The header row went into the math | `next(reader)` before the loop |
| `ValueError: could not convert string to float: '1,299.00'` | A price with a thousands comma | Remove it before converting: `float(price_str.replace(",", ""))` |
| `ValueError: not enough values to unpack (expected 3, got 0)` | A blank line in the middle of `sales.csv` | Delete the blank line |
| `ValueError: not enough values to unpack (expected 3, got 2)` | A row with only two values | Fix that row so it has a product, a price and a quantity |
| `ValueError: too many values to unpack (expected 3)` | The file has a fourth column | Unpack four names, or use `DictReader`, which doesn't care how many columns there are |
| `ValueError: I/O operation on closed file.` | The `for` loop is indented less than the `with` line, so it runs after the file is closed | Indent the loop inside the `with` block |
| `KeyError: 'Price'` with `DictReader` | The key has to match the header exactly, capitals included | `row["price"]`, as spelled in the file's first line |
| `KeyError: 'Widget A'` in Exercise 7 | `summary[product] += total` adds to a key that isn't there yet | `summary[product] = summary.get(product, 0) + total` |
| A second loop over the same reader prints nothing | A reader hands out each row once, and the first loop used them all | Open the file again, as each exercise here does |
| The log always has 1 line | It was opened with `"w"`, which empties it every run | `open(LOG_FILE, "a")` |
| Blank rows between the rows in Excel | `cleaned.csv` was opened without `newline=""` on Windows | `open(CLEANED_FILE, "w", newline="")` |
| `Command 'python' not found` | Ubuntu and macOS call it `python3` | `python3 csv_practice.py` |
| `git push` is rejected | You edited something on github.com | `git pull`, then `git push` |

> **The worst bug here destroys data.** Type `"w"` where you meant `"r"` on `SALES_FILE`, and the file is already empty by the time Python stops with `io.UnsupportedOperation: not readable`. Before you open a file with `"w"`, check the file name, and keep a copy of `sales.csv` somewhere safe.

### Lecture discussion questions to try

*From the lecture.* If you finish early, try these with your new script:

- **Columns that move.** The accounting team adds a `region` column between `price` and `quantity`. Which exercises break, and which keep working? Try it on a copy of `sales.csv`.
- **`"w"` and lost data.** Describe a way Exercise 5's `"w"` could wipe out something you needed, and two ways to protect against it.
- **`csv.reader` or `DictReader`?** When is the list version the better choice?
- **Absolute paths.** A teammate's script opens `/srv/data/sales.csv` because "the server never moves". What could go wrong, and how would you argue for a relative path?
