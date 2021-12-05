from collections import namedtuple
import random
import string
import unittest

from pythonsupermarket.catalog import SupermarketCatalog

from tests.shared_test_functions import set_up_item


class TestSupermarketCatalog(unittest.TestCase):
    def setUp(self):
        self.supermarketcatalog = SupermarketCatalog()
        self.kw_args = set_up_item()

    def test_calling_add_product_raises_exception(self):
        with self.assertRaisesRegex(Exception, "accesses the database"):
            self.supermarketcatalog.add_product(**self.kw_args)

    def test_calling_unit_price_raises_exception(self):
        with self.assertRaisesRegex(Exception, "accesses the database"):
            self.supermarketcatalog.unit_price(self.kw_args['product'])
