# tools.py
# Author: [Your Name]

import database


class BaysideTools:
    """The tools the model may ask for. Every request is checked in run first."""

    def __init__(self, db_file):
        """Remember which database the tools read and write."""
        self.db_file = db_file

    def tool_list(self):
        """Return the tools the model may ask for. They are not called here."""
        return [
            self.look_up_order,
            self.check_stock,
            self.request_address_change,
            self.check_request,
        ]

    def look_up_order(self, order_id):
        """Look up the status of one order.

        Args:
            order_id: The order ID, like A100.
        """
        for word in order_id.upper().split():
            order = database.find_order(self.db_file, word.strip("?.!,"))
            if order is not None:
                return f"Order {order['order_id']} is {order['status']}."
        return "No order with that ID was found. Order IDs look like A100."

    def check_stock(self, item):
        """Check how many of one product are in stock, and its price.

        Args:
            item: The product name, like rain jacket.
        """
        for name in database.product_names(self.db_file):
            if name in item.lower():
                product = database.find_product(self.db_file, name)
                stock = product["stock"]
                return f"We have {stock} of the {name} in stock, at ${product['price']:.2f}."
        return "That product was not found."

    def request_address_change(self, order_id, new_address):
        """Ask staff to change the shipping address on one order. Staff must approve it.

        Args:
            order_id: The order ID, like A100.
            new_address: The full new shipping address.
        """
        order_id = order_id.upper()
        if database.find_order(self.db_file, order_id) is None:
            return "No order with that ID was found. Order IDs look like A100."
        number = database.add_change_request(self.db_file, order_id, new_address)
        return f"Request {number} was sent to staff. The address has not changed yet."

    def check_request(self, number):
        """Check what staff decided about one address change request.

        Args:
            number: The request number, like 3.
        """
        try:
            request = database.find_request(self.db_file, int(number))
        except ValueError:
            return "Request numbers look like 3."
        if request is None:
            return f"There is no request {number}."
        order_id = request["order_id"]
        if request["status"] == "waiting":
            return f"Request {number} for order {order_id} is waiting for staff."
        return f"Request {number} for order {order_id} was {request['status']}."

    def run(self, name, arguments, history):
        """Check one tool request. Run the tool only if every check passes."""
        if name == "look_up_order":
            order_id = self.clean(arguments, "order_id")
            if order_id == "":
                return "The order ID is missing. Ask the customer for it."
            if not self.customer_said(history, order_id):
                return "The customer has not given that order ID. Ask them for it."
            return self.look_up_order(order_id)
        if name == "check_stock":
            item = self.clean(arguments, "item")
            if item == "":
                return "The product is missing. Ask the customer which product."
            return self.check_stock(item)
        if name == "request_address_change":
            order_id = self.clean(arguments, "order_id")
            new_address = self.clean(arguments, "new_address")
            if order_id == "" or new_address == "":
                return "The order ID and the new address are both needed."
            if not self.customer_said(history, order_id):
                return "The customer has not given that order ID. Ask them for it."
            if not self.customer_said(history, new_address):
                return "The customer has not given that address. Ask them for it."
            return self.request_address_change(order_id, new_address)
        if name == "check_request":
            number = self.clean(arguments, "number")
            if number == "":
                return "The request number is missing. Ask the customer for it."
            if not self.customer_said(history, number):
                return (
                    "The customer has not given that request number. Ask them for it."
                )
            return self.check_request(number)
        return f"There is no tool named {name}."

    def clean(self, arguments, key):
        """Return one argument as text without extra spaces, or "" if it is missing."""
        return str(arguments.get(key, "")).strip()

    def customer_said(self, history, text):
        """Return True if text appears in a message the customer typed."""
        for message in history:
            if message["role"] == "user" and text.lower() in message["content"].lower():
                return True
        return False
