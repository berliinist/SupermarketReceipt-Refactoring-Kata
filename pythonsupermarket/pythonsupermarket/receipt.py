
class ReceiptItem:
    def __init__(self, product, quantity, unit_price, total_price):
        self._product = product
        self._quantity = quantity
        self._unit_price = unit_price
        self._total_price = total_price

    @property
    def product(self):
        return self._product

    @property
    def quantity(self):
        return self._quantity

    @property
    def unit_price(self):
        return self._unit_price

    @property
    def total_price(self):
        return self._total_price


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

    def add_product(self, product, quantity, unit_price, total_price):
        self._items.append(ReceiptItem(product, quantity, unit_price, total_price))

    def add_discount(self, discount):
        if discount is not None:
            self._discounts.append(discount)

    @property
    def items(self):
        return self._items[:]

    @property
    def discounts(self):
        return self._discounts[:]
