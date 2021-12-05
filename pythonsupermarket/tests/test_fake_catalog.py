import unittest

from pythonsupermarket.catalog import SupermarketCatalog
from pythonsupermarket.fake_catalog import FakeCatalog


class TestFakeCatalog(unittest.TestCase):
    def setUp(self):
        self.fakecatalog = FakeCatalog()

    def test_fake_catalog_is_instance_of_supermarket_catalog(self):
        self.assertIsInstance(self.fakecatalog, SupermarketCatalog)
