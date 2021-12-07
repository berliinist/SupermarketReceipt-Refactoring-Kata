import copy as cp
import random
import unittest

from parameterized import parameterized

import pythonsupermarket.model_objects as mdl_objcts
import pythonsupermarket.receipt as receipt

from tests.shared_test_functions import setup_product_kwargs, PRODUCT_NAMEDTUPLE


class TestReceiptItem(unittest.TestCase):
    def setUp(self):
        self.kwargs = {'item':          PRODUCT_NAMEDTUPLE(**cp.deepcopy(setup_product_kwargs())),
                       'quantity':      random.randrange(1, 50, 1),
                       'unit_price':    round(random.random() * 100, 2),
                       'total_price':   round(random.random() * 200, 2)}

        self.test_class = receipt.ReceiptItem(**cp.copy(self.kwargs))

    def test_asserts_quantity(self):
        self.assertEqual(self.test_class.quantity, self.kwargs['quantity'])

    def test_asserts_unit_price(self):
        self.assertEqual(self.test_class.unit_price, self.kwargs['unit_price'])

    def test_asserts_total_price(self):
        self.assertEqual(self.test_class.total_price, self.kwargs['total_price'])

    def test_asserts_item_correctly(self):
        self.assertEqual(self.test_class.item, self.kwargs['item'])

    def test_rejects_setting_item(self):
        with self.assertRaises(AttributeError):
            self.test_class.item = self.kwargs['item']

    def test_rejects_setting_quantity(self):
        with self.assertRaises(AttributeError):
            self.test_class.quantity = self.kwargs['quantity']

    def test_rejects_setting_unit_price(self):
        with self.assertRaises(AttributeError):
            self.test_class.unit_price = self.kwargs['unit_price']

    def test_rejects_setting_total_price(self):
        with self.assertRaises(AttributeError):
            self.test_class.total_price = self.kwargs['total_price']


