# ISM2411 Lab W13: First DataFrame — Retail Sales Explorer

## YouTube Metadata

**Title:** First DataFrame — Retail Sales Explorer — Full Lab Walkthrough | ISM2411 Lab 13
**Description:**
Step-by-step, test-as-you-go walkthrough of ISM2411 Module 13 Lab — your first pandas DataFrame. Load retail_sales.csv, inspect its shape/columns/dtypes, filter by a single condition and by two combined conditions, sort by revenue, create a computed column, inspect unique values, select a column subset, and save the result — the foundation for every remaining pandas lab and the capstone.

Course page: https://markumreed.github.io/ism2411/pages/week13_lab.html

**Chapters:**
0:00 — What this lab covers — the foundation for the rest of the semester
0:45 — Exercise 1: load the CSV, inspect shape/columns/dtypes
2:20 — Exercise 2: filter by region
3:40 — Exercise 3: top 5 by revenue, and the index gotcha
5:00 — Exercise 4: the two-condition filter — & and parentheses
6:40 — Exercise 5: creating a computed column
8:00 — Exercise 6: unique values and value_counts()
9:20 — Exercise 7: selecting a column subset
10:20 — Exercise 8: saving the result
11:00 — Reflection questions
11:40 — Submission checklist

**Applies to:** ISM2411 Module 13

**Tags:** pandas dataframe tutorial, pandas boolean filter, pandas groupby value_counts, pandas read_csv to_csv, ISM2411, USF, pandas for business beginners

---

## How to Use This Script

**SAY** it, **DO** it, **CHECK** the exact output, **FIX** it if it doesn't match — then move to the next step. This lab uses the real `retail_sales.csv` provided on Canvas — the exact numbers you see (row counts, revenue totals) will differ from the illustrative examples below, since they depend on your actual dataset. What matters is confirming the *shape* of each result matches what's described.

---

## Script

### INTRO (0:00–0:45)

**SAY:** "Lab 13 — your first pandas DataFrame. Everything for the rest of the semester, including the capstone, builds on what we do in the next fifteen minutes: loading data, filtering it, computing new columns, and saving results. This is the foundation."

---

### EXERCISE 1 — Load It (0:45–2:20)

**SAY:** "Four inspection calls, run immediately after loading — never trust a dataset you haven't looked at first."

**DO:**
```python
import pandas as pd

df = pd.read_csv('data/retail_sales.csv')
print(df.head())
print(df.shape)
print(df.columns.tolist())
print(df.dtypes)
```
```bash
python3 explore.py
```

**CHECK:** `.head()` prints the first 5 rows as a formatted table. `.shape` prints a tuple like `(5000, 6)` — rows, then columns; your actual row count depends on the real file, but it should be in that ballpark. `.columns.tolist()` prints a plain Python list of column names, like `['order_id', 'region', 'product', 'quantity', 'revenue', 'date']`. `.dtypes` prints one line per column, showing `object` for text columns and `int64`/`float64` for numeric ones.

**SAY:** "Read `.dtypes`' output carefully — if a column you expect to be numeric (like `revenue`) instead shows `object`, that's an early warning sign the column contains some non-numeric text somewhere, which Module 14's data cleaning will deal with directly."

**FIX:** If `FileNotFoundError` on `read_csv`, confirm the CSV is actually at `data/retail_sales.csv` relative to where you're running the script — check with `ls data/`.

---

### EXERCISE 2 — Filter by Region (2:20–3:40)

**SAY:** "The single most common pandas operation — a boolean filter. `df['region'] == 'South'` produces a column of `True`/`False` values, and wrapping the whole thing in `df[...]` keeps only the rows where that's `True`."

**DO:**
```python
south = df[df['region'] == 'South']
print(len(south))
print(south.head())
```
```bash
python3 explore.py
```

**CHECK:** `len(south)` prints a single number — some fraction of your total row count. `south.head()` shows 5 rows, and every single one has `'South'` in the `region` column — no other region should ever appear here.

**SAY:** "Say it out loud: `df['region'] == 'South'` isn't filtering anything by itself — it just produces a same-length column of `True`/`False`. It's the *outer* `df[...]` that actually does the filtering, keeping only rows where that inner expression came out `True`."

---

### EXERCISE 3 — Top 5 by Revenue (3:40–5:00)

**SAY:** "Sorting, then taking the top few — and a small gotcha about the row index that catches almost everyone the first time."

**DO:**
```python
top5 = df.sort_values('revenue', ascending=False).head(5)
print(top5)
```
```bash
python3 explore.py
```

**CHECK:** 5 rows, with `revenue` values in strictly descending order from top to bottom. Look at the leftmost column — the row index — it will **not** read `0, 1, 2, 3, 4`. It'll show whatever the *original* row positions were before sorting, e.g. `847, 12, 3901, ...`.

**SAY:** "That's not a bug — `sort_values()` reorders the rows but keeps each row's original index label attached to it, so you can always trace a row back to where it started. If you wanted a clean `0, 1, 2, 3, 4` index instead, you'd chain on `.reset_index(drop=True)`."

---

### EXERCISE 4 — Two-Condition Filter (5:00–6:40)

**SAY:** "Now combine two conditions — and this is the one place pandas syntax genuinely differs from plain Python: `&` instead of `and`, and parentheses around each condition are non-negotiable."

