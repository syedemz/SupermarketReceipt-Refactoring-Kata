
class ReceiptItem:
    def __init__(self, product, quantity, price, total_price):
        self.product = product
        self.quantity = quantity
        self.price = price
        self.total_price = total_price


class Receipt:
    def __init__(self):
        self._items = []
        self._discounts = []

    def total_price(self):
        """
        This function calculates the total amount to be paid also taking into consideration
        the associated discounts as part of the calculation
        :return: Total
        """
        total = 0
        for item in self.items:
            total += item.total_price
        for discount in self.discounts:
            total += discount.discount_amount
        return total

    def add_product(self, product, quantity, price, total_price):
        """
        :param product: Product
        :param quantity: Number
        :param price: Number
        :param total_price: Number
        :return: None
        """
        self._items.append(ReceiptItem(product, quantity, price, total_price))

    def add_discount(self, discount):
        """
        :param discount: Discount
        :return: None
        """
        self._discounts.append(discount)

    @property
    def items(self):
        return self._items[:]

    @property
    def discounts(self):
        return self._discounts[:]
