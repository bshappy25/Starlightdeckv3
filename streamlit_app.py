import json
import os
from datetime import datetime, timezone

import streamlit as st

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
        "sld_network_fund": 0,
        "total_earned": 0,
        "total_spent": 0,
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
    bank["balance"] = int(bank.get("balance", 0)) + amount
    bank["total_earned"] = int(bank.get("total_earned", 0)) + amount
    return record_tx(bank, user_id, "deposit", amount, description)


def spend(bank: dict, user_id: str, amount: int, description: str = ""):
    amount = int(amount)
    if amount <= 0:
        raise ValueError("Spend amount must be greater than 0.")
    bal = int(bank.get("balance", 0))
    if amount > bal:
        raise ValueError(f"Insufficient balance. You have {bal}, tried to spend {amount}.")
    bank["balance"] = bal - amount
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


# -------- Branch A helper (identity badge) --------
def get_user_record(users_db: dict, user_id: str) -> dict:
    for u in users_db.get("users", []):
        if u.get("user_id") == user_id:
            return u
    return {}


# ============================================================
# UI
# ============================================================
st.set_page_config(page_title=APP_TITLE, page_icon=APP_ICON, layout="wide")

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
st.sidebar.caption(f"Signed in as: **{display_map.get(active_user, active_user)}**")

# Branch A: identity badge
u = get_user_record(users_db, active_user)
st.sidebar.caption(f"Title: **{u.get('title','—')}**")
st.sidebar.caption(f"Vibe: **{u.get('vibe','—')}**")
st.sidebar.caption(f"Role: **{u.get('role','player')}**")

# Navigation (Admin only appears if unlocked)
nav = ["Overview", "Join (Redeem Code)", "Economy", "Codes", "Docs"]
if admin_unlocked(active_user):
    nav.append("Admin")

view = st.sidebar.radio("Navigate", nav, index=0)

# Admin password gate (only for non-bshapp users)
if "Admin" in nav and active_user != "bshapp":
    # If they click Admin and aren't unlocked, prompt
    if view == "Admin" and not st.session_state.get("admin_ok", False):
        st.title("🔒 Admin Locked")
        st.write("Enter admin password to continue.")
        pw = st.text_input("Admin password", type="password")
        if st.button("Unlock"):
            try:
                secret_pw = st.secrets.get("ADMIN_PASSWORD", "")
            except Exception:
                secret_pw = ""
            if secret_pw and pw == secret_pw:
                st.session_state["admin_ok"] = True
                st.success("Unlocked.")
                st.rerun()
            else:
                st.error("Incorrect password (or secrets not configured).")
        st.stop()

st.title("🎴 Starlight Deck — v3 Hub")

# Top metrics
c1, c2, c3, c4 = st.columns(4)
c1.metric("Global Balance", int(bank.get("balance", 0)))
c2.metric("Total Earned", int(bank.get("total_earned", 0)))
c3.metric("Total Spent", int(bank.get("total_spent", 0)))
c4.metric("Codes Tracked", len(ledger.get("codes", [])))
st.divider()

# ----------------------------
# Overview
# ----------------------------
if view == "Overview":
    st.subheader("Acuity • Valor • Variety")
    st.write(
        "This hub supports **Frontier onboarding** (access code → username/vibe → +500 Careon) "
        "and keeps Admin protected."
    )
    st.markdown("### Recent activity")
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
    st.caption("Frontier Wave: redeem a code to create your profile and receive +500 Careon (global).")

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

        # Combine options: add bonus to GLOBAL bank + record tx
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
**Bonus:** +{bonus} Careon (added to global)
"""
        )
        st.caption("You now have full hub access (Admin is locked).")
        st.rerun()

# ----------------------------
# Economy
# ----------------------------
elif view == "Economy":
    st.subheader("Economy")
    st.caption("Manual deposit/spend (global ledger). Guardrails prevent negative balance.")

    with st.form("economy_form"):
        tx_type = st.selectbox("Type", ["deposit", "spend"])
        amount = st.number_input("Amount (integer)", min_value=0, step=1, value=0)
        desc = st.text_input("Description (optional)")
        submitted = st.form_submit_button("Record")

    if submitted:
        try:
            if tx_type == "deposit":
                tx = deposit(bank, active_user, int(amount), desc)
            else:
                tx = spend(bank, active_user, int(amount), desc)
            save_json(BANK_PATH, bank)
            st.success(f"Recorded {tx_type}: {tx['amount']}")
            st.rerun()
        except Exception as e:
            st.error(f"{e}")

    st.markdown("### Recent transactions")
    show_only_me = st.toggle("Show only active user", value=True)
    txs = recent_txs(bank, 25, user_id=active_user if show_only_me else None)
    if txs:
        st.dataframe(txs, use_container_width=True, hide_index=True)
    else:
        st.info("No transactions yet.")

# ----------------------------
# Codes
# ----------------------------
elif view == "Codes":
    st.subheader("Codes Ledger")
    st.caption("Read-only for players. Admin can reset/edit via Admin panel.")

    # Show limited fields for players
    rows = ledger.get("codes", [])
    safe_rows = [
        {
            "code": r.get("code"),
            "status": r.get("status"),
            "used_at": r.get("used_at"),
        }
        for r in rows
    ]
    if safe_rows:
        st.dataframe(safe_rows, use_container_width=True, hide_index=True)
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
# Admin (protected)
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
