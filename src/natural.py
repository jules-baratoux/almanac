import datetime
from typing import Literal


def date_from(today: datetime.date):
    tomorrow = today + datetime.timedelta(days=1)
    yesterday = today + datetime.timedelta(days=-1)
    next_fortnight = today + datetime.timedelta(days=14)
    last_fortnight = today + datetime.timedelta(days=-14)
    next_semester = today + datetime.timedelta(days=180)
    last_semester = today + datetime.timedelta(days=-180)

    def date(day: datetime.date):
        if day == today:
            return "today"
        elif day == tomorrow:
            return "tomorrow"
        elif day == yesterday:
            return "yesterday"
        elif abs((day - today).days) < 4:
            return day.strftime("%A")
        elif last_fortnight < day < next_fortnight:
            return day.strftime("%A %d")
        elif last_semester < day < next_semester:
            return day.strftime("%B %d")
        else:
            return day.strftime("%B %d, %Y")

    return date


def date(value: datetime.date) -> Literal["today", "tomorrow", "yesterday"] | str:
    # October 2026
    #
    #  Mo  Tu  We  Th  Fr  Sa  Su
    # ---------------------------
    #  ²⁸  ²⁹  ³⁰   1   2   3   4
    #   5   6   7   8   9 [10] 11
    #  12  13  14  15  16  17  18
    #  19  20  21  22  23  24  25
    #  26  27  28  29  30  31  ¹
    #  ²   ³   ⁴   ⁵   ⁶   ⁷   ⁸
    """
    Natural-language of a date.

    >>> date = date_from(today=datetime.date(2026, 10, 10))

    >>> date(datetime.date(2026, 10, 10))
    'today'

    >>> date(datetime.date(2026, 10, 11))
    'tomorrow'

    >>> date(datetime.date(2026, 10, 9))
    'yesterday'

    >>> date(datetime.date(2026, 10, 12))
    'Monday'

    >>> date(datetime.date(2026, 10, 17))
    'Saturday 17'

    >>> date(datetime.date(2026, 11, 2))
    'November 02'
    """


globals()[date.__name__] = date_from(today=datetime.date.today())
