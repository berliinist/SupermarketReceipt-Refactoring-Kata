from pythonsupermarket.catalog import SupermarketCatalog


class FakeCatalog(SupermarketCatalog):
    def __init__(self):
        self.products = {}
        self.prices = {}

        # TODO: Probably the best way to go is this:
        # catalog.products = {name: {'name': name, 'per_unit_type': per_unit_type, 'price_per_unit': price_per_unit},
        #                     .....}

    def add_product(self, product, price_per_unit):  # TODO: price_per_unit? rename to add_product_info (just an information in catalog...)
        self.products[product.name] = product
        self.prices[product.name] = price_per_unit

    def unit_price(self, product):  # TODO: why does this exist?
        return self.prices[product.name]
