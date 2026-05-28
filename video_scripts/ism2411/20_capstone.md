# Video 20: Capstone Walkthrough — Retail Sales Analysis

## YouTube Metadata

**Title:** Python Capstone Walkthrough — End-to-End Retail Sales Analysis | ISM2411
**Description:**
Watch a complete business analytics project built from scratch: load a retail sales dataset, clean it, answer five business questions, produce four visualizations, and save a formatted summary report. This is the ISM2411 capstone pattern — use it as a reference for structuring your own project.

**Chapters:**
0:00 — Project overview and structure
2:00 — Loading and inspecting the data
5:00 — Cleaning and validation
8:30 — Business question 1: revenue by category
11:00 — Business question 2: weekly trend
13:30 — Business question 3: top 10 products
15:30 — Business question 4: regional performance
18:00 — Business question 5: customer segment analysis
20:00 — Summary report output
22:00 — Recap and submission checklist

**Applies to:** ISM2411 Module 16

**Tags:** python capstone, python business analysis, pandas project, python data analysis project, ISM2411, retail sales analysis, python portfolio, data analytics python, pandas matplotlib project

---

## Script

### INTRO (0:00–2:00)

This video walks through a complete capstone project — start to finish. You're not expected to follow along and type everything — this is a reference. Watch it before you start your own project to understand the structure. Watch it again after if you get stuck. The pattern here is the pattern your project should follow.

A professional analytics deliverable has five parts: a clean dataset, documented data quality decisions, answers to specific business questions with code, visualizations, and a written summary. Let's build all five.

---

### PROJECT STRUCTURE (as intro)

```
ism2411-capstone/
├── data/
│   ├── retail_sales_raw.csv
│   └── retail_sales_clean.csv
├── analysis.py
├── charts/
│   ├── revenue_by_category.png
│   ├── weekly_trend.png
│   ├── top_products.png
│   └── regional_performance.png
├── report.txt
└── README.md
```

Good project hygiene: separate raw data from clean data, separate charts from code, include a README explaining what the project does and how to run it.

---

### LOADING AND INSPECTING (2:00–5:00)

```python
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

plt.style.use("seaborn-v0_8-whitegrid")

# Load
df = pd.read_csv("data/retail_sales_raw.csv", parse_dates=["date"])

# Inspect
print("Shape:", df.shape)
print("\nColumns:", df.columns.tolist())
print("\nFirst 5 rows:")
print(df.head())
print("\nData types:")
print(df.dtypes)
print("\nNull counts:")
print(df.isnull().sum())
print("\nNumeric summary:")
print(df.describe())
```

Document your observations in comments — this is part of your deliverable.

---

### CLEANING (5:00–8:30)

```python
print(f"\n--- DATA QUALITY REPORT ---")
print(f"Raw rows: {len(df)}")

# Drop rows with null in critical columns
df = df.dropna(subset=["date", "product", "category", "region"])
print(f"After dropping critical nulls: {len(df)}")

# Fix quantity and price types
df["quantity"]   = pd.to_numeric(df["quantity"],   errors="coerce")
df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")

# Remove rows where quantity or price couldn't be parsed
df = df.dropna(subset=["quantity", "unit_price"])
df = df[df["quantity"] > 0]
df = df[df["unit_price"] > 0]
print(f"After removing invalid quantities/prices: {len(df)}")

# Standardize text
df["category"] = df["category"].str.strip().str.title()
df["region"]   = df["region"].str.strip().str.title()
df["product"]  = df["product"].str.strip()

# Add computed columns
df["revenue"]  = df["quantity"] * df["unit_price"]
df["week"]     = df["date"].dt.isocalendar().week
df["month"]    = df["date"].dt.month

# Save clean data
df.to_csv("data/retail_sales_clean.csv", index=False)
print(f"Clean rows saved: {len(df)}")
```

---

### Q1: REVENUE BY CATEGORY (8:30–11:00)

```python
cat_revenue = (
    df.groupby("category")["revenue"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)
cat_revenue.columns = ["Category", "Total Revenue"]

print("\n--- Q1: Revenue by Category ---")
print(cat_revenue.to_string(index=False))

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(cat_revenue["Category"], cat_revenue["Total Revenue"],
               color="#1976D2", edgecolor="white")

for bar, val in zip(bars, cat_revenue["Total Revenue"]):
    ax.text(bar.get_width() + 500, bar.get_y() + bar.get_height()/2,
            f"${val:,.0f}", va="center", fontsize=10)

ax.set_title("Revenue by Product Category", fontsize=14, fontweight="bold")
ax.set_xlabel("Total Revenue ($)")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
plt.tight_layout()
plt.savefig("charts/revenue_by_category.png", dpi=150, bbox_inches="tight")
plt.close()
print("Chart saved: charts/revenue_by_category.png")
```

