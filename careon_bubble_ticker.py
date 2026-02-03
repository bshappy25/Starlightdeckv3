# careon_bubble_ticker.py
import streamlit as st

C_LINE = "Ȼ"


def render_careon_ticker():
    phrase = f"{C_LINE} Careon — the fund of the community — {C_LINE}"

    st.markdown(
        f"""
        <style>
        .careon-ticker-wrap {{
            display: flex;
            justify-content: flex-end;
            margin-top: 6px;
            margin-bottom: 8px;
        }}

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
        </style>

        <div class="careon-ticker-wrap">
            <div class="careon-ticker">
                <div class="careon-ticker-track">
                    <span class="careon-ticker-item">{phrase}</span>
                    <span class="careon-ticker-item">{phrase}</span>
                    <span class="careon-ticker-item">{phrase}</span>
                    <span class="careon-ticker-item">{phrase}</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
