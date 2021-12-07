import random
import unittest

from parameterized import parameterized

from pythonsupermarket.template_catalog import TemplateCatalog
from pythonsupermarket.fake_catalog import FakeCatalog

from tests.shared_test_functions import set_up_product_dict, PRODUCT_NAMEDTUPLE


class TestFakeCatalog(unittest.TestCase):
    def setUp(self):
        self.fakecatalog = FakeCatalog()

    def test_fake_catalog_is_instance_of_supermarket_catalog(self):
        self.assertIsInstance(self.fakecatalog, TemplateCatalog)

    def test_products_is_dict_type(self):
        self.assertIsInstance(self.fakecatalog.products, dict)

    def test_initial_products_is_empty(self):
        self.assertEqual(len(self.fakecatalog.products), 0)

    def test_changing_products_property_directly_raises_error(self):
        with self.assertRaises(AttributeError):
            self.fakecatalog.products = {}

    def test_calling_initial_get_product_method_raises_error(self):
        product_catalog_not_added = PRODUCT_NAMEDTUPLE(**set_up_product_dict())
        with self.assertRaises(KeyError):
            self.fakecatalog.get_product(product_catalog_not_added)

    def _add_products(self, nr_add_products):
        products = [PRODUCT_NAMEDTUPLE(**set_up_product_dict()) for _ in range(nr_add_products)]
        for product in products:
            self.fakecatalog.add_product(product)
        return products

    @parameterized.expand([(1, ), (random.randrange(2, 7, 1),)])
    def test_assert_add_product_giving_products_property_correctly(self, nr_add_products):
        products = self._add_products(nr_add_products)
        self.assertDictEqual(self.fakecatalog.products,
                             {product.name: product for product in products})

    @parameterized.expand([(1,), (random.randrange(2, 7, 1),)])
    def test_get_product_returns_product_correctly(self, nr_add_products):
        products = self._add_products(nr_add_products)
        for product in products:
            received_product = self.fakecatalog.get_product(product)
            self.assertEqual(received_product, product)
