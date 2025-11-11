import flet as ft
from ui.app_layout import main_layout
from core.sqlite3 import DatabaseManager

if __name__ == "__main__":
    DatabaseManager(db_path="data/app_data.db")
    ft.app(target=main_layout)
