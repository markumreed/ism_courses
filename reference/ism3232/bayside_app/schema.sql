-- schema.sql
-- Bayside Outfitters: orders, products, and changes waiting for staff.

CREATE TABLE IF NOT EXISTS orders (
    order_id TEXT PRIMARY KEY,
    customer TEXT NOT NULL,
    item     TEXT NOT NULL,
    status   TEXT NOT NULL,
    address  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS products (
    name  TEXT PRIMARY KEY,
    price REAL NOT NULL,
    stock INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS change_requests (
    number      INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id    TEXT NOT NULL,
    new_address TEXT NOT NULL,
    status      TEXT NOT NULL DEFAULT 'waiting'
);

INSERT OR IGNORE INTO orders (order_id, customer, item, status, address) VALUES
    ('A100', 'Dana Cruz', 'rain jacket', 'shipped', '14 Bay Road'),
    ('A101', 'Sam Okafor', 'day pack', 'processing', '3 Gull Lane'),
    ('A102', 'Lee Park', 'trail hat', 'delivered', '88 Pier Street'),
    ('A103', 'Ana Silva', 'fleece vest', 'processing', '21 Harbor Way'),
    ('A104', 'Max Duarte', 'water bottle', 'shipped', '7 Dune Court'),
    ('A105', 'Ivy Chen', 'hiking socks', 'delivered', '40 Tide Street');

INSERT OR IGNORE INTO products (name, price, stock) VALUES
    ('rain jacket', 89.00, 12),
    ('day pack', 45.00, 0),
    ('trail hat', 25.00, 5),
    ('fleece vest', 60.00, 8),
    ('water bottle', 18.00, 30),
    ('hiking socks', 12.00, 0);
