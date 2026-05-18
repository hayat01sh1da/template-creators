import pytest
import glob
import re
import os
import shutil
import sys
from collections.abc import Iterator

sys.path.append('./src')


_USERNAME = 'hayat01sh1da'
_YEAR = '2100'
_BASE_DIR = os.path.join('..', '..', 'working-report', _USERNAME)
_TEMPLATE_FILES_GLOB = os.path.join(
    '..',
    '..',
    'working-report',
    _USERNAME,
    _YEAR,
    '**',
    '*.md')


@pytest.fixture(autouse=True)
def __cleanup_caches__() -> Iterator[None]:
    yield
    cache_dir = re.compile(r'^(?:__pycache__|\.pytest_cache|\.mypy_cache)$')
    for root, dirs, _ in os.walk('.'):
        for name in list(dirs):
            if cache_dir.match(name):
                shutil.rmtree(os.path.join(root, name), ignore_errors=True)
                dirs.remove(name)


@pytest.fixture(autouse=True)
def _cleanup_template_dir() -> Iterator[None]:
    yield
    destination_dir = os.path.join(_BASE_DIR, _YEAR)
    if os.path.exists(destination_dir):
        shutil.rmtree(destination_dir)
    if len(glob.glob(_TEMPLATE_FILES_GLOB, recursive=True)
           ) == 0 and os.path.exists(_BASE_DIR):
        shutil.rmtree(_BASE_DIR)
