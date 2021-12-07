from collections import namedtuple
from enum import Enum
import random
import string


PRODUCT_NAMEDTUPLE = namedtuple('product', ['name', 'unit', 'price_per_unit'])


class ProductUnitForTestOnly(Enum):
    EACH = 1
    KILO = 2


def set_up_product_dict():  # TODO: think of a better name. set_up_product_input_kwargs?
    return {'name':             ''.join(random.choice(string.ascii_lowercase) for x in range(5)).capitalize(),
            'unit':             random.choice([ProductUnitForTestOnly.EACH, ProductUnitForTestOnly.KILO]),
            'price_per_unit':   round(random.random() * 100, 2)}
