# stock_tool.py
# Author: [Your Name]


class StockLookup:
    """A tool that knows how many of each product are in stock."""

    def __init__(self, stock):
        """Store the stock counts this tool can look up."""
        self.stock = stock

    def find_product(self, text):
        """Return the first known product mentioned in text, or None."""
        for product in self.stock:
            if product in text.lower():
                return product
        return None

    def count_for(self, product):
        """Return how many of one product are in stock, or None if unknown."""
        if product in self.stock:
            return self.stock[product]
        return None
