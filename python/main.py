import sys
import os
import shutil
import glob
sys.path.append('./src')
from application import Application

username = input('Provide your username(Default: hayat01sh1da): ')
unit     = input('Provide your preferred unit d(daily - default), w(weekly) or m(monthly): ')
year     = input('Provide the specific year you would like to create working report templates for(Default: the current year): ')

if username and unit and year:
    app = Application(username = username, unit = unit, year = year)
elif username:
    app = Application(username = username)
elif unit:
    app = Application(unit = unit)
elif year:
    app = Application(year = year)
else:
    app = Application()

app.run()

pycaches = glob.glob(os.path.join('.', '**', '__pycache__'), recursive = True)
for pycache in pycaches:
    if os.path.isdir(pycache):
        shutil.rmtree(pycache)
