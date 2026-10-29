from dataclasses import dataclass
from typing import Callable, Optional

import flet
from flet import (
    Alignment,
    Animation, AnimationCurve, AnimationValue,
    BoxConstraints,
    ButtonStyle,
    ColorValue,
    Column,
    ControlEventHandler,
    Event,
    FloatingActionButton,
    Icon, IconButton, IconData, Icons,
    Offset, Page,
    RoundedRectangleBorder,
    Stack,
    TextButton,
    ThemeMode,
    run,
)


@dataclass
class SearchBar(flet.SearchBar):
    on_build: Optional[Callable[[], None]] = None

    async def change(self, value: str):
        if value == self.value:
            return

        self.value = value
        await self._trigger_event("change", value)

    def build(self):
        if self.on_build is not None:
            self.on_build()


class FloatingAction:

    async def on_floating_action_button_click(self, event: Event[FloatingActionButton]):
        self.style(expanded=True)

        await self.bar.focus()

    async def on_collapse_button_click(self, event: Event[IconButton]):
        self.style(expanded=False)

        # Close virtual keyboard
        await self.blur_sink.focus()

    async def on_clear_button_click(self, event: Event[IconButton]):
        self.value = ""

    def __init__(self,
                 expanded: bool = False,  # Starts expanded as a bar or collapsed as a FAB ?
                 bar_hint_text: str = "Filter",
                 animate: Optional[AnimationValue] = Animation(350, AnimationCurve.EASE_IN_OUT),
                 icon: IconData = Icons.FILTER_LIST,
                 bgcolor: Optional[ColorValue] = None,
                 bar_bgcolor: Optional[ColorValue] = None,
                 on_change: Optional[ControlEventHandler[SearchBar]] = None,
                 icon_color: Optional[ColorValue] = None,
                 ):

        self.button = FloatingActionButton(
            key="floating_action_button",
            icon=icon,
            foreground_color=icon_color,
            bgcolor=bgcolor,
            animate_opacity=animate,
            on_click=self.on_floating_action_button_click,
        )

        collapse_button = IconButton(
            icon=Icon(icon, color=icon_color),
            on_click=self.on_collapse_button_click,
        )

        clear_button: IconButton = IconButton(
            icon=Icon(Icons.CLEAR, color=icon_color),
            on_click=self.on_clear_button_click,
        )

        self.blur_sink: TextButton = TextButton(
            width=0,
            height=0,
            opacity=0,
            style=ButtonStyle(padding=0),
        )

        self.bar = SearchBar(
            bar_hint_text=bar_hint_text,
            bar_elevation=0,
            bar_bgcolor=bar_bgcolor or bgcolor,
            bar_leading=collapse_button,
            bar_trailing=[clear_button],
            bar_shape=RoundedRectangleBorder(radius=0),
            bar_size_constraints=BoxConstraints(),
            animate_opacity=animate,
            animate_offset=animate,
            on_change=on_change,
            on_build=self.build,
        )

        self.expanded: bool = NotImplemented  # Force style application during initialization
        self.style(expanded)

    def style(self, expanded: bool):
        if expanded is not self.expanded:
            self.expanded = expanded

            if expanded:
                # Expanded as a search bar
                self.bar.disabled = False
                self.bar.opacity = 1
                self.bar.offset = Offset(0, 0)
                self.button.opacity = 0

            else:
                # Collapsed as a floating action button
                self.bar.disabled = True
                self.bar.opacity = 0
                self.bar.offset = Offset(0, 2)
                self.button.opacity = 1

    @property
    def value(self) -> str:
        return self.bar.value

    @value.setter
    def value(self, value: str):
        if value != self.value:
            # Bar value has to be changed
            self.bar.page.run_task(self.bar.change, value)

            # If value is not empty but the bar is not expanded:
            if value and not self.expanded:
                # The bar has to appear and the FAB to disappear
                self.style(expanded=True)
                self.button.update()

            self.bar.update()

    def update(self):
        self.bar.update()
        self.button.update()

    def build(self):
        self.page.add(self.blur_sink)

    @property
    def page(self):
        return self.bar.page


async def example(page: Page):
    from faker import Faker

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

    def update_event_list_view(query: str):
        print(f"update_event_list_view: {query}")

    async def on_label_click(event: flet.Event[TextButton]):
        value = event.control.content
        assert isinstance(value, str) and value
        filter_bar.value = value

    filter_bar = FloatingAction(
        animate=Animation(350, AnimationCurve.EASE_IN_OUT),
        icon=Icons.FILTER_LIST,
        icon_color=flet.Colors.with_opacity(.5, flet.Colors.WHITE),
        bgcolor="#353638",  # {SearchBar, Searchbar Icons, FAB}.bgcolor: page.bgcolor + 10% white
        expanded=False,  # Starts expanded as a bar or collapsed as a FAB ?
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
                        filter_bar.bar,
                    ],
                )
            ]
        )
    )

    page.floating_action_button = filter_bar.button
    page.add(
        TextButton(
            content=Faker().country(),
            on_click=on_label_click,
        )
    )


if __name__ == "__main__":
    run(example)

__all__ = "FloatingAction",
