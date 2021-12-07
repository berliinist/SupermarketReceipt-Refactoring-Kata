import copy as cp
import random
import unittest

from parameterized import parameterized

from pythonsupermarket.fake_catalog import FakeCatalog
from pythonsupermarket.model_objects import SpecialOfferType, ProductInfo, Offer
from pythonsupermarket.shopping_cart import ShoppingCart
from pythonsupermarket.teller import Teller

from shared_test_functions import setup_product_kwargs


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

    def _create_and_add_products_to_catalog(self, nr_products):
        self.product_dicts_list = [setup_product_kwargs() for _ in range(nr_products)]
        self.products = [ProductInfo(**cp.deepcopy(self.product_dicts_list[i])) for i in range(nr_products)]
        for i in range(nr_products):
            self.catalog.add_product(self.products[i])

    def _create_and_add_offers_and_return_expected_kwargs(self, nr_offers):
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
    def test_assert_correct_order_and_contents_of_added_offers(self, nr_offers):
        self._create_and_add_products_to_catalog(nr_offers)
        self.teller = Teller(self.catalog)
        expected = self._create_and_add_offers_and_return_expected_kwargs(nr_offers)

        for product in self.products:
            self.assertIsInstance(self.teller.offers[product], Offer)
            self.assertEqual(self.teller.offers[product].offer_type, expected[product]['offer_type'])
            self.assertEqual(self.teller.offers[product].argument, expected[product]['argument'])
        self.assertEqual(len(self.teller.offers), nr_offers)

    def _create_and_add_items_to_the_cart_and_return_expected(self, nr_products):
        self._create_and_add_products_to_catalog(nr_products)
        quantities = []
        for i in range(nr_products):
            quantities.append(round(random.random() * 10, 2))
            self.cart.add_item_quantity(item=self.products[i], quantity=quantities[-1])
        expected = sum(quantities[i] * self.product_dicts_list[i]['price_per_unit'] for i in range(nr_products))
        return expected, quantities

    @parameterized.expand([(1,), (3,)])
    def test_assert_correct_total_price_after_checkout_of_articles(self, nr_products):
        expected, _ = self._create_and_add_items_to_the_cart_and_return_expected(nr_products)
        teller = Teller(self.catalog)
        receipt = teller.checks_out_articles_from(self.cart)

        self.assertAlmostEqual(receipt.total_price(), expected, places=2)

    def _setup_item_to_discount_and_return_expected(self, quantities):
        nr_products = len(self.products)
        kwargs = {'offer_type': SpecialOfferType.PERCENT_DISCOUNT, 'argument': round(random.random() * 10, 2)}
        d_i = random.randrange(0, nr_products)


        expected = sum(quantities[i] * self.product_dicts_list[i]['price_per_unit'] for i in range(nr_products) if i != d_i)
        expected += quantities[d_i] * self.product_dicts_list[d_i]['price_per_unit'] * (1 - kwargs['argument'] / 100.)
        return expected, d_i, kwargs

    @parameterized.expand([(1,), (3,)])
    def test_checks_out_articles_with_one_article_percent_discounted_and_returns_receipt_correctly(self, nr_products):
        _, quantities = self._create_and_add_items_to_the_cart_and_return_expected(nr_products)
        self.teller = Teller(self.catalog)
        receipt = self.teller.checks_out_articles_from(self.cart)
        total_price_before_discounts = receipt.total_price()

        expected, discount_index, kwargs = self._setup_item_to_discount_and_return_expected(quantities)
        self.teller.add_special_offer(**kwargs, item=self.products[discount_index])

        receipt = self.teller.checks_out_articles_from(self.cart)
        total_price_after_discounts = receipt.total_price()

        self.assertLess(total_price_after_discounts, total_price_before_discounts)
        self.assertAlmostEqual(total_price_after_discounts, expected, 2)

    def test_returns_empty_receipt_and_zero_total_price_if_no_items_in_cart(self):
        self._create_and_add_products_to_catalog(nr_products=3)
        teller = Teller(self.catalog)

        receipt_result = teller.checks_out_articles_from(self.cart)
        self.assertEqual(receipt_result.total_price(), 0)
        self.assertListEqual(receipt_result.items, [])
