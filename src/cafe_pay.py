import asyncio

import flet as ft

from cafe_status import AppState


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
    total = sum(
        int(item["price"].replace("₩", "").replace(",", ""))
        * int(item["count"])
        for item in state.cart
    )
    receipt_height = 160 + 32 * len(receipt_items)
    receipt_stack_height = max(400, 100 + receipt_height)

    async def start_payment(_):
        set_receipt_items([dict(item) for item in state.cart])
        set_receipt_total(total)
        set_payment_started(True)
        await asyncio.sleep(0.1)
        set_card_at_reader(True)
        await asyncio.sleep(1.5)
        set_card_tapped(True)
        for step in range(6):
            await asyncio.sleep(0.4)
            set_loading_dots(step % 3 + 1)
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
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Text(
                f"Total : ₩{total:,}",
                size=28,
                visible=not payment_started and not payment_complete,
            ),
            ft.Button(
                "Pay",
                on_click=start_payment,
                disabled=payment_started or total == 0,
                visible=not payment_started and not payment_complete and total > 0,
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
                                    ft.Text(
                                        f"{item['name']} x{item['count']}  {item['price']}"
                                    )
                                    for item in receipt_items
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
