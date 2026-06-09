# Video 08: Reading & Debugging Error Messages

## YouTube Metadata

**Title:** Python Debugging — How to Read Tracebacks & Fix Errors | ISM2411 / ISM3232
**Description:**
Error messages are not failures — they're instructions. Python tells you exactly what went wrong, where, and usually why. In this video you'll learn to read a traceback from bottom to top, recognize the five most common error types, and fix bugs systematically using print() debugging.

We'll work through real broken code — a business order processor with multiple bugs — and fix it step by step. By the end, error messages will feel less like obstacles and more like helpful guides.

Course pages: https://markumreed.github.io/ism2411/pages/week07_lecture.html · https://markumreed.github.io/ism3232/docs/week08_lecture.html

**Chapters:**
0:00 — Errors are information, not failure
1:00 — Anatomy of a traceback
3:30 — SyntaxError — before your code runs
5:30 — NameError — undefined variable
7:00 — TypeError — wrong type for the operation
9:00 — ValueError — right type, wrong content
10:30 — IndexError / KeyError
12:00 — Print debugging
14:00 — Recap

**Applies to:** ISM2411 Module 7 · ISM3232 Module 8

**Tags:** python debugging, python traceback, python error messages, python NameError, python TypeError, python SyntaxError, python debug, ISM2411, ISM3232, python tutorial, python beginner, python fix errors

---

## Script

### INTRO (0:00–1:00)

When your code crashes, Python prints a traceback. Most beginners panic and close the terminal. That is exactly backwards. The traceback is Python trying to help you. It tells you the file, the line, and the exact error type. Reading it properly is the fastest way to fix bugs.

In this video we're going to deliberately break a business script in five different ways and fix each error using the traceback as our guide. After this, error messages will feel like help, not punishment.

---

### ANATOMY OF A TRACEBACK (1:00–3:30)

Here's a typical traceback:

```
Traceback (most recent call last):
  File "order_processor.py", line 12, in process_order
    total = subtotal + calculate_tax(subtotal, rate)
  File "order_processor.py", line 5, in calculate_tax
    return amunt * rate
NameError: name 'amunt' is not defined
```

Read it **bottom to top**.

1. **Bottom line** — the error type and message. This is the diagnosis. `NameError: name 'amunt' is not defined`.

2. **Middle lines** — the call stack. Where Python was when the error occurred. The innermost call (closest to the error) is last. `line 5, in calculate_tax` — that's where it broke.

3. **The code line** — `return amunt * rate`. Python shows you the exact line.

4. **Top** — "Traceback (most recent call last)" is just a header. Start at the bottom.

Fix: `amunt` is a typo for `amount`.

---

### SYNTAXERROR (3:30–5:30)

A SyntaxError means Python couldn't even parse your code. It happens before anything runs.

```python
def calculate_tax(amount, rate)    # Missing colon
    return amount * rate
```

Error:
```
SyntaxError: expected ':'
```

Common causes:
- Missing colon after `if`, `def`, `for`, `while`
- Mismatched parentheses or brackets
- Missing closing quote

```python
# Missing colon:
if order_total > 100
    print("Discount applies")

# Mismatched bracket:
sales = [100, 200, 300

# Missing quote:
name = "Priya Sharma
```

SyntaxErrors always point to the line (or the line just after) where Python got confused. Fix the syntax and run again.

---

### NAMEERROR (5:30–7:00)

A NameError means you used a name Python doesn't know about.

```python
subtotal = 199.92
discount = subtotal * discount_rate   # NameError: name 'discount_rate' is not defined
```

Causes:
- Misspelled variable name (`discount_rate` vs `discountrate`)
- Used a variable before assigning it
- Variable defined inside a function, used outside

```python
# Misspelling:
product_nmae = "Laptop Bag"
print(product_name)   # NameError — correct name is product_nmae

# Used before defined:
print(total)           # NameError
total = 100 + 50

# Out of scope:
def set_rate():
    rate = 0.10

set_rate()
print(rate)   # NameError — rate is local to set_rate
```

