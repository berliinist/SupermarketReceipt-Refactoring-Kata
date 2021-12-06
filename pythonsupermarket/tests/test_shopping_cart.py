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

    @parameterized.expand([(1,), (7,)])
    def test_assert_add_item_quantity_yields_correct_number_of_different_items_and_quantities_each(self, nr_items):
        self._set_up_kw_args_of_each_productquantity_in_list(nr_items)
        for i in range(nr_items):
            self.shoppingcart.add_item_quantity(**self.kw_args_list[i])
        expected_names = [self.product_dicts_list[i]['name'] for i in range(nr_items)]
        expected_quantities = [self.kw_args_list[i]['quantity'] for i in range(nr_items)]

        self.assertListEqual([self.shoppingcart.items[i].product.name for i in range(nr_items)], expected_names)
        self.assertListEqual([self.shoppingcart.items[i].quantity for i in range(nr_items)], expected_quantities)

    @parameterized.expand([(1,), (7,)])
    def test_assert_add_item_quantity_yields_correct_number_of_total_quantities_in_each_product(self, nr_items):
        self._set_up_kw_args_of_each_productquantity_in_list(nr_items)
        for i in range(nr_items):
            self.shoppingcart.add_item_quantity(**self.kw_args_list[i])
        expected_dict = {self.kw_args_list[i]['product']: self.kw_args_list[i]['quantity'] for i in range(nr_items)}
        self.assertDictEqual(self.shoppingcart.product_quantities, expected_dict)

    def _add_items_initially_and_repeatedly_and_return_expected_cart_items_lists(self, nr_items):
        for i in range(nr_items):
            self.shoppingcart.add_item_quantity(**self.kw_args_list[i])
        add_qts = [{'product': self.kw_args_list[i]['product'],
                    'quantity': random.randrange(0, 5, 1)} for i in range(nr_items - 1)]
        for i in range(len(add_qts)):
            self.shoppingcart.add_item_quantity(**add_qts[i])
        expected_names_list = [self.product_dicts_list[i]['name'] for i in range(nr_items)] + \
                              [add_qts[i]['product'].name for i in range(nr_items - 1)]
        expected_qts_list = [self.kw_args_list[i]['quantity'] for i in range(nr_items)] + \
                            [add_qts[i]['quantity'] for i in range(nr_items-1)]
        return expected_names_list, expected_qts_list

    def _add_items_initally_and_repeatedly_and_return_expected_product_quantities(self, nr_items):
        for i in range(nr_items):
            self.shoppingcart.add_item_quantity(**self.kw_args_list[i])
        add_qts = [{'product': self.kw_args_list[i]['product'],
                    'quantity': random.randrange(0, 5, 1)} for i in range(nr_items - 1)]
        for i in range(len(add_qts)):
            self.shoppingcart.add_item_quantity(**add_qts[i])
        expected = {self.kw_args_list[i]['product']: self.kw_args_list[i]['quantity'] + add_qts[i]['quantity']
                    for i in range(nr_items - 1)}
        expected.update({self.kw_args_list[nr_items - 1]['product']: self.kw_args_list[nr_items -1]['quantity']})
        return expected

    @parameterized.expand([(1,), (6,)])
    def test_assert_add_item_quantity_repeatedly_to_some_items_yields_items_quantities_correctly(self, nr_items):
        self._set_up_kw_args_of_each_productquantity_in_list(nr_items)
        expected_names_list, expected_qts_list = \
            self._add_items_initially_and_repeatedly_and_return_expected_cart_items_lists(nr_items)

        self.assertListEqual([self.shoppingcart.items[i].product.name for i in range(nr_items * 2 - 1)],
                             expected_names_list)
        self.assertListEqual([self.shoppingcart.items[i].quantity for i in range(nr_items * 2 - 1)],
                             expected_qts_list)

    @parameterized.expand([(1,), (5,)])
    def test_assert_add_item_quantity_repeatedly_to_some_items_yields_product_quantities_correctly(self, nr_items):
        self._set_up_kw_args_of_each_productquantity_in_list(nr_items)
        expected_dict = self._add_items_initally_and_repeatedly_and_return_expected_product_quantities(nr_items)
        self.assertDictEqual(self.shoppingcart.product_quantities, expected_dict)

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
        self.handle_kw_args['receipt'].add_product(p_in_cart, 5, 3,
                                                   15 * 3)  # REFACTOR: parameterize these constant values to more variable
        self.shoppingcart.handle_offers(**self.handle_kw_args)

        self.assertListEqual(self.handle_kw_args['receipt'].discounts, [])

    def test_assert_correct_multiple_discounts_length_unaffected_by_repeat_of_add_same_item_quantity(self):
        products = [mdl_objcts.Product(f'Special{i}', mdl_objcts.ProductUnit.EACH) for i in range(3)]
        self.offers = {product: mdl_objcts.Offer(mdl_objcts.SpecialOfferType.TEN_PERCENT_DISCOUNT, product, 12) for product in products}
        self.handle_kw_args = {'receipt': Receipt(), 'offers': self.offers, 'catalog': FakeCatalog()}
        unit_prices = []
        for p in products:
            unit_prices.append(random.random() * 10)
            self.handle_kw_args['catalog'].add_product(p, unit_prices[-1])
        quantities = []
        for i in range(len(products)):
            quantities.append(random.randrange(1, 4, 1))
            self.shoppingcart.add_item_quantity(products[i], quantities[i])
            self.handle_kw_args['receipt'].add_product(
                products[i], quantities[i], unit_prices[i], quantities[i] * unit_prices[i])

        self.shoppingcart.handle_offers(**self.handle_kw_args)

        self.assertEqual(len(self.handle_kw_args['receipt'].discounts), len(products))


