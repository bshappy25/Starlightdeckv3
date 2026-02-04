# -*- coding: utf-8 -*-

# ================================
# Starlight Deck — Main App (v3+)
# HUB + STARPLACE MERGE (single file)
# ================================

import json
import os
from datetime import datetime, timezone

import streamlit as st

# Local modules (must exist in repo root)
import careon_bubble
import careon_market
import careon_bubble_ticker


# ============================================================
# App constants
# ============================================================
APP_DIR = os.path.dirname(__file__)

# NOTE: Your repo image earlier suggested you may have careon_bank.json
# If your repo file is actually careon_bank.json, change this to "careon_bank.json".
BANK_PATH = os.path.join(APP_DIR, "careon_bank_v2.json")
CODES_PATH = os.path.join(APP_DIR, "codes_ledger.json")
USERS_PATH = os.path.join(APP_DIR, "user_profile.json")

RULES_MD = os.path.join(APP_DIR, "rules.md")
CURRENCY_MD = os.path.join(APP_DIR, "currency.md")
USERS_MD = os.path.join(APP_DIR, "users.md")

APP_TITLE = "Starlight Deck"
APP_ICON = "🎴"

HUB_URL = "https://starlightdeckv3.streamlit.app"  # requested link button


# ============================================================
# PAGE CONFIG MUST BE FIRST
# ============================================================
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="collapsed",  # mobile-friendly default
)


# ============================================================
# 🎨 HUB DESIGN / CSS ZONE — SAFE TO EDIT (your original block)
# ============================================================
THEME = {
    "bg_top": "#111a33",
    "bg_bottom": "#0b1020",
    "panel": "rgba(255,255,255,0.06)",
    "panel2": "rgba(255,255,255,0.09)",
    "text_main": "rgba(245,245,247,0.92)",
    "muted_main": "rgba(245,245,247,0.65)",
    "gold": "#ffd27a",
    "violet": "#b482ff",
    "teal": "#78dcd2",
    "glow": "0.10",
    "sparkle": "0.05",
    "blur": "14px",
    "radius": "18px",
    "title_weight": "900",
    "title_spacing": "0.06em",
}

