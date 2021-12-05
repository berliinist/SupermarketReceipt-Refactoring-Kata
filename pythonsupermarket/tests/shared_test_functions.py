from collections import namedtuple
import random
import string


PRODUCT_NAMEDTUPLE = namedtuple('product', ['name', 'unit'])


def set_up_product_dict():
    return {'name': ''.join(random.choice(string.ascii_lowercase) for x in range(5)).capitalize(),
            'unit': random.choice([1, 2])}

def set_up_item():
    return {
        'product': PRODUCT_NAMEDTUPLE(**set_up_product_dict()), 'price': random.random() * 100}
