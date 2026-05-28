# Video 16: Working with Files & CSVs

## YouTube Metadata

**Title:** Python File I/O & CSV Reading for Business Data | ISM2411
**Description:**
Real business data lives in files — CSVs exported from Excel, ERPs, and databases. In this video you'll learn to read and write text files, then work with CSVs using Python's built-in csv module. We'll load a sales dataset, calculate totals by region, filter records, and write results to a new file.

**Chapters:**
0:00 — Why file I/O matters
1:30 — Reading a text file with open()
4:00 — The with statement
5:30 — Writing to a file
7:00 — CSV files — structure and the csv module
9:00 — csv.reader — reading rows
11:30 — csv.DictReader — rows as dictionaries
14:00 — Writing CSV output
16:00 — Recap

**Applies to:** ISM2411 Module 12

**Tags:** python file io, python csv, python open file, python csv reader, python DictReader, python read csv, python write csv, ISM2411, python business data, python tutorial

---

## Script

### INTRO (0:00–1:30)

Everything we've done so far works on data you type directly into your script. But real business data doesn't live in your code — it lives in files. CSVs from your ERP, exports from your POS system, reports from your CRM. In this module, we learn to read those files, process them, and write results back to disk. This is the foundation of every data pipeline.

---

### READING A TEXT FILE (1:30–4:00)

The built-in `open()` function opens any file. It takes a filename (path) and a mode.

```python
f = open("notes.txt", "r")    # "r" = read mode
content = f.read()             # reads entire file as a string
print(content)
f.close()                      # always close when done
```

Modes:
- `"r"` — read (default)
- `"w"` — write (creates new file, overwrites if exists)
- `"a"` — append (adds to end of existing file)

Reading line by line:

```python
f = open("notes.txt", "r")
for line in f:
    print(line.strip())   # .strip() removes the newline character at the end
f.close()
```

---

### THE with STATEMENT (4:00–5:30)

The problem with `open()` + `close()`: if your code crashes between them, the file stays open. Python's `with` statement handles this automatically — it closes the file even if an exception occurs.

```python
with open("notes.txt", "r") as f:
    content = f.read()
    print(content)
# file is automatically closed here, even if an error occurred inside
```

Always use `with open(...)`. It's cleaner, safer, and is the standard in all professional Python code.

---

### WRITING TO A FILE (5:30–7:00)

```python
report_lines = [
    "Sales Report — Week of 2024-05-28",
    "=" * 40,
    "Monday:    $142.50",
    "Tuesday:    $89.99",
    "Wednesday: $312.00",
    "Total:     $544.49",
]

with open("weekly_report.txt", "w") as f:
    for line in report_lines:
        f.write(line + "\n")   # write() doesn't add newlines automatically

print("Report written.")
```

To verify, open the file:
```python
with open("weekly_report.txt", "r") as f:
    print(f.read())
```

**Append mode** — add to an existing file without overwriting:
```python
with open("weekly_report.txt", "a") as f:
    f.write("End of report.\n")
```

---

### CSV FILES (7:00–9:00)

CSV stands for **Comma-Separated Values**. It's the universal format for tabular data — every spreadsheet application can read and write it.

Example CSV file (`sales_data.csv`):
```
date,region,product,quantity,unit_price
2024-05-20,Southeast,Laptop Bag,3,49.99
2024-05-20,Southeast,USB-C Hub,5,24.99
2024-05-21,Northeast,Laptop Bag,2,49.99
2024-05-21,Southeast,Monitor Stand,4,35.99
2024-05-22,Northeast,USB-C Hub,8,24.99
2024-05-22,Southwest,Laptop Bag,1,49.99
```

The first row is headers. Each subsequent row is one transaction. Commas separate fields. Python's `csv` module parses this correctly — including handling commas inside quoted fields.

Let's create this file for our examples:

```python
sample_data = """date,region,product,quantity,unit_price
2024-05-20,Southeast,Laptop Bag,3,49.99
2024-05-20,Southeast,USB-C Hub,5,24.99
2024-05-21,Northeast,Laptop Bag,2,49.99
2024-05-21,Southeast,Monitor Stand,4,35.99
2024-05-22,Northeast,USB-C Hub,8,24.99
2024-05-22,Southwest,Laptop Bag,1,49.99"""

with open("sales_data.csv", "w") as f:
    f.write(sample_data)
```

---

### csv.reader (9:00–11:30)

`csv.reader` reads each row as a list of strings.

```python
import csv

with open("sales_data.csv", "r") as f:
    reader = csv.reader(f)
    headers = next(reader)   # first row = headers
    print("Headers:", headers)

    total_revenue = 0
    row_count     = 0

    for row in reader:
        date, region, product, quantity, unit_price = row
        revenue = int(quantity) * float(unit_price)
        total_revenue += revenue
        row_count += 1
        print(f"{date} | {region:<12} | {product:<15} | ${revenue:>7.2f}")

print(f"\nTotal rows: {row_count}")
print(f"Total revenue: ${total_revenue:,.2f}")
```

Note: every value from `csv.reader` is a **string** — even numbers. You must convert with `int()` or `float()` before doing math.

---

### csv.DictReader (11:30–14:00)

`csv.DictReader` reads each row as a dictionary, using the header row as keys. This is cleaner — no positional unpacking, and adding or reordering columns doesn't break your code.

```python
import csv

regional_revenue = {}

with open("sales_data.csv", "r") as f:
    reader = csv.DictReader(f)   # no need to call next() — headers handled automatically

    for row in reader:
        region   = row["region"]
        quantity = int(row["quantity"])
        price    = float(row["unit_price"])
        revenue  = quantity * price

        if region not in regional_revenue:
            regional_revenue[region] = 0
        regional_revenue[region] += revenue

print("\nRevenue by Region:")
for region, total in sorted(regional_revenue.items(), key=lambda x: x[1], reverse=True):
    print(f"  {region:<12}: ${total:,.2f}")
```

Output:
```
Revenue by Region:
  Southeast   : $394.87
  Northeast   : $299.90
  Southwest   :  $49.99
```

Access fields by name — readable and robust.

---

### WRITING CSV OUTPUT (14:00–16:00)

Write results back to a CSV using `csv.writer` or `csv.DictWriter`.

```python
import csv

summary = [
    {"region": region, "total_revenue": total}
    for region, total in regional_revenue.items()
]

with open("regional_summary.csv", "w", newline="") as f:
    fieldnames = ["region", "total_revenue"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(summary)

print("Summary written to regional_summary.csv")
```

The `newline=""` argument prevents `csv.writer` from adding extra blank lines on Windows.

---

### RECAP (16:00–17:00)

- `with open(filename, mode) as f:` — always use `with`
- Modes: `"r"` read, `"w"` write, `"a"` append
- `f.read()` — full file as string; iterate `for line in f` for line-by-line
- `csv.reader` — each row as a list of strings; remember to convert types
- `csv.DictReader` — each row as a dict; access fields by column name
- `csv.DictWriter` — write dicts to CSV with headers
- Prefer `DictReader`/`DictWriter` over plain reader/writer for column-name clarity

Next module: introduction to pandas — loading, inspecting, and filtering DataFrames.
