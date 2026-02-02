# =========================
# Standard library
# =========================
import os
import time
import random
from collections import Counter

# =========================
# Third-party
# =========================
import requests
import streamlit as st
import ui_header
ui_header.render_header(["Clarity over noise", "Action beats fear", "Curiosity first"])

import careon_bubble

careon_bubble.render_bubble()

if st.session_state.get("show_market"):
    st.subheader("Careon Market")
    # render market UI here

#import careon_market
#import careon_bank as bank

#careon_market.render_market(bank_module=bank, bank_path="careon_bank_v2.json")

# =========================
# Local app modules (root)
# =========================
import user_profile as profile
#import careon_bank as bank

# =========================
# Optional utils (safe to expand later)
# =========================
# from utils.ai import ask_ai
# from utils.deck import draw_card, zenith_check
# from utils.stats import init_stats

# =========================
# CONFIG
# =========================
MODEL_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent"
FORCE_ZENITH_SYMBOL = "◇"
ZENITH_CHANCE_PERCENT = 5

DRAW_10 = 10
DRAW_20 = 20


# =========================
# DECK DEFINITIONS
# =========================
CARDS = {
    "acuity":  {"name": "ACUITY",  "emoji": "🔵"},
    "valor":   {"name": "VALOR",   "emoji": "🔴"},
    "variety": {"name": "VARIETY", "emoji": "🟡"},
}

LEVELS = {
    1: {"name": "Common",    "weight": 75},
    2: {"name": "Rare",      "weight": 20},
    3: {"name": "Legendary", "weight": 5},
}


# =========================
# HELPERS
# =========================
def get_api_key() -> str:
    """
    Prefer Streamlit Secrets. Falls back to env var.
    In Streamlit Community Cloud, set:
      Settings -> Secrets:
        GEMINI_API_KEY="..."
    """
    key = st.secrets.get("GEMINI_API_KEY", "") if hasattr(st, "secrets") else ""
    if not key:
        key = os.getenv("GEMINI_API_KEY", "")
    return key.strip()


def ask_ai(prompt: str, retries: int = 2) -> str:
    api_key = get_api_key()
    if not api_key:
        return "[AI error] Missing GEMINI_API_KEY. Add it to Streamlit secrets or env var."

    headers = {"Content-Type": "application/json", "x-goog-api-key": api_key}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    last_err = None
    for attempt in range(retries + 1):
        try:
            r = requests.post(MODEL_URL, headers=headers, json=payload, timeout=(10, 90))
            if r.status_code != 200:
                last_err = f"HTTP {r.status_code}: {r.text[:200]}"
            else:
                data = r.json()
                return data["candidates"][0]["content"]["parts"][0]["text"]
        except requests.exceptions.Timeout:
            last_err = "Timeout (API/network slow)."
        except Exception as e:
            last_err = f"{type(e).__name__}: {e}"

        time.sleep(0.8 * (attempt + 1))

    return f"[AI error] {last_err}"


def get_vibe_fields(vibe: str, level: int, zenith: bool) -> dict:
    base = {
        "acuity": {
            1: ("Clarity", "Reduce noise.", "Truth over comfort."),
            2: ("Insight", "See structure.", "Depth and precision."),
            3: ("Revelation", "Cut illusion.", "Crystalline wisdom."),
        },
        "valor": {
            1: ("Courage", "Act once.", "Action beats fear."),
            2: ("Resolve", "Commit fully.", "Strength with purpose."),
            3: ("Command", "Lead boldly.", "Transform through will."),
        },
        "variety": {
            1: ("Play", "Try new paths.", "Curiosity first."),
            2: ("Surprise", "Break pattern.", "Creative risk."),
            3: ("Wonder", "Transcend limits.", "Reality bending."),
        },
    }

    i, g, v = base[vibe][level]
    if zenith:
        i = f"ZENITH: {i}"
        g = "Focus intention."
        v = "Alignment creates power."

    return {"Intention": i, "Personal goal": g, "Affixing value": v}


