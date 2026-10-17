# database.py
# Author: [Your Name]

import sqlite3


def query_all(db_file, sql, values=()):
    """Run a SELECT and return every row as a dictionary."""
    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(sql, values).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def query_one(db_file, sql, values=()):
    """Run a SELECT and return the first row as a dictionary, or None."""
    rows = query_all(db_file, sql, values)
    if rows == []:
        return None
    return rows[0]


def change(db_file, sql, values=()):
    """Run an INSERT or UPDATE, save it, and return the ID of the last row inserted."""
    conn = sqlite3.connect(db_file)
    cursor = conn.execute(sql, values)
    conn.commit()
    row_id = cursor.lastrowid
    conn.close()
    return row_id


def create_tables(db_file):
    """Create the tables and the sample rows, unless they are already there."""
    with open("schema.sql") as f:
        script = f.read()
    conn = sqlite3.connect(db_file)
    conn.executescript(script)
    conn.commit()
    conn.close()


def reset_database(db_file):
    """Delete all three tables, then build them again from schema.sql."""
    conn = sqlite3.connect(db_file)
    conn.execute("DROP TABLE IF EXISTS change_requests")
    conn.execute("DROP TABLE IF EXISTS products")
    conn.execute("DROP TABLE IF EXISTS orders")
    conn.commit()
    conn.close()
    create_tables(db_file)


def find_order(db_file, order_id):
    """Return one order, or None if there is no order with exactly this ID."""
    return query_one(db_file, "SELECT * FROM orders WHERE order_id = ?", (order_id,))


def all_orders(db_file):
    """Return every order, by order ID."""
    return query_all(db_file, "SELECT * FROM orders ORDER BY order_id")


def product_names(db_file):
    """Return the name of every product."""
    rows = query_all(db_file, "SELECT name FROM products ORDER BY name")
    return [row["name"] for row in rows]


def find_product(db_file, name):
    """Return one product, or None if there is no product with this name."""
    return query_one(db_file, "SELECT * FROM products WHERE name = ?", (name,))


def add_change_request(db_file, order_id, new_address):
    """File a new address change. It waits for staff. Return its number."""
    sql = "INSERT INTO change_requests (order_id, new_address) VALUES (?, ?)"
    return change(db_file, sql, (order_id, new_address))


def find_request(db_file, number):
    """Return one change request, or None if there is no request with this number."""
    return query_one(
        db_file, "SELECT * FROM change_requests WHERE number = ?", (number,)
    )


def waiting_requests(db_file):
    """Return the requests still waiting for staff, oldest first."""
    sql = "SELECT * FROM change_requests WHERE status = 'waiting' ORDER BY number"
    return query_all(db_file, sql)


def approve_request(db_file, number):
    """Approve one waiting request: change the order's address and mark it approved."""
    request = find_request(db_file, number)
    if request is None:
        return f"There is no request {number}."
    if request["status"] != "waiting":
        return f"Request {number} is already {request['status']}."
    conn = sqlite3.connect(db_file)
    conn.execute(
        "UPDATE orders SET address = ? WHERE order_id = ?",
        (request["new_address"], request["order_id"]),
    )
    conn.execute(
        "UPDATE change_requests SET status = 'approved' WHERE number = ?", (number,)
    )
    conn.commit()
    conn.close()
    return f"Request {number} approved."


def reject_request(db_file, number):
    """Reject one waiting request. The order does not change."""
    request = find_request(db_file, number)
    if request is None:
        return f"There is no request {number}."
    if request["status"] != "waiting":
        return f"Request {number} is already {request['status']}."
    sql = "UPDATE change_requests SET status = 'rejected' WHERE number = ?"
    change(db_file, sql, (number,))
    return f"Request {number} rejected."


def restock(db_file, name, stock):
    """Set how many of one product are in stock."""
    change(db_file, "UPDATE products SET stock = ? WHERE name = ?", (stock, name))


def status_report(db_file):
    """Return how many orders have each status."""
    sql = (
        "SELECT status, COUNT(*) AS orders FROM orders GROUP BY status ORDER BY status"
    )
    return query_all(db_file, sql)
