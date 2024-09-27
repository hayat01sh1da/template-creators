import sys
sys.path.append('./src')
from application import Application

try:
    _, username, unit, year, *_ = sys.argv
except ValueError:
    username = None
    unit     = None
    year     = None

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
