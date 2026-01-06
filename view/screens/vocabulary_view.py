import flet as ft
from model.vocabulary import *
from view_model.vocabulary_vm import *
from view.components.flash_card import *


class VocabularyScreen(ft.Container):
    def __init__(self, vocabulary_vm: VocabularyViewModel):
        self.vocabulary_vm = vocabulary_vm
        super().__init__(
            content=ft.Text("Vocabulary Screen", size=18),
            expand=True,
            padding=10
        )
        self.build_flash_card(self.vocabulary_vm.random_vocabulary())
        self.render()
    
    def build_flash_card(self, vocabulary: Vocabulary) -> FlashCard:
        self.content = ft.Column(
            controls=[
                ft.Text(vocabulary.word, size=18, weight=ft.FontWeight.BOLD,),
                ft.Divider(),
                ft.Text("Example:", size=16, weight=ft.FontWeight.BOLD,),
                ft.Text(vocabulary.example, size=16, italic=True,),
                ft.ElevatedButton("Next", on_click=self.next),
            ]
        )
    def next(self, e):
        self.build_flash_card(self.vocabulary_vm.random_vocabulary())
        self.render()
    
    def render(self):
        if self.page:
            self.update()
            


    