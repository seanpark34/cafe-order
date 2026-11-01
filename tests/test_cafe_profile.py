from cafe_profile import _show_star_rewards
from cafe_status import AppState


def test_star_rewards_dialog_shows_all_rewards_and_progress():
    state = AppState(
        users=[{"id": "alice", "nickname": "Alice", "stars": 10}],
        current_user_id="alice",
    )
    page = type(
        "Page",
        (),
        {"show_dialog": lambda self, dialog: setattr(self, "dialog", dialog)},
    )()

    _show_star_rewards(state, page)

    reward_rows = page.dialog.content.controls
    assert [row.controls[0].controls[0].value for row in reward_rows] == [
        "커피 1잔",
        "제조음료 1잔",
        "디저트 1개",
        "인형 1개",
    ]
    assert [row.controls[1].value for row in reward_rows] == [
        1.0,
        10 / 12,
        10 / 15,
        0.5,
    ]
    assert reward_rows[0].controls[2].value == "1개 교환 가능 · 다음 2/8개"
