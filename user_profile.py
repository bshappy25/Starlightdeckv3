# user_profile.py
import json
import os
from datetime import datetime

import streamlit as st

PROFILE_PATH = "user_profile.json"


def _now_iso() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def _read_json(path: str, default: dict) -> dict:
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def _write_json(path: str, data: dict) -> None:
    # Atomic-ish write: write temp then replace
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp, path)


def load_profiles(path: str = PROFILE_PATH) -> dict:
    """
    Returns:
      {
        "active_user_id": "default",
        "users": { "default": {...}, ... }
      }
    """
    return _read_json(path, default={"active_user_id": "default", "users": {}})


def save_profiles(data: dict, path: str = PROFILE_PATH) -> None:
    _write_json(path, data)


def get_or_create_user(path: str = PROFILE_PATH):
    """
    Streamlit UI to select/create a simple user profile.
    Also includes a basic age gate.

    Returns:
      (user_dict, preferred_vibe)  # preferred_vibe may be None
      OR (None, None) if age gate failed
    """
    st.subheader("User Profile")

    data = load_profiles(path)
    users = data.get("users", {})
    active_id = data.get("active_user_id", "default")

    # Ensure at least one user exists
    if not users:
        users["default"] = {
            "id": "default",
            "name": "Player",
            "age_confirmed": False,
            "preferred_vibe": None,
            "created_at": _now_iso(),
            "last_seen": _now_iso(),
        }
        data["users"] = users
        data["active_user_id"] = "default"
        save_profiles(data, path)

    # Select user (simple dropdown)
    user_ids = list(users.keys())
    labels = [f"{users[uid].get('name', uid)} ({uid})" for uid in user_ids]

    idx = user_ids.index(active_id) if active_id in user_ids else 0
    choice = st.selectbox("Select user:", options=list(range(len(user_ids))), format_func=lambda i: labels[i], index=idx)
    chosen_id = user_ids[choice]

    # Switch active user
    if chosen_id != active_id:
        data["active_user_id"] = chosen_id
        save_profiles(data, path)
        active_id = chosen_id

    user = users[active_id]

    # Edit user basics
    new_name = st.text_input("Display name:", value=user.get("name", "Player"))
    if new_name.strip() and new_name != user.get("name"):
        user["name"] = new_name.strip()

    user["last_seen"] = _now_iso()

    # Age gate
    st.caption("Age gate: required to use the app.")
    age_ok = st.checkbox("I confirm I am 13 or older", value=bool(user.get("age_confirmed", False)))
    user["age_confirmed"] = bool(age_ok)

    if not user["age_confirmed"]:
        save_profiles(data, path)
        st.error("Age confirmation is required to proceed.")
        return None, None

    # Optional preference (easy to expand later)
    preferred = st.selectbox(
        "Preferred vibe (optional):",
        options=[None, "acuity", "valor", "variety"],
        index=[None, "acuity", "valor", "variety"].index(user.get("preferred_vibe", None)),
        format_func=lambda x: "None" if x is None else x,
    )
    user["preferred_vibe"] = preferred

    # Add/create new user (very simple)
    with st.expander("Add a new user"):
        new_id = st.text_input("New user id (letters/numbers, no spaces)", value="")
        new_user_name = st.text_input("New user name", value="")
        if st.button("Create user"):
            nid = new_id.strip()
            if not nid:
                st.warning("Provide a user id.")
            elif nid in users:
                st.warning("That user id already exists.")
            else:
                users[nid] = {
                    "id": nid,
                    "name": (new_user_name.strip() or nid),
                    "age_confirmed": False,
                    "preferred_vibe": None,
                    "created_at": _now_iso(),
                    "last_seen": _now_iso(),
                }
                data["active_user_id"] = nid
                save_profiles(data, path)
                st.success("User created. Select it above.")
                st.rerun()

    # Persist updates
    data["users"][active_id] = user
    save_profiles(data, path)

    return user, user.get("preferred_vibe", None)
