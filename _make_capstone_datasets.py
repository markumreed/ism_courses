"""Generate the eight ISM2411 capstone datasets, one per business field.

Usage (from the parent repo root):
    python3 _make_capstone_datasets.py ism2411/assets/downloads/capstone

Every file is fictional, 5,000 rows, 2025 dates (HR: hire dates 2016-2025), and
messy in the SAME ways, so every choice is graded on the same rubric:
  1. headers have spaces and capitals ("Order Date")
  2. the date column: ~1.5% typed another way (03/14/2025, "March 14 2025") or junk
     ("TBD", "2025-02-30"), ~0.5% blank. The first 40 rows are clean, because
     pd.to_datetime guesses ONE format from the first value and coerces the rest.
  3. money is text: "$1,234.56", negatives "-$45.00"
  4. negative money that means something (returns, credits, losses, refunds)
  5. typos in one category column: lowercase, UPPERCASE, stray spaces, and two
     misspellings that .str.strip().str.title() alone does not fix
  6. blanks in one category column (~2.5%) and one number column (~2%)
  7. zeros (~0.5%) and three 9999 placeholders in one count column
  8. 40 exact duplicate rows, each right after its original
Each generator also plants a few real patterns, so good questions find real answers.
Seeded, so a rerun gives the same bytes.
"""

import csv
import math
import random
import sys
from datetime import date, timedelta
from pathlib import Path

ROWS = 5000
DUPLICATES = 40
PLACEHOLDERS = 3
CLEAN_HEAD = 40
JUNK_DATES = ["TBD", "unknown", "2025-02-30", "00/00/0000", "2025-13-01", "pending"]
HOLIDAY = [0.85, 0.80, 0.95, 0.95, 1.00, 0.95, 0.95, 1.00, 0.95, 1.05, 1.40, 1.55]


# ── helpers ───────────────────────────────────────────────────
def pick(rng, weights):
    keys = list(weights)
    return rng.choices(keys, weights=[weights[k] for k in keys])[0]


def day_in(rng, month_weights, year=2025):
    month = rng.choices(range(1, 13), weights=month_weights)[0]
    start = date(year, month, 1)
    end = date(year + 1, 1, 1) if month == 12 else date(year, month + 1, 1)
    return start + timedelta(days=rng.randrange((end - start).days))


def skewed(rng, low, high, power=2.2):
    """A value in [low, high], bunched toward low (most prices are cheap)."""
    return low + (high - low) * rng.random() ** power


def price(rng, low, high):
    p = skewed(rng, low, high)
    return round(p) - 0.01 if rng.random() < 0.7 else float(round(p))


def money(x):
    return f"-${abs(x):,.2f}" if x < 0 else f"${x:,.2f}"


def clip(x, low, high):
    return max(low, min(high, x))


# ── 1. Retail (matches the capstone page, video and code skeleton) ─────
RETAIL_CATS = {  # low, high, max qty, weight
    "Electronics": (60, 1400, 3, 14), "Furniture": (80, 1100, 3, 11),
    "Appliances": (40, 900, 3, 9), "Office Supplies": (3, 45, 20, 18),
    "Clothing": (12, 120, 5, 16), "Sporting Goods": (15, 400, 4, 10),
    "Home Decor": (10, 250, 5, 12), "Toys": (8, 90, 6, 10),
}


def retail(rng):
    region = pick(rng, {"South": 31, "West": 24, "North": 24, "East": 21})
    weights = {c: v[3] * (2.6 if region == "West" and c == "Electronics" else 1)
               for c, v in RETAIL_CATS.items()}
    cat = pick(rng, weights)
    low, high, max_qty, _ = RETAIL_CATS[cat]
    segment = pick(rng, {"Consumer": 55, "Corporate": 30, "Home Office": 15})
    qty = min(max_qty, max(1, int(rng.expovariate(3 / max_qty)) + 1))
    if segment == "Corporate":
        qty *= rng.choice([1, 2, 2, 3])
    unit = price(rng, low, high)
    if rng.random() < (0.09 if cat == "Furniture" else 0.02):  # return
        unit, qty = -unit, rng.choice([1, 1, 2])
    return {"Order Date": day_in(rng, HOLIDAY), "Product Category": cat, "Region": region,
            "Unit Price": unit, "Quantity Sold": qty, "Customer Segment": segment}


