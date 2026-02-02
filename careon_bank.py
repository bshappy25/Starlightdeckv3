# careon_bank.py
import json
import os
from datetime import datetime, date

BANK_PATH = "careon_bank_v2.json"

# Economy tuning knobs (easy to change)
DAILY_BONUS = 10
ROUND_COST = 1
AWARD_PER_EVENT = 1


def _today_str() -> str:
    # Use local date (fine for a game). Switch to UTC if you want.
    return date.today().isoformat()


def _now_iso() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def _read_json(path: str, default: dict) -> dict:
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def _write_json(path: str, data: dict) -> None:
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp, path)


def _default_bank() -> dict:
    return {
        "balance": 0,
        "total_earned": 0,
        "total_spent": 0,
        "rounds": 0,
        "last_bonus_date": None,
        "history": [],  # list of transactions
        "updated_at": _now_iso(),
        "created_at": _now_iso(),
    }


def save_bank(careon: dict, path: str = BANK_PATH) -> None:
    careon["updated_at"] = _now_iso()
    _write_json(path, careon)


def load_bank(path: str = BANK_PATH) -> dict:
    careon = _read_json(path, _default_bank())

    # Ensure required keys exist (future-proof)
    for k, v in _default_bank().items():
        careon.setdefault(k, v)

    return careon


def _add_tx(careon: dict, kind: str, amount: int, note: str = "") -> None:
    careon["history"].append({
        "ts": _now_iso(),
        "kind": kind,
        "amount": int(amount),
        "note": note
    })


def display_balance(balance: int) -> str:
    # purely cosmetic
    return f"Balance: {balance} Ȼ"


def check_daily_bonus(careon: dict, path: str = BANK_PATH) -> bool:
    """
    Adds DAILY_BONUS once per calendar day.
    Returns True if bonus was applied.
    """
    today = _today_str()
    if careon.get("last_bonus_date") == today:
        return False

    careon["balance"] = int(careon.get("balance", 0)) + DAILY_BONUS
    careon["total_earned"] = int(careon.get("total_earned", 0)) + DAILY_BONUS
    careon["last_bonus_date"] = today
    _add_tx(careon, "bonus", DAILY_BONUS, "Daily login bonus")
    save_bank(careon, path)
    return True


def can_start_round(balance: int) -> bool:
    return int(balance) >= ROUND_COST


def charge_round(careon: dict, path: str = BANK_PATH) -> None:
    """
    Charges ROUND_COST and increments rounds.
    Raises ValueError if insufficient balance.
    """
    bal = int(careon.get("balance", 0))
    if bal < ROUND_COST:
        raise ValueError("Insufficient balance to start round")

    careon["balance"] = bal - ROUND_COST
    careon["total_spent"] = int(careon.get("total_spent", 0)) + ROUND_COST
    careon["rounds"] = int(careon.get("rounds", 0)) + 1
    _add_tx(careon, "round", -ROUND_COST, "Start round")
    save_bank(careon, path)


def award_careon(careon: dict, path: str = BANK_PATH, amount: int = AWARD_PER_EVENT, note: str = "Session reward") -> None:
    """
    Adds Careons (default +1) for completing milestones.
    """
    amt = int(amount)
    careon["balance"] = int(careon.get("balance", 0)) + amt
    careon["total_earned"] = int(careon.get("total_earned", 0)) + amt
    _add_tx(careon, "award", amt, note)
    save_bank(careon, path)


def spend(careon: dict, amount: int, path: str = BANK_PATH, note: str = "Spend") -> None:
    """
    Optional utility if you add a shop later.
    """
    amt = int(amount)
    bal = int(careon.get("balance", 0))
    if amt <= 0:
        raise ValueError("Amount must be positive")
    if bal < amt:
        raise ValueError("Insufficient balance")

    careon["balance"] = bal - amt
    careon["total_spent"] = int(careon.get("total_spent", 0)) + amt
    _add_tx(careon, "spend", -amt, note)
    save_bank(careon, path)


def deposit(careon: dict, amount: int, path: str = BANK_PATH, note: str = "Deposit") -> None:
    """
    Optional utility.
    """
    amt = int(amount)
    if amt <= 0:
        raise ValueError("Amount must be positive")

    careon["balance"] = int(careon.get("balance", 0)) + amt
    careon["total_earned"] = int(careon.get("total_earned", 0)) + amt
    _add_tx(careon, "deposit", amt, note)
    save_bank(careon, path)


def recent_txs(careon: dict, n: int = 10) -> list:
    hist = careon.get("history", [])
    return list(reversed(hist[-n:]))


def get_stats(careon: dict) -> dict:
    earned = int(careon.get("total_earned", 0))
    spent = int(careon.get("total_spent", 0))
    return {
        "balance": int(careon.get("balance", 0)),
        "earned": earned,
        "spent": spent,
        "net": earned - spent,
        "rounds": int(careon.get("rounds", 0)),
        "last_bonus_date": careon.get("last_bonus_date"),
    }

"sld_network_fund": 0,
"used_deposit_codes": [],
