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
        self.handle_kw_args = {'receipt': Receipt(), 'offers': {}, 'catalog': FakeCatalog()}

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
        self.shoppingcart.handle_offers(**self.handle_kw_args)
        self.assertListEqual(self.handle_kw_args['receipt'].discounts, [])

    def test_discounts_not_added_if_handle_offers_without_offers(self):
        self._set_up_kw_args_of_each_productquantity_in_list(nr_items=1)
        self.shoppingcart.add_item_quantity(**self.kw_args_list[0])

        self.shoppingcart.handle_offers(**self.handle_kw_args)
        self.assertListEqual(self.handle_kw_args['receipt'].discounts, [])

    def test_no_discounts_for_wrong_items_in_cart(self):
        p_not_in_cart = mdl_objcts.Product("toothbrush", mdl_objcts.ProductUnit.EACH)
        p_in_cart = mdl_objcts.Product("toothpaste", mdl_objcts.ProductUnit.EACH)
        self.handle_kw_args.update({'offers':
            {p_not_in_cart: mdl_objcts.Offer(mdl_objcts.SpecialOfferType.THREE_FOR_TWO, p_not_in_cart, 10.0)},
                                    'catalog': FakeCatalog()})
        for p, unit_price in [(p_not_in_cart, 9.99), (p_in_cart, 3)]:
            self.handle_kw_args['catalog'].add_product(p, unit_price)
        self.shoppingcart.add_item_quantity(p_in_cart, 5)
        self.shoppingcart.handle_offers(**self.handle_kw_args)

        self.assertListEqual(self.handle_kw_args['receipt'].discounts, [])

    def test_assert_correct_multiple_discounts_length_for_all_items_offered(self):
        products = [mdl_objcts.Product(f'Special{i}', mdl_objcts.ProductUnit.EACH) for i in range(3)]
        self.offers = {product: mdl_objcts.Offer(mdl_objcts.SpecialOfferType.TEN_PERCENT_DISCOUNT, product, 12) for product in products}
        self.handle_kw_args = {'receipt': Receipt(), 'offers': self.offers, 'catalog': FakeCatalog()}
        for p in products:
            self.handle_kw_args['catalog'].add_product(p, random.random() * 10)
        for i in range(len(products)):
            self.shoppingcart.add_item_quantity(products[i], random.randrange(1, 4, 1))
        self.shoppingcart.handle_offers(**self.handle_kw_args)

        self.assertEqual(len(self.handle_kw_args['receipt'].discounts), len(products))


class TestShoppingCartHandleOffersThreeForTwo(unittest.TestCase):
    def setUp(self):
        self.toothbrush = mdl_objcts.Product('toothbrush', mdl_objcts.ProductUnit.EACH)
        self.offers = {self.toothbrush: mdl_objcts.Offer(mdl_objcts.SpecialOfferType.THREE_FOR_TWO, self.toothbrush, '')}
        self.handle_kw_args = {'receipt': Receipt(), 'offers': self.offers, 'catalog': FakeCatalog()}
        self.toothbrush_unit_price = 0.99
        self.handle_kw_args['catalog'].add_product(self.toothbrush, self.toothbrush_unit_price)

        self.shoppingcart = ShoppingCart()

    def test_no_discount_for_too_little_items_in_cart(self):
        self.shoppingcart.add_item_quantity(self.toothbrush, 2)
        self.shoppingcart.handle_offers(**self.handle_kw_args)
        self.assertListEqual(self.handle_kw_args['receipt'].discounts, [])

    def test_discount_list_for_pay_two_for_three_items_in_cart(self):
        self.shoppingcart.add_item_quantity(self.toothbrush, 3)
        self.shoppingcart.handle_offers(**self.handle_kw_args)

        self.assertEqual(len(self.handle_kw_args['receipt'].discounts), 1)

    def test_discount_correct_amount_to_pay_two_for_three_items_in_cart(self):
        self.shoppingcart.add_item_quantity(self.toothbrush, 3)
        self.shoppingcart.handle_offers(**self.handle_kw_args)

        self.assertAlmostEqual(self.handle_kw_args['receipt'].discounts[0].discount_amount,
                               -self.toothbrush_unit_price, places=3)


