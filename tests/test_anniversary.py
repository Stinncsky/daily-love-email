import sys
import pathlib

tests_dir = pathlib.Path(__file__).resolve().parent
root_dir = tests_dir.parent
src_dir = root_dir / 'src'
sys.path.insert(0, str(src_dir))

import anniversary as anniversary_module


def _fake_today(year=2026, month=3, day=5):
    class FakeDate(anniversary_module.date):
        @classmethod
        def today(cls):
            return cls(year, month, day)
    return FakeDate


def test_next_anniversary_basic(monkeypatch):
    anniversaries = [
        {"name": "Alice", "date": "03-10"},
        {"name": "Bob", "date": "02-28"},
    ]

    FakeDate = _fake_today(2026, 3, 5)
    monkeypatch.setattr(anniversary_module, 'date', FakeDate, raising=True)

    res = anniversary_module.get_next_anniversary(anniversaries)
    assert res is not None
    assert res["name"] == "Alice"
    assert res["date"] == "2026-03-10"
    assert res["days_until"] == 5


def test_next_anniversary_today(monkeypatch):
    anniversaries = [
        {"name": "Today", "date": "03-05"},
        {"name": "Soon", "date": "04-01"},
    ]
    FakeDate = _fake_today(2026, 3, 5)
    monkeypatch.setattr(anniversary_module, 'date', FakeDate, raising=True)

    res = anniversary_module.get_next_anniversary(anniversaries)
    assert res is not None
    assert res["name"] == "Today"
    assert res["date"] == "2026-03-05"
    assert res["days_until"] == 0


def test_next_anniversary_empty():
    res = anniversary_module.get_next_anniversary([])
    assert res is None
