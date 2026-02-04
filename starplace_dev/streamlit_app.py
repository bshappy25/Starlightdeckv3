import streamlit as st

# ============================================================
# ⭐ STARPLACE DEV — SANDBOX (NO TOKENS / NO REAL ECONOMY)
# ------------------------------------------------------------
# S1: Separate from Starlight economy (YES)  ✅
# S2: 5 preassigned whimsical users (YES)   ✅
# S3: 5000 FAKE Careon per session (YES)    ✅
# S4: No persistence (session only) (YES)   ✅
# S5: Store = preview only (YES)            ✅
# S6: 3 tabs (YES)                          ✅
# S7: Reset user button (YES)               ✅
# S8: Reset dev data w/ "RESET" guard (YES) ✅
# S9: Emoji avatars in black window (YES)   ✅
# S10: Styling scheme (YES)                 ✅
# ============================================================

APP_TITLE = "Starplace (DEV)"
APP_ICON = "⭐"

# ------------------------------------------------------------
# Preassigned whimsical users (stored in app)
# ------------------------------------------------------------
DEV_USERS = [
    {
        "user_id": "sp-01",
        "display_name": "Estrella Echo",
        "persona": "cosmic dealer energy",
        "default_quote": "The network grows with you.",
        "default_bg": "nebula_ink",
        "default_avatar": "✨",
    },
    {
        "user_id": "sp-02",
        "display_name": "Captain Pigeon",
        "persona": "whimsical explorer",
        "default_quote": "I travel light. I collect meaning.",
        "default_bg": "ocean_glass",
        "default_avatar": "🕊️",
    },
    {
        "user_id": "sp-03",
        "display_name": "Polly Polar",
        "persona": "cozy guardian",
        "default_quote": "Soft pace. Strong boundaries.",
        "default_bg": "moon_milk",
        "default_avatar": "🐻‍❄️",
    },
    {
        "user_id": "sp-04",
        "display_name": "Billy Blue Crab",
        "persona": "comic relief + truth",
        "default_quote": "Side-step the chaos. Snap to the plan.",
        "default_bg": "forest_hush",
        "default_avatar": "🦀",
    },
    {
        "user_id": "sp-05",
        "display_name": "Mr. Benji Idol",
        "persona": "shiny mascot",
        "default_quote": "Show up bright. Keep it simple.",
        "default_bg": "sunset_pulse",
        "default_avatar": "🌟",
    },
]

# Background theme options (purely visual; session-only)
THEMES = {
    "nebula_ink": {"label": "Nebula Ink", "swatch": "#0b1020"},
    "moon_milk": {"label": "Moon Milk", "swatch": "#f6f6f7"},
    "peach_glow": {"label": "Peach Glow", "swatch": "#ffcfb3"},
    "ocean_glass": {"label": "Ocean Glass", "swatch": "#78dcd2"},
    "forest_hush": {"label": "Forest Hush", "swatch": "#6fcf97"},
    "sunset_pulse": {"label": "Sunset Pulse", "swatch": "#ff7a7a"},
}

# Emoji avatars displayed inside a black window (S9)
AVATAR_EMOJIS = ["✨", "🕊️", "🐻‍❄️", "🦀", "🌟", "🌙", "🌈", "🪐", "🧿", "🦋", "🍀", "🧊"]

# ------------------------------------------------------------
# Session utilities
# ------------------------------------------------------------
def _ss_init():
    st.session_state.setdefault("FAKE_CAREON", 5000)
    st.session_state.setdefault("active_user_id", DEV_USERS[0]["user_id"])
    st.session_state.setdefault("active_user_name", DEV_USERS[0]["display_name"])
    st.session_state.setdefault("starplace_profiles", {})  # keyed by user_id
    st.session_state.setdefault("dev_reset_unlocked", False)


def _get_dev_user(user_id: str):
    for u in DEV_USERS:
        if u["user_id"] == user_id:
            return u
    return DEV_USERS[0]


