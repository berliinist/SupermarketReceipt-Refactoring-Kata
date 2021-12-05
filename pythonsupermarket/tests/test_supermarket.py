import unittest

import pytest

from pythonsupermarket.model_objects import Product, SpecialOfferType, ProductUnit
from pythonsupermarket.shopping_cart import ShoppingCart
from pythonsupermarket.teller import Teller
from pythonsupermarket.fake_catalog import FakeCatalog


class TestTenPercentDiscount(unittest.TestCase):
    def setUp(self):
        catalog = FakeCatalog()
        toothbrush = Product("toothbrush", ProductUnit.EACH)
        catalog.add_product(toothbrush, 0.99)

        self.apples = Product("apples", ProductUnit.KILO)
        catalog.add_product(self.apples, 1.99)

        teller = Teller(catalog)
        teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, toothbrush, 10.0)

        cart = ShoppingCart()
        cart.add_item_quantity(self.apples, 2.5)

        self.receipt = teller.checks_out_articles_from(cart)

    def test_assert_total_price(self):
        self.assertAlmostEqual(4.975, self.receipt.total_price(), places=2)

    def test_everything(self):
        receipt = self.receipt
        assert [] == receipt.discounts
        assert 1 == len(receipt.items)
        receipt_item = receipt.items[0]
        assert self.apples == receipt_item.product
        assert 1.99 == receipt_item.price
        assert 2.5 * 1.99 == pytest.approx(receipt_item.total_price, 0.01)
        assert 2.5 == receipt_item.quantity