CUSTOM_CSS = f"""
<style>
:root {{
  --bg-top: {THEME["bg_top"]};
  --bg-bottom: {THEME["bg_bottom"]};
  --panel: {THEME["panel"]};
  --panel2: {THEME["panel2"]};
  --text-main: {THEME["text_main"]};
  --muted-main: {THEME["muted_main"]};
  --gold: {THEME["gold"]};
  --violet: {THEME["violet"]};
  --teal: {THEME["teal"]};
  --glow: {THEME["glow"]};
  --sparkle: {THEME["sparkle"]};
  --blur: {THEME["blur"]};
  --radius: {THEME["radius"]};
  --title-weight: {THEME["title_weight"]};
  --title-spacing: {THEME["title_spacing"]};
}}

.stApp {{
  background:
    radial-gradient(circle at 20% 15%,
      rgba(180,130,255, calc(var(--sparkle))) 0%,
      transparent 42%),
    radial-gradient(circle at 85% 25%,
      rgba(120,220,210, calc(var(--sparkle))) 0%,
      transparent 42%),
    linear-gradient(180deg,
      var(--bg-top) 0%,
      var(--bg-bottom) 70%);
  color: var(--text-main);
}}

[data-testid="stSidebar"] {{
  background: #ffffff !important;
  border-right: 1px solid rgba(0,0,0,0.18) !important;
  box-shadow: none !important;
}}
[data-testid="stSidebar"] * {{
  color: rgba(15,18,25,0.95) !important;
}}
[data-testid="stSidebar"] input,
[data-testid="stSidebar"] textarea,
[data-testid="stSidebar"] select {{
  background: #ffffff !important;
  border: 1px solid rgba(0,0,0,0.18) !important;
  border-radius: 12px !important;
}}

.sld-glass {{
  border-radius: var(--radius);
  padding: 14px 16px;
  border: 1px solid rgba(255,255,255,0.18);
  background: linear-gradient(135deg,
      rgba(255,255,255,0.08) 0%,
      rgba(180,130,255,0.06) 55%,
      rgba(120,220,210,0.05) 100%);
  backdrop-filter: blur(var(--blur));
  box-shadow:
      0 10px 40px rgba(0,0,0,0.25),
      0 0 24px rgba(255,210,122, calc(var(--glow)));
  position: relative;
  overflow: hidden;
}}

.sld-glass::before {{
  content:'';
  position:absolute;
  top:-60%;
  left:-60%;
  width:220%;
  height:220%;
  background: radial-gradient(circle,
      rgba(255,210,122, calc(var(--sparkle))) 0%,
      transparent 58%);
  animation: sldGlow 28s linear infinite;
  pointer-events:none;
}}

@keyframes sldGlow {{
  from {{ transform: rotate(0deg); }}
  to   {{ transform: rotate(360deg); }}
}}

.sld-title {{
  font-weight: var(--title-weight);
  letter-spacing: var(--title-spacing);
  color: var(--text-main);
  position: relative;
  display: inline-block;
  padding-bottom: 6px;
}}
.sld-title::after {{
  content: "";
  position: absolute;
  left: 0;
  bottom: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, var(--gold), transparent);
}}

.sld-muted {{
  color: var(--muted-main);
}}

.stButton > button {{
  border-radius: 12px !important;
}}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ============================================================
# STARPLACE ACCESS (Hub-controlled)
# ============================================================

STARPLACE_COST = 1200

def has_starplace_access(users_db: dict, user_id: str) -> bool:
    u = get_user_record(users_db, user_id) or {}
    claims = u.get("claims", {}) or {}
    return bool(claims.get("starplace_access", False))

def grant_starplace_access(users_db: dict, user_id: str):
    # Mutates users_db in-place
    for u in users_db.get("users", []):
        if u.get("user_id") == user_id:
            u.setdefault("claims", {})
            u["claims"]["starplace_access"] = True
            users_db.setdefault("meta", {})
            users_db["meta"]["updated_at"] = _now_iso()
            return




# ============================================================
# CORE UTILITIES (your original logic)
# ============================================================

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def save_json(path: str, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_json_safe(path: str, default):
    try:
        if not os.path.exists(path):
            save_json(path, default)
            return default
        with open(path, "r", encoding="utf-8") as f:
            raw = f.read().strip()
        if not raw:
            save_json(path, default)
            return default
        return json.loads(raw)
    except Exception:
        st.session_state.setdefault("_json_warnings", set()).add(path)
        return default


def load_text_safe(path: str):
    try:
        if not os.path.exists(path):
            return None
        with open(path, "r", encoding="utf-8") as f:
            txt = f.read().strip()
        return txt if txt else None
    except Exception:
        return None


def default_bank():
    return {
        "balance": 0,
        "sld_network_fund": 0,
        "total_earned": 0,
        "total_spent": 0,
        "balances_by_user": {},
        "txs": [],
        "meta": {"version": "v3", "updated_at": _now_iso()},
    }


def default_codes():
    return {"codes": [], "meta": {"version": "v3", "updated_at": _now_iso()}}


def default_users():
    return {
        "users": [
            {
                "user_id": "bshapp",
                "display_name": "bshapp",
                "vibe": "Admin",
                "title": "Founder",
                "role": "admin",
                "created_at": _now_iso(),
                "claims": {"admin_auto": True, "intro_access": True, "all_access": True},
            }
        ],
        "meta": {"version": "v3", "updated_at": _now_iso()},
    }


def ensure_user_balances(bank: dict):
    bank.setdefault("balances_by_user", {})
    if bank["balances_by_user"] is None:
        bank["balances_by_user"] = {}


def get_user_balance(bank: dict, user_id: str) -> int:
    ensure_user_balances(bank)
    return int(bank["balances_by_user"].get(user_id, 0))


def set_user_balance(bank: dict, user_id: str, value: int):
    ensure_user_balances(bank)
    bank["balances_by_user"][user_id] = int(value)


def rebuild_user_balances_from_txs(bank: dict):
    ensure_user_balances(bank)
    balances = {}
    for t in reversed(bank.get("txs", [])):
        uid = t.get("user_id") or "user-1"
        amt = int(t.get("amount", 0))
        typ = t.get("type")
        bal = int(balances.get(uid, 0))
        if typ == "deposit":
            bal += amt
        elif typ == "spend":
            bal = max(0, bal - amt)
        balances[uid] = bal
    bank["balances_by_user"] = balances
    bank.setdefault("meta", {})["updated_at"] = _now_iso()


def record_tx(bank: dict, user_id: str, tx_type: str, amount: int, description: str):
    tx = {
        "ts": _now_iso(),
        "user_id": user_id,
        "type": tx_type,
        "amount": int(amount),
        "description": description.strip() if description else "",
    }
    bank.setdefault("txs", []).insert(0, tx)
    bank.setdefault("meta", {})["updated_at"] = _now_iso()
    return tx


def deposit(bank: dict, user_id: str, amount: int, description: str = ""):
    amount = int(amount)
    if amount <= 0:
        raise ValueError("Deposit amount must be greater than 0.")
    bank["balance"] = int(bank.get("balance", 0)) + amount
    set_user_balance(bank, user_id, get_user_balance(bank, user_id) + amount)
    bank["total_earned"] = int(bank.get("total_earned", 0)) + amount
    return record_tx(bank, user_id, "deposit", amount, description)


def spend(bank: dict, user_id: str, amount: int, description: str = ""):
    amount = int(amount)
    if amount <= 0:
        raise ValueError("Spend amount must be greater than 0.")
    personal = get_user_balance(bank, user_id)
    if amount > personal:
        raise ValueError(f"Insufficient personal balance. You have {personal}, tried to spend {amount}.")
    set_user_balance(bank, user_id, personal - amount)
    bank["balance"] = int(bank.get("balance", 0)) + amount
    bank["total_spent"] = int(bank.get("total_spent", 0)) + amount
    return record_tx(bank, user_id, "spend", amount, description)


def recent_txs(bank: dict, n: int = 10, user_id: str | None = None):
    txs = bank.get("txs", [])
    if user_id:
        txs = [t for t in txs if t.get("user_id") == user_id]
    return txs[: max(0, int(n))]


def find_code(ledger: dict, code: str):
    for row in ledger.get("codes", []):
        if row.get("code") == code:
            return row
    return None


def next_user_id(users_db: dict) -> str:
    existing = {u.get("user_id") for u in users_db.get("users", [])}
    i = 1
    while True:
        uid = f"user-{i}"
        if uid not in existing:
            return uid
        i += 1


def create_user(users_db: dict, display_name: str, vibe: str, title: str, role: str = "player"):
    uid = next_user_id(users_db)
    user = {
        "user_id": uid,
        "display_name": display_name.strip(),
        "vibe": vibe.strip(),
        "title": title,
        "role": role,
        "created_at": _now_iso(),
        "claims": {"sign_on_bonus": True},
        # Starplace fields live INSIDE each user record (single JSON)
        "starplace": {
            "confirmed": False,
            "theme_key": "nebula_ink",
            "avatar": "✨",
            "quote": "",
        },
    }
    users_db["users"].append(user)
    users_db.setdefault("meta", {})["updated_at"] = _now_iso()
    return user


def get_user_record(users_db: dict, user_id: str) -> dict:
    for u in users_db.get("users", []):
        if u.get("user_id") == user_id:
            return u
    return {}


def _ensure_admin_user(users_db: dict):
    users_db.setdefault("users", [])
    users_db.setdefault("meta", {})
    for u in users_db["users"]:
        if u.get("user_id") == "bshapp":
            return
    users_db["users"].insert(
        0,
        {
            "user_id": "bshapp",
            "display_name": "bshapp",
            "vibe": "Admin",
            "title": "Founder",
            "role": "admin",
            "created_at": _now_iso(),
            "claims": {"admin_auto": True, "intro_access": True, "all_access": True},
            "starplace": {"confirmed": True, "theme_key": "nebula_ink", "avatar": "✨", "quote": ""},
        },
    )
    users_db["meta"]["updated_at"] = _now_iso()
    save_json(USERS_PATH, users_db)


def admin_unlocked(active_user_id: str) -> bool:
    if active_user_id == "bshapp" and st.session_state.get("admin_view_as_player", False):
        return False
    if active_user_id == "bshapp":
        return True
    return bool(st.session_state.get("admin_ok", False))


# ============================================================
# CARD VIEWER HELPER (your original helper)
# ============================================================
def _safe_join_app_path(app_dir: str, rel_path: str | None) -> str | None:
    if not rel_path:
        return None
    rel_path = str(rel_path).lstrip("/").strip()
    if not rel_path:
        return None
    return os.path.join(app_dir, rel_path)


def render_card_tile(
    name: str,
    image_path: str | None,
    *,
    subtitle: str | None = None,
    placeholder_color: str = "#8EC5FF",
    placeholder_label: str | None = None,
    height_px: int = 320,
):
    full_path = _safe_join_app_path(APP_DIR, image_path)
    exists = bool(full_path and os.path.exists(full_path))

    with st.container():
        if exists:
            st.image(full_path, use_container_width=True)
        else:
            label = placeholder_label if placeholder_label is not None else (name or "CARD")
            html = (
                '<div style="'
                'width:100%;'
                f'height:{int(height_px)}px;'
                'border-radius:14px;'
                f'background:{placeholder_color};'
                'display:flex;'
                'align-items:center;'
                'justify-content:center;'
                'text-align:center;'
                'padding:12px;'
                'font-weight:900;'
                'letter-spacing:0.10em;'
                'color:rgba(0,0,0,0.78);'
                'white-space:pre-line;'
                'box-shadow:0 6px 18px rgba(0,0,0,0.18);'
                '">'
                f'{str(label)}'
                "</div>"
            )
            st.markdown(html, unsafe_allow_html=True)

        st.markdown(f"**{name or 'Unnamed Card'}**")
        if subtitle:
            st.caption(subtitle)


# ============================================================
# LOAD JSON
# ============================================================
bank = load_json_safe(BANK_PATH, default_bank())
ledger = load_json_safe(CODES_PATH, default_codes())
users_db = load_json_safe(USERS_PATH, default_users())

json_warnings = st.session_state.get("_json_warnings", set())
if json_warnings:
    st.warning(
        "One or more JSON files could not be parsed. Running with safe defaults.\n\n- "
        + "\n- ".join(sorted(json_warnings))
    )

try:
    _ensure_admin_user(users_db)
except Exception as e:
    st.warning(f"Admin bootstrap skipped: {e}")

ensure_user_balances(bank)
if not bank.get("balances_by_user"):
    rebuild_user_balances_from_txs(bank)
    save_json(BANK_PATH, bank)


# ============================================================
# ENTRY GATE (your original logic, just placed after config/css)
# ============================================================
st.session_state.setdefault("entry_ok", False)
st.session_state.setdefault("active_user_id", None)
st.session_state.setdefault("entry_success", False)

if not st.session_state["entry_ok"]:
    st.title("✨ Welcome to Starlight Deck")
    st.caption("Enter your access token to join the network.")

    with st.form("entry_gate"):
        token = st.text_input("A) Access Token", placeholder="FRONTIER-XXXX (or your token)")
        display_name = st.text_input("B) Username", placeholder="Pick a name (3+ chars)")
        vibe_yes = st.toggle("C) Vibe Mode (default YES)", value=True)
        submit = st.form_submit_button("Enter")

    if submit:
        token = (token or "").strip()
        display_name = " ".join((display_name or "").split()).strip()

        if len(display_name) < 3:
            st.info("Username must be at least 3 characters.")
            st.stop()

        # Admin override
        if display_name.lower() == "bshapp":
            st.session_state["entry_ok"] = True
            st.session_state["active_user_id"] = "bshapp"
            st.session_state["entry_success"] = True
            st.success("Admin override accepted. Stay tuned ⭐")
            st.rerun()

        if not token:
            st.info("Please enter an access token.")
            st.stop()

        row = find_code(ledger, token)
        if not row or row.get("status") != "new":
            st.info("Token not recognized (or already used).")
            st.stop()

        existing = {u.get("display_name", "").strip().lower() for u in users_db.get("users", [])}
        if display_name.lower() in existing:
            st.info("That username is taken. Try adding a number.")
            st.stop()

        package = row.get("package", {}) or {}
        title = package.get("title", "Frontier")
        bonus = int(package.get("sign_on_bonus", 500))
        vibe = "Vibe: ON" if vibe_yes else "Vibe: OFF"

        new_user = create_user(users_db, display_name=display_name, vibe=vibe, title=title, role="player")

        row["status"] = "used"
        row["used_by"] = new_user["user_id"]
        row["used_at"] = _now_iso()
        ledger.setdefault("meta", {})["updated_at"] = _now_iso()

        deposit(bank, new_user["user_id"], bonus, description=f"Sign-on bonus ({title})")

        save_json(USERS_PATH, users_db)
        save_json(CODES_PATH, ledger)
        save_json(BANK_PATH, bank)

        st.session_state["entry_ok"] = True
        st.session_state["active_user_id"] = new_user["user_id"]
        st.session_state["entry_success"] = True
        st.success("Success. Stay tuned ⭐")
        st.rerun()

    st.stop()


# ============================================================
# SIDEBAR: identity + nav + quick redeem + hub link
# ============================================================
st.sidebar.markdown(f"## {APP_ICON} {APP_TITLE}")

user_ids = [u.get("user_id", "user-1") for u in users_db.get("users", [])] or ["user-1"]
display_map = {u.get("user_id"): u.get("display_name", u.get("user_id")) for u in users_db.get("users", [])}

active_user = st.session_state.get("active_user_id") or "bshapp"

# Admin "view as player"
st.session_state.setdefault("admin_view_as_player", False)
if active_user == "bshapp":
    st.sidebar.markdown("### ⭐ Admin View")
    st.session_state["admin_view_as_player"] = st.sidebar.toggle(
        "⭐ View as Player",
        value=st.session_state["admin_view_as_player"],
        help="Hide admin-only pages to preview what normal users see.",
    )

# Sidebar status
st.sidebar.markdown("### Status")
st.sidebar.metric("Global Balance", int(bank.get("balance", 0)))
st.sidebar.metric("🌍 SLD Network Fund", int(bank.get("sld_network_fund", 0)))
st.sidebar.metric("My Balance", get_user_balance(bank, active_user))
st.sidebar.caption(f"Signed in as: **{display_map.get(active_user, active_user)}**")

u = get_user_record(users_db, active_user)
st.sidebar.caption(f"Title: **{u.get('title','—')}**")
st.sidebar.caption(f"Vibe: **{u.get('vibe','—')}**")
st.sidebar.caption(f"Role: **{u.get('role','player')}**")

# Admin unlock (non-bshapp)
if active_user != "bshapp" and not st.session_state.get("admin_ok", False):
    with st.sidebar.expander("🔒 Admin Unlock", expanded=False):
        pw = st.text_input("Admin password", type="password", key="admin_pw_sidebar")
        if st.button("Unlock Admin", key="admin_unlock_btn"):
            try:
                secret_pw = st.secrets.get("ADMIN_PASSWORD", "")
            except Exception:
                secret_pw = ""
            if secret_pw and pw == secret_pw:
                st.session_state["admin_ok"] = True
                st.sidebar.success("Admin unlocked.")
                st.rerun()
            else:
                st.sidebar.error("Incorrect password (or secrets not configured).")

# Hub link button (requested)
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔗 Hub")
st.sidebar.link_button("⬅️ Go back to hub", HUB_URL, use_container_width=True)

# Quick Redeem scaffold (Z6)
st.sidebar.markdown("---")
with st.sidebar.expander("⚡ Quick Redeem", expanded=False):
    st.caption("Minimal scaffold. Ledger remains primary source of truth.")
    qtab1, qtab2, qtab3 = st.tabs(["Admin Codes", "Careon Awards", "Card Rewards"])

    with qtab1:
        st.caption("Admin-only. Future: redeem admin codes to grant Careon or unlock flags.")
        code = st.text_input("Admin code", placeholder="ADMIN-XXXX", key="qr_admin_code")
        if st.button("Redeem Admin Code", use_container_width=True, key="qr_admin_btn"):
            if not admin_unlocked(active_user):
                st.error("Admin only.")
            else:
                row = find_code(ledger, (code or "").strip())
                if not row or row.get("status") != "new":
                    st.error("Invalid/used code.")
                else:
                    pkg = row.get("package", {}) or {}
                    award = int(pkg.get("award_careon", 0) or 0)
                    # mark used
                    row["status"] = "used"
                    row["used_by"] = active_user
                    row["used_at"] = _now_iso()
                    ledger.setdefault("meta", {})["updated_at"] = _now_iso()

                    if award > 0:
                        deposit(bank, active_user, award, description="Admin code award")
                        save_json(BANK_PATH, bank)

                    save_json(CODES_PATH, ledger)
                    st.success("Redeemed.")
                    st.rerun()

    with qtab2:
        st.caption("Placeholder for a clean award form (admin-driven).")
        if admin_unlocked(active_user):
            amt = st.number_input("Award Careon", min_value=0, step=50, value=0, key="qr_award_amt")
            target = st.selectbox("Target user", user_ids, index=user_ids.index(active_user), key="qr_award_target")
            if st.button("Award", use_container_width=True, key="qr_award_btn"):
                if amt <= 0:
                    st.info("Enter an amount > 0.")
                else:
                    deposit(bank, target, int(amt), description="Admin award")
                    save_json(BANK_PATH, bank)
                    st.success("Awarded.")
                    st.rerun()
        else:
            st.info("Admin only.")

    with qtab3:
        st.caption("Placeholder only. Later: card rewards + claims tracking.")

# ============================================================
# NAV (adds Starplace, hides admin pages for players)
# ============================================================

nav = ["Overview", "Join (Redeem Code)", "Economy", "Cards", "Docs"]

# Admin-only pages
if admin_unlocked(active_user):
    nav.insert(4, "Codes")  # after Cards
    nav.append("Admin")

# Starplace: only visible if user has access
if has_starplace_access(users_db, active_user):
    # put Starplace right after Cards
    insert_at = nav.index("Cards") + 1
    nav.insert(insert_at, "Starplace ⭐")


st.session_state.setdefault("view", "Overview")
view = st.sidebar.radio(
    "Navigate",
    nav,
    index=nav.index(st.session_state["view"]) if st.session_state["view"] in nav else 0,
    key="nav_radio",
)
st.session_state["view"] = view
st.sidebar.caption(f"🧭 Current view: **{view}**")


# ============================================================
# HUB HEADER
# ============================================================
st.title("🎴 Starlight Deck — v3 Hub")

if st.session_state.get("entry_success", False):
    st.markdown(
        """
        <div style="
            border-radius: 16px;
            padding: 10px 14px;
            margin: 10px 0 14px 0;
            border: 1px solid rgba(255,255,255,0.18);
            background: rgba(255,255,255,0.06);
            backdrop-filter: blur(10px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.22);
            text-align: center;
            font-weight: 900;
            letter-spacing: 0.06em;
        ">
            ⭐ The network grows with you — and your input grows the network ⭐
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption("Stay tuned ⭐")

