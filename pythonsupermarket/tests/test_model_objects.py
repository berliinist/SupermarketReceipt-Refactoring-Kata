import copy as cp
import enum
import random
import unittest
from unittest.mock import Mock, PropertyMock

from parameterized import parameterized
import pytest

import pythonsupermarket.model_objects as mdl_objcts

from tests.shared_test_functions import set_up_product_dict, SharedUnitTests


class TestProductInfo(unittest.TestCase):
    def setUp(self):
        self.product_dict = set_up_product_dict()
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

    def test_assert_special_offer_type_of_two_equals_ten_percent_discount(self):
        self.assertEqual(self.class_enum(2), mdl_objcts.SpecialOfferType.TEN_PERCENT_DISCOUNT)

    def test_assert_special_offer_type_of_three_equals_two_for_amount(self):
        self.assertEqual(self.class_enum(3), mdl_objcts.SpecialOfferType.TWO_FOR_AMOUNT)

    def test_assert_special_offer_type_of_four_equals_five_for_amount(self):
        self.assertEqual(self.class_enum(4), mdl_objcts.SpecialOfferType.FIVE_FOR_AMOUNT)

    def test_assert_special_offer_type_of_five_equals_bundle_discount(self):
        self.assertEqual(self.class_enum(5), mdl_objcts.SpecialOfferType.BUNDLE_DISCOUNT)

    def test_raises_error_if_special_offer_type_is_six(self):
        with self.assertRaises(ValueError):
            self.class_enum(6)


@pytest.mark.skip(reason="higher priorities elsewhere for now. please rely on integrated tests for now.")
class TestOffer(unittest.TestCase):
    def setUp(self):
        pass


class TestOfferIntegration(unittest.TestCase, SharedUnitTests):
    def setUp(self):
        self.offer_type_value = random.randrange(1, 5)
        self.product_dict = set_up_product_dict()
        self.argument = 'unsure what is this for'

        self.test_class = mdl_objcts.Offer(offer_type=mdl_objcts.SpecialOfferType(self.offer_type_value),
                                            product=mdl_objcts.ProductInfo(**cp.deepcopy(self.product_dict)),
                                            argument=self.argument)

    def test_asserts_offer_type_setup_correctly(self):
        self.assertEqual(self.test_class.offer_type.value, self.offer_type_value)

    @pytest.mark.skip(reason="unsure at the moment what arguments exactly, will check later.")
    def test_asserts_argument_correctly(self):
        pass


@pytest.mark.skip(reason="not a higher priority.")
class TestDiscount(unittest.TestCase):
    pass


class TestDiscountIntegration(unittest.TestCase, SharedUnitTests):
    def setUp(self):
        self.product_dict = set_up_product_dict()
        self.test_class = mdl_objcts.Discount(product=mdl_objcts.ProductInfo(**cp.deepcopy(self.product_dict)),
                                              description="It's a great discount!",
                                              discount_amount="TODO, what exactly to put here?")

    @pytest.mark.skip(reason="Unsure in what format the description should be (for now)")
    def test_asserts_description_correctly(self):
        pass

    @pytest.mark.skip(reason="Unsure in what format the discount amount should be (for now)")
    def test_asserts_discount_amount_correctly(self):
        pass
