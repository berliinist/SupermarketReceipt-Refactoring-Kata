import copy as cp
import random
import unittest

from parameterized import parameterized

from pythonsupermarket.fake_catalog import FakeCatalog
from pythonsupermarket.model_objects import SpecialOfferType, ProductInfo, Offer
from pythonsupermarket.shopping_cart import ShoppingCart
from pythonsupermarket.teller import Teller

from shared_test_functions import set_up_product_dict


class TestTellerIntegration(unittest.TestCase):
    def setUp(self):
        self.catalog = FakeCatalog()
        self.cart = ShoppingCart()

    def test_teller_initializes_with_empty_catalog_if_no_products_added_to_it(self):
        teller = Teller(self.catalog)
        self.assertDictEqual(teller.catalog.products, {})

    def test_teller_initalizes_with_empty_offers(self):
        teller = Teller(self.catalog)
        self.assertDictEqual(teller.offers, {})

    def test_refuses_setting_catalog_property(self):
        teller = Teller(self.catalog)
        with self.assertRaises(AttributeError):
            teller.catalog = {}

    def test_refuses_setting_offers_property(self):
        teller = Teller(self.catalog)
        with self.assertRaises(AttributeError):
            teller.offers = {}

    def _create_products_and_call_add_product(self, nr_products):
        self.product_dicts_list = [set_up_product_dict() for _ in range(nr_products)]
        self.products = [ProductInfo(**cp.deepcopy(self.product_dicts_list[i])) for i in range(nr_products)]
        for i in range(nr_products):
            self.catalog.add_product(self.products[i])

    def _create_offers_to_add_to_teller_and_return_expected_kwargs(self, nr_offers):
        expected = {}
        for i in range(nr_offers):
            kwargs = {'offer_type': random.choice([SpecialOfferType.PERCENT_DISCOUNT,
                                                   SpecialOfferType.THREE_FOR_TWO,
                                                   SpecialOfferType.TWO_FOR_AMOUNT]),
                      'argument': round(random.random() * 10, 2)}
            self.teller.add_special_offer(**kwargs, item=self.products[i])
            expected.update({self.products[i]: cp.deepcopy(kwargs)})
        return expected

    @parameterized.expand([(1,), (3,)])
    def test_add_special_offer_adds_each_offer_correctly(self, nr_offers):
        self._create_products_and_call_add_product(nr_offers)
        self.teller = Teller(self.catalog)
        expected = self._create_offers_to_add_to_teller_and_return_expected_kwargs(nr_offers)

        for product in self.products:
            self.assertIsInstance(self.teller.offers[product], Offer)
            self.assertEqual(self.teller.offers[product].offer_type, expected[product]['offer_type'])
            self.assertEqual(self.teller.offers[product].argument, expected[product]['argument'])
        self.assertEqual(len(self.teller.offers), nr_offers)

    @parameterized.expand([(1,), (3,)])
    def test_checks_out_articles_and_returns_receipt_correctly(self, nr_products):
        self._create_products_and_call_add_product(nr_products)
        quantity = []
        for i in range(nr_products):
            quantity.append(round(random.random() * 10, 2))
            self.cart.add_item_quantity(item=cp.deepcopy(self.products[i]), quantity=quantity[-1])
        teller = Teller(self.catalog)

        receipt = teller.checks_out_articles_from(self.cart)
        expected = sum(quantity[i] * self.product_dicts_list[i]['price_per_unit'] for i in range(nr_products))
        self.assertAlmostEqual(receipt.total_price(), expected, places=2)

    def test_returns_empty_receipt_if_no_items_in_cart(self):
        self._create_products_and_call_add_product(nr_products=3)
        teller = Teller(self.catalog)

        receipt_result = teller.checks_out_articles_from(self.cart)
        self.assertEqual(receipt_result.total_price(), 0)
        self.assertListEqual(receipt_result.items, [])
