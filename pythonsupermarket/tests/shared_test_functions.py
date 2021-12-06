from collections import namedtuple
import random
import string


PRODUCT_NAMEDTUPLE = namedtuple('product', ['name', 'unit', 'price_per_unit'])  # TODO: review if we still want to keep this namedtuple here?


def set_up_product_dict():
    return {'name': ''.join(random.choice(string.ascii_lowercase) for x in range(5)).capitalize(),
            'unit': random.choice([1, 2]),
            'price_per_unit': round(random.random() * 100, 2)}

def set_up_product_catalog_dict():
    return {'product': PRODUCT_NAMEDTUPLE(**set_up_product_dict())}  # TODO: remove this price_per_unit permanently?


class SharedUnitTests:
    def test_asserts_product_correctly(self):
        self.assertEqual(self.test_class.product.name, self.product_dict['name'])
        self.assertEqual(self.test_class.product.unit, self.product_dict['unit'])  # Do we really need this?
