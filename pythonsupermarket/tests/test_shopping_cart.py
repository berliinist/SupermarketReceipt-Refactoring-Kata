import copy as cp
import random
import unittest

from parameterized import parameterized
import pytest

import pythonsupermarket.model_objects as mdl_objcts
from pythonsupermarket.shopping_cart import ShoppingCart

from shared_test_functions import set_up_product_dict


@pytest.mark.skip(reason="Limited time, priorities.")
class TestShoppingCart(unittest.TestCase):
    pass


class TestShoppingCartIntegration(unittest.TestCase):
    def setUp(self):
        self.shoppingcart = ShoppingCart()

    def _set_up_kw_args_of_each_productquantity_in_list(self, nr_items):
        self.product_dicts_list = [set_up_product_dict() for _ in range(nr_items)]
        self.kw_args_list = [{'product': mdl_objcts.Product(**cp.deepcopy(self.product_dicts_list[i])),
                              'quantity': random.randrange(1, 100, 1)} for i in range(nr_items)]

    def test_initial_list_of_items_is_empty(self):
        self.assertListEqual(self.shoppingcart.items, [])

    def test_initial_dict_of_product_quantities_is_empty(self):
        self.assertDictEqual(self.shoppingcart.product_quantities, {})

    def test_item_added_in_list_of_items_is_instance_of_productquantity(self):
        self._set_up_kw_args_of_each_productquantity_in_list(1)
        self.shoppingcart.add_item_quantity(**self.kw_args_list[0])
        self.assertIsInstance(self.shoppingcart.items[0], mdl_objcts.ProductQuantity)

    @parameterized.expand([(1,), (7,)])  # TODO: this test is too long to read
    def test_assert_add_item_quantity_yields_correct_number_of_different_items_and_quantities_each(self, nr_items):
        self._set_up_kw_args_of_each_productquantity_in_list(nr_items)
        for i in range(nr_items):
            self.shoppingcart.add_item_quantity(**self.kw_args_list[i])
        expected_product_names_list = [self.product_dicts_list[i]['name'] for i in range(nr_items)]
        expected_product_quantities_list = [self.kw_args_list[i]['quantity'] for i in range(nr_items)]

        self.assertListEqual([self.shoppingcart.items[i].product.name for i in range(nr_items)],
                             expected_product_names_list)
        self.assertListEqual([self.shoppingcart.items[i].quantity for i in range(nr_items)],
                             expected_product_quantities_list)

        expected_dict = {self.kw_args_list[i]['product']: self.kw_args_list[i]['quantity'] for i in range(nr_items)}
        self.assertDictEqual(self.shoppingcart.product_quantities, expected_dict)

    @parameterized.expand([(1,), (6,)])  # TODO: this test is also too long to read
    def test_assert_add_item_quantity_repeatedly_for_some_same_items_yields_quantities_correctly(self, nr_items):
        self._set_up_kw_args_of_each_productquantity_in_list(nr_items)
        for i in range(nr_items):
            self.shoppingcart.add_item_quantity(**self.kw_args_list[i])
        add_qts = [{'product': self.kw_args_list[i]['product'],
                    'quantity': random.randrange(0, 5, 1)} for i in range(nr_items - 1)]
        for i in range(len(add_qts)):
            self.shoppingcart.add_item_quantity(**add_qts[i])
        expected = {self.kw_args_list[i]['product']: self.kw_args_list[i]['quantity'] + add_qts[i]['quantity']
                    for i in range(nr_items - 1)}
        expected.update({self.kw_args_list[nr_items - 1]['product']: self.kw_args_list[nr_items -1]['quantity']})
        self.assertDictEqual(self.shoppingcart.product_quantities, expected)

        expected_list = [self.product_dicts_list[i]['name'] for i in range(nr_items)] + [add_qts[i]['product'].name for i in range(nr_items - 1)]
        expected_qts_list = [self.kw_args_list[i]['quantity'] for i in range(nr_items)] + [add_qts[i]['quantity'] for i in range(nr_items-1)]
        self.assertListEqual([self.shoppingcart.items[i].product.name for i in range(nr_items * 2 - 1)], expected_list)
        self.assertListEqual([self.shoppingcart.items[i].quantity for i in range(nr_items * 2 - 1)], expected_qts_list)


    # TODO: add unit tests related to a method handle_offers