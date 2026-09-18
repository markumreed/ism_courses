# ISM2411 Lab W15: Aggregate & Chart — Capstone Warm-up

## YouTube Metadata

**Title:** Aggregate & Chart — Capstone Warm-up — Full Lab Walkthrough | ISM2411 Lab 15
**Description:**
Step-by-step, test-as-you-go walkthrough of ISM2411 Module 15 Lab — the direct dress rehearsal for the capstone. Answer three required business questions with a bar chart, a line chart, and a histogram, add your own fourth chart, rebuild one in Seaborn, run a multi-aggregation .agg() call, and tidy a notebook with markdown headings.

Course page: https://markumreed.github.io/ism2411/pages/week15_lab.html

**Chapters:**
0:00 — What this lab covers — this is the capstone dress rehearsal
0:50 — Exercise 1: Q1 — revenue by region, bar chart
2:40 — Exercise 2: Q2 — monthly revenue trend, line chart
4:50 — Exercise 3: Q3 — order size distribution, histogram
6:40 — Exercise 4: Q4 — your own business question
7:50 — Exercise 5: the Seaborn version
9:10 — Exercise 6: multiple aggregations with .agg()
10:20 — Exercise 7: notebook tidy-up with markdown headings
11:00 — Reflection questions
11:40 — Submission checklist

**Applies to:** ISM2411 Module 15

**Tags:** matplotlib bar line histogram tutorial, seaborn barplot lineplot histplot, pandas groupby agg, seaborn heatmap pivot_table, ISM2411, USF, pandas for business beginners

---

## How to Use This Script

**SAY** it, **DO** it, **CHECK** the exact output, **FIX** it if it doesn't match — then move to the next step. This lab runs on your own cleaned `clean_sales.csv` from Module 14 — the illustrative numbers below (top region, peak month, etc.) will differ on your real data. What matters is the *shape* of the workflow: this is the exact standard the capstone will hold you to.

---

## Script

### INTRO (0:00–0:50)

**SAY:** "Lab 15 — aggregate and chart, the capstone warm-up. Every requirement in this lab — the workflow, the standards, the deliverable format — is identical to what the capstone asks for. If you can do this lab cleanly, you already know how to do the capstone; it's just a longer version of exactly this."

---

### EXERCISE 1 — Q1: Revenue by Region (0:50–2:40)

**SAY:** "First required chart: total revenue, grouped by region, as a bar chart — with everything a chart needs to stand on its own: a title, labeled axes, and a saved file."

**DO:**
```python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data/clean_sales.csv')

by_region = df.groupby('region')['revenue'].sum().reset_index()
by_region = by_region.sort_values('revenue', ascending=False)

plt.figure(figsize=(8, 5))
plt.bar(by_region['region'], by_region['revenue'], color='steelblue')
plt.title('Total Revenue by Region')
plt.xlabel('Region')
plt.ylabel('Revenue ($)')
plt.tight_layout()
plt.savefig('charts/q1_revenue_by_region.png')
plt.show()
```
```bash
mkdir -p charts
python3 aggregate.py
```

**CHECK:** `charts/q1_revenue_by_region.png` exists, showing bars sorted tallest to shortest, a clear title, and both axes labeled. Read off the tallest bar and write one sentence: e.g., "South drove $184,320 in revenue, the highest of any region."

**SAY:** "`.reset_index()` matters here — `groupby(...).sum()` alone returns `region` as the index rather than a normal column, and `plt.bar()` needs it as an actual column to plot against."

---

### EXERCISE 2 — Q2: Monthly Revenue Trend (2:40–4:50)

**SAY:** "Second required chart — revenue over time, which means extracting a month number from the date column first."

