import math

from pythonsupermarket.model_objects import ProductQuantity, SpecialOfferType, Discount


class ShoppingCart:

    def __init__(self):
        self._items = []
        self._product_quantities = {}

    @property
    def items(self):
        return self._items

    @property
    def product_quantities(self):
        return self._product_quantities

    def add_item_quantity(self, product, quantity):
        self._items.append(ProductQuantity(product, quantity))
        if product in self._product_quantities.keys():
            self._product_quantities[product] += quantity
        else:
            self._product_quantities[product] = quantity

    def handle_offers(self, receipt, offers, catalog):
        for p in self._product_quantities.keys():
            quantity = self._product_quantities[p]
            if p in offers.keys():
                offer = offers[p]
                discount = self._get_discount(offer, catalog, quantity, p)

                if discount:
                    receipt.add_discount(discount)

    def _get_discount(self, offer, catalog, quantity, p):
        quantity_as_int = int(quantity)
        unit_price = catalog.unit_price(p)

        def _get_x_denominator(offer_type):
            if offer_type == SpecialOfferType.THREE_FOR_TWO:
                return 3
            elif offer_type == SpecialOfferType.TWO_FOR_AMOUNT:
                return 2
            elif offer_type == SpecialOfferType.FIVE_FOR_AMOUNT:
                return 5
            else:
                return 1
        x = _get_x_denominator(offer.offer_type)
        number_of_x = math.floor(quantity_as_int / x)

        if offer.offer_type == SpecialOfferType.THREE_FOR_TWO and quantity_as_int > 2:
            discount_amount = quantity * unit_price - (
                    (number_of_x * 2 * unit_price) + quantity_as_int % 3 * unit_price)
            return Discount(p, "3 for 2", -discount_amount)
        elif offer.offer_type == SpecialOfferType.TEN_PERCENT_DISCOUNT:  # TODO: rename it to PERCENT_DISCOUNT (it can do 20% or any % discount too.
            return Discount(p, str(offer.argument) + "% off",
                                -quantity * unit_price * offer.argument / 100.0)
        elif offer.offer_type == SpecialOfferType.TWO_FOR_AMOUNT and quantity_as_int >= 2:
            total = offer.argument * (quantity_as_int / x) + quantity_as_int % 2 * unit_price
            discount_n = unit_price * quantity - total
            return Discount(p, "2 for " + str(offer.argument), -discount_n)
        elif offer.offer_type == SpecialOfferType.FIVE_FOR_AMOUNT and quantity_as_int >= 5:
            discount_total = unit_price * quantity - (
                    offer.argument * number_of_x + quantity_as_int % 5 * unit_price)
            return Discount(p, str(x) + " for " + str(offer.argument), -discount_total)
        elif offer.offer_type == SpecialOfferType.BUNDLE_DISCOUNT:
            return Discount(p, str(offer.argument) + "% off for first unique item",
                            -unit_price * offer.argument / 100)
        else:
            return None