import flet as ft
from cafe_status import AppState


@ft.component
def Cart(state: AppState):
    def in_cart_card(product: dict) -> ft.Control:
        display_name = product["name"]
        if product.get("temperature"):
            display_name = f"{display_name} {product['temperature']}"

        return ft.Container(
            expand=1,
            padding=12,
            border_radius=8,
            bgcolor=ft.Colors.YELLOW,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                expand=1,
                controls=[
                    ft.Text(display_name, weight=ft.FontWeight.BOLD, expand=12),
                    ft.Text(product["price"], color=ft.Colors.OUTLINE, expand=3),
                    ft.Container(
                        content=ft.Text(product["count"]),
                        expand=2,
                        alignment=ft.Alignment.CENTER_RIGHT,
                        padding=5
                    ),
                ],
            ),
        )


    def delete():
        state.cart.clear()
        state.cart_count=0
    # state.cart를 기반으로 리스트 생성
    cart_container = ft.Column(
        spacing=10,
        controls=[in_cart_card(product) for product in state.cart],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )
   
    return ft.Column(
        expand=True,
        controls=[
            ft.Container(
                content=ft.Row(
                    controls=[ft.Text("Cart🛒", size=20)],
                    alignment=ft.MainAxisAlignment.CENTER,
                    expand=1
                ),
                bgcolor="#FFAE00",
                height=100
            ),
            ft.Row(
                controls=[
                    ft.Button("Delete", on_click=delete),
                    ft.Button(
                        "Pay",
                        disabled=not state.cart,
                        on_click=lambda e: e.page.navigate("/pay"),
                    ),
                ],
            ),
            cart_container,
        ]
    )
