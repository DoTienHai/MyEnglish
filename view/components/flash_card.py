import flet as ft
from view.theme import *

class FlashCard(ft.Container):
    def __init__(self, word, example_sentence):
        super().__init__(
            content=ft.Column(
                controls=[
                    ft.Text(example_sentence, size=16, italic=True, color=random_text_color()),
                    ft.Text(word, size=24, weight="bold", color=random_text_color()),
                ],
            ),
            expand=True,
            padding=10,
            bgcolor=random_card_color(),
        )

    