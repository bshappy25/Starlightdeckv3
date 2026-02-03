# careon_bubble.py
import base64
import os
import streamlit as st


def _img_to_data_url(path: str) -> str:
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    # png assumed
    return f"data:image/png;base64,{b64}"


def render_careon_bubble():
    """
    Careon Bubble button (image-based).
    Click toggles st.session_state["show_market"].
    """

    st.session_state.setdefault("show_market", False)

    # ---- Configure your image path here (SAFE TO EDIT) ----
    img_path = os.path.join(os.path.dirname(__file__), "assets", "careon_badge.png")

    # Cache the data URL so we don’t re-encode every rerun
    if "careon_bubble_data_url" not in st.session_state:
        if not os.path.exists(img_path):
            st.warning("Careon bubble image missing: assets/careon_badge.png")
            return
        st.session_state["careon_bubble_data_url"] = _img_to_data_url(img_path)

    img_url = st.session_state["careon_bubble_data_url"]

    # ---- CSS (isolated) ----
    st.markdown(
        f"""
        <style>
        /* ===== Careon Bubble Button (Image) ===== */
        .careon-bubble-wrap {{
            display: flex;
            justify-content: flex-end;
            align-items: center;
            margin-top: 6px;
            margin-bottom: 10px;
        }}

        /* Target the button inside our wrap */
        .careon-bubble-wrap div[data-testid="stButton"] > button {{
            width: 220px !important;      /* adjust as needed */
            height: 64px !important;      /* adjust as needed */
            border-radius: 18px !important;
            border: 0 !important;
            background: transparent !important;

            background-image: url("{img_url}") !important;
            background-repeat: no-repeat !important;
            background-position: center !important;
            background-size: contain !important;

            box-shadow:
                0 0 18px rgba(180,130,255,0.55),
                0 0 32px rgba(120,220,210,0.35) !important;

            filter: drop-shadow(0 6px 18px rgba(246,193,119,0.35));
            transition: transform 0.12s ease, filter 0.12s ease;
            padding: 0 !important;
        }}

        /* Hide the button text (we use image) */
        .careon-bubble-wrap div[data-testid="stButton"] > button span {{
            opacity: 0 !important;
        }}

        /* Pulsating glow */
        @keyframes careonPulse {{
            0% {{
                transform: scale(1.0);
                box-shadow:
                    0 0 14px rgba(180,130,255,0.45),
                    0 0 24px rgba(120,220,210,0.25);
                filter: drop-shadow(0 6px 14px rgba(246,193,119,0.28));
            }}
            50% {{
                transform: scale(1.03);
                box-shadow:
                    0 0 22px rgba(180,130,255,0.75),
                    0 0 42px rgba(120,220,210,0.45);
                filter: drop-shadow(0 8px 20px rgba(246,193,119,0.42));
            }}
            100% {{
                transform: scale(1.0);
                box-shadow:
                    0 0 14px rgba(180,130,255,0.45),
                    0 0 24px rgba(120,220,210,0.25);
                filter: drop-shadow(0 6px 14px rgba(246,193,119,0.28));
            }}
        }}

        .careon-bubble-wrap div[data-testid="stButton"] > button {{
            animation: careonPulse 1.8s ease-in-out infinite;
        }}

        /* Hover */
        .careon-bubble-wrap div[data-testid="stButton"] > button:hover {{
            transform: translateY(-1px) scale(1.04);
            filter: drop-shadow(0 10px 26px rgba(246,193,119,0.55));
        }}

        .careon-bubble-wrap div[data-testid="stButton"] > button:active {{
            transform: scale(0.99);
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ---- UI ----
    st.markdown('<div class="careon-bubble-wrap">', unsafe_allow_html=True)
    clicked = st.button("CAREON", key="careon_bubble_open", help="Open Careon Market")
    st.markdown("</div>", unsafe_allow_html=True)

    if clicked:
        st.session_state["show_market"] = not st.session_state.get("show_market", False)
        st.rerun()