# ── 2. Marketing ──────────────────────────────────────────────
CHANNELS = {  # weight, spend low/high, impressions per $, CTR, conversion rate, avg order $
    # return on ad spend ≈ impressions/$ × CTR × conversion × order $ (× campaign mix ≈ 1.2):
    # Email ~10x, Paid Search ~4x, Social ~2x, Display ~1x, Influencer and Television < 1x
    "Email": (18, 200, 1500, 50, 0.035, 0.060, 85),
    "Paid Search": (22, 800, 5000, 24, 0.040, 0.040, 95),
    "Social Media": (22, 500, 4000, 85, 0.012, 0.025, 70),
    "Display": (14, 400, 3000, 230, 0.0025, 0.020, 75),
    "Influencer": (12, 2000, 12000, 55, 0.010, 0.012, 80),
    "Television": (12, 8000, 40000, 280, 0.0005, 0.030, 110),
}
CAMPAIGN = {"Awareness": (0.5, 1.0), "Promotion": (1.4, 0.8),
            "Retargeting": (2.0, 1.0), "Product Launch": (1.0, 1.3)}


def marketing(rng):
    channel = pick(rng, {c: v[0] for c, v in CHANNELS.items()})
    _, lo, hi, per_dollar, ctr, cvr, aov = CHANNELS[channel]
    ctype = pick(rng, {"Awareness": 25, "Promotion": 30, "Retargeting": 20, "Product Launch": 25})
    cvr_mult, aov_mult = CAMPAIGN[ctype]
    day = day_in(rng, HOLIDAY)
    season = 1.5 if day.month == 11 else 1.3 if day.month == 12 else 1.0
    spend = round(skewed(rng, lo, hi, 1.6) * season, 2)
    impressions = int(spend * per_dollar * rng.uniform(0.7, 1.3))
    clicks = int(impressions * ctr * rng.uniform(0.6, 1.4))
    conversions = int(clicks * cvr * cvr_mult * rng.uniform(0.6, 1.4))
    revenue = round(conversions * aov * aov_mult * rng.uniform(0.8, 1.2), 2)
    if rng.random() < (0.05 if ctype == "Promotion" else 0.01):  # refunds beat new sales
        revenue = -round(rng.uniform(150, 3000), 2)
    return {"Date": day, "Channel": channel, "Campaign Type": ctype,
            "Region": pick(rng, {"Southeast": 26, "Northeast": 22, "Midwest": 20, "Southwest": 16, "West": 16}),
            "Spend": spend, "Impressions": impressions, "Clicks": clicks,
            "Conversions": conversions, "Revenue": revenue}


