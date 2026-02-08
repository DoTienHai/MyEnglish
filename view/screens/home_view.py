import flet as ft
from config import Screen
from view_model.home_vm import HomeViewModel
from view.components.vocabulary_table import VocabularyTable
from view.components.paragraph_table import ParagraphTable
from view.components.session_summary_chart import SessionSummaryChart
from view.components.vocabulary_summary_chart import VocabularySummaryChart
from view.components.paragraph_cards import ParagraphCard
from view.theme import *

class HomeScreen(ft.Container):
    def __init__(self, home_vm: HomeViewModel, switcher= None, alert_service=None):
        super().__init__(
            content=ft.Text("Welcome to Home Screen!", size=18),
            expand=True,
            padding=20
        )
        self.switcher = switcher
        self.alert_service = alert_service
        self.home_vm = home_vm
        self.vocabulary_table = None  # Cache component
        self.paragraph_table = None  # Cache paragraph table
        self.tab_bar = None  # Cache tab bar
        self.render()
    
    def build_session_summary_chart(self, height=300):
        data = self.home_vm.get_paragraph_progress_summary()
        completed = data['completed']
        in_progress = data['in_progress']
        open_count = data['open']
        avg_score = self.home_vm.get_avg_score()
        return SessionSummaryChart(completed, in_progress, open_count, avg_score, height)
        
    def build_vocabulary_summary_chart(self):
        vocabulary_daily_count = self.home_vm.count_vocabulary_by_date(10)
        return VocabularySummaryChart(vocabulary_daily_count)
    
    def build_paragraph_table(self):
        all_paragraphs = self.home_vm.get_all_paragraphs()
        
        # Create and cache the component on first build
        if self.paragraph_table is None:
            self.paragraph_table = ParagraphTable(
                all_paragraphs,
                on_continue_click=lambda p: self.switcher(Screen.TRANSLATE, p["id"]),
                on_edit_click=lambda payload: self._handle_edit_paragraph(payload),
                on_delete_click=lambda payload: self._handle_delete_paragraph(payload),
                alert_service=self.alert_service,
                update_callback=self.render,
            )
        else:
            # Update data in the existing component
            self.paragraph_table.paragraph_list = all_paragraphs
            self.paragraph_table.content = self.paragraph_table.build_table()
        
        return self.paragraph_table
    
    def build_vocabulary_table(self):
        all_vocabulary = self.home_vm.get_all_vocabulary()
        
        # Create and cache the component on first build
        if self.vocabulary_table is None:
            self.vocabulary_table = VocabularyTable(
                all_vocabulary,
                on_edit_click=lambda payload: self._handle_edit_vocabulary(payload),
                on_delete_click=lambda payload: self._handle_delete_vocabulary(payload),
                on_create_click=lambda payload: self._handle_create_vocabulary(payload),
                alert_service=self.alert_service,
                update_callback=self.render,
            )
        else:
            # Update data in the existing component
            self.vocabulary_table.vocabulary_list = all_vocabulary
            self.vocabulary_table.content = self.vocabulary_table.build_table()
        
        return self.vocabulary_table
        
    def build_tab_bar(self):
        if self.tab_bar is None:
            self.tab_bar = ft.Tabs(
                selected_index=0,
                animation_duration=0,
                scrollable=False,
                tabs=[
                    ft.Tab(
                        text="Paragraphs",
                        icon=ft.Icons.BOOK,
                        content=self.build_paragraph_table()
                    ),
                    ft.Tab(
                        text="Vocabulary",
                        icon=ft.Icons.STORAGE,
                        content=self.build_vocabulary_table()
                    ),
                ],
            )
        else:
            self.tab_bar.tabs[0].content = self.build_paragraph_table()
            self.tab_bar.tabs[1].content = self.build_vocabulary_table()
        return self.tab_bar

    # ----------------- Handlers for vocabulary actions -----------------
    def _handle_create_vocabulary(self, payload: dict):
        # payload expected as dict {word, part_of_speech, vi_meaning, eng_description, example}
        self.home_vm.create_vocabulary(payload)
        self.render()

    def _handle_edit_vocabulary(self, payload: dict):
        self.home_vm.update_vocabulary(payload)
        self.render()

    def _handle_delete_vocabulary(self, payload: dict):
        # perform delete via VM and refresh
        self.home_vm.delete_vocabulary(payload)
        self.render()
    
    # ----------------- Handlers for paragraph actions -----------------
    def _handle_edit_paragraph(self, payload: dict):
        """Edit paragraph title"""
        self.home_vm.update_paragraph(payload)
        self.render()

    def _handle_delete_paragraph(self, payload: dict):
        """Delete paragraph"""
        self.home_vm.delete_paragraph(payload)
        self.render()
    
    def build_home_view(self):
        chart_area_height = 300
        self.content = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Card(
                            content=ft.Container(
                                content=self.build_session_summary_chart(height=chart_area_height),
                                padding=10,
                                expand=True,
                            ),
                            expand=True,
                        ),
                        ft.Card(
                            content=ft.Container(
                                content=self.build_vocabulary_summary_chart(),
                                padding=10,
                                expand=True,
                            ),
                            expand=True
                        )
                    ],
                    expand=True,
                    height=chart_area_height
                ),
                self.build_tab_bar(),
            ]
        )

    
    def render(self):
        self.build_home_view()
        if self.page:
            self.update()