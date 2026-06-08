# ISM2411 Lab W03: Product Pricer with F-Strings

## YouTube Metadata

**Title:** Product Pricer with F-Strings — Lab Walkthrough | ISM2411 Lab 03
**Description:**
Walkthrough of ISM2411 Module 3 Lab. We build a product pricing tool using variables, the four core data types, f-string formatting, and user input with type conversion.

**Chapters:**
0:00 — What we're building
0:45 — Defining variables for all four data types
2:30 — Formatting output with f-strings
4:30 — Adding user input with float() conversion
6:30 — Exercise 5: the "5" + "3" = "53" trap
8:00 — Submission checklist

**Applies to:** ISM2411 Module 03

**Tags:** python f-strings, python variables, python input type conversion, python product pricer, ISM2411, USF, python beginner lab, python data types tutorial

---

## Script

### INTRO (0:00–0:45)

Lab 3 — Product Pricer with F-Strings. We're combining variables, types, and f-strings into one small tool: a product pricing calculator. By the end, the program takes a user's quantity, calculates the total, and prints a formatted receipt.

---

### FOUR DATA TYPES IN ACTION (0:45–2:30)

Open VS Code, create `module03/pricer.py`.

```python
# pricer.py

product_name     = "Executive Laptop Bag"   # str
unit_price       = 49.99                    # float
quantity         = 12                       # int
is_available     = True                     # bool
```

This is the product record. One of each type. Let's verify with `type()`:

```python
print(type(product_name))     # <class 'str'>
print(type(unit_price))       # <class 'float'>
print(type(quantity))         # <class 'int'>
print(type(is_available))     # <class 'bool'>
```

Run it. All four types confirmed.

---

### F-STRING FORMATTING (2:30–4:30)

Now let's calculate the total and display a formatted receipt:

```python
total = unit_price * quantity

print(f"Product:    {product_name}")
print(f"Unit price: ${unit_price:.2f}")
print(f"Quantity:   {quantity}")
print(f"Total:      ${total:,.2f}")
print(f"Available:  {is_available}")
```

Output:
```
Product:    Executive Laptop Bag
Unit price: $49.99
Quantity:   12
Total:      $599.88
Available:  True
```

The format specs: `:.2f` = two decimal places. `:,.2f` = thousands separator + two decimal places. These are the two you'll use most in business output.

---

### USER INPUT WITH TYPE CONVERSION (4:30–6:30)

The lab asks you to take quantity from the user:

```python
user_qty = input("How many do you want? ")   # always returns str
quantity = int(user_qty)                      # convert to int
total = unit_price * quantity

print(f"\nOrder Summary")
print(f"  {product_name} × {quantity} = ${total:,.2f}")
```

Or more concisely:
```python
quantity = int(input("How many do you want? "))
```

Run it. Type `5`. Output should show `$249.95`.

Now deliberately break it: type `"five"` instead of `5`. You get:
```
ValueError: invalid literal for int() with base 10: 'five'
```

That's the error the lab asks about in Exercise 3. `int()` can only convert strings that actually contain a valid integer.

---

### THE "5" + "3" TRAP (6:30–8:00)

Exercise 5 asks you to run this:
```python
print("5" + "3")   # "53" — string concatenation, not addition
print(5 + 3)       # 8 — integer addition
```

This is why `input()` must always be converted. Without conversion, every number the user types is a string. `"100" + "50"` gives `"10050"`, not `150`.

The fix is always `int()` or `float()` immediately after `input()`.

---

### SUBMISSION CHECKLIST (8:00–10:00)

- `pricer.py` with all four data types assigned as variables
- F-string output with `:.2f` formatting on prices
- `input()` used for quantity with `int()` or `float()` conversion
- Total calculated correctly
- Exercise responses written (type error explanation, "5"+"3" explanation, career scenario)
- Submitted to Canvas

Lab 3 done. Next lab we build a full revenue and margin calculator.