# ── 3. Accounting ─────────────────────────────────────────────
EXPENSES = {  # low, high, vendors
    "Travel": (150, 4500, ["Suncoast Travel Group", "Skyway Air Partners"]),
    "Software": (50, 25000, ["Cobalt Software Co", "Ledgerly Cloud"]),
    "Office Supplies": (20, 800, ["Harbor Point Supply", "Keystone Print Shop"]),
    "Utilities": (300, 6000, ["Pelican Utilities", "Bayside Telecom"]),
    "Consulting": (2000, 40000, ["Northgate Consulting", "Meridian Advisory"]),
    "Marketing": (500, 15000, ["Lighthouse Media", "Palm Street Creative"]),
    "Equipment": (300, 20000, ["Redfern Equipment", "Ironwood Machinery"]),
    "Meals": (25, 1200, ["Mangrove Catering", "Ybor Deli Co"]),
}
DEPT_MIX = {  # department: (weight, favorite categories)
    "Sales": (22, ["Travel", "Meals", "Travel"]),
    "Operations": (20, ["Equipment", "Utilities", "Office Supplies"]),
    "Information Technology": (16, ["Software", "Equipment", "Software"]),
    "Human Resources": (10, ["Consulting", "Office Supplies", "Meals"]),
    "Finance": (12, ["Consulting", "Software", "Office Supplies"]),
    "Marketing": (20, ["Marketing", "Travel", "Marketing"]),
}
TERMS = {"Suncoast Travel Group": 15, "Skyway Air Partners": 30, "Cobalt Software Co": 30,
         "Ledgerly Cloud": 30, "Harbor Point Supply": 30, "Keystone Print Shop": 15,
         "Pelican Utilities": 15, "Bayside Telecom": 30, "Northgate Consulting": 60,
         "Meridian Advisory": 60, "Lighthouse Media": 30, "Palm Street Creative": 30,
         "Redfern Equipment": 60, "Ironwood Machinery": 60, "Mangrove Catering": 15,
         "Ybor Deli Co": 15}
ACCT_MONTHS = [1.25, 1.05, 1.10, 0.95, 0.90, 0.95, 0.85, 0.90, 1.00, 1.05, 1.05, 1.45]


def accounting(rng):
    dept = pick(rng, {d: v[0] for d, v in DEPT_MIX.items()})
    day = day_in(rng, ACCT_MONTHS)
    if rng.random() < 0.55:
        cat = rng.choice(DEPT_MIX[dept][1])
    else:
        cat = rng.choice(list(EXPENSES))
    if dept == "Sales" and day.month in (2, 3, 10) and rng.random() < 0.4:
        cat = "Travel"  # conference season
    low, high, vendors = EXPENSES[cat]
    vendor = rng.choice(vendors)
    amount = round(skewed(rng, low, high, 2.5), 2)
    if cat == "Software" and day.month == 1:
        amount = round(amount * 2.5, 2)  # annual renewals
    if day.month == 12:
        amount = round(amount * 1.2, 2)  # use-it-or-lose-it budgets
    if rng.random() < (0.06 if cat in ("Equipment", "Travel") else 0.015):
        amount = -round(amount * rng.uniform(0.1, 0.6), 2)  # credit memo
    terms = TERMS[vendor]
    days = terms + int(rng.gauss(-3, 5))
    if vendor == "Suncoast Travel Group" and rng.random() < 0.45:
        days = terms + rng.randint(10, 40)
    elif terms == 15 and rng.random() < 0.25:
        days = terms + rng.randint(3, 20)
    if day.month == 12:
        days += rng.randint(3, 12)
    return {"Invoice Date": day, "Vendor": vendor, "Expense Category": cat, "Department": dept,
            "Amount": amount, "Payment Terms": f"Net {terms}", "Days To Pay": max(1, days)}


# ── 4. Finance ────────────────────────────────────────────────
INDUSTRY = {  # weight, base default rate, rate premium
    "Restaurants": (14, 0.20, 1.50), "Retail": (16, 0.12, 0.75),
    "Construction": (13, 0.13, 1.00), "Transportation": (11, 0.11, 0.75),
    "Agriculture": (8, 0.10, 0.50), "Technology": (12, 0.08, 0.50),
    "Professional Services": (14, 0.05, 0.00), "Healthcare": (12, 0.04, 0.00),
}
LOAN_MONTHS = [0.9, 1.0, 1.45, 1.1, 1.0, 0.9, 0.85, 0.9, 1.25, 1.0, 0.9, 0.75]


