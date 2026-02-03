import streamlit as st

def render_careon_bubble():
    """
    Glowing Careon Bubble button.
    Click opens (toggles) market mode via st.session_state["show_market"].
    Designed to be visually isolated from core app logic.
    """

    # Local CSS for the bubble only
    st.markdown(
        """
        <style>
        /* ===== Careon Bubble (isolated styling) ===== */
        .careon-bubble-wrap {
            display: flex;
            justify-content: flex-end;
            align-items: center;
            margin-top: 6px;
            margin-bottom: 10px;
        }

        .careon-bubble-btn > button {
            width: 56px !important;
            height: 56px !important;
            border-radius: 999px !important;
            border: 1px solid rgba(255,255,255,0.25) !important;
            background: radial-gradient(circle at 30% 30%,
                rgba(190, 150, 255, 0.95) 0%,
                rgba(120, 220, 210, 0.55) 35%,
                rgba(40, 60, 120, 0.25) 75%
            ) !important;

            box-shadow:
                0 0 14px rgba(190,150,255,0.55),
                0 0 26px rgba(120,220,210,0.35),
                inset 0 0 10px rgba(255,255,255,0.20) !important;

            transition: transform 0.12s ease, box-shadow 0.12s ease, filter 0.12s ease;
            padding: 0 !important;
            font-size: 22px !important;
        }

        .careon-bubble-btn > button:hover {
            transform: translateY(-1px) scale(1.03);
            filter: brightness(1.08);
            box-shadow:
                0 0 18px rgba(190,150,255,0.70),
                0 0 34px rgba(120,220,210,0.45),
                inset 0 0 12px rgba(255,255,255,0.25) !important;
        }

        .careon-bubble-btn > button:active {
            transform: translateY(0px) scale(0.98);
        }

        /* Hide Streamlit button label spacing */
        .careon-bubble-btn div[data-testid="stButton"] {
            margin: 0 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.session_state.setdefault("show_market", False)

    # Right-aligned bubble
    st.markdown('<div class="careon-bubble-wrap">', unsafe_allow_html=True)
    clicked = st.button("🫧", key="careon_bubble_open", help="Open Careon Market", type="secondary")
    st.markdown("</div>", unsafe_allow_html=True)

    # Toggle market mode
    if clicked:
        st.session_state["show_market"] = not st.session_state.get("show_market", False)
        st.rerun()
