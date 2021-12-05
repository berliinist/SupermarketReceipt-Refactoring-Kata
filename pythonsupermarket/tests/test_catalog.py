from collections import namedtuple
import random
import string
import unittest

from pythonsupermarket.catalog import SupermarketCatalog


class TestSupermarketCatalog(unittest.TestCase):
    def setUp(self):
        self.supermarketcatalog = SupermarketCatalog()
        product = namedtuple('product', ['name', 'unit'])
        self.kw_args = {
            'product': product(name=''.join(random.choice(string.ascii_lowercase) for x in range(5)).capitalize(),
                               unit=1),
            'price': random.random() * 100}

    def test_calling_add_product_raises_exception(self):
        with self.assertRaisesRegex(Exception, "accesses the database"):
            self.supermarketcatalog.add_product(**self.kw_args)

    def test_calling_unit_price_raises_exception(self):
        with self.assertRaisesRegex(Exception, "accesses the database"):
            self.supermarketcatalog.unit_price(self.kw_args['product'])
