import glob
import os

import pytest

from application import Application


USERNAME = 'hayat01sh1da'
YEAR = '2100'
TEMPLATE_FILES_GLOB = os.path.join(
    '..', '..', 'working-report', USERNAME, YEAR, '**', '*.md')


def _check_template_files(unit: str) -> None:
    filepath = os.path.join(
        '..', 'testing_file_lists', f'{unit}_templates.txt')
    with open(filepath) as f:
        expected = [line for line in f.read().split('\n') if line]
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
    Application.run(username=USERNAME, unit=unit, year=YEAR)
    _check_template_files(unit_name)


def test_initialize_with_invalid_username() -> None:
    with pytest.raises(
            Application.ValueError,
            match=r'^InvalidUsername is NOT a permitted username\.$'):
        Application.run(username='InvalidUsername', unit='m', year=YEAR)


def test_initialize_with_invalid_unit() -> None:
    with pytest.raises(
            Application.ValueError,
            match=r'^Provide d, w or m as a valid unit\.$'):
        Application.run(username=USERNAME, unit='foobar', year=YEAR)


def test_initialize_with_non_digit_argument() -> None:
    with pytest.raises(
            ValueError,
            match=r"^invalid literal for int\(\) with base 10: 'foobar'$"):
        Application.run(username=USERNAME, year='foobar')


def test_initialize_with_invalid_value_as_year() -> None:
    with pytest.raises(
            Application.DigitLengthError,
            match=r'^Year must be 4 digits\.$'):
        Application.run(username=USERNAME, year='20233')


def test_initialize_with_older_year() -> None:
    with pytest.raises(
            Application.ValueError,
            match=r'^Provide newer than or equal to the current year\.$'):
        Application.run(username=USERNAME, year='2022')