class SharedHandleOffersSetups:
    def _set_up_kw_args_and_add_product(self, name, unit_price, offer_arg, quantity, p_type, offer_type):
        self.product = mdl_objcts.Product(name, p_type)
        self.offers = {self.product: mdl_objcts.Offer(offer_type, self.product, offer_arg)}
        self.handle_kw_args = {'receipt': Receipt(), 'offers': self.offers, 'catalog': FakeCatalog()}
        self.unit_price = unit_price
        self.handle_kw_args['catalog'].add_product(self.product, self.unit_price)

        self.shoppingcart = ShoppingCart()
        self.shoppingcart.add_item_quantity(self.product, quantity)

        self.handle_kw_args['receipt'].add_product(self.product, quantity, self.unit_price, quantity * self.unit_price)

        self.shoppingcart.handle_offers(**self.handle_kw_args)


class TestShoppingCartHandleOffersThreeForTwo(unittest.TestCase, SharedHandleOffersSetups):
    def test_no_discount_for_too_little_items_in_cart(self):
        self._set_up_kw_args_and_add_product('toothbrush', 0.99, '', 2, mdl_objcts.ProductUnit.EACH,
                                             mdl_objcts.SpecialOfferType.THREE_FOR_TWO)
        self.assertListEqual(self.handle_kw_args['receipt'].discounts, [])

    def test_discount_list_for_pay_two_for_three_items_in_cart(self):
        self._set_up_kw_args_and_add_product('toothbrush', 0.99, '', 3, mdl_objcts.ProductUnit.EACH,
                                             mdl_objcts.SpecialOfferType.THREE_FOR_TWO)
        self.assertEqual(len(self.handle_kw_args['receipt'].discounts), 1)

    def test_discount_correct_amount_to_pay_two_for_three_items_in_cart(self):
        self._set_up_kw_args_and_add_product('toothbrush', 0.99, '', 3, mdl_objcts.ProductUnit.EACH,
                                             mdl_objcts.SpecialOfferType.THREE_FOR_TWO)

        self.assertAlmostEqual(self.handle_kw_args['receipt'].discounts[0].discount_amount,
                               -self.unit_price, places=3)

        # TODO: expected total value


class TestShoppingCartHandleOffersOfPercentDiscount(unittest.TestCase, SharedHandleOffersSetups):
    def test_discount_list_length_of_one_for_specific_item_in_cart(self):
        self._set_up_kw_args_and_add_product('rice', 2.49, 10, 1, mdl_objcts.ProductUnit.EACH, mdl_objcts.SpecialOfferType.TEN_PERCENT_DISCOUNT)
        self.assertEqual(len(self.handle_kw_args['receipt'].discounts), 1)

    @parameterized.expand([('rice', 2.49, 10, mdl_objcts.ProductUnit.EACH), ('apple', 1.99, 20, mdl_objcts.ProductUnit.KILO)])
    def test_discount_correct_percent_for_specific_item_in_cart(self, product, unit_price, percent, p_type):
        self._set_up_kw_args_and_add_product(product, unit_price, percent, 1, p_type, mdl_objcts.SpecialOfferType.TEN_PERCENT_DISCOUNT)
        expected = -percent / 100 * self.unit_price
        self.assertAlmostEqual(self.handle_kw_args['receipt'].discounts[0].discount_amount, expected, places=3)

        # TODO: expected total value


