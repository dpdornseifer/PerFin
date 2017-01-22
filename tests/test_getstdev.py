import os
from perfin import importutils as iu
from perfin import analyticsutils as au
from unittest import TestCase


class TestGetstdev(TestCase):

    def setUp(self):
        path = os.getcwd() + '/files'
        self.data = iu.import_csvs_from_directory(path, 1)

    def test_getstdev_return_no_nan(self):
        dt_start = '2016-01-01'
        dt_end = '2016-12-30'
        stdev = au.get_stdev(self.data, dt_start, dt_end)
        self.assertTrue(stdev.notnull().values.any())

    def test_getstdev_not_null(self):
        dt_start = '2011-01-01'
        dt_end = '2011-01-01'
        stdev = au.get_stdev(self.data, dt_start, dt_end)
        self.assertTrue(stdev.empty)
