from datetime import date, timedelta
from urllib.parse import quote_plus

from flet import Card, Colors, Column, Container, Control, CrossAxisAlignment, Divider, FontWeight, Markdown, \
    MarkdownStyleSheet, Padding, ScrollMode, Text, TextAlign, TextStyle, TextThemeStyle, component

from models import EVENTS, Event


def get_span(start: date, stop: date) -> str:
    """
    >>> get_span(date(2026, 10, 1), date(2026, 10, 7))
    'October 01 – 07'

    >>> get_span(date(2026, 9, 25), date(2026, 9, 25))
    'September 25'

    >>> get_span(date(2026, 9, 25), date(2026, 9, 27))
    'September 25 – 27'

    >>> get_span(date(2026, 9, 25), date(2026, 10, 27))
    'September 25 – October 27'
    """
    if start == stop:
        return f"{start:%B %d}"

    elif start.year == stop.year:
        if start.month == stop.month:
            return f"{start:%B %d} – {stop:%d}"
        return f"{start:%B %d} – {stop:%B %d}"

    return f"{start:%B %d, %Y} – {stop:%B %d, %Y}"


def grouped_events(today: date | None = None) -> list[tuple[str, list[Event]]]:
    """Place each upcoming or ongoing event in the earliest matching section."""
    today = today or date.today()
    next_week = today - timedelta(days=today.weekday()) + timedelta(days=7)
    week_after_next = next_week + timedelta(days=7)
    next_month = (today.replace(day=28) + timedelta(days=4)).replace(day=1)
    month_after_next = (next_month.replace(day=28) + timedelta(days=4)).replace(day=1)
    next_year = date(today.year + 1, 1, 1)

    periods = (
        ("Today", today, today + timedelta(days=1)),
        ("This week", today + timedelta(days=1), next_week),
        ("Next week", next_week, week_after_next),
        ("This month", week_after_next, next_month),
        (next_month.strftime("%B"), next_month, month_after_next),
        ("This year", month_after_next, next_year),
    )
    groups: list[tuple[str, list[Event]]] = [(name, []) for name, _, _ in periods]
    for event in EVENTS:
        start, stop = event.start.date(), event.stop.date()
        if stop < today:
            continue
        for index, (_, begin, end) in enumerate(periods):
            if begin < end and start < end and stop >= begin:
                groups[index][1].append(event)
                break
    return groups


def card(event: Event, today: date) -> Control:
    # Clip the displayed span so an ongoing event doesn't show past dates —
    # only "today" onward is shown, even if the event actually started earlier.
    start = max(event.start.date(), today)
    stop = event.stop.date()

    url = f"https://www.google.com/search?q={quote_plus(event.title)}"

    containers = [
        Markdown(
            f"[{event.title}]({url})",
            md_style_sheet=MarkdownStyleSheet(
                p_text_style=TextStyle(
                    size=22,
                    weight=FontWeight.BOLD,
                    color=Colors.WHITE,
                ),
            ),
            selectable=True,
        ),
        Markdown(
            get_span(start, stop),
            md_style_sheet=MarkdownStyleSheet(
                p_text_style=TextStyle(color=Colors.WHITE_38),
            ),
            selectable=True),
        Text(
            event.description,
            theme_style=TextThemeStyle.BODY_MEDIUM,
            color=Colors.WHITE_70,
            text_align=TextAlign.JUSTIFY,
            selectable=True,
        ),
    ]

    if event.labels - {'Pop'}:
        containers.append(
            Text(
                ", ".join(event.labels),
                selectable=True,
                color=Colors.WHITE_38,
                theme_style=TextThemeStyle.BODY_SMALL,
                font_family="Roboto",
            ),
        )

    return Card(
        content=Container(
            padding=Padding.all(20),
            content=Column(
                controls=containers,
                spacing=10,
            ),
        ),
    )


@component
def view() -> Control:
    today = date.today()
    sections = [
        (heading, events)
        for heading, events in grouped_events(today)
        if events  # Skip groups with no events entirely.
    ]
    return Container(
        expand=True,
        content=Column(
            controls=[
                control
                for index, (heading, events) in enumerate(sections)
                for control in (
                    *([Divider()] if index else []),
                    Text(heading, theme_style=TextThemeStyle.TITLE_MEDIUM, color=Colors.WHITE_38),
                    *[card(event, today) for event in events],
                )
            ],
            horizontal_alignment=CrossAxisAlignment.STRETCH,
            scroll=ScrollMode.AUTO,
            spacing=16,
        ),
    )


if __name__ == "__main__":
    import doctest

    results = doctest.testmod(verbose=True)
    if results.failed:
        raise SystemExit(1)
