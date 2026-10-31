import flet as ft
from urllib.parse import quote

from cafe_status import AppState, PRODUCTS




def create_best_badge():
    return ft.Container(
        content=ft.Text("BEST", size=10, color=ft.Colors.BLACK),
        bgcolor=ft.Colors.YELLOW,
        padding=ft.Padding.symmetric(horizontal=6, vertical=2),
        border_radius=4,
        top=-6,
        right=-6,
    )


def create_on_sale_badge(sale):
    return ft.Container(
        content=ft.Text("SALE " + sale, size=10, color=ft.Colors.WHITE),
        bgcolor=ft.Colors.RED,
        padding=ft.Padding.symmetric(horizontal=6, vertical=2),
        border_radius=4,
        top=-6,
        right=-6,
    )


def create_new_badge():
    return ft.Container(
        content=ft.Text("NEW", size=10, color=ft.Colors.BLACK),
        bgcolor=ft.Colors.GREEN,
        padding=ft.Padding.symmetric(horizontal=6, vertical=2),
        border_radius=4,
        top=-6,
        right=-6,
    )


@ft.component
def Home(state: AppState):
    def add_to_cart(product_name: str, product_price):
        def handle_click(e: ft.ControlEvent):
            item_in_cart = None
            # 전역 IN_CART 대신 state.cart 참조
            for item in state.cart:
                if item["name"] == product_name:
                    item_in_cart = item


            if item_in_cart:
                count = int(item_in_cart["count"]) + 1
                added_item = {"name": product_name, "count": str(count), "price": product_price}
                state.cart.append(added_item)
                state.cart.remove(item_in_cart)
            else:
                added_item = {"name": product_name, "count": "1", "price": product_price}
                state.cart.append(added_item)
           
            # 상태 변경 알림 (Observable이 값이 변경되었음을 감지하고 UI를 다시 그림)
            state.cart = state.cart.copy() # 참조를 변경하여 완벽한 업데이트 트리거
            # state.cart_count = len(state.cart)
            state.cart_count += 1
           
            e.page.show_dialog(ft.SnackBar(ft.Text(f"Added {product_name} to cart")))
        return handle_click


    def product_card(product: dict) -> ft.Control:
        card = ft.Container(
            padding=12,
            border_radius=8,
            bgcolor=product["color"],
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Column(
                        spacing=2,
                        controls=[
                            ft.Text(product["name"], weight=ft.FontWeight.BOLD),
                            ft.Text(product["price"], color=ft.Colors.OUTLINE),
                        ],
                    ),
                    ft.Button(
                        "Add to Cart",
                        on_click=lambda e, name=product["name"]: e.page.navigate(
                            f"/menu/{quote(name, safe='')}"
                        ),
                    ),
                ],
            ),
        )


        badges = []
        if product["best"]:
            badges.append(create_best_badge())
        if product["on_sale"]:
            badges.append(create_on_sale_badge(product["sale"]))
        if product["new"]:
            badges.append(create_new_badge())
       


        return ft.Stack(
            clip_behavior=ft.ClipBehavior.NONE,
            controls=[card, *badges],
        )


    return ft.Column(
        spacing=10,
        controls=[
            ft.Row(
                controls=[
                    ft.Icon(ft.Icons.CIRCLE, color="#FFD500", size=15),
                    ft.Text("Coffee ", size=15),
                    ft.Icon(ft.Icons.CIRCLE, color="#FFA200", size=15),
                    ft.Text("Non-Coffee ", size=15),
                    ft.Icon(ft.Icons.CIRCLE, color="#00E5FF", size=15),
                    ft.Text("Dessert ", size=15),
                    ft.Icon(ft.Icons.CIRCLE, color="#00FF22", size=15),
                    ft.Text("Doll ", size=15),
                ],
                scroll=ft.ScrollMode.AUTO,
            ),
            *[product_card(product) for product in PRODUCTS],
        ],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )
