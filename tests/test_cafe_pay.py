from cafe_pay import _count_paid_items, _format_receipt_item
from cafe_status import cart_item_key


def test_receipt_item_includes_temperature_when_selected():
    assert _format_receipt_item(
        {
            "name": "Americano",
            "temperature": "Iced",
            "count": "2",
            "price": "₩5000",
        }
    ) == "Americano Iced x2  ₩5000"


def test_receipt_item_omits_temperature_when_not_applicable():
    assert _format_receipt_item(
        {"name": "Strawberry Cake", "count": "1", "price": "₩7500"}
    ) == "Strawberry Cake x1  ₩7500"


def test_receipt_item_shows_redeemed_and_paid_quantities_separately():
    assert _format_receipt_item(
        {
            "name": "Americano",
            "count": "3",
            "redeemed_count": 2,
            "price": "₩5000",
        }
    ) == "Americano x2  STAR REDEEM\nAmericano x1  ₩5000"


def test_stars_earned_match_paid_item_quantity():
    cart = [
        {"name": "Americano", "temperature": "Hot", "count": "3"},
        {"name": "Americano", "temperature": "Iced", "count": "2"},
        {"name": "Penguin Doll", "count": "1"},
    ]
    redemptions = {
        cart_item_key(cart[0]): 1,
        cart_item_key(cart[2]): 1,
    }

    assert _count_paid_items(cart, redemptions) == 4


def test_fully_redeemed_cart_earns_no_stars():
    cart = [{"name": "Americano", "temperature": "Iced", "count": "2"}]

    assert _count_paid_items(cart, {cart_item_key(cart[0]): 2}) == 0
