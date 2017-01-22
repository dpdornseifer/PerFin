import glob
import logging
import pandas as pd


def import_csvs_from_directory(path, index=None):
    """ Function which takes a directory path as a input and delivers back one a pandas dataframe.

    Args:
        path (str): The path to the folder containing the csv files which should be imported.
        index (str): The name of the column which should be used and parsed as the index column.

    Returns:
        A single pandas dataframe containing all the data kept in the csv files. If index column has been
        provided which can be parsed the dataframe will have a datetime index.
    """

    dataframe = pd.DataFrame()
    files = glob.glob(path + '/*.csv')
    logging.getLogger().info('Following files have been found and will be imported {}'.format(files))

    if not files:
        logging.getLogger().warning('No files found in the given directory')
    else:
        for file in files:
            dataframe = dataframe.append(pd.read_csv(file, index_col=index, parse_dates=True))

    return dataframe
