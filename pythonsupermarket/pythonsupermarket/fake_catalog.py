from pythonsupermarket.catalog import SupermarketCatalog


class FakeCatalog(SupermarketCatalog):
    def __init__(self):
        self.products = {}

        # TODO: Probably the best way to go is this:
        # catalog.products = {name: {'name': name, 'per_unit_type': per_unit_type, 'price_per_unit': price_per_unit},
        #                     .....}

    def add_product(self, product):  # TODO: price_per_unit? rename to add_product_info (just an information in catalog...)
        self.products[product.name] = product

    def unit_price(self, product):  # TODO: why does this exist? shall we remove it permanently?
        return product.price_per_unit
