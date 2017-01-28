import logging
import pandas as pd


def get_savings(data, column_debit='Debit', column_credit='Credit', dt_start=None, dt_end=None, aggregation_period='M'):
    """ Consumes the checking account data and returns the monthly savings rate.

    Args:
        data (dataframe): The panadas dataframe containing at least a debit and a credit column.
        column_debit (str): The column name for the debit column.
        column_credit (str): The column name for the credit column.
        dt_start (str): The start date (specific if given '2012-11-11' or the month '2012-11')
            from were the savings should be calculated.
        dt_end (str): The end date (specific if given '2012-11-11' or the month '2012-11')
            to were the savings should be calculated.
        aggregation_period (str): Single string character like 'M' for month specifying, over which period the savings
            are aggregated. A full specification can be found here:
            http://pandas.pydata.org/pandas-docs/stable/timeseries.html#timeseries-offset-aliases

    Returns:
        A pandas data frame, with an additional 'Savings' column and the time difference between start and end
        represented with a single row for each aggregation interval that is not null.

    """
    if not isinstance(data.index, pd.DatetimeIndex):
        logging.getLogger().error("A pandas datetimeindex is required for the given dataframe")
        return pd.DataFrame()

    # create a copy of the indexed original data frame
    aggregated = data[dt_start:dt_end][[column_debit, column_credit]].copy()

    aggregated = aggregated.groupby(pd.TimeGrouper(aggregation_period)).sum()
    aggregated = aggregated.fillna(0)

    aggregated['Savings'] = aggregated[column_credit] - aggregated[column_debit]
    return aggregated


def get_outliers(data, column_debit='Debit', column_group_by=None, dt_start=None, dt_end=None, m=1):
    """ Detect outliers in the 'Debit' column and return the events - a normal distribution is expected.

    Args:
        data (dataframe): The panadas dataframe containing at least a debit and a credit column.
        column_debit (str): The column name for the debit column.
        column_group_by (str): The column name that should be used to group the rows.
        dt_start (str): The start date (specific if given '2012-11-11' or the month '2012-11')
            from were the outliers should be calculated.
        dt_end (str): The end date (specific if given '2012-11-11' or the month '2012-11')
            to were the outliers should be calculated.
        m (int): The maximum deviation in terms of standard deviation units.

    Returns:
        A pandas dataframe containing all detected outliers market by a 'TRUE' value.

    """
    # create a copy of the required columns
    columns = [column_debit] + [column_group_by] if column_group_by else [column_debit]
    outlier = data[dt_start:dt_end][columns].copy()

    # look at all outliers taking the all debit transactions into account
    outlier_debit = abs(
        outlier[column_debit] - outlier[column_debit].mean() > m * outlier[column_debit].std())

    # look at the outliers when grouped by a specific column for example by 'description'
    # e.g. all venmo transactions together
    if column_group_by:
        group = outlier.groupby(column_group_by)
        outlier['Outlier_Grouped'] = group.transform(lambda x: abs(x - x.mean()) > m * x.std())
        group.transform(lambda x: abs(x - x.mean()) > m * x.std())
        outlier['Outlier_Debit'] = outlier_debit

        return outlier[outlier['Outlier_Grouped'] | outlier['Outlier_Debit']]

    # return all transactions which have been identified as outliers
    outlier['Outlier_Debit'] = outlier_debit

    return outlier[outlier['Outlier_Debit']]


def get_stdev(data, dt_start=None, dt_end=None):
    """ Returns a dict with the standard deviation of numeric columns over the given time period.

    Args:
        data (dataframe): The panadas dataframe containing at least a debit and a credit column.
        dt_start (str): The start date (specific if given '2012-11-11' or the month '2012-11')
            from were the standard deviation should be calculated.
        dt_end (str): The end date (specific if given '2012-11-11' or the month '2012-11')
            to were the standard deviation should be calculated.

    Returns:
        A pandas dataframe containing a single standard deviation for each colum in the input dataframe.

    """
    stdev = data[dt_start:dt_end].std()
    return stdev[stdev.notnull()]


def get_possible_investment_amount(data, savings_column='Savings', percentage=10, **kwargs):
    """ Returns a possible sum for a weekly, monthly stock investments considering the savings rate and the standard
        deviation.

    Args:
        data (dataframe): The dataframe which contains the savings column.
        savings_column (str): The columns which keeps the savings
        percentage (int): The percent wise amount of the monthly savings that can be invested into stocks or other
        equities.

    Returns:
        The distribution of the savings, mean and the savings stdandard devation. The possible investment amount is
        beeing calculated by taking percentage (recommended ~%10) * savings_mean.
        e.g.
            {possible_investment': 123.123,
            'savings_mean': 1231.23,
            'savings_stdev': 240.12'}
    """

    savings = get_savings(data, **kwargs)[savings_column]
    savings_mean = savings.mean()
    savings_stdev = savings.std()

    return {
        'possible_investment': savings_mean * (percentage / 100),
        'savings_mean': savings_mean,
        'savings_stdev': savings_stdev
    }