# Top metrics
c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Global Balance", int(bank.get("balance", 0)))
c2.metric("🌍 SLD Network Fund", int(bank.get("sld_network_fund", 0)))
c3.metric("My Balance", get_user_balance(bank, active_user))
c4.metric("Total Earned", int(bank.get("total_earned", 0)))
c5.metric("Total Spent", int(bank.get("total_spent", 0)))
c6.metric("Codes Tracked", len(ledger.get("codes", [])))
st.divider()


# ============================================================
# Careon UI (ticker → bubble → market)
# ============================================================
try:
    careon_bubble_ticker.render_careon_ticker()
except Exception as e:
    st.warning(f"Ticker disabled: {e}")

careon_bubble.render_careon_bubble()

careon_market.render_market(
    bank=bank,
    active_user=active_user,
    deposit_fn=deposit,
    save_fn=lambda: save_json(BANK_PATH, bank),
)


# ============================================================
# STARPLACE (integrated; theme ONLY affects starplace)
# ============================================================
STARPLACE_THEMES = {
    "nebula_ink": {"label": "Nebula Ink", "swatch": "#8B5CF6", "bg_a": "#070A13", "bg_b": "#101A33", "panel_tint": "rgba(139,92,246,0.10)", "is_light": False},
    "moon_milk": {"label": "Moon Milk", "swatch": "#111827", "bg_a": "#F5F6F8", "bg_b": "#EDEFF3", "panel_tint": "rgba(17,24,39,0.06)", "is_light": True},
    "peach_glow": {"label": "Peach Glow", "swatch": "#FB7185", "bg_a": "#FFF1F5", "bg_b": "#FFE4EE", "panel_tint": "rgba(251,113,133,0.08)", "is_light": True},
    "ocean_glass": {"label": "Ocean Glass", "swatch": "#78DCD2", "bg_a": "#061A19", "bg_b": "#0D2A2A", "panel_tint": "rgba(120,220,210,0.10)", "is_light": False},
    "forest_hush": {"label": "Forest Hush", "swatch": "#6FCF97", "bg_a": "#06140D", "bg_b": "#0B2216", "panel_tint": "rgba(111,207,151,0.10)", "is_light": False},
    "sunset_pulse": {"label": "Sunset Pulse", "swatch": "#FF7A7A", "bg_a": "#12080A", "bg_b": "#2A1212", "panel_tint": "rgba(255,122,122,0.10)", "is_light": False},
}
STARPLACE_AVATARS = ["✨", "🕊️", "🐻‍❄️", "🦀", "🌟", "🌙", "🌈", "🪐", "🧿", "🦋", "🍀", "🧊"]

