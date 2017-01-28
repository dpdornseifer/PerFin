import os
from unittest import TestCase
from perfin import importutils as iu
from perfin import analyticsutils as au


class TestGetPpossibleInvestmentAmount(TestCase):

    def setUp(self):
        path = os.getcwd() + '/files'
        self.data_datetimeindex = iu.import_csvs_from_directory(path, 1)

    def test_get_possible_investment_amount(self):
        self.assertAlmostEqual(au.get_possible_investment_amount(
            self.data_datetimeindex)['possible_investment'], -65.079, places=3)

