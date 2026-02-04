import streamlit as st

# ============================================================
# ⭐ STARPLACE DEV — SANDBOX (NO TOKENS / NO REAL ECONOMY)
# ------------------------------------------------------------
# C2 IMPLEMENTED:
# - Global soft gate (global_confirmed)
# - Theme takeover CSS ONLY after confirmation
# - Theme color affects WHOLE UI AFTER selection (via CSS variables)
#
# Updates (Feb 2026 patch):
# 1) Moon Milk + Peach Glow -> faded black text + readable panels
# 2) Peach Glow -> lighter soft blush
# 3) Sidebar -> "Go back to hub" link to Starlight Deck v3
# 4) Profiles aligned -> normalize theme keys + defaults respected
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

# ------------------------------------------------------------
# Themes (accent + background + panel tint)
# - is_light=True triggers faded black text + lighter panels
# ------------------------------------------------------------
THEMES = {
    "nebula_ink": {
        "label": "Nebula Ink",
        "swatch": "#8B5CF6",
        "bg_a": "#070A13",
        "bg_b": "#101A33",
        "panel_tint": "rgba(139, 92, 246, 0.10)",
        "is_light": False,
    },
    "moon_milk": {
        "label": "Moon Milk",
        "swatch": "#111827",
        "bg_a": "#F5F6F8",
        "bg_b": "#EDEFF3",
        "panel_tint": "rgba(17, 24, 39, 0.06)",
        "is_light": True,
    },
    "peach_glow": {
        "label": "Peach Glow",
        "swatch": "#FB7185",   # soft blush accent
        "bg_a": "#FFF1F5",     # lighter blush background
        "bg_b": "#FFE4EE",     # soft gradient
        "panel_tint": "rgba(251, 113, 133, 0.08)",
        "is_light": True,
    },
    "ocean_glass": {
        "label": "Ocean Glass",
        "swatch": "#22C55E",
        "bg_a": "#061A19",
        "bg_b": "#0D2A2A",
        "panel_tint": "rgba(120, 220, 210, 0.10)",
        "is_light": False,
    },
    "forest_hush": {
        "label": "Forest Hush",
        "swatch": "#A3E635",
        "bg_a": "#06140D",
        "bg_b": "#0B2216",
        "panel_tint": "rgba(111, 207, 151, 0.10)",
        "is_light": False,
    },
    "sunset_pulse": {
        "label": "Sunset Pulse",
        "swatch": "#F97316",
        "bg_a": "#12080A",
        "bg_b": "#2A1212",
        "panel_tint": "rgba(255, 122, 122, 0.10)",
        "is_light": False,
    },
}

AVATAR_EMOJIS = ["✨", "🕊️", "🐻‍❄️", "🦀", "🌟", "🌙", "🌈", "🪐", "🧿", "🦋", "🍀", "🧊"]


# ============================================================
# Utilities
# ============================================================

def _normalize_theme_key(k: str) -> str:
    return k if k in THEMES else "nebula_ink"


def _ss_init():
    st.session_state.setdefault("global_confirmed", False)
    st.session_state.setdefault("edit_mode", False)

    st.session_state.setdefault("FAKE_CAREON", 5000)

    st.session_state.setdefault("active_user_id", DEV_USERS[0]["user_id"])
    st.session_state.setdefault("active_user_name", DEV_USERS[0]["display_name"])

    st.session_state.setdefault("starplace_profiles", {})
    st.session_state.setdefault("dev_reset_unlocked", False)

    st.session_state.setdefault("show_debug_css", False)
    st.session_state.setdefault("last_view", "My Starplace")


def _get_dev_user(user_id: str):
    for u in DEV_USERS:
        if u["user_id"] == user_id:
            return u
    return DEV_USERS[0]


def _get_profile(user_id: str):
    profiles = st.session_state.get("starplace_profiles", {})

    if user_id in profiles:
        # normalize theme in case older session / typo
        profiles[user_id]["bg"] = _normalize_theme_key(profiles[user_id].get("bg", "nebula_ink"))
        st.session_state["starplace_profiles"] = profiles
        return profiles[user_id]

    base = _get_dev_user(user_id)
    profile = {
        "quote": base.get("default_quote", ""),
        "journal": "",
        "bg": _normalize_theme_key(base.get("default_bg", "nebula_ink")),
        "avatar": base.get("default_avatar", "✨"),
        "persona": base.get("persona", ""),
        "vibe_mode": True,
        "sparkle_fx": True,
        "soft_motion": True,
    }

    profiles[user_id] = profile
    st.session_state["starplace_profiles"] = profiles
    return profile


