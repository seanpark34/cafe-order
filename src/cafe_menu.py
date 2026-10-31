import flet as ft
from urllib.parse import unquote

from cafe_status import AppState, IMAGE, PRODUCTS

@ft.component
def Menu(state: AppState):
    selected_temperature, set_selected_temperature = ft.use_state(None)
    params = ft.use_route_params()
    product_name = unquote(params.get("product", ""))
    product = next(
        (item for item in PRODUCTS if item["name"] == product_name),
        None,
    )
    if product is None:
        return ft.Text("Menu item not found")

    supports_hot = product["hot"]
    supports_iced = product["iced"]
    requires_temperature_choice = supports_hot and supports_iced
    temperature = (
        selected_temperature
        if requires_temperature_choice
        else "Hot" if supports_hot
        else "Iced" if supports_iced
        else None
    )

    def add_to_cart(e: ft.ControlEvent):
        cart_item = next(
            (
                item
                for item in state.cart
                if item["name"] == product_name
                and item.get("temperature") == temperature
            ),
            None,
        )
        if cart_item:
            cart_item["count"] = str(int(cart_item["count"]) + 1)
        else:
            state.cart.append(
                {
                    "name": product_name,
                    "temperature": temperature,
                    "count": "1",
                    "price": product["price"],
                }
            )
        state.cart = state.cart.copy()
        state.cart_count += 1
        cart_item_name = product_name
        if temperature:
            cart_item_name = f"{cart_item_name} {temperature}"
        e.page.show_dialog(
            ft.SnackBar(ft.Text(f"Added {cart_item_name} to cart"))
        )
        e.page.navigate("/home")

    return ft.Column(
        controls=[
            ft.Image(
                src=IMAGE[product_name],
                width=300,
                height=300,
                fit=ft.BoxFit.CONTAIN,
                error_content=ft.Text(f"이미지 파일을 찾을 수 없습니다: {IMAGE[product_name]}"),
            ),
            ft.Text(product_name, size=32, weight=ft.FontWeight.BOLD),
            ft.Text(product["price"], size=24),
            ft.Row(
                controls=[
                    ft.Button(
                        "Hot",
                        bgcolor=(
                            "#FF3333"
                            if selected_temperature == "Hot"
                            or (not requires_temperature_choice and supports_hot)
                            else "#5A5A5A"
                        ),
                        visible=supports_hot,
                        on_click=lambda _: set_selected_temperature("Hot"),
                    ),
                    ft.Button(
                        "Iced",
                        bgcolor=(
                            "#009DFF"
                            if selected_temperature == "Iced"
                            or (not requires_temperature_choice and supports_iced)
                            else "#5A5A5A"
                        ),
                        visible=supports_iced,
                        on_click=lambda _: set_selected_temperature("Iced"),
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Button(
                "Add to Cart",
                on_click=add_to_cart,
                visible=not requires_temperature_choice or selected_temperature is not None,
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )