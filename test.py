import flet as ft

def main(page: ft.Page):
    page.title = "Lottie + Image Demo"

    # Lottie animation
    l = ft.Image(
        src="assets\LoadingDotsBlue.gif",
        width=300,
        height=300,
        repeat=True,
    )

    # Image
    img = ft.Image(
        src="assets/a.png",  # đặt file ảnh vào thư mục assets
        width=300,
        height=300,
        fit=ft.ImageFit.CONTAIN,
    )

    # Container chứa cả 2
    c1 = ft.Row(
        controls=[
            ft.Container(content=l, bgcolor=ft.Colors.AMBER_ACCENT, padding=20),
            ft.Container(content=img, bgcolor=ft.Colors.BLUE_GREY_100, padding=20),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    page.add(c1)


ft.app(main, assets_dir="assets")
