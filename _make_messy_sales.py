"""Generate ism2411/assets/downloads/messy_sales.csv for Module 14.

Usage (from the parent repo root): python3 _make_messy_sales.py ism2411/assets/downloads/messy_sales.csv

Raw columns have spaces and capitals; after the Module 14 one-liner they are
order_id, order_date, product_category, region, unit_price, quantity_sold, customer_id.
4,800 rows (the reading's number), 2025 dates with a holiday peak (Lab 15 Q2).
Problems planted, each one Module 14 teaches:
  - Unit Price is text like "$1,299.00"; returns are "-$45.00"
  - Order Date: mostly 2025-03-14, about 1% typed 03/14/2025 or March 14 2025,
    a few junk values, a few blank. The first rows are clean ISO dates, because
    pd.to_datetime guesses ONE format from the first value and coerces the rest.
  - blanks: Order ID (~0.5%), Customer ID (~7%), Region (~2%), Quantity Sold (~2%)
  - Quantity Sold: a few zeros and three 9999 placeholders
  - 48 exact duplicate rows (export glitch)
Seeded, so a rerun gives the same bytes.
"""

import csv
import random
import sys
from datetime import date, timedelta

OUT = sys.argv[1]
TOTAL_ROWS = 4800
DUPLICATES = 48
SEED = 1414
CLEAN_HEAD = 40  # first rows stay fully clean

# category: (low price, high price, typical max quantity, weight)
CATEGORIES = {
    "Electronics": (49, 1899, 4, 12),
    "Furniture": (79, 1299, 4, 9),
    "Appliances": (39, 899, 4, 8),
    "Software": (19, 499, 6, 7),
    "Storage": (15, 249, 8, 10),
    "Accessories": (9, 149, 10, 16),
    "Office Supplies": (2, 49, 25, 20),
    "Paper": (4, 39, 30, 18),
}
REGIONS = ["South", "West", "North", "East"]
REGION_WEIGHTS = [31, 26, 23, 20]
# monthly order volume: steady year, holiday peak
MONTH_WEIGHTS = [0.80, 0.75, 0.90, 0.90, 1.00, 0.95, 0.90, 1.00, 0.95, 1.05, 1.35, 1.55]
JUNK_DATES = ["TBD", "unknown", "2025-02-30", "00/00/0000", "2025-13-01"]

rng = random.Random(SEED)
customers = [f"C{n}" for n in range(1001, 1801)]


def random_day():
    month = rng.choices(range(1, 13), weights=MONTH_WEIGHTS)[0]
    first = date(2025, month, 1)
    nxt = date(2026, 1, 1) if month == 12 else date(2025, month + 1, 1)
    return first + timedelta(days=rng.randrange((nxt - first).days))


def price_for(low, high):
    # skewed toward the cheap end of the range, ending in .99 or .00
    p = low + (high - low) * rng.random() ** 2.2
    return round(p) - 0.01 if rng.random() < 0.7 else float(round(p))


def money(p):
    return f"-${abs(p):,.2f}" if p < 0 else f"${p:,.2f}"


base = []
for _ in range(TOTAL_ROWS - DUPLICATES):
    cat = rng.choices(list(CATEGORIES), weights=[v[3] for v in CATEGORIES.values()])[0]
    low, high, max_qty, _w = CATEGORIES[cat]
    base.append({
        "day": random_day(),
        "cat": cat,
        "region": rng.choices(REGIONS, weights=REGION_WEIGHTS)[0],
        "price": price_for(low, high),
        "qty": min(max_qty, max(1, int(rng.expovariate(1 / (max_qty / 3))) + 1)),
        "cust": rng.choice(customers),
    })
base.sort(key=lambda r: r["day"])

rows = []
for i, r in enumerate(base):
    messy_ok = i >= CLEAN_HEAD
    roll = rng.random
    d = r["day"]
    order_date = d.isoformat()
    if messy_ok:
        x = roll()
        if x < 0.005:
            order_date = d.strftime("%m/%d/%Y")
        elif x < 0.010:
            order_date = f"{d.strftime('%B')} {d.day} {d.year}"
        elif x < 0.015:
            order_date = rng.choice(JUNK_DATES)
        elif x < 0.020:
            order_date = ""
    price = r["price"]
    if messy_ok and roll() < 0.02:
        price = -price  # return / refund
    qty = str(r["qty"])
    if messy_ok:
        x = roll()
        if x < 0.02:
            qty = ""
        elif x < 0.025:
            qty = "0"
    rows.append({
        "Order ID": f"ORD-{10001 + i}" if not (messy_ok and roll() < 0.005) else "",
        "Order Date": order_date,
        "Product Category": r["cat"],
        "Region": r["region"] if not (messy_ok and roll() < 0.02) else "",
        "Unit Price": money(price),
        "Quantity Sold": qty,
        "Customer ID": r["cust"] if not (messy_ok and roll() < 0.07) else "",
    })

# three 9999 placeholders on cheap, complete rows spread through the year
cheap = [i for i, r in enumerate(rows)
         if i >= CLEAN_HEAD and r["Product Category"] in ("Office Supplies", "Paper")
         and r["Order ID"] and r["Quantity Sold"] not in ("", "0")
         and not r["Unit Price"].startswith("-")]
for i in (cheap[len(cheap) // 5], cheap[len(cheap) // 2], cheap[4 * len(cheap) // 5]):
    rows[i]["Quantity Sold"] = "9999"

# exact duplicates, each placed right after its original (a double export)
for i in sorted(rng.sample(range(CLEAN_HEAD, len(rows)), DUPLICATES), reverse=True):
    rows.insert(i + 1, dict(rows[i]))

assert len(rows) == TOTAL_ROWS
with open(OUT, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
print(f"wrote {len(rows)} rows to {OUT}")
