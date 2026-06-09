# Video 01: Variables & Data Types

## YouTube Metadata

**Title:** Python Variables & Data Types for Business — ISM2411 / ISM3232
**Description:**
Learn how to store and work with data in Python using variables and the four core data types: strings, integers, floats, and booleans. Every business script you write starts here.

In this video we build a product inventory record from scratch — naming a product, storing its price, tracking quantity, and flagging whether it's in stock. Along the way you'll learn exactly what Python is doing when you assign a variable, why the type of your data matters, and the errors beginners make most often.

Course pages: https://markumreed.github.io/ism2411/pages/week03_lecture.html · https://markumreed.github.io/ism3232/docs/week05_lecture.html

**Chapters:**
0:00 — Why variables matter in business programming
1:30 — The four core data types (str, int, float, bool)
4:00 — Building a product record in Python
7:30 — Checking types with type()
9:30 — Type conversion: int(), float(), str()
12:00 — Common errors and how to read them
14:00 — Recap and what's next

**Applies to:** ISM2411 Module 3 · ISM3232 Module 5

**Tags:** python variables, python data types, python for beginners, python string int float bool, python business, python type conversion, ISM2411, ISM3232, USF, python tutorial, learn python, python variables tutorial, python type function, python beginner, business programming

---

## Script

### INTRO (0:00–1:30)

Every Python script you will ever write stores data. A customer's name. A product price. A sales total. Whether an item is in stock. Before you can process data, filter it, calculate with it, or display it — you have to know how to hold it. That's what variables are for.

In this video we're going to build a complete product inventory record using Python's four core data types. By the end you'll know exactly what a variable is, why it matters which *type* your data is, and how to check and convert types when things don't line up. Let's get into VS Code.

---

### THE FOUR DATA TYPES (1:30–4:00)

Python has four types you need to know cold before anything else makes sense.

**str — string.** Text. Anything inside quotes. A product name, a customer email, a status message. It doesn't matter if the text looks like a number — if it's in quotes, Python treats it as text.

**int — integer.** Whole numbers. No decimal point. Quantity on hand: 42. Number of orders today: 150. Age of an account: 3.

**float — floating-point number.** Numbers with a decimal point. Price: 29.99. Tax rate: 0.08. Discount percentage: 0.15.

**bool — boolean.** True or False. In stock or not. Approved or not. Active customer or not. Booleans are the foundation of every decision your code makes.

Let's see all four in action.

---

### BUILDING A PRODUCT RECORD (4:00–7:30)

Open a new file in VS Code. We're going to model a single product — let's say a laptop bag sold by a campus bookstore.

```python
# product_record.py

product_name     = "Executive Laptop Bag"   # str
product_price    = 49.99                    # float
quantity_on_hand = 12                       # int
is_in_stock      = True                     # bool
```

Run it. Nothing prints yet — we've just stored the data. Let's display it.

```python
print(product_name)
print(product_price)
print(quantity_on_hand)
print(is_in_stock)
```

Output:
```
Executive Laptop Bag
49.99
12
True
```

Notice Python prints each value without the quotes. The quotes in your code tell Python the *type* — they're not part of the value itself.

Now let's calculate something useful. How much is all the inventory worth?

```python
inventory_value = product_price * quantity_on_hand
print(inventory_value)
```

Output: `599.88`

Two different types — float times int — and Python handles it automatically, returning a float. This is called implicit type conversion and it works in your favor here.

---

### CHECKING TYPES WITH type() (7:30–9:30)

Python gives you a built-in tool to inspect what type any value is: `type()`.

```python
print(type(product_name))       # <class 'str'>
print(type(product_price))      # <class 'float'>
print(type(quantity_on_hand))   # <class 'int'>
print(type(is_in_stock))        # <class 'bool'>
```

This is useful when something isn't behaving the way you expect. If a calculation is giving you a weird result, check the types of your inputs first.

Here's a classic trap. Suppose you read the price from a user prompt:

```python
user_price = input("Enter price: ")
print(type(user_price))   # <class 'str'>
```

`input()` *always* returns a string — even if the user types a number. If you try to multiply a string by an integer, Python will throw a TypeError.

---

### TYPE CONVERSION (9:30–12:00)

This is where `int()`, `float()`, and `str()` come in. They convert values from one type to another.

```python
user_price = input("Enter price: ")   # returns "49.99" as a string
price_as_float = float(user_price)    # now it's 49.99 as a float

quantity = int(input("Enter quantity: "))   # convert immediately on input
total = price_as_float * quantity
print(f"Total value: {total}")
```

You can also go the other direction — convert a number to a string when you need to concatenate it with text:

```python
reorder_point = 5
message = "Reorder when quantity falls below " + str(reorder_point)
print(message)
```

Output: `Reorder when quantity falls below 5`

Without the `str()` call, Python throws a TypeError because you can't concatenate a string and an integer directly.

---

### COMMON ERRORS (12:00–14:00)

**TypeError: can only concatenate str (not "int") to str**

```python
# This breaks:
print("Quantity: " + quantity_on_hand)

# Fix it:
print("Quantity: " + str(quantity_on_hand))
# Or better — use an f-string:
print(f"Quantity: {quantity_on_hand}")
```

**NameError: name 'x' is not defined**

```python
# This breaks — variable name is misspelled:
print(product_nmae)

# Fix it — check spelling:
print(product_name)
```

Python variable names are case-sensitive. `product_name` and `Product_Name` are two completely different variables.

**ValueError: could not convert string to float**

```python
# This breaks — "twelve" is not a number:
quantity = float("twelve")

# Fix it — only convert strings that actually contain numbers:
quantity = float("12")
```

---

### RECAP (14:00–15:00)

Here's what we covered:

- Python's four core types: **str**, **int**, **float**, **bool**
- Variables store values and you access them by name
- `type()` tells you what type any value is
- `input()` always returns a string — convert it before doing math
- `int()`, `float()`, `str()` convert between types
- f-strings are the cleanest way to mix variables into printed output

In the next video we'll take these values and start doing real business math with operators — calculating order totals, applying discounts, and checking approval thresholds. See you there.
