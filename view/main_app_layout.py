from config import *
from view.services.Alert import *
from service.paragraph_service import ParagraphService
from service.sentence_service import SentenceService
from service.translation_service import TranslationService
from service.scoring_service import ScoringService
from service.vocabulary_service import VocabularyService
from view_model.home_vm import *
from view_model.translate_practice_vm import *
from view_model.vocabulary_vm import *
from view.components.header import *
from view.components.navbar import *
from view.components.footer import *
from view.theme import *
from view.screens.translate_practice_view import *
from view.screens.vocabulary_view import *
from view.screens.home_view import *
import flet as ft


class MainAppLayout:
    def __init__(self, page: ft.Page):
        self.page = page
        self.current_screen = Screen.HOME

        self.alert_service = AlertService(page)
        self.paragraph_service = ParagraphService()
        self.sentence_service = SentenceService()
        self.vocabulary_service = VocabularyService()
        self.translator = TranslationService()
        self.score_service = ScoringService()

        self.home_vm = HomeViewModel(paragraph_service=self.paragraph_service,
                                     sentence_service=self.sentence_service,
                                     vocabulary_service=self.vocabulary_service,
                                     )
        self.translate_practice_vm = TranslatePracticeViewModel(paragraph_service=self.paragraph_service,
                                                                sentence_service=self.sentence_service,
                                                                vocabulary_service=self.vocabulary_service,
                                                                translator=self.translator,
                                                                score_service=self.score_service)
        self.vocabulary_vm = VocabularyViewModel(
            vocabulary_service=self.vocabulary_service)

        self.home_screen = HomeScreen(
            home_vm=self.home_vm, switcher=self.switch_screen, alert_service=self.alert_service)
        self.translate_practice_screen = TranslatePracticeScreen(translate_practice_vm=self.translate_practice_vm,
                                                                 alert_service=self.alert_service,)
        self.vocabulary_screen = VocabularyScreen(
            vocabulary_vm=self.vocabulary_vm)

        self.header = Header(on_refresh=self.refresh)
        self.nav_bar = NavBar(switcher=self.switch_screen)
        self.body_container = ft.Container(
            content=self.home_screen, expand=True, padding=10
        )
        # Wrap body_container with scroll to handle overflow
        self.scrollable_body = ft.ListView(
            controls=[self.body_container],
            expand=True,
            spacing=0,
            padding=0
        )
        self.footer = Footer()

        # ---------------- MAIN LAYOUT ----------------
        self.layout = ft.Column(
            expand=True,
            controls=[
                self.header,
                ft.Row(
                    expand=True,
                    controls=[
                        self.nav_bar,
                        self.scrollable_body,
                    ],
                ),
                self.footer,
            ],
        )

    # ---------------- SWITCH SCREEN ----------------
    def switch_screen(self, screen: Screen, paragraph_id: int = None):
        self.current_screen = screen
        if screen == Screen.HOME:
            self.home_screen.render()
            self.body_container.content = self.home_screen
        elif screen == Screen.TRANSLATE:
            self.body_container.content = self.translate_practice_screen
            if paragraph_id is not None:
                self.translate_practice_vm.load_paragraph(paragraph_id)
                self.translate_practice_vm.switch_step(
                    TRANSLATE_PRACTICE_STEP.STEP_2_TRANSLATE_TEXT)
        elif screen == Screen.VOCABULARY:
            # Refresh vocabulary data before switching (to get newly added words)
            self.vocabulary_vm.refresh()
            self.body_container.content = self.vocabulary_screen
        else:
            self.body_container.content = ft.Text("404 - Not Found")

        self.nav_bar.highlight_active(self.current_screen)
        self.scrollable_body.update()
    # ---------------- REFRESH ----------------

    def refresh(self):
        self.switch_screen(self.current_screen)

    # ---------------- BUILD ----------------
    def build(self):
        return self.layout


def main_layout(page: ft.Page):
    page.title = APP_NAME
    # apply milky/opaque white theme
    page.bgcolor = BG_COLOR
    app = MainAppLayout(page)
    page.add(app.build())


if __name__ == "__main__":
    ft.app(target=main_layout)
