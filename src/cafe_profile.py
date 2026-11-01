import flet as ft

from cafe_status import AppState, CAFE_COLOR, STAR_REWARDS


@ft.component
def Profile(state: AppState, page: ft.Page):
    if not state.is_logged_in:
        return ft.Column(
            controls=[
                ft.Text("로그인 후 프로필을 확인할 수 있어요.", size=22),
                ft.Button("로그인", on_click=lambda e: page.navigate("/login")),
            ]
        )

    nickname_value, set_nickname_value = ft.use_state(state.nickname)
    message, set_message = ft.use_state("")

    return ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=16,
        controls=[
            ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=72, color=CAFE_COLOR),
            ft.Text(state.nickname, size=28, weight=ft.FontWeight.BOLD),
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Icon(ft.Icons.STAR, color=CAFE_COLOR),
                    ft.Text(f" {state.stars}", size=24),
                ],
            ),
            ft.Button(
                "별 사용 가능 목록",
                on_click=lambda _: _show_star_rewards(state, page),
            ),
            ft.Text(f"아이디: {state.current_user['id']}", color="#555555"),
            ft.TextField(
                label="닉네임 변경",
                value=nickname_value,
                on_change=lambda e: set_nickname_value(e.control.value or ""),
                width=320,
            ),
            ft.Button(
                "저장",
                on_click=lambda _: _save_nickname(
                    state, nickname_value, set_message
                ),
                bgcolor=CAFE_COLOR,
                color="#222222",
            ),
            ft.Text(message, color="#7A5200" if message else ft.Colors.ERROR),
            ft.Button("로그아웃", on_click=lambda _: _logout(state, page)),
        ],
    )


def _show_star_rewards(state: AppState, page: ft.Page) -> None:
    reward_rows = []
    for _, reward_name, star_cost in STAR_REWARDS:
        available_count = state.stars // star_cost
        progress_stars = state.stars % star_cost
        progress = min(state.stars / star_cost, 1.0)
        progress_text = (
            f"{available_count}개 교환 가능 · 다음 {progress_stars}/{star_cost}개"
            if available_count
            else f"{state.stars}/{star_cost}개"
        )
        reward_rows.append(
            ft.Column(
                spacing=4,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(reward_name),
                            ft.Text(f"별 {star_cost}개", color="#555555"),
                        ],
                    ),
                    ft.ProgressBar(
                        value=progress,
                        width=280,
                        color=CAFE_COLOR,
                    ),
                    ft.Text(progress_text, size=12, color="#555555"),
                ],
            )
        )
    page.show_dialog(
        ft.AlertDialog(
            modal=True,
            title=ft.Text("별 사용 가능 목록"),
            content=ft.Column(
                spacing=16,
                scroll=ft.ScrollMode.AUTO,
                controls=[
                    *reward_rows,
                ],
            ),
            actions=[
                ft.TextButton("닫기", on_click=lambda _: page.pop_dialog()),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
    )


def _save_nickname(state: AppState, nickname: str, set_message) -> None:
    nickname = nickname.strip()
    if not nickname:
        set_message("닉네임을 입력해 주세요.")
        return
    try:
        state.update_nickname(nickname)
    except OSError:
        set_message("닉네임을 기기에 저장하지 못했습니다.")
        return
    set_message("닉네임을 저장했습니다.")


def _logout(state: AppState, page: ft.Page) -> None:
    state.logout()
    page.navigate("/login")
