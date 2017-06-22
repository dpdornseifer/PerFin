from functools import wraps
import perfin.datautils
import datetime as dt
import pandas as pd
import pickle

class Transaction:
    """ The transaction object represents the details of a buy or sell transaction """

    def __init__(self, date, amount, price, symbol):
        # TODO fix
        """ Creates a transaction object that keeps the details like the amount and date of a buy or sell transaction 
        
        Args:
            date (date):
            amount (int):
            price (int):
            symbol (string):
            
        
        """
        self.date = date
        self.amount = amount
        self.price = price
        self.symbol = symbol


class Stock:
    """ The stock object represents a specific stock symbol"""

    def __init__(self, symbol, name=None):
        """ Creates a stock object which keeps a particular stock symbol, a company name and the transactions.

        Args:
            symbol (str): The given stock symbol.
            name (str): The full company name.

        Returns:
            A stock object.
        """
        self.symbol = symbol
        self.name = name
        self.holdings = []

    def add_transaction(self, date, amount, price=None):
        """ Adds purchase or sell transactions to a stock entity.

        Args:
            date (date): Date of the transaction
            amount (int): A positive integer for a buy transaction or a negative integer for a sell transaction.
            price (float): The price the stocks have been bought or sold for.
        """

        date = date.split('-')

        self.holdings.append(Transaction(dt.date(int(date[0]), int(date[1]), int(date[2])), amount, price, self.symbol))

        # make sure that it is in the right order after a transaction has been added
        self.holdings = sorted(self.holdings, key=lambda x: x.date)

    def get_total_amount(self):
        """ Returns the total amount of shares for the given stock.

        Returns (int):
            The total amount of shares fo the given stock.
        """
        return 0 if not self.holdings else sum([transaction.amount for transaction in self.holdings])


