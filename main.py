import flet as ft
from view.app_layout import main_layout
from model.db_manager import DatabaseManager
from view.components.Loading import *

if __name__ == "__main__":
    DatabaseManager(db_path="./app_data.db")
    ft.app(target=main_layout)
    
