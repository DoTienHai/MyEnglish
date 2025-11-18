import flet as ft

class LoadingOverlay(ft.Container):
    def __init__(self, message="Processing, please wait..."):
        super().__init__()
        self.message = message

    def build(self):
        # Stack: nền mờ + content
        return ft.Stack(
            controls=[
                ft.Container(
                    bgcolor=ft.Colors.BLACK26,  # nền mờ
                    expand=True,
                    visible=True,
                ),
                ft.Column(
                    controls=[
                        ft.ProgressRing(),
                        ft.Text(self.message, color=ft.Colors.WHITE)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True,
                    visible=self.visible,
                )
            ]
        )