def _sp_norm_theme(k: str) -> str:
    return k if k in STARPLACE_THEMES else "nebula_ink"

def _sp_css(theme_key: str) -> str:
    t = STARPLACE_THEMES[_sp_norm_theme(theme_key)]
    is_light = bool(t.get("is_light", False))
    text = "rgba(10,10,12,0.86)" if is_light else "rgba(245,245,247,0.92)"
    muted = "rgba(10,10,12,0.62)" if is_light else "rgba(245,245,247,0.70)"
    panel = "rgba(255,255,255,0.82)" if is_light else "rgba(255,255,255,0.06)"
    border = "rgba(0,0,0,0.10)" if is_light else "rgba(255,255,255,0.16)"
    shadow = "rgba(0,0,0,0.12)" if is_light else "rgba(0,0,0,0.28)"

    return f"""
<style>
/* Starplace theme is scoped to elements inside #starplace-root */
#starplace-root {{
  --sp-accent: {t["swatch"]};
  --sp-text: {text};
  --sp-muted: {muted};
  --sp-panel: {panel};
  --sp-border: {border};
  --sp-shadow: {shadow};
  --sp-bg-a: {t["bg_a"]};
  --sp-bg-b: {t["bg_b"]};
  --sp-panel-tint: {t["panel_tint"]};
}}
#starplace-root .sp-shell {{
  border-radius: 18px;
  padding: 16px 16px;
  border: 1px solid var(--sp-border);
  background: linear-gradient(180deg, var(--sp-bg-a) 0%, var(--sp-bg-b) 60%, var(--sp-bg-a) 100%);
  color: var(--sp-text);
  box-shadow: 0 16px 50px rgba(0,0,0,0.22);
}}
#starplace-root .sp-module {{
  border-radius: 16px;
  padding: 12px 12px;
  border: 1px solid color-mix(in srgb, var(--sp-accent) 18%, var(--sp-border));
  background: linear-gradient(135deg, var(--sp-panel), var(--sp-panel-tint));
  box-shadow: 0 10px 28px var(--sp-shadow);
  margin: 10px 0;
}}
#starplace-root .sp-title {{
  font-weight: 950;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  font-size: 1.10rem;
  margin-bottom: 4px;
}}
#starplace-root .sp-muted {{
  color: var(--sp-muted);
}}
#starplace-root .sp-avatar-tile {{
  width: 100%;
  aspect-ratio: 1 / 1;
  border-radius: 18px;
  position: relative;
  overflow: hidden;
  border: 1px solid color-mix(in srgb, var(--sp-accent) 16%, var(--sp-border));
  background: rgba(255,255,255,0.05);
}}
#starplace-root .sp-avatar-emoji {{
  position:absolute; inset:0;
  display:flex; align-items:center; justify-content:center;
  font-size: 4.4rem;
}}
#starplace-root .sp-chip {{
  position:absolute; left:10px; bottom:10px;
  padding:6px 10px; border-radius:999px;
  border:1px solid rgba(255,255,255,0.18);
  background: rgba(0,0,0,0.30);
  color: rgba(245,245,247,0.86);
  font-weight: 900;
  letter-spacing: 0.06em;
  font-size: 0.75rem;
}}
</style>
"""

