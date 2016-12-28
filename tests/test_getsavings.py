import os
from unittest import TestCase
from perfin import analyticsutils as au
from perfin import importutils as iu


class TestGetsavings(TestCase):

    def setUp(self):
        path = os.getcwd() + '/files'
        self.data_datetimeindex = iu.importcsvsfromdirectory(path, 1)
        self.data_no_datetimeindex = iu.importcsvsfromdirectory(path, 0)

    def test_getsavings_non_datetimeindex(self):
        self.assertTrue(au.getsavings(self.data_no_datetimeindex).empty)

    def test_getsavings_rows(self):
        self.assertEqual(len(au.getsavings(self.data_datetimeindex, aggregation_period='W', thresh=0)), 65)
        self.assertEqual(len(au.getsavings(self.data_datetimeindex, thresh=0)), 15)
        self.assertEqual(len(au.getsavings(self.data_datetimeindex)), 4)

    def test_getsavings_aggregates(self):
        self.assertAlmostEqual(au.getsavings(self.data_datetimeindex)['2016-12']['Debit'].iloc[0], 135.1)
