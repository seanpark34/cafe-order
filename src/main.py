import flet as ft
from cafe_status import AppState, IMOJI
from cafe_sihun34 import Sihun34
from cafe_pay import Pay
from cafe_cart import Cart
from cafe_home import Home
from cafe_menu import Menu

# 전역 상태 인스턴스 생성
global_state = AppState()




# App 최상위 컴포넌트도 state를 받습니다.
@ft.component
def App(state: AppState):
    return ft.SafeArea(
        content=ft.Column(
            controls=[
                ft.Router(
                    [
                        # 라우터의 자식 컴포넌트들에게 state를 주입해 줍니다.
                        ft.Route(index=True, component=lambda: Sihun34(state=state)),
                        ft.Route(path="sihun34", component=lambda: Sihun34(state=state)),
                        ft.Route(path="cart", component=lambda: Cart(state=state)),
                        ft.Route(path="pay", component=lambda: Pay(state=state)),
                        ft.Route(path="home", component=lambda: Home(state=state)),
                        ft.Route(path="menu/:product", component=lambda: Menu(state=state)),
                    ]
                ),
            ],
            expand=True,
        ),
        expand=True,
    )


@ft.component
def MainApp():
    # 여기서 App에 상태를 주입합니다.
    return App(state=global_state)


# 👇 새롭게 추가된 일반 main 함수
def main(page: ft.Page):
    page.title = "Cafe"
    page.appbar = ft.AppBar(
        title=ft.Text("Sihun34 Cafe☕"),
        bgcolor="#00bbff",
        actions=[ft.IconButton(ft.Icons.HOME, on_click=lambda e: ft.context.page.navigate("/")), ft.IconButton(ft.Icons.COFFEE, on_click=lambda e: ft.context.page.navigate("/home")), ft.IconButton(ft.Icons.SHOPPING_CART,  on_click=lambda e: ft.context.page.navigate("/cart"))],
        )
    # 💡 핵심: MainApp() 처럼 괄호를 붙여서 실행하지 말고,
    # MainApp 함수 '이름 자체'를 넘겨야 Flet이 준비된 후 알아서 실행합니다!
    page.render(MainApp)


if __name__ == "__main__":
    # ft.run에는 page를 받는 main 함수를 넘겨줍니다.
    ft.run(main)
