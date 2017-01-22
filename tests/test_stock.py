from perfin.portfolio import Stock
from unittest import TestCase


class TestStock(TestCase):

    def setUp(self):
        self.symbol = 'IBM'
        self.name = 'International Business Machines'
        self.stock = Stock(self.symbol, self.name)

    def test_add_initial_transaction(self):
        self.assertEqual(self.stock.symbol, self.symbol)
        self.assertEqual(self.stock.name, self.name)
        self.assertEqual(self.stock.get_total_amount(), 0)
        self.stock.add_transaction('2015-12-11', 123, 166.32)
        self.assertEqual(self.stock.get_total_amount(), 123)

    def test_get_total_amount(self):
        self.assertEqual(self.stock.symbol, self.symbol)
        self.stock.add_transaction('2016-01-12', 50)
        self.stock.add_transaction('2016-02-17', -10)
        self.stock.add_transaction('2016-03-17', 70)
        self.stock.add_transaction('2016-04-17', 30)
        self.stock.add_transaction('2016-05-17', -5)
        self.assertEqual(self.stock.get_total_amount(), 135)

    def test_ensure_transaction_order(self):
        self.assertEqual(self.stock.symbol, self.symbol)
        self.stock.add_transaction('2015-01-12', 50)
        self.stock.add_transaction('2016-02-17', -10)
        self.stock.add_transaction('2015-03-17', 70)
        self.stock.add_transaction('2015-04-17', 30)
        self.stock.add_transaction('2014-05-17', -5)
        self.assertEqual(self.stock.holdings[-1].amount, -10)