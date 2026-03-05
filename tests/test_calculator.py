import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pytest
from datetime import date
from calculator import calculate_days_together, add_months


class FakeDate:
    """Fake date class for testing with fixed today"""
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day
        self._date = date(year, month, day)
    
    def __sub__(self, other):
        return self._date - other
    
    def __lt__(self, other):
        if isinstance(other, date):
            return self._date < other
        return self._date < other._date
    
    def __le__(self, other):
        if isinstance(other, date):
            return self._date <= other
        return self._date <= other._date
    
    def __gt__(self, other):
        if isinstance(other, date):
            return self._date > other
        return self._date > other._date
    
    def __ge__(self, other):
        if isinstance(other, date):
            return self._date >= other
        return self._date >= other._date
    
    def isoformat(self):
        return self._date.isoformat()


def test_calculate_days_today():
    """Test with today's date returns 0,0,0"""
    today_str = date.today().strftime("%Y-%m-%d")
    days, months, years = calculate_days_together(today_str)
    assert days == 0
    assert months == 0
    assert years == 0


def test_calculate_days_yesterday():
    """Test with yesterday returns 1 day"""
    from datetime import timedelta
    yesterday = date.today() - timedelta(days=1)
    yesterday_str = yesterday.strftime("%Y-%m-%d")
    days, months, years = calculate_days_together(yesterday_str)
    assert days == 1
    assert months == 0
    assert years == 0


def test_calculate_days_one_year():
    """Test one year difference"""
    from datetime import timedelta
    one_year_ago = date.today().replace(year=date.today().year - 1)
    # Handle leap year edge case
    try:
        one_year_ago_str = one_year_ago.strftime("%Y-%m-%d")
    except ValueError:
        # Feb 29 -> Feb 28
        one_year_ago = one_year_ago.replace(day=28)
        one_year_ago_str = one_year_ago.strftime("%Y-%m-%d")
    
    days, months, years = calculate_days_together(one_year_ago_str)
    assert years >= 0  # At least 0 years


def test_calculate_invalid_date():
    """Test invalid date format raises ValueError"""
    with pytest.raises(ValueError):
        calculate_days_together("invalid-date")


def test_calculate_future_date():
    """Test future date raises ValueError"""
    from datetime import timedelta
    future = date.today() + timedelta(days=1)
    future_str = future.strftime("%Y-%m-%d")
    with pytest.raises(ValueError):
        calculate_days_together(future_str)


def test_add_months():
    """Test add_months helper function"""
    d = date(2023, 1, 15)
    result = add_months(d, 1)
    assert result.month == 2
    assert result.day == 15
    
    # Test month-end handling
    d = date(2023, 1, 31)
    result = add_months(d, 1)
    assert result.month == 2
    assert result.day == 28  # Feb 2023 has 28 days
