import flet as ft
from cafe_status import AppState
from flet import CupertinoIcons
from datetime import timedelta, datetime
import asyncio

def _register_user(state: AppState, username: str, password: str, confirmation: str) -> str | None:
    if not username or not password:
        return "아이디와 비밀번호를 입력해 주세요."
    if len(password) < 8:
        return "비밀번호는 8자 이상 입력해 주세요."
    if password != confirmation:
        return "비밀번호가 서로 일치하지 않습니다."
    if any(user["id"].casefold() == username.casefold() for user in state.users):
        return "이미 사용 중인 아이디입니다."

    state.add_user({"id": username, "password": password})
    state.set_logged_in({"id": username})
    return None


async def _authenticate_user(state: AppState, username: str, password: str) -> str | None:
    if not username or not password:
        return "아이디와 비밀번호를 입력해 주세요."

    user = next(
        (
            account for account in state.users
            if account["id"].casefold() == username.casefold()
            and account["password"] == password
        ),
        None,
    )
    if user is None:
        return "아이디 또는 비밀번호가 올바르지 않습니다."

    state.users = [user, *(account for account in state.users if account is not user)]
    state.set_logged_in(user)
    await state.load_user_data()
    return None

today = datetime.now()
day_num = (today.weekday()+1) % 7
last_week_key = today - timedelta(day_num + 7)

@ft.component
def LogIn(state: AppState, page: ft.Page):
    is_signup, set_is_signup = ft.use_state(False)
    username_value, set_username_value = ft.use_state("")
    password, set_password = ft.use_state(True)
    password_value, set_password_value = ft.use_state("")
    confirm_password_value, set_confirm_password_value = ft.use_state("")
    error_message, set_error_message = ft.use_state("")

    trophie_level_up = [1, 2, 3, 4, 5, 7, 10, 15, 20, 25, 30, 35, 40, 45, 52]

    async def check_prize():
        selected_week_plans = state.plans_for_selected_week(last_week_key.strftime("%Y%m%d"))
        total_plan_types = len(selected_week_plans)
        completed_plan_types = sum(
            1
            for plan in selected_week_plans
            if plan.get("Done", 0) >= plan["how_much"]
            )
        this_week_progress_value = (
            completed_plan_types / total_plan_types if total_plan_types else 0
        )
        last_login_day = state.last_login.weekday()
        need_to_add = 6-last_login_day
        next_week_sunday = state.last_login + timedelta(need_to_add)
        if state.last_login < next_week_sunday:
                if this_week_progress_value == 1:    
                    state.week += 1
                    page.show_dialog(ft.SnackBar(ft.Text(f"지난주 할 일을 모두 완료했어요! {state.week}주 완료")))
                    if state.week in trophie_level_up:
                        await asyncio.sleep(3)
                        page.show_dialog(ft.SnackBar(ft.Text(f"{state.levels[state.week]} 트로피를 획득했어요!")))


    async def handle_login(_):
        username = username_value.strip()
        if is_signup:
            error = _register_user(
                state, username, password_value, confirm_password_value
            )
            if error:
                set_error_message(error)
                return
            set_error_message("")
            page.run_task(check_prize)
            state.save_last_login()
            page.navigate("/guide")
        else:
            error = await _authenticate_user(state, username, password_value)
            if error:
                set_error_message(error)
                return
            set_error_message("")
            page.run_task(check_prize)
            state.save_last_login()
            page.navigate("/calendar")

    def toggle_password(_):
        set_password(not password)

    def toggle_mode(_):
        set_is_signup(not is_signup)
        set_password_value("")
        set_confirm_password_value("")
        set_error_message("")

    def update_username(e):
        set_username_value(e.control.value or "")
        set_error_message("")

    def update_password(e):
        set_password_value(e.control.value or "")
        set_error_message("")

    def update_confirm_password(e):
        set_confirm_password_value(e.control.value or "")
        set_error_message("")

    icon = CupertinoIcons.EYE_SLASH if password else CupertinoIcons.EYE
    title = "회원가입" if is_signup else "로그인"

    return ft.Column(
        controls=[
            ft.Text("MyWeek", size=18, color="#52616B"),
            ft.Text(title, size=40),
            ft.Text(
                "새 계정을 만들어 일주일 계획을 관리하세요."
                if is_signup else "계정에 로그인해 계획을 이어가세요.",
                color="#52616B",
            ),
            ft.TextField(
                label="아이디",
                value=username_value,
                on_change=update_username,
            ),
            ft.Row(
                controls=[
                    ft.IconButton(
                        icon,
                        on_click=toggle_password,
                        tooltip="비밀번호 표시 전환",
                    ),
                    ft.TextField(
                        label="비밀번호",
                        value=password_value,
                        password=password,
                        on_change=update_password,
                    ),
                ]
            ),
            ft.TextField(
                label="비밀번호 확인",
                value=confirm_password_value,
                password=password,
                on_change=update_confirm_password,
            ) if is_signup else ft.Container(),
            ft.Text(error_message, color="#B42318") if error_message else ft.Container(),
            ft.Button(
                "가입하기" if is_signup else "로그인",
                on_click=handle_login,
                bgcolor="#60FA41",
            ),
            ft.Button(
                "이미 계정이 있어요. 로그인" if is_signup else "계정이 없으신가요? 회원가입",
                on_click=toggle_mode,
            ),
            ft.Text("⚠️아이디와 비밀번호는 이 기기에만 저장됩니다.", size=20, color="#B42318")
        ]
    )