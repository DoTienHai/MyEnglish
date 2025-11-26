import flet as ft

class Loading(ft.Container):
    def __init__(self, message="Loading..."):
        super().__init__()

        # Hiệu ứng fade
        self.opacity = 1
        self.animate_opacity = 300
        self.expand = True
        self.bgcolor = "#F0F0F0"

        # Nội dung hiển thị
        self.content = ft.Column(
            controls=[
                ft.Image("assets\\Loading.gif", height=160, width=160, repeat=True),
                ft.Text(message, color=ft.Colors.BLACK, size=18),
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

if __name__ == "__main__":
    ft.app(target=loading_overlay_test)
    