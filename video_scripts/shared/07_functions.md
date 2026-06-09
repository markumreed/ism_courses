# Video 07: Functions — def, Parameters & Return

## YouTube Metadata

**Title:** Python Functions for Business — def, Parameters, Return Values | ISM2411 / ISM3232
**Description:**
Functions let you name a block of logic, call it whenever you need it, and change the inputs without rewriting the code. In this video we build a suite of business calculation functions — tax, discount, order total — and learn why functions are the single most important tool for writing maintainable code.

You'll learn the exact syntax, understand parameters vs arguments, master return values, and see the difference between a function that does its own printing versus one that returns a value you can use.

Course pages: https://markumreed.github.io/ism2411/pages/week07_lecture.html · https://markumreed.github.io/ism3232/docs/week07_lecture.html

**Chapters:**
0:00 — Why functions exist
1:30 — def syntax and calling a function
4:00 — Parameters and arguments
6:30 — Return values
9:00 — Multiple parameters and default values
11:30 — Functions calling functions
13:00 — Common mistakes
14:30 — Recap

**Applies to:** ISM2411 Module 7 · ISM3232 Module 7

**Tags:** python functions, python def, python return, python parameters, python arguments, python default parameters, python business, ISM2411, ISM3232, python tutorial, python beginner, python function examples

---

## Script

### INTRO (0:00–1:30)

You've written code that calculates order totals. Tax. Discounts. What happens when you need that same calculation in five different places in your script? You could copy-paste it. But then when the tax rate changes, you have to find and update every copy. Miss one and your numbers are wrong.

Functions solve this. A function is a named block of code you write once and call as many times as you need. Change the logic in one place and every call benefits automatically. Functions also make your code readable — a call to `calculate_total(subtotal, discount_rate)` is self-documenting in a way that inline math never is.

---

### DEF SYNTAX AND CALLING (1:30–4:00)

Define a function with the `def` keyword, a name, parentheses, and a colon. The body is indented.

```python
def greet_customer():
    print("Welcome to the Campus Bookstore!")
    print("How can we help you today?")
```

Defining the function does nothing. You have to call it:

```python
greet_customer()
greet_customer()
greet_customer()
```

Output (three times):
```
Welcome to the Campus Bookstore!
How can we help you today?
```

The function runs when called. Each call is independent.

---

### PARAMETERS AND ARGUMENTS (4:00–6:30)

A function with no parameters always does exactly the same thing. More useful is a function that accepts input and works with it.

```python
def greet_customer(name):
    print(f"Welcome, {name}! How can we help you today?")
```

`name` is the **parameter** — a placeholder inside the function definition. When you call the function, you pass an **argument** — the actual value.

```python
greet_customer("Priya")
greet_customer("Marcus")
greet_customer("Elena")
```

Output:
```
Welcome, Priya! How can we help you today?
Welcome, Marcus! How can we help you today?
Welcome, Elena! How can we help you today?
```

Same function, three different results, depending on the argument passed.

---

### RETURN VALUES (6:30–9:00)

A function that only prints isn't very useful outside of display contexts. Most business functions should **compute something and return it** — so you can use the result in further calculations, store it in a variable, or pass it to another function.

```python
def calculate_tax(amount, rate):
    return amount * rate
```

`return` sends a value back to the caller. The function stops executing at `return`.

```python
subtotal = 214.94
tax = calculate_tax(subtotal, 0.0875)
print(f"Tax: ${tax:.2f}")
```

Output: `Tax: $18.81`

The return value can be stored in a variable, used in a calculation, or passed directly to another function:

```python
total = subtotal + calculate_tax(subtotal, 0.0875)
print(f"Total: ${total:.2f}")
```

**Key distinction:** a function that `print()`s a value gives you something to read. A function that `return`s a value gives you something to use. In business code, almost always return — let the caller decide what to do with the result.

---

### MULTIPLE PARAMETERS AND DEFAULTS (9:00–11:30)

Functions can take multiple parameters. Separate them with commas.

```python
def calculate_order_total(subtotal, discount_rate, tax_rate):
    discount = subtotal * discount_rate
    after_discount = subtotal - discount
    tax = after_discount * tax_rate
    total = after_discount + tax
    return total
```

Call it:

```python
total = calculate_order_total(214.94, 0.10, 0.0875)
print(f"Order total: ${total:.2f}")
```

Output: `Order total: $212.14`

**Default parameter values** — supply a value in the function definition and the caller can omit it:

```python
def calculate_order_total(subtotal, discount_rate=0.0, tax_rate=0.0875):
    discount = subtotal * discount_rate
    after_discount = subtotal - discount
    tax = after_discount * tax_rate
    return after_discount + tax

# Use defaults:
print(f"${calculate_order_total(100):.2f}")            # no discount, default tax

# Override discount:
print(f"${calculate_order_total(100, 0.10):.2f}")      # 10% discount, default tax

# Override both:
print(f"${calculate_order_total(100, 0.15, 0.06):.2f}")
```

Output:
```
$108.75
$98.06
$89.90
```

---

### FUNCTIONS CALLING FUNCTIONS (11:30–13:00)

Break complex logic into small, focused functions. Have higher-level functions call them.

```python
def apply_discount(subtotal, rate):
    return subtotal * (1 - rate)

def apply_tax(amount, rate):
    return amount * (1 + rate)

def get_discount_rate(subtotal):
    if subtotal > 250:
        return 0.15
    elif subtotal > 100:
        return 0.10
    return 0.0

def process_order(subtotal, tax_rate=0.0875):
    rate     = get_discount_rate(subtotal)
    discounted = apply_discount(subtotal, rate)
    total    = apply_tax(discounted, tax_rate)
    return total, rate   # return multiple values as a tuple

total, rate = process_order(300)
print(f"Discount: {rate:.0%}, Total: ${total:.2f}")
```

Output: `Discount: 15%, Total: $272.78`

Each function does one thing. `process_order` orchestrates them. This is the architecture of professional Python.

---

### COMMON MISTAKES (13:00–14:30)

**Forgetting the return statement — function returns None.**

```python
def calculate_tax(amount, rate):
    amount * rate   # computed but not returned!

result = calculate_tax(100, 0.08)
print(result)   # None
```

Fix: add `return amount * rate`.

**Using the result before calling the function.**

```python
print(total)   # NameError — total not assigned yet
total = calculate_order_total(100, 0.10, 0.0875)
```

**Confusing local and global variables.** Variables defined inside a function are local — they don't exist outside it.

```python
def set_discount():
    rate = 0.15   # local to this function

set_discount()
print(rate)   # NameError — rate doesn't exist here
```

Fix: return the value and capture it: `rate = set_discount()`.

---

### RECAP (14:30–15:00)

- `def name(parameters):` — define a function
- `return value` — send a result back to the caller
- Parameters are placeholders; arguments are actual values
- Default parameters make arguments optional
- Almost always `return` rather than `print` — let the caller decide what to do
- Small focused functions that call each other are better than one big function
- Variables inside a function are local — they don't exist outside

Next video: reading and debugging error messages — how to decode a Python traceback systematically.
