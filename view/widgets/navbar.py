from config import *
import flet as ft


class NavBar(ft.Container):
    def __init__(self,switch_screen_callback):
        width = 200
        buttons = []
        for screen in Screen:
            buttons.append(
                ft.ElevatedButton(screen.value, on_click=lambda e, s=screen: switch_screen_callback(s.value), width=width)
            )

        super().__init__(
            width=width,
            bgcolor=ft.Colors.BLUE_GREY_50,
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
            if btn.text == current_screen:
                btn.style = ft.ButtonStyle(bgcolor=ft.Colors.BLUE_100)
        self.update()