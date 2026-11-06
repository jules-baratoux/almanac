import inspect

import natural
from events import EVENTS


def test_natural_number_with_events():
    signature = inspect.signature(natural.number)
    thresholds = signature.parameters['thresholds'].default
    units = [unit for _, unit in thresholds]
    for event in EVENTS:
        formatted = natural.number(event.people)
        assert '+' not in formatted, f"Undesired '+' when formatting {event.people}"
        assert any(unit in formatted for unit in units)