def _save_profile(user_id: str, profile_dict: dict):
    profiles = st.session_state.get("starplace_profiles", {})
    profile_dict["bg"] = _normalize_theme_key(profile_dict.get("bg", "nebula_ink"))
    profiles[user_id] = profile_dict
    st.session_state["starplace_profiles"] = profiles


def _reset_user_profile(user_id: str):
    profiles = st.session_state.get("starplace_profiles", {})
    if user_id in profiles:
        del profiles[user_id]
    st.session_state["starplace_profiles"] = profiles


def _reset_all_dev_data():
    keys_to_clear = [
        "FAKE_CAREON",
        "active_user_id",
        "active_user_name",
        "starplace_profiles",
        "edit_mode",
        "dev_reset_unlocked",
        "global_confirmed",
        "show_debug_css",
        "last_view",
    ]
    for k in keys_to_clear:
        if k in st.session_state:
            del st.session_state[k]


# ============================================================
# Global confirmation (C2)
# ============================================================

def _confirm_everyone():
    st.session_state["global_confirmed"] = True


def _clear_confirmation():
    st.session_state["global_confirmed"] = False


def _is_confirmed() -> bool:
    return bool(st.session_state.get("global_confirmed", False))


# ============================================================
# CSS
# ============================================================

BASE_CSS = """
<style>
:root{
  --sp-accent: #8B5CF6;
  --sp-accent-weak: rgba(139, 92, 246, 0.18);
  --sp-text: rgba(245,245,247,0.92);
  --sp-muted: rgba(245,245,247,0.70);
  --sp-border: rgba(255,255,255,0.16);
  --sp-panel: rgba(255,255,255,0.06);
  --sp-panel-2: rgba(255,255,255,0.04);
  --sp-shadow: rgba(0,0,0,0.28);
}

/* Sidebar: solid white + gray border (NO GLASS) */
section[data-testid="stSidebar"]{
  background: #ffffff !important;
  border-right: 1px solid rgba(0,0,0,0.12);
}
section[data-testid="stSidebar"] *{
  color: rgba(10,10,12,0.92) !important;
}

/* Titles */
.sp-title{
  font-weight: 950;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  font-size: 1.35rem;
  margin-bottom: 4px;
}
.sp-sub{
  color: var(--sp-muted);
  margin-bottom: 10px;
}

/* Modules */
.sp-module{
  border-radius: 18px;
  padding: 14px 16px;
  border: 1px solid var(--sp-border);
  background: var(--sp-panel);
  backdrop-filter: blur(10px);
  box-shadow: 0 10px 34px var(--sp-shadow);
  margin: 10px 0;
}

/* Ticker */
.sp-ticker{
  border-radius: 14px;
  padding: 8px 12px;
  border: 1px solid var(--sp-border);
  background: rgba(255,255,255,0.05);
}

/* Badge */
.sp-badge{
  display:inline-block;
  padding: 6px 10px;
  border-radius: 999px;
  border: 1px solid rgba(255,255,255,0.22);
  background: rgba(255,255,255,0.06);
  font-weight: 800;
  letter-spacing: 0.06em;
}

/* Accent badge */
.sp-badge-accent{
  display:inline-block;
  padding: 6px 10px;
  border-radius: 999px;
  border: 1px solid var(--sp-accent-weak);
  background: rgba(255,255,255,0.05);
  font-weight: 900;
  letter-spacing: 0.10em;
  text-transform: uppercase;
}

/* Avatar window */
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

/* Links */
a, a:visited { color: var(--sp-accent) !important; }
a:hover { opacity: 0.92; }

/* Buttons */
.stButton > button{
  border-radius: 14px !important;
  border: 1px solid rgba(255,255,255,0.22) !important;
}
.stButton > button:hover{
  border-color: var(--sp-accent-weak) !important;
}

div[data-baseweb="input"] input,
div[data-baseweb="textarea"] textarea,
div[data-baseweb="select"] > div{
  border-radius: 14px !important;
}

.block-container { padding-top: 1.2rem; }
</style>
"""

