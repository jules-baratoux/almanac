import flet as ft

from views.almanac import view


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    page.title = "Almanac"
    page.render(lambda: ft.SafeArea(expand=True, content=view()))


ft.run(main)
