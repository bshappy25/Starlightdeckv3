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
    img_path = os.path.join(os.path.dirname(__file__), "assets", "images", "ui", "careon_badge.png")


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
    /* ===== Careon Bubble Button (Image-based, FIXED) ===== */

    .careon-bubble-wrap {{
        display: flex;
        justify-content: flex-end;
        margin-top: 6px;
        margin-bottom: 10px;
    }}

    /* Target the ACTUAL button */
    .careon-bubble-wrap button {{
        all: unset !important;
        cursor: pointer !important;

        width: 240px;
        height: 72px;

        background-image: url("{img_url}") !important;
        background-repeat: no-repeat !important;
        background-position: center !important;
        background-size: contain !important;

        border-radius: 20px;
        display: block;

        /* Glow */
        box-shadow:
            0 0 22px rgba(246,193,119,0.6),
            0 0 38px rgba(180,130,255,0.45),
            0 0 64px rgba(120,220,210,0.35);

        animation: careonPulse 1.8s ease-in-out infinite;
    }}

    /* Kill Streamlit's internal button div */
    .careon-bubble-wrap button > div {{
        display: none !important;
    }}

    @keyframes careonPulse {{
        0% {{
            transform: scale(1.0);
            filter: drop-shadow(0 6px 16px rgba(246,193,119,0.35));
        }}
        50% {{
            transform: scale(1.04);
            filter: drop-shadow(0 10px 28px rgba(246,193,119,0.55));
        }}
        100% {{
            transform: scale(1.0);
            filter: drop-shadow(0 6px 16px rgba(246,193,119,0.35));
        }}
    }}

    .careon-bubble-wrap button:hover {{
        transform: scale(1.06);
    }}

    .careon-bubble-wrap button:active {{
        transform: scale(0.98);
    }}
    </style>
    """,
    unsafe_allow_html=True
)


    # ---- UI ----
    st.markdown('<div class="careon-bubble-wrap">', unsafe_allow_html=True)
    clicked = st.button("CAREON", key="careon_bubble_open", help="Open Careon Market")
    st.markdown("</div>", unsafe_allow_html=True)

    if clicked:
        st.session_state["show_market"] = not st.session_state.get("show_market", False)
        st.rerun()