def _get_profile(user_id: str):
    """
    Returns session-only profile dict for the given user_id.
    Creates it on demand from the user's defaults.
    """
    profiles = st.session_state.get("starplace_profiles", {})
    if user_id in profiles:
        return profiles[user_id]

    base = _get_dev_user(user_id)
    profile = {
        "quote": base.get("default_quote", ""),
        "journal": "",
        "bg": base.get("default_bg", "nebula_ink"),
        "avatar": base.get("default_avatar", "✨"),
        "persona": base.get("persona", ""),
    }
    profiles[user_id] = profile
    st.session_state["starplace_profiles"] = profiles
    return profile


def _reset_user_profile(user_id: str):
    profiles = st.session_state.get("starplace_profiles", {})
    if user_id in profiles:
        del profiles[user_id]
    st.session_state["starplace_profiles"] = profiles


def _reset_all_dev_data():
    # Full wipe: resets everything to defaults
    keys_to_clear = [
        "FAKE_CAREON",
        "active_user_id",
        "active_user_name",
        "starplace_profiles",
        "dev_reset_unlocked",
    ]
    for k in keys_to_clear:
        if k in st.session_state:
            del st.session_state[k]


# ------------------------------------------------------------
# DESIGN / CSS (S10)
# ------------------------------------------------------------
CUSTOM_CSS = """
<style>
/* ===== Main background (dark gradient) ===== */
.stApp{
  background: linear-gradient(180deg, #0b1020 0%, #121a33 55%, #0b1020 100%);
  color: rgba(245,245,247,0.92);
}

/* ===== Sidebar: solid white + gray border (NO GLASS) ===== */
section[data-testid="stSidebar"]{
  background: #ffffff !important;
  border-right: 1px solid rgba(0,0,0,0.12);
}
section[data-testid="stSidebar"] *{
  color: rgba(10,10,12,0.92) !important;
}

/* ===== Titles / headings ===== */
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

/* ===== Glassy modules (calm) ===== */
.sp-module{
  border-radius: 18px;
  padding: 14px 16px;
  border: 1px solid rgba(255,255,255,0.18);
  background: rgba(255,255,255,0.06);
  backdrop-filter: blur(10px);
  box-shadow: 0 10px 34px rgba(0,0,0,0.28);
  margin: 10px 0;
}

/* ===== Ticker (calm) ===== */
.sp-ticker{
  border-radius: 14px;
  padding: 8px 12px;
  border: 1px solid rgba(255,255,255,0.16);
  background: rgba(255,255,255,0.05);
}

/* ===== Badge ===== */
.sp-badge{
  display:inline-block;
  padding: 6px 10px;
  border-radius: 999px;
  border: 1px solid rgba(255,255,255,0.22);
  background: rgba(255,255,255,0.06);
  font-weight: 800;
  letter-spacing: 0.06em;
}

/* ===== Avatar window (S9): black window with emoji ===== */
.sp-avatar-window{
  width: 100%;
  border-radius: 14px;
  padding: 18px 14px;
  background: rgba(0,0,0,0.82);
  border: 1px solid rgba(255,255,255,0.10);
  box-shadow: 0 10px 28px rgba(0,0,0,0.35);
  text-align: center;
}
.sp-avatar-emoji{
  font-size: 3.2rem;
  line-height: 1;
  margin-bottom: 10px;
}
.sp-avatar-caption{
  color: rgba(245,245,247,0.70);
  font-size: 0.9rem;
}

/* ===== Theme swatch ===== */
.sp-swatch{
  border-radius: 12px;
  padding: 12px;
  border: 1px solid rgba(255,255,255,0.14);
  background: rgba(255,255,255,0.04);
}

</style>
"""

# ------------------------------------------------------------
# App
# ------------------------------------------------------------
st.set_page_config(page_title=APP_TITLE, page_icon=APP_ICON, layout="wide")
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
_ss_init()

# Sidebar
st.sidebar.markdown(f"## {APP_ICON} {APP_TITLE}")
st.sidebar.caption("DEV SANDBOX — no tokens, no real economy. Session-only.")

