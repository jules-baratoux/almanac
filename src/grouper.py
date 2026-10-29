from collections import defaultdict
from datetime import date
from itertools import dropwhile
from typing import Iterable

from dates import day_after_tomorrow, month_after_next, next_month, next_week, next_year, today, tomorrow, \
    week_after_next

period_and_stop = {
    # Period title: stop date
    'Today': tomorrow,
    'Tomorrow': day_after_tomorrow,
    'This week': next_week,
    'Next week': week_after_next,
    'This month': next_month,
    f'{next_month:%B}': month_after_next,
    f'{today:%Y}': next_year,
}


def group[Event](events: Iterable[Event]):
    events = dropwhile(lambda event: event.start < today, events)
    tree: dict[str, dict[date, list[Event]]] = defaultdict(lambda: defaultdict(list))
    for event in events:
        try:
            period = next(period for period, stop in period_and_stop.items() if event.start < stop)
        except StopIteration:
            break
        start = event.start
        tree[period][start].append(event)

    for period, days in tree.items():
        yield period, days.items()