class TestReceiptIntegration(unittest.TestCase):
    def setUp(self):
        self.receipt = receipt.Receipt()

    def _set_up_kwargs_of_each_item_in_list(self, nr_items):
        self.product_dicts_list = [setup_product_kwargs() for _ in range(nr_items)]
        self.items = [mdl_objcts.ProductInfo(**cp.deepcopy(self.product_dicts_list[i])) for i in range(nr_items)]
        self.kw_args_list = [{'item': self.items[i],
                              'quantity': random.randrange(1, 100, 1),
                              'unit_price': round(random.random() * 100, 2),
                              'total_price': round(random.random() * 200, 2)} for i, _ in enumerate(range(nr_items))]

    def _set_up_kw_args_of_each_discount_in_list(self, nr_items):
        self.product_dicts_list = [setup_product_kwargs() for _ in range(nr_items)]
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
        self._set_up_kwargs_of_each_item_in_list(1)
        self.receipt.add_item(**self.kw_args_list[0])
        self.assertIsInstance(self.receipt.items[0], receipt.ReceiptItem)

    @parameterized.expand([(1,), (10,)])
    def test_number_of_items_added_returns_the_length_of_items_correctly(self, nr_items):
        self._set_up_kwargs_of_each_item_in_list(nr_items)
        for i in range(nr_items):
            self.receipt.add_item(**self.kw_args_list[i])
        self.assertEqual(len(self.receipt.items), nr_items)

    @parameterized.expand([(1,), (8,)])
    def test_assert_item_name_of_each_added_receipt_item(self, nr_items):  # TODO: refactor this unit test if possible
        self._set_up_kwargs_of_each_item_in_list(nr_items)
        for i in range(nr_items):
            self.receipt.add_item(**self.kw_args_list[i])
        self.assertListEqual([self.receipt.items[i].item.name for i in range(nr_items)],
                             [self.product_dicts_list[i]['name'] for i in range(nr_items)])

    @parameterized.expand([(1,), (8,)])
    def test_assert_items_added_in_correct_order(self, nr_items):
        self._set_up_kwargs_of_each_item_in_list(nr_items)
        for i in range(nr_items):
            self.receipt.add_item(**self.kw_args_list[i])
        self.assertListEqual([self.receipt.items[i].item for i in range(nr_items)], self.items)

    @parameterized.expand([(1,), (7,)])
    def test_assert_item_unit_of_each_added_receipt_item(self, nr_items):
        self._set_up_kwargs_of_each_item_in_list(nr_items)
        for i in range(nr_items):
            self.receipt.add_item(**self.kw_args_list[i])
        self.assertListEqual([self.receipt.items[i].item.unit for i in range(nr_items)],
                             [self.product_dicts_list[i]['unit'] for i in range(nr_items)])

    @parameterized.expand([(1,), (6,)])
    def test_assert_quantity_of_each_added_receipt_item(self, nr_items):
        self._set_up_kwargs_of_each_item_in_list(nr_items)
        for i in range(nr_items):
            self.receipt.add_item(**self.kw_args_list[i])
        self.assertListEqual([self.receipt.items[i].quantity for i in range(nr_items)],
                             [self.kw_args_list[i]['quantity'] for i in range(nr_items)])

    @parameterized.expand([(1,), (6,)])
    def test_assert_unit_price_of_each_added_receipt_item(self, nr_items):
        self._set_up_kwargs_of_each_item_in_list(nr_items)
        for i in range(nr_items):
            self.receipt.add_item(**self.kw_args_list[i])
        self.assertListEqual([self.receipt.items[i].unit_price for i in range(nr_items)],
                             [self.kw_args_list[i]['unit_price'] for i in range(nr_items)])

    @parameterized.expand([(1,), (5,)])
    def test_assert_total_price_of_each_added_receipt_item(self, nr_items):
        self._set_up_kwargs_of_each_item_in_list(nr_items)
        for i in range(nr_items):
            self.receipt.add_item(**self.kw_args_list[i])
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
    def test_assert_item_name_of_each_added_discount(self, nr_items):
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
    def test_assert_total_price_after_adding_items(self, nr_items):
        self._set_up_kwargs_of_each_item_in_list(nr_items)
        for i in range(nr_items):
            self.receipt.add_item(**self.kw_args_list[i])
        expected_total_price = round(sum([self.kw_args_list[i]['total_price'] for i in range(nr_items)]), 2)
        self.assertAlmostEqual(self.receipt.total_price(), expected_total_price, places=2)

    @parameterized.expand([(1,), (7,)])
    def test_assert_total_price_after_adding_discounts(self, nr_discounts):
        self._set_up_kw_args_of_each_discount_in_list(nr_discounts)
        for i in range(nr_discounts):
            self.receipt.add_discount(mdl_objcts.Discount(**self.kw_args_disc_list[i]))
        expected = round(sum([self.kw_args_disc_list[i]['discount_amount'] for i in range(nr_discounts)]), 2)
        self.assertAlmostEqual(self.receipt.total_price(), expected, places=2)

    @parameterized.expand([(1, 1), (1, 7), (7, 1)])
    def test_assert_total_price_after_adding_items_and_discounts(self, nr_items, nr_discounts):
        self._set_up_kwargs_of_each_item_in_list(nr_items)
        self._set_up_kw_args_of_each_discount_in_list(nr_discounts)
        for i in range(nr_items):
            self.receipt.add_item(**self.kw_args_list[i])
        for i in range(nr_discounts):
            self.receipt.add_discount(mdl_objcts.Discount(**self.kw_args_disc_list[i]))
        total_price = round(sum([self.kw_args_list[i]['total_price'] for i in range(nr_items)]), 2)
        total_discounts = round(sum([self.kw_args_disc_list[i]['discount_amount'] for i in range(nr_discounts)]), 2)
        expected_total_price =  total_price + total_discounts
        self.assertAlmostEqual(self.receipt.total_price(), expected_total_price, places=2)
