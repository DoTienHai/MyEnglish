from config import *
from view.services.Alert  import *
from service.session_service import SessionService
from service.sentence_service import SentenceService
from service.translation_service import TranslationService
from service.scoring_service import ScoringService
from service.vocabulary_service import VocabularyService
from view_model.translate_practice_vm import *
from view_model.vocabulary_vm import *
from view.components.header  import *
from view.components.navbar  import *
from view.components.footer  import *
from view.screens.translate_practice_view import *
from view.screens.vocabulary_view import *
from view.screens.home_view import *
import flet as ft

class MainAppLayout:
    def __init__(self, page: ft.Page):
        self.page = page
        self.current_screen = Screen.HOME

        self.alert_service = AlertService(page)
        self.session_service = SessionService()
        self.sentence_service = SentenceService()
        self.vocabulary_service = VocabularyService()
        self.translator = TranslationService()
        self.score_service = ScoringService()
        
        self.translate_practice_vm = TranslatePracticeViewModel(session_service=self.session_service,
                                                                 sentence_service=self.sentence_service,
                                                                 vocabulary_service=self.vocabulary_service,
                                                                 translator=self.translator,
                                                                 score_service=self.score_service)
        self.vocabulary_vm = VocabularyViewModel(vocabulary_service=self.vocabulary_service)

        self.home_screen = HomeScreen()
        self.translate_practice_screen = TranslatePracticeScreen(translate_practice_vm=self.translate_practice_vm, 
                                                                 alert_service=self.alert_service,)
        self.vocabulary_screen = VocabularyScreen(vocabulary_vm=self.vocabulary_vm)

        self.header =  Header(on_refresh=self.refresh)
        self.nav_bar = NavBar(switcher=self.switch_screen)
        self.body_container = ft.Container(
            content=self.home_screen, expand=True, padding=10
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
                        self.body_container,
                    ],
                ),
                self.footer,
            ],
        )

    # ---------------- SWITCH SCREEN ----------------
    def switch_screen(self, screen: Screen):
        self.current_screen = screen
        if screen == Screen.HOME:
            self.body_container.content = self.home_screen
        elif screen == Screen.TRANSLATE:
            self.body_container.content = self.translate_practice_screen
        elif screen == Screen.VOCABULARY:
            self.body_container.content = self.vocabulary_screen
        else:
            self.body_container.content = ft.Text("404 - Not Found")

        self.nav_bar.highlight_active(self.current_screen)
        self.body_container.update()
    # ---------------- REFRESH ----------------
    def refresh(self):
        self.switch_screen(self.current_screen)

    # ---------------- BUILD ----------------
    def build(self):
        return self.layout


def main_layout(page: ft.Page):
    page.title = APP_NAME
    app = MainAppLayout(page)
    page.add(app.build())

if __name__ == "__main__":
    ft.app(target=main_layout)
