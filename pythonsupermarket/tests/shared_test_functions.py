from collections import namedtuple
import random
import string


def set_up_item():
    product = namedtuple('product', ['name', 'unit'])
    return {
        'product': product(name=''.join(random.choice(string.ascii_lowercase) for x in range(5)).capitalize(),
                           unit=random.choice([1, 2])),
        'price': random.random() * 100}
