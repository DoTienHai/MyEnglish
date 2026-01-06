import flet as ft

class FlashCard(ft.Container):
    def __init__(self, word, example_sentence):
        super().__init__(
            content=ft.Column(
                controls=[
                    ft.Text(example_sentence, size=16, italic=True),
                    ft.Text(word, size=24, weight="bold"),
                ],
            ),
            expand=True,
            padding=10
        )

    