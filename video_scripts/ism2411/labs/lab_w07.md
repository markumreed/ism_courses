# ISM2411 Lab W07: Functions + Debug First, Then Ask

## YouTube Metadata

**Title:** Functions + Debug First, Then Ask — Lab Walkthrough | ISM2411 Lab 07
**Description:**
Walkthrough of ISM2411 Module 7 Lab. We write reusable business functions with parameters and return values, then work through the debugging exercise: read the traceback, add print() statements, and only then use AI — as an explainer, not a solution machine.

Course page: https://markumreed.github.io/ism2411/pages/week07_lab.html

**Chapters:**
0:00 — What this lab covers
0:45 — Writing the four business functions
4:00 — The debugging workflow: traceback → print() → AI explainer → fix
7:00 — AI disclosure and reflection
8:30 — Submission checklist

**Applies to:** ISM2411 Module 07

**Tags:** python functions def, python debugging traceback, python AI literacy, python business functions, ISM2411, USF, python function parameters return

---

## Script

### INTRO (0:00–0:45)

Lab 7 — Functions and Debug First, Then Ask. Two parts: writing clean functions with parameters and return values, and a structured debugging exercise that builds the habit of reading errors before asking AI. Both skills matter as much as any syntax.

---

### THE FOUR BUSINESS FUNCTIONS (0:45–4:00)

Create `module07/business_tools.py`:

```python
# business_tools.py

def calculate_total(price: float, quantity: int) -> float:
    """Return the total cost of a line item."""
    return price * quantity


def apply_discount(total: float, rate: float) -> float:
    """Apply a discount rate (0.0–1.0) and return the discounted price."""
    return total * (1 - rate)


def is_high_value(total: float, threshold: float = 500.0) -> bool:
    """Return True if total exceeds the threshold."""
    return total > threshold


def format_receipt(name: str, total: float) -> str:
    """Return a formatted receipt line."""
    return f"{name:<20} ${total:>8,.2f}"
```

Now create `module07/main.py` to call them:

```python
from business_tools import calculate_total, apply_discount, is_high_value, format_receipt

price    = 79.99
qty      = 12
discount = 0.10

total           = calculate_total(price, qty)
discounted      = apply_discount(total, discount)
high_value      = is_high_value(discounted)

print(format_receipt("Laptop Bag", discounted))
print(f"High-value order: {high_value}")
```

Output:
```
Laptop Bag           $  863.89
High-value order: True
```

Each function does one thing. Parameters make them reusable — call `apply_discount` with any total and any rate. Return values make them composable — the output of one feeds directly into the next.

---

### THE DEBUGGING WORKFLOW (4:00–7:00)

The lab provides a buggy script. Work through it in four steps.

**Step 1 — Read the traceback first.** Run the script and read every line of the error. The last line tells you the error type. The line above tells you where it happened. Do not change anything yet.

Example traceback:
```
Traceback (most recent call last):
  File "buggy.py", line 8, in <module>
    result = apply_discount(total, discount_pct)
TypeError: unsupported operand type(s) for *: 'float' and 'str'
```

From this alone you know: line 8, `discount_pct` is a string instead of a float. Probably came from `input()` without conversion.

**Step 2 — Add print() statements.** Before the crashing line, print the variable:
```python
print(f"DEBUG: total={total}, type={type(total)}")
print(f"DEBUG: discount_pct={discount_pct}, type={type(discount_pct)}")
```

**Step 3 — Ask AI for the error type, not the fix.** Paste only the error message into Claude or ChatGPT and ask "what does this error mean?" Not "fix my code." The explanation builds your understanding; the fix shortcircuits it.

**Step 4 — Fix it yourself**, using the AI's explanation as a guide. Write a comment above the fix explaining what you changed and why.

---

### AI DISCLOSURE AND REFLECTION (7:00–8:30)

The lab requires an AI use statement if you used AI at any point. Format it as a comment at the top of your file:

```python
# AI USE: Used Claude to explain the TypeError on line 8.
# It explained that * requires two numbers; my discount_pct was str not float.
# I applied the fix (float conversion) myself.
```

This is not optional. It's the professional standard — the same one you'll follow in any real job where AI tools are involved.

---

### SUBMISSION CHECKLIST (8:30–10:00)

- `business_tools.py` with four functions, type hints, docstrings
- `main.py` importing and calling all four
- Buggy script fixed with print() debugging documented
- AI use statement in the file (even if "AI not used")
- Exercise reflection written
- Submitted to Canvas
