import glob
import logging
import pandas as pd


def importcsvsfromdirectory(path, index=None):
    """ function which takes a directory path as a input and delivers back one a pandas dataframe """

    dataframe = pd.DataFrame()
    files = glob.glob(path + '/*.csv')
    logging.getLogger().info('Following files have been found and will be imported {}'.format(files))

    if not files:
        logging.getLogger().warning('No files found in the given directory')
    else:
        for file in files:
            dataframe = dataframe.append(pd.read_csv(file, index_col=index, parse_dates=True))

    return dataframe



