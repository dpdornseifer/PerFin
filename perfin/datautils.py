""" Collection of utils that support gathering data from external systems and build up data pipelines. """

import logging

from pandas_datareader._utils import RemoteDataError
from zipline.data import load_bars_from_yahoo


def get_prices(symbols, dt_start, dt_end):
    """ Returns the 'adjusted' prices for the given timespan and the given symbols.

    Args:
        symbols [str]: The list of symbols
        dt_start (datetime): The data for the first t
        dt_end (datetime):

    Returns:
        Returns a pandas dataframe with the closing prices for the given symbols in the given timespan.

    """
    try:
        prices = load_bars_from_yahoo(stocks=symbols, start=dt_start, end=dt_end)

    except RemoteDataError as e:
        msg = "An error occurred reading the prices for the given symbols." \
              "Please make sure that the stock symbols are valid: {}".format(e)
        logging.getLogger().warning(msg)
        raise RemoteDataError(msg)

    return prices



def get_realtime_observer(symbols):
    """ Returns an RX observable ...."""
    # TODO
    pass