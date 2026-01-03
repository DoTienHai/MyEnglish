import flet as ft

class VocabularyScreen(ft.Container):
    def __init__(self):
        super().__init__(
            content=ft.Text("Vocabulary Screen", size=18),
            expand=True,
            padding=10
        )

