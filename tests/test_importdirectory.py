import os
from unittest import TestCase
from perfin import importutils as iu


class TestImportdirectory(TestCase):

    def setUp(self):
        self.path_empty = os.getcwd()
        self.path_files = os.getcwd() + '/files'

    def test_importdirectory_empty_dir(self):
        data = iu.importcsvsfromdirectory(self.path_empty)
        self.assertEqual(len(data), 0)

    def test_importdirectory_files_dir(self):
        data = iu.importcsvsfromdirectory(self.path_files)
        self.assertEqual(len(data), 16)

    def test_importdirectory_files_dir_datetime_index(self):
        from pandas import DatetimeIndex
        data = iu.importcsvsfromdirectory(self.path_files, 1)
        self.assertIsInstance(data.index, DatetimeIndex)



