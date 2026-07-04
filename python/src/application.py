import calendar
import datetime
import os
from typing import Iterator


class Application:
    """Generates working-report markdown templates for a username under
    `../../working-report/<username>/<year>/`, one file per day, week, or
    month."""

    class ValueError(Exception):
        pass

    class DigitLengthError(Exception):
        pass

    USERNAMES = ('hayat01sh1da',)
    with open(os.path.join('..', 'markdown', 'body_template.md')) as _f:
        BODY_TEMPLATE = _f.read()
    del _f
    FULL_UNITS = {'d': 'daily', 'w': 'weekly', 'm': 'monthly'}
    MONTHS_WITH_30_DAYS = ('April', 'June', 'September', 'November')

    @classmethod
    def run(cls, username: str = 'hayat01sh1da', unit: str = 'd',
            year: str | None = None) -> None:
        if year is None:
            year = datetime.date.today().strftime('%Y')
        instance = cls(username=username, unit=unit, year=year)
        instance.validate_username()
        instance.validate_unit()
        instance.validate_year()
        instance._run()

    def __init__(self, username: str = 'hayat01sh1da', unit: str = 'd',
                 year: str | None = None) -> None:
        self._username = username
        self._unit = unit
        self._year = year if year is not None else \
            datetime.date.today().strftime('%Y')

    def validate_username(self) -> None:
        if self._username not in self.USERNAMES:
            raise self.ValueError(
                f'{self._username} is NOT a permitted username.')

    def validate_unit(self) -> str:
        match self._unit:
            case 'd' | 'w' | 'm':
                return self._unit
            case _:
                raise self.ValueError('Provide d, w or m as a valid unit.')

    def validate_year(self) -> str:
        int(self._year)
        if len(self._year) > 4:
            raise self.DigitLengthError('Year must be 4 digits.')
        if int(self._year) < int(datetime.date.today().strftime('%Y')):
            raise self.ValueError(
                'Provide newer than or equal to the current year.')
        return self._year

    # private

    def _run(self) -> None:
        for i, month in enumerate(self._month_names(), start=1):
            index = f'{i:02}'
            directory = os.path.join(
                '..', '..', 'working-report', self._username,
                self._year, f'{index}_{month}',
            )
            self._process_month(month, i, index, directory)

    def _month_names(self) -> list[str]:
        return [calendar.month_name[i] for i in range(1, 13)]

    def _process_month(self, month: str, month_index: int,
                       index: str, directory: str) -> None:
        match self._unit:
            case 'd' | 'w':
                self._process_days(month, month_index, index, directory)
            case 'm':
                self._export_template(
                    directory=directory, index=index, month=month)

    def _process_days(self, month: str, month_index: int,
                      index: str, directory: str) -> None:
        for d in self._create_templates(month):
            if self._skip_day(month_index, d):
                continue
            day = f'{d:02}'
            self._export_template(
                directory=directory, index=index, day=day, month=month)

    def _skip_day(self, month_index: int, day: int) -> bool:
        if self._unit == 'd':
            return self._weekend(month_index, day)
        return not self._monday(month_index, day)

    def _full_unit(self) -> str:
        return self.FULL_UNITS.get(self._unit, '')

    def _monday(self, month: int, day: int) -> bool:
        return datetime.date(int(self._year), month, day).weekday() == 0

    def _weekend(self, month: int, day: int) -> bool:
        return datetime.date(int(self._year), month, day).weekday() >= 5

    def _leap_year(self) -> bool:
        y = int(self._year)
        return y % 400 == 0 or (y % 100 != 0 and y % 4 == 0)

    def _body(self, date: str) -> str:
        return self.BODY_TEMPLATE % date

    def _export_template(self, directory: str = '', index: str = '',
                         day: str = '', month: str = '') -> None:
        date_parts: list[str] = []
        if day:
            date_parts.append(f'{day} ')
        date_parts.append(f'{month} {self._year}')
        filename = os.path.join(
            directory,
            f'{self._year}{index}{day}_{self._full_unit()}'
            '_working_report.md',
        )
        os.makedirs(directory, exist_ok=True)
        if not os.path.exists(filename):
            with open(filename, 'w') as f:
                f.write(self._body(''.join(date_parts)))

    def _create_templates(self, month: str) -> Iterator[int]:
        for d in range(1, 32):
            if self._skip_day_of_month(month, d):
                continue
            yield d

    def _skip_day_of_month(self, month: str, day: int) -> bool:
        if month == 'February':
            return day > (29 if self._leap_year() else 28)
        if month in self.MONTHS_WITH_30_DAYS:
            return day > 30
        return False