def _user_starplace(users_db: dict, user_id: str) -> dict:
    urec = get_user_record(users_db, user_id)
    urec.setdefault("starplace", {})
    sp = urec["starplace"]
    sp.setdefault("confirmed", False)
    sp.setdefault("theme_key", "nebula_ink")
    sp.setdefault("avatar", "✨")
    sp.setdefault("quote", "")
    return sp

def _save_users():
    save_json(USERS_PATH, users_db)

def _has_starplace_access(users_db: dict, user_id: str) -> bool:
    urec = get_user_record(users_db, user_id)
    claims = urec.get("claims", {}) or {}
    return bool(claims.get("starplace_access", False))

def _grant_starplace_access(users_db: dict, user_id: str):
    urec = get_user_record(users_db, user_id)
    urec.setdefault("claims", {})
    urec["claims"]["starplace_access"] = True
    users_db.setdefault("meta", {})["updated_at"] = _now_iso()


# ============================================================
# VIEWS
# ============================================================
if view == "Overview":
    st.subheader("Acuity • Valor • Variety")
    st.write(
        "This hub supports **Frontier onboarding** (access code → username/vibe → +500 Careon) "
        "and keeps Admin protected."
    )
    st.markdown("### Recent activity (global)")
    txs = recent_txs(bank, 10)
    if txs:
        st.dataframe(txs, use_container_width=True, hide_index=True)
    else:
        st.info("No transactions yet. Use **Join** or **Economy**.")

    # ------------------------------------------------------------
    # Starplace Gate Panel (only shows if NOT unlocked)
    # ------------------------------------------------------------
    if not has_starplace_access(users_db, active_user):
        st.markdown("### ⭐ Starplace Access")
        bal = int(get_user_balance(bank, active_user))
        need = max(0, STARPLACE_COST - bal)

        with st.container():
            st.info(
                f"Starplace requires a **{STARPLACE_COST} Careon deposit**.\n\n"
                f"**Your balance:** {bal}\n\n"
                f"**Still needed:** {need}"
            )

            can_enter = bal >= STARPLACE_COST

            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button(
                    f"Enter Starplace ({STARPLACE_COST})",
                    use_container_width=True,
                    disabled=not can_enter,
                ):
                    try:
                        spend(bank, active_user, STARPLACE_COST, "Starplace Access Gate")
                        grant_starplace_access(users_db, active_user)
                        save_json(BANK_PATH, bank)
                        save_json(USERS_PATH, users_db)
                        st.success("Starplace unlocked ⭐")
                        st.rerun()
                    except Exception as e:
                        st.error(str(e))

            with col2:
                st.caption("Once unlocked, **Starplace ⭐** appears in the sidebar.")

