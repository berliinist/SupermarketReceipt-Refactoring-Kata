import copy as cp
import random
import unittest

from parameterized import parameterized
import pytest

from pythonsupermarket.fake_catalog import FakeCatalog
import pythonsupermarket.model_objects as mdl_objcts
from pythonsupermarket.shopping_cart import ShoppingCart
from pythonsupermarket.receipt import Receipt

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

    def test_discounts_not_added_if_handle_offers_without_product_quantities(self):
        receipt = Receipt()
        offers = {}
        catalog = FakeCatalog()

        self.shoppingcart.handle_offers(receipt, offers, catalog)
        self.assertListEqual(receipt.discounts, [])

    def test_discounts_not_added_if_handle_offers_without_offers(self):
        receipt = Receipt()
        offers = {}
        catalog = FakeCatalog()

        self._set_up_kw_args_of_each_productquantity_in_list(nr_items=1)
        self.shoppingcart.add_item_quantity(**self.kw_args_list[0])
        self.shoppingcart.handle_offers(receipt, offers, catalog)
        self.assertListEqual(receipt.discounts, [])

    def test_no_discounts_for_items_in_cart_if_handle_offers_for_other_items(self):
        receipt = Receipt()
        some_product_not_in_cart = mdl_objcts.Product("toothbrush", mdl_objcts.ProductUnit.EACH)
        offers = {some_product_not_in_cart: mdl_objcts.Offer(mdl_objcts.SpecialOfferType.THREE_FOR_TWO,
                                                             some_product_not_in_cart, 10.0)}
        some_product_in_cart = mdl_objcts.Product("toothpaste", mdl_objcts.ProductUnit.EACH)
        catalog = FakeCatalog()
        catalog.add_product(some_product_not_in_cart, 0.99)
        catalog.add_product(some_product_in_cart, 3)

        self.shoppingcart.add_item_quantity(some_product_in_cart, 3)
        self.shoppingcart.handle_offers(receipt, offers, catalog)

        self.assertListEqual(receipt.discounts, [])


