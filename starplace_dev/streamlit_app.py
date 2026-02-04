import json
import os
from datetime import datetime, timezone

import streamlit as st

# ============================================================
# STARPLACE DEV (SANDBOX) — NO TOKENS / NO REAL ECONOMY
# ------------------------------------------------------------
# - Free entry
# - Fake Careon only (clearly labeled)
# - Saves profile cosmetics + journal to starplace_dev/state/
# ============================================================

APP_DIR = os.path.dirname(__file__)
STATE_DIR = os.path.join(APP_DIR, "state")
USERS_PATH = os.path.join(STATE_DIR, "starplace_users.json")

APP_TITLE = "Starplace (DEV)"
APP_ICON = "⭐"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _ensure_dir(path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)


def save_json(path: str, data):
    _ensure_dir(path)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_json_safe(path: str, default):
    try:
        if not os.path.exists(path):
            save_json(path, default)
            return default

        raw = open(path, "r", encoding="utf-8").read().strip()
        if not raw:
            save_json(path, default)
            return default

        return json.loads(raw)
    except Exception:
        return default


def default_db():
    return {
        "meta": {"version": "dev1", "updated_at": _now_iso()},
        "users": [
            {
                "user_id": "user-1",
                "display_name": "Guest",
                "created_at": _now_iso(),
                "starplace": {
                    "quote": "",
                    "journal": "",
                    "theme": {"bg": "nebula_ink"},
                    "avatar": {"icon_id": "icon_01"},
                    "cosmetics": {"unlocked": [], "active_stickers": []},
                    "arcade": {"played": []},
                },
            }
        ],
    }


def get_user(db: dict, user_id: str):
    for u in db.get("users", []):
        if u.get("user_id") == user_id:
            return u
    return None


def upsert_user(db: dict, user: dict):
    users = db.setdefault("users", [])
    for i, u in enumerate(users):
        if u.get("user_id") == user.get("user_id"):
            users[i] = user
            db["meta"]["updated_at"] = _now_iso()
            return
    users.append(user)
    db["meta"]["updated_at"] = _now_iso()


# ============================================================
# DESIGN ZONE (safe)
# ============================================================
CUSTOM_CSS = """
<style>
/* Page background */
.stApp{
  background: linear-gradient(180deg, #0b1020 0%, #121a33 55%, #0b1020 100%);
  color: rgba(245,245,247,0.92);
}

/* Sidebar: solid white, subtle gray border */
section[data-testid="stSidebar"]{
  background: #ffffff;
  border-right: 1px solid rgba(0,0,0,0.12);
}
section[data-testid="stSidebar"] *{
  color: rgba(10,10,12,0.92) !important;
}

/* Retro module shell */
.sp-module{
  border-radius: 18px;
  padding: 14px 16px;
  border: 1px solid rgba(255,255,255,0.18);
  background: rgba(255,255,255,0.06);
  backdrop-filter: blur(10px);
  box-shadow: 0 10px 34px rgba(0,0,0,0.28);
  margin: 10px 0;
}

/* Sticker strip vibe */
.sp-strip{
  border-radius: 14px;
  padding: 10px 12px;
  border: 1px dashed rgba(255,255,255,0.20);
  background: rgba(255,255,255,0.04);
}

/* Title */
.sp-title{
  font-weight: 950;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  font-size: 1.35rem;
  margin-bottom: 4px;
}
.sp-sub{
  color: rgba(245,245,247,0.70);
  margin-bottom: 10px;
}

/* Simple badge */
.sp-badge{
  display:inline-block;
  padding: 6px 10px;
  border-radius: 999px;
  border: 1px solid rgba(255,255,255,0.22);
  background: rgba(255,255,255,0.06);
  font-weight: 800;
  letter-spacing: 0.06em;
}

/* Fake Careon ticker */
.sp-ticker{
  border-radius: 14px;
  padding: 8px 12px;
  border: 1px solid rgba(255,255,255,0.16);
  background: rgba(255,255,255,0.05);
}
</style>
"""


