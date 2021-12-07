import copy as cp
import enum
import random
import unittest

from parameterized import parameterized

import pythonsupermarket.model_objects as mdl_objcts

from tests.shared_test_functions import setup_product_kwargs, PRODUCT_NAMEDTUPLE


class TestProductInfo(unittest.TestCase):
    def setUp(self):
        self.product_dict = setup_product_kwargs()
        self.product = mdl_objcts.ProductInfo(**cp.deepcopy(self.product_dict))

    def test_assert_name(self):
        self.assertEqual(self.product.name, self.product_dict['name'])

    def test_assert_per_unit_type(self):
        self.assertEqual(self.product.unit, self.product_dict['unit'])

    def test_assert_price_per_unit(self):
        self.assertEqual(self.product.price_per_unit, self.product_dict['price_per_unit'])


class TestProductUnit(unittest.TestCase):
    def setUp(self):
        self.class_enum = mdl_objcts.ProductUnit

    @parameterized.expand([(1, ), (2, )])
    def test_product_unit_is_instance_of_enum(self, value):
        self.assertIsInstance(self.class_enum(value), enum.Enum)

    def test_assert_product_unit_of_enum_one_equals_productunit_each(self):
        self.assertEqual(self.class_enum(1), mdl_objcts.ProductUnit.EACH)

    def test_assert_product_unit_of_enum_two_equals_productunit_kilo(self):
        self.assertEqual(self.class_enum(2), mdl_objcts.ProductUnit.KILO)


class TestSpecialOfferType(unittest.TestCase):
    def setUp(self):
        self.class_enum = mdl_objcts.SpecialOfferType

    def test_special_offer_type_is_instance_of_enum(self):
        self.assertIsInstance(self.class_enum(1), enum.Enum)

    def test_assert_special_offer_type_of_one_equals_three_for_two(self):
        self.assertEqual(self.class_enum(1), mdl_objcts.SpecialOfferType.THREE_FOR_TWO)

    def test_assert_special_offer_type_of_two_equals_percent_discount(self):
        self.assertEqual(self.class_enum(2), mdl_objcts.SpecialOfferType.PERCENT_DISCOUNT)

    def test_assert_special_offer_type_of_three_equals_two_for_amount(self):
        self.assertEqual(self.class_enum(3), mdl_objcts.SpecialOfferType.TWO_FOR_AMOUNT)

    def test_assert_special_offer_type_of_four_equals_five_for_amount(self):
        self.assertEqual(self.class_enum(4), mdl_objcts.SpecialOfferType.FIVE_FOR_AMOUNT)

    def test_assert_special_offer_type_of_five_equals_bundle_discount(self):
        self.assertEqual(self.class_enum(5), mdl_objcts.SpecialOfferType.BUNDLE_DISCOUNT)

    def test_raises_error_if_special_offer_type_is_six(self):
        with self.assertRaises(ValueError):
            self.class_enum(6)


class TestOffer(unittest.TestCase):
    def setUp(self):
        self.offer_type_value = random.randrange(1, 5)
        self.argument = random.random() * 100

        self.offer = mdl_objcts.Offer(offer_type=mdl_objcts.SpecialOfferType(self.offer_type_value),
                                      argument=self.argument)

    def test_asserts_offer_type_setup_correctly(self):
        self.assertEqual(self.offer.offer_type.value, self.offer_type_value)

    def test_asserts_argument_correctly(self):
        self.assertEqual(self.offer.argument, self.argument)

    def test_refuses_setting_offer_type(self):
        with self.assertRaises(AttributeError):
            self.offer.offer_type = self.offer_type_value

    def test_refuses_setting_argument(self):
        with self.assertRaises(AttributeError):
            self.offer.argument = self.argument


class TestDiscount(unittest.TestCase):
    def setUp(self):
        self.product_dict = setup_product_kwargs()
        self.kwargs = {'product': PRODUCT_NAMEDTUPLE(**cp.deepcopy(self.product_dict)),
                       'description': "A great discount for Christmas!",
                       'discount_amount': random.random() * 100_000}
        self.discount = mdl_objcts.Discount(**cp.copy(self.kwargs))

    def test_asserts_description_correctly(self):
        self.assertEqual(self.discount.description, self.kwargs['description'])

    def test_asserts_discount_amount_correctly(self):
        self.assertEqual(self.discount.discount_amount, self.kwargs['discount_amount'])

    def test_asserts_product_correctly(self):
        self.assertEqual(self.discount.product, self.kwargs['product'])

    def test_refuses_setting_product(self):
        with self.assertRaises(AttributeError):
            self.discount.product = self.kwargs['product']

    def test_refuses_setting_description(self):
        with self.assertRaises(AttributeError):
            self.discount.description = self.kwargs['description']

    def test_refuses_setting_discount_amount(self):
        with self.assertRaises(AttributeError):
            self.discount.discount_amount = self.kwargs['discount_amount']