class TestShoppingCartHandleOffersOfPercentDiscount(unittest.TestCase):

    def _set_up_kw_args_and_add_product(self, p_name, unit_price, percentage, type):
        self.product = mdl_objcts.Product(p_name, type)
        self.offers = {self.product: mdl_objcts.Offer(mdl_objcts.SpecialOfferType.TEN_PERCENT_DISCOUNT,
                                                      self.product,
                                                      percentage)}
        self.handle_kw_args = {'receipt': Receipt(), 'offers': self.offers, 'catalog': FakeCatalog()}
        self.unit_price = unit_price
        self.handle_kw_args['catalog'].add_product(self.product, self.unit_price)

        self.shoppingcart = ShoppingCart()
        self.shoppingcart.add_item_quantity(self.product, 1)
        self.shoppingcart.handle_offers(**self.handle_kw_args)

    def test_discount_list_length_of_one_for_specific_item_in_cart(self):
        self._set_up_kw_args_and_add_product('rice', 2.49, 10, mdl_objcts.ProductUnit.EACH)
        self.assertEqual(len(self.handle_kw_args['receipt'].discounts), 1)

    @parameterized.expand([('rice', 2.49, 10, mdl_objcts.ProductUnit.EACH), ('apple', 1.99, 20, mdl_objcts.ProductUnit.KILO)])
    def test_discount_correct_percent_for_specific_item_in_cart(self, product, unit_price, percent, type):
        self._set_up_kw_args_and_add_product(product, unit_price, percent, type)
        expected = -percent / 100 * self.unit_price
        self.assertAlmostEqual(self.handle_kw_args['receipt'].discounts[0].discount_amount, expected, places=3)


class TestShoppingCartHandleOffersOfTwoForAmount(unittest.TestCase):

    def _set_up_kw_args_and_add_product(self, unit_price, offer_price, quantity):
        self.product = mdl_objcts.Product('cherrytomatoes', mdl_objcts.ProductUnit.EACH)
        self.offers = {self.product: mdl_objcts.Offer(mdl_objcts.SpecialOfferType.TWO_FOR_AMOUNT,
                                                      self.product,
                                                      offer_price)}
        self.handle_kw_args = {'receipt': Receipt(), 'offers': self.offers, 'catalog': FakeCatalog()}
        self.unit_price = unit_price
        self.handle_kw_args['catalog'].add_product(self.product, self.unit_price)

        self.shoppingcart = ShoppingCart()
        self.shoppingcart.add_item_quantity(self.product, quantity)
        self.shoppingcart.handle_offers(**self.handle_kw_args)

    def test_discounts_for_two_quantities_item_with_offer_price_two_for_amount(self):
        self._set_up_kw_args_and_add_product(0.69, 0.99, 2)
        expected = -0.39  # TODO: do math to get this value
        self.assertAlmostEqual(self.handle_kw_args['receipt'].discounts[0].discount_amount, expected, places=3)

    def test_no_discounts_for_less_quantities_item_with_offer_price_two_for_amount(self):
        self._set_up_kw_args_and_add_product(0.69, 0.99, 1)
        self.assertListEqual(self.handle_kw_args['receipt'].discounts, [])


class TestShoppingCartHandleOffersOfFiveForAmount(unittest.TestCase):
    def _set_up_kw_args_and_add_product(self, unit_price, offer_price, quantity):
        self.product = mdl_objcts.Product('toothpaste', mdl_objcts.ProductUnit.EACH)
        self.offers = {self.product: mdl_objcts.Offer(mdl_objcts.SpecialOfferType.FIVE_FOR_AMOUNT,
                                                      self.product,
                                                      offer_price)}
        self.handle_kw_args = {'receipt': Receipt(), 'offers': self.offers, 'catalog': FakeCatalog()}
        self.unit_price = unit_price
        self.handle_kw_args['catalog'].add_product(self.product, self.unit_price)

        self.shoppingcart = ShoppingCart()
        self.shoppingcart.add_item_quantity(self.product, quantity)
        self.shoppingcart.handle_offers(**self.handle_kw_args)

    def test_discounts_for_five_quantities_item_with_offer_price_five_for_amount(self):
        self._set_up_kw_args_and_add_product(1.79, 7.49, 5)
        expected = -1.46  # TODO: do math to get this value
        self.assertAlmostEqual(self.handle_kw_args['receipt'].discounts[0].discount_amount, expected, places=3)

    def test_no_discounts_for_less_quantities_item_with_offer_price_five_for_amount(self):
        self._set_up_kw_args_and_add_product(1.79, 7.49, 4)
        self.assertListEqual(self.handle_kw_args['receipt'].discounts, [])
