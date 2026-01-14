from config import *
from typing import Callable
import flet as ft
from view.theme import *

class Header(ft.Container):
    def __init__(self, on_refresh: Callable[[], None]):
        self.on_refresh = on_refresh
        super().__init__(
            content=ft.Row(
                controls=[
                    ft.Text(APP_NAME, size=20, weight="bold", color=HEADER_TEXT),
                    ft.IconButton(ft.Icons.REFRESH, on_click=self.refresh, icon_size=20, icon_color=HEADER_TEXT),

                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                spacing=10,
            ),
            bgcolor=HEADER_BG,
            height=50,
            padding=ft.padding.all(10),
        )

    def refresh(self, event):
        self.on_refresh()
