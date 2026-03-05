from datetime import datetime, date
from typing import Tuple
from dateutil.tz import tzlocal


def calculate_days_together(start_date: str) -> Tuple[int, int, int]:
    """
    Calculate days together from start_date to today.
    
    Args:
        start_date: Date string in YYYY-MM-DD format
        
    Returns:
        Tuple of (days, months, years)
        
    Raises:
        ValueError: If start_date is in the future or invalid format
    """
    try:
        sd = datetime.strptime(start_date, "%Y-%m-%d").date()
    except ValueError as e:
        raise ValueError(f"Invalid date format. Expected YYYY-MM-DD: {e}")
    
    # Get today with timezone awareness
    today = datetime.now(tz=tzlocal()).date()
    
    if sd > today:
        raise ValueError("Start date cannot be in the future")
    
    # Calculate years
    years = today.year - sd.year
    if (today.month, today.day) < (sd.month, sd.day):
        years -= 1
    
    # Calculate months from the base date after years
    base_date = date(today.year - (0 if (today.month, today.day) >= (sd.month, sd.day) else 1), sd.month, sd.day)
    if base_date.day != sd.day:  # Handle month-end adjustments
        # Find last day of the month
        import calendar
        _, last_day = calendar.monthrange(base_date.year, base_date.month)
        base_date = base_date.replace(day=min(sd.day, last_day))
    
    months = 0
    while True:
        next_month = add_months(base_date, 1)
        if next_month > today:
            break
        base_date = next_month
        months += 1
    
    # Calculate remaining days
    days = (today - base_date).days
    
    return days, months, years


def add_months(d: date, months: int) -> date:
    """Safely add months to a date, handling month-end adjustments."""
    import calendar
    
    month = d.month - 1 + months
    year = d.year + month // 12
    month = month % 12 + 1
    
    # Handle day overflow (e.g., Jan 31 + 1 month = Feb 28/29)
    _, last_day = calendar.monthrange(year, month)
    day = min(d.day, last_day)
    
    return date(year, month, day)
