from unittest import TestCase
import datetime as dt
from pandas_datareader._utils import RemoteDataError
from perfin.portfolioutils import get_prices

class TestGet_prices(TestCase):

    def setUp(self):
        self.symbols = ['SAP', 'APPL']
        self.end = dt.date.today()
        self.start = self.end - dt.timedelta(days=365)

    def test_get_prices_non_exsisting_symbol_requires_online(self):
        with self.assertRaises(RemoteDataError):
            get_prices(symbols=self.symbols, dt_start=self.start, dt_end=self.end)
