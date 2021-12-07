from collections import namedtuple
from enum import Enum
import random
import string


class ProductUnitForTestOnly(Enum):
    EACH = 1
    KILO = 2


PRODUCT_NAMEDTUPLE = namedtuple('product', ['name', 'unit', 'price_per_unit'])  # TODO: review if we still want to keep this namedtuple here?


def set_up_product_dict():  # TODO: think of a better name. set_up_product_input_kwargs?
    return {'name':             ''.join(random.choice(string.ascii_lowercase) for x in range(5)).capitalize(),
            'unit':             random.choice([ProductUnitForTestOnly.EACH, ProductUnitForTestOnly.KILO]),
            'price_per_unit':   round(random.random() * 100, 2)}


class SharedUnitTests:
    def test_asserts_product_correctly(self):  # TODO: this is no longer necessary in long term (or strong refactoring needed).
        self.assertEqual(self.test_class.product.name, self.product_dict['name'])
        self.assertEqual(self.test_class.product.unit, self.product_dict['unit'])  # Do we really need this?
