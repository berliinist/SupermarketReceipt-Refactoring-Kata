from pythonsupermarket.template_catalog import TemplateCatalog


class FakeCatalog(TemplateCatalog):
    def __init__(self):
        self._products = {}

    @property
    def products(self):
        return self._products

    def add_product(self, product):
        self._products[product.name] = product

    def get_product(self, product):
        return self._products[product.name]