class TestShoppingCartHandleOffersDifferentSpecialOffers(unittest.TestCase):
    def setUp(self):
        self.shoppingcart = ShoppingCart()

    def test_no_discounts_for_too_little_items_in_cart_if_handle_offers_for_it_three_for_two(self):
        receipt = Receipt()
        some_product_in_cart = mdl_objcts.Product("toothbrush", mdl_objcts.ProductUnit.EACH)  # TODO: rename it to unique_product?
        offers = {some_product_in_cart: mdl_objcts.Offer(mdl_objcts.SpecialOfferType.THREE_FOR_TWO, some_product_in_cart, 'unused')}
        catalog = FakeCatalog()
        catalog.add_product(some_product_in_cart, 0.99)

        self.shoppingcart.add_item_quantity(some_product_in_cart, 2)
        self.shoppingcart.handle_offers(receipt, offers, catalog)

        self.assertListEqual(receipt.discounts, [])

    def test_discounts_for_three_items_to_pay_for_two_in_cart(self):
        receipt = Receipt()
        some_product_in_cart = mdl_objcts.Product("toothbrush", mdl_objcts.ProductUnit.EACH)  # TODO: rename it to unique_product?
        offers = {some_product_in_cart: mdl_objcts.Offer(mdl_objcts.SpecialOfferType.THREE_FOR_TWO, some_product_in_cart, 'unused')}
        catalog = FakeCatalog()
        catalog.add_product(some_product_in_cart, 0.99)
        self.shoppingcart.add_item_quantity(some_product_in_cart, 3)

        self.shoppingcart.handle_offers(receipt, offers, catalog)

        self.assertEqual(len(receipt.discounts), 1)
        expected_discount_amount = -0.99
        self.assertAlmostEqual(receipt.discounts[0].discount_amount, expected_discount_amount, places=3)

    def test_discounts_for_ten_percent_discount_for_specific_item_in_cart(self):
        receipt = Receipt()
        some_product_in_cart = mdl_objcts.Product("rice", mdl_objcts.ProductUnit.EACH)  # TODO: rename it to unique_product?
        offers = {some_product_in_cart: mdl_objcts.Offer(mdl_objcts.SpecialOfferType.TEN_PERCENT_DISCOUNT, some_product_in_cart, 10.0)}
        catalog = FakeCatalog()
        catalog.add_product(some_product_in_cart, 2.49)
        self.shoppingcart.add_item_quantity(some_product_in_cart, 1)

        self.shoppingcart.handle_offers(receipt, offers, catalog)

        self.assertEqual(len(receipt.discounts), 1)
        expected_discount_amount = -0.10 * 2.49
        self.assertAlmostEqual(receipt.discounts[0].discount_amount, expected_discount_amount, places=3)

    def test_discounts_for_twenty_percent_discount_for_specific_item_in_cart(self):
        receipt = Receipt()
        some_product_in_cart = mdl_objcts.Product("apples", mdl_objcts.ProductUnit.KILO)  # TODO: rename it to unique_product?
        offers = {some_product_in_cart: mdl_objcts.Offer(mdl_objcts.SpecialOfferType.TEN_PERCENT_DISCOUNT, some_product_in_cart, 20.0)}
        catalog = FakeCatalog()
        catalog.add_product(some_product_in_cart, 2.49)
        self.shoppingcart.add_item_quantity(some_product_in_cart, 1)

        self.shoppingcart.handle_offers(receipt, offers, catalog)

        self.assertEqual(len(receipt.discounts), 1)
        expected_discount_amount = -0.20 * 2.49
        self.assertAlmostEqual(receipt.discounts[0].discount_amount, expected_discount_amount, places=3)


    def test_discounts_two_for_amount_to_pay_for_specific_items_in_cart(self):
        receipt = Receipt()
        some_product_in_cart = mdl_objcts.Product("cherrytomatoes", mdl_objcts.ProductUnit.EACH)
        offers = {some_product_in_cart: mdl_objcts.Offer(mdl_objcts.SpecialOfferType.TWO_FOR_AMOUNT, some_product_in_cart, 0.99)}
        catalog = FakeCatalog()
        catalog.add_product(some_product_in_cart, 0.69)
        self.shoppingcart.add_item_quantity(some_product_in_cart, 2)

        self.shoppingcart.handle_offers(receipt, offers, catalog)

        self.assertEqual(len(receipt.discounts), 1)
        expected_discount_amount = -0.39 # TODO: do math to get this value
        self.assertAlmostEqual(receipt.discounts[0].discount_amount, expected_discount_amount, places=3)

    def test_no_discounts_two_for_amount_to_pay_for_too_few_specific_items_in_cart(self):
        receipt = Receipt()
        some_product_in_cart = mdl_objcts.Product("cherrytomatoes", mdl_objcts.ProductUnit.EACH)
        offers = {some_product_in_cart: mdl_objcts.Offer(mdl_objcts.SpecialOfferType.TWO_FOR_AMOUNT, some_product_in_cart, 0.99)}
        catalog = FakeCatalog()
        catalog.add_product(some_product_in_cart, 0.69)
        self.shoppingcart.add_item_quantity(some_product_in_cart, 1)

        self.shoppingcart.handle_offers(receipt, offers, catalog)

        self.assertEqual(len(receipt.discounts), 0)

    def test_discounts_five_for_amount_to_pay_specific_items_in_cart(self):
        receipt = Receipt()
        some_product_in_cart = mdl_objcts.Product("toothpaste", mdl_objcts.ProductUnit.EACH)
        offers = {some_product_in_cart: mdl_objcts.Offer(mdl_objcts.SpecialOfferType.FIVE_FOR_AMOUNT, some_product_in_cart, 7.49)}
        catalog = FakeCatalog()
        catalog.add_product(some_product_in_cart, 1.79)
        self.shoppingcart.add_item_quantity(some_product_in_cart, 5)

        self.shoppingcart.handle_offers(receipt, offers, catalog)

        self.assertEqual(len(receipt.discounts), 1)
        expected_discount_amount = -1.46 # TODO: do math to get this value
        self.assertAlmostEqual(receipt.discounts[0].discount_amount, expected_discount_amount, places=3)

    def test_no_discounts_five_for_amount_to_pay_too_few_specific_items_in_cart(self):
        receipt = Receipt()
        some_product_in_cart = mdl_objcts.Product("toothpaste", mdl_objcts.ProductUnit.EACH)
        offers = {some_product_in_cart: mdl_objcts.Offer(mdl_objcts.SpecialOfferType.FIVE_FOR_AMOUNT, some_product_in_cart, 7.49)}
        catalog = FakeCatalog()
        catalog.add_product(some_product_in_cart, 1.79)
        self.shoppingcart.add_item_quantity(some_product_in_cart, 4)

        self.shoppingcart.handle_offers(receipt, offers, catalog)

        self.assertEqual(len(receipt.discounts), 0)
