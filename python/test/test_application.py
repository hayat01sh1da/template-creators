import unittest
import os
import glob
import shutil
import sys
sys.path.append('./src')
from application import Application

class TestApplication(unittest.TestCase):
    def setUp(self):
        self.year     = '2100'
        self.base_dir = os.path.join('.', 'summary_of_news_articles')

    ########## Regular Cases ##########

    def test_run_by_daily_unit(self):
        app = Application(unit = 'd', year = self.year)
        app.run()
        self._check_template_files('daily')

    def test_run_by_weekly_unit(self):
        app = Application(unit = 'w', year = self.year)
        app.run()
        self._check_template_files('weekly')

    def test_run_by_monthly_unit(self):
        app = Application(unit = 'm', year = self.year)
        app.run()
        self._check_template_files('monthly')

    ########## Irregular Cases ##########

    def test_initialize_with_invalid_unit(self):
        with self.assertRaises(ValueError, msg = 'Provide d, w or y as a valid unit'):
            Application(unit = 'foobar', year = self.year).run()

    def test_initialize_with_non_digit_argument(self):
        with self.assertRaises(ValueError, msg = 'invalid literal for int() with base 10: "foobar"'):
            Application(year = 'foobar')

    def test_initialize_with_invalid_value_as_year(self):
        with self.assertRaises(ValueError, msg = 'Year must be 4 digits'):
            Application(year = '20233')

    def test_initialize_with_older_year(self):
        with self.assertRaises(ValueError, msg = 'Provide newer than or equal to the current year'):
            Application(year = '2022')

    def tearDown(self):
        destination_dir = os.path.join(self.base_dir, self.year)
        if os.path.isdir(destination_dir):
            shutil.rmtree(destination_dir)
        if self._has_no_template():
            shutil.rmtree(self.base_dir)

    # private

    def _check_template_files(self, unit):
        filepath = os.path.join('.', 'test', 'checking_files', '{unit}_templates.txt'.format(unit = unit))
        with open(filepath) as f:
            expected_templates = f.read().split('\n')
        expected_templates.pop()
        actual_templates = glob.glob(os.path.join('.', 'summary_of_news_articles', self.year, '**', '*.md'))
        self.assertListEqual(expected_templates, actual_templates)

    def _has_no_template(self):
        len(glob.glob(os.path.join('.', 'summary_of_news_articles', '**', '*.md'))) == 0

if __name__ == '__main__':
    unittest.main()
