from enum import Enum


class ProductUnit(Enum):
    EACH = 1
    KILO = 2


class SpecialOfferType(Enum):
    THREE_FOR_TWO = 1
    PERCENT_DISCOUNT = 2
    TWO_FOR_AMOUNT = 3
    FIVE_FOR_AMOUNT = 4
    BUNDLE_DISCOUNT = 5


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


class Offer:
    def __init__(self, offer_type, argument):
        self._offer_type = offer_type
        self._argument = argument

    @property
    def offer_type(self):
        return self._offer_type

    @property
    def argument(self):
        return self._argument


class Discount:
    def __init__(self, product, description, discount_amount):
        self._product = product
        self._description = description
        self._discount_amount = discount_amount

    @property
    def product(self):
        return self._product

    @property
    def description(self):
        return self._description

    @property
    def discount_amount(self):
        return self._discount_amount
