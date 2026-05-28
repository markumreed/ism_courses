# Video 17: Introduction to pandas

## YouTube Metadata

**Title:** pandas for Business — Load, Inspect & Filter DataFrames | ISM2411
**Description:**
pandas is the Python library for working with tabular data at scale. In this video you'll load a business CSV into a DataFrame, inspect it with head(), info(), and describe(), select columns, filter rows, and answer real business questions — all without writing a single for loop.

**Chapters:**
0:00 — What pandas is and why it replaces manual CSV processing
1:30 — Installing and importing pandas
3:00 — Loading a CSV — pd.read_csv()
5:00 — Inspecting: head(), tail(), info(), describe()
8:30 — Selecting columns
10:30 — Filtering rows
13:30 — Sorting
15:00 — Saving results
17:00 — Recap

**Applies to:** ISM2411 Module 13

**Tags:** pandas tutorial, pandas DataFrame, python pandas, read csv pandas, pandas filter, pandas head info describe, ISM2411, python data analysis, python business analytics, pandas beginner

---

## Script

### INTRO (0:00–1:30)

In the last module, we read a CSV with Python's `csv` module. We wrote loops, converted types manually, built dictionaries to aggregate by region. It worked. But now imagine your CSV has 500,000 rows and 30 columns. The manual approach gets painful fast.

pandas is the solution. It's the most widely used Python library for data work in business and data science. It loads your CSV into a DataFrame — essentially a programmable spreadsheet — and gives you high-level tools to select, filter, sort, aggregate, and visualize data without writing loops. Let's use it.

---

### INSTALLING AND IMPORTING (1:30–3:00)

Install pandas in your virtual environment:

```bash
pip install pandas
```

Import it (the `pd` alias is universal convention — always use `pd`):

```python
import pandas as pd
print(pd.__version__)
```

For this video we'll use a sales dataset. Let's create it:

```python
import pandas as pd

data = {
    "date":        ["2024-05-20","2024-05-20","2024-05-21","2024-05-21","2024-05-22","2024-05-22","2024-05-23"],
    "region":      ["Southeast","Southeast","Northeast","Southeast","Northeast","Southwest","Southeast"],
    "product":     ["Laptop Bag","USB-C Hub","Laptop Bag","Monitor Stand","USB-C Hub","Laptop Bag","Wireless Mouse"],
    "quantity":    [3, 5, 2, 4, 8, 1, 6],
    "unit_price":  [49.99, 24.99, 49.99, 35.99, 24.99, 49.99, 39.99],
    "rep":         ["Kim","Kim","Patel","Kim","Patel","Johnson","Kim"],
}

df = pd.DataFrame(data)
df.to_csv("campus_sales.csv", index=False)
```

---

### LOADING A CSV (3:00–5:00)

```python
df = pd.read_csv("campus_sales.csv")
```

That one line loads the entire CSV into a DataFrame. pandas automatically:
- Detects the header row
- Infers column types (strings, numbers, dates)
- Stores everything in a tabular structure

Common options:
```python
df = pd.read_csv("campus_sales.csv", parse_dates=["date"])   # parse date column properly
df = pd.read_csv("sales.csv", encoding="utf-8")               # specify encoding if needed
```

---

### INSPECTING (5:00–8:30)

**head() and tail()** — show the first/last N rows:
```python
df.head()     # first 5 rows (default)
df.head(3)    # first 3 rows
df.tail(2)    # last 2 rows
```

**shape** — rows and columns:
```python
print(df.shape)   # (7, 6) — 7 rows, 6 columns
```

**info()** — column names, types, non-null counts:
```python
df.info()
```

Output:
```
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 7 entries, 0 to 6
Data columns (total 6 columns):
 #   Column      Non-Null Count  Dtype
---  ------      --------------  -----
 0   date        7 non-null      object
 1   region      7 non-null      object
 2   product     7 non-null      object
 3   quantity    7 non-null      int64
 4   unit_price  7 non-null      float64
 5   rep         7 non-null      object
```

Use `info()` first on any new dataset — spot missing values and wrong types immediately.

**describe()** — statistics for numeric columns:
```python
df.describe()
```

Shows count, mean, std, min, quartiles, max for every numeric column. Instant snapshot of your data's shape.

**columns** — list of column names:
```python
print(df.columns.tolist())
# ['date', 'region', 'product', 'quantity', 'unit_price', 'rep']
```

---

### SELECTING COLUMNS (8:30–10:30)

Select a single column — returns a Series:
```python
prices = df["unit_price"]
print(prices)
print(type(prices))   # <class 'pandas.core.series.Series'>
```

Select multiple columns — returns a DataFrame:
```python
subset = df[["product", "quantity", "unit_price"]]
print(subset)
```

Add a computed column:
```python
df["revenue"] = df["quantity"] * df["unit_price"]
print(df[["product", "quantity", "unit_price", "revenue"]])
```

---

### FILTERING ROWS (10:30–13:30)

Filter with a boolean condition:

```python
# Orders over $100:
high_value = df[df["revenue"] > 100]
print(high_value)

# Southeast region only:
southeast = df[df["region"] == "Southeast"]
print(southeast)

# Multiple conditions — use & (and) | (or), with parentheses:
se_high = df[(df["region"] == "Southeast") & (df["revenue"] > 100)]
print(se_high)

# Laptop Bag or Monitor Stand:
bags_monitors = df[df["product"].isin(["Laptop Bag", "Monitor Stand"])]
print(bags_monitors)
```

**How filtering works:** `df["revenue"] > 100` creates a boolean Series (True/False for each row). Passing that Series inside `df[...]` returns only the rows where the value is True.

---

### SORTING (13:30–15:00)

```python
# Sort by revenue descending:
df_sorted = df.sort_values("revenue", ascending=False)
print(df_sorted[["date", "product", "revenue"]])

# Sort by multiple columns:
df_sorted2 = df.sort_values(["region", "revenue"], ascending=[True, False])
print(df_sorted2)
```

`sort_values()` returns a new DataFrame — the original is unchanged.

---

### SAVING RESULTS (15:00–17:00)

Write the processed DataFrame back to CSV:

```python
df[["date", "product", "region", "revenue"]].to_csv(
    "sales_with_revenue.csv",
    index=False    # don't write the row numbers as a column
)
print("Saved.")
```

Save a filtered subset:
```python
df[df["revenue"] > 100].to_csv("high_value_orders.csv", index=False)
```

---

### RECAP (17:00–20:00)

- `pd.read_csv("file.csv")` — load a CSV into a DataFrame
- `df.head()`, `df.tail()` — preview rows
- `df.info()` — column types and null counts
- `df.describe()` — statistics for numeric columns
- `df["column"]` — select a Series; `df[["a","b"]]` — select multiple columns
- `df["revenue"] = df["qty"] * df["price"]` — add a computed column
- `df[df["col"] > value]` — filter rows
- `df.sort_values("col", ascending=False)` — sort
- `df.to_csv("output.csv", index=False)` — save results

Next module: data cleaning and descriptive statistics — handling missing values, fixing types, and summarizing business datasets.
