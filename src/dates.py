from calendar import Day, JANUARY, MONDAY, Month, NOVEMBER, THURSDAY, monthrange
from datetime import date, timedelta
from functools import partial
from typing import Annotated

import holidays
from annotated_types import Doc, Gt, Interval
from dateutil.relativedelta import relativedelta

from dispatch import overload


class Span:
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

# Calendars
year: int = today.year
algeria = holidays.Algeria(years=year, language='en_US', categories=holidays.Algeria.supported_categories)
canada = holidays.Canada(years=year, language='en_US', categories=holidays.Canada.supported_categories)
china = holidays.China(years=year, language='en_US')
france = holidays.France(years=year, categories=holidays.France.supported_categories)
france._add_childrens_day("Children's Day", "NOV")

hongkong = holidays.HongKong(years=year, language='en_US')
israel = holidays.Israel(years=year, language='en_US', categories=('optional', 'public', 'school'))
italy = holidays.Italy(years=year, subdiv="MI")
mexico = holidays.Mexico(years=year, language='en_US')
us = holidays.UnitedStates(years=year)

# Dates
ALGERIAN_REVOLUTION_DAY = min(algeria.get_named('Revolution Day'))
ARMISTICE: date = min(france.get_named("Armistice"))
BEAUJOLAIS = third(year, NOVEMBER, THURSDAY)
BLACK_FRIDAY = (THANKSGIVING := min(us.get_named("Thanksgiving"))) + timedelta(days=1)
UN_CHILDRENS_DAY = min(france.get_named("Children's Day"))
CHRISTMAS: date = min(us.get_named('Christmas Day'))
CYBER_MONDAY = BLACK_FRIDAY + timedelta(days=3)
GOLDEN_WEEK = Span(min(china.get_named('National Day')), days=7)
HANUKKAH = israel.get_named("Hanukkah")
IMMACOLATA_CONCEZIONE: date = min(italy.get_named("Immacolata Concezione"))
LABOR_DAY: date = min(us.get_named("Labor Day"))
MID_AUTUMN_FESTIVAL: date = min(china.get_named('Mid-Autumn Festival'))
NEW_YEAR: date = min(us.get_named('New Year'))
PHILOSOPHY = third(year, NOVEMBER, THURSDAY)
ROSH_HASHANAH = israel.get_named("Rosh Hashanah")
SANTO_STEFANO: date = min(italy.get_named('Santo Stefano'))
SANT_AMBROGIO: date = min(italy.get_named("Sant'Ambrogio"))
SUKKOT = israel.get_named('Sukkot')
YENNAYER = min(algeria.get_named('Amazigh New Year'))

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
    'year',
    'yesterday',
)


def test_import():
    assert __all__, "Module did not import correctly"
