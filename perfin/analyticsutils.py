import logging
import pandas as pd


def getsavings(data, dt_start=None, dt_end=None, aggregation_period='M', thresh=1):
    """ consumes the checking account data and returns the monthly savings rate """

    if not isinstance(data.index, pd.DatetimeIndex):
        logging.getLogger().error("A pandas datetimeindex is required for the given dataframe")
        return pd.DataFrame()

    aggregated = data[dt_start:dt_end].groupby(pd.TimeGrouper(aggregation_period)).sum()
    return aggregated.dropna(thresh=thresh)


def getstdev(data, dt_start=None, dt_end=None):
    """ returns a dict with the standard deviation of numeric columns over the given time period """

    stdev = data[dt_start:dt_end].std()
    return stdev[stdev.notnull()]


def getmovingaverage(data, dt_start, dt_end):
    """ returns the moving average """
    pass


