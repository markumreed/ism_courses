# ISM2411 Lab W13: First DataFrame — Retail Sales Explorer

## YouTube Metadata

**Title:** First DataFrame: Retail Sales Explorer — Lab Walkthrough | ISM2411 Lab 13
**Description:**
Walkthrough of ISM2411 Module 13 Lab. We load the retail sales CSV into a pandas DataFrame, explore its shape and columns, run boolean filters, and select subsets — the foundation for every subsequent data lab.

Course page: https://markumreed.github.io/ism2411/pages/week13_lab.html

**Chapters:**
0:00 — What we're building
0:45 — Loading the CSV and first inspection
2:30 — Boolean filters: single and combined conditions
5:00 — Selecting columns and computing a new column
7:00 — Sorting and saving results
8:30 — Submission checklist

**Applies to:** ISM2411 Module 13

**Tags:** pandas dataframe tutorial, python pandas filter, pandas read csv, python pandas for beginners, ISM2411, USF, pandas boolean indexing

---

## Script

### INTRO (0:00–0:45)

Lab 13 — First DataFrame, Retail Sales Explorer. This is your introduction to pandas. Everything from here — cleaning, analysis, the capstone — runs in pandas. The goal today is loading, inspecting, and filtering. Let's get into VS Code.

---

### LOADING AND INSPECTING (0:45–2:30)

```python
# retail_explorer.py
import pandas as pd

df = pd.read_csv("retail_sales.csv")

print(df.shape)          # (rows, columns)
print(df.dtypes)         # column types
print(df.head())         # first 5 rows
print(df.describe())     # summary statistics
print(df.columns.tolist())
```

`shape` gives you dimensions immediately. `dtypes` tells you what pandas inferred for each column — important for spotting columns that should be numeric but loaded as strings. `describe()` gives count, mean, min, max, quartiles for all numeric columns.

---

### BOOLEAN FILTERS (2:30–5:00)

```python
# Single condition
high_revenue = df[df["revenue"] > 500]
print(f"High-revenue rows: {len(high_revenue)}")

# Combined conditions — use & not 'and', wrap each in parens
east_high = df[(df["region"] == "East") & (df["revenue"] > 500)]
print(east_high[["product", "region", "revenue"]].head())

# OR condition
east_or_west = df[(df["region"] == "East") | (df["region"] == "West")]

# Negation
not_east = df[df["region"] != "East"]
```

The two rules that trip everyone up:
1. Use `&` and `|` not `and` and `or`
2. Wrap each condition in parentheses

---

### SELECTING COLUMNS AND ADDING A NEW ONE (5:00–7:00)

```python
# Single column — returns a Series
print(df["revenue"].mean())
print(df["revenue"].sum())
print(df["revenue"].max())

# Multiple columns — returns a DataFrame (double brackets)
subset = df[["product", "region", "revenue"]]

# Adding a computed column
df["revenue_per_unit"] = df["revenue"] / df["quantity"]
print(df[["product", "revenue", "quantity", "revenue_per_unit"]].head())
```

`df["col"]` (single brackets) → Series. `df[["col1", "col2"]]` (double brackets) → DataFrame. The distinction matters when you pass the result to another function.

---

### SORTING AND SAVING (7:00–8:30)

```python
# Sort by revenue descending
top_products = df.sort_values("revenue", ascending=False).head(10)
print(top_products[["product", "revenue"]])

# Save filtered result
east_high.to_csv("east_high_revenue.csv", index=False)
print("Saved to east_high_revenue.csv")
```

`index=False` prevents pandas from writing the row numbers as a column in the output.

---

### SUBMISSION CHECKLIST (8:30–10:00)

- `retail_explorer.py` with load, inspect, filter, select, compute, sort, save
- At least two combined conditions using `&` or `|`
- New column computed from existing columns
- Output CSV saved with `index=False`
- Exercise responses written
- GitHub commit + Canvas URL
