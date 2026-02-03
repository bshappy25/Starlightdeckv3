# careon_market.py
import re
from datetime import datetime, timezone

import streamlit as st


C_LINE = "Ȼ"  # Careon currency symbol

# ---- simple deposit code format ----
# Example: DEP-50-AB12CD  (amount=50, token=AB12CD)
DEP_RE = re.compile(r"^DEP-(\d{1,5})-([A-Z0-9]{4,16})$", re.IGNORECASE)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _parse_deposit_code(code: str):
    if not code:
        return None
    code = code.strip()
    m = DEP_RE.match(code)
    if not m:
        return None
    amount = int(m.group(1))
    token = m.group(2).upper()
    return amount, token


def _get_user_balance(bank: dict, user_id: str) -> int:
    bank.setdefault("balances_by_user", {})
    return int(bank["balances_by_user"].get(user_id, 0))


def _set_user_balance(bank: dict, user_id: str, value: int):
    bank.setdefault("balances_by_user", {})
    bank["balances_by_user"][user_id] = int(value)


def _fallback_deposit_like_main_app(bank: dict, user_id: str, amount: int, description: str = ""):
    """
    Fallback deposit implementation matching your Branch B rules:
    - Deposit adds to BOTH global + personal
    - Adds to total_earned
    - Records a tx
    """
    amount = int(amount)
    if amount <= 0:
        raise ValueError("Deposit amount must be greater than 0.")

    bank["balance"] = int(bank.get("balance", 0)) + amount
    _set_user_balance(bank, user_id, _get_user_balance(bank, user_id) + amount)

    bank["total_earned"] = int(bank.get("total_earned", 0)) + amount

    tx = {
        "ts": _now_iso(),
        "user_id": user_id,
        "type": "deposit",
        "amount": amount,
        "description": (description or "").strip(),
    }
    bank.setdefault("txs", [])
    bank["txs"].insert(0, tx)
    bank.setdefault("meta", {})
    bank["meta"]["updated_at"] = _now_iso()
    return tx


