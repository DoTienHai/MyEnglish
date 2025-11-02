import flet as ft
import re

from core.translator import TranslationService

class TranslatePracticeScreen(ft.Container):
    def __init__(self, page: ft.Page):
        self.page = page
        self.current_step = 1
        self.input_text = ""
        self.sentences = []
        self.translation_text_fields = []
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
            padding=20
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
            text_field = ft.TextField(label="Enter translation", expand=True)
            list_view.controls.append(ft.Row(
                controls=[
                    ft.Text(f"{sentence}", size=16, weight="bold", expand=True),
                    text_field,],
                    spacing=20))
            list_view.controls.append(ft.Divider())

            self.sentences.append(sentence) 
            self.translation_text_fields.append(text_field)
        
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
        for index in range(len(self.sentences)):
            translations.append((self.sentences[index], self.translation_text_fields[index].value))
        # Here you can handle the translations as needed
        print("Submitted Translations:", translations)
        self.current_step = 3
        self.build_step_3()

    # ---------------- STEP 3 ---------------
    def build_step_3(self):
        list_view = ft.ListView(controls=[], spacing=10, padding=10, auto_scroll=False, expand=True)
        for index in range(len(self.sentences)):
            original = self.sentences[index]
            user_translation = self.translation_text_fields[index].value
            correct_translation = TranslationService().translate_eng_to_vn(original)
            list_view.controls.append(ft.Column(
                controls=[
                    ft.Text(f"Original: {original}", size=16, weight="bold"),
                    ft.Text(f"Your Translation: {user_translation}", size=16),
                    ft.Text(f"Correct Translation: {correct_translation}", size=16, color=ft.Colors.GREEN),
                    ft.Divider(),
                ],
                spacing=5,
            ))
        
        button_complete = ft.Row(
            controls=[            
                ft.ElevatedButton("Completed!", on_click=lambda e: self.build_step_1()),
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

        # Những cuộc khám phá muộn nhất đến từ các nhà nghiên cứu từ đại học Geogetown và hội đông nghiên cứu Mỹ.