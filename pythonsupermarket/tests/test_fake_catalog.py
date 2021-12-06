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

    def test_initial_products_is_empty(self):
        self.assertEqual(len(self.fakecatalog.products), 0)

    def test_calling_initial_unit_price_method_raises_error(self):
        product_catalog_not_added = set_up_product_catalog_dict()
        with self.assertRaises(AttributeError):
            self.fakecatalog.unit_price(product_catalog_not_added)

    def test_add_product_is_functioning_correctly_by_asserting_first_added_product_catalog(self):
        catalog = set_up_product_catalog_dict()
        self.fakecatalog.add_product(**catalog)

        self.assertDictEqual(self.fakecatalog.products, {catalog['product'].name: catalog['product']})

    def test_add_product_is_functioning_correctly_by_asserting_first_added_multiple_product_catalogs(self):
        catalogs = [set_up_product_catalog_dict() for _ in range(random.randrange(2, 7, 1))]
        for product_catalog in catalogs:
            self.fakecatalog.add_product(**product_catalog)

        self.assertDictEqual(self.fakecatalog.products,
                             {catalog['product'].name: catalog['product'] for catalog in catalogs})

    def test_unit_price_method_call_returns_value_of_a_product_catalog_correctly(self):
        catalogs = [set_up_product_catalog_dict() for _ in range(random.randrange(2, 7, 1))]
        for catalog in catalogs:
            self.fakecatalog.add_product(**catalog)
        for catalog in catalogs:
            self.assertEqual(self.fakecatalog.unit_price(catalog['product']), catalog['product'].price_per_unit)
