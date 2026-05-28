# Video 30: SQL Foundations for Business Apps

## YouTube Metadata

**Title:** SQL Foundations for Business Apps — CREATE, INSERT, SELECT, WHERE, JOIN | ISM3232
**Description:**
SQL is the language of every business database. In this video you'll learn the five operations your ISM3232 capstone database must support: CREATE TABLE, INSERT, SELECT with WHERE, UPDATE, and DELETE — all through a product inventory scenario. We also cover JOIN for combining tables and schema design principles.

**Chapters:**
0:00 — What SQL is and where it fits in your capstone
1:30 — SQLite — the database you'll use
3:00 — CREATE TABLE — define your schema
6:00 — INSERT — add records
8:00 — SELECT and WHERE — query records
11:00 — UPDATE and DELETE
13:00 — JOIN — combining tables
16:00 — Schema design: choosing types and constraints
18:00 — Recap

**Applies to:** ISM3232 Module 13

**Tags:** SQL tutorial, SQLite, SQL CREATE TABLE, SQL SELECT WHERE, SQL JOIN, SQL for beginners, ISM3232, python database, SQL business, sqlite3 python, database design

---

## Script

### INTRO (0:00–1:30)

Your ISM3232 capstone is a full-stack business application. Data goes in, data gets stored, data comes back. That storage layer is a database, and the language you use to talk to it is SQL — Structured Query Language. SQL has been the standard for 50 years and is used by every business application from corner-shop spreadsheets to Fortune 500 ERPs.

In this module we learn the five SQL operations your capstone requires, using SQLite — the lightweight database that ships with Python. No server to install, no configuration. One file, full SQL.

---

### SQLite (1:30–3:00)

SQLite stores an entire database in a single `.db` file. It's built into Python via the `sqlite3` module — no pip install needed. It supports full SQL, handles up to several GB of data, and is used in production by countless applications including Firefox, iOS, and Android.

For your capstone, SQLite is the right choice. When you're ready to scale, the SQL you learned here transfers directly to PostgreSQL or MySQL.

Open an SQLite shell to try queries interactively:

```bash
sqlite3 capstone.db
```

You'll see:
```
SQLite version 3.43.2
Enter ".help" for usage hints.
sqlite>
```

Type `.quit` to exit. We'll use the shell to learn SQL syntax, then use Python's `sqlite3` module to run queries from code.

---

### CREATE TABLE (3:00–6:00)

`CREATE TABLE` defines the structure of a table — the columns and their types.

```sql
CREATE TABLE IF NOT EXISTS products (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT    NOT NULL,
    category    TEXT    NOT NULL,
    price       REAL    NOT NULL CHECK (price > 0),
    quantity    INTEGER NOT NULL DEFAULT 0,
    is_active   INTEGER NOT NULL DEFAULT 1
);
```

Breaking it down:

