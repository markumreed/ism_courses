# Video 31: Python + SQL Integration with sqlite3

## YouTube Metadata

**Title:** Python + SQLite Integration — sqlite3, database.py & pytest | ISM3232
**Description:**
Connect your Python classes to a SQLite database using the built-in sqlite3 module. In this video we build the five required database functions for ISM3232 capstone projects: create_table, insert, get_all, get_by_id, and update — with parameterized queries to prevent SQL injection, and tests using pytest's tmp_path fixture.

**Chapters:**
0:00 — The database layer architecture
2:00 — Connecting with sqlite3
4:00 — The five required functions
7:00 — Parameterized queries — never use f-strings in SQL
12:00 — Testing with tmp_path
15:30 — Putting it together with your OOP classes
18:00 — Recap

**Applies to:** ISM3232 Module 14

**Tags:** python sqlite3, sqlite3 tutorial, python database, python sql integration, sqlite3 parameterized, sql injection prevention, pytest tmp_path, ISM3232, python capstone database, python database functions

---

## Script

### INTRO (0:00–2:00)

In Module 13 you learned SQL. In Module 10-12 you built Python classes. Now we wire them together. The `sqlite3` module is the bridge: it lets Python open a database file, run SQL queries, and process the results.

Your capstone requires five database functions in a `database.py` file. We'll build all five, protect them against SQL injection with parameterized queries, and test them with pytest's `tmp_path` fixture so every test uses a fresh isolated database.

---

### THE ARCHITECTURE (0:00–2:00, continued)

```
main.py / app.py          ← entry point, UI
    │
    ▼
database.py               ← the five required functions
    │
    ▼
SQLite .db file           ← persistent storage
```

`database.py` is your data access layer. Your UI code (Streamlit, CLI) calls `database.py` functions. `database.py` talks to SQLite. Your OOP classes hold the business logic. This separation makes testing and swapping databases easy.

---

### CONNECTING WITH sqlite3 (2:00–4:00)

```python
import sqlite3

# Connect — creates the file if it doesn't exist:
conn = sqlite3.connect("capstone.db")

# Always set row_factory so rows come back as dicts:
conn.row_factory = sqlite3.Row

# Get a cursor — the object that runs queries:
cursor = conn.cursor()

# Run a query:
cursor.execute("SELECT * FROM products")

# Fetch results:
rows = cursor.fetchall()
for row in rows:
    print(dict(row))

# Commit changes (required for INSERT, UPDATE, DELETE):
conn.commit()

# Close when done:
conn.close()
```

`sqlite3.Row` — without this, rows come back as plain tuples and you access columns by index (`row[0]`). With `row_factory = sqlite3.Row`, rows behave like dicts: `row["name"]`, `row["price"]`. Always set this.

The `with` statement handles commit + close automatically:

```python
with sqlite3.connect("capstone.db") as conn:
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
# conn is committed and closed here
```

---

### THE FIVE REQUIRED FUNCTIONS (4:00–7:00)

```python
# database.py

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "capstone.db"

def get_connection(db_path: Path = DB_PATH) -> sqlite3.Connection:
    """Create and return a database connection."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")   # enforce foreign key constraints
    return conn

def create_tables(db_path: Path = DB_PATH) -> None:
    """Create all required tables if they don't exist."""
    with get_connection(db_path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT    NOT NULL,
                category    TEXT    NOT NULL,
                price       REAL    NOT NULL CHECK (price > 0),
                quantity    INTEGER NOT NULL DEFAULT 0,
                is_active   INTEGER NOT NULL DEFAULT 1
            )
        """)

def insert_product(name: str, category: str, price: float,
                   quantity: int = 0, db_path: Path = DB_PATH) -> int:
    """Insert a product. Returns the new row's id."""
    with get_connection(db_path) as conn:
        cursor = conn.execute(
            "INSERT INTO products (name, category, price, quantity) VALUES (?, ?, ?, ?)",
            (name, category, price, quantity)
        )
        return cursor.lastrowid

def get_all_products(db_path: Path = DB_PATH) -> list[dict]:
    """Return all active products as a list of dicts."""
    with get_connection(db_path) as conn:
        rows = conn.execute(
            "SELECT * FROM products WHERE is_active = 1 ORDER BY name"
        ).fetchall()
        return [dict(row) for row in rows]

def get_product_by_id(product_id: int, db_path: Path = DB_PATH) -> dict | None:
    """Return one product by id, or None if not found."""
    with get_connection(db_path) as conn:
        row = conn.execute(
            "SELECT * FROM products WHERE id = ?",
            (product_id,)
        ).fetchone()
        return dict(row) if row else None

def update_product_price(product_id: int, new_price: float,
                          db_path: Path = DB_PATH) -> bool:
    """Update price for a product. Returns True if a row was updated."""
    if new_price <= 0:
        raise ValueError("Price must be positive.")
    with get_connection(db_path) as conn:
        cursor = conn.execute(
            "UPDATE products SET price = ? WHERE id = ?",
            (new_price, product_id)
        )
        return cursor.rowcount > 0

def delete_product(product_id: int, db_path: Path = DB_PATH) -> bool:
    """Soft-delete: mark product inactive. Returns True if updated."""
    with get_connection(db_path) as conn:
        cursor = conn.execute(
            "UPDATE products SET is_active = 0 WHERE id = ?",
            (product_id,)
        )
        return cursor.rowcount > 0
```

---

### PARAMETERIZED QUERIES (7:00–12:00)

This is the most important security concept in database programming.

