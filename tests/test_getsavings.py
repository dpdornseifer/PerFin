import os
from unittest import TestCase
from perfin import analyticsutils as au
from perfin import importutils as iu


class TestGetsavings(TestCase):

    def setUp(self):
        path = os.getcwd() + '/files'
        self.data_datetimeindex = iu.import_csvs_from_directory(path, 1)
        self.data_no_datetimeindex = iu.import_csvs_from_directory(path, 0)

    def test_getsavings_non_datetimeindex(self):
        self.assertTrue(au.get_savings(self.data_no_datetimeindex).empty)

    def test_getsavings_rows(self):
        self.assertEqual(len(au.get_savings(self.data_datetimeindex, aggregation_period='W')), 75)
        self.assertEqual(len(au.get_savings(self.data_datetimeindex)), 18)

    def test_getsavings_aggregates(self):
        self.assertAlmostEqual(au.get_savings(self.data_datetimeindex)['2016-12']['Debit'].iloc[0], 1882.85)

