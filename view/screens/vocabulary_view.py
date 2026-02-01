import flet as ft
from view_model.vocabulary_vm import VocabularyViewModel, VOCABULARY_STEP, NUMBER_OF_ANSWER_CHOICES, NUMBER_OF_MINIMUM_VOCABULARY
from view.theme import *


class VocabularyScreen(ft.Container):
    def __init__(self, vocabulary_vm: VocabularyViewModel):
        self.vocabulary_vm = vocabulary_vm
        super().__init__(
            content=ft.Text("Vocabulary Screen", size=18),
            expand=True,
            padding=10
        )
        # Subscribe to step changes from ViewModel
        self.vocabulary_vm.step.subscribe(self.render)
        # Render with current state from ViewModel
        self.render(self.vocabulary_vm.step.value)
    
    def build_flash_card(self):
        parts = self.vocabulary_vm.current_vocabulary.example.split(self.vocabulary_vm.current_vocabulary.word)
        
        self.content = ft.Column(
            controls=[
                ft.Text(self.vocabulary_vm.current_vocabulary.word, size=18, weight=ft.FontWeight.BOLD,),
                ft.Text(f"[{self.vocabulary_vm.current_vocabulary.part_of_speech}]", size=14, color=MUTED),
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
            if meaning == self.vocabulary_vm.current_vocabulary.vi_meaning:
                results.append(
                    ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.CHECK_CIRCLE, color=SUCCESS, size=20),
                            ft.Text(meaning, size=16, weight=ft.FontWeight.BOLD, color=SUCCESS),
                        ],
                        spacing=10
                    )
                )
            else:
                results.append(
                    ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.CANCEL, color=ERROR, size=20),
                            ft.Text(meaning, size=16, weight=ft.FontWeight.BOLD, color=ERROR),
                        ],
                        spacing=10
                    )
                )
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
                ft.ElevatedButton("Next", on_click=lambda e: self.vocabulary_vm.refresh()),
            ]
        )
        
    def build_not_enough_vocabulary(self):
        self.content = ft.Column(
            controls=[
                ft.Text("Not enough vocabulary to practice.", size=18, weight=ft.FontWeight.BOLD, color=ERROR),
                ft.Text("Please add more vocabulary entries to continue practicing.", size=16),
                ft.Text(f"You currently have {self.vocabulary_vm.get_vocabulary_count()} entries. You need at least {NUMBER_OF_MINIMUM_VOCABULARY} entries.", size=16),
            ]
        )
        
    def render(self, step:VOCABULARY_STEP):
        if step == VOCABULARY_STEP.QUESTION:
            self.build_flash_card()
        elif step == VOCABULARY_STEP.ANSWER_RESULT:
            self.build_answer_result()
        elif step == VOCABULARY_STEP.NOT_ENOUGH_VOCABULARY:
            self.build_not_enough_vocabulary()
        if self.page:
            self.update()
            


    