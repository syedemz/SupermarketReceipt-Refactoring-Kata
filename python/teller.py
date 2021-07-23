from model_objects import Offer
from receipt import Receipt
from model_objects import ProductQuantity, SpecialOfferType, Discount
import math

'''
Class Description: 

'''


class Teller:
    """
    The teller class can be thought of as the cashier of the supermarket. It prepares the receipts, computes the total cost, discounts etc
    """

    def __init__(self, catalog):
        self.catalog = catalog
        self.offers = {}

    def add_special_offer(self, offer_type, product, argument):
        """
        Function Desc: This function creates a special offer object which contains information about what offer is available on what object
        and then adds this offer to the self.offers dictionary using the product as the key
        :param offer_type: SpecialOfferType
        :param product: Product
        :param argument: Number
        :return: None
        """
        self.offers[product] = Offer(offer_type, product, argument)

    def checks_out_articles_from(self, the_cart):

        """
        Function Desc:This function initiates the process of final amount calculation for all products in
        the shopping cart and creates a Receipt object
        :param the_cart: ShoppingCart
        :return: Receipt
        """
        receipt = Receipt()
        product_quantities = the_cart.items
        for pq in product_quantities:
            p = pq.product
            quantity = pq.quantity
            unit_price = self.catalog.unit_price(p)
            price = quantity * unit_price
            receipt.add_product(p, quantity, unit_price, price)

        self.handle_offers(receipt, self.offers, self.catalog, the_cart.product_quantities)  # change this use the new method below instead of the one in the shopping cart and add unit tests for them

        return receipt

    def handle_offers(self, receipt, offers, catalog, product_quantities):

        """
        Function Desc:This function handles all the discount offers for final calculation. Depending upon the type
        of the special offer, a particular handler function is called and the associated discounted prices are then
        adjusted onto the receipt
        :param the_cart: ShoppingCart
        :receipt: Receipt
        :offers: Offer
        :catalog: Catalog
        :product_quantities: ProductQuantity
        :return: Receipt
        """

        offerSelector = {
            SpecialOfferType.THREE_FOR_TWO: self.three_For_Two,
            SpecialOfferType.TEN_PERCENT_DISCOUNT: self.ten_Percent_Discount,
            SpecialOfferType.TWO_FOR_AMOUNT: self.two_For_Amount,
            SpecialOfferType.FIVE_FOR_AMOUNT: self.five_For_Amount
        }

        for p in product_quantities.keys():
            quantity = product_quantities[p]
            if p in offers.keys():
                offer = offers[p]
                unit_price = catalog.unit_price(p)
                quantity_as_int = int(quantity)
                x = 1
                discounter = offerSelector.get(offer.offer_type, lambda: "Invalid month")
                discount = discounter(p, quantity_as_int, quantity, unit_price, offer)

                if discount:
                    receipt.add_discount(discount)

    def three_For_Two(self, product, quantity_as_int, quantity, unit_price, offer):
        """
        Function Desc: Handler function for three_for_two special offer type
        @param product:
        @param quantity_as_int:
        @param quantity:
        @param unit_price:
        @param offer:
        @return: discount
        """
        number_of_x = math.floor(quantity_as_int / 3)
        if quantity_as_int > 2:
            discount_amount = quantity * unit_price - (
                    (number_of_x * 2 * unit_price) + quantity_as_int % 3 * unit_price)
            discount = Discount(product, "3 for 2", -discount_amount)
            return discount

    def ten_Percent_Discount(self, product, quantity_as_int, quantity, unit_price, offer):
        """
        Function Desc: Handler function for Ten percent discount special offer type

        @param product:
        @param quantity_as_int:
        @param quantity:
        @param unit_price:
        @param offer:
        @return:
        """
        discount = Discount(product, str(offer.argument) + "% off",
                            -quantity * unit_price * offer.argument / 100.0)
        return discount

    def two_For_Amount(self, product, quantity_as_int, quantity, unit_price, offer):
        """
        Function Desc: Handler function for two for amount special offer type

        @param product:
        @param quantity_as_int:
        @param quantity:
        @param unit_price:
        @param offer:
        @return:
        """
        if quantity_as_int >= 2:
            total = offer.argument * (quantity_as_int / 2) + quantity_as_int % 2 * unit_price
            discount_n = unit_price * quantity - total
            discount = Discount(product, "2 for " + str(offer.argument), -discount_n)
            return discount

    def five_For_Amount(self, product, quantity_as_int, quantity, unit_price, offer):
        """
        Function Desc: Handler function for five for amount special offer type

        @param product:
        @param quantity_as_int:
        @param quantity:
        @param unit_price:
        @param offer:
        @return:
        """
        number_of_x = math.floor(quantity_as_int / 5)
        if quantity_as_int >= 5:
            discount_total = unit_price * quantity - (
                    offer.argument * number_of_x + quantity_as_int % 5 * unit_price)
            discount = Discount(product, str(5) + " for " + str(offer.argument), -discount_total)
            return discount
