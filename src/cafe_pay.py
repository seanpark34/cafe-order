import asyncio

import flet as ft

from cafe_status import (
    AppState,
    PRODUCT_STAR_REWARDS,
    STAR_REWARD_COSTS,
    calculate_redemption,
    cart_item_key,
)


def _format_receipt_item(item: dict) -> str:
    name = item["name"]
    if item.get("temperature"):
        name = f"{name} {item['temperature']}"
    count = int(item["count"])
    redeemed_count = item.get("redeemed_count", 0)
    lines = []
    if redeemed_count:
        lines.append(f"{name} x{redeemed_count}  STAR REDEEM")
    paid_count = count - redeemed_count
    if paid_count:
        lines.append(f"{name} x{paid_count}  {item['price']}")
    return "\n".join(lines)


def _count_paid_items(cart: list[dict], redemptions: dict[str, int]) -> int:
    return sum(
        int(item["count"]) - redemptions.get(cart_item_key(item), 0)
        for item in cart
    )


@ft.component
def Pay(state: AppState):
    payment_started, set_payment_started = ft.use_state(False)
    card_at_reader, set_card_at_reader = ft.use_state(False)
    card_tapped, set_card_tapped = ft.use_state(False)
    loading_dots, set_loading_dots = ft.use_state(1)
    payment_complete, set_payment_complete = ft.use_state(False)
    receipt_printing, set_receipt_printing = ft.use_state(False)
    receipt_moving, set_receipt_moving = ft.use_state(False)
    receipt_items, set_receipt_items = ft.use_state([])
    receipt_total, set_receipt_total = ft.use_state(0)
    redemptions, set_redemptions = ft.use_state({})
    stars_spent, amount_discounted = calculate_redemption(
        state.cart, redemptions
    )
    subtotal = sum(
        int(item["price"].replace("₩", "").replace(",", ""))
        * int(item["count"])
        for item in state.cart
    )
    total = subtotal - amount_discounted

    def update_redemption(key: str, change: int) -> None:
        updated = dict(redemptions)
        updated[key] = updated.get(key, 0) + change
        if updated[key] == 0:
            del updated[key]
        set_redemptions(updated)

    redemption_controls = []
    if state.is_logged_in:
        for item in state.cart:
            reward_key = PRODUCT_STAR_REWARDS.get(item["name"])
            if reward_key is None:
                continue
            item_key = cart_item_key(item)
            selected_count = redemptions.get(item_key, 0)
            item_quantity = int(item["count"])
            stars_remaining = state.stars - stars_spent
            star_cost = STAR_REWARD_COSTS[reward_key]
            redemption_controls.append(
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Text(f"{item['name']} · 별 {star_cost}개"),
                        ft.IconButton(
                            ft.Icons.REMOVE,
                            on_click=lambda _, key=item_key: update_redemption(
                                key, -1
                            ),
                            disabled=selected_count == 0,
                        ),
                        ft.Text(f"{selected_count}/{item_quantity}"),
                        ft.IconButton(
                            ft.Icons.ADD,
                            on_click=lambda _, key=item_key: update_redemption(
                                key, 1
                            ),
                            disabled=(
                                selected_count >= item_quantity
                                or stars_remaining < star_cost
                            ),
                        ),
                    ],
                )
            )
    receipt_line_count = sum(
        len(_format_receipt_item(item).splitlines()) for item in receipt_items
    )
    receipt_height = 160 + 32 * receipt_line_count
    receipt_stack_height = max(400, 100 + receipt_height)

    async def start_payment(e):
        stars_earned = _count_paid_items(state.cart, redemptions)
        receipt_snapshot = []
        for item in state.cart:
            receipt_item = dict(item)
            receipt_item["redeemed_count"] = redemptions.get(
                cart_item_key(item), 0
            )
            receipt_snapshot.append(receipt_item)
        set_receipt_items(receipt_snapshot)
        set_receipt_total(total)
        set_payment_started(True)
        if total > 0:
            await asyncio.sleep(0.1)
            set_card_at_reader(True)
            await asyncio.sleep(1.5)
            set_card_tapped(True)
            for step in range(6):
                await asyncio.sleep(0.4)
                set_loading_dots(step % 3 + 1)
        if state.is_logged_in:
            try:
                state.complete_purchase(
                    stars_spent,
                    stars_earned=stars_earned,
                )
            except (OSError, ValueError):
                set_payment_started(False)
                e.page.show_dialog(
                    ft.SnackBar(
                        ft.Text("별 처리에 실패해 주문을 완료하지 못했습니다.")
                    )
                )
                return
        set_payment_complete(True)
        await asyncio.sleep(1)
        set_payment_started(False)
        await asyncio.sleep(0.2)
        set_receipt_printing(True)
        await asyncio.sleep(0.1)
        set_receipt_moving(True)
        await asyncio.sleep(1.5)
        state.cart = []
        state.cart_count = 0

    return ft.Column(
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Text(
                f"Total : ₩{total:,}",
                size=28,
                visible=not payment_started and not payment_complete,
            ),
            ft.Text(
                f"별 {stars_spent}개 사용 · {amount_discounted:,}원 할인",
                visible=(
                    not payment_started
                    and not payment_complete
                    and stars_spent > 0
                ),
            ),
            ft.Column(
                spacing=0,
                controls=redemption_controls,
                visible=not payment_started and not payment_complete,
            ),
            ft.Text(
                "로그인하면 보유 별을 사용할 수 있어요.",
                visible=(
                    not state.is_logged_in
                    and not payment_started
                    and not payment_complete
                ),
            ),
            ft.Button(
                "별로 주문하기" if total == 0 and stars_spent > 0 else "Pay",
                on_click=start_payment,
                disabled=payment_started or (total == 0 and stars_spent == 0),
                visible=(
                    not payment_started
                    and not payment_complete
                    and (total > 0 or stars_spent > 0)
                ),
            ),
            ft.Stack(
                width=300,
                height=220,
                visible=payment_started and not receipt_printing,
                controls=[
                    ft.Container(
                        left=20,
                        top=115,
                        width=260,
                        height=85,
                        bgcolor="#333333",
                        border_radius=12,
                        content=ft.Column(
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Icon(ft.Icons.CONTACTLESS, color=ft.Colors.WHITE, size=34),
                                ft.Text("CARD READER", color=ft.Colors.WHITE),
                            ],
                        ),
                    ),
                    ft.Container(
                        left=40,
                        top=0,
                        width=220,
                        height=130,
                        offset=ft.Offset(0, 0.6 if card_at_reader else -0.3),
                        animate_offset=ft.Animation(
                            1500,
                            ft.AnimationCurve.EASE_IN_OUT,
                        ),
                        scale=0.88 if card_tapped else 1,
                        animate_scale=ft.Animation(
                            400,
                            ft.AnimationCurve.EASE_IN_OUT,
                        ),
                        bgcolor="#1976D2",
                        border_radius=12,
                        padding=16,
                        content=ft.Column(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Icon(ft.Icons.CREDIT_CARD, color=ft.Colors.WHITE, size=32),
                                ft.Text("CREDIT CARD", color=ft.Colors.WHITE),
                            ],
                        ),
                    ),
                ],
            ),
            ft.Text(
                f"loading{'.' * loading_dots}",
                size=22,
                visible=payment_started and not payment_complete,
                no_wrap=True,
            ),
            ft.Icon(
                ft.Icons.CHECK_CIRCLE,
                color=ft.Colors.GREEN,
                size=48,
                visible=payment_complete and payment_started,
            ),
            ft.Stack(
                width=300,
                height=receipt_stack_height,
                visible=receipt_printing,
                controls=[
                    ft.Container(
                        left=25,
                        top=35,
                        width=250,
                        height=75,
                        bgcolor="#333333",
                        border_radius=10,
                        content=ft.Column(
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Icon(
                                    ft.Icons.RECEIPT_LONG,
                                    color=ft.Colors.WHITE,
                                    size=32,
                                ),
                                ft.Text("RECEIPT PRINTER", color=ft.Colors.WHITE),
                            ],
                        ),
                    ),
                    ft.Container(
                        left=55,
                        top=85,
                        width=190,
                        height=receipt_height,
                        offset=ft.Offset(0, 0 if receipt_moving else -0.75),
                        animate_offset=ft.Animation(
                            1500,
                            ft.AnimationCurve.EASE_OUT,
                        ),
                        animate_size=ft.Animation(
                            500,
                            ft.AnimationCurve.EASE_IN_OUT,
                        ),
                        bgcolor=ft.Colors.WHITE,
                        border=ft.Border.all(1, "#BBBBBB"),
                        padding=12,
                        content=ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=6,
                            controls=[
                                ft.Text("SIHUN34 CAFE", weight=ft.FontWeight.BOLD),
                                ft.Text("------------------------", size=12),
                                *[
                                    ft.Text(line)
                                    for item in receipt_items
                                    for line in _format_receipt_item(item).splitlines()
                                ],
                                ft.Text("------------------------", size=12),
                                ft.Text(
                                    f"TOTAL  ₩{receipt_total:,}",
                                    weight=ft.FontWeight.BOLD,
                                ),
                                ft.Text("Thank you!", size=12),
                            ],
                        ),
                    ),
                ],
            ),
        ],
    )