elif view == "Starplace ⭐":
    st.subheader("⭐ Starplace")
    st.caption("Unlocked profile space. (Hook Starplace-dev UI here next.)")
    st.success("Access confirmed ✅")

    # TODO (next step): import and render your Starplace module here
    # from starplace_dev.starplace_page import render_starplace
    # render_starplace(bank=bank, users_db=users_db, active_user=active_user, save_bank=..., save_users=...)


elif view == "Join (Redeem Code)":
    st.subheader("Redeem Access Code")
    st.caption("Frontier Wave: redeem a code to create your profile and receive +500 Careon (global + personal).")

    vibes = ["Calm", "Bold", "Mystic", "Cozy", "Electric", "Ocean", "Forest", "Cosmic"]

    with st.form("redeem_form"):
        code = st.text_input("Access code", placeholder="FRONTIER-A9K2")
        display_name = st.text_input("Choose your username", placeholder="e.g., StarRider")
        vibe = st.selectbox("Choose your vibe", vibes)
        submit = st.form_submit_button("Redeem + Join")

    if submit:
        code = (code or "").strip()
        display_name = " ".join((display_name or "").split()).strip()

        if len(display_name) < 3:
            st.error("Username must be at least 3 characters.")
            st.stop()
        if len(display_name) > 20:
            st.error("Username must be 20 characters or fewer.")
            st.stop()

        reserved = {"admin", "administrator", "mod", "moderator", "bshapp"}
        if display_name.lower() in reserved:
            st.error("That username is reserved. Choose another.")
            st.stop()

        existing_names = {u.get("display_name", "").strip().lower() for u in users_db.get("users", [])}
        if display_name.lower() in existing_names:
            st.error("That username is already taken. Choose another.")
            st.stop()

        row = find_code(ledger, code)
        if not row:
            st.error("Invalid code.")
            st.stop()
        if row.get("status") != "new":
            st.error("That code has already been used.")
            st.stop()

        package = row.get("package", {}) or {}
        title = package.get("title", "Frontier")
        bonus = int(package.get("sign_on_bonus", 500))

        new_user = create_user(users_db, display_name=display_name, vibe=vibe, title=title, role="player")

        row["status"] = "used"
        row["used_by"] = new_user["user_id"]
        row["used_at"] = _now_iso()
        ledger.setdefault("meta", {})["updated_at"] = _now_iso()

        new_user.setdefault("claims", {})
        new_user["claims"]["intro_access"] = True

        deposit(bank, new_user["user_id"], bonus, description=f"Sign-on bonus ({title}) via access code")

        save_json(USERS_PATH, users_db)
        save_json(CODES_PATH, ledger)
        save_json(BANK_PATH, bank)

        st.success("✅ Access code accepted. Welcome to the Frontier.")
        st.markdown(
            f"""
**Username:** {new_user['display_name']}  
**Vibe:** {new_user['vibe']}  
**Title:** {new_user['title']}  
**Bonus:** +{bonus} Careon (global + personal)
"""
        )
        st.caption("You now have full hub access (Admin is locked).")
        st.rerun()

