from calendar import Day, JANUARY, Month, NOVEMBER, THURSDAY, monthrange
from datetime import date, timedelta
from functools import partial
from typing import Annotated, Sequence

import holidays

from annotated import Field
from dispatch import overload


class Span:
    start: date
    end: date

    @overload
    def __init__(self, start: date, end: date):
        self.start = start
        self.end = end

    @overload
    def __init__(self, start: date, days: Annotated[int, Field(gt=1, description="Total amount of days")]):
        self.start = start
        self.end = start + timedelta(days=days - 1)

    def __iter__(self):
        yield self.start
        yield self.end


def weekday(year: int, month: Month, weekday: Day,
            index: Annotated[int, Field(ge=0, le=5, description="Index of weekday in the month")]):
    first_weekday, _ = monthrange(year, month)

    # Calculate offset to the first occurrence
    days_to_first = (weekday - first_weekday) % 7

    # Calculate the exact target day
    day = 1 + days_to_first + index * 7

    return date(year, month, day)


third = partial(weekday, index=2)


def min_max(sequence: Sequence[date]):
    start = min(sequence)
    end = max(sequence)
    return Span(start, end)


# Named relative dates
today = date.today()
yesterday = today - timedelta(days=1)
day_before_yesterday = today - timedelta(days=2)
tomorrow = today + timedelta(days=1)
day_after_tomorrow = tomorrow + timedelta(days=1)
next_week = today + timedelta(days=(7 - today.weekday()))
week_after_next = next_week + timedelta(days=7)
next_month = today.replace(month=today.month + 1, day=1)
month_after_next = next_month.replace(month=next_month.month + 1)
next_year = date(today.year + 1, JANUARY, 1)

# Holiday calendars
year = today.year
algeria = holidays.Algeria(years=year, language='en_US', categories=holidays.Algeria.supported_categories)
china = holidays.China(years=year, language='en_US')
france = holidays.France(years=year)
hongkong = holidays.HongKong(years=year, language='en_US')
israel = holidays.Israel(years=year, language='en_US', categories=('optional', 'public', 'school'))
italy = holidays.Italy(years=year, subdiv="MI")
mexico = holidays.Mexico(years=year, language='en_US')
us = holidays.UnitedStates(years=year)

# Popular dates
YENNAYER = min(algeria.get_named('Amazigh New Year'))
LABOR_DAY: date = min(us.get_named("Labor Day"))
ROSH_HASHANAH = min_max(israel.get_named("Rosh Hashanah"))
MID_AUTUMN_FESTIVAL: date = min(china.get_named('Mid-Autumn Festival'))
SUKKOT = min_max(israel.get_named('Sukkot'))
GOLDEN_WEEK = Span(min(china.get_named('National Day')), days=7)
ALGERIAN_REVOLUTION_DAY = min(algeria.get_named('Revolution Day'))
ARMISTICE: date = min(france.get_named("Armistice"))
BEAUJOLAIS = third(year, NOVEMBER, THURSDAY)
PHILOSOPHY = third(year, NOVEMBER, THURSDAY)
THANKSGIVING: date = min(us.get_named("Thanksgiving"))
BLACK_FRIDAY = THANKSGIVING + timedelta(days=1)
CYBER_MONDAY = BLACK_FRIDAY + timedelta(days=3)
HANUKKAH = min_max(israel.get_named("Hanukkah"))
SANT_AMBROGIO: date = min(italy.get_named("Sant'Ambrogio"))
IMMACOLATA_CONCEZIONE: date = min(italy.get_named("Immacolata Concezione"))
CHRISTMAS: date = min(us.get_named('Christmas Day'))
SANTO_STEFANO: date = min(italy.get_named('Santo Stefano'))
NEW_YEAR: date = min(us.get_named('New Year'))

__all__ = (
    'ALGERIAN_REVOLUTION_DAY',
    'ARMISTICE',
    'BEAUJOLAIS',
    'BLACK_FRIDAY',
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
