# ISM2411 Lab W10: Inventory List Manager

## YouTube Metadata

**Title:** Inventory List Manager — Lab Walkthrough | ISM2411 Lab 10
**Description:**
Walkthrough of ISM2411 Module 10 Lab. We build an inventory management tool using Python lists — indexing, slicing, appending, removing, and looping — that mirrors real operations tooling.

Course page: https://markumreed.github.io/ism2411/pages/week10_lab.html

**Chapters:**
0:00 — What we're building
0:45 — Building the inventory list and indexing
2:30 — Slicing, appending, and removing items
5:00 — Looping to generate a formatted report
7:00 — Finding low-stock items with a conditional loop
8:30 — Submission checklist

**Applies to:** ISM2411 Module 10

**Tags:** python lists, python inventory management, python list methods, python indexing slicing, ISM2411, USF, python list tutorial

---

## Script

### INTRO (0:00–0:45)

Lab 10 — Inventory List Manager. We're working with lists: the ordered, mutable collection that underlies every real data processing pipeline. By the end we'll have a working inventory tool that tracks products, quantities, and low-stock alerts.

---

### BUILDING THE INVENTORY (0:45–2:30)

Create `module10/inventory.py`:

```python
# inventory.py

products   = ["Laptop Bag", "Wireless Mouse", "USB Hub", "Monitor Stand", "Keyboard"]
quantities = [12, 45, 8, 3, 27]
prices     = [49.99, 29.99, 19.99, 34.99, 79.99]

# Indexing — zero-based
print(products[0])         # Laptop Bag
print(quantities[-1])      # 27 (last item)
print(prices[2])           # 19.99

# Verify alignment: products[i] goes with quantities[i]
print(f"{products[3]}: {quantities[3]} in stock at ${prices[3]:.2f}")
```

Lists are zero-indexed. The first element is `[0]`, the last is `[-1]`. Negative indices count from the end.

---

### SLICING, APPENDING, REMOVING (2:30–5:00)

```python
# Slicing — [start:stop] — stop is exclusive
first_three = products[:3]
print(first_three)   # ['Laptop Bag', 'Wireless Mouse', 'USB Hub']

last_two = products[-2:]
print(last_two)      # ['Monitor Stand', 'Keyboard']

# Appending — add to the end
products.append("Webcam")
quantities.append(15)
prices.append(89.99)
print(len(products))   # 6 — now six items

# Removing by value
products.remove("USB Hub")
# But we also need to remove the matching quantity and price at the same index
# Better: find the index first, then delete from all three lists
idx = products.index("Webcam")
products.pop(idx)
quantities.pop(idx)
prices.pop(idx)
```

The three parallel lists are a common beginner pattern. Later in the course (pandas) you'll manage this in a single DataFrame, but for now it builds the indexing intuition.

---

### FORMATTED REPORT (5:00–7:00)

```python
# Loop to generate a full inventory report
print(f"\n{'Product':<20} {'Qty':>6} {'Price':>8} {'Value':>10}")
print("-" * 48)

total_value = 0
for i in range(len(products)):
    value = quantities[i] * prices[i]
    total_value += value
    print(f"{products[i]:<20} {quantities[i]:>6} ${prices[i]:>7.2f} ${value:>9,.2f}")

print("-" * 48)
print(f"{'TOTAL':<20} {'':>6} {'':>8} ${total_value:>9,.2f}")
```

Column alignment with `<` (left-align) and `>` (right-align) in f-strings makes tabular output readable.

---

### LOW-STOCK ALERT (7:00–8:30)

```python
# Find items with quantity < 10
REORDER_THRESHOLD = 10
print("\n⚠ Low Stock Alert:")

for i in range(len(products)):
    if quantities[i] < REORDER_THRESHOLD:
        print(f"  Reorder: {products[i]} (only {quantities[i]} left)")
```

Output:
```
⚠ Low Stock Alert:
  Reorder: Laptop Bag (only 8 left)
  Reorder: Monitor Stand (only 3 left)
```

---

### SUBMISSION CHECKLIST (8:30–10:00)

- `inventory.py` with three parallel lists
- Indexing, slicing, append, remove all demonstrated
- Formatted report with column alignment
- Low-stock conditional loop working
- Exercise responses written
- Submitted to Canvas via GitHub URL
