from app_state import AppState
from log_in import _authenticate_user, _register_user


def test_register_user_validates_and_creates_account():
    state = AppState()

    assert _register_user(state, "", "password1", "password1")
    assert _register_user(state, "alice", "short", "short")
    assert _register_user(state, "alice", "password1", "different")
    assert _register_user(state, "alice", "password1", "password1") is None
    assert _register_user(state, "ALICE", "password1", "password1")
    assert state.users[0]["id"] == "alice"
    assert state.login_done == 1


def test_authenticate_user_rejects_invalid_password():
    state = AppState(users=[{"id": "alice", "password": "password1"}])

    assert _authenticate_user(state, "alice", "wrong")
    assert state.login_done == 0


def test_authenticate_user_activates_matching_account():
    other = {"id": "other", "password": "password2"}
    account = {"id": "alice", "password": "password1"}
    state = AppState(users=[other, account])

    assert _authenticate_user(state, "ALICE", "password1") is None
    assert state.users[0]["id"] == "alice"
    assert state.users[1]["id"] == "other"
    assert state.login_done == 1
