import flet as ft
import threading
from view.services.Alert import AlertService
from view.components.Loading import *
# from controller.translate_practice_controller import TranslatePracticeController
from view_model.translate_practice_vm import TranslatePracticeViewModel

class TranslatePracticeScreen(ft.Container):
    def __init__(self, translate_practice_vm: TranslatePracticeViewModel, alert_service: AlertService):
        self.translate_practice_vm = translate_practice_vm
        self.alert_service = alert_service
        
        # self.controller = TranslatePracticeController()
        
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
        
        self.session_id = None
        self.translation_text_fields = []
        self.new_words_fields = []
        self.content = None
        
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
                self.content.clean()
            self.content = content
        if component_update:
            self.update()


    # ---------------- STEP 1: INPUT TEXT ----------------
    def build_step_1(self):
        self.title.value = ""
        self.ref_source.value = ""
        self.input_text.value = ""
        
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
                actions=[ft.TextButton("OK", on_click=lambda e: self.alert_service.close(alert))],
            )
            self.alert_service.open(alert)
        else:
            loading = Loading(message="Preparing, please wait...")
            self.update_content(content=loading, component_update=True, page_update=False)

            def run_processing():
                self.session_id = self.controller.process_input(self.title.value, self.ref_source.value, self.input_text.value)
                self.build_step_2()

            threading.Thread(target=run_processing).start()

    # ---------------- STEP 2: INPUT TRANSLATIONS ----------------
    def build_step_2(self):
        sentences = self.controller.get_sentences()

        list_view = ft.ListView(controls=[], spacing=10, padding=10, auto_scroll=False, expand=True)
        for sentence in sentences:
            text_input = ft.Text(f"{sentence['sentence_index']}. {sentence['source_sentence']}", size=16, weight="bold", expand=True)
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
                ft.ElevatedButton("Back", on_click=self.build_step_1),
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
        no_translated = []
        for i in range(self.controller.number_of_sentences()):
            tf = self.translation_text_fields[i]
            if not tf.value.strip():
                no_translated.append(str(i+1))
            text_value_translations.append(tf.value)
        new_words_value_translations = [nf.value for nf in self.new_words_fields]
        
        if len(no_translated) > 0:
            alert = ft.AlertDialog(
                title=ft.Text("Warning"),
                content=ft.Column(
                    controls=[  ft.Text(f"You lack translations for the following sentences:", text_align=ft.TextAlign.CENTER, expand=True),
                                ft.Text(f"{",".join(no_translated)}", text_align=ft.TextAlign.CENTER, expand=True),
                                ft.Text("Do you want to submit?", text_align=ft.TextAlign.CENTER, expand=True),],
                    spacing=10, height=150, width=300, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                actions=[ft.TextButton("Cancel", on_click=lambda e: self.alert_service.close(alert)),
                         ft.TextButton("Submit", on_click=lambda e: (self.alert_service.close(alert), self.process_translations(text_value_translations, new_words_value_translations)))],
            )
            self.alert_service.open(alert)
        else:
            self.process_translations(text_value_translations, new_words_value_translations)
    
    def process_translations(self, text_value_translations, new_words_value_translations):    
        loading = Loading(message="Processing, please wait...")
        self.update_content(content=loading, component_update=True, page_update=False)
        def run_processing():
            self.controller.process_translations(text_value_translations)
            self.controller.process_new_words(new_words_value_translations)

            self.build_step_3()

        threading.Thread(target=run_processing).start()


    # ---------------- STEP 3: VIEW RESULTS ---------------
    def build_step_3(self):
        sentences = self.controller.get_sentences()
        user_translations = self.controller.get_user_translations()
        correct_translations = self.controller.get_cloud_translations()
        scores = self.controller.get_scores()
        
        list_view = ft.ListView(controls=[], spacing=10, padding=10, auto_scroll=False, expand=True) 
        for index in range(self.controller.number_of_sentences()):
            list_view.controls.append(ft.Column(
                controls=[
                    ft.Text(f"Source sentence: {sentences[index]}", size=16, weight="bold"),
                    ft.Text(f"Your Translation: {user_translations[index]}", size=16),
                    ft.Text(f"Correct Translation: {correct_translations[index]}", size=16, color=ft.Colors.GREEN),
                    ft.Text(f"Score: {scores[index]}/10.", size=16, color=ft.Colors.GREEN),
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
        self.content.controls.clear()
        self.translation_text_fields.clear()
        self.new_words_fields.clear()

        self.build_step_1()
