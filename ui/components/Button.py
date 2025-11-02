import flet as ft

import flet as ft

class Button(ft.Container):
    def __init__(
        self,
        text: str,
        on_click=None,
        color: str = ft.Colors.BLUE,
        text_color: str = ft.Colors.WHITE,
        icon: str | None = None,
        width: int = 200,
        height: int = 45,
        border_radius: int = 10,
    ):
        super().__init__()
        self.content = ft.Row(
            [
                ft.Icon(icon, color=text_color) if icon else None,
                ft.Text(text, color=text_color, size=16, weight=ft.FontWeight.W_600),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
        )

        self.bgcolor = color
        self.width = width
        self.height = height
        self.border_radius = border_radius
        self.alignment = ft.alignment.center
        self.on_click = on_click
        self.animate = ft.Animation(300, "easeOut")

        # Hiệu ứng hover
        self.on_hover = self._on_hover

    def _on_hover(self, e: ft.HoverEvent):
        """Đổi màu nhẹ khi rê chuột vào"""
        self.bgcolor = (
            ft.Colors.with_opacity(0.8, self.bgcolor)
            if e.data == "true"
            else ft.Colors.with_opacity(1, self.bgcolor)
        )
        self.update()

if __name__ == "__main__":
    def main(page: ft.Page):
        def on_button_click(e):
            print("Button clicked!")

        btn = Button(
            text="Click Me",
            on_click=on_button_click,
            icon=ft.Icons.THUMB_UP,
            color=ft.Colors.GREEN,
        )

        page.add(btn)

    ft.app(target=main) 