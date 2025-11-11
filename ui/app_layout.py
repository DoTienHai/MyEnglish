from config import *
from ui.widgets.header  import *
from ui.widgets.navbar  import *
from ui.widgets.footer  import *
from ui.widgets.translate_practice import *
from ui.widgets.home import *
import flet as ft

class AppLayout:
    def __init__(self, page: ft.Page):
        self.page = page

        self.current_screen = Screen.HOME.value
        self.home_screen = HomeScreen()
        self.translate_practice_screen = TranslatePracticeScreen(self.page)
        self.settings_screen = ft.Text("⚙️ Settings Screen", size=18)

        self.header =  Header(self.page)
        self.nav_bar = NavBar(self.switch_screen)
        self.body_container = ft.Container(
            content=self.home_screen, expand=True, padding=10
        )
        self.footer = Footer()
        # ---------------- MAIN LAYOUT ----------------
        self.layout = ft.Column(
            expand=True,
            controls=[
                self.header,
                ft.Row(
                    expand=True,
                    controls=[
                        self.nav_bar,
                        self.body_container,
                    ],
                ),
                self.footer,
            ],
        )

    # ---------------- SWITCH SCREEN ----------------
    def switch_screen(self, name: str):
        self.current_screen = name
        if name == Screen.HOME.value:
            self.body_container.content = self.home_screen
        elif name == Screen.TRANSLATE.value:
            self.body_container.content = self.translate_practice_screen
        elif name == Screen.SETTINGS.value:
            self.body_container.content = self.settings_screen
        else:
            self.body_container.content = ft.Text("404 - Not Found")

        self.nav_bar.highlight_active(self.current_screen)
        self.body_container.update()


    # ---------------- BUILD ----------------
    def build(self):
        return self.layout


def main_layout(page: ft.Page):
    page.title = APP_NAME
    app = AppLayout(page)
    page.add(app.build())

if __name__ == "__main__":
    ft.app(target=main_layout)
