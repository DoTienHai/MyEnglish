from config import *
import flet as ft
from view.theme import *


class NavBar(ft.Container):
    def __init__(self,switcher):
        width = 200
        buttons = []
        for screen in Screen:
            buttons.append(
                ft.ElevatedButton(screen.value, on_click=lambda e, s=screen: switcher(s), width=width)
            )

        super().__init__(
            width=width,
            bgcolor=NAV_BG,
            padding=ft.padding.all(10),
            content=ft.Column(
                controls=buttons,
                spacing=10,
                expand=True,
            ),
        )

    def highlight_active(self, current_screen):
        for btn in self.content.controls[:]:
            btn.style = ft.ButtonStyle(bgcolor=None)
            if btn.text == current_screen.value:
                btn.style = ft.ButtonStyle(bgcolor=ACCENT)
        self.update()