def _theme_takeover_css(theme_key: str) -> str:
    theme_key = _normalize_theme_key(theme_key)
    t = THEMES[theme_key]

    accent = t["swatch"]
    bg_a = t["bg_a"]
    bg_b = t["bg_b"]
    panel_tint = t["panel_tint"]
    is_light = bool(t.get("is_light", False))

    # Light theme readability overrides
    text_color = "rgba(10,10,12,0.86)" if is_light else "rgba(245,245,247,0.92)"
    muted_color = "rgba(10,10,12,0.62)" if is_light else "rgba(245,245,247,0.70)"
    panel_bg = "rgba(255,255,255,0.78)" if is_light else "rgba(255,255,255,0.06)"
    border = "rgba(0,0,0,0.10)" if is_light else "rgba(255,255,255,0.16)"
    shadow = "rgba(0,0,0,0.12)" if is_light else "rgba(0,0,0,0.28)"

    return f"""
<style>
:root{{
  --sp-accent: {accent};
  --sp-accent-weak: color-mix(in srgb, {accent} 18%, transparent);
  --sp-text: {text_color};
  --sp-muted: {muted_color};
  --sp-border: {border};
  --sp-panel: {panel_bg};
  --sp-shadow: {shadow};

  --sp-bg-a: {bg_a};
  --sp-bg-b: {bg_b};
  --sp-panel-tint: {panel_tint};
}}

.stApp{{
  background: linear-gradient(180deg, var(--sp-bg-a) 0%, var(--sp-bg-b) 55%, var(--sp-bg-a) 100%) !important;
  color: var(--sp-text) !important;
}}

/* MAIN CONTENT: readable (sidebar unchanged by design) */
.block-container, .block-container * {{
  color: var(--sp-text);
}}
.block-container .stCaption, .block-container small {{
  color: var(--sp-muted) !important;
}}

/* Modules adopt theme tint + readable border */
.sp-module{{
  background: linear-gradient(135deg, var(--sp-panel), var(--sp-panel-tint)) !important;
  border-color: color-mix(in srgb, var(--sp-accent) 18%, var(--sp-border)) !important;
  box-shadow: 0 10px 34px var(--sp-shadow);
}}
.sp-ticker{{
  border-color: color-mix(in srgb, var(--sp-accent) 20%, var(--sp-border)) !important;
  color: var(--sp-text) !important;
}}
.sp-badge, .sp-badge-accent {{
  color: var(--sp-text) !important;
}}

/* Buttons: accent ring */
.stButton > button{{
  background: rgba(255,255,255,0.04) !important;
  border-color: color-mix(in srgb, var(--sp-accent) 26%, var(--sp-border)) !important;
}}
.stButton > button:hover{{
  border-color: var(--sp-accent) !important;
  transform: translateY(-1px);
}}
.stButton > button:focus,
.stButton > button:active{{
  outline: none !important;
  box-shadow: 0 0 0 4px color-mix(in srgb, var(--sp-accent) 20%, transparent) !important;
}}

/* Inputs: accent ring */
div[data-baseweb="input"] input:focus,
div[data-baseweb="textarea"] textarea:focus{{
  box-shadow: 0 0 0 4px color-mix(in srgb, var(--sp-accent) 18%, transparent) !important;
  border-color: var(--sp-accent) !important;
}}
div[data-baseweb="select"] > div:focus-within{{
  box-shadow: 0 0 0 4px color-mix(in srgb, var(--sp-accent) 18%, transparent) !important;
  border-color: var(--sp-accent) !important;
}}

/* Metric values in main content */
div[data-testid="stMetricValue"]{{
  color: var(--sp-accent) !important;
  font-weight: 900 !important;
}}

/* Optional glow */
@keyframes spGlow {{
  0% {{ box-shadow: 0 0 0 0 color-mix(in srgb, var(--sp-accent) 0%, transparent); }}
  50% {{ box-shadow: 0 0 0 6px color-mix(in srgb, var(--sp-accent) 14%, transparent); }}
  100% {{ box-shadow: 0 0 0 0 color-mix(in srgb, var(--sp-accent) 0%, transparent); }}
}}
.sp-glow {{
  animation: spGlow 2.5s ease-in-out infinite;
}}
</style>
"""


# ============================================================
# App start
# ============================================================

st.set_page_config(page_title=APP_TITLE, page_icon=APP_ICON, layout="wide")
st.markdown(BASE_CSS, unsafe_allow_html=True)
_ss_init()

# ============================================================
# Sidebar
# ============================================================

st.sidebar.markdown(f"## {APP_ICON} {APP_TITLE}")
st.sidebar.caption("DEV SANDBOX — no tokens, no real economy. Session-only.")

