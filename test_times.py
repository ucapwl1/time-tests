# test_times.py
from times import time_range, compute_overlap_time

def test_no_overlap():
    # A finishes at 10:10, B starts at 10:20 → no overlap expected
    a = time_range("2010-01-12 10:00:00", "2010-01-12 10:10:00")
    b = time_range("2010-01-12 10:20:00", "2010-01-12 10:30:00")
    result = compute_overlap_time(a, b)
    expected = []   # requires compute_overlap_time to ignore empty/negative overlaps
    assert result == expected

def test_multiple_intervals_each():
    # A: [10:00–10:20], [10:20–10:40]      (2 intervals, no gaps)
    # B: [10:10–10:30], [10:30–10:50]      (2 intervals, no gaps)
    # Overlaps: [10:10–10:20], [10:20–10:30], [10:30–10:40]
    a = time_range("2010-01-12 10:00:00", "2010-01-12 10:40:00", number_of_intervals=2, gap_between_intervals_s=0)
    b = time_range("2010-01-12 10:10:00", "2010-01-12 10:50:00", number_of_intervals=2, gap_between_intervals_s=0)
    result = compute_overlap_time(a, b)
    expected = [
        ("2010-01-12 10:10:00", "2010-01-12 10:20:00"),
        ("2010-01-12 10:20:00", "2010-01-12 10:30:00"),
        ("2010-01-12 10:30:00", "2010-01-12 10:40:00"),
    ]
    assert result == expected

def test_touching_endpoints():
    # A ends exactly when B starts → empty overlap by convention (half-open)
    a = time_range("2010-01-12 10:00:00", "2010-01-12 10:10:00")
    b = time_range("2010-01-12 10:10:00", "2010-01-12 10:20:00")
    result = compute_overlap_time(a, b)
    expected = []
    assert result == expected