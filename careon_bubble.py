# careon_bubble.py
import base64
import os
import streamlit as st


def _img_to_data_url(path: str) -> str:
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    return f"data:image/png;base64,{b64}"


def render_careon_bubble():
    """
    Safari-safe Careon Bubble.
    - Always renders a working button.
    - Tries to show your badge image inside the button.
    - If image styling fails, it still looks acceptable (glowy box).
    - Click toggles st.session_state["show_market"].
    """

    st.session_state.setdefault("show_market", False)

    # Path to your badge image in assets/images/ui/
    img_path = os.path.join(os.path.dirname(__file__), "assets", "images", "ui", "careon_badge.png")

    # Create data URL if possible (cache)
    if "careon_badge_data_url" not in st.session_state:
        if os.path.exists(img_path):
            try:
                st.session_state["careon_badge_data_url"] = _img_to_data_url(img_path)
            except Exception:
                st.session_state["careon_badge_data_url"] = None
        else:
            st.session_state["careon_badge_data_url"] = None

    img_url = st.session_state.get("careon_badge_data_url")

    # CSS: Keep simple, minimize Safari weirdness.
    # We style the container + the image, not the button background.
    st.markdown(
        """
        <style>
        .careon-bubble-wrap {
            display: flex;
            justify-content: flex-end;
            align-items: center;
            margin-top: 6px;
            margin-bottom: 10px;
        }

        /* Make the Streamlit button look like a pill */
        .careon-bubble-wrap div[data-testid="stButton"] > button {
            border-radius: 18px !important;
            border: 1px solid rgba(255,255,255,0.22) !important;
            background: rgba(255,255,255,0.06) !important;

            box-shadow:
                0 0 14px rgba(180,130,255,0.45),
                0 0 28px rgba(120,220,210,0.28),
                inset 0 1px 0 rgba(255,255,255,0.10) !important;

            padding: 10px 14px !important;
            transition: transform 0.12s ease, filter 0.12s ease;
        }

        /* Gentle pulse that Safari usually respects */
        @keyframes careonPulse {
            0%   { transform: scale(1.0); filter: brightness(1.00); }
            50%  { transform: scale(1.03); filter: brightness(1.07); }
            100% { transform: scale(1.0); filter: brightness(1.00); }
        }

        .careon-bubble-wrap div[data-testid="stButton"] > button {
            animation: careonPulse 1.9s ease-in-out infinite;
        }

        .careon-bubble-wrap div[data-testid="stButton"] > button:hover {
            transform: translateY(-1px) scale(1.04);
            filter: brightness(1.10);
        }

        .careon-bubble-wrap div[data-testid="stButton"] > button:active {
            transform: scale(0.99);
        }

        /* Inside layout */
        .careon-bubble-inner {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .careon-badge-img {
            height: 40px;
            width: auto;
            display: block;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(246,193,119,0.25);
        }

        .careon-bubble-text {
            font-weight: 900;
            letter-spacing: 0.12em;
            font-size: 0.95rem;
        }

        .careon-bubble-sub {
            font-size: 0.78rem;
            opacity: 0.75;
            margin-top: 2px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="careon-bubble-wrap">', unsafe_allow_html=True)

    # We render a normal Streamlit button (most reliable),
    # and place an HTML preview right above it so you still see the badge.
    # This avoids Safari issues with button background images.
    if img_url:
        st.markdown(
            f"""
            <div class="careon-bubble-inner" style="justify-content:flex-end; margin-bottom:6px;">
                <img class="careon-badge-img" src="{img_url}" alt="CAREON" />
            </div>
            """,
            unsafe_allow_html=True,
        )

    # The actual clickable button (reliable on Safari)
    clicked = st.button("CAREON MARKET", key="careon_bubble_open", help="Open Careon Market")

    st.markdown("</div>", unsafe_allow_html=True)

    if clicked:
        st.session_state["show_market"] = not st.session_state.get("show_market", False)
        st.rerun()
