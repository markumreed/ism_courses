import database


def make_db(tmp_path):
    """Create a fresh database with the sample rows, in a folder only this test uses."""
    db_file = tmp_path / "test.db"
    database.create_tables(db_file)
    return db_file


def test_create_tables_twice_adds_no_duplicate_rows(tmp_path):
    db_file = make_db(tmp_path)
    database.create_tables(db_file)
    assert len(database.all_orders(db_file)) == 6
    assert len(database.product_names(db_file)) == 6


def test_find_order_returns_a_dictionary(tmp_path):
    db_file = make_db(tmp_path)
    order = database.find_order(db_file, "A100")
    assert order["status"] == "shipped"
    assert order["address"] == "14 Bay Road"


def test_find_order_needs_the_exact_id(tmp_path):
    db_file = make_db(tmp_path)
    assert database.find_order(db_file, "A1000") is None
    assert database.find_order(db_file, "a100") is None


def test_sql_in_an_order_id_is_just_text(tmp_path):
    db_file = make_db(tmp_path)
    assert database.find_order(db_file, "A100'; DROP TABLE orders;--") is None
    assert len(database.all_orders(db_file)) == 6


def test_find_product(tmp_path):
    db_file = make_db(tmp_path)
    assert database.find_product(db_file, "day pack")["stock"] == 0
    assert database.find_product(db_file, "tent") is None


def test_change_requests_get_numbers_and_wait(tmp_path):
    db_file = make_db(tmp_path)
    first = database.add_change_request(db_file, "A100", "9 Pine Street")
    second = database.add_change_request(db_file, "A101", "5 Elm Street")
    assert (first, second) == (1, 2)
    assert len(database.waiting_requests(db_file)) == 2
    assert database.find_order(db_file, "A100")["address"] == "14 Bay Road"


def test_approve_changes_the_address_once(tmp_path):
    db_file = make_db(tmp_path)
    database.add_change_request(db_file, "A100", "9 Pine Street")
    assert database.approve_request(db_file, 1) == "Request 1 approved."
    assert database.find_order(db_file, "A100")["address"] == "9 Pine Street"
    assert database.approve_request(db_file, 1) == "Request 1 is already approved."
    assert database.waiting_requests(db_file) == []


def test_reject_changes_nothing_and_cannot_be_approved_later(tmp_path):
    db_file = make_db(tmp_path)
    database.add_change_request(db_file, "A100", "9 Pine Street")
    assert database.reject_request(db_file, 1) == "Request 1 rejected."
    assert database.approve_request(db_file, 1) == "Request 1 is already rejected."
    assert database.find_order(db_file, "A100")["address"] == "14 Bay Road"


def test_unknown_request_number(tmp_path):
    db_file = make_db(tmp_path)
    assert database.approve_request(db_file, 7) == "There is no request 7."
    assert database.reject_request(db_file, 7) == "There is no request 7."


def test_restock(tmp_path):
    db_file = make_db(tmp_path)
    database.restock(db_file, "day pack", 15)
    assert database.find_product(db_file, "day pack")["stock"] == 15


def test_status_report_counts_orders(tmp_path):
    db_file = make_db(tmp_path)
    report = database.status_report(db_file)
    assert report == [
        {"status": "delivered", "orders": 2},
        {"status": "processing", "orders": 2},
        {"status": "shipped", "orders": 2},
    ]


def test_reset_database_starts_again(tmp_path):
    db_file = make_db(tmp_path)
    database.add_change_request(db_file, "A100", "9 Pine Street")
    database.approve_request(db_file, 1)
    database.reset_database(db_file)
    assert database.find_order(db_file, "A100")["address"] == "14 Bay Road"
    assert database.add_change_request(db_file, "A101", "5 Elm Street") == 1
