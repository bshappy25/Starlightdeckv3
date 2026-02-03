# careon_bubble.py
import streamlit as st


C_LINE = "Ȼ"


def render_careon_bubble():
    """
    Safari-safe Careon Bubble + Ticker.
    - Ticker is purely visual: repeating phrase line.
    - Button is the reliable clickable control (toggles market).
    """

    st.session_state.setdefault("show_market", False)

    phrase = f"{C_LINE} Careon — the fund of the community — {C_LINE}"

    st.markdown(
        f"""
        <style>
        .careon-bubble-wrap {{
            display: flex;
            flex-direction: column;
            align-items: flex-end;
            gap: 8px;
            margin-top: 6px;
            margin-bottom: 10px;
        }}

        /* ===== Ticker ===== */
        .careon-ticker {{
            width: min(520px, 100%);
            overflow: hidden;
            border-radius: 14px;
            border: 1px solid rgba(255,255,255,0.18);
            background: rgba(255,255,255,0.05);
            box-shadow:
                0 0 12px rgba(180,130,255,0.25),
                0 0 22px rgba(120,220,210,0.18),
                inset 0 1px 0 rgba(255,255,255,0.10);
            padding: 10px 12px;
            position: relative;
        }}

        .careon-ticker::before {{
            content: "";
            position: absolute;
            inset: 0;
            background: radial-gradient(circle at 25% 20%,
                rgba(246,193,119,0.12) 0%,
                rgba(180,130,255,0.08) 40%,
                transparent 70%);
            pointer-events: none;
        }}

        .careon-ticker-track {{
            display: inline-flex;
            white-space: nowrap;
            gap: 22px;
            will-change: transform;
            animation: careonMarquee 12s linear infinite;
            font-weight: 900;
            letter-spacing: 0.08em;
            font-size: 0.85rem;
            opacity: 0.92;
        }}

        .careon-ticker-item {{
            color: rgba(245,245,247,0.85);
            text-shadow: 0 0 16px rgba(246,193,119,0.18);
        }}

        @keyframes careonMarquee {{
            0%   {{ transform: translateX(0); }}
            100% {{ transform: translateX(-50%); }}
        }}

        /* ===== Button styling (reliable on Safari) ===== */
        .careon-bubble-wrap div[data-testid="stButton"] > button {{
            border-radius: 18px !important;
            border: 1px solid rgba(255,255,255,0.22) !important;
            background: rgba(255,255,255,0.06) !important;

            box-shadow:
                0 0 14px rgba(180,130,255,0.45),
                0 0 28px rgba(120,220,210,0.28),
                inset 0 1px 0 rgba(255,255,255,0.10) !important;

            padding: 10px 14px !important;
            transition: transform 0.12s ease, filter 0.12s ease;
        }}

        @keyframes careonPulse {{
            0%   {{ transform: scale(1.0); filter: brightness(1.00); }}
            50%  {{ transform: scale(1.03); filter: brightness(1.07); }}
            100% {{ transform: scale(1.0); filter: brightness(1.00); }}
        }}

        .careon-bubble-wrap div[data-testid="stButton"] > button {{
            animation: careonPulse 1.9s ease-in-out infinite;
        }}

        .careon-bubble-wrap div[data-testid="stButton"] > button:hover {{
            transform: translateY(-1px) scale(1.04);
            filter: brightness(1.10);
        }}

        .careon-bubble-wrap div[data-testid="stButton"] > button:active {{
            transform: scale(0.99);
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="careon-bubble-wrap">', unsafe_allow_html=True)

    # Ticker bar (two copies so the animation loops cleanly)
    st.markdown(
        f"""
        <div class="careon-ticker">
            <div class="careon-ticker-track">
                <span class="careon-ticker-item">{phrase}</span>
                <span class="careon-ticker-item">{phrase}</span>
                <span class="careon-ticker-item">{phrase}</span>
                <span class="careon-ticker-item">{phrase}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Clickable control
    clicked = st.button("CAREON MARKET", key="careon_bubble_open", help="Open Careon Market")

    st.markdown("</div>", unsafe_allow_html=True)

    if clicked:
        st.session_state["show_market"] = not st.session_state.get("show_market", False)
        st.rerun()
