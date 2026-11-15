"""Generate ism2411/assets/downloads/retail_sales.csv for Module 13.

Usage (from the parent repo root): python3 _make_retail_sales.py ism2411/assets/downloads/retail_sales.csv

Schema comes from the Module 13 reading, lecture and lab code:
order_date, customer_id, region, product, quantity, revenue -> (5000, 6).
Numbers are clean (Lab 13 expects float64/int64 and divides by quantity);
about 1% of region cells are blank (Lab 13 Exercise 6: "with possible nulls").
Seeded, so a rerun gives the same bytes.
"""

import csv
import random
import sys
from datetime import date, timedelta

ROWS = 5000
SEED = 2411
OUT = sys.argv[1]

# product: (unit price, typical max quantity per order)
PRODUCTS = {
    "Laptop": (899.99, 4),
    "Tablet": (429.00, 5),
    "Standing Desk": (349.00, 4),
    "Monitor": (229.99, 6),
    "Office Chair": (189.50, 6),
    "Printer": (149.99, 4),
    "External Drive": (89.99, 8),
    "Headphones": (79.99, 10),
    "Webcam": (59.99, 10),
    "Keyboard": (49.99, 12),
    "Desk Lamp": (34.95, 12),
    "Mouse": (24.99, 20),
    "Notebook Pack": (12.49, 30),
    "USB Cable": (9.99, 30),
    "Printer Paper": (7.49, 40),
}
# cheap items sell more often than expensive ones
PRODUCT_WEIGHTS = [4, 4, 3, 6, 5, 4, 7, 8, 7, 9, 8, 10, 9, 10, 8]
REGIONS = ["South", "West", "North", "East"]
REGION_WEIGHTS = [31, 26, 23, 20]
NULL_REGION_RATE = 0.01
BULK_RATE = 0.03

rng = random.Random(SEED)
customers = [f"C{n}" for n in range(1001, 1801)]  # 800 customers, repeat buyers
start = date(2025, 1, 1)

rows = []
for _ in range(ROWS):
    product = rng.choices(list(PRODUCTS), weights=PRODUCT_WEIGHTS)[0]
    price, max_qty = PRODUCTS[product]
    # most orders are small; a few are bulk (keeps the top-revenue rows distinct)
    if rng.random() < BULK_RATE:
        quantity = rng.randint(max_qty + 1, max_qty * 5)
    else:
        quantity = min(max_qty, max(1, int(rng.expovariate(1 / (max_qty / 3))) + 1))
    region = rng.choices(REGIONS, weights=REGION_WEIGHTS)[0]
    if rng.random() < NULL_REGION_RATE:
        region = ""
    rows.append({
        "order_date": start + timedelta(days=rng.randrange(365)),
        "customer_id": rng.choice(customers),
        "region": region,
        "product": product,
        "quantity": quantity,
        "revenue": f"{price * quantity:.2f}",
    })

rows.sort(key=lambda r: r["order_date"])
with open(OUT, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
    writer.writeheader()
    for r in rows:
        r["order_date"] = r["order_date"].isoformat()
        writer.writerow(r)
print(f"wrote {len(rows)} rows to {OUT}")
