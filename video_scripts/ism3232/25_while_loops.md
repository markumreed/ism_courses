# Video 25: While Loops & the Accumulator Pattern

## YouTube Metadata

**Title:** Python While Loops & Accumulators for Business Logic | ISM3232
**Description:**
While loops repeat as long as a condition is true — essential for validation, retry logic, menus, and processing streams of indefinite length. In this video we build an order input loop with validation, a menu-driven interface, and a business accumulator using while — with careful attention to avoiding infinite loops.

**Chapters:**
0:00 — When while beats for
1:30 — while loop syntax
3:30 — Infinite loop danger and break
6:00 — Input validation loop
8:30 — Menu-driven interface
11:30 — continue — skip an iteration
13:00 — while with accumulators
14:30 — Recap

**Applies to:** ISM3232 Module 6

**Tags:** python while loop, python while, python break continue, python input validation, python menu loop, python accumulator, ISM3232, python control flow, python tutorial

---

## Script

### INTRO (0:00–1:30)

A `for` loop iterates over a known collection — a list, a range, rows in a file. But sometimes you don't know in advance how many times you need to repeat. An order input screen that keeps asking for items until the user says "done." A validation check that keeps prompting until the input is valid. A server that keeps listening until it receives a shutdown signal.

That's the use case for `while`. It repeats as long as a condition is true — potentially forever if you're not careful. Let's learn it properly.

---

### SYNTAX (1:30–3:30)

```python
while condition:
    # body — runs as long as condition is True
```

A simple countdown:

```python
count = 5

while count > 0:
    print(f"T-minus {count}...")
    count -= 1

print("Launch!")
```

Output:
```
T-minus 5...
T-minus 4...
T-minus 3...
T-minus 2...
T-minus 1...
Launch!
```

Each iteration decrements `count` by 1. When `count` hits 0, the condition `count > 0` is False — the loop ends.

The key difference from `for`: you control when the loop ends by managing the condition yourself. This is more flexible and more dangerous.

---

### INFINITE LOOP DANGER (3:30–6:00)

```python
# THIS WILL RUN FOREVER — don't run it:
count = 5
while count > 0:
    print(count)
    # forgot to decrement count — condition never becomes False!
```

If you accidentally create an infinite loop in VS Code's terminal, press **Ctrl+C** to interrupt it.

The three causes of infinite loops:
1. Forgetting to update the loop variable
2. Updating it in the wrong direction
3. Updating it only under a condition that never triggers

Always ask: "What makes this condition become False, and will that actually happen?"

**`break`** — exit the loop immediately, regardless of the condition:

```python
while True:    # deliberate infinite loop — common pattern
    user_input = input("Type 'quit' to exit: ")
    if user_input.lower() == "quit":
        print("Goodbye.")
        break
    print(f"You typed: {user_input}")
```

`while True` with `break` is idiomatic Python for "keep going until an explicit exit condition."

---

### INPUT VALIDATION (6:00–8:30)

The most common real-world `while` use case: keep prompting until the user gives valid input.

```python
def get_positive_number(prompt):
    while True:
        raw = input(prompt)
        try:
            value = float(raw)
            if value <= 0:
                print("Please enter a positive number.")
                continue    # skip to next iteration
            return value    # valid — exit the function (and the loop)
        except ValueError:
            print(f"'{raw}' is not a valid number. Try again.")

price    = get_positive_number("Enter unit price: $")
quantity = get_positive_number("Enter quantity: ")
total    = price * quantity

print(f"\nOrder total: ${total:.2f}")
```

If the user types "abc", `float("abc")` raises a `ValueError` — we catch it and loop again. If they type -5, it's a float but not positive — we `continue`. Only a positive number returns successfully.

---

### MENU-DRIVEN INTERFACE (8:30–11:30)

```python
inventory = {
    "Laptop Bag":      {"price": 49.99, "qty": 12},
    "USB-C Hub":       {"price": 24.99, "qty": 30},
    "Wireless Mouse":  {"price": 39.99, "qty": 18},
    "Monitor Stand":   {"price": 35.99, "qty": 7},
}

def show_menu():
    print("\n=== Campus Bookstore Inventory ===")
    print("1. View all items")
    print("2. Check item price")
    print("3. Update quantity")
    print("4. Quit")

while True:
    show_menu()
    choice = input("\nSelect option (1-4): ").strip()

    if choice == "1":
        print("\nItem                 Price    Qty")
        print("-" * 35)
        for name, info in inventory.items():
            print(f"{name:<20} ${info['price']:.2f}    {info['qty']}")

    elif choice == "2":
        name = input("Item name: ").strip()
        if name in inventory:
            print(f"{name}: ${inventory[name]['price']:.2f}")
        else:
            print("Item not found.")

    elif choice == "3":
        name = input("Item name: ").strip()
        if name in inventory:
            new_qty = int(input(f"New quantity for {name}: "))
            inventory[name]["qty"] = new_qty
            print(f"Updated {name} quantity to {new_qty}.")
        else:
            print("Item not found.")

    elif choice == "4":
        print("Closing inventory system.")
        break

    else:
        print("Invalid option. Enter 1, 2, 3, or 4.")
```

This is the pattern for any interactive terminal application: `while True` loop, menu display, input capture, conditional dispatch, `break` to exit.

---

### continue (11:30–13:00)

`continue` skips the rest of the current iteration and goes back to the condition check.

```python
sales = [142.50, -5.00, 89.99, 0, 312.00, -10.00, 203.80]
total = 0
skipped = 0

for sale in sales:
    if sale <= 0:
        skipped += 1
        continue    # skip negative or zero values
    total += sale

print(f"Valid sales total: ${total:.2f}")
print(f"Skipped {skipped} invalid entries.")
```

Output:
```
Valid sales total: $748.29
Skipped 3 invalid entries.
```

`continue` is cleaner than wrapping the body in an `if`/`else` for simple skip conditions.

---

### while WITH ACCUMULATOR (13:00–14:30)

```python
total    = 0
count    = 0
MAX_ITEMS = 10

print("Enter order items (press Enter with no price to finish):")

while count < MAX_ITEMS:
    raw = input(f"Item {count + 1} price (or Enter to finish): $").strip()

    if raw == "":
        break

    try:
        price = float(raw)
        if price <= 0:
            print("Price must be positive.")
            continue
        total += price
        count += 1
        print(f"  Running total: ${total:.2f}")
    except ValueError:
        print("Invalid number. Try again.")

print(f"\nOrder complete: {count} items, total ${total:.2f}")
```

This combines `while`, `break`, `continue`, input validation, and the accumulator pattern into a realistic order-entry interface.

---

### RECAP (14:30–15:00)

- `while condition:` — repeat until condition is False
- Always ensure the condition can become False — or use `break`
- `while True:` + `break` — deliberate loop until explicit exit
- `continue` — skip current iteration, back to condition
- Input validation pattern: `while True` + `try/except` + `return` or `break`
- Menu pattern: `while True` + display menu + read input + dispatch + `break` on quit
- Ctrl+C kills a runaway loop in the terminal

Next module: functions, modules, and pytest — organizing and testing business logic.
