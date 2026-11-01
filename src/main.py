import flet as ft
from cafe_status import AppState, CAFE_COLOR
from cafe_sihun34 import Sihun34
from cafe_pay import Pay
from cafe_cart import Cart
from cafe_home import Home
from cafe_menu import Menu
from cafe_login import LogIn
from cafe_profile import Profile

global_state = AppState()


@ft.component
def App(state: AppState):
    return ft.SafeArea(
        content=ft.Column(
            controls=[
                ft.Router(
                    [
                        ft.Route(index=True, component=lambda: Sihun34(state=state)),
                        ft.Route(path="cart", component=lambda: Cart(state=state)),
                        ft.Route(path="pay", component=lambda: Pay(state=state)),
                        ft.Route(path="home", component=lambda: Home(state=state)),
                        ft.Route(path="menu/:product", component=lambda: Menu(state=state)),
                        ft.Route(
                            path="login",
                            component=lambda: LogIn(state=state, page=ft.context.page),
                        ),
                        ft.Route(
                            path="profile",
                            component=lambda: Profile(state=state, page=ft.context.page),
                        ),
                    ]
                ),
            ],
            expand=True,
        ),
        expand=True,
    )


@ft.component
def MainApp():
    return App(state=global_state)


def main(page: ft.Page):
    global_state.load_accounts()
    page.title = "Cafe"
    page.appbar = ft.AppBar(
        title=ft.Text("Sihun34 Cafe"),
        bgcolor=CAFE_COLOR,
        color="#222222",
        actions=[
            ft.IconButton(
                ft.Icons.HOME,
                tooltip="홈",
                on_click=lambda e: e.page.navigate("/"),
            ),
            ft.IconButton(
                ft.Icons.COFFEE,
                tooltip="주문",
                on_click=lambda e: e.page.navigate("/home"),
            ),
            ft.IconButton(
                ft.Icons.SHOPPING_CART,
                tooltip="카트",
                on_click=lambda e: e.page.navigate("/cart"),
            ),
            ft.IconButton(
                ft.Icons.ACCOUNT_CIRCLE,
                tooltip="프로필",
                on_click=lambda e: e.page.navigate("/profile"),
            ),
        ],
    )
    page.render(MainApp)


if __name__ == "__main__":
    ft.run(main)
