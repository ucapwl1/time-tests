# test_times.py
import pytest
from times import time_range, compute_overlap_time

def test_time_range_backwards_raises():
    with pytest.raises(ValueError, match="end_time must be after start_time"):
        time_range("2010-01-12 12:00:00", "2010-01-12 10:00:00")

def test_no_overlap():
    a = time_range("2010-01-12 10:00:00", "2010-01-12 10:10:00")
    b = time_range("2010-01-12 10:20:00", "2010-01-12 10:30:00")
    result = compute_overlap_time(a, b)
    assert result == []

def test_multiple_intervals_each():
    a = time_range("2010-01-12 10:00:00", "2010-01-12 10:40:00", number_of_intervals=2, gap_between_intervals_s=0)
    b = time_range("2010-01-12 10:10:00", "2010-01-12 10:50:00", number_of_intervals=2, gap_between_intervals_s=0)
    expected = [
        ("2010-01-12 10:10:00", "2010-01-12 10:20:00"),
        ("2010-01-12 10:20:00", "2010-01-12 10:30:00"),
        ("2010-01-12 10:30:00", "2010-01-12 10:40:00"),
    ]
    assert compute_overlap_time(a, b) == expected

def test_touching_endpoints():
    a = time_range("2010-01-12 10:00:00", "2010-01-12 10:10:00")
    b = time_range("2010-01-12 10:10:00", "2010-01-12 10:20:00")
    assert compute_overlap_time(a, b) == []
