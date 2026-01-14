import flet as ft
from model.vocabulary import Vocabulary
from view_model.vocabulary_vm import VocabularyViewModel, VOCABULARY_STEP
from view.components.flash_card import FlashCard
from view.theme import *


class VocabularyScreen(ft.Container):
    def __init__(self, vocabulary_vm: VocabularyViewModel):
        self.vocabulary_vm = vocabulary_vm
        self.vocabulary_vm.step.subscribe(self.render)
        super().__init__(
            content=ft.Text("Vocabulary Screen", size=18),
            expand=True,
            padding=10
        )
        self.render(VOCABULARY_STEP.QUESTION)
    
    def build_flash_card(self):
        parts = self.vocabulary_vm.current_vocabulary.example.split(self.vocabulary_vm.current_vocabulary.word)
        
        self.content = ft.Column(
            controls=[
                ft.Text(self.vocabulary_vm.current_vocabulary.word, size=18, weight=ft.FontWeight.BOLD,),
                ft.Divider(),
                ft.Text("Example:", size=16, weight=ft.FontWeight.BOLD,),
                ft.Text(spans=[
                    ft.TextSpan(parts[0]),
                        ft.TextSpan(self.vocabulary_vm.current_vocabulary.word, style=ft.TextStyle(weight=ft.FontWeight.BOLD, color=SUCCESS)),
                    ft.TextSpan(parts[1]),
                    ], size=16, italic=True),
                ft.Column(
                    controls=[
                        ft.ElevatedButton(
                            meaning,
                            on_click=lambda e, m=meaning: self.vocabulary_vm.check_answer(m)
                        )
                        for meaning in self.vocabulary_vm.current_answers
                    ]
                ),
            ]
        )
    
    def build_answer_result(self):
        parts = self.vocabulary_vm.current_vocabulary.example.split(self.vocabulary_vm.current_vocabulary.word)
        meanings = self.vocabulary_vm.current_answers
        results = []
        for meaning in meanings:
            if meaning == self.vocabulary_vm.current_vocabulary.meaning:
                results.append(ft.Text(meaning + " ✔", size=16, weight=ft.FontWeight.BOLD, color=SUCCESS))
            else:
                results.append(ft.Text(meaning + " ✘", size=16, weight=ft.FontWeight.BOLD, color=ERROR))
        self.content = ft.Column(
            controls=[
                ft.Text(self.vocabulary_vm.current_vocabulary.word, size=18, weight=ft.FontWeight.BOLD,),
                ft.Divider(),
                ft.Text("Example:", size=16, weight=ft.FontWeight.BOLD,),
                ft.Text(spans=[
                    ft.TextSpan(parts[0]),
                    ft.TextSpan(self.vocabulary_vm.current_vocabulary.word, style=ft.TextStyle(weight=ft.FontWeight.BOLD, color=SUCCESS)),
                    ft.TextSpan(parts[1]),
                    ], size=16, italic=True),
                ft.Column(
                    controls=results
                ),
                ft.ElevatedButton("Next", on_click=lambda e: self.vocabulary_vm.next()),
            ]
        )
     
    def render(self, step:VOCABULARY_STEP):
        if step == VOCABULARY_STEP.QUESTION:
            self.build_flash_card()
        elif step == VOCABULARY_STEP.ANSWER_RESULT:
            self.build_answer_result()
        if self.page:
            self.update()
            


    