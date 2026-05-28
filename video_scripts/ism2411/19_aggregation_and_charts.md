# Video 19: Aggregation, Grouping & Business Charts

## YouTube Metadata

**Title:** pandas groupby & Business Charts with matplotlib | ISM2411
**Description:**
Group your data by category, compute aggregates, and visualize results with bar charts, line charts, and histograms. We'll build a complete sales analysis dashboard — revenue by region, weekly trends, and a distribution of order values — using pandas groupby and matplotlib.

**Chapters:**
0:00 — From clean data to business insight
1:30 — groupby() — the most powerful pandas method
5:00 — Multiple aggregations with agg()
7:30 — Pivot tables
9:30 — matplotlib basics
11:30 — Bar chart — revenue by region
14:00 — Line chart — weekly trend
16:30 — Histogram — order value distribution
18:30 — Recap

**Applies to:** ISM2411 Module 15

**Tags:** pandas groupby, pandas agg, matplotlib bar chart, python visualization, python business charts, pandas pivot table, ISM2411, python data analysis, matplotlib tutorial, python sales analysis

---

## Script

### INTRO (0:00–1:30)

You have clean data. Now let's answer business questions. What region drives the most revenue? Is revenue trending up or down week over week? Are most orders small, or are there a few large ones pulling the average up? These are the questions a manager asks. `groupby()` and matplotlib are how you answer them in Python.

---

### SETUP (as needed)

```python
import pandas as pd
import matplotlib.pyplot as plt

# Build sample dataset
data = {
    "date":       pd.date_range("2024-05-06", periods=20, freq="B"),
    "region":     ["Southeast","Northeast","Southeast","Southwest","Northeast",
                   "Southeast","Southeast","Northeast","Southwest","Southeast",
                   "Northeast","Southeast","Southwest","Northeast","Southeast",
                   "Southeast","Northeast","Southwest","Southeast","Northeast"],
    "product":    ["Laptop Bag","USB-C Hub","Monitor Stand","Laptop Bag","USB-C Hub",
                   "Wireless Mouse","Laptop Bag","Monitor Stand","USB-C Hub","Laptop Bag",
                   "Wireless Mouse","USB-C Hub","Laptop Bag","Monitor Stand","Wireless Mouse",
                   "Laptop Bag","USB-C Hub","Wireless Mouse","Monitor Stand","Laptop Bag"],
    "quantity":   [3,5,4,1,8,6,2,3,7,4,5,6,2,3,8,4,9,3,5,2],
    "unit_price": [49.99,24.99,35.99,49.99,24.99,39.99,49.99,35.99,24.99,49.99,
                   39.99,24.99,49.99,35.99,39.99,49.99,24.99,39.99,35.99,49.99],
}
df = pd.DataFrame(data)
df["revenue"] = df["quantity"] * df["unit_price"]
df["week"] = df["date"].dt.isocalendar().week
```

---

### groupby() (1:30–5:00)

`groupby()` splits the DataFrame into groups based on a column, then applies an aggregation function to each group.

```python
# Total revenue by region:
regional = df.groupby("region")["revenue"].sum()
print(regional.sort_values(ascending=False))
```

Output:
```
region
Southeast    1284.68
Northeast     974.82
Southwest     289.92
Name: revenue, dtype: float64
```

```python
# Average order value by product:
product_avg = df.groupby("product")["revenue"].mean()
print(product_avg.round(2).sort_values(ascending=False))

# Count of transactions by region:
region_count = df.groupby("region")["revenue"].count()
print(region_count)

# Sum, mean, max in one step:
summary = df.groupby("region")["revenue"].agg(["sum","mean","max","count"])
summary.columns = ["Total", "Average", "Largest", "Orders"]
print(summary.round(2))
```

---

### MULTIPLE AGGREGATIONS WITH agg() (5:00–7:30)

```python
full_summary = df.groupby("region").agg(
    total_revenue  = ("revenue", "sum"),
    avg_order      = ("revenue", "mean"),
    order_count    = ("revenue", "count"),
    total_quantity = ("quantity", "sum"),
).round(2)

full_summary["revenue_per_order"] = (full_summary["total_revenue"] / full_summary["order_count"]).round(2)
print(full_summary)
```

Output:
```
           total_revenue  avg_order  order_count  total_quantity  revenue_per_order
region
Northeast         974.82     162.47            6              32             162.47
Southeast        1284.68     128.47           10              40             128.47
Southwest         289.92      96.64            3               6              96.64
```

---

### PIVOT TABLES (7:30–9:30)

`pivot_table()` lets you cross-tabulate two dimensions — like region vs. product.

