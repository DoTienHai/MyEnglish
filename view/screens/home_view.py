import flet as ft
import math
from config import Screen
from view_model.home_vm import HomeViewModel
from view.theme import *

class HomeScreen(ft.Container):
    def __init__(self, home_vm: HomeViewModel, switcher= None):
        super().__init__(
            content=ft.Text("🏡 Welcome to Home Screen!", size=18),
            expand=True,
            padding=20
        )
        self.switcher = switcher
        self.home_vm = home_vm
        self.render()
    
    def build_session_summary_chart(self, height=300):
        def legend_item(color, label, value):
            return ft.Row(
                spacing=6,
                controls=[
                    ft.Container(
                        width=12,
                        height=12,
                        bgcolor=color,
                        border_radius=2,
                    ),
                    ft.Text(f"{label}: {value}", size=12, color=HEADER_TEXT),
                ],
            )
        radius = (height-50)/4
        space_radius = radius*2/3
        completed, in_progress, open = self.home_vm.get_session_progress_summary()
        return ft.Column(
            controls=[
                ft.Text("Session summary", size=18, weight="bold", color=PRIMARY_DARK, text_align=ft.TextAlign.CENTER),
                ft.Row(
                    controls=[
                        ft.PieChart(
                            sections=[
                                ft.PieChartSection(
                                    value=completed,
                                    title=f"{completed}",
                                    color=PRIMARY,
                                    radius=radius,
                                    title_style=ft.TextStyle(size=12, color=OPAQUE_WHITE),
                                ),
                                ft.PieChartSection(
                                    value=in_progress,
                                    title=f"{in_progress}",
                                    color=HOT_IN_PROGRESS,
                                    radius=radius,
                                    title_style=ft.TextStyle(size=12, color=OPAQUE_WHITE),
                                ),
                                ft.PieChartSection(
                                    value=open,
                                    title=f"{open}",
                                    color=HOT_OPEN,
                                    radius=radius,
                                    title_style=ft.TextStyle(size=12, color=OPAQUE_WHITE),
                                ),
                            ],
                            center_space_radius=space_radius,
                            expand=True
                        ),
                        ft.Column(
                            spacing=8,
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.Text(f"Avg score: {self.home_vm.get_avg_score()}", size=16, weight="bold", color=PRIMARY_DARK, text_align=ft.TextAlign.CENTER),
                                ft.Divider(),
                                legend_item(PRIMARY, "Completed", completed),
                                legend_item(HOT_IN_PROGRESS, "In progress", in_progress),
                                legend_item(HOT_OPEN, "Open", open),
                            ],
                        ),
                    ],
                    height=height*0.8,
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        
    def build_vocabulary_summary_chart(self):
        vocabulary_daily_count = self.home_vm.count_vocabulary_by_date(10)
        dates = list(vocabulary_daily_count.keys())
        counts = list(vocabulary_daily_count.values())

        bar_groups = []
        for i, count in enumerate(counts):
            bar_groups.append(
                        ft.BarChartGroup(
                    x=i,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=count,
                            width=18,
                            border_radius=4,
                            color=PRIMARY
                        )
                    ],
                )
            )

        max_value = max(counts) if counts else 0
        label_interval = max(math.ceil(max_value / 10), 1)

        return ft.Column(
            controls=[
                ft.Text("Vocabulary summary", size=18, weight="bold", color=PRIMARY_DARK, text_align=ft.TextAlign.CENTER),
                ft.BarChart(
                    bar_groups=bar_groups,
                    left_axis=ft.ChartAxis(
                        title=ft.Text("Number of vocabulary", size=12, weight=ft.FontWeight.BOLD),
                        title_size=25,
                        labels_size=40,
                        labels_interval=label_interval
                    ),
                    bottom_axis=ft.ChartAxis(
                        title=ft.Text("Date", size=12, weight=ft.FontWeight.BOLD),
                        labels=[
                            ft.ChartAxisLabel(
                                value=i,
                                label=ft.Text(dates[i][5:], size=10),  # MM-DD
                            )
                            for i in range(len(dates))
                        ],
                    ),
                    horizontal_grid_lines=ft.ChartGridLines(
                        interval=label_interval,
                        color=BORDER,
                        width=1,
                        dash_pattern=[3, 3]
                    ),
                    max_y=round(math.ceil(max_value/label_interval)*label_interval*1.2, 0),
                    min_y=0,
                    interactive=True,
                    expand=True,
                    border=ft.border.all(1, MUTED),
                ),
            ],
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
        )
        
    def build_session_cards(self):
        session_list = self.home_vm.get_not_done_sessions()
        cards_list = []
        row_card = ft.Row(controls=[])
        for session in session_list:
            # map session status to pie-chart colors
            # score == 0 => open, score > 0 => in-progress
            if session.get("score", 0) == 0:
                card_color = HOT_OPEN
            else:
                card_color = HOT_IN_PROGRESS
            row_card.controls.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text(session["title"], size=16, weight="bold", color=TEXT_COLOR, text_align=ft.TextAlign.CENTER),
                                ft.Text(f"Score: {session["score"]}", size=14, weight="bold", color=TEXT_COLOR, text_align=ft.TextAlign.CENTER),
                                ft.Text(f"Created at: {session["created_at"]}", size=14, weight="bold", color=TEXT_COLOR, text_align=ft.TextAlign.CENTER),
                                ft.ElevatedButton("Continue Session",on_click=lambda e, s=session: self.switcher(Screen.TRANSLATE, s["id"])),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        padding=10,
                    ),
                    color=card_color,
                    expand=True
                )
            )
            if len(row_card.controls) == 3:
                cards_list.append(row_card)
                row_card = ft.Row(controls=[])
        cards_list.append(row_card)
        return cards_list
        
    def build_home_view(self):
        chart_area_height = 300
        session_summary_chart = self.build_session_summary_chart(height=chart_area_height)
        vocabulary_summary_chart = self.build_vocabulary_summary_chart()
        self.content = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Card(
                            content=ft.Container(
                                content=session_summary_chart,
                                padding=10,
                                width=chart_area_height*4/3,
                                height=chart_area_height
                            ),
                        ),
                        ft.Card(
                            content=ft.Container(
                                content=vocabulary_summary_chart,
                                padding=10,
                            ),
                            expand=True
                        )
                    ],
                    height=chart_area_height
                ),
                ft.ListView(
                    controls=self.build_session_cards(),
                    expand=True
                )
            ]
        )
    
    def render(self):
        self.build_home_view()
        if self.page:
            self.update()