import flet as ft

from views.almanac import view


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    page.title = "Almanac"
    page.render(view)


ft.run(main)
