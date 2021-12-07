from pythonsupermarket.catalog import SupermarketCatalog


class FakeCatalog(SupermarketCatalog):
    def __init__(self):
        self._products = {}

        # TODO: Probably the best way to go is this:
        # catalog.products = {name: {'name': name, 'per_unit_type': per_unit_type, 'price_per_unit': price_per_unit},
        #                     .....}

    @property
    def products(self):
        return self._products

    def add_product(self, product):
        self._products[product.name] = product

    def get_product(self, product):
        return self._products[product.name]

    def unit_price(self, product):  # TODO: delete this method permanently.
        return product.price_per_unit