user_labels = {u["user_id"]: u["display_name"] for u in DEV_USERS}
_user_ids = [u["user_id"] for u in DEV_USERS]

default_index = 0
if st.session_state.get("active_user_id") in _user_ids:
    default_index = _user_ids.index(st.session_state["active_user_id"])

user_choice = st.sidebar.selectbox(
    "Select a dev user",
    options=_user_ids,
    index=default_index,
    format_func=lambda uid: f"{user_labels.get(uid, uid)} ({uid})",
)

active_dev_user = _get_dev_user(user_choice)
st.session_state["active_user_id"] = active_dev_user["user_id"]
st.session_state["active_user_name"] = active_dev_user["display_name"]

st.sidebar.markdown("### Balance")
st.sidebar.metric("FAKE Careon (dev)", int(st.session_state.get("FAKE_CAREON", 5000)))
st.sidebar.caption("Fake currency. Clears if session resets.")

view = st.sidebar.radio("Navigate", ["My Starplace", "Dev Store", "Data"], index=0)
st.session_state["last_view"] = view

# ---- NEW: Back to hub (Starlight Deck v3) ----
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔗 Hub")
st.sidebar.link_button("⬅️ Go back to hub", "https://starlightdeckv3.streamlit.app", use_container_width=True)

st.sidebar.markdown("---")
st.session_state["show_debug_css"] = st.sidebar.toggle(
    "Show CSS Debug (dev)", value=bool(st.session_state.get("show_debug_css", False))
)

gate_state = "CONFIRMED" if _is_confirmed() else "LOCKED"
st.sidebar.markdown(f"**Gate:** `{gate_state}`")
if st.sidebar.button("Reset Gate (global)", use_container_width=True):
    _clear_confirmation()
    st.toast("Gate reset (global).")
    st.rerun()

# ============================================================
# Header
# ============================================================

st.markdown('<div class="sp-title">⭐ STARPLACE</div>', unsafe_allow_html=True)
st.markdown('<div class="sp-sub">MySpace vibes, sandbox rules. Customize safely.</div>', unsafe_allow_html=True)

st.markdown(
    f'<div class="sp-ticker">✦ FAKE CAREON DEV MODE ✦ Balance: <b>{int(st.session_state.get("FAKE_CAREON", 5000))}</b> ✦</div>',
    unsafe_allow_html=True,
)
st.write("")

# Pull profile early
uid = st.session_state["active_user_id"]
profile = _get_profile(uid)