def finance(rng):
    industry = pick(rng, {k: v[0] for k, v in INDUSTRY.items()})
    _, base_default, premium = INDUSTRY[industry]
    score = int(clip(rng.gauss(690, 55), 520, 830))
    risk = 2.6 if score < 620 else 1.3 if score < 680 else 0.75 if score < 740 else 0.35
    amount = round(clip(math.exp(rng.gauss(math.log(75000), 0.8)), 10000, 500000) / 500) * 500
    term = rng.choice([12, 24, 36]) if amount < 60000 else rng.choice([36, 60, 84])
    rate = round((6.5 + max(0, 760 - score) * 0.04 + premium + rng.uniform(-0.5, 0.5)) * 4) / 4
    employees = max(1, int(math.exp(rng.gauss(math.log(12), 1.0))))
    if rng.random() < base_default * risk:
        status = "Default"
        profit = -round(amount * rng.uniform(0.3, 0.8), 2)
    else:
        status = pick(rng, {"Current": 60, "Paid Off": 32 if term <= 24 else 8, "Late": 7})
        profit = round(amount * rate / 100 * min(term, 12) / 12 * rng.uniform(0.45, 0.7), 2)
    return {"Application Date": day_in(rng, LOAN_MONTHS), "Industry": industry,
            "Region": pick(rng, {"Tampa Bay": 30, "Central Florida": 26, "South Florida": 28, "North Florida": 16}),
            "Loan Amount": float(amount), "Interest Rate": f"{rate:.2f}", "Term Months": term,
            "Credit Score": score, "Employees": employees, "Loan Status": status, "Profit": profit}


# ── 5. Management / HR ────────────────────────────────────────
DEPTS = {"Sales": (18, 1.05), "Customer Support": (22, 0.80), "Operations": (18, 0.95),
         "Engineering": (14, 1.35), "Finance": (8, 1.15), "Marketing": (10, 1.05),
         "Human Resources": (6, 1.00)}
LEVELS = {"Entry": (34, 48000), "Associate": (28, 62000), "Senior": (20, 82000),
          "Manager": (13, 105000), "Director": (5, 145000)}
LOCATIONS = {"Tampa": (34, 1.00), "Orlando": (22, 0.97), "Miami": (20, 1.08), "Remote": (24, 1.02)}
HIRE_MONTHS = [1.4, 1.0, 0.9, 0.9, 1.0, 1.3, 1.3, 1.2, 1.0, 0.8, 0.7, 0.5]


def hr(rng):
    year = rng.choices(range(2016, 2026), weights=[3, 4, 5, 5, 4, 7, 9, 11, 13, 15])[0]
    hired = day_in(rng, HIRE_MONTHS, year)
    dept = pick(rng, {k: v[0] for k, v in DEPTS.items()})
    level = pick(rng, {k: v[0] for k, v in LEVELS.items()})
    if dept == "Customer Support" and level in ("Senior", "Director"):
        level = "Associate"
    location = pick(rng, {k: v[0] for k, v in LOCATIONS.items()})
    band = rng.random()  # where this person sits in the pay band
    salary = round(LEVELS[level][1] * DEPTS[dept][1] * LOCATIONS[location][1] * (0.85 + 0.3 * band), -2)
    training = 0 if rng.random() < 0.06 else int(clip(rng.expovariate(1 / 24), 1, 120))
    rating = int(clip(round(rng.gauss(3.4, 0.9)), 1, 5))
    if hired >= date(2025, 7, 1) and rng.random() < 0.7:
        rating = None  # not rated yet
    p = 0.11
    p *= 2.3 if dept == "Customer Support" else 1.0
    p *= 1.5 if level == "Entry" else 0.7 if level in ("Manager", "Director") else 1.0
    p *= 1.9 if training < 10 else 0.8 if training > 40 else 1.0
    p *= 0.7 if location == "Remote" else 1.0
    p *= 1.5 if band < 0.3 else 1.0
    p *= {1: 2.0, 2: 1.6, 5: 0.6}.get(rating, 1.0)
    left = "Yes" if rng.random() < min(p, 0.85) else "No"
    raise_amt = round(salary * rng.uniform(0.02, 0.06), 2)
    if rng.random() < 0.08:
        raise_amt = 0.0
    if (dept == "Sales" and rng.random() < 0.09) or rng.random() < 0.01:
        raise_amt = -round(salary * rng.uniform(0.01, 0.05), 2)  # 2025 pay cut
    return {"Hire Date": hired, "Department": dept, "Job Level": level, "Location": location,
            "Annual Salary": salary, "Last Raise": raise_amt,
            "Performance Rating": "" if rating is None else rating,
            "Training Hours": training, "Left Company": left}


