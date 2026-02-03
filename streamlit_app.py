import json
import os
from datetime import datetime, timezone

import streamlit as st

# ============================================================
# Starlight Deck v3 — Single-file spine (no external modules)
# Repo files expected in same folder as this file:
#   - careon_bank_v2.json
#   - codes_ledger.json
#   - user_profile.json
#   - rules.md / currency.md / users.md
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


# ----------------------------
# Helpers: safe JSON handling
# ----------------------------
def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load_json_safe(path: str, default):
    """
    Loads JSON if present and valid.
    If file is missing OR blank OR invalid, returns default (and attempts to seed file).
    """
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
        # If it's corrupted, keep the app usable but don't nuke the file silently.
        # We'll return default and surface an in-app warning.
        st.session_state.setdefault("_json_warnings", set()).add(path)
        return default


def save_json(path: str, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_text_safe(path: str) -> str | None:
    try:
        if not os.path.exists(path):
            return None
        with open(path, "r", encoding="utf-8") as f:
            txt = f.read().strip()
        return txt if txt else None
    except Exception:
        return None


# ----------------------------
# Data defaults (placeholder-safe)
# ----------------------------
def default_bank():
    return {
        "balance": 0,
        "sld_network_fund": 0,
        "total_earned": 0,
        "total_spent": 0,
        "txs": [],  # list of dicts
        "meta": {"version": "v3", "updated_at": _now_iso()},
    }


def default_codes():
    return {
        "codes": [],  # list of dicts: {code, status, created_at, used_by, used_at, note}
        "meta": {"version": "v3", "updated_at": _now_iso()},
    }


def default_users():
    return {
        "users": [
            {
                "user_id": "user-1",
                "display_name": "Player One",
                "role": "player",  # player | admin
                "created_at": _now_iso(),
            }
        ],
        "meta": {"version": "v3", "updated_at": _now_iso()},
    }


# ----------------------------
# Economy actions (bank is global in this simple version)
# ----------------------------
def record_tx(bank: dict, user_id: str, tx_type: str, amount: int, description: str):
    tx = {
        "ts": _now_iso(),
        "user_id": user_id,
        "type": tx_type,  # deposit | spend
        "amount": int(amount),
        "description": description.strip() if description else "",
    }
    bank["txs"].insert(0, tx)  # newest first
    bank["meta"]["updated_at"] = _now_iso()
    return tx


def deposit(bank: dict, user_id: str, amount: int, description: str = ""):
    amount = int(amount)
    if amount <= 0:
        raise ValueError("Deposit amount must be greater than 0.")
    bank["balance"] = int(bank.get("balance", 0)) + amount
    bank["total_earned"] = int(bank.get("total_earned", 0)) + amount
    tx = record_tx(bank, user_id, "deposit", amount, description)
    return tx


def spend(bank: dict, user_id: str, amount: int, description: str = ""):
    amount = int(amount)
    if amount <= 0:
        raise ValueError("Spend amount must be greater than 0.")
    bal = int(bank.get("balance", 0))
    if amount > bal:
        raise ValueError(f"Insufficient balance. You have {bal}, tried to spend {amount}.")
    bank["balance"] = bal - amount
    bank["total_spent"] = int(bank.get("total_spent", 0)) + amount
    tx = record_tx(bank, user_id, "spend", amount, description)
    return tx


def recent_txs(bank: dict, n: int = 10, user_id: str | None = None):
    txs = bank.get("txs", [])
    if user_id:
        txs = [t for t in txs if t.get("user_id") == user_id]
    return txs[: max(0, int(n))]


# ----------------------------
# Code ledger actions
# ----------------------------
def add_code(ledger: dict, code: str, note: str = ""):
    code = (code or "").strip()
    if not code:
        raise ValueError("Code cannot be blank.")
    # prevent duplicates
    existing = {c.get("code") for c in ledger.get("codes", [])}
    if code in existing:
        raise ValueError("That code already exists in the ledger.")
    row = {
        "code": code,
        "status": "new",  # new | used | retired
        "created_at": _now_iso(),
        "used_by": "",
        "used_at": "",
        "note": note.strip() if note else "",
    }
    ledger["codes"].insert(0, row)
    ledger["meta"]["updated_at"] = _now_iso()
    return row


def mark_code_used(ledger: dict, code: str, used_by: str = "", note: str = ""):
    for row in ledger.get("codes", []):
        if row.get("code") == code:
            if row.get("status") == "used":
                raise ValueError("That code is already marked used.")
            row["status"] = "used"
            row["used_by"] = used_by.strip() if used_by else ""
            row["used_at"] = _now_iso()
            if note:
                row["note"] = note.strip()
            ledger["meta"]["updated_at"] = _now_iso()
            return row
    raise ValueError("Code not found.")


# ============================================================
# UI
# ============================================================
st.set_page_config(page_title=APP_TITLE, page_icon=APP_ICON, layout="wide")

# Seed warnings (if any corrupted JSON was detected)
json_warnings = st.session_state.get("_json_warnings", set())
if json_warnings:
    st.warning(
        "One or more JSON files could not be parsed. "
        "The app is running with safe defaults. "
        "Fix or replace these files:\n\n- " + "\n- ".join(sorted(json_warnings))
    )

bank = load_json_safe(BANK_PATH, default_bank())
ledger = load_json_safe(CODES_PATH, default_codes())
users_db = load_json_safe(USERS_PATH, default_users())

# Sidebar identity + navigation (Variety)
st.sidebar.markdown(f"## {APP_ICON} {APP_TITLE}")

user_ids = [u.get("user_id", "user-1") for u in users_db.get("users", [])] or ["user-1"]
display_map = {u.get("user_id"): u.get("display_name", u.get("user_id")) for u in users_db.get("users", [])}

st.sidebar.markdown("### Identity")
active_user = st.sidebar.selectbox(
    "Active user",
    options=user_ids,
    index=0,
    format_func=lambda uid: f"{display_map.get(uid, uid)} ({uid})",
)

view = st.sidebar.radio(
    "Navigate",
    ["Overview", "Economy", "Codes", "Docs", "Admin"],
    index=0,
)

# Header
st.title("🎴 Starlight Deck — v3 Spine")

# Quick summary strip
col1, col2, col3, col4 = st.columns(4)
col1.metric("Careon Balance", int(bank.get("balance", 0)))
col2.metric("Total Earned", int(bank.get("total_earned", 0)))
col3.metric("Total Spent", int(bank.get("total_spent", 0)))
col4.metric("Codes Tracked", len(ledger.get("codes", [])))

st.divider()

# ----------------------------
# Overview (Acuity)
# ----------------------------
if view == "Overview":
    st.subheader("Acuity • Valor • Variety")
    st.write(
        "This is the **spine UI**: a clean foundation that reads your docs, "
        "tracks Careon balance + transactions, and maintains a code ledger."
    )

    left, right = st.columns([1, 1])

    with left:
        st.markdown("### What’s live right now")
        st.markdown(
            "- **Economy**: deposit / spend with guardrails\n"
            "- **Codes**: create codes, mark used\n"
            "- **Docs**: render `rules.md`, `currency.md`, `users.md`\n"
            "- **Users**: simple identity selector (no auth yet)"
        )

    with right:
        st.markdown("### Next safe expansions (no refactor required)")
        st.markdown(
            "- Add per-user balances (instead of one global bank)\n"
            "- Add ‘Draw’ gameplay loop (earn/spend tied to draws)\n"
            "- Add marketplace packages (Careon Market)\n"
            "- Add styled UI (glass / cards) once behavior is stable"
        )

    st.markdown("### Recent activity")
    txs = recent_txs(bank, 8)
    if txs:
        st.dataframe(txs, use_container_width=True, hide_index=True)
    else:
        st.info("No transactions yet. Go to **Economy** to record one.")

# ----------------------------
# Economy (Valor)
# ----------------------------
elif view == "Economy":
    st.subheader("Economy")
    st.caption("Deposit and spend Careon with strict guardrails. Saves to `careon_bank_v2.json`.")

    with st.form("economy_form", clear_on_submit=False):
        c1, c2, c3 = st.columns([1, 1, 2])
        tx_type = c1.selectbox("Type", ["deposit", "spend"])
        amount = c2.number_input("Amount (integer)", min_value=0, step=1, value=0)
        desc = c3.text_input("Description (optional)", value="")
        submitted = st.form_submit_button("Record")

    if submitted:
        try:
            if tx_type == "deposit":
                tx = deposit(bank, active_user, int(amount), desc)
            else:
                tx = spend(bank, active_user, int(amount), desc)

            save_json(BANK_PATH, bank)
            st.success(f"Recorded {tx_type} for {active_user}: {tx['amount']}")
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
# Codes (Variety mechanics)
# ----------------------------
elif view == "Codes":
    st.subheader("Codes Ledger")
    st.caption("Creates and tracks codes. Saves to `codes_ledger.json`.")

    c1, c2 = st.columns([1, 1])

    with c1:
        st.markdown("### Add a code")
        with st.form("add_code_form"):
            new_code = st.text_input("Code", placeholder="e.g., STAR-001")
            note = st.text_input("Note (optional)", placeholder="e.g., Reward, invite, drop…")
            add = st.form_submit_button("Add code")
        if add:
            try:
                add_code(ledger, new_code, note=note)
                save_json(CODES_PATH, ledger)
                st.success("Code added.")
                st.rerun()
            except Exception as e:
                st.error(f"{e}")

    with c2:
        st.markdown("### Mark code used")
        codes = [c.get("code") for c in ledger.get("codes", [])]
        with st.form("use_code_form"):
            if codes:
                pick = st.selectbox("Select code", options=codes)
            else:
                pick = ""
                st.info("No codes yet.")
            used_note = st.text_input("Use note (optional)")
            mark = st.form_submit_button("Mark used")
        if mark and pick:
            try:
                mark_code_used(ledger, pick, used_by=active_user, note=used_note)
                save_json(CODES_PATH, ledger)
                st.success("Marked used.")
                st.rerun()
            except Exception as e:
                st.error(f"{e}")

    st.markdown("### Ledger")
    rows = ledger.get("codes", [])
    if rows:
        st.dataframe(rows, use_container_width=True, hide_index=True)
    else:
        st.info("Ledger is empty.")

# ----------------------------
# Docs (Acuity)
# ----------------------------
elif view == "Docs":
    st.subheader("Docs")
    st.caption("Renders your markdown guides from the repo root.")

    tab1, tab2, tab3 = st.tabs(["rules.md", "currency.md", "users.md"])

    with tab1:
        txt = load_text_safe(RULES_MD)
        if txt:
            st.markdown(txt)
        else:
            st.info("No rules defined yet. Add content to `rules.md`.")

    with tab2:
        txt = load_text_safe(CURRENCY_MD)
        if txt:
            st.markdown(txt)
        else:
            st.info("No currency guide yet. Add content to `currency.md`.")

    with tab3:
        txt = load_text_safe(USERS_MD)
        if txt:
            st.markdown(txt)
        else:
            st.info("No users guide yet. Add content to `users.md`.")

# ----------------------------
# Admin (safe controls)
# ----------------------------
elif view == "Admin":
    st.subheader("Admin")
    st.caption("Safe utilities. These do not require terminal. Use carefully.")

    st.markdown("### Data status")
    st.code(
        f"Bank:  {os.path.basename(BANK_PATH)}\n"
        f"Codes: {os.path.basename(CODES_PATH)}\n"
        f"Users: {os.path.basename(USERS_PATH)}\n",
        language="text",
    )

    with st.expander("View raw JSON (read-only)", expanded=False):
        st.markdown("**careon_bank_v2.json**")
        st.json(bank)
        st.markdown("**codes_ledger.json**")
        st.json(ledger)
        st.markdown("**user_profile.json**")
        st.json(users_db)

    st.markdown("### Seed / Reset (explicit)")
    st.warning("These actions overwrite files. Use only if you truly want a reset.")

    colA, colB, colC = st.columns(3)

    with colA:
        if st.button("Reset bank to default"):
            bank = default_bank()
            save_json(BANK_PATH, bank)
            st.success("Bank reset.")
            st.rerun()

    with colB:
        if st.button("Reset codes to default"):
            ledger = default_codes()
            save_json(CODES_PATH, ledger)
            st.success("Codes reset.")
            st.rerun()

    with colC:
        if st.button("Reset users to default"):
            users_db = default_users()
            save_json(USERS_PATH, users_db)
            st.success("Users reset.")
            st.rerun()