class Portfolio:
    """ A portfolio represents a collection of different stocks. """

    def __init__(self, stock=None, stocks=None, name=None):
        """

        Args:
            stock (stock): A single stock object that should be added to the portfolio at construction time.
            stocks [stock]: A list of stock objects that should be added to the portfolio at construction time.
            name (string): A name for the portfolio object.
        """
        # dct keeping the stock information 'symbol -> stock' for easy and fast access
        self.stocks = {}

        # TODO use tuple / namedtuple to add update/create timestamp for _dataframe
        self._dataframe = None

        # if stocks are passed in the constructor, add the
        if stock:
            self.add_stock(stock)
        if stocks:
            self.add_stocks(stocks)

        self.name = name

    def add_stock(self, stock):
        """ Adds a single stock to the portfolio.

        Args:
            stock (stock) : A single stock object which should be added to the portfolio.
        """
        self.add_stocks([stock])

    def add_stocks(self, stocks):
        """ Adds a list of stocks to the portfolio

        Args:
            stocks [stocks]: A list of stock objects which should be added to the portfolio.
        """
        for stock in stocks:
            self.stocks[stock.symbol] = stock

    def get_current_stocks(self):
        """ Returns list of symbols in the current portfolio. """
        return list(self.stocks.keys())

    def save_to_file(self, path, name=None):
        """ Saves the stocks contained in the portfolio as a file on harddrive. 
        
        Args:
            path (string): The path to the file where the portfolio should be saved.
        """
        with open(path, 'wb') as f:
            pickle.dump((self.stocks, self._dataframe), f)

    def load_from_file(self, path):
        """ Loads stocks from a saved portfolio. 
        
        Args:
            path (string): The path to the saved portfolio. 
        """
        with open(path, 'rb') as f:
            self.stocks, self._dataframe = pickle.load(f)

    def _requires_dataframe(func):
        """ Decorator function for all class methods requiring the _dataframe to make sure that the df has been generated.

        Returns:
            A function wrapper, that makes sure, that the _dataframe is available before the method is called.
        """
        @wraps(func)
        def func_wrapper(self, *args, **kwargs):
            if self._dataframe is None:
                self._create_dataframe()
            return func(self, *args, **kwargs)
        return func_wrapper

    def _create_dataframe(self):
        """ Converts the current stocks kept in the portfolio into a _dataframe for fast processing.
            The _dataframe is not recreated automatically after a stock or a stock related transaction has been added.
            For better performance, a recreation should just be triggered after all stock related updates are done.

        Dataframe:
            date,     stock_1,    stock_2
            1-1-2010, +100,       0
            5-2-2012, 0,          +37

        """
        symbols = self.get_current_stocks()
        transactions = []
        dt_start = None
        dt_stop = None

        for symbol in symbols:

            holdings = self.stocks[symbol].holdings

            # add holdings to overall transaction list
            transactions += holdings

            # get the date of the first and the last transaction
            dt_start = holdings[0].date if not dt_start or holdings[0].date < dt_start else dt_start
            dt_stop = holdings[-1].date if not dt_stop or holdings[-1].date > dt_stop else dt_stop

        # create index for all transactions
        dt_index = pd.date_range(dt_start, dt_stop).date

        self._dataframe = pd.DataFrame(columns=symbols, index=pd.DatetimeIndex(dt_index)).fillna(0)
        self._dataframe.index.name = 'date'

        # fill the _dataframe with the transactions from the overall list
        for transaction in transactions:
            self._dataframe.loc[transaction.date][transaction.symbol] = transaction.amount

    @_requires_dataframe
    def get_dataframe(self):
        """ Returns a copy of the internal _dataframe containing all given transactions of all stocks.
            If the _dataframe does not exist yet, it's generated before the first access."""
        return self._dataframe.copy()

    @_requires_dataframe
    def get_weights(self, weight_by='number', prices=None):
        """ Returns the current weight distributions of stocks in the portfolio.

        Args:
            weight_by (str): A parameter to distinguish between number of shares: 'number' or the
                total value of the shares of a certain stock: 'value' which is number_of_shares * share_price_today.
            prices: Dict with a 'symbol -> price' mapping where the symbol is a string and the price an int or float,
             for all stocks in the portfolio e.g. '{'appl': 100.32, 'sap': 80.43}'.

        Returns:
            A pandas series containing the weight distribution of the stocks in the portfolio weather by the amount
            of shares or by value.

        """
        # get the cumulative sum over the vertical axis
        shares_sums = self._dataframe.sum(axis=0)

        # total amount of shares
        shares_total = shares_sums.sum()

        if weight_by != 'value':
            return shares_sums / shares_total

        else:
            # convert the prices to a _dataframe for easy processing
            shares_prices = pd.DataFrame([prices.values()], columns=prices.keys())
            shares_values = shares_sums * shares_prices
            shares_totalvalue = shares_values.sum(axis=1)

            return shares_values / shares_totalvalue.iloc[0]

    @_requires_dataframe
    def get_current_value(self, prices=None):
        """ Returns the current total value of the single stocks as well as the overall portfolio value.

        Args:
            prices: Dict with a 'symbol -> price' mapping where the symbol is a string and the price an int or float,
                for all stocks in the portfolio e.g. '{'appl': 100.32, 'sap': 80.43}'.

        Returns:
            A _dataframe containing a column for each stock with its total value given the input price as well as a
            'TOTAL' column with the portfolio value.
        """
        shares_sums = self._dataframe.sum(axis=0)
        shares_prices = pd.DataFrame([prices.values()], columns=prices.keys())

        shares_values = shares_sums * shares_prices
        shares_values['TOTAL'] = shares_values.sum(axis=1)

        return shares_values

    @_requires_dataframe
    def get_prices(self, date=None, range='today'):
        """ Returns the market prices for the current porfolio in the given total timespan.

        Args:
            date (datetime): The datetime object which will be evaluated when range == 'date'.

            range (str):
                'today': Take today's date as end date and today - 1 day as start date.
                'date': Use the datetime object given in the date parameter as end date and end - 1 day as start date.
                'range': Use the specific date range given in all stock transactions, the earliest as start and the
                     latest as end date.
                'full': Use the earliest transaction date as a start date and today as end date.

        Returns:
            A pandas panel containing the market prices for the given stocks in the given timespan.

        """
        symbols = self.get_current_stocks()

        if range == 'today':
            dt_end = dt.date.today()
            dt_start = dt_end - dt.timedelta(days=1)

        elif range == 'date':
            assert isinstance(date, dt.date)
            dt_end = date
            dt_start = dt_end - dt.timedelta(days=1)

        elif range == 'range':
            index = self._dataframe.index
            dt_end = index[-1].date()
            dt_start = index[0].date()

        else:
            index = self._dataframe.index
            dt_end = dt.date.today()
            dt_start = index[0].date()

        return perfin.datautils.get_prices(symbols=symbols, dt_start=dt_start, dt_end=dt_end)
