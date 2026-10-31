from dataclasses import dataclass, field
import flet as ft


# 1. 상태 관리를 위한 Observable 클래스 정의
@ft.observable
@dataclass
class AppState():
    cart: list = field(default_factory=list)
    cart_count: int = 0




PRODUCTS = [
    {"name": "Americano", "price": "₩5000", "on_sale": False, "best":False, "new": False, "sale":"0%", "color":"#FFD500", "hot":True, "iced": True},
    {"name": "Cafe Latte", "price": "₩5200", "on_sale": True, "best":False,"new": False, "sale":"10%", "color":"#FFD500", "hot":True, "iced": True},
    {"name": "Vanila Latte", "price": "₩5500", "on_sale": True, "best":False,"new": False, "sale":"25%", "color":"#FFD500", "hot":True, "iced": True},
    {"name": "Strawberry Latte", "price": "₩6000", "on_sale": False, "best":True,"new": False, "sale":"0%", "color":"#FFA200", "hot":False, "iced": True},
    {"name": "Mango Latte", "price": "₩6300", "on_sale": False, "best":False,"new": False, "sale":"0%", "color":"#FFA200", "hot":False, "iced": True},
    {"name": "Hot Chocolate", "price": "₩6200", "on_sale": False, "best":False,"new": False, "sale":"0%", "color":"#FFA200", "hot":True, "iced": False},
    {"name": "Strawberry Cake", "price": "₩7500", "on_sale": False, "best":False,"new": False, "sale":"0%", "color":"#00E5FF", "hot":False, "iced": False},
    {"name": "Mango Cake", "price": "₩7700", "on_sale": False, "best":True, "new": False,"sale":"0%", "color":"#00E5FF", "hot":False, "iced": False},
    {"name": "Ham Egg Sandwich", "price": "₩5800", "on_sale": False, "best":False, "new": True, "sale":"0%", "color":"#00E5FF", "hot":False, "iced": False},
    {"name": "Penguin Doll", "price": "₩12000", "on_sale": True, "best":False, "new": False, "sale":"20%", "color":"#00FF22", "hot":False, "iced": False},
]


IMOJI = {
    "Americano": "(💧☕️)",
    "Cafe Latte": "(🥛☕)",
    "Vanila Latte": "(🌼☕️)",
    "Strawberry Latte": "(🍓🥛)",
    "Mango Latte": "(🥭🥛)",
    "Hot Chocolate": "(🍫🥛)",
    "Strawberry Cake": "(🍓🍰)",
    "Mango Cake": "(🥭🍰)",
    "Penguin Doll": "(🐧)",
    "Ham Egg Sandwich": "(🥪)"
}

IMAGE = {
    "Americano": "cafe_americano.png",
    "Cafe Latte": "cafe_latte.png",
    "Vanila Latte": "cafe_vanilalatte.png",
    "Strawberry Latte": "cafe_strawberrylatte.png",
    "Mango Latte": "cafe_mangolatte.png",
    "Hot Chocolate": "caffe_hotchocolete.png",
    "Strawberry Cake": "cafe_strawberrycake.png",
    "Mango Cake": "cafe_mangocake.png",
    "Penguin Doll": "cafe_penguindoll.png",
    "Ham Egg Sandwich": "cafe_hameggsandwitch.png"
}