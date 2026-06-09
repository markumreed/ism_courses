# Video 32: Streamlit — Building a Business Interface

## YouTube Metadata

**Title:** Streamlit Business App — Build 5 Required Features | ISM3232
**Description:**
Streamlit turns Python scripts into web applications with no HTML, CSS, or JavaScript. In this video we build the five features every ISM3232 capstone Streamlit app must have: view all records, add a record, update a record, delete/deactivate a record, and a summary dashboard — all wired to a SQLite database.

Course page: https://markumreed.github.io/ism3232/docs/week15_lecture.html

**Chapters:**
0:00 — What Streamlit is and how it executes
2:00 — Installing and running Streamlit
3:30 — The execution model — re-runs on every interaction
5:30 — Feature 1: View all records
7:30 — Feature 2: Add a record form
10:00 — Feature 3: Update a record
12:30 — Feature 4: Delete/deactivate
14:30 — Feature 5: Summary dashboard
17:00 — Session state
19:00 — Recap

**Applies to:** ISM3232 Module 15

**Tags:** streamlit tutorial, streamlit python, streamlit database, streamlit form, streamlit app, python web app, ISM3232, streamlit capstone, streamlit sqlite, python business app

---

## Script

### INTRO (0:00–2:00)

Streamlit is the reason your capstone is a working web application and not just a script. It takes your Python functions and turns them into an interactive UI — no frontend skills required. You write Python, Streamlit renders the interface.

The catch is that Streamlit has a unique execution model that confuses everyone the first time. This video explains that model clearly before we build anything. Understand the model — the rest is just writing functions.

---

### INSTALL AND RUN (2:00–3:30)

```bash
# In your project venv:
pip install streamlit
streamlit --version
```

Create `app.py`:

```python
import streamlit as st

st.title("Campus Bookstore Inventory")
st.write("Hello, Streamlit!")
```

Run:
```bash
streamlit run app.py
```

A browser tab opens at `http://localhost:8501`. Every time you save `app.py`, Streamlit reloads automatically.

---

### THE EXECUTION MODEL (3:30–5:30)

This is the most important concept in Streamlit. Read it twice.

**Streamlit re-runs your entire script from top to bottom every time the user interacts with any widget.**

Click a button — full re-run. Type in a text box — full re-run. Select from a dropdown — full re-run.

This means:
- Local variables reset every re-run (use `st.session_state` to persist)
- Any code at the module level runs every re-run
- The order of your code is the order of your UI

```python
import streamlit as st

name = st.text_input("Your name:")    # renders input box
                                       # on every re-run, name = whatever the user typed

if name:
    st.write(f"Hello, {name}!")        # only shows when name is not empty
```

Every interaction triggers a re-run. `st.text_input()` returns the current value of the text box — whatever the user has typed so far. If they haven't typed anything, it returns an empty string.

---

### PROJECT STRUCTURE (as needed)

```
module15_streamlit/
├── .venv/
├── app.py           ← Streamlit UI
├── database.py      ← your 5 database functions
├── models.py        ← your OOP classes (optional but good practice)
├── capstone.db      ← auto-created
├── requirements.txt
└── .gitignore
```

Import your database functions into `app.py`:

```python
import streamlit as st
from database import (create_tables, insert_product, get_all_products,
                      get_product_by_id, update_product_price, delete_product)
from pathlib import Path

DB = Path("capstone.db")
create_tables(DB)   # runs every re-run but IF NOT EXISTS makes it idempotent
```

---

### FEATURE 1: VIEW ALL RECORDS (5:30–7:30)

```python
st.header("📦 Product Inventory")

products = get_all_products(DB)

if not products:
    st.info("No products in inventory. Add one below.")
else:
    st.metric("Total Products", len(products))

    # Display as a table:
    import pandas as pd
    df = pd.DataFrame(products)
    df["price"] = df["price"].apply(lambda x: f"${x:.2f}")
    st.dataframe(df[["id", "name", "category", "price", "quantity"]], use_container_width=True)
```

`st.metric()` — displays a big number with a label. `st.dataframe()` — renders a DataFrame as an interactive table. `use_container_width=True` — stretches to full page width.

---

### FEATURE 2: ADD A RECORD (7:30–10:00)

```python
st.header("➕ Add New Product")

with st.form("add_product_form"):
    name     = st.text_input("Product Name")
    category = st.selectbox("Category", ["Electronics", "Office Supplies", "Furniture"])
    price    = st.number_input("Price ($)", min_value=0.01, step=0.01, format="%.2f")
    quantity = st.number_input("Quantity", min_value=0, step=1)
    submitted = st.form_submit_button("Add Product")

if submitted:
    if not name.strip():
        st.error("Product name is required.")
    else:
        pid = insert_product(name.strip(), category, price, quantity, DB)
        st.success(f"✅ Added '{name}' with ID {pid}.")
        st.rerun()   # re-run to refresh the product list
```

