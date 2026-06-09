# ISM2411 Lab W15: Aggregate & Chart — Capstone Warm-up

## YouTube Metadata

**Title:** Aggregate & Chart: Capstone Warm-up — Lab Walkthrough | ISM2411 Lab 15
**Description:**
Walkthrough of ISM2411 Module 15 Lab. We use the cleaned sales data to answer three business questions with groupby aggregations and four publication-ready charts. This is the exact workflow the capstone uses.

Course page: https://markumreed.github.io/ism2411/pages/week15_lab.html

**Chapters:**
0:00 — What we're building
0:45 — Three business questions and groupby aggregations
3:30 — Revenue by region bar chart
5:30 — Top 10 products chart
7:00 — Monthly trend line chart and category pie chart
8:30 — Submission checklist

**Applies to:** ISM2411 Module 15

**Tags:** pandas groupby, matplotlib charts python, python business charts, python bar chart, ISM2411, USF, pandas aggregation tutorial, python data visualization

---

## Script

### INTRO (0:00–0:45)

Lab 15 — Aggregate and Chart, Capstone Warm-up. We use the cleaned data from Lab 14 to answer three business questions, then produce four charts. The workflow — question → groupby → chart → label → save — is identical to the capstone. This is the dress rehearsal.

---

### BUSINESS QUESTIONS AND GROUPBY (0:45–3:30)

```python
# aggregate.py
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("cleaned_sales.csv")

# Business Question 1: Which region drives the most revenue?
region_revenue = df.groupby("region")["revenue"].sum().sort_values(ascending=False)
print("Revenue by region:")
print(region_revenue)

# Business Question 2: Which are the top 10 products by revenue?
top_products = df.groupby("product")["revenue"].sum().sort_values(ascending=False).head(10)

# Business Question 3: How does revenue trend month over month?
df["date"] = pd.to_datetime(df["date"])
df["month"] = df["date"].dt.to_period("M")
monthly = df.groupby("month")["revenue"].sum()
```

State your findings as numbers with context — that's what Exercise 2 asks:
*"The East region drove $42,300 in revenue, which is 34% above the average region."*

---

### REVENUE BY REGION BAR CHART (3:30–5:30)

```python
fig, ax = plt.subplots(figsize=(8, 5))
region_revenue.plot(kind="bar", ax=ax, color="#2563eb", edgecolor="white")

ax.set_title("Total Revenue by Region", fontsize=14, fontweight="bold")
ax.set_xlabel("Region")
ax.set_ylabel("Revenue ($)")
ax.tick_params(axis="x", rotation=0)

# Add value labels on bars
for bar in ax.patches:
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 100,
        f"${bar.get_height():,.0f}",
        ha="center", va="bottom", fontsize=9
    )

plt.tight_layout()
plt.savefig("chart_region_revenue.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved chart_region_revenue.png")
```

Every chart needs: title, axis labels, value labels or a legend. Exercise 1 asks whether someone could state the key finding in 10 seconds. If not, fix the labels.

---

### TOP 10 PRODUCTS (5:30–7:00)

```python
fig, ax = plt.subplots(figsize=(10, 6))
top_products.plot(kind="barh", ax=ax, color="#16a34a")
ax.set_title("Top 10 Products by Revenue", fontsize=14, fontweight="bold")
ax.set_xlabel("Revenue ($)")
ax.invert_yaxis()   # highest revenue at the top
plt.tight_layout()
plt.savefig("chart_top_products.png", dpi=150, bbox_inches="tight")
plt.close()
```

Horizontal bars work better than vertical when product names are long.

---

### MONTHLY TREND AND CATEGORY PIE (7:00–8:30)

```python
# Monthly trend line
fig, ax = plt.subplots(figsize=(10, 5))
monthly.plot(kind="line", ax=ax, marker="o", color="#dc2626")
ax.set_title("Monthly Revenue Trend", fontsize=14, fontweight="bold")
ax.set_xlabel("Month")
ax.set_ylabel("Revenue ($)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("chart_monthly_trend.png", dpi=150, bbox_inches="tight")
plt.close()

# Category breakdown pie
category_rev = df.groupby("category")["revenue"].sum()
fig, ax = plt.subplots(figsize=(7, 7))
ax.pie(category_rev, labels=category_rev.index, autopct="%1.1f%%", startangle=90)
ax.set_title("Revenue by Category", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig("chart_category_pie.png", dpi=150, bbox_inches="tight")
plt.close()
```

---

### SUBMISSION CHECKLIST (8:30–10:00)

- Three business questions answered with groupby aggregations
- Four PNG chart files saved (region, top products, monthly, category)
- All charts have title, axis labels, and value labels or legend
- Findings written as numbers with context for Exercise 2
- `aggregate.py` (or `aggregate.ipynb`) and all four PNGs in `module15/` folder
- GitHub commit + Canvas URL
