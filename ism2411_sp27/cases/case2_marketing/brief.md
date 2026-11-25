# Case 2 — Marketing: Where should the summer budget go?

| | |
| --- | --- |
| Released | Monday, March 8, 2027 (Week 9) |
| Due | Sunday, March 28, 2027, 11:59 p.m. Eastern Time (after Spring Break) |
| Weight | 6.25% of the course grade |
| Work | Individual. Generative AI is required, using CRIT. |

## The business situation

Mangrove Outfitters (fictional) ran a 13-week spring campaign in 2026 to win new customers. It spent about $510,000 across five channels in four Florida regions. The summer campaign has the same total budget.

The Chief Marketing Officer wants to reallocate it. The CMO has heard three different claims: "Influencer brought in the most customers," "Social Ads had the best conversion rate," and "Email is too small to matter." The CMO wants an answer grounded in the spring results.

## Your question

**Based on spring 2026 results, which channels should get more of the summer budget, and which should get less? Recommend a direction (more, about the same, or less) for each channel.**

## Constraints

- The summer total equals the spring total.
- Email spend can grow by **at most 20%**, because the size of the email list limits it.
- The goal is new customers at a reasonable cost, whose first orders help pay back what was spent to win them.
- The weekly ad-platform exports were combined by hand. They are provided exactly as exported.

## Data

The starter notebook loads these files from the course repository; there is nothing to download or upload.

File: `campaign_weekly.csv`, one row per week × channel × region, weeks starting March 2 through May 25, 2026.

| Column | Meaning |
| --- | --- |
| week_start | Monday that starts the week, YYYY-MM-DD |
| channel | Marketing channel |
| region | Mangrove sales region |
| spend | Amount spent that week, US dollars |
| impressions | Number of times the ad or email was shown |
| clicks | Clicks through to Mangrove's site |
| new_customers | First-time customers credited to the channel |
| first_order_revenue | Revenue from those customers' first orders, US dollars |
| conversion_rate | new_customers divided by clicks for that row, as exported by the ad platform |

## What to submit

1. **Open and save.** Open the [starter notebook in Colab](https://colab.research.google.com/github/markumreed/ism_courses/blob/sp27/ism2411_sp27/cases/case2_marketing/starter.ipynb). Right away, choose **File → Save a copy in GitHub** and save it as `case2_marketing/analysis.ipynb` in your `ism2411` repository.
2. **Complete all eight sections of the notebook:**
   1. Question and measures
   2. Data inspection, including the *What looks wrong* notes
   3. Cleaning decisions, with a table of each step's rows before and after
   4. Comparisons and charts (at least two charts)
   5. Verification
   6. Recommendation and limitations
   7. The verification checklist
   8. The AI decision record (about 200–300 words)
3. **README.** On GitHub, create `case2_marketing/README.md` from the [README template](../templates/README_template.md); the technical guide, section 11, gives the steps.
4. **Submit in Canvas** the GitHub **permalink** to your notebook: open `analysis.ipynb` on GitHub and select **⋯ → Copy permalink**. Create the README first, because the permalink pins your repository as it is at that moment.

## Technical help for this case

Read the [technical guide](../templates/TECHNICAL_GUIDE.md) first. Patterns this case uses:

```python
# several totals per group at once
by_channel = df.groupby("channel").agg(
    spend=("spend", "sum"),
    customers=("new_customers", "sum"),
    revenue=("first_order_revenue", "sum"),
).reset_index()

# a rate computed from the group totals
by_channel["spend_per_customer"] = by_channel["spend"] / by_channel["customers"]

# two grouping columns
by_channel_region = df.groupby(["channel", "region"])[["spend", "new_customers"]].sum()

# a bar chart with a clear title and no error bars
ax = sns.barplot(data=by_channel, x="channel", y="spend_per_customer", errorbar=None)
ax.set_title("…a title that states the finding…")
ax.set_ylabel("Spend per new customer (US dollars)")
```

**CRIT starter (adapt it):**

> **Context:** I am a marketing analyst at Mangrove Outfitters. We spent about $510,000 on a 13-week spring campaign across five channels and four regions, and summer has the same budget. Email can grow at most 20%. My data has these columns: [paste `df.info()`] and these rows: [paste `df.head()`]. I need a recommendation for each channel: more, about the same, or less.
> **Role:** Act as a performance-marketing manager who has to defend the budget to a CFO.
> **Interview:** Before writing code, ask me up to five questions, one at a time.
> **Task:** [your specific request]

**Questions to keep asking:**

- *Frame the question:* What does one dollar of spend buy in each channel? Which measure would the CFO accept?
- *Choose meaningful comparisons:* A total and a rate can tell different stories. Which one matches a budget decision? Is a column of per-row rates safe to average?
- *Check the evidence:* Do your corrected spend totals match the size of the campaign described above? Are any values impossible?
- *Explain the decision:* Does each channel's recommendation follow from a number on your chart?

## How it is graded

| Criterion | Weight |
| --- | --- |
| Question and measures | 15% |
| Data preparation | 20% |
| Comparisons and charts | 20% |
| Verification | 25% |
| Recommendation and decision record | 20% |

Late work receives a 25% grade reduction (25% of the possible points) for each calendar day it is late, subject to approved accommodations.
