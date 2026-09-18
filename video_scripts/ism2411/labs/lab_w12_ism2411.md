# ISM2411 Lab W12: Read a Sales CSV, Write a Cleaned Report

## YouTube Metadata

**Title:** Read a Sales CSV, Write a Cleaned Report — Full Lab Walkthrough | ISM2411 Lab 12
**Description:**
Step-by-step, test-as-you-go walkthrough of ISM2411 Module 12 Lab — your first complete ETL pipeline. Read sales.csv with csv.reader, skip the header explicitly, compute per-row and total revenue, filter and write a cleaned CSV, re-read with DictReader, build a product-summary dictionary, and append timestamped run logs across multiple executions.

Course page: https://markumreed.github.io/ism2411/pages/week12_lab.html

**Chapters:**
0:00 — What this lab covers — your first ETL pipeline
0:45 — Exercise 1: get sales.csv in place
1:40 — Exercise 2: read raw rows with csv.reader
2:50 — Exercise 3: skip the header explicitly
3:50 — Exercise 4: compute per-row and total revenue
5:20 — Exercise 5: filter and write cleaned.csv
7:10 — Exercise 6: re-read with DictReader
8:40 — Exercise 7: sales summary by product
10:20 — Exercise 8: the append-mode run log
12:00 — Reflection questions
12:40 — Submission checklist

**Applies to:** ISM2411 Module 12

**Tags:** python csv module tutorial, python csv.reader dictreader, python file io append mode, python etl pipeline beginners, ISM2411, USF, python for business beginners

---

## How to Use This Script

**SAY** it, **DO** it, **CHECK** the exact output, **FIX** it if it doesn't match — then move to the next step. This walkthrough uses a specific 10-row sample `sales.csv` so every number is checkable — if your Canvas-provided file has different data, your totals will differ, but the *pattern* is identical.

---

## Script

### INTRO (0:00–0:45)

**SAY:** "Lab 12 — read a sales CSV, write a cleaned report. This is your first complete ETL pipeline: Extract data from a file, Transform it — filter, compute, summarize — and Load the result into a new file. This exact shape is what a huge amount of real business analytics work looks like."

---

### EXERCISE 1 — Get the File (0:45–1:40)

**SAY:** "Set up the folder structure first, before any code."

**DO:**
```bash
mkdir -p week12/data
```
Place the Canvas-provided `sales.csv` at `week12/data/sales.csv`. If you don't have it yet, create it yourself with this sample content — a header row plus 10 data rows:
```csv
product,price,quantity
Widget A,9.99,50
Gadget B,24.99,12
Widget A,9.99,30
Stapler,5.49,8
Gadget B,24.99,5
Notebook,3.99,100
Marker Pack,7.25,20
Stapler,5.49,15
Notebook,3.99,60
Gadget B,24.99,3
```

**CHECK:**
```bash
cat week12/data/sales.csv
```
Confirm the header row exactly matches `product,price,quantity`, and there are 10 data rows below it — 11 lines total.

---

### EXERCISE 2 — Read and Print Raw Rows (1:40–2:50)

**SAY:** "The most basic way to read a CSV — every row comes back as a plain list of strings, header included."

**DO:**
```python
import csv

with open("week12/data/sales.csv") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
```
```bash
python3 csv_practice.py
```

**CHECK:**
```
['product', 'price', 'quantity']
['Widget A', '9.99', '50']
['Gadget B', '24.99', '12']
['Widget A', '9.99', '30']
['Stapler', '5.49', '8']
['Gadget B', '24.99', '5']
['Notebook', '3.99', '100']
['Marker Pack', '7.25', '20']
['Stapler', '5.49', '15']
['Notebook', '3.99', '60']
['Gadget B', '24.99', '3']
```

**SAY:** "Notice every single value is a string — `'9.99'` and `'50'` both have quotes around them, even though they look like numbers. That's true for *every* CSV read this way, and it's the reason Exercise 4 needs explicit type conversion."

---

### EXERCISE 3 — Skip the Header (2:50–3:50)

**SAY:** "Now separate the header from the data explicitly, instead of printing them mixed together."

**DO:**
```python
with open("week12/data/sales.csv") as f:
    reader = csv.reader(f)
    header = next(reader)
    print(f"Header: {header}")
    for row in reader:
        print(row)
```
```bash
python3 csv_practice.py
```

