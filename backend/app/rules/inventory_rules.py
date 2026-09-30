from datetime import date, timedelta


def days_until_expiry(expiry: date, today: date | None = None) -> int:
    today = today or date.today()
    return (expiry - today).days


def is_near_expiry(expiry: date, window_days: int = 60, today: date | None = None) -> bool:
    return 0 <= days_until_expiry(expiry, today) <= window_days


def is_expired(expiry: date, today: date | None = None) -> bool:
    return days_until_expiry(expiry, today) < 0


def classify_velocity(quantity: int, low_threshold: int = 20, high_threshold: int = 100) -> str:
    if quantity <= low_threshold:
        return "FAST"
    if quantity >= high_threshold:
        return "SLOW"
    return "MEDIUM"


def needs_cold_chain_alert(cold_chain_flag: bool, requires_cold_chain: bool) -> bool:
    return requires_cold_chain or cold_chain_flag


def suggested_reorder_qty(quantity: int, velocity_tag: str | None) -> int:
    base = max(30, 80 - quantity)
    if velocity_tag == "FAST":
        return base + 40
    if velocity_tag == "SLOW":
        return max(10, base // 2)
    return base


def default_near_expiry_window_end(today: date | None = None) -> date:
    today = today or date.today()
    return today + timedelta(days=60)