# Theme takeover injection AFTER confirmation (and AFTER selection exists)
if _is_confirmed():
    selected_theme = _normalize_theme_key(profile.get("bg", "nebula_ink"))
    st.markdown(_theme_takeover_css(selected_theme), unsafe_allow_html=True)

    if st.session_state.get("show_debug_css", False):
        st.markdown(
            f"""
            <div class="sp-module">
              <div class="sp-badge-accent sp-glow">Theme Active</div>
              <div style="margin-top:10px; color: var(--sp-muted);">
                <b>theme_key</b>: <code>{selected_theme}</code><br/>
                <b>accent</b>: <code>{THEMES[selected_theme]["swatch"]}</code><br/>
                <b>is_light</b>: <code>{THEMES[selected_theme].get("is_light", False)}</code>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ============================================================
# TAB 1: My Starplace
# ============================================================

if view == "My Starplace":
    uid = st.session_state["active_user_id"]
    profile = _get_profile(uid)

    confirmed = _is_confirmed()
    edit_mode = bool(st.session_state.get("edit_mode", False))

    # Global soft gate intake
    if not confirmed:
        st.markdown('<div class="sp-module">', unsafe_allow_html=True)
        st.markdown("### ✨ Starplace Intake (Global)")
        st.caption("Confirm once to enter Starplace (this session). Pick your look first.")

        quote = st.text_input("Quote", value=profile.get("quote", ""), placeholder="Write something iconic...")

        theme_keys = list(THEMES.keys())
        current_bg = _normalize_theme_key(profile.get("bg", "nebula_ink"))

        bg_choice = st.selectbox(
            "Background theme",
            options=theme_keys,
            index=theme_keys.index(current_bg),
            format_func=lambda k: f"{THEMES[k]['label']} ({THEMES[k]['swatch']})",
        )

        avatar_choice = st.selectbox(
            "Avatar (emoji)",
            options=AVATAR_EMOJIS,
            index=AVATAR_EMOJIS.index(profile.get("avatar", "✨")) if profile.get("avatar", "✨") in AVATAR_EMOJIS else 0,
        )

        vibe_yes = st.toggle("Vibe Mode (default YES)", value=bool(profile.get("vibe_mode", True)))
        sparkle_fx = st.toggle("Sparkle FX (soft)", value=bool(profile.get("sparkle_fx", True)))
        soft_motion = st.toggle("Soft Motion (subtle)", value=bool(profile.get("soft_motion", True)))

        profile["quote"] = " ".join((quote or "").split())
        profile["bg"] = _normalize_theme_key(bg_choice)
        profile["avatar"] = avatar_choice
        profile["vibe_mode"] = bool(vibe_yes)
        profile["sparkle_fx"] = bool(sparkle_fx)
        profile["soft_motion"] = bool(soft_motion)
        _save_profile(uid, profile)

        st.markdown(
            f"""
            <div class="sp-module">
              <div class="sp-badge-accent sp-glow">PREVIEW</div>
              <div style="margin-top:10px;">
                Theme: <b>{THEMES[bg_choice]['label']}</b><br/>
                Accent: <code>{THEMES[bg_choice]['swatch']}</code><br/>
                Light-mode: <code>{THEMES[bg_choice].get("is_light", False)}</code>
              </div>
              <div style="margin-top:10px; color: rgba(245,245,247,0.72);">
                (Theme applies to the whole UI after you confirm.)
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("✅ Enter Starplace", use_container_width=True):
            _confirm_everyone()
            st.success("Confirmed. Welcome to Starplace ⭐")
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
        st.stop()

    # Confirmed view
    st.markdown('<div class="sp-module">', unsafe_allow_html=True)
    topA, topB, topC = st.columns([4, 1, 1])

    with topA:
        st.markdown(
            f'<span class="sp-badge-accent sp-glow">PROFILE</span> '
            f'<span class="sp-badge">{st.session_state["active_user_name"]}</span>',
            unsafe_allow_html=True,
        )
        st.caption(f"Persona: {profile.get('persona','')}")

    with topB:
        if st.button("✏️ Edit Profile", use_container_width=True):
            st.session_state["edit_mode"] = True
            st.rerun()

    with topC:
        if st.button("🔓 Re-lock Gate", use_container_width=True):
            _clear_confirmation()
            st.session_state["edit_mode"] = False
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # Edit drawer
    if edit_mode:
        st.markdown('<div class="sp-module">', unsafe_allow_html=True)
        st.markdown("### ✨ Edit Profile (confirmed session)")
        st.caption("Edits apply on rerun. Theme affects whole UI after Apply.")

        quote = st.text_input("Quote", value=profile.get("quote", ""))
        theme_keys = list(THEMES.keys())
        current_bg = _normalize_theme_key(profile.get("bg", "nebula_ink"))

        bg_choice = st.selectbox(
            "Background theme",
            options=theme_keys,
            index=theme_keys.index(current_bg),
            format_func=lambda k: f"{THEMES[k]['label']} ({THEMES[k]['swatch']})",
        )

        avatar_choice = st.selectbox(
            "Avatar (emoji)",
            options=AVATAR_EMOJIS,
            index=AVATAR_EMOJIS.index(profile.get("avatar", "✨")) if profile.get("avatar", "✨") in AVATAR_EMOJIS else 0,
        )

        vibe_yes = st.toggle("Vibe Mode", value=bool(profile.get("vibe_mode", True)))
        sparkle_fx = st.toggle("Sparkle FX (soft)", value=bool(profile.get("sparkle_fx", True)))
        soft_motion = st.toggle("Soft Motion (subtle)", value=bool(profile.get("soft_motion", True)))

        c1, c2 = st.columns(2)
        with c1:
            if st.button("Apply changes", use_container_width=True):
                profile["quote"] = " ".join((quote or "").split())
                profile["bg"] = _normalize_theme_key(bg_choice)
                profile["avatar"] = avatar_choice
                profile["vibe_mode"] = bool(vibe_yes)
                profile["sparkle_fx"] = bool(sparkle_fx)
                profile["soft_motion"] = bool(soft_motion)
                _save_profile(uid, profile)
                st.session_state["edit_mode"] = False
                st.rerun()

        with c2:
            if st.button("Cancel edit", use_container_width=True):
                st.session_state["edit_mode"] = False
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    # Main layout
    left, right = st.columns([3, 2])

    with left:
        st.markdown('<div class="sp-module">', unsafe_allow_html=True)
        st.markdown("### 💬 Quote")
        st.markdown(f"> **{profile.get('quote','')}**" if profile.get("quote") else "_No quote yet._")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="sp-module">', unsafe_allow_html=True)
        st.markdown("### ✍️ Journal")
        journal = st.text_area(
            "Journal (simple)",
            value=profile.get("journal", ""),
            height=180,
            placeholder="Notes, vibes, reflections...",
            label_visibility="collapsed",
        )
        cJ1, cJ2 = st.columns([1, 1])
        with cJ1:
            if st.button("Save Journal (session)", use_container_width=True):
                profile["journal"] = journal or ""
                _save_profile(uid, profile)
                st.success("Journal saved ✅")
        with cJ2:
            if st.button("Clear Journal", use_container_width=True):
                profile["journal"] = ""
                _save_profile(uid, profile)
                st.info("Cleared.")
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="sp-module">', unsafe_allow_html=True)
        st.markdown("### ⭐ Network Motto")
        st.markdown("**✨ ⭐ The network grows with you, your input grows the network ⭐ ✨**")
        st.caption("Stay tuned ⭐")
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown('<div class="sp-module">', unsafe_allow_html=True)
        st.markdown("### Avatar Window")
        st.markdown(
            f"""
            <div class="sp-avatar-window">
              <div class="sp-avatar-emoji">{profile.get("avatar","✨")}</div>
              <div class="sp-avatar-caption">confirmed session · theme affects whole UI</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

        current_theme = _normalize_theme_key(profile.get("bg", "nebula_ink"))
        t = THEMES[current_theme]

        st.markdown('<div class="sp-module">', unsafe_allow_html=True)
        st.markdown("### 🎛️ Active Theme")
        st.markdown(
            f"""
            <div style="display:flex; gap:10px; align-items:center; margin-top:6px;">
              <div style="width:18px; height:18px; border-radius:7px; background:{t['swatch']};
                          box-shadow:0 0 0 4px color-mix(in srgb, {t['swatch']} 22%, transparent);"></div>
              <div style="font-weight:900;">{t['label']}</div>
            </div>
            <div style="margin-top:8px; color: var(--sp-muted);">
              Accent: <code>{t['swatch']}</code><br/>
              Light-mode: <code>{t.get("is_light", False)}</code>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# TAB 2: Dev Store
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
        st.caption("Coming soon: unlock theme changes with FAKE Careon (not in dev).")
        st.button("Buy (placeholder)", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="sp-module">', unsafe_allow_html=True)
        st.markdown("**Icon Pack**")
        st.caption("Coming soon: unlock icon changes with FAKE Careon (not in dev).")
        st.button("Buy (placeholder)", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c3:
        st.markdown('<div class="sp-module">', unsafe_allow_html=True)
        st.markdown("**Sticker Pack**")
        st.caption("Coming soon: sticker strip visuals + placements.")
        st.button("Buy (placeholder)", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# TAB 3: Data
# ============================================================
else:
    st.markdown('<div class="sp-module">', unsafe_allow_html=True)
    st.markdown("**Data (DEV)**")
    st.caption("Session snapshot only. No JSON persistence in this build.")
    st.markdown("</div>", unsafe_allow_html=True)

    uid = st.session_state["active_user_id"]
    snap_profile = _get_profile(uid)

    st.markdown('<div class="sp-module">', unsafe_allow_html=True)
    st.markdown("**Current user snapshot**")
    st.json(
        {
            "active_user_id": uid,
            "active_user_name": st.session_state.get("active_user_name"),
            "profile_session": snap_profile,
            "fake_careon": int(st.session_state.get("FAKE_CAREON", 5000)),
            "global_confirmed": bool(st.session_state.get("global_confirmed", False)),
            "edit_mode": bool(st.session_state.get("edit_mode", False)),
            "theme_key_active_user": snap_profile.get("bg", "nebula_ink"),
        }
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="sp-module">', unsafe_allow_html=True)
    st.markdown("**Reset User (session)**")
    st.caption("Resets this user's profile AND re-locks the global gate.")
    if st.button("Reset THIS user", use_container_width=True):
        _reset_user_profile(uid)
        _clear_confirmation()
        st.session_state["edit_mode"] = False
        st.success("User reset ✅ (and gate reset)")
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

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

