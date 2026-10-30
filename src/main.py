import re
from datetime import date, timedelta
from enum import IntEnum
from typing import Optional, Sequence

import flet
from flet import (
    Alignment,
    BoxFit, ColorValue, Column,
    Container,
    ControlEventHandler,
    CrossAxisAlignment,
    DecorationImage, FontWeight,
    GestureDetector,
    Icon, Icons, ListView,
    MainAxisAlignment,
    Margin,
    MouseCursor,
    Padding,
    Page,
    Row,
    Stack,
    Text, ThemeMode,
    run,
)

import grouper
import natural
from events import EVENTS, Event, Labels
from floating_action import FloatingAction


class FontSize(IntEnum):
    SMALL = 12
    DEFAULT = 14
    MEDIUM = 20


class Colors:
    BLACK_75P = flet.Colors.with_opacity(.75, flet.Colors.BLACK)
    BLOSSOM = "#64394f"
    BLUE = "#a8c8fb"
    CLAY = "#49443a"
    CORAL = "#632632"
    DUSK = "#463360"
    FOG = "#386377"
    MINT = "#314d3b"
    PEACH = "#60311e"
    SAGE = "#2e625d"
    SAND = "#744a00"
    STORM = "#2f4255"
    TRANSPARENT = flet.Colors.with_opacity(0, flet.Colors.WHITE)
    WHITE_10P = flet.Colors.with_opacity(.1, flet.Colors.WHITE)
    WHITE_50P = flet.Colors.with_opacity(.5, flet.Colors.WHITE)
    WHITE_75P = flet.Colors.with_opacity(.75, flet.Colors.WHITE)
    WHITE_90P = flet.Colors.with_opacity(.9, flet.Colors.WHITE)

    # Assign colors to Labels
    ALGERIA = MINT
    CHINA = CORAL
    FAMILY = CLAY
    FRANCE = FOG
    ISLAM = MINT
    ISRAEL = DUSK
    ITALY = SAGE
    MEXICO = SAND
    POP = BLOSSOM
    USA = STORM


