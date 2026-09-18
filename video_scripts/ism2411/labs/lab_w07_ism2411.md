# ISM2411 Lab W07: Functions + Debug First, Then Ask

## YouTube Metadata

**Title:** Functions & Debug-First-Then-Ask — Full Lab Walkthrough | ISM2411 Lab 07
**Description:**
Step-by-step, test-as-you-go walkthrough of ISM2411 Module 7 Lab. Build functions.py: calculate_tax and apply_discount as standalone functions, compose them into final_price, loop a function over a list of orders, run the four-step Debug-First-Then-Ask protocol on a provided buggy file, and a hands-on scope experiment with global vs. local variables.

Course page: https://markumreed.github.io/ism2411/pages/week07_lab.html

**Chapters:**
0:00 — What this lab covers
0:45 — Exercise 1: calculate_tax()
1:50 — Exercise 2: apply_discount() with four tiers
3:20 — Exercise 3: composing two functions into final_price()
5:10 — Exercise 4: looping final_price() over a list of orders
6:30 — Exercise 5: the Debug-First-Then-Ask protocol
9:30 — Exercise 6: the scope experiment
11:20 — Reflection questions
12:10 — Submission checklist

**Applies to:** ISM2411 Module 07

**Tags:** python functions tutorial, python global vs local scope, rubber duck debugging, python default parameters docstring, ISM2411, USF, python for business beginners

---

## How to Use This Script

**SAY** it, **DO** it, **CHECK** the exact output, **FIX** it if it doesn't match — then move to the next step. Everything builds into one file, `functions.py`.

---

## Script

### INTRO (0:00–0:45)

**SAY:** "Lab 7 — functions, plus your first structured debugging protocol. Two skills today that compound for the rest of the semester: writing reusable functions, and a disciplined four-step process for fixing bugs *before* reaching for AI."

---

### EXERCISE 1 — calculate_tax (0:45–1:50)

**SAY:** "The smallest possible function — one calculation, two parameters, one return."

**DO:**
```python
# --- Exercise 1 ---
def calculate_tax(price, rate):
    return price * rate

print(f"Tax on $100 at 7%: ${calculate_tax(100, 0.07):.2f}")
print(f"Tax on $250 at 8%: ${calculate_tax(250, 0.08):.2f}")
```
```bash
python3 functions.py
```

**CHECK:**
```
Tax on $100 at 7%: $7.00
Tax on $250 at 8%: $20.00
```
Confirm: `100 × 0.07 = 7.00`, `250 × 0.08 = 20.00`.

---

### EXERCISE 2 — apply_discount (1:50–3:20)

**SAY:** "Now a function with branching logic inside it — same tier structure from Module 5, wrapped in a reusable function this time."

**DO:**
```python
# --- Exercise 2 ---
def apply_discount(price, tier):
    if tier == "gold":
        discount = 0.15
    elif tier == "silver":
        discount = 0.10
    elif tier == "bronze":
        discount = 0.05
    else:
        discount = 0
    return price * (1 - discount)

print(f"gold:   ${apply_discount(200, 'gold'):.2f}")
print(f"silver: ${apply_discount(200, 'silver'):.2f}")
print(f"bronze: ${apply_discount(200, 'bronze'):.2f}")
print(f"none:   ${apply_discount(200, 'anything_else'):.2f}")
```
```bash
python3 functions.py
```

**CHECK:**
```
gold:   $170.00
silver: $180.00
bronze: $190.00
none:   $200.00
```
Confirm each: `200 × 0.85 = 170`, `200 × 0.90 = 180`, `200 × 0.95 = 190`, and any tier that isn't recognized falls to `else` with no discount at all.

---

### EXERCISE 3 — Compose Them (3:20–5:10)

**SAY:** "Now use both functions together — the output of one feeds into the input of the other — and then wrap that composition in a third function."

**DO:**
```python
# --- Exercise 3 ---
after_discount = apply_discount(200, "gold")
after_tax = after_discount + calculate_tax(after_discount, 0.07)
print(f"After gold discount: ${after_discount:.2f}")
print(f"After tax: ${after_tax:.2f}")


def final_price(price, tier, tax_rate):
    discounted = apply_discount(price, tier)
    return discounted + calculate_tax(discounted, tax_rate)


print(f'final_price(200, "gold", 0.07) = ${final_price(200, "gold", 0.07):.2f}')
```
```bash
python3 functions.py
```

**CHECK:**
```
After gold discount: $170.00
After tax: $181.90
final_price(200, "gold", 0.07) = $181.90
```

**SAY:** "Trace the composition: `apply_discount(200, 'gold')` returns `170.00`. Tax is calculated *on the discounted price*, not the original $200 — `calculate_tax(170, 0.07) = 11.90`. Add them: `170 + 11.90 = 181.90`. `final_price` does exactly this same sequence internally, so calling it directly produces the identical number."

---

### EXERCISE 4 — Loop + Function (5:10–6:30)

**SAY:** "Now the payoff of writing `final_price` as a function — running it across an entire list of orders with a loop, instead of retyping the calculation four times."

