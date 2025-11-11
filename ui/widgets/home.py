import flet as ft

class HomeScreen(ft.Container):
    def __init__(self):
        super().__init__(
            content=ft.Text("🏡 Welcome to Home Screen!", size=18),
            expand=True,
            padding=20
        )