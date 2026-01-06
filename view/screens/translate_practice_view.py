import flet as ft
from view.services.Alert import AlertService
from view.components.loading import Loading
from view_model.translate_practice_vm import *

class TranslatePracticeScreen(ft.Container):
    def __init__(self, translate_practice_vm: TranslatePracticeViewModel, alert_service: AlertService):
        self.alert_service = alert_service
        self.translate_practice_vm = translate_practice_vm

        super().__init__(
            content=ft.Text("Translate Practice Screen", size=18),
            expand=True,
            padding=10
        )
        self.translate_practice_vm.step.subscribe(self.render)
        self.render(TRANSLATE_PRACTICE_STEP.STEP_1_INPUT_TEXT)
        

    def build_step_1(self):
        title_text_field = ft.TextField(
                    label="Enter title of session",
                    multiline=False,
                    height=50,
                    width=200,
                )
        ref_source_text_field = ft.TextField(
                    label="Enter reference of session",
                    multiline=False,
                    expand=True
                )
        input_text_text_field = ft.TextField(
                    label="Enter text to translate",
                    multiline=True,
                    expand=True,
                )
        self.content = ft.Column(
            controls=[
                ft.Row(
                  controls=[
                      ft.Text("Title: ", size=18, weight=ft.FontWeight.BOLD,),
                      title_text_field,
                      ft.Text("Reference: ", size=18, weight=ft.FontWeight.BOLD,),
                      ref_source_text_field,
                  ],
                  height=70,
                ),
                ft.Divider(),
                ft.Text("Input Text: ", size=18, weight=ft.FontWeight.BOLD,),
                input_text_text_field,
                ft.ElevatedButton(
                    "Start translate",
                    on_click=lambda e: self.translate_practice_vm.handle_step_1(
                        title_text_field.value,
                        ref_source_text_field.value,                        
                        input_text_text_field.value,
                    ),
                ),
            ],
            spacing=10
        )
        
    def build_step_2(self):
        translation_text_fields = []
        new_words_fields = []
        list_view = ft.ListView(controls=[], spacing=10, padding=10, auto_scroll=False, expand=True)
        sentences = self.translate_practice_vm.input_sentences
        for sentence in sentences:
            sentence_input = ft.Text(f"{sentences.index(sentence) + 1}. {sentence}", size=16, weight="bold", expand=True)
            text_field = ft.TextField(label="Enter translation", expand=True)
            new_words_field = ft.TextField(label="New words (optional), split by comma", expand=True)
            list_view.controls.append(ft.Row(
                controls=[
                    sentence_input,
                    text_field,
                    new_words_field,],
                    spacing=20))
            list_view.controls.append(ft.Divider())

            translation_text_fields.append(text_field)
            new_words_fields.append(new_words_field)

        button_bar = ft.Row(
            controls=[
                ft.ElevatedButton("Submit Translations", on_click=lambda e : self.translate_practice_vm.handle_step_2(
                    sentence_translations=[tf.value for tf in translation_text_fields],
                    new_words_list=[nwf.value for nwf in new_words_fields])),
            ],
            alignment=ft.MainAxisAlignment.END,
            spacing=10,
        )
        
        self.content = ft.Column(
            controls=[
                list_view,
                button_bar,
            ],
            spacing=10,
        )

    def build_step_3(self):
        list_view = ft.ListView(controls=[], spacing=10, padding=10, auto_scroll=False, expand=True) 
        for index in range(len(self.translate_practice_vm.input_sentences)):
            list_view.controls.append(ft.Column(
                controls=[
                    ft.Text(f"Source sentence: {self.translate_practice_vm.input_sentences[index]}", size=16, weight="bold"),
                    ft.Text(f"Your Translation: {self.translate_practice_vm.sentence_translations[index]}", size=16),
                    ft.Text(f"Correct Translation: {self.translate_practice_vm.sentences_translated_by_translator[index]}", size=16, color=ft.Colors.GREEN),
                    ft.Text(f"Score: {self.translate_practice_vm.scores[index]}.", size=16, color=ft.Colors.GREEN),
                    ft.Divider(),
                ],
                spacing=5,
            ))

        button_complete = ft.Row(
            controls=[            
                ft.ElevatedButton("Completed!", on_click=lambda e: self.translate_practice_vm.handle_step_3()),
            ],
            alignment=ft.MainAxisAlignment.END,
            spacing=10,
        )
        self.content = ft.Column(
            controls=[
                list_view,
                button_complete,
            ],
            spacing=10,
        )
    
    def build_loading(self):
        self.content = Loading("Processing, please wait...")
    
    def render(self, step: TRANSLATE_PRACTICE_STEP):
        if step == TRANSLATE_PRACTICE_STEP.STEP_1_INPUT_TEXT:
            self.build_step_1()
        elif step == TRANSLATE_PRACTICE_STEP.STEP_2_TRANSLATE_TEXT:
            self.build_step_2()
        elif step == TRANSLATE_PRACTICE_STEP.STEP_3_REVIEW_TRANSLATION:
            self.build_step_3()
        elif step == TRANSLATE_PRACTICE_STEP.LOADING:
            self.build_loading()
        if self.page:
            self.update()