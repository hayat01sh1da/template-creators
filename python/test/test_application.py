import glob
import os

import pytest

from application import Application


USERNAME = 'hayat01sh1da'
YEAR = '2100'
TEMPLATE_FILES_GLOB = os.path.join(
    '..',
    '..',
    'working-report',
    USERNAME,
    YEAR,
    '**',
    '*.md')


def _check_template_files(unit: str) -> None:
    filepath = os.path.join(
        '..',
        'testing_file_lists',
        f'{unit}_templates.txt')
    with open(filepath) as f:
        expected = f.read().split('\n')
    expected.pop()
    actual = sorted(glob.glob(TEMPLATE_FILES_GLOB, recursive=True))
    assert actual == expected


@pytest.mark.parametrize(
    ('unit', 'unit_name'),
    [
        ('d', 'daily'),
        ('w', 'weekly'),
        ('m', 'monthly'),
    ],
)
def test_run_by_unit(unit: str, unit_name: str) -> None:
    Application(username=USERNAME, unit=unit, year=YEAR).run()
    _check_template_files(unit_name)


def test_initialize_with_invalid_username() -> None:
    with pytest.raises(ValueError, match=r'^InvalidUsername is NOT a permitted username\.$'):
        Application(username='InvalidUsername', unit='foobar', year=YEAR).run()


def test_initialize_with_invalid_unit() -> None:
    with pytest.raises(ValueError, match=r'^Provide d, w or m as a valid unit\.$'):
        Application(username=USERNAME, unit='foobar', year=YEAR).run()


def test_initialize_with_non_digit_argument() -> None:
    with pytest.raises(ValueError, match=r"^invalid literal for int\(\) with base 10: 'foobar'$"):
        Application(username=USERNAME, year='foobar')


def test_initialize_with_invalid_value_as_year() -> None:
    with pytest.raises(ValueError, match=r'^Year must be 4 digits\.$'):
        Application(username=USERNAME, year='20233')


def test_initialize_with_older_year() -> None:
    with pytest.raises(ValueError, match=r'^Provide newer than or equal to the current year\.$'):
        Application(username=USERNAME, year='2022')
