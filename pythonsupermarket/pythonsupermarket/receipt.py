
class ReceiptItem:
    def __init__(self, product, quantity, price, total_price):
        self.product = product
        self.quantity = quantity
        self.price = price  # TODO: price per unit?
        self.total_price = total_price


class Receipt:
    def __init__(self):
        self._items = []
        self._discounts = []

    def total_price(self):
        total = 0
        for item in self.items:
            total += item.total_price
        for discount in self.discounts:
            total += discount.discount_amount
        return total

    def add_product(self, product, quantity, price, total_price):  # TODO: should rather be product, quantity, total_price? this "price" is price per unit?
        self._items.append(ReceiptItem(product, quantity, price, total_price))  # DO: price_per_unit to avoid confusion.

    def add_discount(self, discount):
        if discount is not None:
            self._discounts.append(discount)

    @property
    def items(self):
        return self._items[:]

    @property
    def discounts(self):
        return self._discounts[:]
