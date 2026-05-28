# Video 18: Data Cleaning & Descriptive Statistics

## YouTube Metadata

**Title:** Data Cleaning & Descriptive Stats in Python pandas | ISM2411
**Description:**
Real business data is messy — missing values, wrong types, inconsistent formatting. In this video you'll learn to detect and handle nulls, fix data types, standardize text fields, and compute descriptive statistics (mean, median, std, percentiles) on a realistic customer dataset.

**Chapters:**
0:00 — Why data is always messy
1:30 — Detecting missing values: isnull(), info()
4:00 — Handling nulls: dropna(), fillna()
7:00 — Fixing data types: astype(), to_numeric()
9:30 — Standardizing text: str.strip(), str.lower()
11:30 — Descriptive statistics: mean, median, std, percentile
14:30 — Recap

**Applies to:** ISM2411 Module 14

**Tags:** pandas data cleaning, python missing values, pandas fillna dropna, pandas astype, descriptive statistics python, pandas mean median, ISM2411, python data science, data wrangling python

---

## Script

### INTRO (0:00–1:30)

Every data analyst has a saying: 80% of the work is cleaning the data, 20% is the actual analysis. Real datasets have nulls, inconsistent casing, numbers stored as strings, and outliers that make your averages meaningless. In this module we tackle all of it systematically using pandas tools. By the end you'll have a clean DataFrame ready for aggregation and visualization.

---

### OUR MESSY DATASET (1:30 as setup)

```python
import pandas as pd
import numpy as np

data = {
    "customer_id":  [101, 102, 103, 104, 105, 106, 107, 108],
    "name":         ["Alice Johnson", "  bob smith  ", "Carol White", "DAVID BROWN", None, "Eve Davis", "Frank Miller", "Grace Lee"],
    "tier":         ["Gold", "silver", "Gold", "BRONZE", "Silver", "Bronze", None, "Gold"],
    "ytd_spend":    [1840.50, 620.00, None, 185.75, 4200.00, "eight hundred", 890.25, 1200.00],
    "age_months":   [24, 6, 18, None, 36, 12, 8, 30],
    "is_active":    [True, True, True, False, True, True, None, True],
}

df = pd.DataFrame(data)
df.to_csv("customers_messy.csv", index=False)
df = pd.read_csv("customers_messy.csv")
print(df)
```

Problems to fix: extra whitespace in names, inconsistent case in tier, None in name, a string in ytd_spend, missing values in age_months and is_active.

---

### DETECTING MISSING VALUES (1:30–4:00)

```python
# How many nulls per column:
print(df.isnull().sum())
```

Output:
```
customer_id    0
name           1
tier           1
ytd_spend      0   (the string "eight hundred" isn't null — just wrong type)
age_months     1
is_active      1
```

```python
# Which rows have any null:
print(df[df.isnull().any(axis=1)])

# Total null count:
print(f"Total nulls: {df.isnull().sum().sum()}")

# Percentage null per column:
print((df.isnull().sum() / len(df) * 100).round(1))
```

---

### HANDLING NULLS (4:00–7:00)

**dropna()** — remove rows with any null:

```python
df_clean = df.dropna()   # drops all rows with any null
print(f"Rows after dropna: {len(df_clean)}")   # lost 4 rows
```

Too aggressive here — we lose too many rows. Better: drop only where we truly can't impute.

**fillna()** — fill nulls with a value:

```python
# Fill missing age with median:
median_age = df["age_months"].median()
df["age_months"] = df["age_months"].fillna(median_age)

# Fill missing is_active with True (assume active if not marked):
df["is_active"] = df["is_active"].fillna(True)

# Fill missing tier with "Unknown":
df["tier"] = df["tier"].fillna("Unknown")

# Drop rows where name is null (can't identify customer):
df = df.dropna(subset=["name"])

print(df.isnull().sum())   # only ytd_spend has issues now
```

---

### FIXING DATA TYPES (7:00–9:30)

The `ytd_spend` column has "eight hundred" as a string. `pd.to_numeric()` with `errors='coerce'` converts bad values to NaN instead of crashing.

```python
df["ytd_spend"] = pd.to_numeric(df["ytd_spend"], errors="coerce")
print(df["ytd_spend"].isnull().sum())   # 1 null (the "eight hundred" row)

# Fill the coerced null with the median:
df["ytd_spend"] = df["ytd_spend"].fillna(df["ytd_spend"].median())
```

Convert types explicitly when needed:
```python
df["customer_id"] = df["customer_id"].astype(int)
df["age_months"]  = df["age_months"].astype(int)
```

---

### STANDARDIZING TEXT (9:30–11:30)

String columns often have inconsistent spacing and case. The pandas `.str` accessor applies string methods to the whole column.

```python
# Strip whitespace:
df["name"] = df["name"].str.strip()

# Title case (first letter of each word capitalized):
df["name"] = df["name"].str.title()

# Standardize tier to Title Case:
df["tier"] = df["tier"].str.strip().str.title()

print(df[["name", "tier"]].head(8))
```

Output:
```
            name     tier
0   Alice Johnson     Gold
1      Bob Smith   Silver
2    Carol White     Gold
3   David Brown   Bronze
4      Eve Davis   Silver
5  Frank Miller   Bronze
6     Grace Lee     Gold
```

All names and tiers are now consistently formatted.

---

### DESCRIPTIVE STATISTICS (11:30–14:30)

With clean data, compute meaningful statistics:

```python
print(df["ytd_spend"].describe())
```

Output:
```
count       7.000000
mean     1248.107143
std      1265.748305
min       185.750000
25%       620.000000
50%       890.250000
75%      1840.500000
max      4200.000000
```

Individual statistics:
```python
print(f"Mean spend:   ${df['ytd_spend'].mean():,.2f}")
print(f"Median spend: ${df['ytd_spend'].median():,.2f}")
print(f"Std dev:      ${df['ytd_spend'].std():,.2f}")
print(f"Min spend:    ${df['ytd_spend'].min():,.2f}")
print(f"Max spend:    ${df['ytd_spend'].max():,.2f}")
```

The median is more meaningful than mean when there's an outlier (4200 skews the mean).

Statistics by tier:
```python
print(df.groupby("tier")["ytd_spend"].agg(["count", "mean", "median"]).round(2))
```

Output:
```
                count      mean    median
tier
Bronze              2    538.00    538.00
Gold                3   1413.50   1200.00
Silver              2   2410.00   2410.00
```

Save the clean DataFrame:
```python
df.to_csv("customers_clean.csv", index=False)
print("Cleaned data saved.")
```

---

### RECAP (14:30–15:00)

- `df.isnull().sum()` — count nulls per column
- `df.dropna()` — drop rows with nulls; use `subset=["col"]` to target columns
- `df["col"].fillna(value)` — fill nulls with a value (median, mode, or constant)
- `pd.to_numeric(col, errors="coerce")` — fix bad numeric values, turn invalid to NaN
- `df["col"].str.strip().str.title()` — standardize text
- `df["col"].astype(type)` — convert column type
- `describe()` — count, mean, std, quartiles in one call
- Median is more robust than mean when outliers are present

Next module: aggregation, groupby, and business charts — turning clean data into insights.