`st.form()` — groups widgets so the whole form submits at once (not on every keystroke). `st.form_submit_button()` — returns True when clicked. `st.rerun()` — triggers an immediate re-run to refresh state.

Input validation: check that required fields are filled before calling the database function.

---

### FEATURE 3: UPDATE A RECORD (10:00–12:30)

```python
st.header("✏️ Update Product Price")

products = get_all_products(DB)
if products:
    product_names = {p["name"]: p["id"] for p in products}

    with st.form("update_form"):
        selected_name = st.selectbox("Select Product", list(product_names.keys()))
        new_price     = st.number_input("New Price ($)", min_value=0.01, step=0.01, format="%.2f")
        submitted     = st.form_submit_button("Update Price")

    if submitted:
        pid     = product_names[selected_name]
        success = update_product_price(pid, new_price, DB)
        if success:
            st.success(f"✅ Updated price for '{selected_name}' to ${new_price:.2f}.")
            st.rerun()
        else:
            st.error("Update failed — product not found.")
else:
    st.info("No products to update.")
```

Build a dict of `{name: id}` from the product list. `st.selectbox()` displays names — use the dict to look up the id when the form submits.

---

### FEATURE 4: DELETE/DEACTIVATE (12:30–14:30)

```python
st.header("🗑️ Deactivate Product")

products = get_all_products(DB)
if products:
    product_names = {p["name"]: p["id"] for p in products}

    selected_name = st.selectbox("Select Product to Deactivate", list(product_names.keys()),
                                  key="delete_select")   # unique key prevents conflict with update selectbox

    col1, col2 = st.columns([1, 4])
    with col1:
        confirm = st.checkbox("I confirm")
    with col2:
        if st.button("Deactivate", disabled=not confirm):
            pid = product_names[selected_name]
            delete_product(pid, DB)
            st.success(f"'{selected_name}' deactivated.")
            st.rerun()
else:
    st.info("No products to deactivate.")
```

The `key=` parameter gives a widget a unique identifier — required when you have two `st.selectbox()` calls on the same page. The confirmation checkbox prevents accidental deletes.

---

### FEATURE 5: SUMMARY DASHBOARD (14:30–17:00)

```python
st.header("📊 Inventory Dashboard")

products = get_all_products(DB)

if products:
    import pandas as pd
    df = pd.DataFrame(products)
    df["total_value"] = df["price"] * df["quantity"]

    # Metrics row:
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Products",   len(df))
    col2.metric("Total Stock Value", f"${df['total_value'].sum():,.2f}")
    col3.metric("Avg Price",         f"${df['price'].mean():.2f}")

    # Bar chart by category:
    cat_summary = df.groupby("category")["total_value"].sum().reset_index()
    st.subheader("Stock Value by Category")
    st.bar_chart(cat_summary.set_index("category")["total_value"])

    # Low stock warning:
    low_stock = df[df["quantity"] < 5]
    if not low_stock.empty:
        st.warning(f"⚠️ {len(low_stock)} product(s) with low stock (< 5 units):")
        st.dataframe(low_stock[["name", "quantity"]], use_container_width=True)
else:
    st.info("Add products to see the dashboard.")
```

`st.columns(3)` — three equal-width columns side by side. `st.bar_chart()` — quick built-in chart from a Series or DataFrame. `st.warning()` — amber banner for important notices.

---

### SESSION STATE (17:00–19:00)

Variables reset every re-run. `st.session_state` persists across re-runs within the same browser session.

```python
# Track how many products were added this session:
if "added_count" not in st.session_state:
    st.session_state.added_count = 0

# In the form submission:
if submitted and name.strip():
    insert_product(name.strip(), category, price, quantity, DB)
    st.session_state.added_count += 1
    st.rerun()

st.sidebar.metric("Added this session", st.session_state.added_count)
```

Use `st.session_state` for: counters, selected items, multi-step form state, anything that must survive a re-run.

---

### RECAP (19:00–20:00)

- `streamlit run app.py` — launch the app
- Streamlit re-runs the entire script on every interaction
- Use `st.form()` to batch widget submissions
- `st.rerun()` — force a refresh after a database change
- Give multiple same-type widgets unique `key=` parameters
- `st.session_state` — persist values across re-runs
- The 5 required features: view all, add, update, delete, dashboard
- Always validate inputs before calling database functions

Module 16: GenAI feature and final demo.
