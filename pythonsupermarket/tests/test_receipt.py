import copy as cp
import random
import unittest

from parameterized import parameterized
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
        self.product_quantity = random.randrange(1, 50, 1)
        self.unit_price = round(random.random() * 100, 2)
        self.total_price = max(self.unit_price, round(random.random() * 200, 2))
        self.test_class = receipt.ReceiptItem(product=mdl_objcts.ProductInfo(**cp.deepcopy(self.product_dict)),
                                              quantity=self.product_quantity,
                                              unit_price=self.unit_price,
                                              total_price=self.total_price)

    def test_asserts_quantity(self):
        self.assertEqual(self.test_class.quantity, self.product_quantity)

    def test_asserts_unit_price(self):
        self.assertEqual(self.test_class.unit_price, self.unit_price)

    def test_asserts_total_price(self):
        self.assertEqual(self.test_class.total_price, self.total_price)


@pytest.mark.skip(reason="Mocked ReceiptItem of a lower priority currently.")
class TestReceipt(unittest.TestCase):
    pass


class TestReceiptIntegration(unittest.TestCase):
    def setUp(self):
        self.receipt = receipt.Receipt()

    def _set_up_kw_args_of_each_product_in_list(self, nr_items):
        self.product_dicts_list = [set_up_product_dict() for _ in range(nr_items)]
        self.kw_args_list = [{'product': mdl_objcts.ProductInfo(**cp.deepcopy(self.product_dicts_list[i])),
                              'quantity': random.randrange(1, 100, 1),
                              'unit_price': round(random.random() * 100, 2),
                              'total_price': round(random.random() * 200, 2)} for i, _ in enumerate(range(nr_items))]

    def _set_up_kw_args_of_each_discount_in_list(self, nr_items):
        self.product_dicts_list = [set_up_product_dict() for _ in range(nr_items)]
        self.kw_args_disc_list = [
            {'product': mdl_objcts.ProductInfo(**cp.deepcopy(self.product_dicts_list[i])),
             'description': f'Some discount number {i+1}',
             'discount_amount': round(random.random() * -10, 2)} for i, _ in enumerate(range(nr_items))]

    def test_initial_receipt_items_returns_empty(self):
        self.assertListEqual(self.receipt.items, [])

    def test_initial_receipt_discounts_returns_empty(self):
        self.assertListEqual(self.receipt.discounts, [])

    def test_initial_total_price_returns_empty(self):
        self.assertEqual(self.receipt.total_price(), 0)

    def test_item_added_is_an_instance_of_receipt_item(self):
        self._set_up_kw_args_of_each_product_in_list(1)
        self.receipt.add_product(**self.kw_args_list[0])
        self.assertIsInstance(self.receipt.items[0], receipt.ReceiptItem)

    @parameterized.expand([(1,), (10,)])
    def test_number_of_products_added_returns_the_length_of_items_correctly(self, nr_items):
        self._set_up_kw_args_of_each_product_in_list(nr_items)
        for i in range(nr_items):
            self.receipt.add_product(**self.kw_args_list[i])
        self.assertEqual(len(self.receipt.items), nr_items)

    @parameterized.expand([(1,), (8,)])
    def test_assert_product_name_of_each_added_receipt_item(self, nr_items):
        self._set_up_kw_args_of_each_product_in_list(nr_items)
        for i in range(nr_items):
            self.receipt.add_product(**self.kw_args_list[i])
        self.assertListEqual([self.receipt.items[i].product.name for i in range(nr_items)],
                             [self.product_dicts_list[i]['name'] for i in range(nr_items)])

    @parameterized.expand([(1,), (7,)])
    def test_assert_product_unit_of_each_added_receipt_item(self, nr_items):
        self._set_up_kw_args_of_each_product_in_list(nr_items)
        for i in range(nr_items):
            self.receipt.add_product(**self.kw_args_list[i])
        self.assertListEqual([self.receipt.items[i].product.unit for i in range(nr_items)],
                             [self.product_dicts_list[i]['unit'] for i in range(nr_items)])

    @parameterized.expand([(1,), (6,)])
    def test_assert_quantity_of_each_added_receipt_item(self, nr_items):
        self._set_up_kw_args_of_each_product_in_list(nr_items)
        for i in range(nr_items):
            self.receipt.add_product(**self.kw_args_list[i])
        self.assertListEqual([self.receipt.items[i].quantity for i in range(nr_items)],
                             [self.kw_args_list[i]['quantity'] for i in range(nr_items)])

    @parameterized.expand([(1,), (6,)])
    def test_assert_unit_price_of_each_added_receipt_item(self, nr_items):
        self._set_up_kw_args_of_each_product_in_list(nr_items)
        for i in range(nr_items):
            self.receipt.add_product(**self.kw_args_list[i])
        self.assertListEqual([self.receipt.items[i].unit_price for i in range(nr_items)],
                             [self.kw_args_list[i]['unit_price'] for i in range(nr_items)])

    @parameterized.expand([(1,), (5,)])
    def test_assert_total_price_of_each_added_receipt_item(self, nr_items):
        self._set_up_kw_args_of_each_product_in_list(nr_items)
        for i in range(nr_items):
            self.receipt.add_product(**self.kw_args_list[i])
        self.assertListEqual([self.receipt.items[i].total_price for i in range(nr_items)],
                             [self.kw_args_list[i]['total_price'] for i in range(nr_items)])

    @parameterized.expand([(1,), (4,)])
    def test_assert_no_discounts_added_if_discount_is_none(self, nr_items):
        self._set_up_kw_args_of_each_discount_in_list(nr_items)
        for i in range(nr_items):
            self.receipt.add_discount(None)
        self.assertEqual(len(self.receipt.discounts), 0)

    @parameterized.expand([(1,), (4,)])
    def test_assert_number_of_discounts_added_returns_the_length_of_discounts_correctly(self, nr_items):
        self._set_up_kw_args_of_each_discount_in_list(nr_items)
        for i in range(nr_items):
            self.receipt.add_discount(mdl_objcts.Discount(**self.kw_args_disc_list[i]))
        self.assertEqual(len(self.receipt.discounts), nr_items)

    @parameterized.expand([(1,), (3,)])
    def test_assert_product_name_of_each_added_discount(self, nr_items):
        self._set_up_kw_args_of_each_discount_in_list(nr_items)
        for i in range(nr_items):
            self.receipt.add_discount(mdl_objcts.Discount(**self.kw_args_disc_list[i]))
        self.assertListEqual([self.receipt.discounts[i].product.name for i in range(nr_items)],
                             [self.product_dicts_list[i]['name'] for i in range(nr_items)])

    @parameterized.expand([(1,), (4,)])
    def test_assert_description_of_each_added_discount(self, nr_items):
        self._set_up_kw_args_of_each_discount_in_list(nr_items)
        for i in range(nr_items):
            self.receipt.add_discount(mdl_objcts.Discount(**self.kw_args_disc_list[i]))
        self.assertListEqual([self.receipt.discounts[i].description for i in range(nr_items)],
                             [self.kw_args_disc_list[i]['description'] for i in range(nr_items)])

    @parameterized.expand([(1,), (2, )])
    def test_assert_discount_amount_of_each_added_discount(self, nr_items):
        self._set_up_kw_args_of_each_discount_in_list(nr_items)
        for i in range(nr_items):
            self.receipt.add_discount(mdl_objcts.Discount(**self.kw_args_disc_list[i]))
        self.assertListEqual([self.receipt.discounts[i].discount_amount for i in range(nr_items)],
                             [self.kw_args_disc_list[i]['discount_amount'] for i in range(nr_items)])

    @parameterized.expand([(1,), (5,)])
    def test_assert_total_price_after_adding_products(self, nr_items):
        self._set_up_kw_args_of_each_product_in_list(nr_items)
        for i in range(nr_items):
            self.receipt.add_product(**self.kw_args_list[i])
        expected_total_price = round(sum([self.kw_args_list[i]['total_price'] for i in range(nr_items)]), 2)
        self.assertAlmostEqual(self.receipt.total_price(), expected_total_price, places=2)

    @parameterized.expand([(1,), (7,)])
    def test_assert_total_price_after_adding_discounts(self, nr_discounts):
        self._set_up_kw_args_of_each_discount_in_list(nr_discounts)
        for i in range(nr_discounts):
            self.receipt.add_discount(mdl_objcts.Discount(**self.kw_args_disc_list[i]))
        expected_total_discounts = round(sum([self.kw_args_disc_list[i]['discount_amount'] for i in range(nr_discounts)]), 2)
        self.assertAlmostEqual(self.receipt.total_price(), expected_total_discounts, places=2)

    @parameterized.expand([(1, 1), (1, 7), (7, 1)])
    def test_assert_total_price_after_adding_products_and_discounts(self, nr_items, nr_discounts):
        self._set_up_kw_args_of_each_product_in_list(nr_items)
        self._set_up_kw_args_of_each_discount_in_list(nr_discounts)
        for i in range(nr_items):
            self.receipt.add_product(**self.kw_args_list[i])
        for i in range(nr_discounts):
            self.receipt.add_discount(mdl_objcts.Discount(**self.kw_args_disc_list[i]))
        total_price = round(sum([self.kw_args_list[i]['total_price'] for i in range(nr_items)]), 2)
        total_discounts = round(sum([self.kw_args_disc_list[i]['discount_amount'] for i in range(nr_discounts)]), 2)
        expected_total_price =  total_price + total_discounts
        self.assertAlmostEqual(self.receipt.total_price(), expected_total_price, places=2)
