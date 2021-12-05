import copy as cp
import random
import unittest
from unittest.mock import Mock, PropertyMock

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


class TestProductQuantity(unittest.TestCase):
    def setUp(self):
        self.product_dict = set_up_product_dict()
        self.product_quantity = range(random.randrange(2, 50, 1))
        self.product_class = Mock(spec_set=mdl_objcts.Product, **cp.deepcopy(self.product_dict))
        self.productquantity_class = mdl_objcts.ProductQuantity(product=self.product_class,
                                                                quantity=self.product_quantity)


    def test_assert_product_attribute_of_product_quantity(self):
        self.assertEqual(self.productquantity_class.product._extract_mock_name(), self.product_dict['name'])
            # TODO: there must be a better approach to access name without calling _extract_mock_name(), but not now.
        self.assertEqual(self.productquantity_class.product.unit, self.product_dict['unit'])

    def test_assert_quantity_attribute_of_product_quantity(self):
        self.assertEqual(self.productquantity_class.quantity, self.product_quantity)


class TestProductQuantityIntegration(unittest.TestCase):
    def setUp(self):
        self.product_dict = set_up_product_dict()
        self.product_quantity = range(random.randrange(2, 50, 1))
        self.product_class = mdl_objcts.Product(**cp.deepcopy(self.product_dict))
        self.productquantity_class = mdl_objcts.ProductQuantity(product=self.product_class,
                                                                quantity=self.product_quantity)

    def test_assert_product_attribute_of_product_quantity(self):
        self.assertEqual(self.productquantity_class.product.name, self.product_dict['name'])
        self.assertEqual(self.productquantity_class.product.unit, self.product_dict['unit'])

    def test_assert_quantity_attribute_of_product_quantity(self):
        self.assertEqual(self.productquantity_class.quantity, self.product_quantity)