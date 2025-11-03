import flet as ft
import re

from core.translator import TranslationService

class TranslatePracticeScreen(ft.Container):
    def __init__(self, page: ft.Page):
        self.page = page
        self.current_step = 1
        self.input_text = ""
        self.sentences_fields = []
        self.translation_text_fields = []
        self.new_words_fields = []
        self.content_default = ft.Column( # default content same step 1
            controls=[
                ft.TextField(
                    label="Enter text to translate",
                    multiline=True,
                    expand=True,
                ),
                ft.ElevatedButton(
                    "Start translate",
                    on_click=self.start_translate,
                ),
            ],
            spacing=10
        )
        self.content = self.content_default
        super().__init__(
            content=self.content,
            expand=False,
            padding=10
        )

    def update_content(self, content=None, component_update=False, page_update=False):
        if content:
            self.content = content
        if component_update:
            self.update()
        if page_update:
            self.page.update()

    # ---------------- STEP 1 ----------------
    def build_step_1(self):
        step_1_content = self.content_default
        self.update_content(content=step_1_content, component_update=True, page_update=False)
    def start_translate(self, event):
        self.input_text = self.content.controls[0].value
        if not self.input_text.strip():
            alert = ft.AlertDialog(
                title=ft.Text("Input Error"),
                content=ft.Text("Please enter some text to translate."),
                actions=[ft.TextButton("OK", on_click=lambda e: self.page.close(alert))],
            )
            self.page.open(alert)
        else:
            self.current_step = 2
            self.build_step_2()

    # ---------------- STEP 2 ----------------
    def build_step_2(self):
        sentences = re.split(r'(?<=[.!?])\s+', self.input_text.strip())

        list_view = ft.ListView(controls=[], spacing=10, padding=10, auto_scroll=False, expand=True)
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
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

            self.sentences_fields.append(text_input) 
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
        translations = []
        for index in range(len(self.sentences_fields)):
            translations.append((self.sentences_fields[index].value, self.translation_text_fields[index].value))

        self.current_step = 3
        self.build_step_3()

    # ---------------- STEP 3 ---------------
    def build_step_3(self):
        list_view = ft.ListView(controls=[], spacing=10, padding=10, auto_scroll=False, expand=True)

        process_bar = ft.Column(controls=[
            ft.Text(value="Translating!", color=ft.Colors.GREEN_300, size=24),
            ft.ProgressBar(bar_height=200, width=500, bgcolor="#eeeeee", color=ft.Colors.GREEN_300, ),],
            spacing=20, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        for index in range(len(self.sentences_fields)):
            process_bar.controls[0].value = f"Translating: {(index+1)}/{len(self.sentences_fields)}!"
            process_bar.controls[1].value = (index)/len(self.sentences_fields)
            self.update_content(content=process_bar,component_update=True, page_update=False)

            user_translation = self.translation_text_fields[index].value
            correct_translation = TranslationService().translate_eng_to_vn(self.sentences_fields[index].value)
            list_view.controls.append(ft.Column(
                controls=[
                    self.sentences_fields[index],
                    ft.Text(f"Your Translation: {user_translation}", size=16),
                    ft.Text(f"Correct Translation: {correct_translation}", size=16, color=ft.Colors.GREEN),
                    ft.Divider(),
                ],
                spacing=5,
            ))

            process_bar.controls[0].value = f"Translating: {(index+1)}/{len(self.sentences_fields)}!"
            process_bar.controls[1].value = (index+1)/len(self.sentences_fields)
            self.update_content(content=process_bar,component_update=True, page_update=False)


        
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
        self.current_step = 1
        self.input_text = ""
        self.sentences_fields = []
        self.translation_text_fields = []
        self.build_step_1()