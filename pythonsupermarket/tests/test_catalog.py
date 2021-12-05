import random
import string
import unittest

from pythonsupermarket.catalog import SupermarketCatalog


class TestSupermarketCatalog(unittest.TestCase):
    def setUp(self):
        self.supermarketcatalog = SupermarketCatalog()

    def test_calling_add_product_raises_exception(self):
        with self.assertRaisesRegex(Exception, "accesses the database"):
            self.supermarketcatalog.add_product(
                product=''.join(random.choice(string.ascii_lowercase) for x in range(5)).capitalize(),
                price=random.random() * 100)

    def test_calling_unit_price_raises_exception(self):
        with self.assertRaisesRegex(Exception, "accesses the database"):
            self.supermarketcatalog.unit_price(
                product=''.join(random.choice(string.ascii_lowercase) for x in range(5)).capitalize())
