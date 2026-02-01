import flet as ft
from view.theme import *


class ParagraphCard(ft.Card):
    """Hiển thị 1 paragraph card"""
    
    def __init__(self, paragraph, on_continue_click=None):
        self.paragraph = paragraph
        self.on_continue_click = on_continue_click
        
        super().__init__(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(paragraph["title"], size=16, weight="bold", color=TEXT_COLOR, text_align=ft.TextAlign.CENTER),
                        ft.Text(f"Score: {paragraph['score']}", size=14, weight="bold", color=TEXT_COLOR, text_align=ft.TextAlign.CENTER),
                        ft.Text(f"Created at: {paragraph['created_at']}", size=14, weight="bold", color=TEXT_COLOR, text_align=ft.TextAlign.CENTER),
                        ft.ElevatedButton(
                            "Continue Paragraph",
                            on_click=lambda e: self.on_continue()
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                padding=10,
            ),
            color=self.determine_card_color(),
            expand=True
        )
    
    def determine_card_color(self):
        if self.paragraph.get("score", 0) == 0:
            return HOT_OPEN
        else:
            return HOT_IN_PROGRESS
    
    def on_continue(self):
        if self.on_continue_click:
            self.on_continue_click(self.paragraph)
        print(f"Continue paragraph: {self.paragraph['title']}")
