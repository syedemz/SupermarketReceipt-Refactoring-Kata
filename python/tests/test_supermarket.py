import pytest
import unittest
from approvaltests import verify

from model_objects import Product, SpecialOfferType, ProductUnit
from shopping_cart import ShoppingCart
from teller import Teller
from tests.fake_catalog import FakeCatalog
from receipt_printer import ReceiptPrinter


class SupermarketTest(unittest.TestCase):
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


    def test_two_normal_items(self):
        self.the_cart.add_item(self.toothbrush)
        self.the_cart.add_item(self.rice)
        receipt = self.teller.checks_out_articles_from(self.the_cart)
        #print(receipt)
        assert(len(receipt.discounts) == 0)
        assert(len(receipt.items) == 2)
        assert(receipt.items[0].price == 0.99)
        assert(receipt.items[0].quantity == 1.0)
        assert(receipt.items[0].product.name == "toothbrush")
        assert(receipt.total_price() == 3.9800000000000004)
        self.the_cart.empty_cart()


        #verify(ReceiptPrinter(40).print_receipt(receipt))

    def test_three_for_two(self):
        self.the_cart.add_item(self.toothbrush)
        self.the_cart.add_item(self.toothbrush)
        self.the_cart.add_item(self.toothbrush)
        self.the_cart.add_item(self.toothbrush)
        self.the_cart.add_item(self.toothbrush)
        self.teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, self.toothbrush,
                                      self.catalog.unit_price(self.toothbrush))
        receipt = self.teller.checks_out_articles_from(self.the_cart)
        assert (len(receipt.discounts) == 1)
        assert (receipt.discounts[0].description == "3 for 2")
        assert (receipt.discounts[0].discount_amount == -0.9900000000000002)
        assert (len(receipt.items) == 5)
        assert (receipt.items[0].price == 0.99)
        assert (receipt.items[0].quantity == 1.0)
        assert (receipt.items[0].product.name == "toothbrush")
        assert (receipt.total_price() == 3.96 )
        self.the_cart.empty_cart()

    def test_five_for_amount(self):
        self.the_cart.add_item(self.toothbrush)
        self.the_cart.add_item(self.toothbrush)
        self.the_cart.add_item(self.toothbrush)
        self.the_cart.add_item(self.toothbrush)
        self.the_cart.add_item(self.toothbrush)
        self.teller.add_special_offer(SpecialOfferType.FIVE_FOR_AMOUNT, self.toothbrush,
                                      self.catalog.unit_price(self.toothbrush))
        receipt = self.teller.checks_out_articles_from(self.the_cart)
        assert (len(receipt.discounts) == 1)
        assert (receipt.discounts[0].description == "5 for 0.99")
        assert (receipt.discounts[0].discount_amount == -3.96)
        assert (len(receipt.items) == 5)
        assert (receipt.items[0].price == 0.99)
        assert (receipt.items[0].quantity == 1.0)
        assert (receipt.items[0].product.name == "toothbrush")
        assert (receipt.total_price() == 0.9900000000000002)
        self.the_cart.empty_cart()

    def test_ten_percent(self):
        self.the_cart.add_item(self.toothbrush)
        self.the_cart.add_item(self.toothbrush)
        self.the_cart.add_item(self.toothbrush)
        self.the_cart.add_item(self.toothbrush)
        self.the_cart.add_item(self.toothbrush)
        self.teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, self.toothbrush,10)
        receipt = self.teller.checks_out_articles_from(self.the_cart)
        assert (len(receipt.discounts) == 1)
        assert (receipt.discounts[0].description == "10% off")
        assert (receipt.discounts[0].discount_amount == -0.495)
        assert (len(receipt.items) == 5)
        assert (receipt.items[0].price == 0.99)
        assert (receipt.items[0].quantity == 1.0)
        assert (receipt.items[0].product.name == "toothbrush")
        assert (receipt.total_price() == 4.455)
        self.the_cart.empty_cart()



'''spr = SupermarketTest()
spr.setUp()
spr.test_two_normal_items()
spr.test_three_for_two()
spr.test_five_for_amount()
spr.test_ten_percent()
#spr.test_buy_five_get_one_free()
'''
