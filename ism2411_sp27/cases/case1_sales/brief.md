# Case 1 — Sales: Which category earns its floor space?

| | |
| --- | --- |
| Released | Monday, February 22, 2027 (Week 7) |
| Checkpoint | Sunday, February 28, 2027, 11:59 p.m. Eastern Time (ungraded): sections 1 and 2 saved to GitHub |
| Due | Sunday, March 7, 2027, 11:59 p.m. Eastern Time |
| Weight | 6.25% of the course grade |
| Work | Individual. Generative AI is required, using CRIT. |

## The business situation

Mangrove Outfitters is a fictional Florida outdoor-gear retailer with six stores and an online shop. Every store uses the same floor plan. This spring, leadership will reset the floor plan: one product category will lose floor space, and another will gain it.

The Vice President of Store Operations has asked you for a recommendation. In the VP's words: "I need to know how much profit each category's floor space actually produces. Revenue alone won't convince the leadership team."

## Your question

**Using 2026 transactions, which product category should lose floor space in the spring reset, and which should gain it? Recommend one of each.**

Everyone answers this same question with the same data.

## Constraints

- The decision affects the **physical stores only**.
- Every store gives each category the same floor space:

| Category | Square feet per store |
| --- | --- |
| Camping | 450 |
| Hiking Apparel | 400 |
| Footwear | 300 |
| Water Sports | 300 |
| Fishing | 200 |
| Electronics | 150 |
| Accessories | 100 |

The same figures as a Python dictionary:

```python
floor_sqft = {"Camping": 450, "Hiking Apparel": 400, "Footwear": 300, "Water Sports": 300,
              "Fishing": 200, "Electronics": 150, "Accessories": 100}
```

- Use only the data provided. `unit_cost` is what Mangrove pays its supplier for one unit.
- Your recommendation must be one the VP could act on next month.

## Data

The starter notebook loads these files from the course repository; there is nothing to download or upload.

File: `sales_transactions.csv`, one row per transaction line, calendar year 2026.

| Column | Meaning |
| --- | --- |
| transaction_id | ID of the transaction line |
| order_date | Date of the sale, YYYY-MM-DD |
| channel | "In-store" or "Online" |
| store | Store name for in-store sales; blank for online sales |
| category | Product category |
| product | Product name |
| quantity | Units on the line; negative values are returns |
| unit_price | Selling price per unit, US dollars |
| unit_cost | Mangrove's cost per unit, US dollars |

## What to submit

1. **Open and save.** Open the [starter notebook in Colab](https://colab.research.google.com/github/markumreed/ism_courses/blob/sp27/ism2411_sp27/cases/case1_sales/starter.ipynb). Right away, choose **File → Save a copy in GitHub** and save it as `case1_sales/analysis.ipynb` in your `ism2411` repository.
2. **Checkpoint (ungraded), Sunday, February 28, 11:59 p.m. Eastern Time.** Finish sections 1 and 2, including the *What looks wrong* notes, save to GitHub, and submit the notebook's GitHub URL in Canvas. A TA replies with feedback, so you find out early whether you are on track.
3. **Complete all eight sections of the notebook:**
   1. Question and measures
   2. Data inspection, including the *What looks wrong* notes
   3. Cleaning decisions, with a table of each step's rows before and after
   4. Comparisons and charts (at least two charts)
   5. Verification
   6. Recommendation and limitations
   7. The verification checklist
   8. The AI decision record (about 200–300 words)
4. **README.** On GitHub, create `case1_sales/README.md` from the [README template](../templates/README_template.md); the technical guide, section 11, gives the steps.
5. **Submit in Canvas** the GitHub **permalink** to your notebook: open `analysis.ipynb` on GitHub and select **⋯ → Copy permalink**. Create the README first, because the permalink pins your repository as it is at that moment.

## Technical help for this case

Read the [technical guide](../templates/TECHNICAL_GUIDE.md) first. These patterns are the ones this case uses most:

```python
# a new column from two others
df["revenue"] = df["quantity"] * df["unit_price"]

# keep only some rows
in_store = df[df["channel"] == "In-store"]

# one row per category, with totals
summary = in_store.groupby("category")[["revenue"]].sum().reset_index()

# look up a value for each row from a dictionary
summary["sqft_per_store"] = summary["category"].map(floor_sqft)

# sort to see the order
summary.sort_values("revenue", ascending=False)
```

**A CRIT starter you can adapt.** It is a starting point, not a script.

> **Context:** I am an analyst at Mangrove Outfitters, a retailer with six stores and an online shop. Leadership will move floor space from one product category to another in every store. I have 2026 transaction data with these columns: [paste `df.info()`]. Here are five rows: [paste `df.head()`]. The decision covers physical stores only. Each category's floor space per store is [paste the table]. I need a recommendation supported by evidence about the profit each category's floor space produces.
> **Role:** Act as a retail merchandising analyst who reviews work before it reaches executives.
> **Interview:** Before you write any code, ask me up to five clarifying questions, one at a time.
> **Task:** [your specific request, for example a cleaning plan, or code for a summary table]

**Questions to keep asking, one for each habit:**

- *Frame the question:* What does "profit each category's floor space produces" mean as a number? What are its units?
- *Choose meaningful comparisons:* Which rows belong in a decision about store floor space? Does your denominator match that decision?
- *Check the evidence:* After each cleaning step, do your row counts and totals change by the amount you expect?
- *Explain the decision:* Would the VP act on your top chart without asking you to redo it?

## How it is graded

| Criterion | Weight |
| --- | --- |
| Question and measures | 15% |
| Data preparation | 20% |
| Comparisons and charts | 20% |
| Verification | 25% |
| Recommendation and decision record | 20% |

Late work receives a 25% grade reduction (25% of the possible points) for each calendar day it is late, subject to approved accommodations.
