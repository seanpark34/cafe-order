import flet as ft
from app_state import AppState
@ft.component
def Profile(state: AppState, page: ft.Page):
    if not state.is_logged_in:
        return ft.Column(
            controls=[
                ft.Text("로그인이 필요합니다.", size=30),
                ft.Button("로그인", on_click=lambda e: page.navigate("/log_in"), bgcolor="#60FA41"),
            ]
        )
    
    icons = {
        "루키(1/16)": ft.Icons.EMOJI_EVENTS, "스톤(2/16)": ft.Icons.EMOJI_EVENTS,
        "핑크(3/16)": ft.Icons.EMOJI_EVENTS, "오렌지(4/16)": ft.Icons.EMOJI_EVENTS,
        "브론즈(5/16)": ft.Icons.EMOJI_EVENTS, "실버(6/16)": ft.Icons.EMOJI_EVENTS,
        "골드(7/16)": ft.Icons.EMOJI_EVENTS, "플래티넘(8/16)": ft.Icons.EMOJI_EVENTS,
        "사파이어(9/16)": ft.Icons.EMOJI_EVENTS, "루비(10/16)": ft.Icons.EMOJI_EVENTS,
        "에메랄드(11/16)": ft.Icons.EMOJI_EVENTS, "자수정(12/16)": ft.Icons.EMOJI_EVENTS,
        "펄(13/16)": ft.Icons.EMOJI_EVENTS,
        "다이아몬드(14/16)": ft.Icons.AUTO_AWESOME, "계획 마스터(15/16)": ft.Icons.AUTO_AWESOME, "계획 왕(16/16)": ft.Icons.AUTO_AWESOME,
    }

    colors = {
        "루키(1/16)": "#00000000", "스톤(2/16)": "#535353", "핑크(3/16)": "#e500ed",
        "오렌지(4/16)": "#ff7f00", "브론즈(5/16)": "#673300", "실버(6/16)": "#a2a2a2",
        "골드(7/16)": "#ffd700", "플래티넘(8/16)": "#e8e8e8", "사파이어(9/16)": "#1e78fe",
        "루비(10/16)": "#ff2525", "에메랄드(11/16)": "#50c878", "자수정(12/16)": "#9966cc",
        "펄(13/16)": "#f9a9f9", "다이아몬드(14/16)" : "#a9eaf9", "계획 마스터(15/16)": "#e0a4f9", "계획 왕(16/16)": "#ffe600",
    }

    nickname = state.nickname
    profile_color = "#000000" if state.levels.get(state.week, "루키(1/16)") == "루키(1/16)" else colors.get(state.levels.get(state.week, "루키(1/16)"), "#000000")
    level = state.levels.get(state.week, "루키(1/16)")
    color = colors[level]
    icon = icons[level]

    return ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=30, color=profile_color), 
                        ft.Text(nickname, size=20),
                    ]
                ),
                ft.Button("닉네임 변경", bgcolor="#60FA41", on_click=lambda e: page.navigate("/settings")),
                ft.Text(f"Week {state.week}", size=20),
                ft.Text(level, size=30),
                ft.Icon(icon, color=color, size=100),
            ]
    )
