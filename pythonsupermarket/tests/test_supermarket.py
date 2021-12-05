import unittest

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

    def test_assert_expected_total_price_in_receipt(self):
        self.assertAlmostEqual(4.975, self.receipt.total_price(), delta=0.01)

    def test_assert_discounts_list_is_empty(self):
        self.assertListEqual(self.receipt.discounts, [])

    def test_assert_number_of_items_in_receipt_is_one(self):
        self.assertEqual(len(self.receipt.items), 1)

    def test_assert_item_is_apple(self):
        self.assertEqual(self.apples, self.receipt.items[0].product)

    def test_assert_normal_price_of_an_item_per_kilo(self):
        self.assertEqual(self.receipt.items[0].price, 1.99)

    def test_assert_total_price_of_item(self):
        self.assertAlmostEqual(2.5 * 1.99, self.receipt.items[0].total_price, delta=0.01)

    def test_assert_quantity_of_item(self):
        self.assertEqual(2.5, self.receipt.items[0].quantity)