---

### Q2: WEEKLY TREND (11:00–13:30)

```python
weekly = df.groupby("week")["revenue"].sum()

print("\n--- Q2: Weekly Revenue Trend ---")
print(weekly.to_string())

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(weekly.index, weekly.values, marker="o", linewidth=2.5, color="#388E3C")
ax.fill_between(weekly.index, weekly.values, alpha=0.15, color="#388E3C")

ax.set_title("Weekly Revenue Trend", fontsize=14, fontweight="bold")
ax.set_xlabel("Week Number")
ax.set_ylabel("Revenue ($)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
plt.tight_layout()
plt.savefig("charts/weekly_trend.png", dpi=150, bbox_inches="tight")
plt.close()
```

---

### Q3: TOP 10 PRODUCTS (13:30–15:30)

```python
top_products = (
    df.groupby("product")["revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\n--- Q3: Top 10 Products by Revenue ---")
for rank, (product, rev) in enumerate(top_products.items(), 1):
    print(f"  {rank:2}. {product:<30} ${rev:>10,.2f}")

fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(top_products.index[::-1], top_products.values[::-1], color="#7B1FA2")
ax.set_title("Top 10 Products by Revenue", fontsize=14, fontweight="bold")
ax.set_xlabel("Total Revenue ($)")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
plt.tight_layout()
plt.savefig("charts/top_products.png", dpi=150, bbox_inches="tight")
plt.close()
```

---

### Q4: REGIONAL PERFORMANCE (15:30–18:00)

```python
regional = df.groupby("region").agg(
    total_revenue  = ("revenue", "sum"),
    avg_order      = ("revenue", "mean"),
    order_count    = ("revenue", "count"),
).round(2).sort_values("total_revenue", ascending=False)

regional["share_pct"] = (regional["total_revenue"] / regional["total_revenue"].sum() * 100).round(1)

print("\n--- Q4: Regional Performance ---")
print(regional.to_string())

fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(regional["total_revenue"], labels=regional.index,
       autopct="%1.1f%%", startangle=140,
       colors=["#1976D2","#388E3C","#F57C00","#7B1FA2"])
ax.set_title("Revenue Share by Region", fontsize=14, fontweight="bold")
plt.savefig("charts/regional_performance.png", dpi=150, bbox_inches="tight")
plt.close()
```

---

### SUMMARY REPORT (20:00–22:00)

```python
total_rev    = df["revenue"].sum()
total_orders = len(df)
avg_order    = df["revenue"].mean()
best_cat     = cat_revenue.iloc[0]["Category"]
best_region  = regional.index[0]
best_product = top_products.index[0]

report = f"""
CAMPUS BOOKSTORE — RETAIL SALES ANALYSIS
{"=" * 50}
Analysis period: {df["date"].min().date()} to {df["date"].max().date()}
Total orders:    {total_orders:,}
Total revenue:   ${total_rev:,.2f}
Average order:   ${avg_order:.2f}

KEY FINDINGS
{"─" * 50}
Top category:    {best_cat}
Top region:      {best_region} ({regional.loc[best_region, 'share_pct']:.1f}% of revenue)
Top product:     {best_product} (${top_products.iloc[0]:,.2f})

CATEGORY BREAKDOWN
{"─" * 50}
"""
for _, row in cat_revenue.iterrows():
    pct = row["Total Revenue"] / total_rev * 100
    report += f"  {row['Category']:<25} ${row['Total Revenue']:>10,.2f}  ({pct:.1f}%)\n"

with open("report.txt", "w") as f:
    f.write(report)
print(report)
print("Report saved to report.txt")
```

---

### RECAP AND CHECKLIST (22:00–25:00)

**Submission checklist:**

- [ ] `data/` folder with raw and clean CSV
- [ ] `analysis.py` runs without errors from top to bottom
- [ ] Null handling documented with comments
- [ ] 4+ charts saved as PNG files
- [ ] 3+ business questions answered with code and output
- [ ] `report.txt` with key findings
- [ ] `README.md` explaining what the project does and how to run it
- [ ] All files committed and pushed to GitHub
- [ ] GitHub URL submitted on Canvas

**The pattern for every business analytics project:**
1. Load and inspect
2. Document data quality issues and decisions
3. Clean
4. Answer specific questions with code
5. Visualize
6. Summarize in plain language

That's the capstone. Good luck.
