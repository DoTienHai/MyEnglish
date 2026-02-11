import flet as ft
from view.theme import *

class Loading(ft.Container):
    def __init__(self, message="Loading..."):
        super().__init__()

        # Fade effect
        self.opacity = 1
        self.animate_opacity = 300
        self.expand = True
        self.bgcolor = BG_COLOR

        # Display content
        self.content = ft.Column(
            controls=[
                ft.Image("assets\\Loading.gif", repeat=True),
                ft.Text(message, color=TEXT_COLOR, size=18),
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def show(self):
        self.opacity = 1
        self.update()

    def hide(self):
        self.opacity = 0
        self.update()
        
def loading_overlay_test(page: ft.Page):
    page.title = "Loading Overlay Preview"
    # page.window_width = 400
    # page.window_height = 500
    page.padding = 0
    overlay = Loading("Loading...")
    overlay.opacity = 1
    page.add(overlay)

if __name__ == "__main__":  # pragma: no cover
    ft.app(target=loading_overlay_test)
    