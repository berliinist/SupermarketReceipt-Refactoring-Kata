from enum import Enum


class ProductInfo:
    def __init__(self, name, unit, price_per_unit):
        self._name = name
        self._unit = unit
        self._price_per_unit = price_per_unit

    @property
    def name(self):
        return self._name

    @property
    def unit(self):
        return self._unit

    @property
    def price_per_unit(self):
        return self._price_per_unit


class ProductUnit(Enum):
    EACH = 1
    KILO = 2


class SpecialOfferType(Enum):
    THREE_FOR_TWO = 1
    TEN_PERCENT_DISCOUNT = 2
    TWO_FOR_AMOUNT = 3
    FIVE_FOR_AMOUNT = 4
    BUNDLE_DISCOUNT = 5


class Offer:
    def __init__(self, offer_type, product, argument):  # TODO: remove this "product". what for?
        self.offer_type = offer_type
        self.product = product
        self.argument = argument


class Discount:
    def __init__(self, product, description, discount_amount):  # TODO: find out if this "product" still makes sense?
        self.product = product
        self.description = description
        self.discount_amount = discount_amount