# ── 6. Information Systems: IT help desk ──────────────────────
IT_CATS = {  # weight, hours low/high, priority weights (Low, Medium, High, Critical)
    "Password Reset": (20, 0.3, 2, (70, 25, 5, 0)), "Software": (18, 1, 24, (30, 45, 20, 5)),
    "Hardware": (12, 3, 48, (25, 45, 25, 5)), "Network": (10, 1, 36, (10, 35, 35, 20)),
    "Email": (12, 0.5, 8, (40, 45, 12, 3)), "Security": (7, 4, 72, (5, 20, 45, 30)),
    "Printer": (9, 0.5, 10, (55, 35, 10, 0)), "Access Request": (12, 1, 12, (45, 45, 10, 0)),
}
SLA = {"Low": 72, "Medium": 24, "High": 8, "Critical": 4}
FEE = {"Low": 45, "Medium": 85, "High": 150, "Critical": 300}
WEEKDAY = [1.45, 1.15, 1.0, 1.0, 0.9, 0.35, 0.3]
STORM = (date(2025, 9, 25), date(2025, 10, 6))


def it_helpdesk(rng):
    storm = rng.random() < 0.06
    if storm:
        day = STORM[0] + timedelta(days=rng.randrange((STORM[1] - STORM[0]).days))
        cat = rng.choice(["Network", "Network", "Hardware"])
    else:
        while True:
            day = day_in(rng, [1.0] * 12)
            if rng.random() < WEEKDAY[day.weekday()] / 1.45:
                break
        cat = pick(rng, {k: v[0] for k, v in IT_CATS.items()})
    _, lo, hi, pw = IT_CATS[cat]
    priority = rng.choices(["Low", "Medium", "High", "Critical"], weights=pw)[0]
    channel = pick(rng, {"Phone": 30, "Email": 25, "Chat": 25, "Portal": 20})
    hours = skewed(rng, lo, hi, 1.8)
    hours *= 0.7 if channel == "Chat" else 1.0
    hours *= 1.8 if day.weekday() >= 5 else 1.0
    hours *= 2.0 if storm else 1.0
    hours = round(hours, 1)
    if hours > SLA[priority] and priority in ("High", "Critical"):
        billed = -round(FEE[priority] * rng.uniform(0.5, 1.0), 2)  # SLA credit
    else:
        billed = round(FEE[priority] + min(hours, 40) * 65 * rng.uniform(0.8, 1.1), 2)
    sat = clip(round(4.6 - max(0, hours - 4) * 0.05 + (0.3 if channel == "Chat" else 0) + rng.gauss(0, 0.6)), 1, 5)
    return {"Opened Date": day, "Category": cat, "Priority": priority, "Channel": channel,
            "Client Size": pick(rng, {"Small": 45, "Medium": 35, "Enterprise": 20}),
            "Resolution Hours": hours, "Billed Amount": billed,
            "Satisfaction": "" if rng.random() < 0.12 else int(sat)}


# ── 7. Supply chain: shipments ────────────────────────────────
CARRIERS = {  # weight, cost multiplier, late rate, money-back guarantee
    "Swift Line Freight": (28, 1.00, 0.12, True), "Coastal Express": (22, 1.35, 0.05, True),
    "Blue Route Logistics": (25, 0.95, 0.15, False), "Gulf Parcel": (25, 0.75, 0.32, False),
}
GOODS = {  # weight, units low/high, value per unit, freight per unit
    "Electronics": (16, 1, 60, 180, 1.8), "Apparel": (18, 5, 200, 22, 0.4),
    "Home Goods": (16, 2, 120, 45, 1.2), "Groceries": (20, 20, 500, 4, 0.3),
    "Health & Beauty": (15, 5, 250, 12, 0.25), "Auto Parts": (15, 1, 80, 65, 1.5),
}


