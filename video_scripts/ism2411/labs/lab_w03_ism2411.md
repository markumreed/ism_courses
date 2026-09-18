# ISM2411 Lab W03: Product Pricer with f-strings

## YouTube Metadata

**Title:** Product Pricer with f-strings — Full Lab Walkthrough | ISM2411 Lab 03
**Description:**
Step-by-step, test-as-you-go walkthrough of ISM2411 Module 3 Lab. Build pricer.py from scratch: four core variable types, f-string formatting with format specs, an input()-driven version with type conversion, a five-line product card computing margin, and a live investigation of string concatenation vs. numeric addition in the Python interpreter.

Course page: https://markumreed.github.io/ism2411/pages/week03_lab.html

**Chapters:**
0:00 — What this lab covers
0:40 — Exercise 1: four variables, four types
1:50 — Exercise 2: the first f-string summary line
3:00 — Exercise 3: convert the script to use input()
4:20 — Exercise 4: the five-line product card with margin
6:10 — Exercise 5: type() and string vs. numeric + in the interpreter
7:50 — Reflection questions
8:40 — Submission checklist

**Applies to:** ISM2411 Module 03

**Tags:** python f-strings tutorial, python format spec, python type conversion, python interactive interpreter, ISM2411, USF, python for business beginners

---

## How to Use This Script

**SAY** it, **DO** it, **CHECK** the exact output, **FIX** it if it doesn't match — then move to the next step. Everything gets built inside one file, `pricer.py`, with comments separating each exercise — that's the exact submission format required.

---

## Script

### INTRO (0:00–0:40)

**SAY:** "Lab 3 — the Product Pricer. This is the first lab where you build something that looks like a real tiny tool, not just a print statement. Four variable types, f-string formatting, user input, and a small business calculation — margin — all in one file called `pricer.py`."

---

### EXERCISE 1 — Variables and Types (0:40–1:50)

**SAY:** "Four variables, four different data types — and we confirm each type explicitly with `type()`, rather than assuming."

**DO:** In `pricer.py`:
```python
# Exercise 1: variables and types
product    = "Notebook"
unit_price = 4.99
quantity   = 12
in_stock   = True

print(type(product))
print(type(unit_price))
print(type(quantity))
print(type(in_stock))
```
```bash
python3 pricer.py
```

**CHECK:**
```
<class 'str'>
<class 'float'>
<class 'int'>
<class 'bool'>
```
Four distinct types, matching exactly what you'd expect from how each value is written: quotes mean string, a decimal point means float, a whole number means int, `True`/`False` means bool.

---

### EXERCISE 2 — f-string Practice (1:50–3:00)

**SAY:** "Now format those four variables into one readable sentence, computing the total right inside the f-string."

**DO:**
```python
# Exercise 2: f-string practice
print(f"{quantity} units of {product} at ${unit_price} each = ${unit_price * quantity:.2f}")
```
```bash
python3 pricer.py
```

**CHECK:**
```
12 units of Notebook at $4.99 each = $59.88
```

**SAY:** "Notice `{unit_price * quantity:.2f}` — the calculation happens directly inside the curly braces, and `:.2f` forces exactly two decimal places on the result, so `59.88` prints cleanly instead of risking something like `59.879999999999995` from floating-point math."

---

### EXERCISE 3 — Input Version (3:00–4:20)

**SAY:** "Same summary line, but now the three values come from the user at runtime instead of being hardcoded."

**DO:**
```python
# Exercise 3: input version
product_in  = input("Product name: ")
price_in    = float(input("Unit price: "))
quantity_in = int(input("Quantity: "))

print(f"{quantity_in} units of {product_in} at ${price_in} each = ${price_in * quantity_in:.2f}")
```
```bash
python3 pricer.py
```
Type `Pen`, `1.25`, and `20` at the three prompts.

**CHECK:**
```
Product name: Pen
Unit price: 1.25
Quantity: 20
20 units of Pen at $1.25 each = $25.00
```

**FIX:** If you get `ValueError: could not convert string to float`, you likely typed non-numeric text at the price prompt — `input()` always returns a string, and `float(...)` needs that string to actually look like a number.

---

### EXERCISE 4 — Multi-Variable Product Card (4:20–6:10)

**SAY:** "Now a five-line formatted report, including a business calculation you haven't done yet this semester: margin — the percentage of revenue that's profit."

**DO:**
```python
# Exercise 4: multi-variable product card
unit_cost = 3.29

revenue = unit_price * quantity
margin  = (unit_price - unit_cost) / unit_price * 100

print(f"Product:  {product}")
print(f"Price:    ${unit_price:.2f}")
print(f"Qty:      {quantity}")
print(f"Revenue:  ${revenue:.2f}")
print(f"Margin:   {margin:.1f}%")
```
```bash
python3 pricer.py
```

**CHECK:**
```
Product:  Notebook
Price:    $4.99
Qty:      12
Revenue:  $59.88
Margin:   34.1%
```

**SAY:** "Trace the margin formula out loud before trusting the output: `(4.99 - 3.29) / 4.99 * 100` — that's `1.70 / 4.99`, roughly `0.3407`, times 100 is `34.07`, and `:.1f` rounds that to one decimal place: `34.1`."

---

### EXERCISE 5 — Type Investigation (6:10–7:50)

**SAY:** "Now a completely different environment — the Python interactive interpreter, where you type one line at a time and see the result immediately, with no file at all."

**DO:**
```bash
python3
```
```python
>>> type("12")
>>> type(12)
>>> type(12.0)
>>> type(True)
>>> "5" + "3"
>>> 5 + 3
>>> exit()
```

**CHECK:**
```
>>> type("12")
<class 'str'>
>>> type(12)
<class 'int'>
>>> type(12.0)
<class 'float'>
>>> type(True)
<class 'bool'>
>>> "5" + "3"
'53'
>>> 5 + 3
8
```

**SAY:** "Write down exactly what you're seeing: `\"5\" + \"3\"` produces `'53'` — that's *concatenation*, gluing two strings end to end, because both sides are strings. `5 + 3` produces `8` — plain addition, because both sides are integers. Same `+` symbol, completely different behavior, entirely determined by the types on either side."

---

### REFLECTION QUESTIONS (7:50–8:40)

**DO:** Answer honestly:
1. What happened when you ran Exercise 3 and forgot to convert the price from string to float? Describe the exact error message and explain why it occurred in your own words.
2. In Exercise 5, `"5" + "3"` returned `"53"` instead of `8`. Why does Python do this, and how does it explain why `input()` must always be converted before doing math?
3. How would you use variables, types, and f-strings to build a real tool for a task in your future career? Describe a specific scenario in 2–3 sentences.

**CHECK:** Question 2's answer should connect directly back to Exercise 5's observation: `input()` always returns a `str`, and `+` on two strings concatenates rather than adds — exactly the behavior you just saw, which is why Exercise 3 required `float(...)` and `int(...)` wrappers around every `input()` call.

---

### SUBMISSION CHECKLIST (8:40–end)

- [ ] `pricer.py` — filename matches exactly, lowercase
- [ ] Exercises 1–4 present as one runnable script, with `#` comments separating each exercise
- [ ] Exercise 5's written observations about `"5" + "3"` vs `5 + 3`
- [ ] Three reflection questions answered honestly
- [ ] Submitted to Canvas