**CHECK:**
```
Header: ['product', 'price', 'quantity']
['Widget A', '9.99', '50']
['Gadget B', '24.99', '12']
...
```
(Same 10 data rows as Exercise 2, but the header is now printed once, separately, and the loop starts directly at the first data row.)

**SAY:** "`next(reader)` pulls exactly one row off the reader — the very first one — and advances it, so the `for` loop that follows starts from the second row onward. This works because a `csv.reader` is an *iterator*: once you've consumed a row from it, it's gone, and the next thing to read it picks up where you left off."

---

### EXERCISE 4 — Compute Totals (3:50–5:20)

**SAY:** "Now the type conversion that Exercise 2 warned about — every `price` and `quantity` needs to become a real number before any arithmetic happens."

**DO:**
```python
total_revenue = 0
with open("week12/data/sales.csv") as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        product, price, quantity = row
        price = float(price)
        quantity = int(quantity)
        line_total = price * quantity
        total_revenue += line_total
        print(f"{product}: {quantity} units × ${price:.2f} = ${line_total:.2f}")

print(f"\nTotal revenue: ${total_revenue:,.2f}")
```
```bash
python3 csv_practice.py
```

**CHECK:**
```
Widget A: 50 units × $9.99 = $499.50
Gadget B: 12 units × $24.99 = $299.88
Widget A: 30 units × $9.99 = $299.70
Stapler: 8 units × $5.49 = $43.92
Gadget B: 5 units × $24.99 = $124.95
Notebook: 100 units × $3.99 = $399.00
Marker Pack: 20 units × $7.25 = $145.00
Stapler: 15 units × $5.49 = $82.35
Notebook: 60 units × $3.99 = $239.40
Gadget B: 3 units × $24.99 = $74.97

Total revenue: $2,208.67
```
Confirm the total by adding all ten line totals by hand, or trust the running accumulator — either way it should land on `$2,208.67`.

**FIX:** If you get a `ValueError: could not convert string to float`, check for stray whitespace or an extra blank line at the end of your CSV file.

---

### EXERCISE 5 — Filter and Write (5:20–7:10)

**SAY:** "Now the 'Load' half of ETL — write a brand-new, filtered CSV file, keeping only orders over $100."

**DO:**
```python
rows_written = 0
rows_total = 0

with open("week12/data/sales.csv") as infile, \
     open("week12/data/cleaned.csv", "w", newline="") as outfile:

    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    header = next(reader)
    writer.writerow(["Product", "Price", "Qty", "Total"])

    for row in reader:
        rows_total += 1
        product, price, quantity = row
        price = float(price)
        quantity = int(quantity)
        total = price * quantity
        if total > 100:
            writer.writerow([product, price, quantity, round(total, 2)])
            rows_written += 1

print(f"Wrote {rows_written} of {rows_total} rows to cleaned.csv")
```
```bash
python3 csv_practice.py
```

**CHECK:**
```
Wrote 7 of 10 rows to cleaned.csv
```
Confirm: the three rows that *don't* qualify are Stapler×8 ($43.92), Stapler×15 ($82.35), and Gadget B×3 ($74.97) — all under $100 — leaving exactly 7 rows in `cleaned.csv`.

```bash
cat week12/data/cleaned.csv
```
```
Product,Price,Qty,Total
Widget A,9.99,50,499.5
Gadget B,24.99,12,299.88
Widget A,9.99,30,299.7
Gadget B,24.99,5,124.95
Notebook,3.99,100,399.0
Marker Pack,7.25,20,145.0
Notebook,3.99,60,239.4
```

**SAY:** "`newline=\"\"` in the `open()` call is required on every CSV file you *write* in Python — without it, Windows systems can end up with an extra blank line after every row, since the `csv` module handles line endings itself."

---

### EXERCISE 6 — csv.DictReader (7:10–8:40)

**SAY:** "Same file, same totals, but accessed by column name instead of position — much more readable once a CSV has more than three or four columns."

