# ISM2411 Lab W14: Clean a Messy Sales CSV

## YouTube Metadata

**Title:** Clean a Messy Sales CSV — Full Lab Walkthrough | ISM2411 Lab 14
**Description:**
Step-by-step, test-as-you-go walkthrough of ISM2411 Module 14 Lab. Inspect a deliberately messy dataset with .info() and .isnull().sum(), standardize column names, choose between filling and dropping missing values with documented reasoning, fix dtypes including dates and currency strings, remove duplicates, spot suspicious statistics with .describe(), and save the cleaned result.

Course page: https://markumreed.github.io/ism2411/pages/week14_lab.html

**Chapters:**
0:00 — What this lab covers — cleaning feeds every downstream analysis
0:45 — Exercise 1: inspect with .info() and .isnull().sum()
2:30 — Exercise 2: standardize column names
3:40 — Exercise 3: fill vs. drop — handling missing values
5:40 — Exercise 4: fixing dtypes — dates, currency, integers
7:40 — Exercise 5: checking for duplicates
8:50 — Exercise 6: .describe() and suspicious statistics
10:30 — Exercise 7: save and reload to verify
11:50 — Reflection questions
12:30 — Submission checklist

**Applies to:** ISM2411 Module 14

**Tags:** pandas data cleaning tutorial, pandas fillna dropna, pandas dtype conversion, pandas iqr outliers, ISM2411, USF, pandas for business beginners

---

## How to Use This Script

**SAY** it, **DO** it, **CHECK** the exact output, **FIX** it if it doesn't match — then move to the next step. This lab uses the real `messy_sales.csv` provided on Canvas — the exact counts and values below are illustrative of the *pattern* you should see; your real numbers will differ.

---

## Script

### INTRO (0:00–0:45)

**SAY:** "Lab 14 — clean a messy sales CSV. Every decision you make in the next few exercises — what to drop, what to fill, what to flag — feeds directly into Module 15's analysis and the capstone. Cleaning isn't busywork before the 'real' analysis; it *is* real analytical work, and it's usually where most of a data project's actual time goes."

---

### EXERCISE 1 — Inspect (0:45–2:30)

**SAY:** "Never start cleaning until you've actually looked at what's broken — two calls that surface almost every kind of problem at once."

**DO:**
```python
import pandas as pd

df = pd.read_csv('data/messy_sales.csv')
print(df.info())
print(df.isnull().sum())
```
```bash
python3 clean.py
```

**CHECK:** `.info()` prints one line per column, showing its dtype and a "non-null count" that's *lower* than the total row count for any column with missing values — that gap is your first clue. `.isnull().sum()` prints the exact count of missing values per column, e.g.:
```
order_id           0
order_date         12
product_category    0
region              3
unit_price          47
quantity_sold        0
customer_id          8
```

**SAY:** "In a comment block, write down at least three specific issues — not 'data has problems,' but specific: 'unit_price has 47 missing values, about 2% of rows,' or 'order_date is dtype object, meaning pandas is treating it as text, not an actual date.'"

---

### EXERCISE 2 — Standardize Column Names (2:30–3:40)

**SAY:** "One line, cleaning up whatever inconsistent naming convention the raw file arrived with."

**DO:**
```python
df.columns = df.columns.str.lower().str.replace(' ', '_')
print(df.columns.tolist())
```
```bash
python3 clean.py
```

**CHECK:**
```
['order_id', 'order_date', 'product_category', 'region', 'unit_price', 'quantity_sold', 'customer_id']
```
All lowercase, no spaces — any column that originally had, say, `"Order Date"` now reads `order_date`.

**SAY:** "Trace the chain: `.str.lower()` runs on every column name at once, then `.str.replace(' ', '_')` runs on the result of that. This is exactly the same vectorized idea as Module 13's `df['revenue'] / df['quantity']` — one operation applied across a whole collection at once, no loop needed."

---

### EXERCISE 3 — Handle Missing Values (3:40–5:40)

**SAY:** "Two different strategies for two different kinds of missingness — and the choice between them needs a documented reason, not just a default habit."

**DO:**
```python
print(f"Shape before: {df.shape}")

# unit_price has relatively few missing values (47 of ~5000) — filling with the
# column mean preserves the row rather than losing real order data over one field.
df['unit_price'] = df['unit_price'].fillna(df['unit_price'].mean())

# order_id and order_date are essential identifiers — a row missing either one
# can't be reliably matched to a real transaction, so those rows get dropped entirely.
df = df.dropna(subset=['order_id', 'order_date'])

print(f"Shape after: {df.shape}")
print(df.isnull().sum())
```
```bash
python3 clean.py
```

**CHECK:** "Shape before" and "shape after" print two different row counts — the second is smaller, reflecting however many rows were missing `order_id` or `order_date`. `.isnull().sum()` afterward shows `0` for `unit_price` (filled) and `0` for `order_id`/`order_date` (rows dropped), while any other columns with missing values you haven't addressed yet still show a nonzero count.

**SAY:** "This is the core judgment call of the whole lab: fill when the column is non-essential and only lightly missing, drop when the missing field is something you genuinely can't substitute a reasonable guess for. Both choices need a comment explaining *why*, not just *what* — that's what Reflection Question 2 grades."

---

### EXERCISE 4 — Fix Types (5:40–7:40)

