import unittest

from pythonsupermarket.template_catalog import TemplateCatalog


class TestSupermarketCatalog(unittest.TestCase):
    def test_refuses_instantiating_templatecatalog(self):
        with self.assertRaisesRegex(TypeError, "Can't instantiate"):
            TemplateCatalog()

    def test_accepts_newcatalog_with_all_required_abstracts(self):
        class NewCatalog(TemplateCatalog):
            def products(self):
                pass

            def add_product(self):
                pass

            def get_product(self):
                pass
        NewCatalog()

    def test_rejects_new_catalog_with_missing_required_abstract(self):
        class BadNewCatalog(TemplateCatalog):
            def add_product(self):
                pass

            def get_product(self):
                pass

        with self.assertRaisesRegex(TypeError, "Can't instantiate"):
            BadNewCatalog()
