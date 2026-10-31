from cafe_pay import _format_receipt_item


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
