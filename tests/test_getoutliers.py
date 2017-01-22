import os
from datetime import date
from unittest import TestCase
from perfin import importutils as iu
from perfin import analyticsutils as au


class TestGetoutliers(TestCase):
    def setUp(self):
        path = os.getcwd() + '/files'
        self.data_datetimeindex = iu.import_csvs_from_directory(path, 1)

    def test_getoutliers_all(self):
        self.assertEqual(len(au.get_outliers(self.data_datetimeindex)), 1)
        self.assertEqual(au.get_outliers(self.data_datetimeindex).index[0].date(), date(2015, 7, 21))

    def test_getoutliers_group(self):
        self.assertEqual(len(au.get_outliers(self.data_datetimeindex, column_group_by='Description', m=1)), 2)
        self.assertEqual(au.get_outliers(self.data_datetimeindex).index[0].date(), date(2015, 7, 21))

    def test_getoutliers_none(self):
        self.assertEqual(
            len(au.get_outliers(self.data_datetimeindex, column_group_by='Description', dt_start='2015-7-22', m=1)), 2)
        self.assertEqual(
            au.get_outliers(self.data_datetimeindex, column_group_by='Description', dt_start='2015-7-22', m=1).index[
                1].date(), date(2016, 12, 21))