def shipments(rng):
    day = day_in(rng, HOLIDAY)
    carrier = pick(rng, {k: v[0] for k, v in CARRIERS.items()})
    _, cost_mult, late_rate, guarantee = CARRIERS[carrier]
    goods = pick(rng, {k: v[0] for k, v in GOODS.items()})
    _, ulo, uhi, value, per_unit = GOODS[goods]
    warehouse = pick(rng, {"Tampa": 30, "Atlanta": 25, "Dallas": 25, "Charlotte": 20})
    units = int(skewed(rng, ulo, uhi, 1.8))
    promised = rng.choice([2, 3, 3, 5])
    late_p = late_rate * (1.6 if day.month in (11, 12) else 1.0) * (1.4 if warehouse == "Dallas" else 1.0)
    late = rng.random() < late_p
    actual = promised + (rng.randint(1, 6) if late else -rng.choice([0, 0, 0, 1]))
    cost = round((25 + units * per_unit) * cost_mult * rng.uniform(0.85, 1.15), 2)
    if late and guarantee:
        cost = -cost  # refunded under the carrier's guarantee
    return {"Ship Date": day, "Warehouse": warehouse, "Carrier": carrier, "Product Category": goods,
            "Units": max(1, units), "Order Value": round(units * value * rng.uniform(0.9, 1.1), 2),
            "Freight Cost": cost, "Promised Days": promised, "Actual Days": max(1, actual)}


# ── 8. Sport & entertainment: arena ticket sales ───────────────
SEASON = {  # event: month weights
    "Hockey": [1.2, 1.2, 1.1, 0.8, 0, 0, 0, 0, 0.3, 1.2, 1.2, 1.3],
    "Basketball": [1.1, 1.1, 1.1, 0.6, 0, 0, 0, 0, 0, 0.4, 1.1, 1.2],
    "Concert": [0.5, 0.6, 0.8, 1.0, 1.2, 1.5, 1.6, 1.4, 1.0, 0.9, 0.7, 0.8],
    "Comedy": [0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6],
    "Family Show": [0.2, 0.3, 0.9, 0.5, 0.2, 0.4, 0.5, 0.2, 0.1, 0.2, 0.3, 0.9],
}
BASE_PRICE = {  # event: {section: price}
    "Concert": {"Floor": 180, "Lower Bowl": 120, "Upper Bowl": 65, "Club": 220, "Suite": 450},
    "Hockey": {"Lower Bowl": 95, "Upper Bowl": 45, "Club": 160, "Suite": 380},
    "Basketball": {"Lower Bowl": 105, "Upper Bowl": 50, "Club": 175, "Suite": 400},
    "Comedy": {"Floor": 85, "Lower Bowl": 70, "Upper Bowl": 40, "Club": 110},
    "Family Show": {"Floor": 60, "Lower Bowl": 45, "Upper Bowl": 30, "Club": 75},
}


