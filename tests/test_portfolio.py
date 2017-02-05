import datetime as dt
from perfin import portfolioutils
from perfin.portfolio import Stock
from perfin.portfolio import Portfolio
from unittest import TestCase, mock
from unittest.mock import ANY



class TestPortfolio(TestCase):

    def setUp(self):
        self.stocks = [Stock('IBM'), Stock('AAPL')]
        self.portfolio = Portfolio()

    def test_new_portfolio_single_stock(self):
        self.portfolio = Portfolio(stock=self.stocks[0])
        self.assertListEqual(self.portfolio.get_current_stocks(), ['IBM'])

    def test_new_portfolio_list_of_stocks(self):
        self.portfolio = Portfolio(stocks=self.stocks)
        self.assertSetEqual(set(self.portfolio.get_current_stocks()), {'IBM', 'AAPL'})

    def test_add_stock(self):
        self.portfolio.add_stocks(self.stocks)
        self.assertSetEqual(set(self.portfolio.get_current_stocks()), {'IBM', 'AAPL'})
        stock = Stock('SAP')
        self.portfolio.add_stock(stock)
        self.assertSetEqual(set(self.portfolio.get_current_stocks()), {'IBM', 'AAPL', 'SAP'})

    def test_add_stocks(self):
        self.portfolio.add_stocks(self.stocks)
        self.assertSetEqual(set(self.portfolio.get_current_stocks()), {'IBM', 'AAPL'})
        stocks = [Stock('SAP'), Stock('GOOGL')]
        self.portfolio.add_stocks(stocks)
        self.assertSetEqual(set(self.portfolio.get_current_stocks()), {'IBM', 'AAPL', 'SAP', 'GOOGL'})

    def test_get_current_stocks(self):
        stocks = [Stock('SAP'), Stock('GOOGL')]
        self.portfolio = Portfolio(stocks=stocks)
        self.assertSetEqual(set(self.portfolio.get_current_stocks()), {'SAP', 'GOOGL'})

    def test_get_dataframe(self):
        ibm = Stock('IBM')
        ibm.add_transaction('2014-10-12', 100)
        ibm.add_transaction('2015-10-12', 150)
        ibm.add_transaction('2016-10-12', -100)

        aapl = Stock('AAPL')
        aapl.add_transaction('2014-10-6', 10)
        aapl.add_transaction('2015-10-6', 15)
        aapl.add_transaction('2016-10-6', 30)

        self.portfolio = Portfolio(stocks=[ibm, aapl])
        df = self.portfolio.get_dataframe()

        # sum - vertical
        shares_sum = df.sum(axis=0)
        self.assertEqual(shares_sum['IBM'], 150)
        self.assertEqual(shares_sum['AAPL'], 55)

        # total shares
        shares_total = shares_sum.sum()
        self.assertEqual(shares_total, 205)

    def test_get_weights_number(self):
        ibm = Stock('IBM')
        ibm.add_transaction('2014-10-12', 100)
        ibm.add_transaction('2015-10-12', 150)
        ibm.add_transaction('2016-10-12', -100)

        aapl = Stock('AAPL')
        aapl.add_transaction('2014-10-6', 10)
        aapl.add_transaction('2015-10-6', 15)
        aapl.add_transaction('2016-10-6', 30)

        self.portfolio = Portfolio(stocks=[ibm, aapl])

        weight_ibm = 0.73
        weight_aapl = 0.27

        weights = self.portfolio.get_weights()
        self.assertAlmostEqual(weights.sum(), 1.00)
        self.assertAlmostEqual(weights['IBM'], weight_ibm, 2)
        self.assertAlmostEqual(weights['AAPL'], weight_aapl, 2)

    def test_get_weights_value(self):
        ibm = Stock('IBM')
        ibm.add_transaction('2014-10-12', 100)
        ibm.add_transaction('2015-10-12', 150)
        ibm.add_transaction('2016-10-12', -100)

        aapl = Stock('AAPL')
        aapl.add_transaction('2014-10-6', 10)
        aapl.add_transaction('2015-10-6', 15)
        aapl.add_transaction('2016-10-6', 30)

        self.portfolio = Portfolio(stocks=[ibm, aapl])

        prices = {'AAPL': 100.32, 'IBM': 171.03}

        weights = self.portfolio.get_weights(weight_by='value', prices=prices)

        self.assertAlmostEqual(weights.sum(axis=1)[0], 1.00)

        weight_ibm = 0.82
        weight_aapl = 0.18

        self.assertAlmostEqual(weights['IBM'].iloc[0], weight_ibm, 2)
        self.assertAlmostEqual(weights['AAPL'].iloc[0], weight_aapl, 2)

    def test_get_current_value(self):
        ibm = Stock('IBM')
        ibm.add_transaction('2014-10-12', 100)
        ibm.add_transaction('2015-10-12', 150)
        ibm.add_transaction('2016-10-12', -100)

        aapl = Stock('AAPL')
        aapl.add_transaction('2014-10-6', 10)
        aapl.add_transaction('2015-10-6', 15)
        aapl.add_transaction('2016-10-6', 30)

        self.portfolio = Portfolio(stocks=[ibm, aapl])

        prices = {'AAPL': 100.32, 'IBM': 171.03}

        value_ibm = 25654.5
        value_aapl = 5517.6
        value_total = 31172.1

        values = self.portfolio.get_current_value(prices)

        self.assertAlmostEqual(values['IBM'].iloc[0], value_ibm, 2)
        self.assertAlmostEqual(values['AAPL'].iloc[0], value_aapl, 2)
        self.assertAlmostEqual(values['TOTAL'].iloc[0], value_total, 2)

    @mock.patch.object(portfolioutils, 'get_prices', autospec=True)
    def test_get_prices(self, mock_get_prices):
        ibm = Stock('IBM')
        ibm.add_transaction('2014-10-12', 100)
        ibm.add_transaction('2015-10-12', 150)
        ibm.add_transaction('2016-10-12', -100)

        aapl = Stock('AAPL')
        aapl.add_transaction('2014-10-06', 10)
        aapl.add_transaction('2015-10-06', 15)
        aapl.add_transaction('2016-10-06', 30)

        self.portfolio = Portfolio(stocks=[ibm, aapl])

        symbols = ['IBM', 'AAPL']

        # today's date (default)
        dt_end = dt.date.today()
        dt_start = dt_end - dt.timedelta(days=1)

        self.portfolio.get_prices()
        mock_get_prices.assert_called_with(symbols=symbols, dt_start=dt_start, dt_end=dt_end)

    @mock.patch.object(portfolioutils, 'get_prices', autospec=True)
    def test_get_prices(self, mock_get_prices):
        ibm = Stock('IBM')
        ibm.add_transaction('2014-10-12', 100)
        ibm.add_transaction('2015-10-12', 150)
        ibm.add_transaction('2016-10-12', -100)

        aapl = Stock('AAPL')
        aapl.add_transaction('2014-10-06', 10)
        aapl.add_transaction('2015-10-06', 15)
        aapl.add_transaction('2016-10-06', 30)

        self.portfolio = Portfolio(stocks=[ibm, aapl])

        # today's date (default)
        dt_end = dt.date.today()
        dt_start = dt_end - dt.timedelta(days=1)

        self.portfolio.get_prices()
        mock_get_prices.assert_called_with(symbols=ANY, dt_start=dt_start, dt_end=dt_end)

        # specific date
        date_str = '2016-07-13'
        date = dt.datetime.strptime(date_str, '%Y-%m-%d').date()
        dt_end = dt.datetime.strptime(date_str, '%Y-%m-%d').date()
        dt_start = dt_end - dt.timedelta(days=1)

        self.portfolio.get_prices(date=date, range='date')
        mock_get_prices.assert_called_with(symbols=ANY, dt_start=dt_start, dt_end=dt_end)

        # validate the date input field
        with self.assertRaises(AssertionError):
            self.portfolio.get_prices(date=date_str, range='date')

        # date range of all transactions
        dt_start = dt.datetime.strptime('2014-10-06', '%Y-%m-%d').date()
        dt_end = dt.datetime.strptime('2016-10-12', '%Y-%m-%d').date()

        self.portfolio.get_prices(range='range')
        mock_get_prices.assert_called_with(symbols=ANY, dt_start=dt_start, dt_end=dt_end)

        # full range - first transaction data to today
        dt_end = dt.date.today()

        self.portfolio.get_prices(range='full')
        mock_get_prices.assert_called_with(symbols=ANY, dt_start=dt_start, dt_end=dt_end)