async def main(page: Page):
    page.title = "Almanac"
    page.bgcolor = "#1e1f21"
    page.theme_mode = ThemeMode.DARK
    page.theme = flet.Theme(
        scrollbar_theme=flet.ScrollbarTheme(
            thumb_visibility=False,
            thickness=4,
        )
    )
    page.padding = 0
    page.spacing = 0

    unfiltered_event_list = EVENTS
    displayed_event_list = unfiltered_event_list

    def periode_view(title: str, days, on_label_tap: Optional[ControlEventHandler] = None):
        event_card_padding = Padding.all(20)

        day_row_horizontal_margin = 24
        date_column_width = 28 + day_row_horizontal_margin * 2

        def day_row(weekday: str, num: str, events):
            date_view = Container(
                width=date_column_width,
                padding=Padding.only(top=2),
                content=Column(
                    spacing=0,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    controls=[
                        Text(weekday, size=FontSize.SMALL, weight=FontWeight.W_600, color=Colors.WHITE_50P),
                        Text(num, size=FontSize.MEDIUM, weight=FontWeight.W_700, color=Colors.WHITE_75P),
                    ]
                )
            )

            return Row(
                spacing=0,
                vertical_alignment=CrossAxisAlignment.START,
                controls=[
                    date_view,
                    Column(
                        expand=True,
                        spacing=15,
                        controls=[
                            event_card(event) for event in events
                        ]
                    )
                ]
            )

        def get_event_date(start: date, end: date) -> str:
            if (end - start) > timedelta(days=1):
                span = f"{natural.date(start)} – {natural.date(end)}"
            else:
                span = natural.date(start)
            return span

        def get_event_color(labels: Sequence[Labels]):
            try:
                label = labels[0]
            except IndexError:
                return Colors.WHITE_10P
            else:
                return getattr(Colors, label.name)

        def event_card(event: Event):

            title: str = event.title
            span = get_event_date(event.start, event.end)
            description: str = event.description
            color: ColorValue = get_event_color(event.labels)
            people: str = natural.number(event.people)

            def label_card(value: str):
                async def on_tap(e: flet.Event[GestureDetector]):
                    await on_label_tap(flet.ControlEvent(e.name, data=text.value, control=text))

                text = Text(value=value, size=FontSize.SMALL, color=Colors.WHITE_50P)
                return GestureDetector(
                    mouse_cursor=MouseCursor.CLICK,
                    on_tap=on_tap,
                    content=Container(
                        bgcolor=Colors.WHITE_10P,
                        border_radius=8,
                        padding=Padding.symmetric(vertical=4, horizontal=10),
                        content=text,
                    ),
                )

            return Container(
                image=DecorationImage(event.image, opacity=.1, fit=BoxFit.COVER) if event.image else None,
                bgcolor=color,
                expand=True,
                border_radius=30,
                padding=event_card_padding,
                margin=Margin.only(right=day_row_horizontal_margin),
                content=Column(
                    spacing=4,
                    controls=[
                        Column(
                            spacing=10,
                            controls=[
                                Text(title, size=FontSize.MEDIUM, weight=FontWeight.W_600, color=Colors.WHITE_90P),
                                Text(span.title(), size=FontSize.SMALL, color=Colors.WHITE_50P),
                                Text(description, size=FontSize.DEFAULT, color=Colors.WHITE_75P),
                            ]
                        ),
                        Row(
                            alignment=MainAxisAlignment.END,
                            controls=[
                                Row(
                                    controls=[
                                        Icon(
                                            Icons.PEOPLE_ALT, color=Colors.WHITE_10P, size=14
                                        ),
                                        Text(
                                            value=people,
                                            color=Colors.WHITE_50P,
                                            size=FontSize.SMALL,
                                            weight=FontWeight.W_600,
                                        ),
                                    ],
                                    spacing=6,
                                    vertical_alignment=CrossAxisAlignment.CENTER,
                                ),
                                *(label_card(label.value) for label in event.labels)
                            ]
                        )
                    ]
                )
            )

        return Column(
            spacing=20,
            controls=[

                # Title
                Container(
                    margin=Margin.only(
                        left=date_column_width + event_card_padding.left,
                        top=24,
                    ),
                    content=Text(title, size=FontSize.SMALL, color=Colors.WHITE_50P),
                ),

                # Days
                *(
                    day_row(_date.strftime("%a"), _date.strftime("%d"), events)
                    for _date, events in days
                )
            ]
        )

    async def on_label_tap(event: flet.ControlEvent):
        value = event.data
        assert isinstance(value, str) and value
        floating_action.value = value

    def update_event_list_view(query: str = ""):

        nonlocal displayed_event_list

        if query:
            search = re.compile(query, re.IGNORECASE).search
            displayed_event_list = filter(lambda event: search(repr(tuple(event))), unfiltered_event_list)
        else:
            displayed_event_list = unfiltered_event_list

        event_list_view.controls = [
            periode_view(title, days, on_label_tap)
            for title, days in grouper.group(displayed_event_list)
        ]

    event_list_view = ListView(expand=True)
    update_event_list_view()

    floating_action = FloatingAction(
        expanded=False,
        icon_color=Colors.WHITE_50P,
        bgcolor="#222426",
        bar_bgcolor="#131313",
        on_change=lambda event: update_event_list_view(event.data),
    )

    page.overlay.append(
        Column(
            expand=True,
            controls=[
                Stack(
                    expand=True,
                    alignment=Alignment.BOTTOM_CENTER,
                    controls=[
                        floating_action.bar,
                    ],
                )
            ]
        )
    )

    page.floating_action_button = floating_action.button
    page.add(event_list_view)


if __name__ == "__main__":
    run(main)
