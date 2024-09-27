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
        self.base_dir       = os.path.join('..', self.username, 'summary_of_news_articles')
        self.template_files = os.path.join('..', self.username, 'summary_of_news_articles', self.year, '**', '*.md')

    ########## Regular Cases ##########

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

    ########## Irregular Cases ##########

    def test_initialize_with_invalid_username(self):
        with self.assertRaises(ValueError, msg = 'InvalidUsername is NOT an allowed value'):
            Application(username = 'InvalidUsername', unit = 'foobar', year = self.year).run()

    def test_initialize_with_invalid_unit(self):
        with self.assertRaises(ValueError, msg = 'Provide d, w or y as a valid unit'):
            Application(username = self.username, unit = 'foobar', year = self.year).run()

    def test_initialize_with_non_digit_argument(self):
        with self.assertRaises(ValueError, msg = 'invalid literal for int() with base 10: "foobar"'):
            Application(username = self.username, year = 'foobar')

    def test_initialize_with_invalid_value_as_year(self):
        with self.assertRaises(ValueError, msg = 'Year must be 4 digits'):
            Application(username = self.username, year = '20233')

    def test_initialize_with_older_year(self):
        with self.assertRaises(ValueError, msg = 'Provide newer than or equal to the current year'):
            Application(username = self.username, year = '2022')

    def tearDown(self):
        destination_dir = os.path.join(self.base_dir, self.year)
        if os.path.isdir(destination_dir):
            shutil.rmtree(destination_dir)
        if self.__has_no_template__():
            shutil.rmtree(self.base_dir)

    # private

    def __check_template_files__(self, unit):
        filepath = os.path.join('..', 'testing_file_lists', '{unit}_templates.txt'.format(unit = unit))
        with open(filepath) as f:
            expected_templates = f.read().split('\n')
        expected_templates.pop()
        actual_templates = glob.glob(os.path.join(self.template_files))
        self.assertListEqual(expected_templates, actual_templates)

    def __has_no_template__(self):
        len(glob.glob(os.path.join(self.template_files))) == 0

if __name__ == '__main__':
    unittest.main()
