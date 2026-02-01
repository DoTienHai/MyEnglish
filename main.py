import flet as ft
from view.main_app_layout import *
from repositories.db_connect import DBConnect
from repositories.db_init import DBInit

def main(): 
    db = DBConnect(db_path="data.db")
    DBInit(db).create_tables()
    ft.app(target=main_layout)

if __name__ == "__main__":
    main()
