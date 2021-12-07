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
        self.receiptitem = receipt.ReceiptItem(**cp.copy(self.kwargs))

    def test_asserts_quantity(self):
        self.assertEqual(self.receiptitem.quantity, self.kwargs['quantity'])

    def test_asserts_unit_price(self):
        self.assertEqual(self.receiptitem.unit_price, self.kwargs['unit_price'])

    def test_asserts_total_price(self):
        self.assertEqual(self.receiptitem.total_price, self.kwargs['total_price'])

    def test_asserts_item_correctly(self):
        self.assertEqual(self.receiptitem.item, self.kwargs['item'])

    def test_rejects_setting_item(self):
        with self.assertRaises(AttributeError):
            self.receiptitem.item = self.kwargs['item']

    def test_rejects_setting_quantity(self):
        with self.assertRaises(AttributeError):
            self.receiptitem.quantity = self.kwargs['quantity']

    def test_rejects_setting_unit_price(self):
        with self.assertRaises(AttributeError):
            self.receiptitem.unit_price = self.kwargs['unit_price']

    def test_rejects_setting_total_price(self):
        with self.assertRaises(AttributeError):
            self.receiptitem.total_price = self.kwargs['total_price']


class TestReceiptIntegration(unittest.TestCase):
    def setUp(self):
        self.receipt = receipt.Receipt()

    def _setup_list_kwargs_of_each_item(self, nr_items):
        self.prod_kwargs_list = [setup_product_kwargs() for _ in range(nr_items)]
        self.kwargs_list = [{'item': mdl_objcts.ProductInfo(**cp.deepcopy(self.prod_kwargs_list[i])),
                             'quantity': random.randrange(1, 100, 1),
                             'unit_price': round(random.random() * 100, 2),
                             'total_price': round(random.random() * 200, 2)} for i, _ in enumerate(range(nr_items))]

    def _setup_list_kwargs_of_each_discount(self, nr_items):
        self.prod_kwargs_list = [setup_product_kwargs() for _ in range(nr_items)]
        self.kw_args_disc_list = [
            {'product': mdl_objcts.ProductInfo(**cp.deepcopy(self.prod_kwargs_list[i])),
             'description': f'Some discount number {i+1}',
             'discount_amount': round(random.random() * -10, 2)} for i, _ in enumerate(range(nr_items))]

    def test_initial_receipt_items_returns_empty(self):
        self.assertListEqual(self.receipt.items, [])

    def test_initial_receipt_discounts_returns_empty(self):
        self.assertListEqual(self.receipt.discounts, [])

    def test_initial_total_price_returns_empty(self):
        self.assertEqual(self.receipt.total_price(), 0)

    def test_item_added_is_an_instance_of_receipt_item(self):
        self._setup_list_kwargs_of_each_item(1)
        self.receipt.add_item(**self.kwargs_list[0])
        self.assertIsInstance(self.receipt.items[0], receipt.ReceiptItem)

    @parameterized.expand([(1,), (10,)])
    def test_assert_number_of_items(self, nr_items):
        self._setup_list_kwargs_of_each_item(nr_items)
        for i in range(nr_items):
            self.receipt.add_item(**self.kwargs_list[i])
        self.assertEqual(len(self.receipt.items), nr_items)

    @parameterized.expand([(1,), (8,)])
    def test_assert_correct_order_of_items(self, nr_items):
        self._setup_list_kwargs_of_each_item(nr_items)
        for i in range(nr_items):
            self.receipt.add_item(**self.kwargs_list[i])
        self.assertListEqual([self.receipt.items[i].item for i in range(nr_items)],
                             [self.kwargs_list[i]['item'] for i in range(nr_items)])

    @parameterized.expand([(1,), (8,)])
    def test_assert_names_of_items(self, nr_items):
        self._setup_list_kwargs_of_each_item(nr_items)
        for i in range(nr_items):
            self.receipt.add_item(**self.kwargs_list[i])
        self.assertListEqual([self.receipt.items[i].item.name for i in range(nr_items)],
                             [self.prod_kwargs_list[i]['name'] for i in range(nr_items)])

    @parameterized.expand([(1,), (7,)])
    def test_assert_units_of_items(self, nr_items):
        self._setup_list_kwargs_of_each_item(nr_items)
        for i in range(nr_items):
            self.receipt.add_item(**self.kwargs_list[i])
        self.assertListEqual([self.receipt.items[i].item.unit for i in range(nr_items)],
                             [self.prod_kwargs_list[i]['unit'] for i in range(nr_items)])

    @parameterized.expand([(1,), (6,)])
    def test_assert_quantities_of_items(self, nr_items):
        self._setup_list_kwargs_of_each_item(nr_items)
        for i in range(nr_items):
            self.receipt.add_item(**self.kwargs_list[i])
        self.assertListEqual([self.receipt.items[i].quantity for i in range(nr_items)],
                             [self.kwargs_list[i]['quantity'] for i in range(nr_items)])

    @parameterized.expand([(1,), (6,)])
    def test_assert_unit_prices_of_items(self, nr_items):
        self._setup_list_kwargs_of_each_item(nr_items)
        for i in range(nr_items):
            self.receipt.add_item(**self.kwargs_list[i])
        self.assertListEqual([self.receipt.items[i].unit_price for i in range(nr_items)],
                             [self.kwargs_list[i]['unit_price'] for i in range(nr_items)])

    @parameterized.expand([(1,), (5,)])
    def test_assert_total_price_of_each_item(self, nr_items):
        self._setup_list_kwargs_of_each_item(nr_items)
        for i in range(nr_items):
            self.receipt.add_item(**self.kwargs_list[i])
        self.assertListEqual([self.receipt.items[i].total_price for i in range(nr_items)],
                             [self.kwargs_list[i]['total_price'] for i in range(nr_items)])

    @parameterized.expand([(1,), (4,)])
    def test_assert_no_discounts_if_no_discounts_added(self, nr_items):
        self._setup_list_kwargs_of_each_discount(nr_items)
        for i in range(nr_items):
            self.receipt.add_discount(None)
        self.assertEqual(len(self.receipt.discounts), 0)

    @parameterized.expand([(1,), (4,)])
    def test_assert_correct_number_of_discounts_after_added(self, nr_discounts):
        self._setup_list_kwargs_of_each_discount(nr_discounts)
        for i in range(nr_discounts):
            self.receipt.add_discount(mdl_objcts.Discount(**self.kw_args_disc_list[i]))
        self.assertEqual(len(self.receipt.discounts), nr_discounts)

    @parameterized.expand([(1,), (4,)])
    def test_assert_correct_order_of_discounts(self, nr_discounts):
        self._setup_list_kwargs_of_each_discount(nr_discounts)
        discounts = [mdl_objcts.Discount(**self.kw_args_disc_list[i]) for i in range(nr_discounts)]
        for i in range(nr_discounts):
            self.receipt.add_discount(discounts[i])
        self.assertListEqual(self.receipt.discounts, discounts)

    @parameterized.expand([(1,), (3,)])
    def test_assert_names_of_discounts(self, nr_items):
        self._setup_list_kwargs_of_each_discount(nr_items)
        for i in range(nr_items):
            self.receipt.add_discount(mdl_objcts.Discount(**self.kw_args_disc_list[i]))
        self.assertListEqual([self.receipt.discounts[i].product.name for i in range(nr_items)],
                             [self.prod_kwargs_list[i]['name'] for i in range(nr_items)])

    @parameterized.expand([(1,), (4,)])
    def test_assert_descriptions_of_discounts(self, nr_discounts):
        self._setup_list_kwargs_of_each_discount(nr_discounts)
        for i in range(nr_discounts):
            self.receipt.add_discount(mdl_objcts.Discount(**self.kw_args_disc_list[i]))
        self.assertListEqual([self.receipt.discounts[i].description for i in range(nr_discounts)],
                             [self.kw_args_disc_list[i]['description'] for i in range(nr_discounts)])

    @parameterized.expand([(1,), (2, )])
    def test_assert_discount_amounts(self, nr_discounts):
        self._setup_list_kwargs_of_each_discount(nr_discounts)
        for i in range(nr_discounts):
            self.receipt.add_discount(mdl_objcts.Discount(**self.kw_args_disc_list[i]))
        self.assertListEqual([self.receipt.discounts[i].discount_amount for i in range(nr_discounts)],
                             [self.kw_args_disc_list[i]['discount_amount'] for i in range(nr_discounts)])

    @parameterized.expand([(1,), (5,)])
    def test_assert_receipt_total_price_if_items_only(self, nr_items):
        self._setup_list_kwargs_of_each_item(nr_items)
        for i in range(nr_items):
            self.receipt.add_item(**self.kwargs_list[i])
        expected = round(sum([self.kwargs_list[i]['total_price'] for i in range(nr_items)]), 2)
        self.assertAlmostEqual(self.receipt.total_price(), expected, places=2)

    @parameterized.expand([(1,), (7,)])
    def test_assert_receipt_total_price_if_discounts_only(self, nr_discounts):
        self._setup_list_kwargs_of_each_discount(nr_discounts)
        for i in range(nr_discounts):
            self.receipt.add_discount(mdl_objcts.Discount(**self.kw_args_disc_list[i]))
        expected = round(sum([self.kw_args_disc_list[i]['discount_amount'] for i in range(nr_discounts)]), 2)
        self.assertAlmostEqual(self.receipt.total_price(), expected, places=2)

    @parameterized.expand([(1, 1), (1, 7), (7, 1)])
    def test_assert_receipt_total_price_of_items_and_discounts(self, nr_items, nr_discounts):
        self._setup_list_kwargs_of_each_item(nr_items)
        self._setup_list_kwargs_of_each_discount(nr_discounts)
        for i in range(nr_items):
            self.receipt.add_item(**self.kwargs_list[i])
        for i in range(nr_discounts):
            self.receipt.add_discount(mdl_objcts.Discount(**self.kw_args_disc_list[i]))
        total_price = round(sum([self.kwargs_list[i]['total_price'] for i in range(nr_items)]), 2)
        total_discounts = round(sum([self.kw_args_disc_list[i]['discount_amount'] for i in range(nr_discounts)]), 2)
        expected_total_price =  total_price + total_discounts
        self.assertAlmostEqual(self.receipt.total_price(), expected_total_price, places=2)
