# ISM2411 Lab W14: Clean a Messy Sales CSV

## YouTube Metadata

**Title:** Clean a Messy Sales CSV — Lab Walkthrough | ISM2411 Lab 14
**Description:**
Walkthrough of ISM2411 Module 14 Lab. We apply the full pandas cleaning workflow to a deliberately messy dataset: find and handle nulls, fix data types, remove duplicates, flag outliers, and document every decision.

**Chapters:**
0:00 — What we're cleaning
0:45 — Inspecting the mess: isnull, dtypes, describe
3:00 — Handling nulls: drop, fill, or flag
5:30 — Fixing data types and removing duplicates
7:00 — Flagging outliers and documenting decisions
8:30 — Submission checklist

**Applies to:** ISM2411 Module 14

**Tags:** pandas data cleaning, python handle missing values, pandas dropna fillna, python data cleaning tutorial, ISM2411, USF, pandas duplicates outliers

---

## Script

### INTRO (0:00–0:45)

Lab 14 — Clean a Messy Sales CSV. Real data is never clean. This lab gives you a deliberately messy dataset and asks you to make deliberate decisions about every problem you find — not just fix it, but document *why* you fixed it that way.

---

### INSPECT FIRST (0:45–3:00)

```python
# clean_sales.py
import pandas as pd

df = pd.read_csv("messy_sales.csv")

print("Shape:", df.shape)
print("\nNull counts:")
print(df.isnull().sum())
print("\nDtypes:")
print(df.dtypes)
print("\nDescribe:")
print(df.describe())
```

Read the output before touching anything. Document what you find in comments:
```python
# Found: 'price' column has 3 nulls — likely data entry gaps
# Found: 'quantity' loaded as object (str) — contains "TBD" entries
# Found: 12 duplicate rows — same order_id appears twice
# Found: revenue has values > $50,000 — potential outliers
```

Exercise 3 asks what surprised you in `describe()`. Write a genuine answer — not the first obvious thing, something you actually didn't expect.

---

### HANDLING NULLS (3:00–5:30)

Three options. Pick the right one for each column:

```python
# Drop rows where price is null (can't compute revenue without it)
df = df.dropna(subset=["price"])
# Document why: price is required for all calculations

# Fill nulls in 'region' with 'Unknown'
df["region"] = df["region"].fillna("Unknown")
# Document why: region is informational, not required for math

# Flag nulls in 'customer_id' rather than dropping
df["has_customer_id"] = df["customer_id"].notnull()
# Document why: missing customer_id may indicate walk-in sales — legitimate data
```

The choice between drop/fill/flag depends on your business context. There's no universal right answer — document your reasoning.

---

### DATA TYPES AND DUPLICATES (5:30–7:00)

```python
# Fix 'quantity' column — remove non-numeric values first
df = df[pd.to_numeric(df["quantity"], errors="coerce").notnull()]
df["quantity"] = df["quantity"].astype(int)

# Fix date column
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# Remove duplicates
print(f"Before dedup: {len(df)}")
df = df.drop_duplicates(subset=["order_id"])
print(f"After dedup: {len(df)}")
```

---

### FLAGGING OUTLIERS (7:00–8:30)

```python
# Flag high-value orders rather than removing them
Q3 = df["revenue"].quantile(0.75)
IQR = df["revenue"].quantile(0.75) - df["revenue"].quantile(0.25)
upper_bound = Q3 + 1.5 * IQR

df["is_outlier"] = df["revenue"] > upper_bound
print(f"Outliers flagged: {df['is_outlier'].sum()}")

# Save cleaned data
df.to_csv("cleaned_sales.csv", index=False)
print(f"Cleaned data saved. Shape: {df.shape}")
```

---

### SUBMISSION CHECKLIST (8:30–10:00)

- Inspection run first with null counts and dtypes printed
- At least one each: drop, fill, flag decision — all commented with reasoning
- Duplicate removal with before/after count printed
- Data types corrected
- Outliers flagged (not dropped)
- Comments explain WHY each decision was made
- `cleaned_sales.csv` saved
- GitHub commit + Canvas URL
