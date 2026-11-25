# Case 3 — Operations: Which carrier deserves more volume?

| | |
| --- | --- |
| Released | Monday, March 29, 2027 (Week 11) |
| Due | Sunday, April 11, 2027, 11:59 p.m. Eastern Time |
| Weight | 6.25% of the course grade |
| Work | Individual. Generative AI is required, using CRIT. |

## The business situation

Mangrove Outfitters (fictional) ships online orders from two warehouses, Tampa DC and Jacksonville DC, using two carriers: Coastal Parcel and SwiftShip (both fictional). Both carrier contracts are up for renewal, and Mangrove can shift volume between them.

The Director of Fulfillment has heard two claims from the team: "Coastal Parcel is on time more often" and "SwiftShip is much more expensive." Before shifting any volume, the Director wants evidence.

## Your question

**Should Mangrove move more shipping volume to one carrier? If so, which shipments should move, and why?**

## Constraints

- Mangrove promises delivery within **2 days for Local** orders and **5 days for Long-haul** orders. These promises are in `promised_days`.
- A shipment is **on time** when `transit_days` is less than or equal to `promised_days`.
- Measure performance **per shipment**. Some orders ship in more than one box, and each box is a shipment.
- Cancelled orders never ship.
- Mangrove will accept a somewhat higher cost per shipment for meaningfully better on-time performance. You decide what "meaningfully" means, and you must justify it.

## Data

The starter notebook loads these files from the course repository; there is nothing to download or upload.

Two files, July–December 2026. You need both to answer the question.

`orders.csv`, one row per order:

| Column | Meaning |
| --- | --- |
| order_id | Order ID |
| order_date | Date the order was placed, YYYY-MM-DD |
| warehouse | Warehouse that fulfilled the order |
| destination_zone | "Local" or "Long-haul" |
| promised_days | Delivery promise for the order, in days |
| order_value | Order value, US dollars |
| order_status | "Shipped" or "Cancelled" |

`shipments.csv`, one row per shipment (box):

| Column | Meaning |
| --- | --- |
| shipment_id | Shipment ID |
| order_id | Order the shipment belongs to |
| carrier | Carrier that delivered the shipment |
| ship_date | Date the shipment left the warehouse, YYYY-MM-DD |
| transit_days | Days from ship date to delivery |
| shipping_cost | What Mangrove paid for the shipment, US dollars |

## What to submit

1. **Open and save.** Open the [starter notebook in Colab](https://colab.research.google.com/github/markumreed/ism_courses/blob/sp27/ism2411_sp27/cases/case3_operations/starter.ipynb). Right away, choose **File → Save a copy in GitHub** and save it as `case3_operations/analysis.ipynb` in your `ism2411` repository.
2. **Complete all eight sections of the notebook:**
   1. Question and measures
   2. Data inspection, including the *What looks wrong* notes
   3. Cleaning decisions, with a table of each step's rows before and after
   4. Comparisons and charts (at least two charts)
   5. Verification
   6. Recommendation and limitations
   7. The verification checklist
   8. The AI decision record (about 200–300 words)

   Your cleaning table must reconcile the row counts before and after the join.
3. **README.** On GitHub, create `case3_operations/README.md` from the [README template](../templates/README_template.md); the technical guide, section 11, gives the steps.
4. **Submit in Canvas** the GitHub **permalink** to your notebook: open `analysis.ipynb` on GitHub and select **⋯ → Copy permalink**. Create the README first, because the permalink pins your repository as it is at that moment.

## Technical help for this case

Read the [technical guide](../templates/TECHNICAL_GUIDE.md) first. Patterns this case uses:

```python
orders = pd.read_csv(f"{DATA}/orders.csv")
ships = pd.read_csv(f"{DATA}/shipments.csv")

# join, and label where each row came from
merged = orders.merge(ships, on="order_id", how="outer", indicator=True)
merged["_merge"].value_counts()          # both / left_only / right_only

# compare the row counts before and after
len(orders), len(ships), len(merged)

# a True/False column; the mean of True/False is a share
matched = merged[merged["_merge"] == "both"].copy()
matched["on_time"] = matched["transit_days"] <= matched["promised_days"]

# group by two columns
matched.groupby(["carrier", "destination_zone"]).agg(
    shipments=("shipment_id", "count"),
    on_time_rate=("on_time", "mean"),
    avg_cost=("shipping_cost", "mean"),
)
```

`how=` decides which rows survive a join: `"inner"` keeps matches only, `"left"` keeps every order, `"outer"` keeps everything. Know which one you used and why.

**CRIT starter (adapt it):**

> **Context:** I am an operations analyst at Mangrove Outfitters. We ship online orders from two warehouses with two carriers and are renewing both contracts. Orders have these columns: [paste], and shipments have these: [paste]. On time means transit_days ≤ promised_days, measured per shipment. I need a recommendation on whether to shift volume between carriers.
> **Role:** Act as a logistics manager who negotiates carrier contracts.
> **Interview:** Before writing code, ask me up to five questions, one at a time.
> **Task:** [your specific request]

**Questions to keep asking:**

- *Frame the question:* "More volume" for which shipments? Is one answer right for every shipment?
- *Choose meaningful comparisons:* Do the two carriers handle the same mix of shipments? If not, is comparing their overall averages fair?
- *Check the evidence:* After the join, can you account for every order and every shipment, including the ones that did not match?
- *Explain the decision:* What would you tell the Director if both claims they heard turned out to be technically true?

## How it is graded

| Criterion | Weight |
| --- | --- |
| Question and measures | 15% |
| Data preparation | 20% |
| Comparisons and charts | 20% |
| Verification | 25% |
| Recommendation and decision record | 20% |

Late work receives a 25% grade reduction (25% of the possible points) for each calendar day it is late, subject to approved accommodations.