Fix: check spelling first. Then check where the variable is defined and whether it's in scope.

---

### TYPEERROR (7:00–9:00)

A TypeError means you performed an operation on the wrong type.

```python
quantity = "8"              # string, not int
unit_price = 24.99
total = quantity * unit_price   # TypeError: can't multiply sequence by non-int of type 'float'
```

Common causes:
- Forgetting to convert `input()` results from str to int/float
- Concatenating str + int directly
- Calling a function with the wrong number of arguments

```python
# input() always returns str:
qty = input("Quantity: ")          # returns "8" as string
total = qty * 24.99                # TypeError

# Fix:
qty = int(input("Quantity: "))     # convert immediately

# Concatenation:
count = 5
print("Items: " + count)           # TypeError: can only concatenate str (not "int") to str

# Fix:
print("Items: " + str(count))     # or: print(f"Items: {count}")
```

---

### VALUEERROR (9:00–10:30)

The type is right, but the content isn't valid for the operation.

```python
price = float("twenty-four dollars")   # ValueError: could not convert string to float
```

Causes:
- Converting a string that doesn't look like a number
- `int()` on a float-looking string (`int("24.99")` fails — use `int(float("24.99"))`)

```python
# This works:
price = float("24.99")     # 24.99

# This fails:
price = float("$24.99")    # ValueError — dollar sign confuses it

# Fix — strip the symbol first:
price = float("$24.99".replace("$", ""))
```

---

### INDEXERROR / KEYERROR (10:30–12:00)

**IndexError** — list index out of range.

```python
sales = [100, 200, 300]
print(sales[5])   # IndexError: list index out of range
```

Lists are zero-indexed. `sales[0]` is 100, `sales[2]` is 300. `sales[3]` and beyond don't exist.

**KeyError** — dictionary key doesn't exist.

```python
customer = {"name": "Priya", "tier": "Gold"}
print(customer["email"])   # KeyError: 'email'
```

Fix: use `.get()` for safe access, or check with `in` first:

```python
if "email" in customer:
    print(customer["email"])
else:
    print("No email on file.")

# Or:
print(customer.get("email", "No email on file."))
```

---

### PRINT DEBUGGING (12:00–14:00)

When there's no error but the output is wrong — a logic bug — print debugging is your first tool. Add `print()` statements to see what your variables actually contain at each step.

```python
def process_order(subtotal, discount_rate, tax_rate):
    print(f"DEBUG: subtotal={subtotal}, discount_rate={discount_rate}")   # add this

    discount = subtotal * discount_rate
    print(f"DEBUG: discount={discount}")   # and this

    after_discount = subtotal - discount
    tax = after_discount * tax_rate
    total = after_discount + tax

    print(f"DEBUG: total={total}")   # and this
    return total

result = process_order(200, 1.10, 0.0875)   # bug: rate is 1.10 not 0.10
```

Output:
```
DEBUG: subtotal=200, discount_rate=1.10
DEBUG: discount=220.0     ← discount is bigger than subtotal — found the bug!
```

The print statements revealed that `discount_rate=1.10` when it should be `0.10`. Remove the debug prints once fixed.

---

### RECAP (14:00–15:00)

- Read tracebacks **bottom to top** — the error type is at the bottom
- **SyntaxError** — malformed code, missing colon/bracket/quote
- **NameError** — name used before defined or misspelled
- **TypeError** — wrong type for the operation; `input()` always returns str
- **ValueError** — right type, content doesn't parse
- **IndexError/KeyError** — index or key doesn't exist; use `.get()` or bounds-check
- **Print debugging** — add `print()` to see variable values mid-execution; remove when done

Next video: 5 core terminal commands — the shell skills you need to navigate, create, and manage your project files.
