from config import *
import flet as ft

class Footer(ft.Container):
    def __init__(self):
        super().__init__(
            content=ft.Text("© 2025 My English App", size=12, color="white"),
            bgcolor=ft.Colors.BLUE_GREY_900,
            height=40,
            alignment=ft.alignment.center,
        )