elif view == "Cards":
    h1, h2 = st.columns([4, 1])
    with h1:
        st.markdown("## 🃏 Cards Library")
        st.caption("Read-only preview from the cards manifest.")
    with h2:
        if st.button("Reset View", use_container_width=True):
            st.session_state["selected_card_id"] = None
            st.rerun()

    manifest_path = os.path.join(APP_DIR, "assets", "manifests", "cards_manifest.json")
    manifest = {"version": "v1", "sets": []}

    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
    except Exception as e:
        st.warning(f"Cards manifest not ready yet: {e}")

    sets = manifest.get("sets", []) or []
    if not sets:
        st.info("No card sets yet. Add sets/cards to assets/manifests/cards_manifest.json")

    all_cards = []
    for s in sets:
        set_name = s.get("set_name", "Unnamed Set")
        for card in s.get("cards", []) or []:
            c = dict(card)
            c["_set_name"] = set_name
            all_cards.append(c)

    def _card_key(c: dict) -> str:
        return c.get("card_id") or f"{c.get('_set_name','set')}-{c.get('name','card')}"

    st.session_state.setdefault("selected_card_id", None)
    selected = None
    if st.session_state["selected_card_id"]:
        for c in all_cards:
            if _card_key(c) == st.session_state["selected_card_id"]:
                selected = c
                break

    st.markdown("### ✦ Card Stage")
    stage_card = selected if selected else (all_cards[0] if all_cards else None)

    if not stage_card:
        st.info("No cards available yet to preview.")
    else:
        colA, colB = st.columns([2, 3])
        name = stage_card.get("name", "Card")
        img = stage_card.get("image") or stage_card.get("thumb")

        with colA:
            render_card_tile(name=name, image_path=img, subtitle=None)
        with colB:
            st.markdown(f"**{name}**")
            st.caption(f"Set: {stage_card.get('_set_name', 'Unnamed Set')}")
            if stage_card.get("rarity"):
                st.write(f"Rarity: `{stage_card.get('rarity')}`")
            if stage_card.get("tags"):
                st.write("Tags: " + ", ".join(stage_card.get("tags")))
            if stage_card.get("text"):
                st.markdown(f"> {stage_card.get('text')}")
            st.button("Open (placeholder)", use_container_width=True)

    st.divider()

    set_options = sorted({c.get("_set_name", "Unnamed Set") for c in all_cards})
    rarity_options = sorted({(c.get("rarity") or "").strip() for c in all_cards if (c.get("rarity") or "").strip()})

    with st.expander("Filters", expanded=True):
        f_set = st.selectbox("Set", ["All"] + set_options)
        f_rarity = st.selectbox("Rarity", ["All"] + rarity_options) if rarity_options else "All"
        search = st.text_input("Search name")

    def _match(c: dict) -> bool:
        if f_set != "All" and c.get("_set_name") != f_set:
            return False
        if f_rarity != "All" and (c.get("rarity") or "").strip() != f_rarity:
            return False
        if search and search.lower() not in (c.get("name", "") or "").lower():
            return False
        return True

    cards = [c for c in all_cards if _match(c)]
    st.caption(f"Showing {len(cards)} card(s)")

    if not cards:
        st.info("No cards match your filters.")
    else:
        cols = st.columns(4)
        for i, card in enumerate(cards):
            with cols[i % 4]:
                render_card_tile(
                    name=card.get("name", "Card"),
                    image_path=card.get("thumb") or card.get("image"),
                    subtitle=card.get("rarity"),
                )
                if st.button(f"View: {card.get('name','Card')}", key=f"cardpick_{_card_key(card)}", use_container_width=True):
                    st.session_state["selected_card_id"] = _card_key(card)
                    st.rerun()

elif view == "Economy":
    is_admin = admin_unlocked(active_user)

    st.subheader("Economy")
    st.caption("Personal economy. Deposits are admin-only. Spending transfers into the global pool.")

    st.markdown("## 🫧 CAREON_BUBBLE PLACEHOLDER (DO NOT REMOVE)")
    st.info("This space is reserved for careon_bubble.py UI later.")
    st.empty()

    with st.form("economy_form"):
        if is_admin:
            tx_type = st.selectbox("Type", ["deposit", "spend"])
        else:
            tx_type = "spend"
            st.info("Deposits are admin-only. You can spend what you’ve earned.")

        amount = st.number_input("Amount (integer)", min_value=0, step=1, value=0)
        desc = st.text_input("Description (optional)")
        submitted = st.form_submit_button("Record")

    if submitted:
        try:
            if tx_type == "deposit":
                if not is_admin:
                    raise ValueError("Deposits are admin-only.")
                tx = deposit(bank, active_user, int(amount), desc)
            else:
                tx = spend(bank, active_user, int(amount), desc)

            save_json(BANK_PATH, bank)
            st.success(f"Recorded {tx_type}: {tx['amount']}")
            st.rerun()
        except Exception as e:
            st.error(f"{e}")

    st.markdown("### Recent transactions (me)")
    txs = recent_txs(bank, 25, user_id=active_user)
    if txs:
        st.dataframe(txs, use_container_width=True, hide_index=True)
    else:
        st.info("No transactions yet.")

elif view == "Codes":
    st.subheader("Codes Ledger")
    st.caption("Admin view. (Hidden from players.)")
    rows = ledger.get("codes", [])
    if rows:
        st.dataframe(rows, use_container_width=True, hide_index=True)
    else:
        st.info("No codes yet.")

elif view == "Docs":
    st.subheader("Guides")
    tab1, tab2, tab3 = st.tabs(["rules.md", "currency.md", "users.md"])
    with tab1:
        txt = load_text_safe(RULES_MD)
        st.markdown(txt) if txt else st.info("Add content to `rules.md`.")
    with tab2:
        txt = load_text_safe(CURRENCY_MD)
        st.markdown(txt) if txt else st.info("Add content to `currency.md`.")
    with tab3:
        txt = load_text_safe(USERS_MD)
        st.markdown(txt) if txt else st.info("Add content to `users.md`.")

