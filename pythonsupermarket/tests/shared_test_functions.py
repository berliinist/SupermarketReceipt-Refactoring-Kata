from collections import namedtuple
import random
import string


PRODUCT_NAMEDTUPLE = namedtuple('product', ['name', 'unit'])


def set_up_item():
    return {
        'product': PRODUCT_NAMEDTUPLE(name=''.join(random.choice(string.ascii_lowercase) for x in range(5)).capitalize(),
                                      unit=random.choice([1, 2])),
        'price': random.random() * 100}