THEMES = {
    "nebula_ink": {"label": "Nebula Ink", "swatch": "#0b1020"},
    "moon_milk": {"label": "Moon Milk", "swatch": "#f6f6f7"},
    "peach_glow": {"label": "Peach Glow", "swatch": "#ffcfb3"},
    "ocean_glass": {"label": "Ocean Glass", "swatch": "#78dcd2"},
    "forest_hush": {"label": "Forest Hush", "swatch": "#6fcf97"},
    "sunset_pulse": {"label": "Sunset Pulse", "swatch": "#ff7a7a"},
}

ICON_OPTIONS = [f"icon_{i:02d}" for i in range(1, 11)]
COST_THEME = 200
COST_ICON = 100
COST_STICKER = 150


def _get_fake_balance() -> int:
    st.session_state.setdefault("FAKE_CAREON", 5000)
    return int(st.session_state["FAKE_CAREON"])


def _spend_fake(amount: int) -> bool:
    bal = _get_fake_balance()
    if amount <= 0:
        return True
    if bal < amount:
        return False
    st.session_state["FAKE_CAREON"] = bal - amount
    return True


# ============================================================
# UI
# ============================================================
st.set_page_config(page_title=APP_TITLE, page_icon=APP_ICON, layout="wide")
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

db = load_json_safe(USERS_PATH, default_db())

st.sidebar.markdown(f"## {APP_ICON} {APP_TITLE}")
st.sidebar.caption("DEV SANDBOX. No tokens. No real economy.")

# User select (free entry)
users = db.get("users", [])
user_ids = [u.get("user_id", "user-1") for u in users] or ["user-1"]
display_map = {u.get("user_id"): u.get("display_name", u.get("user_id")) for u in users}

active_user_id = st.sidebar.selectbox(
    "Select user (dev)",
    options=user_ids,
    index=0,
    format_func=lambda uid: f"{display_map.get(uid, uid)} ({uid})",
)

active = get_user(db, active_user_id)
if not active:
    active = default_db()["users"][0]
    active["user_id"] = active_user_id
    upsert_user(db, active)
    save_json(USERS_PATH, db)

# Fake Careon display
st.sidebar.markdown("### Balance")
st.sidebar.metric("FAKE Careon (dev)", _get_fake_balance())
st.sidebar.caption("This currency is fake and resets if you clear session.")

view = st.sidebar.radio("Navigate", ["My Starplace", "Dev Store", "Data"], index=0)

# Header
st.markdown('<div class="sp-title">⭐ STARPLACE</div>', unsafe_allow_html=True)
st.markdown('<div class="sp-sub">MySpace vibes, sandbox rules. Customize safely.</div>', unsafe_allow_html=True)

# Ticker
st.markdown(
    f'<div class="sp-ticker">✦ FAKE CAREON DEV MODE ✦ Balance: <b>{_get_fake_balance()}</b> ✦</div>',
    unsafe_allow_html=True,
)

st.write("")

# Ensure starplace exists
active.setdefault("starplace", {})
sp = active["starplace"]
sp.setdefault("quote", "")
sp.setdefault("journal", "")
sp.setdefault("theme", {"bg": "nebula_ink"})
sp.setdefault("avatar", {"icon_id": "icon_01"})
sp.setdefault("cosmetics", {"unlocked": [], "active_stickers": []})
sp.setdefault("arcade", {"played": []})

# ------------------------------------------------------------
# My Starplace
# ------------------------------------------------------------
if view == "My Starplace":
    left, right = st.columns([3, 2])

    with left:
        st.markdown('<div class="sp-module">', unsafe_allow_html=True)
        st.markdown(f'<span class="sp-badge">PROFILE: {active.get("display_name","User")}</span>', unsafe_allow_html=True)
        st.write("")

        quote = st.text_input("Quote (user-written)", value=sp.get("quote", ""), placeholder="Write something iconic...")
        journal = st.text_area("Journal (simple)", value=sp.get("journal", ""), height=160, placeholder="Notes, vibes, reflections...")

        if st.button("Save Profile", use_container_width=True):
            sp["quote"] = " ".join((quote or "").split())
            sp["journal"] = journal or ""
            active["starplace"] = sp
            upsert_user(db, active)
            save_json(USERS_PATH, db)
            st.success("Saved (DEV).")

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="sp-module">', unsafe_allow_html=True)
        st.markdown("**Arcade History (coming soon)**")
        st.caption("This will list games played + tickets earned later.")
        played = sp.get("arcade", {}).get("played", [])
        st.write(played if played else "No arcade records yet.")
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown('<div class="sp-module">', unsafe_allow_html=True)
        st.markdown("**Preview**")
        bg_id = sp.get("theme", {}).get("bg", "nebula_ink")
        bg = THEMES.get(bg_id, THEMES["nebula_ink"])
        icon_id = sp.get("avatar", {}).get("icon_id", "icon_01")

        st.write(f"Theme: `{bg.get('label')}`  |  Avatar: `{icon_id}`")
        st.markdown(f"Background swatch: **{bg.get('swatch')}**")

        st.markdown('<div class="sp-strip">', unsafe_allow_html=True)
        st.markdown("**Stickers strip (coming soon)**")
        st.caption("Retro modules + sticker packs will appear here.")
        st.markdown("</div>", unsafe_allow_html=True)

        st.write("")
        if sp.get("quote"):
            st.markdown(f"> **{sp.get('quote')}**")
        else:
            st.caption("No quote yet.")

        st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------
