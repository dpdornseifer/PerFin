import os
from perfin import importutils as iu
from perfin import analyticsutils as au


# read the environment variable which points to the .csv files
filepath = os.environ['PERFIN_FILES']
print('filepath', filepath)


# import the .csv files and convert the first column to the datetimeindex
data = iu.import_csvs_from_directory(filepath, 1)
print('raw data', data)


# calculate the savings
savings = au.get_savings(data)
print('savings', savings)


# get the stdev of the savings
stdev = au.get_stdev(savings)
print('stdev', stdev)


# print the available variables
print('following variables are available now ', ['data', 'savings', 'stdev'])
