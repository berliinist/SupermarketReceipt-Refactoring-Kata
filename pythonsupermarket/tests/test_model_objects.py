import copy as cp
import unittest

import pythonsupermarket.model_objects as mdl_objcts

from tests.shared_test_functions import set_up_product_dict


class TestProduct(unittest.TestCase):
    def setUp(self):
        self.product_dict = set_up_product_dict()
        self.product_class = mdl_objcts.Product(**cp.deepcopy(self.product_dict))

    def test_assert_name_attribute_of_product_class(self):
        self.assertEqual(self.product_class.name, self.product_dict['name'])

    def test_assert_unit_attribute_of_product_class(self):
        self.assertEqual(self.product_class.unit, self.product_dict['unit'])

