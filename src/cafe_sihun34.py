import flet as ft
from cafe_status import AppState


@ft.component
def Sihun34(state:AppState):
    return ft.Stack(
        controls=[
            ft.Image("10637.png", expand=1),
            ft.Text("Welcome to Sihun34 Cafe!", size=50, color="#FFFFFF", text_align=ft.TextAlign.CENTER),
        ]
    )
