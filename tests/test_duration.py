from datetime import datetime

import pytest

from cvforge import duration
from cvforge.config import Config


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("June 2018 - September 2021", "(3 years 3 months)"),
        ("January 2020 - January 2021", "(1 year)"),
        ("March 2024 - April 2024", "(1 month)"),
        ("March 2024 - May 2024", "(2 months)"),
        ("2016 - 2018", "(2 years)"),
        ("June 2018 – December 2019", "(1 year 6 months)"),
        ("March 2024 - March 2024", "(less than 1 month)"),
    ],
)
def test_calculate_duration(text, expected):
    assert duration.calculate_duration(text) == expected


@pytest.mark.parametrize("text", ["", "Present", "2020", "a - b - c", "not a date - nope"])
def test_unparseable_ranges_return_empty(text):
    assert duration.calculate_duration(text) == ""


def test_present_counts_to_today(monkeypatch):
    class FixedDatetime(datetime):
        @classmethod
        def now(cls, tz=None):
            return cls(2025, 3, 15)

    monkeypatch.setattr(duration, "datetime", FixedDatetime)
    assert duration.calculate_duration("January 2020 - Present") == "(5 years 2 months)"
    assert duration.calculate_duration("January 2025 - Current") == "(2 months)"


def test_disabled_by_config(monkeypatch):
    monkeypatch.setattr(Config, "CALCULATE_DURATIONS", False)
    assert duration.calculate_duration("June 2018 - September 2021") == ""


def test_dateutil_missing(monkeypatch):
    monkeypatch.setattr(duration, "DATEUTIL_AVAILABLE", False)
    assert duration.calculate_duration("June 2018 - September 2021") == ""
    assert duration.is_dateutil_available() is False
