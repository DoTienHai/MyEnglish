import flet as ft
import math
from view.theme import *


class VocabularySummaryChart(ft.Column):
    """Hiển thị bar chart tóm tắt vocabulary học được theo ngày"""
    
    def __init__(self, vocabulary_daily_count):
        self.vocabulary_daily_count = vocabulary_daily_count
        
        super().__init__(
            controls=self.build_chart(),
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    
    def build_chart(self):
        dates = list(self.vocabulary_daily_count.keys())
        counts = list(self.vocabulary_daily_count.values())

        bar_groups = []
        for i, count in enumerate(counts):
            bar_groups.append(
                ft.BarChartGroup(
                    x=i,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=int(count),
                            width=18,
                            border_radius=4,
                            color=PRIMARY
                        )
                    ],
                )
            )

        max_value = int(max(counts)) if counts else 0
        label_interval = int(max(math.ceil(max_value / 10), 1))

        return [
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
                max_y=int(round(math.ceil(max_value/label_interval)*label_interval*1.2)),
                min_y=0,
                interactive=True,
                expand=True,
                border=ft.border.all(1, MUTED),
            ),
        ]
