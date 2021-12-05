import copy as cp
import random
import unittest

import pytest

import pythonsupermarket.model_objects as mdl_objcts
import pythonsupermarket.receipt as receipt

from tests.shared_test_functions import set_up_product_dict, SharedUnitTests


@pytest.mark.skip(reason="Mocked items of product class a lower priority at the moment.")
class TestReceiptItem(unittest.TestCase):
    pass


class TestReceiptItemIntegration(unittest.TestCase, SharedUnitTests):
    def setUp(self):
        self.product_dict = set_up_product_dict()
        self.product_quantity = random.randrange(1, 100, 1)
        self.price = random.randrange(1, 50, 1)
        self.total_price = max(self.price, random.randrange(1, 100, 2))
        self.test_class = receipt.ReceiptItem(product=mdl_objcts.Product(**cp.deepcopy(self.product_dict)),
                                              quantity=self.product_quantity,
                                              price=self.price,
                                              total_price=self.total_price)

    def test_asserts_quantity(self):
        self.assertEqual(self.test_class.quantity, self.product_quantity)

    def test_asserts_price(self):
        self.assertEqual(self.test_class.price, self.price)

    def test_asserts_total_price(self):
        self.assertEqual(self.test_class.total_price, self.total_price)