**DO:**
```python
big_south = df[(df['region'] == 'South') & (df['revenue'] > 1000)]
print(len(big_south))
print(big_south.head())
```
```bash
python3 explore.py
```

**CHECK:** `len(big_south)` should be smaller than *either* `len(south)` from Exercise 2 alone, or the count of all `revenue > 1000` rows alone — since it requires *both* conditions simultaneously. Every row in `.head()` shows both `'South'` in `region` and a `revenue` value over `1000`.

**SAY:** "Two things that trip people up here: plain Python's `and` doesn't work row-by-row across a whole column, so pandas uses `&` instead. And without the parentheses around each individual condition, Python's operator precedence would try to evaluate `df['revenue'] > (1000 & df['region'])` or similar nonsense — the parentheses force each comparison to fully evaluate first, *then* combine with `&`."

---

### EXERCISE 5 — A New Column (6:40–8:00)

**SAY:** "Creating a new column is just an assignment — pandas computes it for every row at once, no loop required."

**DO:**
```python
df['per_unit'] = df['revenue'] / df['quantity']
print(df.head())
print(df['per_unit'].mean())
```
```bash
python3 explore.py
```

**CHECK:** `.head()` now shows a `per_unit` column that wasn't there in Exercise 1 — one more column than before. `.mean()` returns a single float — the average per-unit price across every row in the entire dataset.

**SAY:** "This is the single biggest shift from Module 6's manual loops — `df['revenue'] / df['quantity']` divides *every row's* revenue by *that same row's* quantity, all in one vectorized operation, without writing a single `for` loop."

---

### EXERCISE 6 — Unique Values (8:00–9:20)

**SAY:** "Two related but different views of the same column — one shows what values exist, the other shows how often each one appears."

**DO:**
```python
print(df['region'].unique())
print(df['region'].value_counts())
```
```bash
python3 explore.py
```

**CHECK:** `.unique()` prints a plain array of distinct values, e.g. `['South' 'North' 'East' 'West']` — no counts, no particular order, just the set of values that appear. `.value_counts()` prints a small table, each distinct value alongside how many rows contain it, sorted from most common to least — the four values should roughly sum to your total row count from Exercise 1 (allowing for any nulls, which `value_counts()` excludes by default).

---

### EXERCISE 7 — Select Columns (9:20–10:20)

**SAY:** "A quick way to reduce a wide dataset down to only the columns you actually need for a given analysis."

**DO:**
```python
subset = df[['region', 'product', 'revenue']]
print(subset.shape)
```
```bash
python3 explore.py
```

**CHECK:** `subset.shape` prints `(same_row_count, 3)` — same number of rows as the full DataFrame, but exactly 3 columns instead of 6 (or however many the original had, now plus the `per_unit` column from Exercise 5).

**SAY:** "Notice the double square brackets — `df[['region', 'product', 'revenue']]`. Single brackets with a list of names would raise an error; the outer brackets mean 'select from this DataFrame,' and the inner list is what to select — a list of column names, not one bare name."

---

### EXERCISE 8 — Save (10:20–11:00)

**SAY:** "Last step — write the DataFrame, with its new `per_unit` column, back out to a file."

**DO:**
```python
df.to_csv('data/explored.csv', index=False)
```
```bash
python3 explore.py
ls data/
```

**CHECK:** `data/explored.csv` now exists alongside the original `retail_sales.csv`. Open it in a text editor and confirm the header row includes `per_unit` at the end — that column didn't exist in the original file, so its presence confirms this is the *transformed* output, not just a copy.

**SAY:** "`index=False` is the important part here — without it, pandas would write that row-index column from Exercise 3's sorting gotcha out as an extra, meaningless first column in the CSV."

---

### REFLECTION QUESTIONS (11:00–11:40)

**DO:** Answer honestly:
1. Without looking at your code, can you explain what a boolean filter does in plain English? Practice saying it out loud.
2. What is the difference between `df["revenue"]` and `df[["revenue"]]`? When does the distinction matter?
3. If a colleague who only knows Excel asked you to explain why you'd choose pandas for this task, what's the single most compelling reason you'd give?

**CHECK:** Question 2's honest answer: `df["revenue"]` (single brackets, single name) returns a **Series** — a single column — while `df[["revenue"]]` (double brackets) returns a **DataFrame** with just one column in it. The distinction matters whenever a later operation expects a DataFrame specifically (like most plotting and `.to_csv()` calls that assume multiple columns) rather than a bare Series.

---

### SUBMISSION CHECKLIST (11:40–end)

- [ ] `explore.py` (or `explore.ipynb`) runs top to bottom with no errors
- [ ] Exercise 1: `.head()`, `.shape`, `.columns.tolist()`, `.dtypes` all printed
- [ ] Exercise 2: single-condition filter, with row count and head printed
- [ ] Exercise 3: top 5 by revenue, sorted descending
- [ ] Exercise 4: two-condition filter using `&` and parentheses
- [ ] Exercise 5: `per_unit` column created, mean computed
- [ ] Exercise 6: `.unique()` and `.value_counts()` both printed
- [ ] Exercise 7: 3-column subset created, shape confirmed
- [ ] Exercise 8: `data/explored.csv` written and verified
- [ ] Three reflection questions answered honestly
- [ ] Pushed to GitHub in a `module13/` folder
- [ ] Repo URL submitted to Canvas
