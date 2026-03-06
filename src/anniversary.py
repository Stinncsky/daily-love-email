from datetime import date
from typing import List, Dict, Optional


def get_next_anniversary(anniversaries: List[Dict]) -> Optional[Dict]:
    """
    Find the next upcoming anniversary.

    Args:
        anniversaries: List of dicts with 'name' and 'date' (MM-DD format)
        - Example: {'name': 'Mom Birthday', 'date': '05-12'}
        - Date is monthly-day only; anniversaries recur yearly.
        - If multiple anniversaries occur on the same future day, the one with the
          smallest days_until is preferred.
    Returns:
        Dict with 'name', 'date' (YYYY-MM-DD) and 'days_until', or None if list is empty/invalid.
    """
    if not anniversaries:
        return None

    today = date.today()

    best: Optional[Dict] = None
    best_days: Optional[int] = None

    for item in anniversaries:
        name = item.get("name")
        mmdd = item.get("date")
        if not name or not mmdd:
            continue
        try:
            month_str, day_str = mmdd.split("-")
            month = int(month_str)
            day = int(day_str)
        except Exception:
            # skip invalid date formats
            continue

        try:
            year = today.year
            next_date = date(year, month, day)
        except Exception:
            # invalid month/day values
            continue

        # If already passed this year, move to next year (recurring yearly)
        if next_date < today:
            try:
                next_date = date(year + 1, month, day)
            except Exception:
                continue

        days_until = (next_date - today).days

        candidate = {
            "name": name,
            "date": next_date.isoformat(),
            "days_until": days_until,
        }

        if best is None or days_until < best_days:
            best = candidate
            best_days = days_until
        elif days_until == best_days:
            # tie-breaker: pick the earlier next_date for determinism
            if date.fromisoformat(candidate["date"]) < date.fromisoformat(best["date"]):
                best = candidate
                best_days = days_until

    return best
