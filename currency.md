# Currency System

## Careon (₢)

**Symbol:** ₢

**Name:** Careon

# Currency — Starlight Deck

## What Careons Are

Careons (■) are not money. The name comes from "care on" — they represent **attention, intention, and community support**. The goal is not to accumulate them. The goal is to circulate them.

A healthy Starlight Deck economy is one where Careons move — through play, through community contributions, through shared milestones. Hoarding is possible but philosophically misaligned with the experience.

---

## How Careons Flow

### Earning

| Source | Amount | Notes |
|---|---|---|
| Classic Mode (completion) | +3 ■ | Awarded over the course of 20 draws, at checkpoints |
| Rapid Mode (win) | +23 ■ | +20 reward, +3 completion bonus |
| Rapid Mode (loss) | +1 ■ | Failure still teaches something |
| Code Redemption | 95% of code value | The remainder goes to the Network Fund |

### Spending

| Action | Cost | Notes |
|---|---|---|
| Play Classic Mode | 1 ■ | Investment in mindfulness |
| Play Rapid Mode | 5 ■ | A genuine gamble |
| Submit Community Phrase | 100 ■ | Your voice enters the shared space |

### Automatic Outflow

Every code redemption splits: **95% to the user, 5% to the SLD Network Fund.** This is not optional. It is baked into the transaction. The fund is the economy's breathing mechanism — it ensures the collective always grows alongside the individual.

---

## The 95/5 Split

This split is the economic heartbeat of Starlight Deck. It is intentionally small on the community side — most of the value stays with the person who earned it. But over time, across many users and many redemptions, that 5% builds into something meaningful.

**Implementation note:** The split must be calculated server-side (or in a trusted write path). It must be atomic — if the user portion saves but the fund portion fails, the transaction is corrupted. Both writes succeed or neither does.

---

## Economy Health & Known Risks

The review identified two significant imbalances that must be addressed before the economy is considered stable:

**Rapid Mode is currently player-favorable.** At a 5% Zenith rate across 20 pulses, the probability of drawing 2+ Zeniths is roughly 26.4%. The expected payout works out to approximately +2.54 ■ net per play. Over time, this drains the system. Options: reduce the win payout, raise the play cost, or adjust the Zenith threshold for a win.

**Classic Mode has guaranteed positive ROI.** It costs 1 ■ and awards 3 ■ at checkpoints — a 200% return with zero risk. This needs rebalancing. One approach: make the Estrella reflection itself the reward, and reduce or remove the automatic Careon payout.

Both of these are flagged as **pre-launch priorities.**

---

## Validation Rules

All Careon transactions must enforce the following before executing:

- Balance cannot go negative. Spending is rejected if insufficient funds exist.
- Amounts must be positive integers. Negative deposits or zero-value transactions are invalid.
- Code redemption must check whether a code has already been used. Duplicate redemptions are blocked.
- Transactions are logged. Every spend, earn, and split is recorded with a timestamp and context (which mode, which action).

---

## What Careons Are Not

Careons are not a score. They are not a measure of skill or dedication. They are not something to optimize. A user who finishes a session with fewer Careons than they started with has not "lost" — they may have simply participated more fully.
