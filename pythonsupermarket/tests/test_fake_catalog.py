from collections import namedtuple
import random
import string
import unittest

from pythonsupermarket.catalog import SupermarketCatalog
from pythonsupermarket.fake_catalog import FakeCatalog

from tests.shared_test_functions import set_up_product_catalog_dict


class TestFakeCatalog(unittest.TestCase):
    def setUp(self):
        self.fakecatalog = FakeCatalog()

    def test_fake_catalog_is_instance_of_supermarket_catalog(self):
        self.assertIsInstance(self.fakecatalog, SupermarketCatalog)

    def test_products_is_dict_type(self):
        self.assertIsInstance(self.fakecatalog.products, dict)

    def test_prices_is_dict_type(self):
        self.assertIsInstance(self.fakecatalog.prices, dict)

    def test_initial_products_is_empty(self):
        self.assertEqual(len(self.fakecatalog.products), 0)

    def test_initial_prices_is_empty(self):
        self.assertEqual(len(self.fakecatalog.prices), 0)

    def test_calling_initial_unit_price_method_raises_error(self):
        item_not_added = set_up_product_catalog_dict()
        with self.assertRaises(AttributeError):
            self.fakecatalog.unit_price(item_not_added)

    def test_add_product_is_functioning_correctly_by_asserting_first_added_item(self):
        item = set_up_product_catalog_dict()
        self.fakecatalog.add_product(**item)

        self.assertDictEqual(self.fakecatalog.products, {item['product'].name: item['product']})
        self.assertDictEqual(self.fakecatalog.prices, {item['product'].name: item['price']})

    def test_add_product_is_functioning_correctly_by_asserting_first_added_multiple_items(self):
        items = [set_up_product_catalog_dict() for _ in range(random.randrange(2, 7, 1))]
        for item in items:
            self.fakecatalog.add_product(**item)

        self.assertDictEqual(self.fakecatalog.products, {item['product'].name: item['product'] for item in items})
        self.assertDictEqual(self.fakecatalog.prices, {item['product'].name: item['price'] for item in items})

    def test_unit_price_method_call_returns_value_of_an_item_correctly(self):
        items = [set_up_product_catalog_dict() for _ in range(random.randrange(2, 7, 1))]
        for item in items:
            self.fakecatalog.add_product(**item)
        for item in items:
            self.assertEqual(self.fakecatalog.unit_price(item['product']), item['price'])