**DO:**
```python
df['order_date'] = pd.to_datetime(df['order_date'])
df['month'] = df['order_date'].dt.month

by_month = df.groupby('month')['revenue'].sum().reset_index()

plt.figure(figsize=(9, 5))
plt.plot(by_month['month'], by_month['revenue'], marker='o', color='darkorange')
plt.title('Monthly Revenue Trend')
plt.xlabel('Month')
plt.ylabel('Revenue ($)')
plt.xticks(range(1, 13))
plt.tight_layout()
plt.savefig('charts/q2_monthly_trend.png')
plt.show()
```
```bash
python3 aggregate.py
```

**CHECK:** `charts/q2_monthly_trend.png` shows a line with visible circular markers at every data point, x-axis ticks for all 12 months even if some months have no data. Compute the peak: `by_month.loc[by_month['revenue'].idxmax()]` and write one sentence, e.g., "November was the peak month at $31,200, about 22% above the monthly average."

**SAY:** "`.dt.month` only works because `order_date` was explicitly re-parsed with `pd.to_datetime()` first — remember from Module 14, a column reloaded from CSV comes back as plain text, not a real date, until you convert it again."

---

### EXERCISE 3 — Q3: Order Size Distribution (4:50–6:40)

**SAY:** "Third required chart — not grouped by anything, just the raw shape of how order revenue is distributed across every single transaction."

**DO:**
```python
plt.figure(figsize=(8, 5))
plt.hist(df['revenue'], bins=20, color='seagreen', edgecolor='black')
plt.title('Order Size Distribution')
plt.xlabel('Revenue ($)')
plt.ylabel('Number of Orders')
plt.tight_layout()
plt.savefig('charts/q3_order_distribution.png')
plt.show()

print(f"Median order size: ${df['revenue'].median():.2f}")
print(f"Mean order size: ${df['revenue'].mean():.2f}")
```
```bash
python3 aggregate.py
```

**CHECK:** `charts/q3_order_distribution.png` shows 20 bars forming a distribution shape. Compare the printed mean and median — if the mean is noticeably *higher* than the median, the distribution is right-skewed (a small number of very large orders pull the mean up); if they're close, it's roughly symmetric.

**SAY:** "Write one sentence connecting the shape to a real decision: right-skewed data means the mean gets pulled upward by a few big orders, so the median is usually the more honest 'typical order size' for a business report — the mean alone can make a typical customer's order look larger than it really is."

---

### EXERCISE 4 — Q4: Your Own Business Question (6:40–7:50)

**SAY:** "Now a chart with no template — pick a question you're genuinely curious about from this dataset, and justify the chart type you chose for it."

**DO:** For example, revenue by product category:
```python
by_category = df.groupby('product_category')['revenue'].sum().sort_values(ascending=False)

# A horizontal bar chart works well here because category names can be long —
# horizontal bars keep labels readable without rotating or truncating text.
plt.figure(figsize=(8, 5))
plt.barh(by_category.index, by_category.values, color='mediumpurple')
plt.title('Revenue by Product Category')
plt.xlabel('Revenue ($)')
plt.tight_layout()
plt.savefig('charts/q4_custom.png')
plt.show()
```
```bash
python3 aggregate.py
```

**CHECK:** `charts/q4_custom.png` exists, with a comment above it explaining *why* this specific chart type fits this specific question — not just "I made a bar chart."

**SAY:** "This is graded on the quality of the question as much as the chart itself — pick something a real manager reading this dataset would actually want to know, not just the easiest thing to plot."

---

### EXERCISE 5 — Seaborn Version (7:50–9:10)

**SAY:** "Now rebuild one of the three required charts using Seaborn instead of matplotlib, and notice what changes."

**DO:**
```python
import seaborn as sns

plt.figure(figsize=(8, 5))
sns.barplot(data=by_region, x='region', y='revenue', hue='region', palette='Blues_d', legend=False)
plt.title('Total Revenue by Region (Seaborn)')
plt.xlabel('Region')
plt.ylabel('Revenue ($)')
plt.tight_layout()
plt.savefig('charts/q1_seaborn_version.png')
plt.show()
```
```bash
python3 aggregate.py
```

