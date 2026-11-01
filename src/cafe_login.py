import flet as ft

from cafe_status import AppState, CAFE_COLOR


def _register_user(
    state: AppState,
    username: str,
    nickname: str,
    password: str,
    confirmation: str,
) -> str | None:
    if not username or not nickname or not password:
        return "아이디, 닉네임, 비밀번호를 모두 입력해 주세요."
    if len(password) < 8:
        return "비밀번호는 8자 이상 입력해 주세요."
    if password != confirmation:
        return "비밀번호가 서로 일치하지 않습니다."
    if any(user["id"].casefold() == username.casefold() for user in state.users):
        return "이미 사용 중인 아이디입니다."

    state.add_user(username, nickname, password)
    return None


def _authenticate_user(state: AppState, username: str, password: str) -> str | None:
    if not username or not password:
        return "아이디와 비밀번호를 입력해 주세요."
    if not state.authenticate(username, password):
        return "아이디 또는 비밀번호가 올바르지 않습니다."
    return None


@ft.component
def LogIn(state: AppState, page: ft.Page):
    is_signup, set_is_signup = ft.use_state(False)
    username_value, set_username_value = ft.use_state("")
    nickname_value, set_nickname_value = ft.use_state("")
    password_value, set_password_value = ft.use_state("")
    confirm_password_value, set_confirm_password_value = ft.use_state("")
    error_message, set_error_message = ft.use_state("")

    def handle_login(_):
        username = username_value.strip()
        if is_signup:
            try:
                error = _register_user(
                    state,
                    username,
                    nickname_value.strip(),
                    password_value,
                    confirm_password_value,
                )
            except OSError:
                set_error_message("계정 정보를 기기에 저장하지 못했습니다.")
                return
        else:
            error = _authenticate_user(state, username, password_value)
        if error:
            set_error_message(error)
            return
        set_error_message("")
        page.navigate("/profile")

    def toggle_mode(_):
        set_is_signup(not is_signup)
        set_nickname_value("")
        set_password_value("")
        set_confirm_password_value("")
        set_error_message("")

    def update_field(e, setter):
        setter(e.control.value or "")
        set_error_message("")

    return ft.Container(
        expand=True,
        alignment=ft.Alignment.CENTER,
        padding=16,
        content=ft.Container(
            width=420,
            padding=24,
            border_radius=20,
            bgcolor="#F2F2F7",
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=14,
                controls=[
                    ft.Icon(ft.Icons.COFFEE, size=48, color=CAFE_COLOR),
                    ft.Text("Sihun34 Cafe", size=18, color="#333333"),
                    ft.Text(
                        "회원가입" if is_signup else "로그인",
                        size=32,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Text(
                        "계정을 만들고 주문과 별을 관리하세요."
                        if is_signup
                        else "계정에 로그인해 주문을 이어가세요.",
                        color="#555555",
                    ),
                    ft.TextField(
                        label="아이디",
                        value=username_value,
                        on_change=lambda e: update_field(e, set_username_value),
                    ),
                    ft.TextField(
                        label="닉네임",
                        value=nickname_value,
                        visible=is_signup,
                        on_change=lambda e: update_field(e, set_nickname_value),
                    ),
                    ft.TextField(
                        label="비밀번호",
                        value=password_value,
                        password=True,
                        can_reveal_password=True,
                        on_change=lambda e: update_field(e, set_password_value),
                    ),
                    ft.TextField(
                        label="비밀번호 확인",
                        value=confirm_password_value,
                        password=True,
                        can_reveal_password=True,
                        visible=is_signup,
                        on_change=lambda e: update_field(e, set_confirm_password_value),
                    ),
                    ft.Text(error_message, color="#B42318")
                    if error_message
                    else ft.Container(),
                    ft.Button(
                        "가입하기" if is_signup else "로그인",
                        on_click=handle_login,
                        bgcolor=CAFE_COLOR,
                        color="#222222",
                        width=360,
                    ),
                    ft.TextButton(
                        "이미 계정이 있어요. 로그인"
                        if is_signup
                        else "계정이 없으신가요? 회원가입",
                        on_click=toggle_mode,
                    ),
                    ft.Text(
                        "계정 정보는 이 기기에 저장되며, 비밀번호는 해시로 보관됩니다.",
                        size=12,
                        color="#555555",
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
            ),
        ),
    )
