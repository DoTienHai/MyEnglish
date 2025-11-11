import flet as ft
import re

from controller.translate_practice_controller import TranslatePracticeController

class TranslatePracticeScreen(ft.Container):
    def __init__(self, page: ft.Page):
        self.page = page
        
        self.controller = TranslatePracticeController()
        self.title = ft.TextField(
                    label="Enter title of session",
                    multiline=False,
                    height=50,
                    width=200,
                )
        self.ref_source = ft.TextField(
                    label="Enter reference of session",
                    multiline=False,
                    expand=True
                )
        self.input_text = ft.TextField(
                    label="Enter text to translate",
                    multiline=True,
                    expand=True,
                )
        
        self.translation_text_fields = []
        self.new_words_fields = []
        self.content = None
        
        self.number_of_sentences = 0
        self.session_id = None
        self.sentence_id = []
        self.score = []
        
        super().__init__(
            content=ft.Column( # default content same step 1
            controls=[
                ft.Row(
                  controls=[
                      ft.Text("Title: ", size=18, weight=ft.FontWeight.BOLD,),
                      self.title,
                      ft.Text("Reference: ", size=18, weight=ft.FontWeight.BOLD,),
                      self.ref_source,
                  ],
                  height=70,
                ),
                ft.Divider(),
                ft.Text("Input Text: ", size=18, weight=ft.FontWeight.BOLD,),
                self.input_text,
                ft.ElevatedButton(
                    "Start translate",
                    on_click=self.start_translate,
                ),
            ],
            spacing=10
        ),
            expand=False,
            padding=10
        )

    def update_content(self, content=None, component_update=False, page_update=False, clear_content=False):
        if content:
            if self.content and clear_content:
                self.content.controls.clear()
            self.content = content
        if component_update:
            self.update()
        if page_update:
            self.page.update()

    # ---------------- STEP 1: INPUT TEXT ----------------
    def build_step_1(self):
        self.title.value = ""
        self.ref_source.value = ""
        self.input_text.value = ""
        self.number_of_sentences = 0
        
        step_1_content = ft.Column(
            controls=[
                ft.Row(
                  controls=[
                      ft.Text("Title: ", size=18, weight=ft.FontWeight.BOLD,),
                      self.title,
                      ft.Text("Reference: ", size=18, weight=ft.FontWeight.BOLD,),
                      self.ref_source,
                  ],
                  height=70,
                ),
                ft.Divider(),
                ft.Text("Input Text: ", size=18, weight=ft.FontWeight.BOLD,),
                self.input_text,
                ft.ElevatedButton(
                    "Start translate",
                    on_click=self.start_translate,
                ),
            ],
            spacing=10
        )
        self.update_content(content=step_1_content, component_update=True, page_update=False)
    def start_translate(self, event):
        if not self.input_text.value.strip():
            alert = ft.AlertDialog(
                title=ft.Text("Input Error"),
                content=ft.Text("Please enter some text to translate."),
                actions=[ft.TextButton("OK", on_click=lambda e: self.page.close(alert))],
            )
            self.page.open(alert)
        else:
            self.controller.process_input(self.title.value, self.ref_source.value, self.input_text.value)
            self.build_step_2()

    # ---------------- STEP 2: INPUT TRANSLATIONS ----------------
    def build_step_2(self):
        sentences = self.controller.get_sentences()

        list_view = ft.ListView(controls=[], spacing=10, padding=10, auto_scroll=False, expand=True)
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            self.number_of_sentences += 1
            text_input = ft.Text(sentence, size=16, weight="bold", expand=True)
            text_field = ft.TextField(label="Enter translation", expand=True)
            new_words_field = ft.TextField(label="New words (optional), split by comma", expand=True)
            list_view.controls.append(ft.Row(
                controls=[
                    text_input,
                    text_field,
                    new_words_field,],
                    spacing=20))
            list_view.controls.append(ft.Divider())

            self.translation_text_fields.append(text_field)
            self.new_words_fields.append(new_words_field)

        button_bar = ft.Row(
            controls=[
                ft.ElevatedButton("Submit Translations", on_click=self.submit_translations),
                ft.ElevatedButton("Back", on_click=lambda e: self.build_step_1()),
            ],
            alignment=ft.MainAxisAlignment.END,
            spacing=10,
        )
        
        step_2_content = ft.Column(
            controls=[
                list_view,
                button_bar,
            ],
            spacing=10,
        )
        self.update_content(content=step_2_content, component_update=True, page_update=False)

    def submit_translations(self, event):
        text_value_translations = []
        for text_field in self.translation_text_fields:
            text_value_translations.append(text_field.value)
            
        new_words_value_translations = []
        for new_words_field in self.new_words_fields:
            new_words_value_translations.append(new_words_field.value)

        self.score = self.controller.process_translations(text_value_translations, new_words_value_translations)
        self.build_step_3()

    # ---------------- STEP 3: VIEW RESULTS ---------------
    def build_step_3(self):
        list_view = ft.ListView(controls=[], spacing=10, padding=10, auto_scroll=False, expand=True) 
        for index in range(self.number_of_sentences):
            user_translation = self.translation_text_fields[index].value
            correct_translation = self.controller.get_cloud_translations()[index]
            list_view.controls.append(ft.Column(
                controls=[
                    ft.Text(f"Source sentence: {self.controller.get_sentences()[index]}", size=16, weight="bold"),
                    ft.Text(f"Your Translation: {user_translation}", size=16),
                    ft.Text(f"Correct Translation: {correct_translation}", size=16, color=ft.Colors.GREEN),
                    ft.Text(f"Score: {self.score[index]}/10.", size=16, color=ft.Colors.GREEN),
                    ft.Divider(),
                ],
                spacing=5,
            ))

        button_complete = ft.Row(
            controls=[            
                ft.ElevatedButton("Completed!", on_click=lambda e: self.reset()),
            ],
            alignment=ft.MainAxisAlignment.END,
            spacing=10,
        )
        step_3_content = ft.Column(
            controls=[
                list_view,
                button_complete,
            ],
            spacing=10,
        )
        self.content = step_3_content
        self.update_content(content=step_3_content,component_update=True, page_update=False)

    def reset(self):
        # Xóa control cũ để ngắt tham chiếu
        self.content.controls.clear()
        self.translation_text_fields.clear()
        self.new_words_fields.clear()

        # Reset dữ liệu
        self.title.value = ""
        self.ref_source.value = ""
        self.input_text.value = ""

        # Build lại UI gốc
        self.build_step_1()
