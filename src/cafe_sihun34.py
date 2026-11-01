import flet as ft
from cafe_status import AppState, CAFE_COLOR


@ft.component
def Sihun34(state: AppState):
    return ft.Container(
        expand=True,
        alignment=ft.Alignment.CENTER,
        bgcolor="#F7F7F2",
        padding=32,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
            controls=[
                ft.Icon(ft.Icons.COFFEE, size=88, color=CAFE_COLOR),
                ft.Text(
                    "Welcome to Sihun34 Cafe",
                    size=32,
                    weight=ft.FontWeight.BOLD,
                    color="#333333",
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text("원하는 메뉴를 주문하고 별을 모아보세요."),
                ft.Button(
                    "로그인 / 회원가입",
                    on_click=lambda e: e.page.navigate("/login"),
                    bgcolor=CAFE_COLOR,
                    color="#222222",
                ),
                ft.Button(
                    "메뉴 보기",
                    on_click=lambda e: e.page.navigate("/home"),
                ),
            ],
        ),
    )