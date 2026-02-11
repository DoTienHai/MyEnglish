import flet as ft
from config import DATABASE_PATH
from view.main_app_layout import *
from repositories.db_connect import DBConnect
from repositories.db_init import DBInit


def main():
    """Application entry point"""
    db = DBConnect(db_path=DATABASE_PATH)
    DBInit(db).create_tables()
    ft.app(target=main_layout)


if __name__ == "__main__":  # pragma: no cover
    main()
