from collections import namedtuple


class Stock:
    """ The stock object represents a specific stock symbol"""

    def __init__(self, symbol, name=None):
        """

        Args:
            symbol (str): The given stock symbol.

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
            price (float): Optional parameter. The price the stocks have been bought or sold for.
        """
        Transaction = namedtuple('Transaction', ['date', 'amount', 'price'])

        self.holdings.append(Transaction(date, amount, price))

    def get_total_amount(self):
        """ Returns the total amount of shares for the given stock.

        Returns (int):
            The total amount of shares fo the given stock.
        """
        return 0 if not self.holdings else sum([transaction.amount for transaction in self.holdings])


class Portfolio:
    """ A portfolio represents a collection of different stocks. """

    def __init__(self, stocks=None):
        """

        Args:
            stocks:
        """
        self.stocks = stocks

    def get_current_value(self):
        """ Returns the current value of the portfolio. """
        pass

    def get_weights(self):
        """ Returns the weight distribution of the single stocks in the portfolio. """
        pass

    def save(self):
        """ Save the portfolio to the harddrive. """
        pass