def tickets(rng):
    day = day_in(rng, [1.0] * 12)
    event = pick(rng, {e: w[day.month - 1] for e, w in SEASON.items()})
    sections = BASE_PRICE[event]
    section = pick(rng, {s: {"Upper Bowl": 40, "Lower Bowl": 32, "Floor": 14, "Club": 9, "Suite": 3}[s]
                         for s in sections})
    channel = pick(rng, {"Website": 40, "Mobile App": 30, "Box Office": 15, "Reseller": 15})
    sports = event in ("Hockey", "Basketball")
    fan = pick(rng, {"Season Member": 20 if sports else 0, "Single Game": 65, "Group": 15})
    lead = int(rng.expovariate(1 / (6 if channel == "Mobile App" else 20)))
    p = sections[section] * rng.uniform(0.9, 1.1)
    p *= 1.25 if lead <= 2 else 0.9 if lead >= 45 else 1.0
    p *= 1.35 if channel == "Reseller" else 1.0
    p *= 0.8 if fan == "Group" else 0.85 if fan == "Season Member" else 1.0
    qty = rng.randint(10, 40) if fan == "Group" else min(8, max(1, int(rng.expovariate(1 / 2.2)) + 1))
    p = round(p, 2)
    if (event == "Concert" and day.month == 8 and rng.random() < 0.35) or rng.random() < 0.005:
        p = -p  # refund: the August concert was canceled
    return {"Purchase Date": day, "Event Type": event, "Seat Section": section,
            "Sales Channel": channel, "Fan Type": fan, "Ticket Price": p, "Tickets": qty,
            "Days Before Event": lead}


# ── dataset specs ─────────────────────────────────────────────
SPECS = [
    dict(file="capstone_retail.csv", make=retail, seed=1601,
         columns=["Order Date", "Product Category", "Region", "Unit Price", "Quantity Sold", "Customer Segment"],
         date="Order Date", money=["Unit Price"], typo="Product Category",
         misspell={"Electronics": "Electronix", "Furniture": "furnitu re"},
         missing_cat="Region", missing_num="Quantity Sold", count="Quantity Sold"),
    dict(file="capstone_marketing.csv", make=marketing, seed=1602,
         columns=["Date", "Channel", "Campaign Type", "Region", "Spend", "Impressions", "Clicks", "Conversions", "Revenue"],
         date="Date", money=["Spend", "Revenue"], typo="Channel",
         misspell={"Social Media": "Socail Media", "Paid Search": "paid serch"},
         missing_cat="Region", missing_num="Conversions", count="Conversions"),
    dict(file="capstone_accounting.csv", make=accounting, seed=1603, id_col="Invoice Number", id_start=20001,
         columns=["Invoice Number", "Invoice Date", "Vendor", "Expense Category", "Department", "Amount", "Payment Terms", "Days To Pay"],
         date="Invoice Date", money=["Amount"], typo="Expense Category",
         misspell={"Software": "Sofware", "Office Supplies": "office suplies"},
         missing_cat="Department", missing_num="Days To Pay", count="Days To Pay"),
    dict(file="capstone_finance.csv", make=finance, seed=1604, id_col="Loan ID", id_start=30001,
         columns=["Loan ID", "Application Date", "Industry", "Region", "Loan Amount", "Interest Rate", "Term Months", "Credit Score", "Employees", "Loan Status", "Profit"],
         date="Application Date", money=["Loan Amount", "Profit"], typo="Industry",
         misspell={"Restaurants": "Resturants", "Construction": "constrction"},
         missing_cat="Region", missing_num="Credit Score", count="Employees"),
    dict(file="capstone_hr.csv", make=hr, seed=1605, id_col="Employee ID", id_start=40001,
         columns=["Employee ID", "Hire Date", "Department", "Job Level", "Location", "Annual Salary", "Last Raise", "Performance Rating", "Training Hours", "Left Company"],
         date="Hire Date", money=["Annual Salary", "Last Raise"], typo="Department",
         misspell={"Customer Support": "Customer Suport", "Engineering": "engneering"},
         missing_cat="Location", missing_num="Performance Rating", count="Training Hours"),
    dict(file="capstone_it_helpdesk.csv", make=it_helpdesk, seed=1606, id_col="Ticket ID", id_start=50001,
         columns=["Ticket ID", "Opened Date", "Category", "Priority", "Channel", "Client Size", "Resolution Hours", "Billed Amount", "Satisfaction"],
         date="Opened Date", money=["Billed Amount"], typo="Category",
         misspell={"Network": "Netwrok", "Hardware": "hard ware"},
         missing_cat="Channel", missing_num="Satisfaction", count="Resolution Hours"),
    dict(file="capstone_shipments.csv", make=shipments, seed=1607, id_col="Shipment ID", id_start=60001,
         columns=["Shipment ID", "Ship Date", "Warehouse", "Carrier", "Product Category", "Units", "Order Value", "Freight Cost", "Promised Days", "Actual Days"],
         date="Ship Date", money=["Order Value", "Freight Cost"], typo="Carrier",
         misspell={"Coastal Express": "Costal Express", "Gulf Parcel": "gulf  parcel"},
         missing_cat="Warehouse", missing_num="Actual Days", count="Units"),
    dict(file="capstone_ticket_sales.csv", make=tickets, seed=1608, id_col="Order ID", id_start=70001,
         columns=["Order ID", "Purchase Date", "Event Type", "Seat Section", "Sales Channel", "Fan Type", "Ticket Price", "Tickets", "Days Before Event"],
         date="Purchase Date", money=["Ticket Price"], typo="Event Type",
         misspell={"Concert": "Concrt", "Family Show": "family  show"},
         missing_cat="Sales Channel", missing_num="Days Before Event", count="Tickets"),
]