**DO:**
```python
# --- Exercise 4 ---
orders = [(200, "gold"), (150, "silver"), (80, "bronze"), (500, "none")]
for price, tier in orders:
    total = final_price(price, tier, 0.07)
    print(f"Price: ${price} | Tier: {tier} | Final: ${total:.2f}")
```
```bash
python3 functions.py
```

**CHECK:**
```
Price: $200 | Tier: gold | Final: $181.90
Price: $150 | Tier: silver | Final: $144.45
Price: $80 | Tier: bronze | Final: $81.32
Price: $500 | Tier: none | Final: $535.00
```
Spot-check the silver row: `150 × 0.90 = 135`, tax on that at 7% is `9.45`, and `135 + 9.45 = 144.45`.

**SAY:** "Notice `tier == 'none'` falls into `apply_discount`'s `else` branch just like Exercise 2's `'anything_else'` did — the string `'none'` isn't special to the function, it's just another string that doesn't match `'gold'`, `'silver'`, or `'bronze'`."

---

### EXERCISE 5 — Debug First, Then Ask (6:30–9:30)

**SAY:** "Your instructor will provide `broken_sales.py` with three intentional bugs, separately from this lab page — open that file now and follow this exact four-step protocol, timed."

**DO — 5 min, solo debug:** Add `print()` statements to trace variable values as the script runs. Read the full traceback, top to bottom. Then explain the suspect section out loud, line by line, to a rubber duck — or your water bottle, or any patient object within reach. Write down what you *think* each bug is before fixing anything.

**CHECK:** You should have a written note, for each of the three bugs, stating your hypothesis — *before* any AI tool has been consulted.

**DO — 5 min, AI explainer:** Paste only the error message — not your code — into ChatGPT or Claude. Ask "what does this error mean?" Do not ask for the fix.

**CHECK:** You have the AI's plain-language explanation of the error *type*, not a corrected version of your code.

**DO — 5 min, fix it yourself:** Use the AI's explanation as a guide, not an answer key. Write the fix in your own words as a comment, *before* implementing it in code.

**CHECK:** A comment above each fix, in your own words, stating what was wrong and why the fix addresses it — written before the corrected code, not after.

**DO — 5 min, class debrief:** Share what you found. Did the AI's explanation match what you'd already suspected from the traceback and the rubber-duck explanation?

**SAY:** "That out-loud explanation in step one is rubber duck debugging — from *The Pragmatic Programmer* (Hunt & Thomas, 1999). Full technique in the Module 7 reading."

**DO:** Paste your fixed version of `broken_sales.py` directly into `functions.py`, under a `# --- Exercise 5 ---` comment — it belongs in the same submitted file as everything else.

---

### EXERCISE 6 — Scope Experiment (9:30–11:20)

**SAY:** "Before running this, predict out loud what each `print()` will show."

**DO:**
```python
# --- Exercise 6 ---
x = 100   # global variable

def double_it():
    x = 999   # local variable — different from global x!
    return x * 2

print(x)           # what prints here?
print(double_it()) # what prints here?
print(x)           # has x changed?
```
```bash
python3 functions.py
```

**CHECK:**
```
100
1998
100
```

**SAY:** "First `print(x)` — `100`, the global value, untouched so far. `print(double_it())` — `1998`, because *inside* the function, `x = 999` creates a brand-new *local* variable that happens to share the same name as the global one, and `999 * 2 = 1998` is what gets returned. Third `print(x)` — still `100`. The function's `x = 999` never touched the global `x` at all; it created a completely separate variable that only exists while `double_it()` is running, and disappears the moment the function returns."

Add a comment explaining this in your own words directly in the file.

---

### REFLECTION QUESTIONS (11:20–12:10)

**DO:** Answer honestly:
1. In Exercise 5 (Debug First, Then Ask), what was the first bug you spotted? Did you find it from the traceback, from a `print()` statement, from explaining the code out loud to the duck, or only after asking AI? What does that tell you about your current debugging instincts?
2. Without looking at your code, explain in plain English what `apply_discount(price, tier)` does, what its inputs are, and what it returns. Could a colleague use it without reading the body?
3. If you used AI on any part of today's lab, write the disclosure comment you would add to the top of your file. Then reflect: did the AI use build your understanding, or did it shortcut it?

**CHECK:** Question 2 is a real test of your own function's documentation — if you can't answer it cleanly without opening `apply_discount`'s body, that's a signal its naming or structure needs work.

---

### SUBMISSION CHECKLIST (12:10–end)

- [ ] `functions.py` — filename matches exactly, lowercase, one runnable script
- [ ] Exercises 1–6 each separated by a `# --- Exercise N ---` comment: `apply_discount`, `calculate_tax`, `final_price`, the loop over `orders`, your fixed version of `broken_sales.py`, and the scope experiment with its explanatory comment
- [ ] Comment block at the top of the file with your answers to Self-Assessment Questions 1 and 2
- [ ] If you used AI on any part of the lab: the disclosure comment from Question 3 at the top of the file (write "No AI used" if none)
- [ ] The script runs from top to bottom with no errors
