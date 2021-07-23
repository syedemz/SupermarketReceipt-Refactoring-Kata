import pytest
import unittest

from model_objects import Product, SpecialOfferType, ProductUnit, ProductQuantity, Offer
from shopping_cart import ShoppingCart
from teller import Teller
from tests.fake_catalog import FakeCatalog
from teller import Teller


class SpecialOfferTest(unittest.TestCase):
    def setUp(self):
        self.catalog = FakeCatalog()
        self.teller = Teller(self.catalog)
        self.the_cart = ShoppingCart()
        self.toothbrush = Product("toothbrush", ProductUnit.EACH)
        self.catalog.add_product(self.toothbrush, 0.99)
        self.rice = Product("rice", ProductUnit.EACH)
        self.catalog.add_product(self.rice, 2.99)
        self.apples = Product("apples", ProductUnit.KILO)
        self.catalog.add_product(self.apples, 1.99)
        self.cherry_tomatoes = Product("cherry tomato box", ProductUnit.EACH)
        self.catalog.add_product(self.cherry_tomatoes, 0.69)
        self.teller = Teller(self.catalog)


    def testTenPercent(self):
        self.qty = ProductQuantity(self.toothbrush, 3)
        self.offer = Offer(SpecialOfferType.THREE_FOR_TWO, self.toothbrush, self.catalog.unit_price(self.toothbrush))
        discount = self.teller.ten_Percent_Discount(self.toothbrush, 3, 3, 0.99, self.offer)
        assert (discount.description == '0.99% off')
        assert (discount.discount_amount == -0.029403)
        assert (discount.product == self.toothbrush)

    def testTwoForAmount(self):
        self.offer = Offer(SpecialOfferType.TWO_FOR_AMOUNT, self.toothbrush, self.catalog.unit_price(self.toothbrush))
        discount = self.teller.two_For_Amount(self.toothbrush, 3, 3, 0.99, self.offer)
        assert (discount.description == '2 for 0.99')
        assert (discount.discount_amount == -0.4950000000000001)
        assert (discount.product == self.toothbrush)




'''spr = SpecialOfferTest()
spr.setUp()
#spr.testTenPercent()
spr.testTwoForAmount()
#product, quantity_as_int, quantity, unit_price, offer
#self.offers[product] = Offer(offer_type, product, argument)'''