def build(spec):
    rng = random.Random(spec["seed"])
    base = [spec["make"](rng) for _ in range(ROWS - DUPLICATES)]
    base.sort(key=lambda r: r[spec["date"]])
    rows = []
    for i, r in enumerate(base):
        if "id_col" in spec:
            r[spec["id_col"]] = spec["id_start"] + i
        messy = i >= CLEAN_HEAD
        d = r[spec["date"]]
        out = {}
        for col in spec["columns"]:
            v = r[col]
            if col == spec["date"]:
                v = d.isoformat()
            elif col in spec["money"]:
                v = money(v)
            out[col] = "" if v is None else str(v)
        if messy:
            x = rng.random()
            if x < 0.005:
                out[spec["date"]] = d.strftime("%m/%d/%Y")
            elif x < 0.010:
                out[spec["date"]] = f"{d.strftime('%B')} {d.day} {d.year}"
            elif x < 0.015:
                out[spec["date"]] = rng.choice(JUNK_DATES)
            elif x < 0.020:
                out[spec["date"]] = ""
            t = spec["typo"]
            v = out[t]
            if v in spec["misspell"] and rng.random() < 0.04:
                out[t] = spec["misspell"][v]
            else:
                y = rng.random()
                if y < 0.012:
                    out[t] = v.lower()
                elif y < 0.016:
                    out[t] = v.upper()
                elif y < 0.022:
                    out[t] = rng.choice([f" {v}", f"{v} ", f"{v}  "])
            if rng.random() < 0.025:
                out[spec["missing_cat"]] = ""
            if rng.random() < 0.02:
                out[spec["missing_num"]] = ""
            if out[spec["count"]] and rng.random() < 0.005:
                out[spec["count"]] = "0"
        rows.append(out)
    # three 9999 placeholders, spread through the year
    ok = [i for i, r in enumerate(rows) if i >= CLEAN_HEAD and r[spec["count"]] not in ("", "0")
          and not any(r[m].startswith("-") for m in spec["money"])]
    for i in (ok[len(ok) // 5], ok[len(ok) // 2], ok[4 * len(ok) // 5]):
        rows[i][spec["count"]] = "9999"
    # exact duplicates right after their originals (a double export)
    for i in sorted(rng.sample(range(CLEAN_HEAD, len(rows)), DUPLICATES), reverse=True):
        rows.insert(i + 1, dict(rows[i]))
    assert len(rows) == ROWS
    return rows


def main():
    out_dir = Path(sys.argv[1])
    out_dir.mkdir(parents=True, exist_ok=True)
    for spec in SPECS:
        rows = build(spec)
        with open(out_dir / spec["file"], "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=spec["columns"], lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)
        print(f"wrote {len(rows)} rows to {out_dir / spec['file']}")


if __name__ == "__main__":
    main()
