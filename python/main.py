import sys
import os
import shutil
import glob
sys.path.append('./src')
from application import Application

username = input('Provide your username(Default: hayat01sh1da): ').strip()
unit     = input('Provide your preferred unit d(daily - default), w(weekly) or m(monthly): ').strip()
year     = input('Provide the specific year you would like to create working report templates for(Default: the current year): ').strip()

params = dict()
for key, value in { 'username': username, 'unit': unit, 'year': year }.items():
    if value:
        params[key] = value

Application(**params).run()

pycaches = glob.glob(os.path.join('.', '**', '__pycache__'), recursive = True)
for pycache in pycaches:
    if os.path.exists(pycache):
        shutil.rmtree(pycache)