def draw_card():
    vibe = random.choice(list(CARDS.keys()))
    roll = random.randint(1, 100)
    if roll <= 75:
        return vibe, 1
    elif roll <= 95:
        return vibe, 2
    return vibe, 3


def zenith_check(forced: bool):
    if forced:
        return True, True
    return (random.randint(1, 100) <= ZENITH_CHANCE_PERCENT), False


def init_session():
    st.session_state.setdefault("careon", None)
    st.session_state.setdefault("user", None)
    st.session_state.setdefault("stats", {
        "draws": 0,
        "vibe": Counter({"acuity": 0, "valor": 0, "variety": 0}),
        "level": Counter({1: 0, 2: 0, 3: 0}),
        "zenith": 0,
        "zenith_forced": 0,
    })
    st.session_state.setdefault("last_card", None)
    st.session_state.setdefault("history", [])
    st.session_state.setdefault("ai_10_done", False)
    st.session_state.setdefault("ai_20_done", False)
    st.session_state.setdefault("final_done", False)


def render_ratio_bar(label: str, value: int, total: int):
    pct = (value / total * 100) if total else 0
    st.write(f"**{label}**: {value} ({pct:.0f}%)")
    st.progress(min(max(pct / 100, 0.0), 1.0))


def estrella_header(text="✨ Estrella ✨"):
    st.markdown(
        f"""
        <div style="font-weight:800; color:#caa7ff; font-size:1.1rem;">
            {text}
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================
# LOAD USER + BANK
# =========================
def bootstrap_user_and_bank():
    # User
    if st.session_state.user is None:
        # Expecting profile.get_or_create_user() -> (user, vibe) OR just user dict
        try:
            out = profile.get_or_create_user()
            if isinstance(out, tuple) and len(out) == 2:
                user, _vibe = out
            else:
                user = out
            st.session_state.user = user
        except Exception as e:
            st.session_state.user = {"name": "Player"}
            st.warning(f"User profile module fallback: {e}")

    # Bank
    if st.session_state.careon is None:
        try:
            careon = bank.load_bank()
            st.session_state.careon = careon

            # Daily bonus
            try:
                got_bonus = bank.check_daily_bonus(careon)
                if got_bonus:
                    st.success("✨ Daily bonus! +10 Ȼ")
            except Exception:
                pass

        except Exception as e:
            st.session_state.careon = {"balance": 0}
            st.warning(f"Bank module fallback: {e}")


def start_round_if_needed():
    """
    Starts a round once per session (charges -1 unless TGIF bypass).
    We keep a flag so we don’t charge repeatedly on reruns.
    """
    st.session_state.setdefault("round_started", False)
    st.session_state.setdefault("tgif_bypass", False)

    careon = st.session_state.careon

    if st.session_state.round_started:
        return

    # If bank has helper functions, use them; otherwise do basic balance check.
    can_afford = True
    try:
        can_afford = bank.can_start_round(careon.get("balance", 0))
    except Exception:
        can_afford = careon.get("balance", 0) >= 1

    if can_afford:
        try:
            bank.charge_round(careon)
            st.info(f"-1 Ȼ to start | Balance: {careon.get('balance', 0)}")
        except Exception:
            careon["balance"] = max(0, careon.get("balance", 0) - 1)
            st.info(f"-1 Ȼ to start | Balance: {careon.get('balance', 0)}")

        st.session_state.round_started = True
        return

    # Not enough: TGIF bypass gate
    st.warning("Insufficient Careons to start a paid round.")
    code = st.text_input("Enter TGIF to play free:", type="default")
    if code.strip().upper() == "TGIF":
        st.session_state.tgif_bypass = True
        st.session_state.round_started = True
        st.success("TGIF bypass activated! (free round)")
    else:
        st.stop()


# =========================
# MAIN UI
# =========================
def main():
    st.set_page_config(page_title="Starlight Deck", page_icon="⭐", layout="centered")
    init_session()
    bootstrap_user_and_bank()
    start_round_if_needed()

    user = st.session_state.user or {"name": "Player"}
    careon = st.session_state.careon
    stats = st.session_state.stats

    st.title("⭐ Starlight Deck")
    st.caption("Normal is deliberate. Rapid is a gamble.")

    # Top status
    c1, c2 = st.columns(2)
    with c1:
        st.write(f"**Player:** {user.get('name', 'Player')}")
        st.write(f"**Draws:** {stats['draws']}")
    with c2:
        st.write(f"**Balance:** {careon.get('balance', 0)} Ȼ")
        st.write(f"**Zenith:** {stats['zenith']} (forced {stats['zenith_forced']})")

    st.divider()

    # Ratios
    st.subheader("Session Ratios")
    total = stats["draws"]
    render_ratio_bar("🔵 Acuity", stats["vibe"]["acuity"], total)
    render_ratio_bar("🔴 Valor", stats["vibe"]["valor"], total)
    render_ratio_bar("🟡 Variety", stats["vibe"]["variety"], total)

    st.divider()

    # Prompt area
    st.subheader("Draw a Card")
    q = st.text_input(
        f"Ask (optional). Add {FORCE_ZENITH_SYMBOL} to force Zenith.",
        key="question_input",
        placeholder=f"Type a thought... (use {FORCE_ZENITH_SYMBOL} to force Zenith)"
    )

    draw = st.button("Draw", type="primary", use_container_width=True)

    if draw:
        vibe, level = draw_card()
        forced = FORCE_ZENITH_SYMBOL in (q or "")
        zenith, forced_flag = zenith_check(forced)

        stats["draws"] += 1
        stats["vibe"][vibe] += 1
        stats["level"][level] += 1
        if zenith:
            stats["zenith"] += 1
        if forced_flag:
            stats["zenith_forced"] += 1

        fields = get_vibe_fields(vibe, level, zenith)
        card_meta = CARDS[vibe]
        level_meta = LEVELS[level]

        st.session_state.last_card = {
            "vibe": vibe,
            "level": level,
            "zenith": zenith,
            "fields": fields,
        }

        st.session_state.history.append({
            "n": stats["draws"],
            "vibe": vibe,
            "level": level,
            "zenith": zenith
        })

        # Clear the input on draw (cosmetic)
        st.session_state.question_input = ""

    # Show last card
    if st.session_state.last_card:
        last = st.session_state.last_card
        vibe = last["vibe"]
        level = last["level"]
        zenith = last["zenith"]
        fields = last["fields"]

        card_meta = CARDS[vibe]
        level_meta = LEVELS[level]

        st.subheader("Latest Card")
        z_txt = "◇ ZENITH ◇" if zenith else ""

        st.markdown(
            f"""
            <div style="
                border:1px solid rgba(255,255,255,0.12);
                border-radius:16px;
                padding:14px 16px;
                background: rgba(255,255,255,0.04);
            ">
              <div style="font-size:1.2rem; font-weight:800;">
                {card_meta['emoji']} {card_meta['name']}
              </div>
              <div style="opacity:0.85; margin-top:4px;">
                Level {level} — {level_meta['name']} &nbsp;&nbsp; <span style="opacity:0.9;">{z_txt}</span>
              </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")
        for k, v in fields.items():
            st.write(f"**{k}:** {v}")

    st.divider()

    # ===== AI EVENTS =====
    # Draw 10 event
    if stats["draws"] >= DRAW_10 and not st.session_state.ai_10_done:
        estrella_header("✨ Estrella ✨  — 10-Draw Check-In")
        if st.button("Run Estrella (10-draw check-in)", use_container_width=True):
            prompt = (
                "Write two short paragraphs reflecting on the first 10 draws.\n"
                f"Vibes counts: {dict(stats['vibe'])}\n"
                f"Zenith count: {stats['zenith']}\n"
                "Tone: supportive, direct, grounded."
            )
            with st.spinner("Estrella is reading the table..."):
                out = ask_ai(prompt)
            st.write(out)

            # Award Careon (+1)
            try:
                bank.award_careon(st.session_state.careon)
            except Exception:
                st.session_state.careon["balance"] = st.session_state.careon.get("balance", 0) + 1
            st.success(f"+1 Ȼ earned! | Balance: {st.session_state.careon.get('balance', 0)}")

            st.session_state.ai_10_done = True

    # Draw 20 event
    if stats["draws"] >= DRAW_20 and not st.session_state.ai_20_done:
        estrella_header("✨ Estrella ✨  — 20-Draw Ratio & Energy Analysis")
        if st.button("Run Estrella (20-draw analysis)", use_container_width=True):
            prompt = (
                "Write two short paragraphs analyzing ratios and energy across 20 draws.\n"
                f"Vibes counts: {dict(stats['vibe'])}\n"
                f"Levels counts: {dict(stats['level'])}\n"
                f"Zenith: {stats['zenith']} (forced {stats['zenith_forced']})\n"
                "Give one practical suggestion for how to draw the next 5 cards deliberately."
            )
            with st.spinner("Estrella is calculating ratios..."):
                out = ask_ai(prompt)
            st.write(out)

            # Award Careon (+1)
            try:
                bank.award_careon(st.session_state.careon)
            except Exception:
                st.session_state.careon["balance"] = st.session_state.careon.get("balance", 0) + 1
            st.success(f"+1 Ȼ earned! | Balance: {st.session_state.careon.get('balance', 0)}")

            st.session_state.ai_20_done = True

    # Final question (after 20 analysis)
    if stats["draws"] >= DRAW_20 and st.session_state.ai_20_done and not st.session_state.final_done:
        st.subheader("Final Question for Estrella")
        fq = st.text_input("Your final question:", key="final_q", placeholder="Ask one precise question…")
        if st.button("Ask Estrella (final 5-part)", use_container_width=True) and fq.strip():
            clean_q = fq.replace(FORCE_ZENITH_SYMBOL, "").strip()
            final_prompt = (
                "Return EXACTLY five lines in this exact format:\n"
                "Intention:\n"
                "Forward action:\n"
                "Past reflection:\n"
                "Energy level:\n"
                "Aspirational message:\n\n"
                f"Session stats: draws={stats['draws']}, vibes={dict(stats['vibe'])}, levels={dict(stats['level'])}, "
                f"zenith={stats['zenith']} forced={stats['zenith_forced']}\n"
                f"Question: {clean_q}"
            )
            with st.spinner("Estrella answers..."):
                out = ask_ai(final_prompt)
            st.code(out, language="text")

            # Award Careon (+1)
            try:
                bank.award_careon(st.session_state.careon)
            except Exception:
                st.session_state.careon["balance"] = st.session_state.careon.get("balance", 0) + 1
            st.success(f"+1 Ȼ earned! | Balance: {st.session_state.careon.get('balance', 0)}")

            # Show final stats (optional)
            try:
                s = bank.get_stats(st.session_state.careon)
                st.info(f"Session complete! Net: {s.get('net', 0):+d} Ȼ | Total rounds: {s.get('rounds', 0)}")
            except Exception:
                pass

            st.session_state.final_done = True

    st.divider()

    # Controls
    st.subheader("Controls")
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("Reset session stats (keep bank)", use_container_width=True):
            st.session_state.stats = {
                "draws": 0,
                "vibe": Counter({"acuity": 0, "valor": 0, "variety": 0}),
                "level": Counter({1: 0, 2: 0, 3: 0}),
                "zenith": 0,
                "zenith_forced": 0,
            }
            st.session_state.last_card = None
            st.session_state.history = []
            st.session_state.ai_10_done = False
            st.session_state.ai_20_done = False
            st.session_state.final_done = False
            st.session_state.round_started = False
            st.session_state.tgif_bypass = False
            st.rerun()

    with col_b:
        if st.button("Hard reset (reload user + bank)", use_container_width=True):
            for k in ["careon", "user", "round_started", "tgif_bypass"]:
                if k in st.session_state:
                    del st.session_state[k]
            st.rerun()

    # Optional: History
    with st.expander("History"):
        if st.session_state.history:
            st.write(st.session_state.history)
        else:
            st.caption("No draws yet.")


if __name__ == "__main__":
    main()
