from pythonsupermarket.model_objects import Offer
from pythonsupermarket.receipt import Receipt


class Teller:

    def __init__(self, catalog):
        self._catalog = catalog
        self._offers = {}

    @property
    def catalog(self):
        return self._catalog

    @property
    def offers(self):
        return self._offers

    def add_special_offer(self, offer_type, item, argument):
        self._offers[item] = Offer(offer_type, argument)

    def checks_out_articles_from(self, the_cart):
        receipt = Receipt()
        for item, quantity in the_cart.items.items():
            unit_price = self._catalog.get_product(item).price_per_unit
            receipt.add_item(item, quantity, unit_price, quantity * unit_price)
        the_cart.handle_offers(receipt, self._offers, self._catalog)

        return receipt
