from perfin.portfolio import Stock
from perfin.portfolio import Portfolio
from unittest import TestCase


class TestPortfolio(TestCase):

    def setUp(self):
        self.stocks = [Stock('IBM'), Stock('APPL')]
        self.portfolio = Portfolio()

    def test_new_portfolio_single_stock(self):
        self.portfolio = Portfolio(stock=self.stocks[0])
        self.assertListEqual(self.portfolio.get_current_stocks(), ['IBM'])

    def test_new_portfolio_list_of_stocks(self):
        self.portfolio = Portfolio(stocks=self.stocks)
        self.assertSetEqual(set(self.portfolio.get_current_stocks()), {'IBM', 'APPL'})

    def test_add_stock(self):
        self.portfolio.add_stocks(self.stocks)
        self.assertSetEqual(set(self.portfolio.get_current_stocks()), {'IBM', 'APPL'})
        stock = Stock('SAP')
        self.portfolio.add_stock(stock)
        self.assertSetEqual(set(self.portfolio.get_current_stocks()), {'IBM', 'APPL', 'SAP'})

    def test_add_stocks(self):
        self.portfolio.add_stocks(self.stocks)
        self.assertSetEqual(set(self.portfolio.get_current_stocks()), {'IBM', 'APPL'})
        stocks = [Stock('SAP'), Stock('GOOGL')]
        self.portfolio.add_stocks(stocks)
        self.assertSetEqual(set(self.portfolio.get_current_stocks()), {'IBM', 'APPL', 'SAP', 'GOOGL'})

    def test_get_current_stocks(self):
        stocks = [Stock('SAP'), Stock('GOOGL')]
        self.portfolio = Portfolio(stocks=stocks)
        self.assertSetEqual(set(self.portfolio.get_current_stocks()), {'SAP', 'GOOGL'})

    def test_get_dataframe(self):
        ibm = Stock('IBM')
        ibm.add_transaction('2014-10-12', 100)
        ibm.add_transaction('2015-10-12', 150)
        ibm.add_transaction('2016-10-12', -100)

        appl = Stock('APPL')
        appl.add_transaction('2014-10-6', 10)
        appl.add_transaction('2015-10-6', 15)
        appl.add_transaction('2016-10-6', 30)

        self.portfolio = Portfolio(stocks=[ibm, appl])
        df = self.portfolio.get_dataframe()

        # sum - vertical
        shares_sum = df.sum(axis=0)
        self.assertEqual(shares_sum['IBM'], 150)
        self.assertEqual(shares_sum['APPL'], 55)

        # total shares
        shares_total = shares_sum.sum()
        self.assertEqual(shares_total, 205)

    def test_get_weights_number(self):
        ibm = Stock('IBM')
        ibm.add_transaction('2014-10-12', 100)
        ibm.add_transaction('2015-10-12', 150)
        ibm.add_transaction('2016-10-12', -100)

        appl = Stock('APPL')
        appl.add_transaction('2014-10-6', 10)
        appl.add_transaction('2015-10-6', 15)
        appl.add_transaction('2016-10-6', 30)

        self.portfolio = Portfolio(stocks=[ibm, appl])

        weight_ibm = 0.73
        weight_appl = 0.27

        weights = self.portfolio.get_weights()
        self.assertAlmostEqual(weights.sum(), 1.00)
        self.assertAlmostEqual(weights['IBM'], weight_ibm, 2)
        self.assertAlmostEqual(weights['APPL'], weight_appl, 2)

    def test_get_weights_value(self):
        ibm = Stock('IBM')
        ibm.add_transaction('2014-10-12', 100)
        ibm.add_transaction('2015-10-12', 150)
        ibm.add_transaction('2016-10-12', -100)

        appl = Stock('APPL')
        appl.add_transaction('2014-10-6', 10)
        appl.add_transaction('2015-10-6', 15)
        appl.add_transaction('2016-10-6', 30)

        self.portfolio = Portfolio(stocks=[ibm, appl])

        prices = {'APPL': 100.32, 'IBM': 171.03}

        weights = self.portfolio.get_weights(weight_by='value', prices=prices)

        self.assertAlmostEqual(weights.sum(axis=1)[0], 1.00)

        weight_ibm = 0.82
        weight_appl = 0.18

        self.assertAlmostEqual(weights['IBM'].iloc[0], weight_ibm, 2)
        self.assertAlmostEqual(weights['APPL'].iloc[0], weight_appl, 2)

    def test_get_current_value(self):
        ibm = Stock('IBM')
        ibm.add_transaction('2014-10-12', 100)
        ibm.add_transaction('2015-10-12', 150)
        ibm.add_transaction('2016-10-12', -100)

        appl = Stock('APPL')
        appl.add_transaction('2014-10-6', 10)
        appl.add_transaction('2015-10-6', 15)
        appl.add_transaction('2016-10-6', 30)

        self.portfolio = Portfolio(stocks=[ibm, appl])

        prices = {'APPL': 100.32, 'IBM': 171.03}

        value_ibm = 25654.5
        value_appl = 5517.6
        value_total = 31172.1

        values = self.portfolio.get_current_value(prices)

        self.assertAlmostEqual(values['IBM'].iloc[0], value_ibm, 2)
        self.assertAlmostEqual(values['APPL'].iloc[0], value_appl, 2)
        self.assertAlmostEqual(values['TOTAL'].iloc[0], value_total, 2)