class TestShoppingCartHandleOffersOfTwoForAmount(unittest.TestCase, SharedHandleOffersSetups):
    def test_discounts_for_two_quantities_item_with_offer_price_two_for_amount(self):
        self._set_up_kw_args_and_add_product('cherrytomatoes', 0.69, 0.99, 2, mdl_objcts.ProductUnit.EACH,
                                             mdl_objcts.SpecialOfferType.TWO_FOR_AMOUNT)
        expected = -0.39  # TODO: do math to get this value
        self.assertAlmostEqual(self.handle_kw_args['receipt'].discounts[0].discount_amount, expected, places=3)

        # TODO: expected total value.

    def test_no_discounts_for_less_quantities_item_with_offer_price_two_for_amount(self):
        self._set_up_kw_args_and_add_product('cherrytomatoes', 0.69, 0.99, 1, mdl_objcts.ProductUnit.EACH,
                                             mdl_objcts.SpecialOfferType.TWO_FOR_AMOUNT)
        self.assertListEqual(self.handle_kw_args['receipt'].discounts, [])


class TestShoppingCartHandleOffersOfFiveForAmount(unittest.TestCase, SharedHandleOffersSetups):
    def test_discounts_for_five_quantities_item_with_offer_price_five_for_amount(self):
        self._set_up_kw_args_and_add_product('toothpaste', 1.79, 7.49, 5, mdl_objcts.ProductUnit.EACH,
                                             mdl_objcts.SpecialOfferType.FIVE_FOR_AMOUNT)
        expected = -1.46  # TODO: do math to get this value
        self.assertAlmostEqual(self.handle_kw_args['receipt'].discounts[0].discount_amount, expected, places=3)

        # TODO: expected total value.

    def test_no_discounts_for_less_quantities_item_with_offer_price_five_for_amount(self):
        self._set_up_kw_args_and_add_product('toothpaste', 1.79, 7.49, 4, mdl_objcts.ProductUnit.EACH,
                                             mdl_objcts.SpecialOfferType.FIVE_FOR_AMOUNT)
        self.assertListEqual(self.handle_kw_args['receipt'].discounts, [])


class TestShoppingCartHandleOffersOfDiscountedBundles(unittest.TestCase):  # TODO: this needs some serious refactoring.
    def setUp(self):
        self.products = [mdl_objcts.Product('toothpaste', mdl_objcts.ProductUnit.EACH),
                         mdl_objcts.Product('toothbrush', mdl_objcts.ProductUnit.EACH)]
        self.bndl_discounts = [round(random.random() * 10, 2) for i in range(len(self.products))]
        self.unit_prices = [round(random.random() * 5, 2) for _ in range(len(self.products))]

        self.offers = {self.products[i]: mdl_objcts.Offer(
            mdl_objcts.SpecialOfferType.BUNDLE_DISCOUNT, self.products[i], self.bndl_discounts[i]
        ) for i in range(len(self.products))}
        self.handle_kw_args = {'receipt': Receipt(), 'offers': self.offers, 'catalog': FakeCatalog()}
        for i in range(len(self.products)):
            self.handle_kw_args['catalog'].add_product(self.products[i], self.unit_prices[i])
        self.shoppingcart = ShoppingCart()

    def test_two_unique_product_items_with_quantity_of_one_each_get_full_bundle_discount(self):
        quantities = [1, 1]
        for i in range(len(self.products)):
            self.shoppingcart.add_item_quantity(self.products[i], quantities[i])
            self.handle_kw_args['receipt'].add_product(
                self.products[i], quantities[i], self.unit_prices[i], quantities[i] * self.unit_prices[i])
        self.shoppingcart.handle_offers(**self.handle_kw_args)
        total_price = self.handle_kw_args['receipt'].total_price()
        expected_discount = sum([self.unit_prices[i] * -self.bndl_discounts[i] / 100 for i in range(len(self.products))])
        total_expected_price = sum([self.unit_prices[i] * quantities[i] for i in range(len(self.products))]) + expected_discount

        self.assertEqual(expected_discount,
                         sum([self.handle_kw_args['receipt'].discounts[i].discount_amount for i in range(len(self.products))]))
        self.assertAlmostEqual(total_price, total_expected_price, places=2)

    def test_two_unique_product_items_with_multiple_quantities_of_one_each_get_partial_bundle_discount(self):
        quantities = [random.randrange(1, 8, 1) for _ in range(len(self.products))]
        for i in range(len(self.products)):
            self.shoppingcart.add_item_quantity(self.products[i], quantities[i])
            self.handle_kw_args['receipt'].add_product(
                self.products[i], quantities[i], self.unit_prices[i], quantities[i] * self.unit_prices[i])
        self.shoppingcart.handle_offers(**self.handle_kw_args)
        total_price = self.handle_kw_args['receipt'].total_price()
        expected_discount = sum([self.unit_prices[i] * -self.bndl_discounts[i] / 100 for i in range(len(self.products))])
        total_expected_price = sum([self.unit_prices[i] * quantities[i] for i in range(len(self.products))]) + expected_discount

        self.assertEqual(expected_discount,
                         sum([self.handle_kw_args['receipt'].discounts[i].discount_amount for i in range(len(self.products))]))
        self.assertAlmostEqual(total_price, total_expected_price, places=2)
