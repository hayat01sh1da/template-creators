import sys
sys.path.append('./src')
from application import Application

try:
    _, unit, year, *_ = sys.argv
except ValueError:
    unit = None
    year = None

if unit and year:
    app = Application(unit = unit, year = year)
elif unit:
    app = Application(unit = unit)
elif year:
    app = Application(year = year)
else:
    app = Application()

app.run()
