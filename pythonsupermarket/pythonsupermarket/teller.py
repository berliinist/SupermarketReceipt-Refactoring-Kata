from pythonsupermarket.model_objects import Offer
from pythonsupermarket.receipt import Receipt


class Teller:

    def __init__(self, catalog):
        self.catalog = catalog
        self.offers = {}

    def add_special_offer(self, offer_type, product, argument):
        self.offers[product] = Offer(offer_type, product, argument)  # TODO: perhaps offer_type and argument in Offer is enough?

    def checks_out_articles_from(self, the_cart):
        receipt = Receipt()
        for item, quantity in the_cart.items.items():
            unit_price = self.catalog.get_product(item).price_per_unit
            receipt.add_product(item, quantity, unit_price, quantity * unit_price)
        the_cart.handle_offers(receipt, self.offers, self.catalog)

        return receipt