- `IF NOT EXISTS` — don't error if the table already exists
- `id INTEGER PRIMARY KEY AUTOINCREMENT` — unique row identifier, auto-incremented
- `TEXT NOT NULL` — text field, required (no empty values)
- `REAL` — floating-point number (SQLite's float type)
- `CHECK (price > 0)` — constraint: price must be positive
- `DEFAULT 0` — default value when not specified
- SQLite stores booleans as `INTEGER` (0 = False, 1 = True)

SQLite's four type affinities:
- `INTEGER` — whole numbers
- `REAL` — floating-point
- `TEXT` — strings
- `BLOB` — binary data

```sql
CREATE TABLE IF NOT EXISTS categories (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    name    TEXT NOT NULL UNIQUE,
    slug    TEXT NOT NULL UNIQUE
);
```

`UNIQUE` — no two rows can have the same value in this column.

---

### INSERT (6:00–8:00)

`INSERT INTO` adds a new row to a table.

```sql
INSERT INTO categories (name, slug) VALUES ('Electronics', 'electronics');
INSERT INTO categories (name, slug) VALUES ('Office Supplies', 'office-supplies');
INSERT INTO categories (name, slug) VALUES ('Furniture', 'furniture');

INSERT INTO products (name, category, price, quantity) VALUES
    ('Laptop Bag',     'Electronics',     49.99, 12),
    ('USB-C Hub',      'Electronics',     24.99, 30),
    ('Wireless Mouse', 'Electronics',     39.99, 18),
    ('Monitor Stand',  'Office Supplies', 35.99,  7),
    ('Desk Chair',     'Furniture',      249.99,  3);
```

The `id` column is omitted — `AUTOINCREMENT` fills it automatically. The `is_active` column is omitted — it uses its default value of 1.

---

### SELECT AND WHERE (8:00–11:00)

`SELECT` retrieves rows. `*` means all columns.

```sql
-- All products:
SELECT * FROM products;

-- Specific columns:
SELECT name, price, quantity FROM products;

-- Filtered by condition:
SELECT name, price FROM products WHERE price < 50;

-- Multiple conditions:
SELECT name, price FROM products
WHERE price < 50 AND quantity > 10;

-- Pattern matching with LIKE:
SELECT name FROM products WHERE name LIKE '%Laptop%';

-- Sort results:
SELECT name, price FROM products ORDER BY price DESC;

-- Limit results:
SELECT name, price FROM products ORDER BY price DESC LIMIT 3;

-- Aggregate functions:
SELECT COUNT(*) AS total_products   FROM products;
SELECT AVG(price) AS avg_price      FROM products WHERE is_active = 1;
SELECT SUM(quantity) AS total_stock FROM products;
SELECT MIN(price) AS cheapest       FROM products;
SELECT MAX(price) AS most_expensive FROM products;
```

---

### UPDATE AND DELETE (11:00–13:00)

`UPDATE` modifies existing rows.

```sql
-- Update price for one product:
UPDATE products SET price = 44.99 WHERE name = 'Laptop Bag';

-- Update multiple columns:
UPDATE products
SET price = 27.99, quantity = 25
WHERE name = 'USB-C Hub';

-- Mark all furniture as inactive:
UPDATE products SET is_active = 0 WHERE category = 'Furniture';
```

**Always use WHERE with UPDATE and DELETE.** Without `WHERE`, you update or delete every row.

```sql
-- Delete a specific row:
DELETE FROM products WHERE name = 'Monitor Stand';

-- Delete all inactive products:
DELETE FROM products WHERE is_active = 0;
```

---

### JOIN (13:00–16:00)

`JOIN` combines rows from two tables based on a related column.

Restructure: add a `category_id` foreign key to products:

```sql
CREATE TABLE products_v2 (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT    NOT NULL,
    category_id INTEGER NOT NULL REFERENCES categories(id),
    price       REAL    NOT NULL,
    quantity    INTEGER NOT NULL DEFAULT 0
);

INSERT INTO products_v2 (name, category_id, price, quantity) VALUES
    ('Laptop Bag',     1, 49.99, 12),
    ('USB-C Hub',      1, 24.99, 30),
    ('Monitor Stand',  2, 35.99,  7),
    ('Desk Chair',     3, 249.99, 3);
```

`INNER JOIN` — returns rows where both tables have a match:

```sql
SELECT
    p.name        AS product,
    c.name        AS category,
    p.price,
    p.quantity
FROM products_v2 p
INNER JOIN categories c ON p.category_id = c.id
ORDER BY c.name, p.name;
```

Output:
```
product        category          price    quantity
Laptop Bag     Electronics       49.99    12
USB-C Hub      Electronics       24.99    30
Monitor Stand  Office Supplies   35.99     7
Desk Chair     Furniture         249.99    3
```

`GROUP BY` with `JOIN` — total stock value by category:

```sql
SELECT
    c.name                        AS category,
    COUNT(p.id)                   AS product_count,
    SUM(p.price * p.quantity)     AS total_value
FROM products_v2 p
INNER JOIN categories c ON p.category_id = c.id
GROUP BY c.id
ORDER BY total_value DESC;
```

---

### SCHEMA DESIGN (16:00–18:00)

For your capstone, design before you create.

**Rules:**
1. One table per entity (class). `products`, `customers`, `orders`, `order_items`.
2. Every table needs a primary key (`id INTEGER PRIMARY KEY AUTOINCREMENT`).
3. Relationships use foreign keys (`customer_id INTEGER REFERENCES customers(id)`).
4. Store booleans as `INTEGER` (0/1). Store dates as `TEXT` in ISO format (`'2024-05-28'`).
5. Add `NOT NULL` to required fields. Add `DEFAULT` where it makes sense.
6. Add `CHECK` constraints for business rules (`CHECK (price > 0)`).

Your capstone schema should have at minimum 2 tables with a foreign key relationship between them.

---

### RECAP (18:00–20:00)

- SQLite is file-based, zero-config, built into Python
- `CREATE TABLE IF NOT EXISTS` — define columns, types, constraints
- `INSERT INTO ... VALUES` — add rows
- `SELECT ... FROM ... WHERE` — query rows with conditions
- `UPDATE ... SET ... WHERE` — modify rows (always use WHERE!)
- `DELETE FROM ... WHERE` — remove rows (always use WHERE!)
- `JOIN ... ON` — combine tables on a related column
- `GROUP BY` + aggregates — summary statistics per group
- Design your schema before creating tables — one table per entity, foreign keys for relationships

Module 14: Python + SQL integration — connecting your classes to SQLite using sqlite3.
