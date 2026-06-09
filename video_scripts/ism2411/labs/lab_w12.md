# ISM2411 Lab W12: Read a Sales CSV, Write a Cleaned Report

## YouTube Metadata

**Title:** Read a Sales CSV, Write a Cleaned Report — Lab Walkthrough | ISM2411 Lab 12
**Description:**
Walkthrough of ISM2411 Module 12 Lab. We build a complete ETL pipeline: read a sales CSV with Python's csv module, filter for high-value orders, compute totals, and write a cleaned summary back to disk.

Course page: https://markumreed.github.io/ism2411/pages/week12_lab.html

**Chapters:**
0:00 — What we're building
0:45 — Reading a CSV with csv.reader
2:30 — Reading with csv.DictReader (column names)
4:30 — Filtering and accumulating totals
6:00 — Writing a cleaned output CSV
8:00 — Append mode for a log file
9:00 — Submission checklist

**Applies to:** ISM2411 Module 12

**Tags:** python csv reader, python file io, python ETL pipeline, python write csv, ISM2411, USF, python csv tutorial, python read write file

---

## Script

### INTRO (0:00–0:45)

Lab 12 — Read a Sales CSV, Write a Cleaned Report. This is your first complete ETL pipeline: extract data from a CSV, transform it (filter, compute), load the results to a new file. The same pattern runs in every data engineering job.

---

### THE DATA FILE

First, create `module12/sales.csv`:
```
product,price,quantity,region
Laptop Bag,49.99,12,East
Wireless Mouse,29.99,3,West
USB Hub,19.99,45,East
Monitor Stand,34.99,8,West
Keyboard,79.99,2,North
```

---

### CSV.READER (0:45–2:30)

```python
# file_io.py
import csv

with open("sales.csv", "r") as f:
    reader = csv.reader(f)
    header = next(reader)   # skip header row
    print(f"Columns: {header}")

    for row in reader:
        product  = row[0]
        price    = float(row[1])
        quantity = int(row[2])
        revenue  = price * quantity
        print(f"{product:<20} ${revenue:>8,.2f}")
```

`csv.reader` gives you rows as lists — access by index. `next()` skips the header.

---

### CSV.DICTREADER (2:30–4:30)

```python
# Exercise 5: DictReader — access by column name
with open("sales.csv", "r") as f:
    reader = csv.DictReader(f)    # header row becomes keys automatically

    for row in reader:
        revenue = float(row["price"]) * int(row["quantity"])
        print(f"{row['product']:<20} ${revenue:>8,.2f}")
```

Same result, more readable code. Use `DictReader` whenever you have headers — column names are self-documenting.

---

### FILTERING AND ACCUMULATING (4:30–6:00)

```python
# Filter for high-value orders and compute total
THRESHOLD = 200.00
total_revenue = 0
high_value_rows = []

with open("sales.csv", "r") as f:
    reader = csv.DictReader(f)

    for row in reader:
        revenue = float(row["price"]) * int(row["quantity"])
        if revenue >= THRESHOLD:
            high_value_rows.append({**row, "revenue": revenue})
            total_revenue += revenue

print(f"High-value orders: {len(high_value_rows)}")
print(f"Total revenue:     ${total_revenue:,.2f}")
```

---

### WRITING THE OUTPUT CSV (6:00–8:00)

```python
# Write filtered results to cleaned_sales.csv
with open("cleaned_sales.csv", "w", newline="") as f:
    fieldnames = ["product", "price", "quantity", "region", "revenue"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)

    writer.writeheader()
    for row in high_value_rows:
        writer.writerow(row)

print("Written to cleaned_sales.csv")
```

Open the output in Excel or a text editor to verify. This is the standard verification step for any ETL output.

---

### APPEND MODE (8:00–9:00)

```python
# Append-mode log file — records each run
import datetime

with open("run_log.txt", "a") as log:
    log.write(f"{datetime.datetime.now()} — processed {len(high_value_rows)} records\n")
```

`"w"` overwrites; `"a"` appends. Use append for logs where you want to keep all history.

---

### SUBMISSION CHECKLIST (9:00–10:00)

- `file_io.py` using both `csv.reader` and `csv.DictReader`
- High-value filter applied with threshold constant
- `cleaned_sales.csv` written with `DictWriter`
- Append-mode log file demonstrated
- `summary.csv` written sorted by revenue descending
- Exercise responses written
- GitHub commit + Canvas URL
