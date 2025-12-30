import unittest
import os
import glob
import shutil
import sys
sys.path.append('./src')
from application import Application

class TestApplication(unittest.TestCase):
    def setUp(self):
        self.username       = 'hayat01sh1da'
        self.year           = '2100'
        self.base_dir       = os.path.join('..', '..', 'working-report', self.username)
        self.template_files = os.path.join('..', '..', 'working-report', self.username, self.year, '**', '*.md')
        self.pycaches       = glob.glob(os.path.join('.', '**', '__pycache__'), recursive = True)

    def tearDown(self):
        destination_dir = os.path.join(self.base_dir, self.year)
        if os.path.exists(destination_dir):
            shutil.rmtree(destination_dir)
        if self.__has_no_template__():
            shutil.rmtree(self.base_dir)
        for pycache in self.pycaches:
            if os.path.exists(pycache):
                shutil.rmtree(pycache)

    # private

    def __check_template_files__(self, unit):
        filepath = os.path.join('..', 'testing_file_lists', f'{unit}_templates.txt')
        with open(filepath) as f:
            expected_templates = f.read().split('\n')
        expected_templates.pop()
        actual_templates = glob.glob(os.path.join(self.template_files), recursive = True)
        if not str(type(actual_templates)) == "<class 'NoneType'>":
            actual_templates.sort()
        self.assertListEqual(actual_templates, expected_templates)

    def __has_no_template__(self):
        len(glob.glob(os.path.join(self.template_files), recursive = True)) == 0

class TestRegularCase(TestApplication):
    def test_run_by_daily_unit(self):
        app = Application(username = self.username, unit = 'd', year = self.year)
        app.run()
        self.__check_template_files__('daily')

    def test_run_by_weekly_unit(self):
        app = Application(username = self.username, unit = 'w', year = self.year)
        app.run()
        self.__check_template_files__('weekly')

    def test_run_by_monthly_unit(self):
        app = Application(username = self.username, unit = 'm', year = self.year)
        app.run()
        self.__check_template_files__('monthly')

class TestIrregularCase(TestApplication):
    def test_initialize_with_invalid_username(self):
        with self.assertRaises(ValueError) as cm:
            Application(username = 'InvalidUsername', unit = 'foobar', year = self.year).run()
        self.assertEqual('InvalidUsername is NOT a permitted username.', str(cm.exception))

    def test_initialize_with_invalid_unit(self):
        with self.assertRaises(ValueError) as cm:
            Application(username = self.username, unit = 'foobar', year = self.year).run()
        self.assertEqual('Provide d, w or m as a valid unit.', str(cm.exception))

    def test_initialize_with_non_digit_argument(self):
        with self.assertRaises(ValueError) as cm:
            Application(username = self.username, year = 'foobar')
        self.assertEqual('invalid literal for int() with base 10: "foobar"', str(cm.exception))

    def test_initialize_with_invalid_value_as_year(self):
        with self.assertRaises(ValueError) as cm:
            Application(username = self.username, year = '20233')
        self.assertEqual('Year must be 4 digits.', str(cm.exception))

    def test_initialize_with_older_year(self):
        with self.assertRaises(ValueError) as cm:
            Application(username = self.username, year = '2022')
        self.assertEqual('Provide newer than or equal to the current year.', str(cm.exception))

if __name__ == '__main__':
    unittest.main()