user_labels = {u["user_id"]: u["display_name"] for u in DEV_USERS}
user_choice = st.sidebar.selectbox(
    "Select a dev user",
    options=[u["user_id"] for u in DEV_USERS],
    index=[u["user_id"] for u in DEV_USERS].index(st.session_state["active_user_id"])
    if st.session_state.get("active_user_id") in user_labels
    else 0,
    format_func=lambda uid: f"{user_labels.get(uid, uid)} ({uid})",
)

active_dev_user = _get_dev_user(user_choice)
st.session_state["active_user_id"] = active_dev_user["user_id"]
st.session_state["active_user_name"] = active_dev_user["display_name"]

# Fake currency (S3)
st.sidebar.markdown("### Balance")
st.sidebar.metric("FAKE Careon (dev)", int(st.session_state.get("FAKE_CAREON", 5000)))
st.sidebar.caption("Fake currency. Clears if session resets.")

view = st.sidebar.radio("Navigate", ["My Starplace", "Dev Store", "Data"], index=0)

# Header
st.markdown('<div class="sp-title">⭐ STARPLACE</div>', unsafe_allow_html=True)
st.markdown('<div class="sp-sub">MySpace vibes, sandbox rules. Customize safely.</div>', unsafe_allow_html=True)

# Global ticker
st.markdown(
    f'<div class="sp-ticker">✦ FAKE CAREON DEV MODE ✦ Balance: <b>{int(st.session_state.get("FAKE_CAREON", 5000))}</b> ✦</div>',
    unsafe_allow_html=True,
)
st.write("")

# Pull profile (session-only)
uid = st.session_state["active_user_id"]
profile = _get_profile(uid)

