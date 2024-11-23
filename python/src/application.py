import os
import datetime
import calendar

class Application:
    def __init__(self, username = 'hayat01sh1da', unit = 'd', year = datetime.date.today().strftime('%Y')):
        USERNAMES = ('hayat01sh1da')
        if not username in USERNAMES:
            raise ValueError('{username} is NOT a permitted username.'.format(username = username))
        match unit:
            case 'd' | 'w' | 'm':
                self.unit = unit
            case _:
                raise ValueError('Provide d, w or m as a valid unit.')
        int(year)
        if len(year) > 4:
            raise ValueError('Year must be 4 digits.')
        if int(year) < int(datetime.date.today().strftime('%Y')):
            raise ValueError('Provide newer than or equal to the current year.')
        self.username = username
        self.year     = year
        self.months   = list()
        for i in range(1, 13):
            self.months.append(calendar.month_name[i])

    def run(self):
        for i, month in enumerate(self.months):
            index     = '{:02}'.format(i + 1)
            directory = os.path.join('..', '..', 'working-report', self.username, '{year}'.format(year = self.year), '{index}_{month}'.format(index = index, month = month))
            match self.unit:
                case 'd' | 'w':
                    for d in range(1, 32):
                        match month:
                            case 'February':
                                if self.__is_leap_year__() and d > 29:
                                    continue
                                elif d > 28:
                                    continue
                                self.__create_template__(d, directory, index, month)
                            case 'April' | 'June' | 'September' | 'November':
                                if d > 30:
                                    continue
                                self.__create_template__(d, directory, index, month)
                            case _:
                                self.__create_template__(d, directory, index, month)
                case 'm':
                    self.__export_template__(directory = directory, index = index, month = month)
                case _:
                    raise ValueError('Provide d, w or m as a valid unit.')

    # private

    def __full_unit__(self):
        match self.unit:
            case 'd':
                return 'daily'
            case 'w':
                return 'weekly'
            case 'm':
                return 'monthly'

    def __is_monday__(self, month, day):
        # 0: Monday
        # 1: Tuesday
        # 2: Wednesday
        # 3: Thursday
        # 4: Friday
        # 5: Saturday
        # 6: Sunday
        return datetime.date(int(self.year), month, day).weekday() == 0

    def __is_saturday__(self, month, day):
        # 0: Monday
        # 1: Tuesday
        # 2: Wednesday
        # 3: Thursday
        # 4: Friday
        # 5: Saturday
        # 6: Sunday
        return datetime.date(int(self.year), month, day).weekday() == 5

    def __is_sunday__(self, month, day):
        # 0: Monday
        # 1: Tuesday
        # 2: Wednesday
        # 3: Thursday
        # 4: Friday
        # 5: Saturday
        # 6: Sunday
        return datetime.date(int(self.year), month, day).weekday() == 6

    def __is_weekend__(self, month, day):
        date = datetime.date(int(self.year), month, day).weekday()
        return date == 5 or date == 6

    def __is_leap_year__(self):
        return int(self.year) % 400 == 0 or (int(self.year) % 100 != 0 and int(self.year) % 4 == 0)

    def __body__(self, date):
        text =  "# TITLE on #{date}\n\n"
        text += "## 1. CATEGORY\n\n"
        text += "### 1-1. SUBCATEGORY\n\n"
        text += "- ITEM\n"
        text += "- ITEM\n"
        text += "- ITEM\n"
        text += "### 1-2. SUBCATEGORY\n\n"
        text += "- ITEM\n"
        text += "- ITEM\n"
        text += "- ITEM\n"
        text += "### 1-3. SUBCATEGORY\n\n"
        text += "- ITEM\n"
        text += "- ITEM\n"
        text += "- ITEM\n"
        text += "## 2. CATEGORY\n\n"
        text += "### 2-1. SUBCATEGORY\n\n"
        text += "- ITEM\n"
        text += "- ITEM\n"
        text += "- ITEM\n"
        text += "### 2-2. SUBCATEGORY\n\n"
        text += "- ITEM\n"
        text += "- ITEM\n"
        text += "- ITEM\n"
        text += "### 2-3. SUBCATEGORY\n\n"
        text += "- ITEM\n"
        text += "- ITEM\n"
        text += "- ITEM\n"
        return text

    def __export_template__(self, directory, index, day = '', month = ''):
        date = ''
        if not len(day) == 0:
            date += '{day} '.format(day = day)
        date += '{month} {year}'.format(month = month, year = self.year)
        filename = os.path.join(directory, '{year}{index}{day}_{full_unit}_working_report.md'.format(year = self.year, index = index, day = day, full_unit = self.__full_unit__()))
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(filename, 'w') as f:
            f.write(self.__body__(date))

    def __create_template__(self, d, directory, index, month):
        day = '{:02}'.format(d)
        if self.unit == 'd':
            if self.__is_weekend__(int(index), d):
                return
            else:
                self.__export_template__(directory, index, day, month)
        else:
            if not self.__is_monday__(int(index), d):
                return
            else:
                self.__export_template__(directory, index, day, month)
