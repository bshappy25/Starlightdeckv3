# ================================
# Starlight Deck — Main App
# ================================

import json
import os
from datetime import datetime, timezone

import streamlit as st

# Local modules (must exist in repo root)
import careon_bubble
import careon_market
import careon_bubble_ticker


# ----------------
# App constants
# ----------------
APP_DIR = os.path.dirname(__file__)

BANK_PATH = os.path.join(APP_DIR, "careon_bank_v2.json")
CODES_PATH = os.path.join(APP_DIR, "codes_ledger.json")
USERS_PATH = os.path.join(APP_DIR, "user_profile.json")

RULES_MD = os.path.join(APP_DIR, "rules.md")
CURRENCY_MD = os.path.join(APP_DIR, "currency.md")
USERS_MD = os.path.join(APP_DIR, "users.md")

APP_TITLE = "Starlight Deck"
APP_ICON = "🎴"




# ============================================================
# 🎨🎨🎨 DESIGN / CSS ZONE — SAFE TO EDIT (OBNOXIOUS ON PURPOSE)
# ------------------------------------------------------------
# Only edit CSS + UI styling here.
# DO NOT change logic, JSON loading, deposit/spend, onboarding here.
# If something breaks after design edits, revert this block first.
# ============================================================

CUSTOM_CSS = """
<style>
/* === SAFE STYLING ZONE === */

/* Example:
.main { background: #0b1020; color: #e6e6e6; }
[data-testid="stSidebar"] { background: #0f1630; }
*/

/* === END SAFE STYLING ZONE === */
</style>
"""

# ============================================================
# CORE CONFIG — DO NOT EDIT UNLESS YOU KNOW WHY
# ============================================================

APP_DIR = os.path.dirname(__file__)

BANK_PATH = os.path.join(APP_DIR, "careon_bank_v2.json")
CODES_PATH = os.path.join(APP_DIR, "codes_ledger.json")
USERS_PATH = os.path.join(APP_DIR, "user_profile.json")

RULES_MD = os.path.join(APP_DIR, "rules.md")
CURRENCY_MD = os.path.join(APP_DIR, "currency.md")
USERS_MD = os.path.join(APP_DIR, "users.md")

APP_TITLE = "Starlight Deck"
APP_ICON = "🎴"


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


def load_text_safe(path: str) -> str | None:
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
        "sld_network_fund": 0,          # C5: visible to everyone, intentional changes only
        "total_earned": 0,
        "total_spent": 0,
        "balances_by_user": {},         # B1: per-user balances
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
                "claims": {"admin_auto": True},
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
    """
    B5: Backward compatible migration.
    Rebuild personal balances by replaying txs:
    - deposit => personal +amount
    - spend   => personal -amount (floored at 0)
    Global bank balance is NOT recomputed here.
    """
    ensure_user_balances(bank)
    balances = {}

    # txs are newest-first; replay oldest-first for correctness
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
    bank["meta"]["updated_at"] = _now_iso()


def record_tx(bank: dict, user_id: str, tx_type: str, amount: int, description: str):
    tx = {
        "ts": _now_iso(),
        "user_id": user_id,
        "type": tx_type,
        "amount": int(amount),
        "description": description.strip() if description else "",
    }
    bank["txs"].insert(0, tx)
    bank["meta"]["updated_at"] = _now_iso()
    return tx


def deposit(bank: dict, user_id: str, amount: int, description: str = ""):
    amount = int(amount)
    if amount <= 0:
        raise ValueError("Deposit amount must be greater than 0.")

    # B4a: deposit adds to BOTH global + personal
    bank["balance"] = int(bank.get("balance", 0)) + amount
    set_user_balance(bank, user_id, get_user_balance(bank, user_id) + amount)

    bank["total_earned"] = int(bank.get("total_earned", 0)) + amount
    return record_tx(bank, user_id, "deposit", amount, description)


def spend(bank: dict, user_id: str, amount: int, description: str = ""):
    amount = int(amount)
    if amount <= 0:
        raise ValueError("Spend amount must be greater than 0.")

    # B10: guardrail on PERSONAL balance
    personal = get_user_balance(bank, user_id)
    if amount > personal:
        raise ValueError(f"Insufficient personal balance. You have {personal}, tried to spend {amount}.")

    # B3 NO: spend transfers into global pool (global INCREASES on spend)
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
    # user-1, user-2, ... skipping existing
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
    }
    users_db["users"].append(user)
    users_db["meta"]["updated_at"] = _now_iso()
    return user