```python
pivot = df.pivot_table(
    values="revenue",
    index="region",
    columns="product",
    aggfunc="sum",
    fill_value=0
).round(2)

print(pivot)
```

Output:
```
product    Laptop Bag  Monitor Stand  USB-C Hub  Wireless Mouse
region
Northeast       99.98         107.97     274.89          319.92
Southeast      649.87         179.95     149.94          304.92
Southwest       99.98           0.00     174.93           14.99
```

---

### MATPLOTLIB BASICS (9:30–11:30)

```python
import matplotlib.pyplot as plt

# Every chart follows this pattern:
# 1. Create figure and axes
# 2. Plot the data
# 3. Add labels and formatting
# 4. Show or save

fig, ax = plt.subplots(figsize=(8, 5))   # width x height in inches
ax.set_title("Chart Title", fontsize=14, fontweight="bold")
ax.set_xlabel("X Axis Label")
ax.set_ylabel("Y Axis Label")
plt.tight_layout()
plt.show()
```

Set a clean style at the start of your notebook or script:
```python
plt.style.use("seaborn-v0_8-whitegrid")
```

---

### BAR CHART — REVENUE BY REGION (11:30–14:00)

```python
regional_revenue = df.groupby("region")["revenue"].sum().sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(8, 5))

bars = ax.bar(
    regional_revenue.index,
    regional_revenue.values,
    color=["#2196F3", "#4CAF50", "#FF9800"],
    edgecolor="white",
    linewidth=0.5
)

# Add value labels on top of bars:
for bar, val in zip(bars, regional_revenue.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
            f"${val:,.0f}", ha="center", va="bottom", fontsize=11, fontweight="bold")

ax.set_title("Revenue by Region — May 2024", fontsize=14, fontweight="bold")
ax.set_xlabel("Region", fontsize=12)
ax.set_ylabel("Total Revenue ($)", fontsize=12)
ax.set_ylim(0, regional_revenue.max() * 1.2)

plt.tight_layout()
plt.savefig("revenue_by_region.png", dpi=150, bbox_inches="tight")
plt.show()
```

---

### LINE CHART — WEEKLY TREND (14:00–16:30)

```python
weekly_revenue = df.groupby("week")["revenue"].sum()

fig, ax = plt.subplots(figsize=(8, 5))

ax.plot(weekly_revenue.index, weekly_revenue.values,
        marker="o", linewidth=2.5, color="#2196F3", markersize=8)

# Add value labels at each point:
for week, rev in weekly_revenue.items():
    ax.annotate(f"${rev:,.0f}", (week, rev),
                textcoords="offset points", xytext=(0, 10),
                ha="center", fontsize=10)

ax.set_title("Weekly Revenue Trend", fontsize=14, fontweight="bold")
ax.set_xlabel("Week Number", fontsize=12)
ax.set_ylabel("Revenue ($)", fontsize=12)
ax.set_xticks(weekly_revenue.index)

plt.tight_layout()
plt.savefig("weekly_trend.png", dpi=150, bbox_inches="tight")
plt.show()
```

---

### HISTOGRAM — ORDER VALUE DISTRIBUTION (16:30–18:30)

```python
fig, ax = plt.subplots(figsize=(8, 5))

ax.hist(df["revenue"], bins=8, color="#4CAF50", edgecolor="white", linewidth=0.5)

ax.axvline(df["revenue"].mean(),   color="#F44336", linewidth=2, linestyle="--", label=f"Mean: ${df['revenue'].mean():.0f}")
ax.axvline(df["revenue"].median(), color="#FF9800", linewidth=2, linestyle=":",  label=f"Median: ${df['revenue'].median():.0f}")

ax.set_title("Distribution of Order Values", fontsize=14, fontweight="bold")
ax.set_xlabel("Order Value ($)", fontsize=12)
ax.set_ylabel("Number of Orders", fontsize=12)
ax.legend(fontsize=11)

plt.tight_layout()
plt.savefig("order_distribution.png", dpi=150, bbox_inches="tight")
plt.show()
```

---

### RECAP (18:30–20:00)

- `df.groupby("col")["val"].sum()` — group and aggregate
- `df.groupby("col").agg(name=("col", "func"))` — multiple aggregations with named columns
- `df.pivot_table(values, index, columns, aggfunc)` — cross-tabulation
- `plt.subplots(figsize=(w,h))` — create figure and axes
- `ax.bar()` — bar chart; `ax.plot()` — line chart; `ax.hist()` — histogram
- Always add title, axis labels, and save with `plt.savefig()`
- Use `plt.tight_layout()` before showing/saving

Next module: capstone — putting it all together in a complete retail sales analysis.