**Never, ever do this:**

```python
# DANGEROUS — SQL injection vulnerability:
name = input("Product name: ")
conn.execute(f"SELECT * FROM products WHERE name = '{name}'")
```

If the user types `'; DROP TABLE products; --`, the query becomes:
```sql
SELECT * FROM products WHERE name = ''; DROP TABLE products; --'
```

Your entire products table is deleted.

**Always use parameterized queries:**

```python
# SAFE — parameterized:
name = input("Product name: ")
conn.execute("SELECT * FROM products WHERE name = ?", (name,))
```

The `?` is a placeholder. The second argument is a tuple of values. SQLite treats the value as data, not as SQL — no injection possible. The attacker's `'; DROP TABLE` becomes a literal string that won't match any product name.

**Note the tuple syntax:** `(name,)` — single-element tuple requires the trailing comma. `(name)` is just parentheses around `name`, not a tuple.

```python
# Multiple parameters:
conn.execute(
    "SELECT * FROM products WHERE category = ? AND price < ?",
    (category, max_price)   # tuple, no trailing comma needed for multiple elements
)

# Named parameters (alternative style):
conn.execute(
    "INSERT INTO products (name, price) VALUES (:name, :price)",
    {"name": "Laptop Bag", "price": 49.99}
)
```

Use parameterized queries for every query that includes user input or variable data. No exceptions.

---

### TESTING WITH tmp_path (12:00–15:30)

`tmp_path` is a pytest built-in fixture that creates a temporary directory unique to each test — automatically cleaned up after the test runs. Use it to give each test its own fresh database.

```python
# tests/test_database.py

import pytest
from pathlib import Path
from database import create_tables, insert_product, get_all_products, \
                     get_product_by_id, update_product_price, delete_product

@pytest.fixture
def db(tmp_path):
    """Create a fresh test database for each test."""
    db_path = tmp_path / "test_capstone.db"
    create_tables(db_path)
    return db_path

# 1. Happy path — insert and retrieve
def test_insert_and_retrieve(db):
    pid = insert_product("Laptop Bag", "Electronics", 49.99, 12, db)
    assert pid == 1

    product = get_product_by_id(1, db)
    assert product is not None
    assert product["name"]  == "Laptop Bag"
    assert product["price"] == 49.99

# 2. Get all returns list
def test_get_all_products(db):
    insert_product("Laptop Bag",  "Electronics", 49.99, db_path=db)
    insert_product("USB-C Hub",   "Electronics", 24.99, db_path=db)
    insert_product("Desk Chair",  "Furniture",  249.99, db_path=db)
    products = get_all_products(db)
    assert len(products) == 3
    assert isinstance(products, list)
    assert isinstance(products[0], dict)

# 3. Update price
def test_update_price(db):
    pid = insert_product("Laptop Bag", "Electronics", 49.99, db_path=db)
    result = update_product_price(pid, 54.99, db)
    assert result is True
    updated = get_product_by_id(pid, db)
    assert updated["price"] == 54.99

# 4. Soft delete
def test_delete_product(db):
    pid = insert_product("Laptop Bag", "Electronics", 49.99, db_path=db)
    assert delete_product(pid, db) is True
    products = get_all_products(db)
    assert len(products) == 0   # soft-deleted, not returned by get_all

# 5. Missing product returns None
def test_get_nonexistent_product(db):
    result = get_product_by_id(999, db)
    assert result is None

# 6. Invalid price raises ValueError
def test_invalid_price_raises(db):
    pid = insert_product("Test", "Cat", 10.0, db_path=db)
    with pytest.raises(ValueError):
        update_product_price(pid, -5.0, db)

# 7. Return types
def test_return_types(db):
    pid = insert_product("Laptop Bag", "Electronics", 49.99, db_path=db)
    assert isinstance(pid, int)
    products = get_all_products(db)
    assert isinstance(products, list)
    product = get_product_by_id(pid, db)
    assert isinstance(product, dict)
```

Run:
```bash
pytest tests/test_database.py -v
```

Every test gets its own fresh database — no test can affect another.

---

### WIRING TO OOP CLASSES (15:30–18:00)

```python
# In main.py or wherever you use both:
from product import Product   # your OOP class
from database import insert_product, get_all_products

# Convert an OOP object to database row:
def save_product(product: Product, db_path) -> int:
    return insert_product(
        name=product.name,
        category=product.category,
        price=product.price,
        quantity=product.quantity,
        db_path=db_path
    )

# Load database rows back into OOP objects:
def load_all_products(db_path) -> list[Product]:
    rows = get_all_products(db_path)
    return [Product(r["name"], r["category"], r["price"], r["quantity"]) for r in rows]
```

Your OOP objects hold business logic. Your database functions handle persistence. They stay separate and talk through these thin adapter functions.

---

### RECAP (18:00–20:00)

- `sqlite3.connect("file.db")` — open or create a database file
- `conn.row_factory = sqlite3.Row` — rows come back as dict-like objects
- `PRAGMA foreign_keys = ON` — enforce foreign key constraints
- `cursor.execute(sql, (param, param))` — always parameterized
- `cursor.lastrowid` — id of the last inserted row
- `fetchone()` — one row or None; `fetchall()` — list of all rows
- `cursor.rowcount` — number of rows affected by UPDATE/DELETE
- **Never use f-strings in SQL** — always use `?` placeholders
- `tmp_path` pytest fixture — fresh isolated database per test
- OOP objects ↔ database rows through thin adapter functions

Module 15: Streamlit — building a five-feature business interface.
