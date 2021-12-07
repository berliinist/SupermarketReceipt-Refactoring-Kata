import copy as cp
import random
import unittest

from parameterized import parameterized
import pytest

from pythonsupermarket.fake_catalog import FakeCatalog
from pythonsupermarket.model_objects import SpecialOfferType, ProductInfo, Offer
from pythonsupermarket.shopping_cart import ShoppingCart
from pythonsupermarket.teller import Teller

from shared_test_functions import set_up_product_dict


@pytest.mark.skip(reason="lower priority currently")
class TestTeller(unittest.TestCase):
    pass


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

    def _create_products_and_call_add_product(self, nr_products):
        self.product_dicts_list = [set_up_product_dict() for _ in range(nr_products)]
        self.products = [ProductInfo(**cp.deepcopy(self.product_dicts_list[i])) for i in range(nr_products)]
        for i in range(nr_products):
            self.catalog.add_product(self.products[i])

    def _create_offers_and_add_them_to_teller(self, nr_offers):
        for i in range(nr_offers):
            self.teller.add_special_offer(offer_type=SpecialOfferType.TEN_PERCENT_DISCOUNT,
                                          product=self.products[i],
                                          argument=round(random.random() * 10, 2))

    @parameterized.expand([(1,), (3,)])
    def test_add_special_offer_adds_each_offer_correctly(self, nr_offers):
        self._create_products_and_call_add_product(nr_offers)
        self.teller = Teller(self.catalog)
        self._create_offers_and_add_them_to_teller(nr_offers)

        self.assertEqual(len(self.teller.offers), nr_offers)
        for product in self.products:
            self.assertIsInstance(self.teller.offers[product], Offer)

    @parameterized.expand([(1,), (3,)])
    def test_assert_checks_out_articles_and_returns_receipt_successfully(self, nr_unique_products):
        self._create_products_and_call_add_product(nr_unique_products)
        quantity = []
        for i in range(nr_unique_products):
            quantity.append(round(random.random() * 10, 2))
            self.cart.add_item_quantity(item=cp.deepcopy(self.products[i]), quantity=quantity[-1])
        teller = Teller(self.catalog)

        receipt_result = teller.checks_out_articles_from(self.cart)
        expected = sum(quantity[i] * self.product_dicts_list[i]['price_per_unit'] for i in range(nr_unique_products))
        self.assertAlmostEqual(receipt_result.total_price(), expected, places=2)

    def test_returns_empty_receipt_if_no_items_in_cart(self):
        nr_unique_products = 3
        self._create_products_and_call_add_product(nr_unique_products)
        teller = Teller(self.catalog)
        receipt_result = teller.checks_out_articles_from(self.cart)
        self.assertEqual(receipt_result.total_price(), 0)