def admin_unlocked(active_user_id: str) -> bool:
    # Auto admin for bshapp
    if active_user_id == "bshapp":
        return True
    # Otherwise require password session
    return bool(st.session_state.get("admin_ok", False))


def get_user_record(users_db: dict, user_id: str) -> dict:
    for u in users_db.get("users", []):
        if u.get("user_id") == user_id:
            return u
    return {}


# ============================================================
# UI
# ============================================================
st.set_page_config(page_title=APP_TITLE, page_icon=APP_ICON, layout="wide")
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)  # ✅ safe design injection

# Branch A: allow auto-select after redeem
st.session_state.setdefault("active_user_override", None)

json_warnings = st.session_state.get("_json_warnings", set())
if json_warnings:
    st.warning(
        "One or more JSON files could not be parsed. Running with safe defaults.\n\n- "
        + "\n- ".join(sorted(json_warnings))
    )

bank = load_json_safe(BANK_PATH, default_bank())
ledger = load_json_safe(CODES_PATH, default_codes())
users_db = load_json_safe(USERS_PATH, default_users())

# Branch B: ensure per-user balances exist and rebuild from txs if missing/empty
ensure_user_balances(bank)
if not bank.get("balances_by_user"):
    rebuild_user_balances_from_txs(bank)
    save_json(BANK_PATH, bank)

# Sidebar identity + navigation
st.sidebar.markdown(f"## {APP_ICON} {APP_TITLE}")

user_ids = [u.get("user_id", "user-1") for u in users_db.get("users", [])] or ["user-1"]
display_map = {u.get("user_id"): u.get("display_name", u.get("user_id")) for u in users_db.get("users", [])}

st.sidebar.markdown("### Identity")

default_index = 0
if st.session_state.get("active_user_override") in user_ids:
    default_index = user_ids.index(st.session_state["active_user_override"])

active_user = st.sidebar.selectbox(
    "Active user",
    options=user_ids,
    index=default_index,
    format_func=lambda uid: f"{display_map.get(uid, uid)} ({uid})",
)

# clear override after it takes effect
st.session_state["active_user_override"] = None

# Sidebar status
st.sidebar.markdown("### Status")
st.sidebar.metric("Global Balance", int(bank.get("balance", 0)))
st.sidebar.metric("🌍 SLD Network Fund", int(bank.get("sld_network_fund", 0)))
st.sidebar.metric("My Balance", get_user_balance(bank, active_user))
st.sidebar.caption(f"Signed in as: **{display_map.get(active_user, active_user)}**")

# Branch A: identity badge
u = get_user_record(users_db, active_user)
st.sidebar.caption(f"Title: **{u.get('title','—')}**")
st.sidebar.caption(f"Vibe: **{u.get('vibe','—')}**")
st.sidebar.caption(f"Role: **{u.get('role','player')}**")

# C1: Admin unlock control (non-bshapp only)
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

# C2: Codes + Admin are admin-only in navigation
nav = ["Overview", "Join (Redeem Code)", "Economy", "Docs"]
if admin_unlocked(active_user):
    nav.insert(3, "Codes")  # shows only for admin
    nav.append("Admin")

view = st.sidebar.radio("Navigate", nav, index=0)

st.title("🎴 Starlight Deck — v3 Hub")

# Top metrics (B2 + C5 + B9)
c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Global Balance", int(bank.get("balance", 0)))
c2.metric("🌍 SLD Network Fund", int(bank.get("sld_network_fund", 0)))
c3.metric("My Balance", get_user_balance(bank, active_user))
c4.metric("Total Earned", int(bank.get("total_earned", 0)))
c5.metric("Total Spent", int(bank.get("total_spent", 0)))
c6.metric("Codes Tracked", len(ledger.get("codes", [])))
st.divider()

# ============================
# Careon UI (ticker → bubble → market)
# ============================

# --- Careon ticker (visual only) ---
try:
    import careon_bubble_ticker
    careon_bubble_ticker.render_careon_ticker()