**DO:**
```python
total_revenue_dict = 0
with open("week12/data/sales.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        price = float(row["price"])
        quantity = int(row["quantity"])
        total_revenue_dict += price * quantity

print(f"Total revenue (DictReader): ${total_revenue_dict:,.2f}")

# csv.reader gives each row as a plain list — access by position (row[1]).
# csv.DictReader gives each row as a dict using the header — access by name (row["price"]),
# which is more readable but very slightly slower for huge files.
```
```bash
python3 csv_practice.py
```

**CHECK:**
```
Total revenue (DictReader): $2,208.67
```
Identical to Exercise 4's total — proof both approaches read the exact same underlying data, just packaged differently.

**SAY:** "Notice there's no `next(reader)` needed here at all — `DictReader` automatically treats the first row as the header and uses it to build each row's dict keys, so the loop only ever sees data rows."

---

### EXERCISE 7 — Sales Summary by Product (8:40–10:20)

**SAY:** "Now Module 11's accumulator-in-a-dict pattern, applied directly to data coming out of a CSV instead of a hardcoded list."

**DO:**
```python
product_totals = {}
with open("week12/data/sales.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        product = row["product"]
        line_total = float(row["price"]) * int(row["quantity"])
        product_totals[product] = product_totals.get(product, 0) + line_total

for product in sorted(product_totals):
    print(f"{product}: ${product_totals[product]:,.2f}")
```
```bash
python3 csv_practice.py
```

**CHECK:**
```
Gadget B: $499.80
Marker Pack: $145.00
Notebook: $638.40
Stapler: $126.27
Widget A: $799.20
```
Confirm `Gadget B` — it appears in three separate rows (`12`, `5`, and `3` units) — accumulates to `299.88 + 124.95 + 74.97 = 499.80`, exactly matching this summary.

---

### EXERCISE 8 — Append Mode Log (10:20–12:00)

**SAY:** "One more file-writing mode — `'a'` for append — used here to build a log that grows every time the script runs, rather than getting overwritten each time."

**DO:**
```python
from datetime import datetime

with open("week12/data/run_log.txt", "a") as log:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log.write(f"{timestamp} — total revenue: ${total_revenue:,.2f}\n")
```
Run the full script three separate times:
```bash
python3 csv_practice.py
python3 csv_practice.py
python3 csv_practice.py
cat week12/data/run_log.txt
```

**CHECK:**
```
2026-08-25 10:14:02 — total revenue: $2,208.67
2026-08-25 10:14:05 — total revenue: $2,208.67
2026-08-25 10:14:08 — total revenue: $2,208.67
```
Three lines, three different timestamps, same total revenue each time (since the source data didn't change between runs).

**FIX:** If the file only ever shows one line, confirm you opened it with `"a"` (append), not `"w"` (write) — `"w"` truncates the file back to empty every single time it's opened.

---

### REFLECTION QUESTIONS (12:00–12:40)

**SAY:** "Add these as a comment block at the very top of the file."

**DO:** Answer, 2–3 sentences each:
1. You've now completed a full ETL pipeline: read a CSV, transform the data, write a new CSV. How does this compare to doing the same task in Excel? What can Python do that Excel can't do easily, and vice versa?
2. Exercise 8 showed you append mode. Think of a real business process that would benefit from an append-mode log file — describe it and explain why append mode is the right tool.

**CHECK:** Question 2's honest answer should specifically name why append (not write) matters — a log that's supposed to accumulate history (audit trails, error logs, transaction records) breaks entirely if each run silently erases everything before it.

---

### SUBMISSION CHECKLIST (12:40–end)

- [ ] `csv_practice.py` — filename matches exactly, lowercase
- [ ] `week12/data/sales.csv` present with header + 10 data rows
- [ ] Exercise 2–3: raw rows read, header separated correctly
- [ ] Exercise 4: per-row totals and overall total revenue correct
- [ ] Exercise 5: `cleaned.csv` written with only orders over $100, plus a printed count
- [ ] Exercise 6: `DictReader` version producing the identical total, with a comparison comment
- [ ] Exercise 7: product summary dict, sorted by product name
- [ ] Exercise 8: `run_log.txt` with three accumulated entries from three separate runs
- [ ] Reflection comment block at the top of the file, both questions answered
- [ ] All output files (`cleaned.csv`, `run_log.txt`, etc.) pushed to GitHub in `week12/`
- [ ] Repo URL submitted to Canvas
