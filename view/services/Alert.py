import flet as ft
class AlertService:
    def __init__(self, page: ft.Page):
        self._page = page

    def open(self, alert: ft.AlertDialog):
        self._page.open(alert)
    def close(self, alert: ft.AlertDialog):
        self._page.close(alert)