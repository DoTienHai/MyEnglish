from config import *
import flet as ft

class Header(ft.Container):
    def __init__(self, page: ft.Page):
        self.page = page
        super().__init__(
            content=ft.Row(
                controls=[
                    ft.Text(APP_NAME, size=20, weight="bold", color="white"),
                    ft.IconButton(ft.Icons.REFRESH, on_click=self.refresh,icon_size=20, icon_color="white"),

                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                spacing=10,
            ),
            bgcolor=ft.Colors.BLUE_GREY_900,
            height=50,
            padding=ft.padding.all(10),
        )

    def refresh(self, event):
        self.page.update()
