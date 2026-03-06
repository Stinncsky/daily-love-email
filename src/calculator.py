from datetime import datetime, date
import calendar

def calculate_days_together(start_date: str) -> tuple[int, int, int]:
    """Calculate (days, months, years) between start_date and today.

    - days: number of days remaining after removing full months and years
    - months: number of full months after the years
    - years: number of full years

    Accepts ISO format dates (YYYY-MM-DD) or YYYY/MM/DD. If parsing fails or the date
    is in the future, returns (0, 0, 0).
    """
    try:
        # Normalize input to a date object
        if isinstance(start_date, date):
            sd = start_date
        else:
            if isinstance(start_date, str):
                for fmt in ("%Y-%m-%d", "%Y/%m/%d"):
                    try:
                        sd = datetime.strptime(start_date, fmt).date()
                        break
                    except ValueError:
                        continue
                else:
                    return (0, 0, 0)
            else:
                return (0, 0, 0)
        today = date.today()
        if sd > today:
            return (0, 0, 0)

        def add_month(dt: date, months: int = 1) -> date:
            year = dt.year + (dt.month + months - 1) // 12
            month = (dt.month + months - 1) % 12 + 1
            day = min(dt.day, calendar.monthrange(year, month)[1])
            return date(year, month, day)

        cur = sd
        total_months = 0
        while add_month(cur, 1) <= today:
            cur = add_month(cur, 1)
            total_months += 1

        years = total_months // 12
        months = total_months % 12
        days = (today - cur).days
        return (days, months, years)
    except Exception:
        return (0, 0, 0)
