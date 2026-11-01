import hashlib
import json
import os
import secrets
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import flet as ft


CAFE_COLOR = "#FFBB00"
STAR_REWARDS = (
    ("coffee", "커피 1잔", 8),
    ("drink", "제조음료 1잔", 12),
    ("dessert", "디저트 1개", 15),
    ("doll", "인형 1개", 20),
)
STAR_REWARD_COSTS = {key: cost for key, _, cost in STAR_REWARDS}
PRODUCT_STAR_REWARDS = {
    "Americano": "coffee",
    "Cafe Latte": "coffee",
    "Vanila Latte": "coffee",
    "Strawberry Latte": "drink",
    "Mango Latte": "drink",
    "Hot Chocolate": "drink",
    "Strawberry Cake": "dessert",
    "Mango Cake": "dessert",
    "Penguin Doll": "doll",
}


def cart_item_key(item: dict[str, Any]) -> str:
    return f"{item['name']}|{item.get('temperature', '')}"


def calculate_redemption(cart: list[dict[str, Any]], counts: dict[str, int]) -> tuple[int, int]:
    stars_spent = 0
    amount_discounted = 0
    cart_keys = set()

    for item in cart:
        key = cart_item_key(item)
        cart_keys.add(key)
        count = counts.get(key, 0)
        quantity = int(item["count"])
        reward_key = PRODUCT_STAR_REWARDS.get(item["name"])
        if count < 0 or count > quantity or (count and reward_key is None):
            raise ValueError("별 교환 수량이 주문 메뉴와 일치하지 않습니다.")
        if count:
            stars_spent += STAR_REWARD_COSTS[reward_key] * count
            amount_discounted += (
                int(item["price"].replace("₩", "").replace(",", "")) * count
            )

    if any(key not in cart_keys and count for key, count in counts.items()):
        raise ValueError("별 교환 메뉴가 주문에 없습니다.")
    return stars_spent, amount_discounted


def _account_storage_path() -> Path:
    if os.name == "nt":
        data_dir = Path(
            os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local")
        )
    elif sys.platform == "darwin":
        data_dir = Path.home() / "Library" / "Application Support"
    else:
        data_dir = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
    return data_dir / "Sihun34Cafe" / "accounts.json"


def _password_hash(password: str, salt: bytes) -> str:
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 310_000).hex()


@ft.observable
@dataclass
class AppState:
    cart: list[dict[str, Any]] = field(default_factory=list)
    cart_count: int = 0
    users: list[dict[str, Any]] = field(default_factory=list)
    current_user_id: str | None = None
    accounts_path: Path = field(default_factory=_account_storage_path, repr=False)

    @property
    def current_user(self) -> dict[str, Any] | None:
        return next(
            (user for user in self.users if user["id"] == self.current_user_id),
            None,
        )

    @property
    def is_logged_in(self) -> bool:
        return self.current_user is not None

    @property
    def nickname(self) -> str:
        user = self.current_user
        return user["nickname"] if user else ""

    @property
    def stars(self) -> int:
        user = self.current_user
        return user["stars"] if user else 0

    def load_accounts(self) -> None:
        if not self.accounts_path.exists():
            return

        payload = json.loads(self.accounts_path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict) or not isinstance(payload.get("users"), list):
            raise ValueError("로컬 계정 파일 형식이 올바르지 않습니다.")

        users = payload["users"]
        for user in users:
            if (
                not isinstance(user, dict)
                or not all(
                    isinstance(user.get(key), str)
                    for key in ("id", "nickname", "password_salt", "password_hash")
                )
                or not isinstance(user.get("stars"), int)
                or user["stars"] < 0
            ):
                raise ValueError("로컬 계정 데이터가 올바르지 않습니다.")
        self.users = users

    def _save_accounts(self, users: list[dict[str, Any]]) -> None:
        self.accounts_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "users": [
                {
                    key: user[key]
                    for key in (
                        "id",
                        "nickname",
                        "password_salt",
                        "password_hash",
                        "stars",
                    )
                }
                for user in users
            ]
        }
        temp_path: Path | None = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=self.accounts_path.parent,
                delete=False,
            ) as temp_file:
                temp_path = Path(temp_file.name)
                json.dump(payload, temp_file, ensure_ascii=False, indent=2)
            os.replace(temp_path, self.accounts_path)
        finally:
            if temp_path is not None and temp_path.exists():
                temp_path.unlink()

    def add_user(self, username: str, nickname: str, password: str) -> None:
        salt = secrets.token_bytes(16)
        user = {
            "id": username,
            "nickname": nickname,
            "password_salt": salt.hex(),
            "password_hash": _password_hash(password, salt),
            "stars": 0,
        }
        users = [*self.users, user]
        self._save_accounts(users)
        self.users = users
        self.current_user_id = username

    def authenticate(self, username: str, password: str) -> bool:
        user = next(
            (
                account
                for account in self.users
                if account["id"].casefold() == username.casefold()
            ),
            None,
        )
        if user is None:
            return False
        salt = bytes.fromhex(user["password_salt"])
        if not secrets.compare_digest(
            user["password_hash"], _password_hash(password, salt)
        ):
            return False
        self.current_user_id = user["id"]
        return True

    def update_nickname(self, nickname: str) -> None:
        user = self.current_user
        if user is None:
            raise ValueError("로그인이 필요합니다.")
        updated_user = {**user, "nickname": nickname}
        users = [
            updated_user if account is user else account for account in self.users
        ]
        self._save_accounts(users)
        self.users = users

    def add_stars(self, count: int = 1) -> None:
        user = self.current_user
        if user is None or count <= 0:
            return
        updated_user = {**user, "stars": user["stars"] + count}
        users = [
            updated_user if account is user else account for account in self.users
        ]
        self._save_accounts(users)
        self.users = users

    def complete_purchase(self, stars_spent: int, stars_earned: int = 0) -> None:
        if stars_spent < 0 or stars_earned < 0:
            raise ValueError("별 사용 및 적립 개수는 음수일 수 없습니다.")
        if stars_spent == 0 and stars_earned == 0:
            return
        user = self.current_user
        if user is None:
            raise ValueError("로그인이 필요합니다.")
        if stars_spent > user["stars"]:
            raise ValueError("보유한 별보다 많이 사용할 수 없습니다.")

        updated_user = {
            **user,
            "stars": user["stars"] - stars_spent + stars_earned,
        }
        users = [
            updated_user if account is user else account for account in self.users
        ]
        self._save_accounts(users)
        self.users = users

    def logout(self) -> None:
        self.current_user_id = None




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