elif view == "Starplace":
    st.subheader("⭐ Starplace")
    st.caption("Starplace lives inside the Hub. Themes apply only here.")

    # Access gate: 1200 Careon one-time unlock
    fee = 1200
    if not _has_starplace_access(users_db, active_user):
        st.info(f"Starplace requires a one-time unlock: **{fee} Careon**.")
        st.caption("This is stored in your user record. (Careon is protected.)")

        colA, colB = st.columns([2, 3])
        with colA:
            st.metric("My Balance", get_user_balance(bank, active_user))
        with colB:
            st.caption("Unlock will spend from your **personal** balance (and transfer into global pool).")

        if st.button(f"Unlock Starplace ({fee} Careon)", use_container_width=True):
            try:
                spend(bank, active_user, fee, description="Starplace unlock (one-time)")
                _grant_starplace_access(users_db, active_user)
                save_json(BANK_PATH, bank)
                _save_users()
                st.success("Unlocked ⭐")
                st.rerun()
            except Exception as e:
                st.error(str(e))
        st.stop()

    # Render starplace shell
    sp = _user_starplace(users_db, active_user)
    sp["theme_key"] = _sp_norm_theme(sp.get("theme_key", "nebula_ink"))
    st.markdown(_sp_css(sp["theme_key"]), unsafe_allow_html=True)

    st.markdown('<div id="starplace-root"><div class="sp-shell">', unsafe_allow_html=True)
    st.markdown('<div class="sp-title">STARPLACE</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sp-muted">Profile space for: <b>{display_map.get(active_user, active_user)}</b></div>', unsafe_allow_html=True)

    t1, t2, t3 = st.tabs(["Profile", "Journal", "Settings"])

    with t1:
        st.markdown('<div class="sp-module">', unsafe_allow_html=True)
        st.markdown(f"**Quote:** {sp.get('quote','') or '_No quote yet._'}")
        st.markdown("</div>", unsafe_allow_html=True)

        colL, colR = st.columns([3, 2], gap="small")
        with colL:
            st.markdown('<div class="sp-module">', unsafe_allow_html=True)
            st.markdown("**⭐ Motto**")
            st.markdown("✨ ⭐ The network grows with you, your input grows the network ⭐ ✨")
            st.markdown("</div>", unsafe_allow_html=True)
        with colR:
            st.markdown(
                f"""
                <div class="sp-avatar-tile">
                  <div class="sp-avatar-emoji">{sp.get("avatar","✨")}</div>
                  <div class="sp-chip">{STARPLACE_THEMES[sp["theme_key"]]["label"]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with t2:
        st.markdown('<div class="sp-module">', unsafe_allow_html=True)
        st.markdown("**Journal**")
        urec = get_user_record(users_db, active_user)
        urec.setdefault("starplace", {})
        urec["starplace"].setdefault("journal", "")
        j = st.text_area("Journal", value=urec["starplace"]["journal"], height=220, label_visibility="collapsed")
        if st.button("Save Journal", use_container_width=True):
            urec["starplace"]["journal"] = j or ""
            users_db.setdefault("meta", {})["updated_at"] = _now_iso()
            _save_users()
            st.success("Saved ✅")
        st.markdown("</div>", unsafe_allow_html=True)

    with t3:
        st.markdown('<div class="sp-module">', unsafe_allow_html=True)
        st.caption("Theme affects ONLY Starplace. Hub stays ink gradient forever.")
        quote = st.text_input("Quote", value=sp.get("quote",""))
        theme_key = st.selectbox(
            "Theme",
            options=list(STARPLACE_THEMES.keys()),
            index=list(STARPLACE_THEMES.keys()).index(sp["theme_key"]),
            format_func=lambda k: f"{STARPLACE_THEMES[k]['label']} ({STARPLACE_THEMES[k]['swatch']})",
        )
        avatar = st.selectbox(
            "Avatar",
            options=STARPLACE_AVATARS,
            index=STARPLACE_AVATARS.index(sp.get("avatar","✨")) if sp.get("avatar","✨") in STARPLACE_AVATARS else 0,
        )

        if st.button("Apply", use_container_width=True):
            urec = get_user_record(users_db, active_user)
            urec.setdefault("starplace", {})
            urec["starplace"]["quote"] = " ".join((quote or "").split())
            urec["starplace"]["theme_key"] = _sp_norm_theme(theme_key)
            urec["starplace"]["avatar"] = avatar
            users_db.setdefault("meta", {})["updated_at"] = _now_iso()
            _save_users()
            st.success("Applied ✅")
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)

elif view == "Admin":
    st.subheader("🔧 Admin Console")
    st.caption("Admin-only utilities. Safe mode: resets require confirmation.")

    st.session_state.setdefault("admin_view_as_player", False)
    st.session_state["admin_view_as_player"] = st.toggle(
        "⭐ View as Player (hide admin powers)",
        value=st.session_state["admin_view_as_player"],
    )

    if st.session_state["admin_view_as_player"]:
        st.info("Player View is ON. Admin actions hidden.")
        st.stop()

    with st.expander("Raw JSON (read-only)", expanded=False):
        st.markdown("**careon_bank_v2.json**")
        st.json(bank)
        st.markdown("**codes_ledger.json**")
        st.json(ledger)
        st.markdown("**user_profile.json**")
        st.json(users_db)

    st.divider()

    st.markdown("### 🧨 Resets (protected)")
    st.caption("Type RESET to unlock the reset buttons for this session.")
    st.session_state.setdefault("reset_unlocked", False)

    confirm = st.text_input("Type RESET", value="", key="reset_confirm_text")
    if confirm.strip().upper() == "RESET":
        st.session_state["reset_unlocked"] = True

    if not st.session_state["reset_unlocked"]:
        st.info("Resets are locked until you type RESET.")
        st.stop()

    colA, colB, colC = st.columns(3)

    with colA:
        if st.button("Reset bank", use_container_width=True):
            bank = default_bank()
            save_json(BANK_PATH, bank)
            st.success("Bank reset.")
            st.rerun()

    with colB:
        if st.button("Reset codes (empty)", use_container_width=True):
            ledger = default_codes()
            save_json(CODES_PATH, ledger)
            st.success("Codes reset.")
            st.rerun()

    with colC:
        if st.button("Reset users (admin only)", use_container_width=True):
            users_db = default_users()
            save_json(USERS_PATH, users_db)
            st.success("Users reset.")
            st.rerun()

# ----------------------------
# END OF APP
# ----------------------------