# ============================================================
# TAB 1: My Starplace
# ============================================================
if view == "My Starplace":
    left, right = st.columns([3, 2])

    with left:
        st.markdown('<div class="sp-module">', unsafe_allow_html=True)
        st.markdown(
            f'<span class="sp-badge">PROFILE: {st.session_state["active_user_name"]}</span>',
            unsafe_allow_html=True,
        )
        st.caption(f"Persona: {profile.get('persona','')}")

        quote = st.text_input(
            "Quote (user-written)",
            value=profile.get("quote", ""),
            placeholder="Write something iconic...",
        )
        journal = st.text_area(
            "Journal (simple)",
            value=profile.get("journal", ""),
            height=160,
            placeholder="Notes, vibes, reflections...",
        )

        # Session-only save
        if st.button("Save (session)", use_container_width=True):
            profile["quote"] = " ".join((quote or "").split())
            profile["journal"] = journal or ""
            st.success("Saved to session ✅")

        st.markdown("</div>", unsafe_allow_html=True)

        # Calm success ticker (your requested message)
        # Always visible so users feel guided (mobile-safe)
        st.markdown('<div class="sp-module">', unsafe_allow_html=True)
        st.markdown("**✨ ⭐ The network grows with you, your input grows the network ⭐ ✨**")
        st.caption("Stay tuned ⭐")
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown('<div class="sp-module">', unsafe_allow_html=True)
        st.markdown("**Preview**")

        # Theme selection (session-only)
        theme_keys = list(THEMES.keys())
        current_bg = profile.get("bg", "nebula_ink")
        if current_bg not in THEMES:
            current_bg = "nebula_ink"

        bg_choice = st.selectbox(
            "Background theme (dev)",
            options=theme_keys,
            index=theme_keys.index(current_bg),
            format_func=lambda k: f"{THEMES[k]['label']} ({THEMES[k]['swatch']})",
        )
        profile["bg"] = bg_choice

        # Avatar selection (emoji window)
        avatar_choice = st.selectbox(
            "Avatar (emoji)",
            options=AVATAR_EMOJIS,
            index=AVATAR_EMOJIS.index(profile.get("avatar", "✨"))
            if profile.get("avatar", "✨") in AVATAR_EMOJIS
            else 0,
        )
        profile["avatar"] = avatar_choice

        # Black avatar window
        st.markdown(
            f"""
            <div class="sp-avatar-window">
              <div class="sp-avatar-emoji">{profile.get("avatar","✨")}</div>
              <div class="sp-avatar-caption">avatar window (dev)</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Theme swatch preview
        swatch = THEMES.get(profile["bg"], THEMES["nebula_ink"])["swatch"]
        st.markdown(
            f"""
            <div class="sp-swatch">
              <div style="font-weight:800; letter-spacing:0.06em;">Theme swatch</div>
              <div style="margin-top:8px; height:48px; border-radius:10px; background:{swatch}; border:1px solid rgba(0,0,0,0.10);"></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write("")
        if profile.get("quote"):
            st.markdown(f"> **{profile.get('quote')}**")
        else:
            st.caption("No quote yet.")

        st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# TAB 2: Dev Store (preview only, no spending)
# ============================================================
elif view == "Dev Store":
    st.markdown('<div class="sp-module">', unsafe_allow_html=True)
    st.markdown("**Dev Store (Preview Only)**")
    st.caption("Buttons are placeholders. No spending, no unlocks, no persistence (by design).")
    st.markdown("</div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown('<div class="sp-module">', unsafe_allow_html=True)
        st.markdown("**Themes Pack**")
        st.caption("Coming soon: unlock theme changes with FAKE Careon.")
        st.button("Buy (placeholder)", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="sp-module">', unsafe_allow_html=True)
        st.markdown("**Icon Pack**")
        st.caption("Coming soon: unlock icon changes with FAKE Careon.")
        st.button("Buy (placeholder)", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c3:
        st.markdown('<div class="sp-module">', unsafe_allow_html=True)
        st.markdown("**Sticker Pack**")
        st.caption("Coming soon: sticker strip visuals + placements.")
        st.button("Buy (placeholder)", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="sp-module">', unsafe_allow_html=True)
    st.markdown("**Arcade Panel (placeholder)**")
    st.caption("Later: show which terminal games were played and tickets earned.")
    st.info("Arcade system not connected in Starplace-dev.")
    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# TAB 3: Data (session snapshot + resets)
# ============================================================
else:
    st.markdown('<div class="sp-module">', unsafe_allow_html=True)
    st.markdown("**Data (DEV)**")
    st.caption("Session snapshot only. No JSON persistence in this build (S4-C).")
    st.markdown("</div>", unsafe_allow_html=True)

    # Snapshot for current user
    st.markdown('<div class="sp-module">', unsafe_allow_html=True)
    st.markdown("**Current user snapshot**")
    st.json(
        {
            "active_user_id": uid,
            "active_user_name": st.session_state.get("active_user_name"),
            "profile_session": _get_profile(uid),
            "fake_careon": int(st.session_state.get("FAKE_CAREON", 5000)),
        }
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # Reset user button (S7)
    st.markdown('<div class="sp-module">', unsafe_allow_html=True)
    st.markdown("**Reset User (session)**")
    st.caption("Resets this user's quote/journal/theme/avatar back to defaults.")
    if st.button("Reset THIS user", use_container_width=True):
        _reset_user_profile(uid)
        st.success("User reset ✅")
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # Reset all dev data (S8) with RESET guard
    st.markdown('<div class="sp-module">', unsafe_allow_html=True)
    st.markdown("**Reset DEV DATA (all users)**")
    st.caption('Type RESET to unlock full wipe for this session.')
    reset_word = st.text_input("Type RESET to unlock", value="", placeholder="RESET")
    if reset_word.strip().upper() == "RESET":
        st.session_state["dev_reset_unlocked"] = True

    if not st.session_state.get("dev_reset_unlocked", False):
        st.info("Resets are locked until you type RESET.")
    else:
        st.warning("Unlocked. This will wipe the whole dev session state.")
        if st.button("WIPE ALL DEV DATA NOW", use_container_width=True):
            _reset_all_dev_data()
            st.success("Dev session wiped ✅")
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)