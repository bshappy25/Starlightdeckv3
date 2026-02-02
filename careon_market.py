# careon_market.py
import re
import streamlit as st


# ---- simple deposit code format ----
# Example: DEP-50-AB12CD  (amount=50, token=AB12CD)
DEP_RE = re.compile(r"^DEP-(\d{1,5})-([A-Z0-9]{4,16})$", re.IGNORECASE)


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


def render_market(bank_module, bank_path: str):
    """
    Premium Careon marketplace with glassmorphic design.
    Shows balance, placeholder packages, and deposit-code redemption.

    bank_module must implement:
      - load_bank(path) -> dict
      - save_bank(careon, path) -> None
      - deposit(careon, amount, path, note="...") -> None   (optional)
    """

    if not st.session_state.get("show_market", False):
        return

    # Load bank
    b = bank_module.load_bank(bank_path)
    balance = int(b.get("balance", 0))
    network_fund = int(b.get("sld_network_fund", 0))
    used_codes = set(b.get("used_deposit_codes", []))

    # Inject CSS once
    if not st.session_state.get("_careon_market_css"):
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
                margin: 1.2rem 0;
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
                font-size: 1.8rem;
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
                margin-bottom: 1.2rem;
                filter: drop-shadow(0 2px 8px rgba(246,193,119,0.3));
                position: relative;
                z-index: 2;
            }

            /* Balance display */
            .balance-shrine {
                background: rgba(255, 255, 255, 0.06);
                border: 1px solid rgba(246, 193, 119, 0.25);
                border-radius: 18px;
                padding: 1.2rem;
                margin-bottom: 1.5rem;
                text-align: center;
                box-shadow:
                    0 0 24px rgba(246, 193, 119, 0.15),
                    inset 0 1px 0 rgba(255, 255, 255, 0.08);
                position: relative;
                z-index: 2;
            }

            .balance-label {
                font-size: 0.9rem;
                color: rgba(245, 245, 247, 0.75);
                letter-spacing: 0.08em;
                text-transform: uppercase;
                margin-bottom: 0.4rem;
            }

            .balance-amount {
                font-size: 2.4rem;
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
                grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
                gap: 1rem;
                margin: 1.5rem 0;
                position: relative;
                z-index: 2;
            }

            .package-card {
                background: rgba(255, 255, 255, 0.04);
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 16px;
                padding: 1.2rem 0.9rem;
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
                font-size: 1.8rem;
                font-weight: 900;
                color: #ffd27a;
                margin-bottom: 0.3rem;
            }

            .package-price {
                font-size: 0.85rem;
                color: rgba(245, 245, 247, 0.70);
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
                margin: 1.5rem 0;
                position: relative;
                z-index: 2;
            }

            /* Info */
            .market-info {
                text-align: center;
                font-size: 0.88rem;
                color: rgba(245, 245, 247, 0.70);
                line-height: 1.5;
                margin-top: 1rem;
                position: relative;
                z-index: 2;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        st.session_state["_careon_market_css"] = True

    # ---------- UI ----------
    st.markdown('<div class="market-palace">', unsafe_allow_html=True)
    st.markdown('<div class="market-title">✦ CAREON MARKET ✦</div>', unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="balance-shrine">
            <div class="balance-label">Your Balance</div>
            <div class="balance-amount">{balance} Ȼ</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("#### Purchase Careons")
    st.markdown(
        """
        <div class="package-grid">
            <div class="package-card">
                <div class="package-amount">25 Ȼ</div>
                <div class="package-price">Coming Soon</div>
            </div>
            <div class="package-card">
                <div class="package-amount">50 Ȼ</div>
                <div class="package-price">Coming Soon</div>
            </div>
            <div class="package-card">
                <div class="package-amount">100 Ȼ</div>
                <div class="package-price">Coming Soon</div>
            </div>
            <div class="package-card">
                <div class="package-amount">250 Ȼ</div>
                <div class="package-price">Coming Soon</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="market-divider"></div>', unsafe_allow_html=True)

    st.markdown("#### Redeem Deposit Code")
    col1, col2 = st.columns([3, 1])

    with col1:
        code_input = st.text_input(
            "Enter code",
            placeholder="DEP-50-AB12CD",
            key="market_code_input",
            label_visibility="collapsed"
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

            # Basic guardrails
            if amount <= 0:
                st.error("Invalid amount.")
            elif amount > 5000:
                st.error("That deposit amount is too large.")
            elif norm_code in used_codes:
                st.error("That deposit code was already redeemed.")
            else:
                # 5% to network fund
                network_cut = max(1, int(round(amount * 0.05))) if amount >= 20 else 0
                user_credit = amount - network_cut

                b["balance"] = int(b.get("balance", 0)) + user_credit
                b["sld_network_fund"] = int(b.get("sld_network_fund", 0)) + network_cut

                # Track used code
                b.setdefault("used_deposit_codes", [])
                b["used_deposit_codes"].append(norm_code)

                # Optional: add to history if your bank supports it
                hist = b.setdefault("history", [])
                hist.append({
                    "kind": "deposit_code",
                    "code": norm_code,
                    "amount": amount,
                    "credited": user_credit,
                    "network_cut": network_cut,
                })

                bank_module.save_bank(b, bank_path)

                st.success(f"Redeemed {amount} Ȼ → +{user_credit} Ȼ to you, +{network_cut} Ȼ to SLD Network Fund.")
                st.rerun()

    # Footer
    st.markdown(
        f"""
        <div class="market-info">
            🌐 SLD Network Fund: {network_fund} Ȼ<br/>
            <em>5% of all deposits support the community</em>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

    # Close button
    if st.button("✕ Close Market", key="market_close_btn"):
        st.session_state["show_market"] = False
        st.rerun()
