import datetime as dt
import pytest

import src.calculator as calculator


def _patch_today(monkeypatch):
    class FixedDate(dt.date):
        @classmethod
        def today(cls):
            return dt.date(2026, 3, 6)
    # Try patching both common import styles
    monkeypatch.setattr(calculator, 'date', FixedDate, raising=False)
    # In case calculator uses datetime.date, patch that too (best effort)
    monkeypatch.setattr(calculator, 'datetime', dt, raising=False)
    return FixedDate


def test_calculate_days_together_past_returns_tuple(monkeypatch):
    _patch_today(monkeypatch)
    start_date = "2026-03-01"  # 5 days before 2026-03-06
    result = calculator.calculate_days_together(start_date)
    assert isinstance(result, tuple) and len(result) == 3, "Expected a (days, months, years) tuple"
    days, months, years = result
    assert isinstance(days, int) and isinstance(months, int) and isinstance(years, int)
    assert days >= 0 and months >= 0 and years >= 0


def test_calculate_days_together_today_returns_zero_tuple(monkeypatch):
    _patch_today(monkeypatch)
    start_date = "2026-03-06"  # same as frozen today
    result = calculator.calculate_days_together(start_date)
    assert isinstance(result, tuple) and len(result) == 3
    days, months, years = result
    assert days == 0 and months == 0 and years == 0


def test_calculate_days_together_future_returns_zero_tuple(monkeypatch):
    _patch_today(monkeypatch)
    result = calculator.calculate_days_together("2026-03-07")
    assert isinstance(result, tuple) and len(result) == 3
    days, months, years = result
    assert days == 0 and months == 0 and years == 0


def test_calculate_days_together_invalid_format_returns_zero(monkeypatch):
    _patch_today(monkeypatch)
    result = calculator.calculate_days_together("not-a-date")
    assert isinstance(result, tuple) and len(result) == 3
    days, months, years = result
    assert days == 0 and months == 0 and years == 0
