from flet import Page, SafeArea, ThemeMode, run

from views.almanac import view


def main(page: Page):
    page.theme_mode = ThemeMode.DARK
    page.title = "Almanac"
    page.render(lambda: SafeArea(expand=True, content=view()))


run(main)