**CHECK:** A bar chart visually similar in content to Exercise 1's, but with Seaborn's default styling — typically a lighter background grid and a different default color palette.

**SAY:** "Write a comment naming one concrete difference — commonly: Seaborn's default styling looks more polished with less manual configuration, but matplotlib gives you more granular control when you need something Seaborn doesn't have a built-in shortcut for."

---

### EXERCISE 6 — Multiple Aggregations (9:10–10:20)

**SAY:** "One `.agg()` call computing two different statistics per group at once, instead of two separate `groupby` calls."

**DO:**
```python
region_summary = df.groupby('region').agg(
    total_revenue=('revenue', 'sum'),
    order_count=('revenue', 'count')
).reset_index()
region_summary['avg_order_value'] = region_summary['total_revenue'] / region_summary['order_count']

print(region_summary)
```
```bash
python3 aggregate.py
```

**CHECK:** A table with columns `region`, `total_revenue`, `order_count`, `avg_order_value`. In a comment, name which region has the most orders (`order_count`) and which has the highest `avg_order_value` — these are not necessarily the same region, and that distinction itself is worth a sentence.

**SAY:** "Named aggregation — `total_revenue=('revenue', 'sum')` — is doing two things: aggregating the `revenue` column with `'sum'`, and naming the result column `total_revenue` directly, rather than ending up with a generic column name you'd have to rename afterward."

---

### EXERCISE 7 — Notebook Tidy-Up (10:20–11:00)

**SAY:** "Presentation matters — a notebook or script full of unlabeled code blocks is much harder for a reader (including a grader) to follow than one with a clear narrative."

**DO:** If working in Jupyter, add a markdown cell before each chart block:
```markdown
## Q1: Which region drives the most revenue?
```
If working in a `.py` file, add a section comment instead:
```python
# --- Q1: Which region drives the most revenue? ---
```

**CHECK:** Every one of your four required charts has a clear one-sentence business question stated directly above its code — a reader should be able to skim just the headings/comments and understand the entire report's structure without reading any code.

---

### REFLECTION QUESTIONS (11:00–11:40)

**DO:** Answer honestly:
1. Look at each of your four charts. If someone who had never seen this dataset looked at them for 10 seconds, could they state the key finding? If not, what needs to change — the chart type, the labels, or the title?
2. The capstone requires you to state your findings as numbers with context: "Region X drove $Y in revenue, which is Z% above the average." Practice writing that sentence for each of your three required charts.
3. This lab is the capstone dress rehearsal. What felt difficult or unclear? Note it now — the capstone is a longer version of exactly this workflow, and Module 16 gives you dedicated time to finish.

**CHECK:** Question 2 is worth actually doing, not just describing — write the three sentences out for real, using your own computed numbers from Exercises 1–3, since that's the exact deliverable format the capstone will hold you to.

---

### SUBMISSION CHECKLIST (11:40–end)

- [ ] `aggregate.ipynb` (or `aggregate.py`) runs top to bottom with no errors
- [ ] Exercise 1: `charts/q1_revenue_by_region.png` with title, axis labels, sorted bars, and a one-sentence finding
- [ ] Exercise 2: `charts/q2_monthly_trend.png` with markers, all 12 months, and a one-sentence finding
- [ ] Exercise 3: `charts/q3_order_distribution.png` with 20 bins, median/mean printed, skew described
- [ ] Exercise 4: `charts/q4_custom.png` answering your own business question, with a justifying comment
- [ ] Exercise 5: one chart rebuilt in Seaborn, with a comparison comment
- [ ] Exercise 6: `.agg()` table with total revenue and order count per region, both questions answered in a comment
- [ ] Exercise 7: markdown headings or section comments before every chart
- [ ] Three reflection questions answered honestly
- [ ] All 4 required PNG files pushed to GitHub in a `module15/` folder
- [ ] Repo URL submitted to Canvas
