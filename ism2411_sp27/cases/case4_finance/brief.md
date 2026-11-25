# Case 4 — Finance: What is driving expense growth?

| | |
| --- | --- |
| Released | Monday, April 12, 2027 (Week 13) |
| Due | Sunday, April 25, 2027, 11:59 p.m. Eastern Time |
| Weight | 6.25% of the course grade |
| Work | Individual. Generative AI is required, using CRIT. |

## The business situation

Mangrove Outfitters' (fictional) operating expenses rose in 2026. The Chief Financial Officer is planning actions for the second quarter of 2027 and needs to separate three kinds of increase:

- **One-time** increases that will not repeat.
- **Seasonal** increases that come back every year at the same time.
- **Ongoing** increases that will keep growing unless someone acts.

The CFO also wants to know whether any department is running over its approved budget in a way that needs action now.

## Your question

**What drove the increase in operating expense from 2025 to 2026, and which department, if any, needs action before Q2 2027?**

## Constraints

- Use `posted_date` for timing.
- `budget_2026.csv` is the approved 2026 budget, by department and month.
- Operating expense in this case excludes the cost of goods sold and advertising spend.
- Vendor credits and refunds are recorded as negative amounts.
- Compare like periods: a month is not directly comparable to a different month of the year in a seasonal business.

## Data

The starter notebook loads these files from the course repository; there is nothing to download or upload.

`expenses.csv`, one row per posted expense line, January 2025 – December 2026:

| Column | Meaning |
| --- | --- |
| expense_id | Expense line ID |
| posted_date | Date the expense was posted |
| department | Department charged |
| category | Expense category |
| vendor | Vendor paid |
| amount | Amount, US dollars; negative values are credits |

`budget_2026.csv`, one row per department per month of 2026:

| Column | Meaning |
| --- | --- |
| month | Budget month, YYYY-MM |
| department | Department |
| budget | Approved budget for that department and month, US dollars |

## What to submit

1. **Open and save.** Open the [starter notebook in Colab](https://colab.research.google.com/github/markumreed/ism_courses/blob/sp27/ism2411_sp27/cases/case4_finance/starter.ipynb). Right away, choose **File → Save a copy in GitHub** and save it as `case4_finance/analysis.ipynb` in your `ism2411` repository.
2. **Complete all eight sections of the notebook:**
   1. Question and measures
   2. Data inspection, including the *What looks wrong* notes
   3. Cleaning decisions, with a table of each step's rows before and after
   4. Comparisons and charts (at least two charts)
   5. Verification
   6. Recommendation and limitations
   7. The verification checklist
   8. The AI decision record (about 200–300 words)

   At least one chart must show a monthly trend.
3. **README.** On GitHub, create `case4_finance/README.md` from the [README template](../templates/README_template.md); the technical guide, section 11, gives the steps.
4. **Submit in Canvas** the GitHub **permalink** to your notebook: open `analysis.ipynb` on GitHub and select **⋯ → Copy permalink**. Create the README first, because the permalink pins your repository as it is at that moment.

## Technical help for this case

Read the [technical guide](../templates/TECHNICAL_GUIDE.md) first. Patterns this case uses:

```python
# turn text into real dates, then check that none failed
df["date"] = pd.to_datetime(df["posted_date"], errors="coerce")
df["date"].isna().sum()

# year and month from a date
df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.to_period("M").astype(str)     # "2026-03"

# monthly totals by department
monthly = df.groupby(["month", "department"])["amount"].sum().reset_index()

# line chart of a trend
ax = sns.lineplot(data=monthly, x="month", y="amount", hue="department", errorbar=None)
plt.xticks(rotation=90)

# attach the budget to the actuals (both have month and department)
vs_budget = monthly.merge(budget, on=["month", "department"], how="left")
vs_budget["variance"] = vs_budget["amount"] - vs_budget["budget"]

# a wide table: one row per category, one column per year
df.pivot_table(index=["department", "category"], columns="year", values="amount", aggfunc="sum")
```

If `pd.to_datetime` returns missing dates (`NaT`), find out which rows failed and why before you continue. Never silently drop rows.

**CRIT starter (adapt it):**

> **Context:** I am a financial analyst at Mangrove Outfitters. Operating expenses rose from 2025 to 2026, and the CFO needs to separate one-time, seasonal, and ongoing increases and check departments against the 2026 budget. Expenses have these columns: [paste]; the budget has these: [paste].
> **Role:** Act as an FP&A manager preparing a briefing for a CFO.
> **Interview:** Before writing code, ask me up to five questions, one at a time.
> **Task:** [your specific request]

**Questions to keep asking:**

- *Frame the question:* What will the CFO do differently for a one-time, a seasonal, and an ongoing increase?
- *Choose meaningful comparisons:* Which periods are fair to compare in a seasonal business? Against what should a large increase be judged?
- *Check the evidence:* Does every row get a valid date? Do your yearly totals stay the same no matter how you group them?
- *Explain the decision:* Which single chart would convince the CFO to act, or not to act?

## How it is graded

| Criterion | Weight |
| --- | --- |
| Question and measures | 15% |
| Data preparation | 20% |
| Comparisons and charts | 20% |
| Verification | 25% |
| Recommendation and decision record | 20% |

Late work receives a 25% grade reduction (25% of the possible points) for each calendar day it is late, subject to approved accommodations.
