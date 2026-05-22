import os
import sys

from invoke import Context, task

_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_ROOT, 'src'))

from application import Application  # noqa: E402


@task
def run_template_creator(c: Context) -> None:
    """Run Template Creator"""
    print('Provide your username(Default: hayat01sh1da)')
    username = input().strip()

    print('Provide your preferred unit d(daily - default), w(weekly) '
          'or m(monthly)')
    unit = input().strip()

    print('Provide the specific year you would like to create working '
          'report templates for(Default: the current year)')
    year = input().strip()

    params: dict[str, str] = {}
    for key, value in {
        'username': username, 'unit': unit, 'year': year,
    }.items():
        if value:
            params[key] = value

    Application(**params).run()


@task(default=True)
def test(c: Context) -> None:
    """Run all tests"""
    c.run('pytest .')
