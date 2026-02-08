import flet as ft
import math
from view.theme import *


class SessionSummaryChart(ft.Column):
    """Hiển thị pie chart tóm tắt session (Completed/In-Progress/Open)"""
    
    def __init__(self, completed, in_progress, open_count, avg_score, height=300):
        self.completed = completed
        self.in_progress = in_progress
        self.open_count = open_count
        self.avg_score = avg_score
        
        super().__init__(
            controls=self.build_chart(height),
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
            height=height,
        )
    
    def build_chart(self, height):
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
        space_radius = radius*1/2
        
        return [
            ft.Text("Paragraph summary", size=18, weight="bold", color=PRIMARY_DARK, text_align=ft.TextAlign.CENTER),
            ft.Row(
                controls=[
                    ft.PieChart(
                        sections=[
                            ft.PieChartSection(
                                value=self.completed,
                                title=f"Completed\n{self.completed}",
                                color=PRIMARY,
                                radius=radius,
                                title_style=ft.TextStyle(size=12, color=OPAQUE_WHITE),
                            ),
                            ft.PieChartSection(
                                value=self.in_progress,
                                title=f"In progress\n{self.in_progress}",
                                color=HOT_IN_PROGRESS,
                                radius=radius,
                                title_style=ft.TextStyle(size=12, color=OPAQUE_WHITE),
                            ),
                            ft.PieChartSection(
                                value=self.open_count,
                                title=f"Open\n{self.open_count}",
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
                            ft.Text(f"Avg score: {self.avg_score}", size=16, weight="bold", color=PRIMARY_DARK, text_align=ft.TextAlign.CENTER),
                            ft.Divider(),
                            legend_item(PRIMARY, "Completed", self.completed),
                            legend_item(HOT_IN_PROGRESS, "In progress", self.in_progress),
                            legend_item(HOT_OPEN, "Open", self.open_count),
                        ],
                    ),
                ],
                height=height*0.8,
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            )
        ]