except Exception as e:
    st.warning(f"Ticker disabled: {e}")

# --- Careon bubble button (clickable) ---
careon_bubble.render_careon_bubble()

# --- Careon Market UI (renders only when show_market == True) ---
careon_market.render_market(
    bank=bank,
    active_user=active_user,
    deposit_fn=deposit,
    save_fn=lambda: save_json(BANK_PATH, bank),
)

# ============================
# Main Views
# ============================

# ----------------------------
# Overview
# ----------------------------
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
        
# ----------------------------
# Join (Redeem Code)
# ----------------------------
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
        display_name = (display_name or "").strip()

        # -------- Branch A1: username rules --------
        if len(display_name) < 3:
            st.error("Username must be at least 3 characters.")
            st.stop()

        # Normalize whitespace
        display_name = " ".join(display_name.split())

        if not display_name:
            st.error("Username cannot be blank.")
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
        # ------------------------------------------

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

        # Create user
        new_user = create_user(users_db, display_name=display_name, vibe=vibe, title=title, role="player")

        # Mark code used
        row["status"] = "used"
        row["used_by"] = new_user["user_id"]
        row["used_at"] = _now_iso()
        ledger["meta"]["updated_at"] = _now_iso()

        # Sign-on: deposit adds to GLOBAL + PERSONAL (B4a)
        deposit(bank, new_user["user_id"], bonus, description=f"Sign-on bonus ({title}) via access code")

        # Save everything
        save_json(USERS_PATH, users_db)
        save_json(CODES_PATH, ledger)
        save_json(BANK_PATH, bank)

        # Branch A3: auto-select the new user after redeem
        st.session_state["active_user_override"] = new_user["user_id"]

        # Branch A4: better confirmation card
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

# ----------------------------
# Economy
# ----------------------------
elif view == "Economy":
    # C4b + Branch B behavior:
    # - Deposits are admin-only
    # - Players can spend from PERSONAL balance
    # - Spending transfers into GLOBAL balance (global increases on spend)
    is_admin = admin_unlocked(active_user)

    st.subheader("Economy")
    st.caption("Personal economy. Deposits are admin-only. Spending transfers into the global pool.")

    # B6c: leave obnoxiously obvious placeholder for careon_bubble.py later
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

# ----------------------------
# Codes (admin-only; hidden from players by nav)
# ----------------------------
elif view == "Codes":
    st.subheader("Codes Ledger")
    st.caption("Admin view. (Hidden from players.)")

    rows = ledger.get("codes", [])
    if rows:
        st.dataframe(rows, use_container_width=True, hide_index=True)
    else:
        st.info("No codes yet.")

# ----------------------------
# Docs
# ----------------------------
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

# ----------------------------
# Admin (protected; hidden unless unlocked)
# ----------------------------
elif view == "Admin":
    st.subheader("Admin")
    st.caption("Visible only to admin. Auto-unlocked for user_id `bshapp`.")

    with st.expander("Raw JSON (read-only)", expanded=False):
        st.markdown("**careon_bank_v2.json**")
        st.json(bank)
        st.markdown("**codes_ledger.json**")
        st.json(ledger)
        st.markdown("**user_profile.json**")
        st.json(users_db)

    st.warning("Reset actions overwrite files.")

    # C3: Danger Zone confirmation
    with st.expander("☠️ Danger Zone (Resets)", expanded=False):
        confirm = st.text_input('Type RESET to enable destructive actions', value="")
        if confirm.strip().upper() == "RESET":
            colA, colB, colC = st.columns(3)

            with colA:
                if st.button("Reset bank"):
                    bank = default_bank()
                    save_json(BANK_PATH, bank)
                    st.success("Bank reset.")
                    st.rerun()

            with colB:
                if st.button("Reset codes (empty)"):
                    ledger = default_codes()
                    save_json(CODES_PATH, ledger)
                    st.success("Codes reset.")
                    st.rerun()

            with colC:
                if st.button("Reset users (admin only)"):
                    users_db = default_users()
                    save_json(USERS_PATH, users_db)
                    st.success("Users reset.")
                    st.rerun()
        else:
            st.info("Resets are locked until you type RESET.")
