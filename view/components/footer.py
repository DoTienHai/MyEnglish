from config import *
import flet as ft
from view.theme import *

class Footer(ft.Container):
    def __init__(self):
        super().__init__(
            content=ft.Text("© 2025 My English App", size=12, color=FOOTER_TEXT),
            bgcolor=FOOTER_BG,
            height=40,
            alignment=ft.alignment.center,
        )