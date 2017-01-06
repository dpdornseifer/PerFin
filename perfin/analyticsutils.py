import logging
import pandas as pd


def getsavings(data, column_debit='Debit', column_credit='Credit', dt_start=None, dt_end=None, aggregation_period='M',
               thresh=1):
    """ consumes the checking account data and returns the monthly savings rate """

    if not isinstance(data.index, pd.DatetimeIndex):
        logging.getLogger().error("A pandas datetimeindex is required for the given dataframe")
        return pd.DataFrame()

    # create a copy of the indexed original data frame
    aggregated = data[dt_start:dt_end][[column_debit, column_credit]].copy()

    aggregated = aggregated.groupby(pd.TimeGrouper(aggregation_period)).sum()
    aggregated['Savings'] = aggregated[column_credit] - aggregated[column_debit]

    return aggregated.dropna(thresh=thresh)


def getoutliers(data, column_debit='Debit', column_group_by=None, dt_start=None, dt_end=None, m=1.96):
    """ detect outliers in the 'Debit' column and return the events - a normal distribution is expected """

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


def getstdev(data, dt_start=None, dt_end=None):
    """ returns a dict with the standard deviation of numeric columns over the given time period """

    stdev = data[dt_start:dt_end].std()
    return stdev[stdev.notnull()]


def getmovingaverage(data, dt_start=None, dt_end=None):
    """ returns the moving average """
    pass
