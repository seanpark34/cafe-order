import pytest

from cafe_login import _authenticate_user, _register_user
from cafe_status import AppState, calculate_redemption, cart_item_key


def test_register_user_validates_and_persists_account(tmp_path):
    state = AppState(accounts_path=tmp_path / "accounts.json")

    assert _register_user(state, "", "Alice", "password1", "password1")
    assert _register_user(state, "alice", "", "password1", "password1")
    assert _register_user(state, "alice", "Alice", "short", "short")
    assert _register_user(state, "alice", "Alice", "password1", "different")
    assert _register_user(state, "alice", "Alice", "password1", "password1") is None
    assert _register_user(state, "ALICE", "Alice 2", "password1", "password1")
    assert state.users[0]["id"] == "alice"
    assert state.users[0]["nickname"] == "Alice"
    assert state.users[0]["stars"] == 0
    assert state.is_logged_in

    stored_data = (tmp_path / "accounts.json").read_text(encoding="utf-8")
    assert "password1" not in stored_data
    assert "password_hash" in stored_data


def test_authenticate_user_rejects_invalid_password(tmp_path):
    state = AppState(accounts_path=tmp_path / "accounts.json")
    _register_user(state, "alice", "Alice", "password1", "password1")
    state.logout()

    assert _authenticate_user(state, "alice", "wrong")
    assert not state.is_logged_in


def test_authenticate_user_restores_account_and_stars(tmp_path):
    accounts_path = tmp_path / "accounts.json"
    state = AppState(accounts_path=accounts_path)
    _register_user(state, "other", "Other", "password2", "password2")
    _register_user(state, "alice", "Alice", "password1", "password1")
    state.add_stars(3)

    loaded_state = AppState(accounts_path=accounts_path)
    loaded_state.load_accounts()
    assert _authenticate_user(loaded_state, "ALICE", "password1") is None
    assert loaded_state.current_user["id"] == "alice"
    assert loaded_state.nickname == "Alice"
    assert loaded_state.stars == 3


def test_nickname_and_star_updates_persist(tmp_path):
    accounts_path = tmp_path / "accounts.json"
    state = AppState(accounts_path=accounts_path)
    _register_user(state, "alice", "Alice", "password1", "password1")
    state.update_nickname("Cafe Alice")
    state.add_stars()

    loaded_state = AppState(accounts_path=accounts_path)
    loaded_state.load_accounts()
    assert _authenticate_user(loaded_state, "alice", "password1") is None
    assert loaded_state.nickname == "Cafe Alice"
    assert loaded_state.stars == 1


def test_complete_purchase_deducts_redeemed_stars_and_awards_paid_order_star(
    tmp_path,
):
    state = AppState(accounts_path=tmp_path / "accounts.json")
    _register_user(state, "alice", "Alice", "password1", "password1")
    state.add_stars(35)

    state.complete_purchase(stars_spent=35, stars_earned=1)

    assert state.stars == 1


def test_complete_purchase_rejects_spending_more_stars_than_available(tmp_path):
    state = AppState(accounts_path=tmp_path / "accounts.json")
    _register_user(state, "alice", "Alice", "password1", "password1")
    state.add_stars(7)

    with pytest.raises(ValueError, match="보유한 별보다"):
        state.complete_purchase(stars_spent=8)
    assert state.stars == 7


def test_calculate_redemption_supports_multiple_reward_categories():
    cart = [
        {"name": "Americano", "temperature": "Iced", "count": "2", "price": "₩5000"},
        {"name": "Mango Latte", "temperature": "Iced", "count": "1", "price": "₩6300"},
        {"name": "Strawberry Cake", "count": "1", "price": "₩7500"},
        {"name": "Penguin Doll", "count": "1", "price": "₩12000"},
    ]
    redemptions = {
        cart_item_key(cart[0]): 1,
        cart_item_key(cart[1]): 1,
        cart_item_key(cart[2]): 1,
        cart_item_key(cart[3]): 1,
    }

    assert calculate_redemption(cart, redemptions) == (55, 30_800)


def test_calculate_redemption_rejects_more_items_than_cart_quantity():
    cart = [{"name": "Cafe Latte", "count": "1", "price": "₩5200"}]

    with pytest.raises(ValueError, match="주문 메뉴"):
        calculate_redemption(cart, {cart_item_key(cart[0]): 2})
