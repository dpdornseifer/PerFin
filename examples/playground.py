import os
from perfin import importutils as iu
from perfin import analyticsutils as au



# read the environment variable which points to the .csv files
filepath = os.environ['PERFIN_FILES']
print('filepath', filepath)


# import the .csv files and convert the first column to the datetimeindex
data = iu.importcsvsfromdirectory(filepath, 1)
print('raw data', data)


# calculate the savings
savings = au.getsavings(data)
print('savings', savings)


# get the stdev of the savings
stdev = au.getstdev(savings)
print('stdev', stdev)


# print the available variables
print('following variables are available now ', ['data', 'savings', 'stdev'])
