import os
from perfin import importutils as iu
from perfin import analyticsutils as au
from perfin import pltutils as plt

# set the environment variable first for the files
# export PERFIN_FILES=/Users/i841521/PycharmProjects/perfin/tests/files
#exec(open("/Users/i841521/PycharmProjects/perfin/examples/playground.py
#    ...: ").read(), globals()

filepath = os.environ['PERFIN_FILES']
print('filepath', filepath)

data = iu.importcsvsfromdirectory(filepath, 1)
print('raw data', data)

savings = au.getsavings(data)
print('savings', savings)

stdev = au.getstdev(savings)
print('stdev', stdev)

print('following variables are available now ', ['data', 'savings', 'stdev'])
