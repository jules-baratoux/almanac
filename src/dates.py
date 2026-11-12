from calendar import Day, JANUARY, MONDAY, Month, monthrange
from collections.abc import Iterable
from datetime import date, timedelta
from functools import partial
from typing import Annotated

from annotated_types import Doc, Gt, Interval
from dateutil.relativedelta import relativedelta

from dispatch import overload


class Span(Iterable[date]):
    start: date
    end: date

    @overload
    def __init__(self, start: date, end: date):
        self.start = start
        self.end = end

    @overload
    def __init__(self, start: date, days: Annotated[int, Gt(1), Doc("Total amount of days")]):
        self.start = start
        self.end = start + timedelta(days=days - 1)

    def __iter__(self):
        yield self.start
        yield self.end

    def __repr__(self):
        return repr((self.start, self.end))


def weekday(year: int, month: Month, weekday: Day,
            index: Annotated[int, Interval(ge=0, le=5), Doc("Index of weekday in the month")]):
    first_weekday, _ = monthrange(year, month)

    # Calculate offset to the first occurrence
    days_to_first = (weekday - first_weekday) % 7

    # Calculate the exact target day
    day = 1 + days_to_first + index * 7

    return date(year, month, day)


third = partial(weekday, index=2)

# Named relative dates
today = date.today()
yesterday = today + relativedelta(days=-1)
day_before_yesterday = today + relativedelta(days=-2)
tomorrow = today + relativedelta(days=+1)
day_after_tomorrow = today + relativedelta(days=+2)
next_week = today + relativedelta(days=+1, weekday=MONDAY)
week_after_next = next_week + relativedelta(weeks=1)
next_month = today + relativedelta(months=+1, day=1)
month_after_next = today + relativedelta(months=+2, day=1)
next_year = today + relativedelta(years=1, month=JANUARY, day=1)

# Dates
ALGERIAN_REVOLUTION_DAY = date(2026, 11, 1)
ARMISTICE = date(2026, 11, 11)
BEAUJOLAIS = date(2026, 11, 19)
BLACK_FRIDAY = date(2026, 11, 27)
UN_CHILDRENS_DAY = date(2026, 11, 20)
CHRISTMAS = date(2026, 12, 25)
CYBER_MONDAY = date(2026, 11, 30)
GOLDEN_WEEK = date(2026, 10, 1), date(2026, 10, 7)
HANUKKAH = date(2026, 12, 5), date(2026, 12, 12)
IMMACOLATA_CONCEZIONE = date(2026, 12, 8)
LABOR_DAY = date(2026, 9, 7)
MID_AUTUMN_FESTIVAL = date(2026, 9, 25)
NEW_YEAR = date(2026, 1, 1)
PHILOSOPHY = date(2026, 11, 19)
ROSH_HASHANAH = date(2026, 9, 12), date(2026, 9, 13)
SANTO_STEFANO = date(2026, 12, 26)
SANT_AMBROGIO = date(2026, 12, 7)
SUKKOT = date(2026, 9, 26), date(2026, 10, 1)
THANKSGIVING = date(2026, 11, 26)
YENNAYER = date(2026, 1, 12)

__all__ = (
    'ALGERIAN_REVOLUTION_DAY',
    'ARMISTICE',
    'BEAUJOLAIS',
    'BLACK_FRIDAY',
    'UN_CHILDRENS_DAY',
    'CHRISTMAS',
    'CYBER_MONDAY',
    'GOLDEN_WEEK',
    'HANUKKAH',
    'IMMACOLATA_CONCEZIONE',
    'LABOR_DAY',
    'MID_AUTUMN_FESTIVAL',
    'NEW_YEAR',
    'PHILOSOPHY',
    'ROSH_HASHANAH',
    'SANTO_STEFANO',
    'SANT_AMBROGIO',
    'SUKKOT',
    'THANKSGIVING',
    'YENNAYER',
    'day_after_tomorrow',
    'day_before_yesterday',
    'month_after_next',
    'next_month',
    'next_week',
    'next_year',
    'today',
    'tomorrow',
    'week_after_next',
    'yesterday',
)


def test_import():
    assert __all__, "Module did not import correctly"


def hardcode():
    for name in __all__:
        if name.isupper():
            value = globals()[name]
            _repr = f"{min(value)!r}, {max(value)!r}" if isinstance(value, Iterable) else repr(value)
            print(f"{name} = {_repr}")


if __name__ == '__main__':
    hardcode()
