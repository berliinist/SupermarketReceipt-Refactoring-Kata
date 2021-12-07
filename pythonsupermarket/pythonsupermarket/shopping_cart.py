import math

from pythonsupermarket.model_objects import SpecialOfferType, Discount


class ShoppingCart:

    def __init__(self):
        self._items = {}

    @property
    def items(self):
        return self._items

    def add_item_quantity(self, item, quantity):  # TODO: is there a maybe pythonic approach? find out.
        if item in self._items.keys():
            self._items[item] += quantity
        else:
            self._items[item] = quantity

    def handle_offers(self, receipt, offers, catalog):
        items_with_offers = set(self._items).intersection(set(offers))
        for item in items_with_offers:
            quantity = self._items[item]
            discount = self._get_discount(offers[item], catalog, quantity, item)
            receipt.add_discount(discount)

    def _get_discount(self, offer, catalog, quantity, item):
        price_per_unit = catalog.get_product(item).price_per_unit

        if offer.offer_type == SpecialOfferType.THREE_FOR_TWO:
            return self._discount_three_for_two(
                item, price_per_unit, quantity)
        elif offer.offer_type == SpecialOfferType.TEN_PERCENT_DISCOUNT:  # TODO: rename it to PERCENT_DISCOUNT (it can do 20% or any % discount too.
            return self._discount_percent_discount(
                item, price_per_unit, quantity, offer)
        elif offer.offer_type == SpecialOfferType.TWO_FOR_AMOUNT:
            return self._discount_two_for_amount(
                item, price_per_unit, quantity, offer)
        elif offer.offer_type == SpecialOfferType.FIVE_FOR_AMOUNT:
            return self._discount_five_for_amount(
                item, price_per_unit, quantity, offer)
        elif offer.offer_type == SpecialOfferType.BUNDLE_DISCOUNT:
            return self._discount_bundle_discount(
                item, price_per_unit, quantity, offer)
        else:
            return None

    def _discount_three_for_two(self, item, price_per_unit, quantity):
        if int(quantity) > 2:
            x = 3
            number_of_x = math.floor(int(quantity) / x)
            discount_amount = quantity * price_per_unit - (
                    (number_of_x * 2 * price_per_unit) + int(quantity) % 3 * price_per_unit)
            return Discount(item, "3 for 2", -discount_amount)
        return None

    def _discount_percent_discount(self, item, price_per_unit, quantity, offer):
        return Discount(item, str(offer.argument) + "% off",
                        -quantity * price_per_unit * offer.argument / 100.0)

    def _discount_two_for_amount(self, item, price_per_unit, quantity, offer):
        if int(quantity) >= 2:
            x = 2
            total = offer.argument * (int(quantity) / x) + int(quantity) % 2 * price_per_unit
            discount_n = price_per_unit * quantity - total
            return Discount(item, "2 for " + str(offer.argument), -discount_n)
        return None

    def _discount_five_for_amount(self, item, price_per_unit, quantity, offer):
        if int(quantity) >= 5:
            x = 5
            number_of_x = math.floor(int(quantity) / x)
            total_price = price_per_unit * quantity
            discount_total = price_per_unit * quantity - (
                    offer.argument * number_of_x + int(quantity) % 5 * price_per_unit)
            return Discount(item, str(x) + " for " + str(offer.argument), -discount_total)
        return None

    def _discount_bundle_discount(self, item, price_per_unit, quantity, offer):
        return Discount(item, str(offer.argument) + "% off for first unique item",
                        -price_per_unit * offer.argument / 100)