# Dev Store (fake purchases)
# ------------------------------------------------------------
elif view == "Dev Store":
    st.markdown('<div class="sp-module">', unsafe_allow_html=True)
    st.markdown("**Dev Store (FAKE Careon only)**")
    st.caption("Buy cosmetics in sandbox. This does not affect the real Starlight economy.")
    st.markdown("</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="sp-module">', unsafe_allow_html=True)
        st.markdown("**Background Themes**")
        theme_keys = list(THEMES.keys())
        chosen_theme = st.selectbox(
            "Choose theme",
            options=theme_keys,
            index=theme_keys.index(sp.get("theme", {}).get("bg", "nebula_ink")) if sp.get("theme") else 0,
            format_func=lambda k: f"{THEMES[k]['label']} ({THEMES[k]['swatch']})",
        )
        if st.button(f"Buy + Apply Theme ({COST_THEME} FAKE)", use_container_width=True):
            if _spend_fake(COST_THEME):
                sp["theme"]["bg"] = chosen_theme
                active["starplace"] = sp
                upsert_user(db, active)
                save_json(USERS_PATH, db)
                st.success("Theme applied (DEV).")
                st.rerun()
            else:
                st.warning("Not enough FAKE Careon.")
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="sp-module">', unsafe_allow_html=True)
        st.markdown("**Avatar Icons**")
        chosen_icon = st.selectbox("Choose icon", options=ICON_OPTIONS, index=0)
        if st.button(f"Buy + Apply Icon ({COST_ICON} FAKE)", use_container_width=True):
            if _spend_fake(COST_ICON):
                sp["avatar"]["icon_id"] = chosen_icon
                active["starplace"] = sp
                upsert_user(db, active)
                save_json(USERS_PATH, db)
                st.success("Icon applied (DEV).")
                st.rerun()
            else:
                st.warning("Not enough FAKE Careon.")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="sp-module">', unsafe_allow_html=True)
    st.markdown("**Sticker Pack (placeholder)**")
    st.caption("Unlock a sticker pack (no visuals yet).")
    if st.button(f"Buy Sticker Pack ({COST_STICKER} FAKE)", use_container_width=True):
        if _spend_fake(COST_STICKER):
            sp["cosmetics"].setdefault("unlocked", []).append(f"sticker_pack_{len(sp['cosmetics'].get('unlocked', [])) + 1}")
            active["starplace"] = sp
            upsert_user(db, active)
            save_json(USERS_PATH, db)
            st.success("Sticker pack unlocked (DEV).")
            st.rerun()
        else:
            st.warning("Not enough FAKE Careon.")
    st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------
# Data
# ------------------------------------------------------------
else:
    st.markdown('<div class="sp-module">', unsafe_allow_html=True)

st.markdown("## ⭐ Starplace DEV is live")
st.caption("If you can read this, the app UI is rendering.")
st.success("DEV sandbox loaded ✅")
st.write("Open the sidebar (top-left) to select a user + navigate.")
st.divider()
    st.markdown("**Data (DEV)**")
    st.caption("This is the sandbox user database stored in starplace_dev/state/starplace_users.json")
    st.json(db)
    st.markdown("</div>", unsafe_allow_html=True)

    st.warning("If you want a clean reset: delete starplace_dev/state/starplace_users.json")