**SAY:** "Three columns, three different type-conversion problems — a date stored as text, a price stored with a currency symbol, and a count that should be a whole number."

**DO:**
```python
df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')

df['unit_price'] = df['unit_price'].astype(str).str.replace('$', '', regex=False).astype(float)

df['quantity_sold'] = df['quantity_sold'].astype(int)

print(df.dtypes)
```
```bash
python3 clean.py
```

**CHECK:**
```
order_id                     object
order_date            datetime64[ns]
product_category             object
region                       object
unit_price                  float64
quantity_sold                  int64
customer_id                  object
```

**SAY:** "`errors='coerce'` on `pd.to_datetime` is doing quiet, important work — any value that genuinely can't be parsed as a date becomes `NaT` (pandas' 'not a time' marker) instead of crashing the whole conversion. The `unit_price` line strips a literal dollar sign *before* converting to float, since `float('$19.99')` would raise a `ValueError` — the currency symbol has to go first."

**FIX:** If `.astype(int)` on `quantity_sold` raises an error, check whether that column still has any missing values — you can't convert `NaN` directly to an integer type; it needs to be filled or dropped first, same as Exercise 3.

---

### EXERCISE 5 — Check Duplicates (7:40–8:50)

**SAY:** "One more common data-quality issue — the exact same row appearing more than once."

**DO:**
```python
print(f"Duplicate rows: {df.duplicated().sum()}")
df = df.drop_duplicates()
print(f"Shape after removing duplicates: {df.shape}")
```
```bash
python3 clean.py
```

**CHECK:** The first line reports some count of duplicate rows (possibly `0`, if this dataset doesn't have any). If nonzero, the shape after `drop_duplicates()` shows fewer rows than before this step.

**SAY:** "`.duplicated()` flags every row that's an *exact* match of an earlier row across every single column — it won't catch two rows that are the same transaction with a typo in one field. That's a different, harder problem than what this method solves."

---

### EXERCISE 6 — Describe (8:50–10:30)

**SAY:** "Now step back and look at the cleaned data statistically — `.describe()` is where analytical thinking, not just code, starts to matter."

**DO:**
```python
print(df.describe())
```
```bash
python3 clean.py
```

**CHECK:** A table with `count`, `mean`, `std`, `min`, `25%`, `50%`, `75%`, `max` for every numeric column.

**SAY:** "Look specifically for two kinds of red flags: a `min` that's negative for a column that should never be negative — like `unit_price` or `quantity_sold` — which might indicate a refund or a data-entry error rather than a real sale. And a `max` that's wildly larger than the `75%` value, which could be a legitimate bulk order, or could be a typo — an extra zero typed into a quantity field. Write a comment proposing a business explanation for at least two suspicious values you find — that's the difference between running code and doing analysis."

---

### EXERCISE 7 — Save (10:30–11:50)

**SAY:** "Write the cleaned result out, then immediately reload it to prove the types actually survived the round trip."

**DO:**
```python
df.to_csv('data/clean_sales.csv', index=False)

reloaded = pd.read_csv('data/clean_sales.csv')
print(reloaded.info())
```
```bash
python3 clean.py
```

**CHECK:** `data/clean_sales.csv` exists on disk. The reloaded `.info()` output should closely match what you had right before saving — though watch `order_date` specifically: CSV files don't preserve pandas' `datetime64` dtype natively, so it very likely comes back as `object` (plain text) on reload, unless you explicitly re-parse it with `pd.to_datetime()` again after loading.

**SAY:** "That's a real, common gotcha worth calling out on camera: CSV is a plain-text format — it has no concept of 'this column is a date type,' it just stores whatever text representation pandas wrote out. Every time you reload a CSV, date columns need to be re-converted."

---

### REFLECTION QUESTIONS (11:50–12:30)

**SAY:** "Add these as a comment block at the top of the file."

**DO:** Answer honestly:
1. Which of the three cleaning decisions — drop, fill, or flag — feels most ambiguous to you? What additional information would you want before making that call on real data?
2. Look at your comments. If someone who didn't know the dataset read your script, would they understand why you made each decision? Revise any comment that only says *what* you did without saying *why*.
3. After running `.describe()`, what is the most important thing you noticed about this dataset that you did not expect when you first loaded it?

**CHECK:** Question 2 is a real audit, not just a reflection — go back through Exercise 3's comments specifically and confirm each one explains the *reasoning* (why fill vs. why drop), not just the mechanics.

---

### SUBMISSION CHECKLIST (12:30–end)

- [ ] `clean.py` (or `clean.ipynb`) runs top to bottom with no errors
- [ ] Exercise 1: `.info()` and `.isnull().sum()` output, with 3+ specific issues noted in a comment
- [ ] Exercise 2: column names standardized to lowercase with underscores
- [ ] Exercise 3: missing values handled with fill/drop, each choice commented with reasoning
- [ ] Exercise 4: `order_date`, `unit_price`, `quantity_sold` all converted to correct dtypes
- [ ] Exercise 5: duplicates checked and removed if present
- [ ] Exercise 6: `.describe()` run, with 2+ suspicious statistics identified and explained
- [ ] Exercise 7: `data/clean_sales.csv` written and verified by reloading
- [ ] Three reflection questions answered honestly
- [ ] `clean_sales.csv` pushed to GitHub in a `module14/` folder alongside `clean.py`
- [ ] Repo URL submitted to Canvas