def render_market(
    bank: dict,
    active_user: str,
    *,
    deposit_fn=None,
    save_fn=None,
):
    """
    Premium Careon marketplace with glassmorphic design + purchase placeholders + deposit-code redemption.

    Parameters:
      bank (dict): your loaded careon_bank_v2.json structure (already in memory)
      active_user (str): current user id from sidebar

    Optional (recommended):
      deposit_fn: function(bank, user_id, amount, description="") -> tx
                 (use your main app deposit() to keep totals/txs consistent)
      save_fn: function() -> None
               a callback that persists bank to JSON (e.g., lambda: save_json(BANK_PATH, bank))

    Behavior:
      - Market only renders if st.session_state["show_market"] is True
      - Deposit codes credit global + personal (like a deposit)
      - 🌍 SLD fund remains read-only / intentional-only (no auto addition)
    """

    if not st.session_state.get("show_market", False):
        return

    # CSS injection once
    if not st.session_state.get("_careon_market_css", False):
        st.markdown(
            """
            <style>
            /* ========== MARKET CONTAINER ========== */
            .market-palace {
                background: linear-gradient(
                    135deg,
                    rgba(180, 130, 255, 0.08) 0%,
                    rgba(120, 220, 210, 0.06) 100%
                );
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 24px;
                padding: 1.8rem 2rem;
                margin: 0.75rem 0 1.2rem 0;
                backdrop-filter: blur(16px);
                box-shadow:
                    0 12px 48px rgba(0, 0, 0, 0.25),
                    inset 0 1px 0 rgba(255, 255, 255, 0.10);
                position: relative;
                overflow: hidden;
            }

            /* Ambient light effect */
            .market-palace::before {
                content: '';
                position: absolute;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: radial-gradient(
                    circle,
                    rgba(246, 193, 119, 0.08) 0%,
                    transparent 50%
                );
                animation: ambientRotate 20s linear infinite;
                pointer-events: none;
            }

            @keyframes ambientRotate {
                from { transform: rotate(0deg); }
                to { transform: rotate(360deg); }
            }

            /* Title */
            .market-title {
                font-size: 1.65rem;
                font-weight: 900;
                letter-spacing: 0.15em;
                text-align: center;
                background: linear-gradient(
                    135deg,
                    #ffd27a 0%,
                    #b482ff 50%,
                    #78dcd2 100%
                );
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                margin-bottom: 1.0rem;
                filter: drop-shadow(0 2px 8px rgba(246,193,119,0.3));
                position: relative;
                z-index: 2;
            }

            /* Balance display */
            .balance-shrine {
                background: rgba(255, 255, 255, 0.06);
                border: 1px solid rgba(246, 193, 119, 0.25);
                border-radius: 18px;
                padding: 1.05rem;
                margin-bottom: 1.25rem;
                text-align: center;
                box-shadow:
                    0 0 24px rgba(246, 193, 119, 0.15),
                    inset 0 1px 0 rgba(255, 255, 255, 0.08);
                position: relative;
                z-index: 2;
            }

            .balance-label {
                font-size: 0.85rem;
                color: rgba(245, 245, 247, 0.75);
                letter-spacing: 0.08em;
                text-transform: uppercase;
                margin-bottom: 0.35rem;
            }

            .balance-amount {
                font-size: 2.15rem;
                font-weight: 950;
                color: #ffd27a;
                letter-spacing: 0.08em;
                text-shadow:
                    0 0 24px rgba(246, 193, 119, 0.60),
                    0 2px 4px rgba(0, 0, 0, 0.40);
            }

            /* Package cards */
            .package-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
                gap: 1rem;
                margin: 1.0rem 0 0.6rem 0;
                position: relative;
                z-index: 2;
            }

            .package-card {
                background: rgba(255, 255, 255, 0.04);
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 16px;
                padding: 1.05rem 0.95rem;
                text-align: center;
                transition: all 0.25s ease;
                cursor: default;
            }

            .package-card:hover {
                background: rgba(255, 255, 255, 0.08);
                border-color: rgba(246, 193, 119, 0.40);
                transform: translateY(-3px);
                box-shadow: 0 8px 24px rgba(246, 193, 119, 0.25);
            }

            .package-amount {
                font-size: 1.55rem;
                font-weight: 900;
                color: #ffd27a;
                margin-bottom: 0.2rem;
            }

            .package-price {
                font-size: 0.85rem;
                color: rgba(245, 245, 247, 0.72);
            }

            /* Divider */
            .market-divider {
                height: 1px;
                background: linear-gradient(
                    90deg,
                    transparent,
                    rgba(255, 255, 255, 0.15) 50%,
                    transparent
                );
                margin: 1.25rem 0;
                position: relative;
                z-index: 2;
            }

            /* Info */
            .market-info {
                text-align: center;
                font-size: 0.88rem;
                color: rgba(245, 245, 247, 0.70);
                line-height: 1.5;
                margin-top: 0.9rem;
                position: relative;
                z-index: 2;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        st.session_state["_careon_market_css"] = True

    # Derived values
    global_balance = int(bank.get("balance", 0))
    network_fund = int(bank.get("sld_network_fund", 0))
    my_balance = _get_user_balance(bank, active_user)
    used_codes = set(bank.get("used_deposit_codes", []))

    # Pick deposit engine
    do_deposit = deposit_fn if deposit_fn is not None else _fallback_deposit_like_main_app

    # ---------- UI ----------
    st.markdown('<div class="market-palace">', unsafe_allow_html=True)
    st.markdown('<div class="market-title">✦ CAREON MARKET ✦</div>', unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="balance-shrine">
            <div class="balance-label">My Balance</div>
            <div class="balance-amount">{my_balance} {C_LINE}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Quick line of world stats
    c1, c2, c3 = st.columns(3)
    c1.metric(f"Global ({C_LINE})", global_balance)
    c2.metric(f"🌍 Fund ({C_LINE})", network_fund)
    c3.caption(f"User: **{active_user}**")

    # ============================
    # PURCHASE PLACEHOLDERS
    # ============================
    st.markdown("#### Purchase Careons")

    packages = [
        {"name": "Explorer Pack", "usd": 4.99, "careon": 500},
        {"name": "Voyager Pack", "usd": 9.99, "careon": 1200},
        {"name": "Frontier Pack", "usd": 19.99, "careon": 2600},
        {"name": "Zenith Pack", "usd": 49.99, "careon": 7200},
    ]

    # Stylish cards (your style), with real selection below
    st.markdown(
        f"""
        <div class="package-grid">
            <div class="package-card">
                <div class="package-amount">{packages[0]['careon']} {C_LINE}</div>
                <div class="package-price">${packages[0]['usd']:.2f} • {packages[0]['name']}</div>
            </div>
            <div class="package-card">
                <div class="package-amount">{packages[1]['careon']} {C_LINE}</div>
                <div class="package-price">${packages[1]['usd']:.2f} • {packages[1]['name']}</div>
            </div>
            <div class="package-card">
                <div class="package-amount">{packages[2]['careon']} {C_LINE}</div>
                <div class="package-price">${packages[2]['usd']:.2f} • {packages[2]['name']}</div>
            </div>
            <div class="package-card">
                <div class="package-amount">{packages[3]['careon']} {C_LINE}</div>
                <div class="package-price">${packages[3]['usd']:.2f} • {packages[3]['name']}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    labels = [f"{p['name']} — ${p['usd']:.2f} → {p['careon']} {C_LINE}" for p in packages]
    choice = st.selectbox("Select a package (placeholder)", labels, index=0, key="market_pkg_select")
    pkg = packages[labels.index(choice)]

    left, right = st.columns(2)
    with left:
        st.markdown("**Stripe (placeholder)**")
        st.info("Stripe checkout will be wired later.")
        if st.button("Pay with Stripe", key="stripe_placeholder", use_container_width=True):
            st.warning("Stripe is not connected yet. (Placeholder)")

    with right:
        st.markdown("**PayPal (placeholder)**")
        st.info("PayPal checkout will be wired later.")
        if st.button("Pay with PayPal", key="paypal_placeholder", use_container_width=True):
            st.warning("PayPal is not connected yet. (Placeholder)")

    st.caption(
        f"Selected: **{pkg['name']}** • ${pkg['usd']:.2f} • would grant **{pkg['careon']} {C_LINE}** after verified payment."
    )

    st.markdown('<div class="market-divider"></div>', unsafe_allow_html=True)

    # ============================
    # DEPOSIT CODE REDEMPTION
    # ============================
    st.markdown("#### Redeem Deposit Code")
    st.caption(f"Format: DEP-<amount>-<token> (example: DEP-50-AB12CD) • Credits add to **global + personal**.")

    col1, col2 = st.columns([3, 1])
    with col1:
        code_input = st.text_input(
            "Enter code",
            placeholder="DEP-50-AB12CD",
            key="market_code_input",
            label_visibility="collapsed",
        )

    with col2:
        redeem_btn = st.button("Redeem", key="market_redeem_btn", use_container_width=True)

    if redeem_btn:
        raw = (code_input or "").strip()
        parsed = _parse_deposit_code(raw)

        if not raw:
            st.warning("Enter a deposit code first.")
        elif not parsed:
            st.error("Invalid code format. Use DEP-<amount>-<token> (example: DEP-50-AB12CD).")
        else:
            amount, token = parsed
            norm_code = f"DEP-{amount}-{token}"

            # Guardrails
            if amount <= 0:
                st.error("Invalid amount.")
            elif amount > 5000:
                st.error("That deposit amount is too large.")
            elif norm_code in used_codes:
                st.error("That deposit code was already redeemed.")
            else:
                # Credit as a deposit under your Branch B rules (global + personal)
                try:
                    do_deposit(bank, active_user, amount, description=f"Deposit code redeemed: {norm_code}")
                except Exception as e:
                    st.error(f"Could not apply deposit: {e}")
                else:
                    bank.setdefault("used_deposit_codes", [])
                    bank["used_deposit_codes"].append(norm_code)

                    hist = bank.setdefault("history", [])
                    hist.append(
                        {
                            "ts": _now_iso(),
                            "kind": "deposit_code",
                            "code": norm_code,
                            "amount": amount,
                            "user_id": active_user,
                            "note": "Credited to global + personal. No auto network fund.",
                        }
                    )

                    # Persist if a save function is provided
                    if save_fn is not None:
                        save_fn()

                    st.success(f"Redeemed {amount} {C_LINE} → credited to **you + global**.")
                    st.rerun()

    # Footer
    st.markdown(
        f"""
        <div class="market-info">
            🌍 SLD Network Fund: {network_fund} {C_LINE}<br/>
            <em>Fund changes are intentional-only (no automatic cuts).</em>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)

    # Close button
    if st.button("✕ Close Market", key="market_close_btn"):
        st.session_state["show_market"] = False
        st.rerun()
