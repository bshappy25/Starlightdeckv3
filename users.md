# Users — Starlight Deck

## Identity & Persistence

Each user is identified by a **username** set at session start. Currently, usernames live only in `st.session_state` — closing the tab means losing your identity entirely. A persistent user store (SQLite or equivalent) is required before launch so that balances, history, and VIP status survive across sessions.

---

## VIP Tiers

VIP status is a reflection of engagement, not rank. There are no leaderboards, no public standings. Tiers are personal milestones — quiet acknowledgments that a user has been showing up.

| Tier | Careon Threshold | Meaning |
|---|---|---|
| Stargazer | 0–99 ■ | Just arriving. Curiosity is enough. |
| Constellation | 100–499 ■ | A practice is forming. |
| Nebula | 500–999 ■ | Deep and sustained engagement. |
| Supernova | 1,000+ ■ | A cosmic veteran. The journey is the point. |

Tiers update automatically based on current balance. They are **not** locked in — if a balance drops, the tier reflects that honestly.

---

## Community Participation

Users can participate in the collective in two ways:

**SLD Network Fund** — A shared pool that grows passively. Every time a user redeems a code, 5% of the value flows into the fund automatically. When the fund hits milestones (e.g. 1,000 ■), everyone benefits. No individual is credited. No one "wins" it.

**Community Phrases (The Ticker)** — For 100 ■, any user can submit a phrase (max 20 characters) that scrolls across the top of the experience. This is collective expression, not advertising. The cost exists because the phrase has real weight — it becomes part of the shared space.

---

## Estrella & the User

Estrella is not a feature users "unlock." She is a reflective companion who appears at specific, meaningful points in a user's session — never randomly, never on demand (outside of the final Classic Mode question). A user does not interact with Estrella so much as *receive* her when the moment is right.

Estrella's appearances are tied to **session milestones**, not user tiers or history. Every user gets the same touchpoints regardless of how long they've been playing.

---

## What a User Is Not

A user is not a player in a competitive sense. There is no head-to-head, no leaderboard, no "best" user. The entire system is designed so that users exist in relation to *their own* journey and to the *collective* — never to each other as opponents.
